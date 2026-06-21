-- BNC INBOUND CLASSIFICATION VIEW — foundation for all BNC-specific payer analysis.
-- Tags every BNC inbound row with: txn_type, payer identity (prefix/number/name/account),
-- is_individual, is_intrabank_bnc, and a canonical counterparty_key for dedupe/rollup.
--
-- Use this file as the base. Q3a (individual-payer rollup) and Q3b (biz-to-biz intrabank rollup)
-- duplicate the CTE so each file is self-contained.
--
-- Scope: BNC (Banco Nacional de Crédito), VES, Q1 2026, inbound (amount > 0), non-discarded.
-- NOTE: tt.reference_code — adjust column name if your schema calls it something else
--       (e.g. external_reference_id). Matches the field we saw in the Q3 xlsx export.

WITH bnc_inbound AS (
  SELECT
    w.id                                 AS workspace_id,
    w.name                               AS workspace,
    tt.id,
    tt.transaction_date,
    tt.amount_cents / 100.0              AS amount_ves,
    tt.description,
    tt.reference_code
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  JOIN workspaces w                           ON w.id = ta.workspace_id AND w.discarded_at IS NULL
  WHERE tt.discarded_at IS NULL
    AND tt.amount_cents > 0
    AND tt.amount_currency = 'VES'
    AND b.name ILIKE 'BNC'
    AND tt.transaction_date >= '2026-01-01'
    AND tt.transaction_date <  '2026-04-01'
    AND tt.description IS NOT NULL
    AND tt.description <> ''
),
extracted AS (
  SELECT
    *,
    -- Transaction type (priority ordering: Intrabank > CrediInmediato > PagoMovil > POS > Other)
    CASE
      WHEN description ~* 'TRANSFERENCIA RECIBIDA DEL BCO\.? NACIONAL DE CREDITO' THEN 'Intrabank'
      WHEN description ~* 'Credito Inmediato Recibido|CIPOTR|EMISOR\s*:'          THEN 'CrediInmediato'
      WHEN description ~* 'Abono Pago Movil BNC|^PMPC'                            THEN 'PagoMovil'
      WHEN description ~* '^POS:|Abono Comercio por Tarjeta'                      THEN 'POS'
      ELSE 'Other'
    END                                                                            AS txn_type,

    -- Intrabank flag (sender account is also on BNC — the biz-biz unlock)
    (description ~* 'TRANSFERENCIA RECIBIDA DEL BCO\.? NACIONAL DE CREDITO')       AS is_intrabank_bnc,

    -- Prefix letter from Intrabank pattern: "A NOMBRE DE: V-012345678 NAME..."
    UPPER(substring(description from '(?i)A NOMBRE DE:\s*([VEJGP])[-\s]'))         AS payer_prefix,

    -- Cedula/RIF digits from Intrabank pattern (strip leading zeros; caller LPADs)
    substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?0*([0-9]{6,10})')  AS payer_number_raw,

    -- Payer name from Intrabank pattern — between ID and "DE LA CUENTA"
    TRIM(substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?[0-9]+\s+(.+?)\s+DE LA CUENTA'))
                                                                                   AS payer_name_intrabank,

    -- Payer name from CrediInmediato pattern — between "EMISOR :" and " - "
    TRIM(substring(description from '(?i)EMISOR\s*:\s*(.+?)\s*-\s*'))              AS payer_name_credi,

    -- Rare PMPC cedula pattern ("c i 1234567")
    substring(description from '(?i)\mc\s*i\s+([0-9]{6,10})')                      AS payer_cedula_pmpc,

    -- Sender's BNC account number (Intrabank only)
    substring(description from '(?i)DE LA CUENTA NRO\.?\s*([0-9]+)')               AS payer_account
  FROM bnc_inbound
),
classified AS (
  SELECT
    *,
    -- Best-available payer name (prefer Intrabank, else CrediInmediato)
    COALESCE(payer_name_intrabank, payer_name_credi)                               AS payer_name,

    -- Canonical payer ID: "<PREFIX>-<9-digit-padded-number>" when we have prefix + number
    CASE
      WHEN payer_prefix IS NOT NULL AND payer_number_raw IS NOT NULL
        THEN payer_prefix || '-' || LPAD(payer_number_raw, 9, '0')
      WHEN payer_cedula_pmpc IS NOT NULL
        THEN 'V-' || LPAD(payer_cedula_pmpc, 9, '0')
      ELSE NULL
    END                                                                            AS payer_id_canonical,

    -- Identity type label (V/E = individual, J/G = legal, N = name-only, X = none)
    CASE
      WHEN payer_prefix IN ('V','E')                                 THEN 'V_or_E_cedula'
      WHEN payer_prefix = 'J'                                        THEN 'J_RIF'
      WHEN payer_prefix = 'G'                                        THEN 'G_gov'
      WHEN payer_cedula_pmpc IS NOT NULL                             THEN 'V_or_E_cedula'
      WHEN COALESCE(payer_name_intrabank, payer_name_credi) IS NOT NULL THEN 'name_only'
      ELSE 'none'
    END                                                                            AS payer_id_type,

    -- Individual flag (TRUE = natural person, FALSE = legal entity, NULL = unknown)
    CASE
      WHEN payer_prefix IN ('V','E')                                 THEN TRUE
      WHEN payer_prefix IN ('J','G')                                 THEN FALSE
      WHEN payer_cedula_pmpc IS NOT NULL                             THEN TRUE
      ELSE NULL
    END                                                                            AS is_individual
  FROM extracted
),
final_view AS (
  SELECT
    id,
    workspace_id,
    workspace,
    transaction_date,
    amount_ves,
    txn_type,
    is_intrabank_bnc,
    payer_id_type,
    payer_id_canonical,
    payer_name,
    payer_account,
    is_individual,
    -- Dedupe key: canonical ID if present, else normalized name, else NULL
    COALESCE(
      payer_id_canonical,
      CASE
        WHEN payer_name_intrabank IS NOT NULL OR payer_name_credi IS NOT NULL
          THEN 'NAME:' || UPPER(regexp_replace(TRIM(COALESCE(payer_name_intrabank, payer_name_credi)), '\s+', ' ', 'g'))
        ELSE NULL
      END
    )                                                                              AS counterparty_key,
    description,
    reference_code
  FROM classified
)

-- ====== PREVIEW: per-workspace × txn_type × id_type rollup (sanity check) ======
SELECT
  workspace,
  txn_type,
  payer_id_type,
  COUNT(*)                                             AS tx_count,
  ROUND(SUM(amount_ves)::numeric, 0)                   AS ves_volume,
  COUNT(DISTINCT counterparty_key)
    FILTER (WHERE counterparty_key IS NOT NULL)        AS unique_counterparties
FROM final_view
GROUP BY workspace, txn_type, payer_id_type
ORDER BY workspace, ves_volume DESC NULLS LAST
