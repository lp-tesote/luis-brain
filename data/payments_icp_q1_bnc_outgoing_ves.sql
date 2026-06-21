-- PAYMENTS ICP — Query 1: BNC outgoing VES by workspace, monthly Jan/Feb/Mar 2026.
-- Purpose: identify Tesote customers who are sending meaningful VES volume out of BNC accounts today.
-- Signal for Track C (Send via BNC APIs) of the Payments execution plan.
--
-- Output columns:
--   workspace                — workspace name
--   bnc_active_accounts      — distinct active BNC accounts in the workspace
--   txn_count_jan/feb/mar    — number of outgoing BNC VES transactions per month
--   ves_outflow_jan/feb/mar  — raw VES outflow per month
--   usd_outflow_jan/feb/mar  — VES ÷ 550 (avg Q1 2026 rate per Luis)
--   usd_outflow_total_q1     — Q1 total in USD equivalent
--   txn_count_total_q1       — Q1 total transaction count
--
-- Notes:
--  - "Active BNC account" = tesote_accounts joined to banks.name='BNC', not discarded, not archived, syncable=true.
--  - Outflows = amount_cents < 0, currency = VES.
--  - Uses transaction_date (not created_at) for the monthly bucket — matches the schema convention.
--  - Workspaces with zero Q1 outflow but ≥1 active BNC account are still included (they might start moving volume).

WITH bnc_accounts AS (
  SELECT
    ta.id           AS account_id,
    ta.workspace_id
  FROM tesote_accounts ta
  JOIN external_service_bank_connections esbc
    ON ta.external_service_bank_connection_id = esbc.id
  JOIN banks b ON esbc.bank_id = b.id AND b.name = 'BNC'
  WHERE ta.discarded_at IS NULL
    AND (ta.archived = false OR ta.archived IS NULL)
    AND ta.syncable = true
    AND esbc.discarded_at IS NULL
),
bnc_accounts_by_workspace AS (
  SELECT workspace_id, COUNT(DISTINCT account_id) AS bnc_active_accounts
  FROM bnc_accounts
  GROUP BY workspace_id
),
monthly_outflows AS (
  SELECT
    ba.workspace_id,
    DATE_TRUNC('month', tt.transaction_date)::date AS month,
    SUM(ABS(tt.amount_cents) / 100.0) AS outflow_ves,
    COUNT(*)                          AS txn_count
  FROM tesote_transactions tt
  JOIN bnc_accounts ba ON ba.account_id = tt.tesote_account_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_cents < 0
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= '2026-01-01'
    AND tt.transaction_date <  '2026-04-01'
  GROUP BY ba.workspace_id, DATE_TRUNC('month', tt.transaction_date)
),
pivoted AS (
  SELECT
    workspace_id,
    SUM(CASE WHEN month = DATE '2026-01-01' THEN outflow_ves ELSE 0 END) AS ves_jan,
    SUM(CASE WHEN month = DATE '2026-02-01' THEN outflow_ves ELSE 0 END) AS ves_feb,
    SUM(CASE WHEN month = DATE '2026-03-01' THEN outflow_ves ELSE 0 END) AS ves_mar,
    SUM(CASE WHEN month = DATE '2026-01-01' THEN txn_count   ELSE 0 END) AS cnt_jan,
    SUM(CASE WHEN month = DATE '2026-02-01' THEN txn_count   ELSE 0 END) AS cnt_feb,
    SUM(CASE WHEN month = DATE '2026-03-01' THEN txn_count   ELSE 0 END) AS cnt_mar
  FROM monthly_outflows
  GROUP BY workspace_id
)
SELECT
  w.name                                                                            AS workspace,
  COALESCE(b.bnc_active_accounts, 0)                                                AS bnc_active_accounts,
  COALESCE(p.cnt_jan, 0)                                                            AS txn_count_jan,
  COALESCE(p.cnt_feb, 0)                                                            AS txn_count_feb,
  COALESCE(p.cnt_mar, 0)                                                            AS txn_count_mar,
  COALESCE(p.cnt_jan, 0) + COALESCE(p.cnt_feb, 0) + COALESCE(p.cnt_mar, 0)          AS txn_count_total_q1,
  ROUND(COALESCE(p.ves_jan, 0), 2)                                                  AS ves_outflow_jan,
  ROUND(COALESCE(p.ves_feb, 0), 2)                                                  AS ves_outflow_feb,
  ROUND(COALESCE(p.ves_mar, 0), 2)                                                  AS ves_outflow_mar,
  ROUND(COALESCE(p.ves_jan, 0) / 550.0, 2)                                          AS usd_outflow_jan,
  ROUND(COALESCE(p.ves_feb, 0) / 550.0, 2)                                          AS usd_outflow_feb,
  ROUND(COALESCE(p.ves_mar, 0) / 550.0, 2)                                          AS usd_outflow_mar,
  ROUND((COALESCE(p.ves_jan, 0) + COALESCE(p.ves_feb, 0) + COALESCE(p.ves_mar, 0)) / 550.0, 2) AS usd_outflow_total_q1
FROM workspaces w
JOIN bnc_accounts_by_workspace b ON b.workspace_id = w.id
LEFT JOIN pivoted p               ON p.workspace_id = w.id
WHERE w.discarded_at IS NULL
ORDER BY usd_outflow_total_q1 DESC NULLS LAST, workspace;
