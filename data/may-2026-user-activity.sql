-- =============================================================================
-- May 2026 user activity — power users, drop-offs, engagement segments
-- Run each query as a separate Metabase native question (Finance DB).
-- Source: user_activity_logs (1 row ≈ session start: >30min gap or IP/UA change)
-- Excludes admin impersonation rows. Timestamps shifted UTC → America/Caracas.
-- `internal` flags @tesote.com users — filter in Metabase if you want clients only.
-- =============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- Q1. Per-user May 2026 summary + weekly trajectory (the core query)
-- One row per user active in May OR seen in April (to catch full drop-offs).
-- ─────────────────────────────────────────────────────────────────────────────



-- ─────────────────────────────────────────────────────────────────────────────
-- Q2. Workspace-level rollup — engagement breadth per client
-- seats vs active seats vs deeply-active seats; silent workspaces = churn risk
-- ─────────────────────────────────────────────────────────────────────────────
WITH may AS (
  SELECT
    ual.user_id,
    (ual.created_at AT TIME ZONE 'utc' AT TIME ZONE 'America/Caracas')::date AS d
  FROM user_activity_logs ual
  WHERE ual.impersonation_info IS NULL
    AND ual.created_at >= '2026-05-01 04:00:00'
    AND ual.created_at <  '2026-06-01 04:00:00'
),
per_user AS (
  SELECT user_id, COUNT(DISTINCT d) AS active_days, COUNT(*) AS sessions
  FROM may GROUP BY 1
)
SELECT
  w.name                                              AS workspace,
  COUNT(DISTINCT wu.user_id)                          AS seats,
  COUNT(DISTINCT wu.user_id) FILTER (WHERE u.email NOT ILIKE '%@tesote.com') AS client_seats,
  COUNT(DISTINCT pu.user_id)                          AS active_users_may,
  COUNT(DISTINCT pu.user_id) FILTER (WHERE pu.active_days >= 10) AS engaged_users_may,
  COALESCE(SUM(pu.sessions), 0)                       AS total_sessions,
  ROUND(100.0 * COUNT(DISTINCT pu.user_id) / NULLIF(COUNT(DISTINCT wu.user_id), 0), 0) AS pct_seats_active
FROM workspaces w
JOIN workspace_users wu ON wu.workspace_id = w.id
JOIN users u            ON u.id = wu.user_id
LEFT JOIN per_user pu   ON pu.user_id = wu.user_id
WHERE w.discarded_at IS NULL
GROUP BY w.id, w.name
ORDER BY total_sessions DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- Q3. Daily active users through May — overall pulse (chart as line in Metabase)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
  (ual.created_at AT TIME ZONE 'utc' AT TIME ZONE 'America/Caracas')::date AS day,
  COUNT(DISTINCT ual.user_id)                         AS dau,
  COUNT(DISTINCT ual.user_id) FILTER (WHERE u.email NOT ILIKE '%@tesote.com') AS dau_clients,
  COUNT(*)                                            AS sessions
FROM user_activity_logs ual
JOIN users u ON u.id = ual.user_id
WHERE ual.impersonation_info IS NULL
  AND ual.created_at >= '2026-05-01 04:00:00'
  AND ual.created_at <  '2026-06-01 04:00:00'
GROUP BY 1
ORDER BY 1;
