-- Q3a — BNC INDIVIDUAL-PAYER ROLLUP (augments Segment 1)
-- Workspaces ranked by BNC inbound from individual payers (V/E cedula).
-- Uses the Q3 classification CTE (duplicated below so file is self-contained).
--
-- Two outputs merged: tx count + volume per workspace + unique-individual-cedula count.

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
    CASE
      WHEN description ~* 'TRANSFERENCIA RECIBIDA DEL BCO\.? NACIONAL DE CREDITO' THEN 'Intrabank'
      WHEN description ~* 'Credito Inmediato Recibido|CIPOTR|EMISOR\s*:'          THEN 'CrediInmediato'
      WHEN description ~* 'Abono Pago Movil BNC|^PMPC'                            THEN 'PagoMovil'
      WHEN description ~* '^POS:|Abono Comercio por Tarjeta'                      THEN 'POS'
      ELSE 'Other'
    END                                                                            AS txn_type,
    (description ~* 'TRANSFERENCIA RECIBIDA DEL BCO\.? NACIONAL DE CREDITO')       AS is_intrabank_bnc,
    UPPER(substring(description from '(?i)A NOMBRE DE:\s*([VEJGP])[-\s]'))         AS payer_prefix,
    substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?0*([0-9]{6,10})')  AS payer_number_raw,
    TRIM(substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?[0-9]+\s+(.+?)\s+DE LA CUENTA'))
                                                                                   AS payer_name_intrabank,
    TRIM(substring(description from '(?i)EMISOR\s*:\s*(.+?)\s*-\s*'))              AS payer_name_credi,
    substring(description from '(?i)\mc\s*i\s+([0-9]{6,10})')                      AS payer_cedula_pmpc
  FROM bnc_inbound
),
classified AS (
  SELECT
    *,
    CASE
      WHEN payer_prefix IS NOT NULL AND payer_number_raw IS NOT NULL
        THEN payer_prefix || '-' || LPAD(payer_number_raw, 9, '0')
      WHEN payer_cedula_pmpc IS NOT NULL
        THEN 'V-' || LPAD(payer_cedula_pmpc, 9, '0')
      ELSE NULL
    END                                                                            AS payer_id_canonical,
    CASE
      WHEN payer_prefix IN ('V','E')                                 THEN TRUE
      WHEN payer_prefix IN ('J','G')                                 THEN FALSE
      WHEN payer_cedula_pmpc IS NOT NULL                             THEN TRUE
      ELSE NULL
    END                                                                            AS is_individual,
    COALESCE(
      CASE
        WHEN payer_prefix IS NOT NULL AND payer_number_raw IS NOT NULL
          THEN payer_prefix || '-' || LPAD(payer_number_raw, 9, '0')
        WHEN payer_cedula_pmpc IS NOT NULL
          THEN 'V-' || LPAD(payer_cedula_pmpc, 9, '0')
        ELSE NULL
      END,
      CASE
        WHEN payer_name_intrabank IS NOT NULL OR payer_name_credi IS NOT NULL
          THEN 'NAME:' || UPPER(regexp_replace(TRIM(COALESCE(payer_name_intrabank, payer_name_credi)), '\s+', ' ', 'g'))
        ELSE NULL
      END
    )                                                                              AS counterparty_key
  FROM extracted
),
individual_rows AS (
  SELECT *
  FROM classified
  WHERE is_individual = TRUE
),
rollup AS (
  SELECT
    workspace,
    COUNT(*)                                                  AS individual_tx_count,
    ROUND(SUM(amount_ves)::numeric, 0)                        AS individual_ves,
    COUNT(DISTINCT counterparty_key)                          AS unique_individuals,
    COUNT(*) FILTER (WHERE is_intrabank_bnc)                  AS intrabank_tx,
    ROUND(SUM(amount_ves) FILTER (WHERE is_intrabank_bnc)::numeric, 0)
                                                              AS intrabank_ves,
    COUNT(*) FILTER (WHERE NOT is_intrabank_bnc)              AS interbank_tx,
    ROUND(SUM(amount_ves) FILTER (WHERE NOT is_intrabank_bnc)::numeric, 0)
                                                              AS interbank_ves
  FROM individual_rows
  GROUP BY workspace
)
SELECT
  workspace,
  individual_tx_count,
  individual_ves,
  ROUND((individual_ves / 550.0)::numeric, 0)                 AS individual_usd,
  unique_individuals,
  ROUND((individual_ves::numeric / NULLIF(individual_tx_count,0)), 0)
                                                              AS avg_ticket_ves,
  intrabank_tx,
  intrabank_ves,
  interbank_tx,
  interbank_ves
FROM rollup
WHERE individual_tx_count >= 10
ORDER BY individual_ves DESC NULLS LAST
