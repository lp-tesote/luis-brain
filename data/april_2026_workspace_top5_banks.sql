-- April 2026 — Top 5 banks per workspace, by VES volume (dolarized at 500 VES/USD)
-- Goal: for each of these workspaces, see which 5 banks they transact through most heavily,
-- so we can understand which rails matter for them.
--
-- Scope:
--   * VES currency only
--   * April 2026 (2026-04-01 inclusive → 2026-05-01 exclusive)
--   * Active (non-discarded) accounts/connections; transactions with amount <> 0
--   * Bank = the workspace's OWN account bank (via esbc → banks), not the counterparty bank
--
-- Direction:
--   * Volume / ranking = absolute value, both directions combined
--     ("which banks do they use to transact" — collection AND payments)
--   * in_tx / out_tx and in_ves / out_ves columns let you spot collection-banks
--     vs payment-banks at a glance
--
-- Ranking:
--   * vol_rank = primary signal (top 5 cut applied here)
--   * count_rank shown alongside; if the two disagree it means many small-tx vs few big-tx
--
-- IMPORTANT: run april_2026_workspace_top5_banks_resolve.sql FIRST
-- to confirm workspace name patterns each match exactly one active workspace.

WITH params AS (
  SELECT
    DATE '2026-04-01' AS start_date,
    DATE '2026-05-01' AS end_date_excl,
    500.0::numeric    AS ves_per_usd
),
inputs(input_name, pattern, exclude) AS (
  VALUES
    ('Procesadora Marsoca',         '%marsoca%',                    NULL::text),
    ('Molinos Carabobo SA',         '%molinos%carabobo%',           NULL),
    ('Molinos Nacionales CA',       '%molinos%nacionales%',         NULL),
    ('AVICOLA LAS TUNAS',           '%avicola%tunas%',              NULL),
    ('Grupo Maralac',               '%maralac%',                    NULL),
    ('Casa Franceschi',             '%franceschi%',                 NULL),
    ('CAMOR INTERNACIONAL',         '%camor%',                      NULL),
    ('PASTCA',                      '%pastca%',                     NULL),
    ('ALMACENADORA ASOPORTUGUESA',  '%almacenadora%asoportuguesa%', NULL),
    ('ALIMENTOS LPRADO',            '%lprado%',                     NULL),
    ('alimentosmunchy',             '%munchy%',                     NULL),
    ('ALIMENTOS DOÑA EMILIA',       '%emilia%',                     NULL),
    ('Asoportuguesa',               '%asoportuguesa%',              '%almacenadora%'),
    ('Capitalfoods',                '%capital%foods%',              NULL),
    ('suvica',                      '%suvica%',                     NULL),
    ('Alimentos Global',            '%alimentos%global%',           NULL),
    ('Casagri de Lara',             '%casagri%',                    NULL),
    ('Grupo Mimesa',                '%mimesa%',                     NULL),
    ('Alimentos Alvarigua, c.a.',   '%alvarigua%',                  NULL),
    ('TORONDOY',                    '%torondoy%',                   NULL),
    ('Corporación JSL, C.A.',       '%jsl%',                        NULL),
    ('ARAWAK',                      '%arawak%',                     NULL),
    ('ASOPRODUCTOS',                '%asoproductos%',               NULL),
    ('Protinal',                    '%protinal%',                   NULL)
),
matched_workspaces AS (
  SELECT
    i.input_name,
    w.id   AS workspace_id,
    w.name AS workspace_name
  FROM inputs i
  JOIN workspaces w
    ON w.name ILIKE i.pattern
   AND (i.exclude IS NULL OR w.name NOT ILIKE i.exclude)
   AND w.discarded_at IS NULL
),
base AS (
  SELECT
    mw.input_name,
    mw.workspace_id,
    mw.workspace_name,
    b.name                                                  AS bank,
    tt.amount_cents / 100.0                                 AS amount_ves,
    CASE WHEN tt.amount_cents > 0 THEN 'in' ELSE 'out' END  AS direction
  FROM matched_workspaces mw
  JOIN tesote_accounts ta
    ON ta.workspace_id = mw.workspace_id
   AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc
    ON esbc.id = ta.external_service_bank_connection_id
   AND esbc.discarded_at IS NULL
  JOIN banks b
    ON b.id = esbc.bank_id
  JOIN tesote_transactions tt
    ON tt.tesote_account_id = ta.id
   AND tt.discarded_at IS NULL
   AND tt.amount_cents <> 0
   AND tt.amount_currency = 'VES'
   AND tt.transaction_date >= (SELECT start_date    FROM params)
   AND tt.transaction_date <  (SELECT end_date_excl FROM params)
),
per_bank AS (
  SELECT
    input_name,
    workspace_name,
    bank,
    COUNT(*)                                                AS tx_count,
    COUNT(*) FILTER (WHERE direction = 'in')                AS in_tx,
    COUNT(*) FILTER (WHERE direction = 'out')               AS out_tx,
    SUM(ABS(amount_ves))                                    AS volume_ves,
    SUM(ABS(amount_ves)) FILTER (WHERE direction = 'in')    AS in_ves,
    SUM(ABS(amount_ves)) FILTER (WHERE direction = 'out')   AS out_ves
  FROM base
  GROUP BY input_name, workspace_name, bank
),
ranked AS (
  SELECT
    pb.*,
    ROW_NUMBER() OVER (PARTITION BY input_name, workspace_name
                       ORDER BY volume_ves DESC NULLS LAST)  AS vol_rank,
    ROW_NUMBER() OVER (PARTITION BY input_name, workspace_name
                       ORDER BY tx_count   DESC)             AS count_rank
  FROM per_bank pb
)
SELECT
  input_name,
  workspace_name,
  vol_rank,
  count_rank,
  bank,
  tx_count,
  in_tx,
  out_tx,
  ROUND(volume_ves::numeric, 0)                                       AS volume_ves,
  ROUND((volume_ves / (SELECT ves_per_usd FROM params))::numeric, 0)  AS volume_usd,
  ROUND(in_ves::numeric, 0)                                           AS in_ves,
  ROUND(out_ves::numeric, 0)                                          AS out_ves
FROM ranked
WHERE vol_rank <= 5
ORDER BY input_name, workspace_name, vol_rank;
