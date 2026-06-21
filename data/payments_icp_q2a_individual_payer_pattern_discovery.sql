-- PAYMENTS ICP — Query 2a (NOISE-FILTERED SAMPLE): up to 1000 transactions per bank, all banks.
-- Purpose: strip known-noise descriptions, then hand-inspect what's left per bank to decide next filters.
-- Output from this query fed the bank mapping used in Query 2b.
--
-- Global filters:
--   - VES, Q1 2026, inbound (amount_cents > 0)
--   - description !~* 'RIF'
--   - exclude known noise: L/POS, LIQUIDACI*, INTERESES, PROVEEDOR, N/C CRED, N/C INCENTIVO,
--     INCENTIVO POS, RECEPCION DE PAGO TERCERO, FONDOS RECIBIDOS P2C, P2C

WITH ranked AS (
  SELECT
    b.name                              AS bank,
    w.name                              AS workspace,
    tt.transaction_date,
    tt.description,
    tt.amount_cents / 100.0             AS amount,
    tt.amount_currency                  AS currency,
    ROW_NUMBER() OVER (
      PARTITION BY b.name
      ORDER BY tt.transaction_date DESC, tt.id
    ) AS rn
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
    AND tt.description !~* 'RIF'
    AND tt.description !~* '(L/POS|LIQUIDACI|INTERESES|PROVEEDOR|N/C CRED|N/C INCENTIVO|NC INCENTIVO|INCENTIVO POS|RECEPCION DE PAGO TERCERO|FONDOS RECIBIDOS P2C|P2C)'
)
SELECT bank, workspace, transaction_date, description, amount, currency
FROM ranked
WHERE rn <= 1000
ORDER BY bank, transaction_date DESC, description;
