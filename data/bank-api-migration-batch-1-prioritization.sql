-- Bank API migration — batch 1 prioritization
-- Goal: decide order to move customers from scraping → bank APIs.
-- Target banks (priority order): BBVA (Provincial), Banesco, Mercantil, Bancaribe.
-- Grain = entity × bank, because a bank API request is granted per legal entity AT a specific bank,
-- and moving an entity to one bank's API only relieves that entity's accounts at that bank.
-- accounts/tx are counted at that intersection = the pressure one request actually relieves.
-- tx_last_90d = ongoing scrape pressure (sort on this); tx_total = lifetime context.

WITH target_banks AS (
  SELECT id, name
  FROM banks
  WHERE name IN ('Provincial', 'Banesco', 'Mercantil', 'Bancaribe')  -- Provincial = BBVA
),

-- Live accounts only (these are what we scrape today; archived/manual/non-syncable = no pressure)
acct AS (
  SELECT
    ta.id                                                       AS account_id,
    ta.workspace_id,
    COALESCE(ta.tesote_legal_entity_id, esbc.tesote_legal_entity_id) AS entity_id,
    tb.name                                                     AS bank_name
  FROM tesote_accounts ta
  JOIN external_service_bank_connections esbc
    ON esbc.id = ta.external_service_bank_connection_id
   AND esbc.discarded_at IS NULL
   AND esbc.status = 'active'
  JOIN target_banks tb ON tb.id = esbc.bank_id
  WHERE ta.discarded_at IS NULL
    AND ta.syncable = true
    AND COALESCE(ta.archived, false) = false
    AND ta.account_type <> 'manual'
),

acct_counts AS (
  SELECT workspace_id, entity_id, bank_name, COUNT(*) AS num_accounts
  FROM acct
  GROUP BY workspace_id, entity_id, bank_name
),

tx AS (
  SELECT
    a.workspace_id,
    a.entity_id,
    a.bank_name,
    COUNT(*) FILTER (WHERE tt.discarded_at IS NULL)                                                          AS tx_total,
    COUNT(*) FILTER (WHERE tt.discarded_at IS NULL AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days') AS tx_90d
  FROM acct a
  JOIN tesote_transactions tt ON tt.tesote_account_id = a.account_id
  GROUP BY a.workspace_id, a.entity_id, a.bank_name
),

-- Total distinct legal entities per workspace, across ALL banks (full org footprint, not just target banks)
ws_entities AS (
  SELECT ta.workspace_id, COUNT(DISTINCT ta.tesote_legal_entity_id) AS total_entities_in_workspace
  FROM tesote_accounts ta
  WHERE ta.discarded_at IS NULL
    AND ta.tesote_legal_entity_id IS NOT NULL
  GROUP BY ta.workspace_id
)

SELECT
  w.name                                  AS workspace,
  COALESCE(we.total_entities_in_workspace, 0) AS total_entities_in_workspace,
  COALESCE(tle.legal_name, tle.nickname)  AS entity,
  CASE ac.bank_name WHEN 'Provincial' THEN 'BBVA' ELSE ac.bank_name END AS bank,
  ac.num_accounts,
  COALESCE(tx.tx_90d, 0)                  AS tx_last_90d,
  COALESCE(tx.tx_total, 0)                AS tx_total
FROM acct_counts ac
JOIN workspaces w ON w.id = ac.workspace_id AND w.discarded_at IS NULL
LEFT JOIN tesote_legal_entities tle ON tle.id = ac.entity_id
LEFT JOIN ws_entities we ON we.workspace_id = ac.workspace_id
LEFT JOIN tx
  ON tx.workspace_id = ac.workspace_id
 AND tx.entity_id   = ac.entity_id
 AND tx.bank_name   = ac.bank_name
ORDER BY
  CASE ac.bank_name
    WHEN 'Provincial' THEN 1   -- BBVA
    WHEN 'Banesco'    THEN 2
    WHEN 'Mercantil'  THEN 3
    WHEN 'Bancaribe'  THEN 4
    ELSE 5
  END,
  tx_last_90d DESC NULLS LAST;


-- =====================================================================
-- v2 — CLIENT x BANK summary (rollup of v1 to the decision grain)
-- One row per client x bank. Adds:
--   * manual client grouping (multi-workspace customers collapse to one client)
--   * active-account count   ("active" = live account with >=1 txn in last 90d)
--   * entities_at_bank        (= # API access requests we'd send that bank)
-- Same target banks + priority order as v1. BBVA shown (banks.name='Provincial').
-- =====================================================================

WITH target_banks AS (
  SELECT id, name FROM banks
  WHERE name IN ('Provincial', 'Banesco', 'Mercantil', 'Bancaribe')  -- Provincial = BBVA
),

-- Manual customer grouping: some customers span multiple workspaces but are ONE client.
-- Extend this VALUES list as the groupings evolve. Workspaces not listed default to their own name.
client_map (workspace_name, client) AS (
  VALUES
    ('ALIMENTOS DOÑA EMILIA',        'Asoportuguesa'),
    ('ALMACENADORA ASOPORTUGUESA',   'Asoportuguesa'),
    ('ASOPRODUCTOS',                 'Asoportuguesa'),
    ('Avila',                        'Grupo Avila'),
    ('FARMACIAS SAN IGNACIO - JT',   'Farmacias San Ignacio'),
    ('FARMACIAS SAN IGNACIO AE',     'Farmacias San Ignacio'),
    ('Grahndes',                     'Pharmakum'),
    ('Grupo Da Silva',               'Maxy Sweet'),
    ('Casagri de Lara',              'Casagri'),
    ('ARAWAK',                       'Arawak')
),

acct AS (
  SELECT
    ta.id AS account_id,
    ta.workspace_id,
    COALESCE(ta.tesote_legal_entity_id, esbc.tesote_legal_entity_id) AS entity_id,
    tb.name AS bank_name
  FROM tesote_accounts ta
  JOIN external_service_bank_connections esbc
    ON esbc.id = ta.external_service_bank_connection_id
   AND esbc.discarded_at IS NULL
   AND esbc.status = 'active'
  JOIN target_banks tb ON tb.id = esbc.bank_id
  WHERE ta.discarded_at IS NULL
    AND ta.syncable = true
    AND COALESCE(ta.archived, false) = false
    AND ta.account_type <> 'manual'
),

acct_tx AS (
  SELECT
    a.account_id,
    COUNT(*) FILTER (WHERE tt.discarded_at IS NULL)                                                          AS tx_total,
    COUNT(*) FILTER (WHERE tt.discarded_at IS NULL AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days') AS tx_90d
  FROM acct a
  LEFT JOIN tesote_transactions tt ON tt.tesote_account_id = a.account_id
  GROUP BY a.account_id
),

acct_full AS (
  SELECT
    a.account_id, a.entity_id, a.bank_name,
    COALESCE(cm.client, w.name) AS client,
    COALESCE(atx.tx_total, 0)   AS tx_total,
    COALESCE(atx.tx_90d, 0)     AS tx_90d
  FROM acct a
  JOIN workspaces w ON w.id = a.workspace_id AND w.discarded_at IS NULL
  LEFT JOIN client_map cm ON cm.workspace_name = w.name
  LEFT JOIN acct_tx atx ON atx.account_id = a.account_id
),

client_entities AS (   -- distinct entities per client across all 4 target banks
  SELECT client, COUNT(DISTINCT entity_id) AS client_entities_total
  FROM acct_full
  WHERE entity_id IS NOT NULL
  GROUP BY client
)

SELECT
  af.client,
  ce.client_entities_total,
  CASE af.bank_name WHEN 'Provincial' THEN 'BBVA' ELSE af.bank_name END   AS bank,
  COUNT(DISTINCT af.entity_id)                                            AS entities_at_bank,        -- = API requests to this bank
  COUNT(DISTINCT af.account_id)                                           AS accounts_at_bank,
  COUNT(DISTINCT af.account_id) FILTER (WHERE af.tx_90d > 0)              AS active_accounts_at_bank,  -- txn in last 90d
  SUM(af.tx_total)                                                        AS tx_total,
  SUM(af.tx_90d)                                                          AS tx_last_90d
FROM acct_full af
JOIN client_entities ce ON ce.client = af.client
GROUP BY af.client, ce.client_entities_total, af.bank_name
ORDER BY
  CASE af.bank_name
    WHEN 'Provincial' THEN 1   -- BBVA
    WHEN 'Banesco'    THEN 2
    WHEN 'Mercantil'  THEN 3
    WHEN 'Bancaribe'  THEN 4
    ELSE 5
  END,
  tx_last_90d DESC NULLS LAST;
