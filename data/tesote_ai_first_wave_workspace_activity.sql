-- Tesote AI first-wave — rank workspaces by 30-day engagement
-- Goal: pick 2-3 design-partner / first-customer candidates for the AI surface.
-- Signal of "engaged customer" = active sync + transactions flowing + the user
-- is doing the manual work (categorizing, attaching counterparties) that the AI
-- would replace.
--
-- Window: last 30 days (parameterizable below).
--
-- Output columns:
--   live_accounts          -- non-discarded, non-archived, syncable, non-manual accounts
--   sync_sessions_30d      -- all bank_sync_sessions in the window
--   sync_completed_30d     -- of those, status='completed'
--   sync_failed_30d        -- of those, status='failed'
--   last_sync_at           -- most recent bank_sync_session.created_at
--   txn_count_30d          -- live transactions in the window (positive activity floor)
--   txn_categorized_30d    -- distinct txns with at least one join_transaction_categories row
--   pct_categorized_30d    -- txn_categorized_30d / txn_count_30d (%)
--   txn_with_cp_30d        -- txns where counterparty_id IS NOT NULL
--   pct_with_cp_30d        -- txn_with_cp_30d / txn_count_30d (%)
--
-- Sort: txn_count_30d DESC (raw volume = primary engagement signal).
-- Adjust the ORDER BY / LIMIT to slice by other dimensions.

WITH params AS (
  SELECT (NOW() - INTERVAL '30 days') AS window_start
),

txns_30d AS (
  SELECT
    ta.workspace_id,
    COUNT(*)                                                                    AS txn_count_30d,
    COUNT(*) FILTER (WHERE tt.counterparty_id IS NOT NULL)                      AS txn_with_cp_30d
  FROM tesote_transactions tt
  INNER JOIN tesote_accounts ta
    ON ta.id = tt.tesote_account_id
   AND ta.discarded_at IS NULL
  CROSS JOIN params
  WHERE tt.discarded_at IS NULL
    AND tt.transaction_date >= params.window_start
  GROUP BY ta.workspace_id
),

categorized_30d AS (
  SELECT
    ta.workspace_id,
    COUNT(DISTINCT jtc.tesote_transaction_id) AS txn_categorized_30d
  FROM join_transaction_categories jtc
  INNER JOIN tesote_transactions tt
    ON tt.id = jtc.tesote_transaction_id
   AND tt.discarded_at IS NULL
  INNER JOIN tesote_accounts ta
    ON ta.id = tt.tesote_account_id
   AND ta.discarded_at IS NULL
  CROSS JOIN params
  WHERE tt.transaction_date >= params.window_start
  GROUP BY ta.workspace_id
),

sync_30d AS (
  SELECT
    esbc.workspace_id,
    COUNT(*)                                              AS sync_sessions_30d,
    COUNT(*) FILTER (WHERE bss.status = 'completed')      AS sync_completed_30d,
    COUNT(*) FILTER (WHERE bss.status = 'failed')         AS sync_failed_30d,
    MAX(bss.created_at)                                   AS last_sync_at
  FROM bank_sync_sessions bss
  INNER JOIN external_service_bank_connections esbc
    ON esbc.id = bss.external_service_bank_connection_id
   AND esbc.discarded_at IS NULL
  CROSS JOIN params
  WHERE bss.created_at >= params.window_start
  GROUP BY esbc.workspace_id
),

accounts AS (
  SELECT
    workspace_id,
    COUNT(*) AS live_accounts
  FROM tesote_accounts
  WHERE discarded_at IS NULL
    AND (archived IS NULL OR archived = FALSE)
    AND syncable = TRUE
    AND account_type <> 'manual'
  GROUP BY workspace_id
)

SELECT
  w.id                                                                          AS workspace_id,
  w.name                                                                        AS workspace_name,
  COALESCE(a.live_accounts, 0)                                                  AS live_accounts,
  COALESCE(s.sync_sessions_30d, 0)                                              AS sync_sessions_30d,
  COALESCE(s.sync_completed_30d, 0)                                             AS sync_completed_30d,
  COALESCE(s.sync_failed_30d, 0)                                                AS sync_failed_30d,
  s.last_sync_at,
  COALESCE(t.txn_count_30d, 0)                                                  AS txn_count_30d,
  COALESCE(c.txn_categorized_30d, 0)                                            AS txn_categorized_30d,
  CASE
    WHEN COALESCE(t.txn_count_30d, 0) > 0
      THEN ROUND(100.0 * COALESCE(c.txn_categorized_30d, 0) / t.txn_count_30d, 1)
    ELSE NULL
  END                                                                           AS pct_categorized_30d,
  COALESCE(t.txn_with_cp_30d, 0)                                                AS txn_with_cp_30d,
  CASE
    WHEN COALESCE(t.txn_count_30d, 0) > 0
      THEN ROUND(100.0 * COALESCE(t.txn_with_cp_30d, 0) / t.txn_count_30d, 1)
    ELSE NULL
  END                                                                           AS pct_with_cp_30d
FROM workspaces w
LEFT JOIN txns_30d        t ON t.workspace_id = w.id
LEFT JOIN categorized_30d c ON c.workspace_id = w.id
LEFT JOIN sync_30d        s ON s.workspace_id = w.id
LEFT JOIN accounts        a ON a.workspace_id = w.id
WHERE w.discarded_at IS NULL
  AND COALESCE(t.txn_count_30d, 0) > 0     -- active workspaces only
ORDER BY txn_count_30d DESC
LIMIT 50;
