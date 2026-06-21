-- PAYMENTS ICP — Query 2b VALIDATION: actual rows behind the workspace ranking.
-- Purpose: hand-inspect transactions per top workspace to validate the "individual payer" label.
-- Strategy: for the top 20 workspaces (by tx_count), return up to 50 rows each, sorted by
-- amount DESC so the biggest amounts surface first — those are the most likely false positives.
--
-- Uses the same filter stack as Query 2b. Keep both files in sync if filters change.

WITH individual_payer_rows AS (
  SELECT
    b.name                              AS bank,
    w.id                                AS workspace_id,
    w.name                              AS workspace,
    tt.id,
    tt.transaction_date,
    tt.description,
    tt.amount_cents / 100.0             AS amount
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  JOIN workspaces w                           ON w.id = ta.workspace_id AND w.discarded_at IS NULL
  WHERE tt.discarded_at IS NULL
    AND tt.amount_cents > 0
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= '2026-01-01'
    AND tt.transaction_date <  '2026-04-01'
    AND tt.description IS NOT NULL
    AND tt.description <> ''
    AND (
         b.name ILIKE '%banco de venezuela%'
      OR b.name ILIKE '%exterior%'
      OR b.name ILIKE '%fondo comun%'
      OR (b.name ILIKE '%banesco%' AND b.name NOT ILIKE '%panama%')
      OR b.name ILIKE '%bbva%'
    )
    AND tt.description ~ '[VE][0-9]{7,}'
    AND tt.description !~ 'J[0-9]{7,}'
    AND tt.description !~* ' PJ '
    AND tt.description !~* 'RIF'
    AND tt.description !~* '(L/POS|LIQUIDACI|LIQ\.|LIQ TDD|LIQ TDC|LIQ ELE|INTERESES|PROVEEDOR|N/C CRED|INCENTIVO|RECEPCION DE PAGO TERCERO|FONDOS RECIBIDOS|P2C|REINTEGRO|DEPOS\.ELECTRONI|MONEDERO PATRIA|COMPRA EN PUNTO DE VENTA|TITULOS DE COBERTURA|COBERTURA|RENDIMIENTO|PAGO DE INTERES|AB\.LOTE|PAC APP REC|TDY PAGO DE|REV\.PAGO|REV\.COM|DEVOLUCION RECIBIDA|TRANSF CUENTAS PROPIAS|TRANSF A TERCEROS MB)'
),
top_workspaces AS (
  SELECT workspace_id, workspace, COUNT(*) AS tx_count
  FROM individual_payer_rows
  GROUP BY workspace_id, workspace
  ORDER BY tx_count DESC
  LIMIT 20
),
ranked_rows AS (
  SELECT
    ipr.*,
    tw.tx_count AS workspace_tx_count,
    ROW_NUMBER() OVER (
      PARTITION BY ipr.workspace_id
      ORDER BY ipr.amount DESC, ipr.id
    ) AS rn
  FROM individual_payer_rows ipr
  JOIN top_workspaces tw ON tw.workspace_id = ipr.workspace_id
)
SELECT workspace, workspace_tx_count, bank, transaction_date, description, amount
FROM ranked_rows
WHERE rn <= 50
ORDER BY workspace_tx_count DESC, workspace, amount DESC
