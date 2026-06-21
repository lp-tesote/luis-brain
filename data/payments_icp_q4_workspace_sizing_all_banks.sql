-- Q4 — WORKSPACE SIZING (all banks, inbound + outbound, with BNC share)
-- Goal: see the raw size of each workspace's money movement in Q1 2026, irrespective of ICP
-- filters. Helps prioritize by actual business size — some workspaces may be more interesting
-- for outbound (Seg 2) than inbound (Seg 1), or vice versa.
--
-- Scope: VES currency, Q1 2026, non-discarded transactions on active accounts.
-- Inbound = amount_cents > 0, Outbound = amount_cents < 0 (using sign convention).
-- USD at 550 VES/USD throughout.
-- BNC matched via b.name ILIKE 'BNC' — adjust if schema uses different name.

WITH base AS (
  SELECT
    w.id                                          AS workspace_id,
    w.name                                        AS workspace,
    b.name                                        AS bank,
    tt.amount_cents / 100.0                       AS amount_ves,
    CASE WHEN tt.amount_cents > 0 THEN 'in' ELSE 'out' END AS direction,
    (b.name ILIKE 'BNC')                          AS is_bnc
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  JOIN workspaces w                           ON w.id = ta.workspace_id AND w.discarded_at IS NULL
  WHERE tt.discarded_at IS NULL
    AND tt.amount_cents <> 0
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= '2026-01-01'
    AND tt.transaction_date <  '2026-04-01'
),
agg AS (
  SELECT
    workspace,

    -- Totals (absolute value so volumes are positive)
    COUNT(*)                                                                   AS total_tx,
    SUM(ABS(amount_ves))                                                       AS total_ves,
    COUNT(DISTINCT bank)                                                       AS active_banks,

    -- Inbound
    COUNT(*)               FILTER (WHERE direction = 'in')                     AS in_tx,
    SUM(ABS(amount_ves))   FILTER (WHERE direction = 'in')                     AS in_ves,

    -- Outbound
    COUNT(*)               FILTER (WHERE direction = 'out')                    AS out_tx,
    SUM(ABS(amount_ves))   FILTER (WHERE direction = 'out')                    AS out_ves,

    -- BNC inbound
    COUNT(*)               FILTER (WHERE direction = 'in'  AND is_bnc)         AS bnc_in_tx,
    SUM(ABS(amount_ves))   FILTER (WHERE direction = 'in'  AND is_bnc)         AS bnc_in_ves,

    -- BNC outbound
    COUNT(*)               FILTER (WHERE direction = 'out' AND is_bnc)         AS bnc_out_tx,
    SUM(ABS(amount_ves))   FILTER (WHERE direction = 'out' AND is_bnc)         AS bnc_out_ves
  FROM base
  GROUP BY workspace
)
SELECT
  workspace,
  total_tx,
  ROUND(total_ves::numeric, 0)                                                 AS total_ves,
  ROUND((total_ves / 550.0)::numeric, 0)                                       AS total_usd,
  active_banks,

  -- Inbound breakdown
  in_tx,
  ROUND(in_ves::numeric, 0)                                                    AS in_ves,
  ROUND((in_ves / 550.0)::numeric, 0)                                          AS in_usd,

  -- Outbound breakdown
  out_tx,
  ROUND(out_ves::numeric, 0)                                                   AS out_ves,
  ROUND((out_ves / 550.0)::numeric, 0)                                         AS out_usd,

  -- BNC inbound share
  bnc_in_tx,
  ROUND(bnc_in_ves::numeric, 0)                                                AS bnc_in_ves,
  ROUND((bnc_in_ves / 550.0)::numeric, 0)                                      AS bnc_in_usd,
  ROUND((bnc_in_ves / NULLIF(in_ves, 0) * 100)::numeric, 1)                    AS bnc_in_pct,

  -- BNC outbound share
  bnc_out_tx,
  ROUND(bnc_out_ves::numeric, 0)                                               AS bnc_out_ves,
  ROUND((bnc_out_ves / 550.0)::numeric, 0)                                     AS bnc_out_usd,
  ROUND((bnc_out_ves / NULLIF(out_ves, 0) * 100)::numeric, 1)                  AS bnc_out_pct,

  -- BNC overall share
  ROUND(((bnc_in_ves + bnc_out_ves) / NULLIF(total_ves, 0) * 100)::numeric, 1) AS bnc_overall_pct
FROM agg
WHERE total_tx >= 25
ORDER BY total_ves DESC NULLS LAST
LIMIT 500
