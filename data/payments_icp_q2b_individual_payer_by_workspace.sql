-- PAYMENTS ICP — Query 2b: workspaces ranked by individual-payer VES flow.
-- Goal: find workspaces receiving high volume & high tx-count from individuals.
--
-- Scope: 5 banks that expose payer identity in description:
--   Banco de Venezuela, Banco Exterior, Banco Fondo Comun, Banesco (VE, not Panama), BBVA.
-- Dark banks dropped (Bancamiga, Bancaribe, Banplus, Bangente, 100% Banco, Mercantil, R4,
--   Venezolano Credito, Banco Activo, Banco Del Tesoro, Banco Plaza, BNC) — description-blind.
--
-- Filter stack:
--   - VES, Q1 2026, inbound (amount_cents > 0), non-discarded
--   - description contains [VE][0-9]{7,} (natural-person cedula)
--   - description does NOT contain J[0-9]{7,} (legal-entity RIF)
--   - description does NOT contain ' PJ ' (Persona Jurídica marker in pago-movil flows)
--   - description does NOT contain noise patterns: POS/card liquidations, reversals, govt, cobertura,
--     aggregator labels, bond yields, etc. (see regex below)

WITH individual_payer_rows AS (
  SELECT
    b.name                              AS bank,
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
    -- Identity-exposing banks only
    AND (
         b.name ILIKE '%banco de venezuela%'
      OR b.name ILIKE '%exterior%'
      OR b.name ILIKE '%fondo comun%'
      OR (b.name ILIKE '%banesco%' AND b.name NOT ILIKE '%panama%')
      OR b.name ILIKE '%bbva%'
    )
    -- Require individual cedula pattern
    AND tt.description ~ '[VE][0-9]{7,}'
    -- Exclude legal-entity RIF pattern
    AND tt.description !~ 'J[0-9]{7,}'
    -- Exclude PJ (Persona Jurídica) marker
    AND tt.description !~* ' PJ '
    -- Exclude literal "RIF"
    AND tt.description !~* 'RIF'
    -- Exclude known noise patterns
    AND tt.description !~* '(L/POS|LIQUIDACI|LIQ\.|LIQ TDD|LIQ TDC|LIQ ELE|INTERESES|PROVEEDOR|N/C CRED|INCENTIVO|RECEPCION DE PAGO TERCERO|FONDOS RECIBIDOS|P2C|REINTEGRO|DEPOS\.ELECTRONI|MONEDERO PATRIA|COMPRA EN PUNTO DE VENTA|TITULOS DE COBERTURA|COBERTURA|RENDIMIENTO|PAGO DE INTERES|AB\.LOTE|PAC APP REC|TDY PAGO DE|REV\.PAGO|REV\.COM|DEVOLUCION RECIBIDA|TRANSF CUENTAS PROPIAS|TRANSF A TERCEROS MB)'
)

SELECT
  workspace,
  COUNT(*)                                AS tx_count,
  ROUND(SUM(amount)::numeric, 2)          AS total_ves,
  ROUND(AVG(amount)::numeric, 2)          AS avg_ves,
  ROUND(MIN(amount)::numeric, 2)          AS min_ves,
  ROUND(MAX(amount)::numeric, 2)          AS max_ves,
  COUNT(DISTINCT bank)                    AS distinct_banks,
  STRING_AGG(DISTINCT bank, ', ') AS banks
FROM individual_payer_rows
GROUP BY workspace
ORDER BY tx_count DESC, total_ves DESC
LIMIT 100
