-- Q3b — BNC BIZ-TO-BIZ INTRABANK ROLLUP (Segment 3)
-- Workspaces ranked by inbound from legal entities (J-prefix RIF) on BNC, intrabank only.
-- These are the biz-biz prospects where Tesote's collection / direct-debit motion
-- can work WITHOUT the gated interbank ACH rail — because sender and receiver are
-- both on BNC, money moves intrabank.
--
-- Output per workspace: total J-sender tx + volume, unique J-counterparty count, top-10 concentration.

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
    (description ~* 'TRANSFERENCIA RECIBIDA DEL BCO\.? NACIONAL DE CREDITO')       AS is_intrabank_bnc,
    UPPER(substring(description from '(?i)A NOMBRE DE:\s*([VEJGP])[-\s]'))         AS payer_prefix,
    substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?0*([0-9]{6,10})')  AS payer_number_raw,
    TRIM(substring(description from '(?i)A NOMBRE DE:\s*[VEJGP][-\s]?[0-9]+\s+(.+?)\s+DE LA CUENTA'))
                                                                                   AS payer_name_intrabank,
    substring(description from '(?i)DE LA CUENTA NRO\.?\s*([0-9]+)')               AS payer_account
  FROM bnc_inbound
),
j_intrabank AS (
  -- Only intrabank-BNC J-prefix rows (biz-to-biz, same bank)
  SELECT
    workspace_id,
    workspace,
    amount_ves,
    payer_name_intrabank                                                           AS payer_name,
    payer_account,
    payer_prefix || '-' || LPAD(payer_number_raw, 9, '0')                          AS payer_rif
  FROM extracted
  WHERE is_intrabank_bnc = TRUE
    AND payer_prefix = 'J'
    AND payer_number_raw IS NOT NULL
),
per_counterparty AS (
  SELECT
    workspace_id,
    workspace,
    payer_rif,
    MAX(payer_name)                             AS payer_name,
    COUNT(*)                                    AS cp_tx_count,
    SUM(amount_ves)                             AS cp_ves
  FROM j_intrabank
  GROUP BY workspace_id, workspace, payer_rif
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY workspace_id ORDER BY cp_ves DESC) AS rn_in_workspace
  FROM per_counterparty
),
top10 AS (
  SELECT workspace_id, SUM(cp_ves) AS top10_ves
  FROM ranked
  WHERE rn_in_workspace <= 10
  GROUP BY workspace_id
),
ws_rollup AS (
  SELECT
    workspace_id,
    workspace,
    SUM(cp_tx_count)                                           AS j_tx_count,
    SUM(cp_ves)                                                AS j_ves_total,
    COUNT(DISTINCT payer_rif)                                  AS unique_j_counterparties
  FROM per_counterparty
  GROUP BY workspace_id, workspace
)
SELECT
  w.workspace,
  w.j_tx_count,
  ROUND(w.j_ves_total::numeric, 0)                             AS j_ves_total,
  ROUND((w.j_ves_total / 550.0)::numeric, 0)                   AS j_usd_total,
  w.unique_j_counterparties,
  ROUND((w.j_ves_total::numeric / NULLIF(w.j_tx_count,0)), 0)  AS avg_ticket_ves,
  ROUND((t.top10_ves / NULLIF(w.j_ves_total, 0) * 100)::numeric, 1)
                                                               AS top10_concentration_pct
FROM ws_rollup w
LEFT JOIN top10 t USING (workspace_id)
WHERE w.unique_j_counterparties >= 3
ORDER BY w.j_ves_total DESC NULLS LAST
