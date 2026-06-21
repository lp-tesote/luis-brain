-- =====================================================================
-- Purolomo — bank-by-bank nomenclature samples
-- =====================================================================
-- Goal: rebuild Majo's Notion playbook ("Playbook - Descripciones de Bancos")
-- with the credit/debit split it's missing. Each query is self-contained
-- so it drops straight into a Metabase question.
--
-- The PM's existing schema has these fields per bank:
--   RIF, Razón Social, Concepto, Número de Cuenta, Código de Transacción
-- Each needs to be evaluated SEPARATELY for credits (cobros entrantes)
-- and debits (egresos), because banks behave asymmetrically.
--
-- Window: last 90 days, VES only, non-discarded.
-- Adjust dates / currency / bank list as needed.
-- =====================================================================


-- =====================================================================
-- Q1 — Coverage sanity check
-- =====================================================================
-- Which banks have enough data to inspect, split by direction. Run this
-- first; any bank with <100 rows on a given direction is too thin to
-- score reliably from samples alone.
--
SELECT
  b.name                                                 AS bank,
  b.external_bank_code                                   AS code,
  COUNT(*) FILTER (WHERE tt.amount_cents > 0)            AS credit_rows,
  COUNT(*) FILTER (WHERE tt.amount_cents < 0)            AS debit_rows,
  COUNT(*) FILTER (WHERE tt.description IS NULL OR tt.description = '') AS null_desc_rows,
  COUNT(*)                                               AS total_rows
FROM tesote_transactions tt
JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
JOIN banks b                                ON b.id = esbc.bank_id
WHERE tt.discarded_at IS NULL
  AND tt.amount_currency = 'VES'
  AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY b.name, b.external_bank_code
ORDER BY total_rows DESC;


-- =====================================================================
-- Q2 — Sample descriptions per bank × direction (the main tool)
-- =====================================================================
-- 10 random credit + 10 random debit samples per bank. Visual-inspection
-- query. Eyeball the description column and score each bank's row in the
-- Notion playbook for: RIF / Razón Social / Concepto / Cuenta / Cód Tx
-- in EACH direction.
--
-- Tip: in Metabase, sort by (bank, direction) and read top-to-bottom.
--
WITH ranked AS (
  SELECT
    b.name                                  AS bank,
    b.external_bank_code                    AS code,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.transaction_date,
    tt.amount_cents / 100.0                 AS amount_ves,
    tt.description,
    tt.reference_code,
    ROW_NUMBER() OVER (
      PARTITION BY b.id, SIGN(tt.amount_cents)
      ORDER BY random()
    )                                       AS rn
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
)
SELECT bank, code, direction, transaction_date, amount_ves, description, reference_code
FROM ranked
WHERE rn <= 10
ORDER BY bank, direction, rn;


-- =====================================================================
-- Q3 — RIF/Cédula presence rate per bank × direction
-- =====================================================================
-- The one column we can score quantitatively. Detects any V/E/J/G/P
-- prefix followed by 6-10 digits anywhere in the description.
--
-- Scoring rule of thumb for the playbook:
--   >= 90% match → COMPLETO
--   30%-90%      → PARCIAL  (or COMPLETO for one tx-type, NO for another)
--   <  30%       → NO
--
-- "PARCIAL" usually means the bank delivers RIF only on certain tx-types
-- (e.g., intrabank transfers but not POS). Cross-reference with Q2 to
-- understand WHICH tx-types are missing it.
--
SELECT
  b.name                                                 AS bank,
  b.external_bank_code                                   AS code,
  CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
  COUNT(*)                                               AS rows_evaluated,
  COUNT(*) FILTER (
    WHERE tt.description ~* '\m[VEJGP][-\s]?[0-9]{6,10}\M'
  )                                                      AS rows_with_rif_or_cedula,
  ROUND(
    100.0 * COUNT(*) FILTER (
      WHERE tt.description ~* '\m[VEJGP][-\s]?[0-9]{6,10}\M'
    )::numeric / NULLIF(COUNT(*), 0),
    1
  )                                                      AS pct_with_rif
FROM tesote_transactions tt
JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
JOIN banks b                                ON b.id = esbc.bank_id
WHERE tt.discarded_at IS NULL
  AND tt.amount_currency = 'VES'
  AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
  AND tt.amount_cents <> 0
  AND tt.description IS NOT NULL
  AND tt.description <> ''
GROUP BY b.name, b.external_bank_code, direction
ORDER BY bank, direction;


-- =====================================================================
-- Q4 — Account-number presence rate per bank × direction
-- =====================================================================
-- Same shape as Q3. Detects any contiguous 11-20 digit number, or a
-- common "Cta/Cuenta/Nro" preamble. Imperfect — fall back to Q2 if a
-- bank's percentage looks suspicious.
--
SELECT
  b.name                                                 AS bank,
  b.external_bank_code                                   AS code,
  CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
  COUNT(*)                                               AS rows_evaluated,
  COUNT(*) FILTER (
    WHERE tt.description ~* '(cta|cuenta|nro\.?|n°)\s*[0-9]{8,}'
       OR tt.description ~* '\m[0-9]{16,20}\M'
  )                                                      AS rows_with_account,
  ROUND(
    100.0 * COUNT(*) FILTER (
      WHERE tt.description ~* '(cta|cuenta|nro\.?|n°)\s*[0-9]{8,}'
         OR tt.description ~* '\m[0-9]{16,20}\M'
    )::numeric / NULLIF(COUNT(*), 0),
    1
  )                                                      AS pct_with_account
FROM tesote_transactions tt
JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
JOIN banks b                                ON b.id = esbc.bank_id
WHERE tt.discarded_at IS NULL
  AND tt.amount_currency = 'VES'
  AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
  AND tt.amount_cents <> 0
  AND tt.description IS NOT NULL
  AND tt.description <> ''
GROUP BY b.name, b.external_bank_code, direction
ORDER BY bank, direction;


-- =====================================================================
-- Q5 — Description shape: length & reference_code coverage
-- =====================================================================
-- Indirect signal for "Concepto" (free-text memo) richness and whether
-- reference_code is populated. A bank with a 25-char median description
-- is unlikely to be carrying a useful concepto field.
--
SELECT
  b.name                                                 AS bank,
  b.external_bank_code                                   AS code,
  CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
  COUNT(*)                                               AS rows_evaluated,
  ROUND(AVG(CHAR_LENGTH(tt.description))::numeric, 0)    AS avg_desc_len,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY CHAR_LENGTH(tt.description))::int AS median_desc_len,
  MAX(CHAR_LENGTH(tt.description))                       AS max_desc_len,
  COUNT(*) FILTER (
    WHERE tt.reference_code IS NOT NULL AND tt.reference_code <> ''
  )                                                      AS rows_with_ref_code,
  ROUND(
    100.0 * COUNT(*) FILTER (
      WHERE tt.reference_code IS NOT NULL AND tt.reference_code <> ''
    )::numeric / NULLIF(COUNT(*), 0),
    1
  )                                                      AS pct_with_ref_code
FROM tesote_transactions tt
JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
JOIN banks b                                ON b.id = esbc.bank_id
WHERE tt.discarded_at IS NULL
  AND tt.amount_currency = 'VES'
  AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
  AND tt.amount_cents <> 0
  AND tt.description IS NOT NULL
  AND tt.description <> ''
GROUP BY b.name, b.external_bank_code, direction
ORDER BY bank, direction;


-- =====================================================================
-- Q6 — Deep-dive on a single bank (parameterized)
-- =====================================================================
-- For when Q2's 10 samples aren't enough to score a bank confidently.
-- Replace the bank name and run again. Returns 50 samples per direction.
--
WITH ranked AS (
  SELECT
    b.name                                  AS bank,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.transaction_date,
    tt.amount_cents / 100.0                 AS amount_ves,
    tt.description,
    tt.reference_code,
    ROW_NUMBER() OVER (
      PARTITION BY SIGN(tt.amount_cents)
      ORDER BY random()
    )                                       AS rn
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
    AND b.name ILIKE 'Bancaribe'        -- <<< change me
)
SELECT direction, transaction_date, amount_ves, description, reference_code
FROM ranked
WHERE rn <= 50
ORDER BY direction, rn;


-- =====================================================================
-- Q7 — Out-of-scope classifier (run this BEFORE rebuilding the playbook)
-- =====================================================================
-- v3 (2026-04-27, p.m. round 2): tightened against Q2-K leak audit.
--   • Bancrecer 85% credit leak: added LIQUIDACION CREDITO/ELECTRON to CARD_LIQ
--   • Banco Plaza ~50% debit leak (TDY COM.P2P/C2P/P2C): dropped the
--     trailing \s requirement on \mCOM\.\s → now \mCOM\. catches
--     "COM.P2P", "COM.PAT", "COM.PAGO", "COM.CREDITO" etc. without space
--   • Banco Activo ~25% debit leak (bare "COM RECEP", "COM MOV CTA"):
--     re-added \mCOM\M\s+ standalone-word rule
--   • Bancaribe 29% credit leak: added \m(TDD|TDC)\M\s*-\s*ADMIN
--   • Smaller fixes: DESCUENTO TARJETA (Mercantil), INCENTIVO POS
--     (Bancamiga), TC POS (BBVA), REEMBOLSO COSTOS POS (Banplus),
--     SERVICIO ESPECIALIZADO POS (BE), RECARGO and MTTO (FEE).
-- v2: switched from ^ anchors to word boundaries (\m...\M) so banks
-- that prefix descriptions with metadata (Banco Exterior's "9023 …"
-- numeric prefix; BNC's "TELF.: CED.: CTA.: …" header) get classified
-- correctly. Added Mercantil RVR (CANCELACION RESUMEN), BNC POS
-- ("POS:" / "Abono Comercio por Tarjeta"), and BE fees.
--
-- Buckets every transaction into KEEP or one of four EXCLUDE classes.
--
--   EXCLUDE_CARD_LIQ → POS / TDD / TDC / Maestro / BiopagoBDV settlements.
--                      By design no payer RIF (PCI + acquirer model).
--   EXCLUDE_FEE      → Bank fees, comisiones, retenciones (ISLR), cargos.
--                      The bank charging the workspace, not a payer.
--   EXCLUDE_INTERNAL → Transfers between own / same-titular accounts.
--   EXCLUDE_REVERSAL → Reintegros, cancelaciones, reversiones.
--   KEEP             → Real third-party cobros, INCLUDING diagnostic
--                      cases where the bank stripped payer info ("Pago
--                      movil recibido" with no name/RIF). Those rows
--                      are the proof that a bank scores NO/PARCIAL.
--
-- Edge cases I deliberately KEEP:
--   • Pago Móvil P2C with phone-only payer (Banco Plaza "TDY COBRO …",
--     Banplus "Pago Plus Comercios Recibido", Bancaribe "Pago movil
--     recibido") — real cobros, just no payer ID.
--   • Banco Fondo Comun "AB.LOTE 0162 …" — could be card OR payroll
--     batch. Currently classified as CARD_LIQ; eyeball Q6 on BFC and
--     move to KEEP if it turns out to be batch transfers.
--
WITH classified AS (
  SELECT
    b.id                                                     AS bank_id,
    b.name                                                   AS bank,
    b.external_bank_code                                     AS code,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.amount_cents,
    tt.amount_cents / 100.0                                  AS amount_ves,
    tt.transaction_date,
    tt.description,
    tt.reference_code,
    CASE
      -- Card / POS / TDD / TDC / Maestro liquidations
      WHEN tt.description ~* 'BIOPAGOBDV|LIQUIDACI(O|Ó)N\s+(TDD|TDC|MAESTRO|TARJETA|VENTAS|A\s+COMERCIO|CREDITO|ELECTRON)|LIQUIDACION\s+VENTAS|DEPOS\.ELECTRONI|LIQ\.TARJETA|LIQ\s+(MONEDERO|TARJETA|TDD|TDC)|COM/LIQ/(TDD|TDC)|LQ\s+(TDD|TDC)\s|N/?C\s+LIQUIDACION\s+MAESTRO|N/?D\s+COM\.\s+LIQUIDACION\s+MAESTRO|CANCELACION\s+RESUMEN\s+DE\s+VENTAS|ABONO\s+COMERCIO\s+POR\s+TARJETA|COMPRA\s+POS|TDB\s+CAPIT|TD\s+POS|C\.O\.TPV'
        OR tt.description ~* '\mL/POS\M'
        OR tt.description ~* '\mPOS\s*:|\mPOS\s+(DEB|CR|MA|CREDITO)'
        OR tt.description ~* '\m(TDC|TMD|TT)\s+\d{6,}'
        OR tt.description ~* '\mTD\s+\d{6,}'
        OR tt.description ~* '\mAB\.LOTE\M'
        OR tt.description ~* '\m(TDD|TDC)\M\s*-\s*ADMIN'
        OR tt.description ~* '\mDESCUENTO\s+TARJETA\M'
        OR tt.description ~* '\mINCENTIVO\s+POS\M'
        OR tt.description ~* '\mTC\s+POS\M'
        OR tt.description ~* '\mREEMBOLSO\s+(DE\s+)?COSTOS?\s+POS\M'
        OR tt.description ~* '\mSERVICIO\s+ESPECIALIZADO\s+POS\M'
        THEN 'EXCLUDE_CARD_LIQ'
      -- Bank fees, commissions, retenciones, cargos
      WHEN tt.description ~* '\mCOMIS|\mCOM\.|\mCOM\M\s+|\mN/?D\s+COM\M|\mCARGO\s|\mRECARGO\M|\mMTTO\M|\mREI\.ISLR|\mREINTEGRO\s+(COMIS|ISLR)|\mCONTRAPRESTACION|\mCOBRO\s+POR\s+PROCESAMIENTO|\mEMISI(O|Ó)N\s+(DE\s+)?ESTADO|\mC/CUOTA|\mMANTENIMIENTO\s+CTA'
        THEN 'EXCLUDE_FEE'
      -- Same-account / own-titular transfers
      WHEN tt.description ~* '\mTRANSF\s+CUENTAS\s+PROPIAS|\mTRASPASO\M|\mTRANSF\s+ENTRE\s+CTAS|\mTRANS\s+ENTRE\s+CTAS|\mMISMO\s+(CLIENTE|TIT)'
        THEN 'EXCLUDE_INTERNAL'
      -- Reversals / cancellations / refunds (after FEE so REINTEGRO COMIS goes to FEE)
      WHEN tt.description ~* '\mREINTEGRO\M|\mCANCELACI(O|Ó)N\M|\mREVERSI(O|Ó)N|\mREVERSO\M'
        THEN 'EXCLUDE_REVERSAL'
      ELSE 'KEEP'
    END                                                      AS txn_class
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
)
-- Per-bank × direction × class breakdown — sanity check the buckets
SELECT
  bank,
  direction,
  txn_class,
  COUNT(*)                                                                       AS rows,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY bank, direction), 1) AS pct_of_direction
FROM classified
GROUP BY bank, direction, txn_class
ORDER BY bank, direction, rows DESC;


-- =====================================================================
-- Q2-K — Filtered samples (KEEP only) — the playbook workhorse
-- =====================================================================
-- Same as Q2 but only includes in-scope rows. Pulls 100 random samples
-- per bank × direction. This is what you eyeball to fill the playbook.
--
WITH classified AS (
  SELECT
    b.id                                                     AS bank_id,
    b.name                                                   AS bank,
    b.external_bank_code                                     AS code,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.amount_cents,
    tt.amount_cents / 100.0                                  AS amount_ves,
    tt.transaction_date,
    tt.description,
    tt.reference_code,
    CASE
      WHEN tt.description ~* 'BIOPAGOBDV|LIQUIDACI(O|Ó)N\s+(TDD|TDC|MAESTRO|TARJETA|VENTAS|A\s+COMERCIO|CREDITO|ELECTRON)|LIQUIDACION\s+VENTAS|DEPOS\.ELECTRONI|LIQ\.TARJETA|LIQ\s+(MONEDERO|TARJETA|TDD|TDC)|COM/LIQ/(TDD|TDC)|LQ\s+(TDD|TDC)\s|N/?C\s+LIQUIDACION\s+MAESTRO|N/?D\s+COM\.\s+LIQUIDACION\s+MAESTRO|CANCELACION\s+RESUMEN\s+DE\s+VENTAS|ABONO\s+COMERCIO\s+POR\s+TARJETA|COMPRA\s+POS|TDB\s+CAPIT|TD\s+POS|C\.O\.TPV'
        OR tt.description ~* '\mL/POS\M'
        OR tt.description ~* '\mPOS\s*:|\mPOS\s+(DEB|CR|MA|CREDITO)'
        OR tt.description ~* '\m(TDC|TMD|TT)\s+\d{6,}'
        OR tt.description ~* '\mTD\s+\d{6,}'
        OR tt.description ~* '\mAB\.LOTE\M'
        OR tt.description ~* '\m(TDD|TDC)\M\s*-\s*ADMIN'
        OR tt.description ~* '\mDESCUENTO\s+TARJETA\M'
        OR tt.description ~* '\mINCENTIVO\s+POS\M'
        OR tt.description ~* '\mTC\s+POS\M'
        OR tt.description ~* '\mREEMBOLSO\s+(DE\s+)?COSTOS?\s+POS\M'
        OR tt.description ~* '\mSERVICIO\s+ESPECIALIZADO\s+POS\M'
        THEN 'EXCLUDE_CARD_LIQ'
      WHEN tt.description ~* '\mCOMIS|\mCOM\.|\mCOM\M\s+|\mN/?D\s+COM\M|\mCARGO\s|\mRECARGO\M|\mMTTO\M|\mREI\.ISLR|\mREINTEGRO\s+(COMIS|ISLR)|\mCONTRAPRESTACION|\mCOBRO\s+POR\s+PROCESAMIENTO|\mEMISI(O|Ó)N\s+(DE\s+)?ESTADO|\mC/CUOTA|\mMANTENIMIENTO\s+CTA'
        THEN 'EXCLUDE_FEE'
      WHEN tt.description ~* '\mTRANSF\s+CUENTAS\s+PROPIAS|\mTRASPASO\M|\mTRANSF\s+ENTRE\s+CTAS|\mTRANS\s+ENTRE\s+CTAS|\mMISMO\s+(CLIENTE|TIT)'
        THEN 'EXCLUDE_INTERNAL'
      WHEN tt.description ~* '\mREINTEGRO\M|\mCANCELACI(O|Ó)N\M|\mREVERSI(O|Ó)N|\mREVERSO\M'
        THEN 'EXCLUDE_REVERSAL'
      ELSE 'KEEP'
    END                                                      AS txn_class
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
),
ranked AS (
  SELECT
    bank, code, direction, transaction_date, amount_ves, description, reference_code,
    ROW_NUMBER() OVER (PARTITION BY bank_id, SIGN(amount_cents) ORDER BY random()) AS rn
  FROM classified
  WHERE txn_class = 'KEEP'
)
SELECT bank, code, direction, transaction_date, amount_ves, description, reference_code
FROM ranked
WHERE rn <= 100
ORDER BY bank, direction, rn;


-- =====================================================================
-- Q3-K — RIF / Cédula presence rate per bank × direction (KEEP only)
-- =====================================================================
-- Detects any V/E/J/G/P prefix followed by 6-10 digits (with or without
-- dash). Uses the v3 classifier so out-of-scope rows (card POS, fees,
-- internal moves, reversals) don't dilute the percentage.
--
-- Scoring rule of thumb for the Notion playbook:
--   ≥ 90 %  → COMPLETO
--   30 – 90% → PARCIAL  (often: bank ships RIF on intrabank but not on
--                        pago móvil; cross-check Q2-K to know which)
--   <  30 % → NO
--
-- Caveat: false positives possible (any V<digits> string). If a bank's
-- pct looks suspiciously high, eyeball Q2-K samples to validate.
--
WITH classified AS (
  SELECT
    b.id                                                     AS bank_id,
    b.name                                                   AS bank,
    b.external_bank_code                                     AS code,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.amount_cents,
    tt.description,
    CASE
      WHEN tt.description ~* 'BIOPAGOBDV|LIQUIDACI(O|Ó)N\s+(TDD|TDC|MAESTRO|TARJETA|VENTAS|A\s+COMERCIO|CREDITO|ELECTRON)|LIQUIDACION\s+VENTAS|DEPOS\.ELECTRONI|LIQ\.TARJETA|LIQ\s+(MONEDERO|TARJETA|TDD|TDC)|COM/LIQ/(TDD|TDC)|LQ\s+(TDD|TDC)\s|N/?C\s+LIQUIDACION\s+MAESTRO|N/?D\s+COM\.\s+LIQUIDACION\s+MAESTRO|CANCELACION\s+RESUMEN\s+DE\s+VENTAS|ABONO\s+COMERCIO\s+POR\s+TARJETA|COMPRA\s+POS|TDB\s+CAPIT|TD\s+POS|C\.O\.TPV'
        OR tt.description ~* '\mL/POS\M'
        OR tt.description ~* '\mPOS\s*:|\mPOS\s+(DEB|CR|MA|CREDITO)'
        OR tt.description ~* '\m(TDC|TMD|TT)\s+\d{6,}'
        OR tt.description ~* '\mTD\s+\d{6,}'
        OR tt.description ~* '\mAB\.LOTE\M'
        OR tt.description ~* '\m(TDD|TDC)\M\s*-\s*ADMIN'
        OR tt.description ~* '\mDESCUENTO\s+TARJETA\M'
        OR tt.description ~* '\mINCENTIVO\s+POS\M'
        OR tt.description ~* '\mTC\s+POS\M'
        OR tt.description ~* '\mREEMBOLSO\s+(DE\s+)?COSTOS?\s+POS\M'
        OR tt.description ~* '\mSERVICIO\s+ESPECIALIZADO\s+POS\M'
        THEN 'EXCLUDE_CARD_LIQ'
      WHEN tt.description ~* '\mCOMIS|\mCOM\.|\mCOM\M\s+|\mN/?D\s+COM\M|\mCARGO\s|\mRECARGO\M|\mMTTO\M|\mREI\.ISLR|\mREINTEGRO\s+(COMIS|ISLR)|\mCONTRAPRESTACION|\mCOBRO\s+POR\s+PROCESAMIENTO|\mEMISI(O|Ó)N\s+(DE\s+)?ESTADO|\mC/CUOTA|\mMANTENIMIENTO\s+CTA'
        THEN 'EXCLUDE_FEE'
      WHEN tt.description ~* '\mTRANSF\s+CUENTAS\s+PROPIAS|\mTRASPASO\M|\mTRANSF\s+ENTRE\s+CTAS|\mTRANS\s+ENTRE\s+CTAS|\mMISMO\s+(CLIENTE|TIT)'
        THEN 'EXCLUDE_INTERNAL'
      WHEN tt.description ~* '\mREINTEGRO\M|\mCANCELACI(O|Ó)N\M|\mREVERSI(O|Ó)N|\mREVERSO\M'
        THEN 'EXCLUDE_REVERSAL'
      ELSE 'KEEP'
    END                                                      AS txn_class
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
)
SELECT
  bank,
  code,
  direction,
  COUNT(*)                                                  AS rows_evaluated,
  COUNT(*) FILTER (
    WHERE description ~* '[VEJGP][-]?[0-9]{6,10}'
  )                                                         AS rows_with_rif,
  ROUND(
    100.0 * COUNT(*) FILTER (
      WHERE description ~* '[VEJGP][-]?[0-9]{6,10}'
    )::numeric / NULLIF(COUNT(*), 0),
    1
  )                                                         AS pct_with_rif,
  CASE
    WHEN ROUND(100.0 * COUNT(*) FILTER (WHERE description ~* '[VEJGP][-]?[0-9]{6,10}')::numeric / NULLIF(COUNT(*), 0), 1) >= 90 THEN 'COMPLETO'
    WHEN ROUND(100.0 * COUNT(*) FILTER (WHERE description ~* '[VEJGP][-]?[0-9]{6,10}')::numeric / NULLIF(COUNT(*), 0), 1) >= 30 THEN 'PARCIAL'
    ELSE 'NO'
  END                                                       AS playbook_score
FROM classified
WHERE txn_class = 'KEEP'
GROUP BY bank, code, direction
ORDER BY bank, direction;


-- =====================================================================
-- Q4-K — Account-number presence rate per bank × direction (KEEP only)
-- =====================================================================
-- Detects either:
--   (a) labeled form: "Cta/Cuenta/Nro/N°" preamble + 8+ digits
--   (b) bare form:    16-20 contiguous digits (full VE account format)
--
-- Same scoring buckets as Q3-K (≥90% → COMPLETO, 30-90% → PARCIAL, <30% → NO).
--
WITH classified AS (
  SELECT
    b.id                                                     AS bank_id,
    b.name                                                   AS bank,
    b.external_bank_code                                     AS code,
    CASE WHEN tt.amount_cents > 0 THEN 'CREDIT' ELSE 'DEBIT' END AS direction,
    tt.amount_cents,
    tt.description,
    CASE
      WHEN tt.description ~* 'BIOPAGOBDV|LIQUIDACI(O|Ó)N\s+(TDD|TDC|MAESTRO|TARJETA|VENTAS|A\s+COMERCIO|CREDITO|ELECTRON)|LIQUIDACION\s+VENTAS|DEPOS\.ELECTRONI|LIQ\.TARJETA|LIQ\s+(MONEDERO|TARJETA|TDD|TDC)|COM/LIQ/(TDD|TDC)|LQ\s+(TDD|TDC)\s|N/?C\s+LIQUIDACION\s+MAESTRO|N/?D\s+COM\.\s+LIQUIDACION\s+MAESTRO|CANCELACION\s+RESUMEN\s+DE\s+VENTAS|ABONO\s+COMERCIO\s+POR\s+TARJETA|COMPRA\s+POS|TDB\s+CAPIT|TD\s+POS|C\.O\.TPV'
        OR tt.description ~* '\mL/POS\M'
        OR tt.description ~* '\mPOS\s*:|\mPOS\s+(DEB|CR|MA|CREDITO)'
        OR tt.description ~* '\m(TDC|TMD|TT)\s+\d{6,}'
        OR tt.description ~* '\mTD\s+\d{6,}'
        OR tt.description ~* '\mAB\.LOTE\M'
        OR tt.description ~* '\m(TDD|TDC)\M\s*-\s*ADMIN'
        OR tt.description ~* '\mDESCUENTO\s+TARJETA\M'
        OR tt.description ~* '\mINCENTIVO\s+POS\M'
        OR tt.description ~* '\mTC\s+POS\M'
        OR tt.description ~* '\mREEMBOLSO\s+(DE\s+)?COSTOS?\s+POS\M'
        OR tt.description ~* '\mSERVICIO\s+ESPECIALIZADO\s+POS\M'
        THEN 'EXCLUDE_CARD_LIQ'
      WHEN tt.description ~* '\mCOMIS|\mCOM\.|\mCOM\M\s+|\mN/?D\s+COM\M|\mCARGO\s|\mRECARGO\M|\mMTTO\M|\mREI\.ISLR|\mREINTEGRO\s+(COMIS|ISLR)|\mCONTRAPRESTACION|\mCOBRO\s+POR\s+PROCESAMIENTO|\mEMISI(O|Ó)N\s+(DE\s+)?ESTADO|\mC/CUOTA|\mMANTENIMIENTO\s+CTA'
        THEN 'EXCLUDE_FEE'
      WHEN tt.description ~* '\mTRANSF\s+CUENTAS\s+PROPIAS|\mTRASPASO\M|\mTRANSF\s+ENTRE\s+CTAS|\mTRANS\s+ENTRE\s+CTAS|\mMISMO\s+(CLIENTE|TIT)'
        THEN 'EXCLUDE_INTERNAL'
      WHEN tt.description ~* '\mREINTEGRO\M|\mCANCELACI(O|Ó)N\M|\mREVERSI(O|Ó)N|\mREVERSO\M'
        THEN 'EXCLUDE_REVERSAL'
      ELSE 'KEEP'
    END                                                      AS txn_class
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents <> 0
    AND tt.description IS NOT NULL
    AND tt.description <> ''
)
SELECT
  bank,
  code,
  direction,
  COUNT(*)                                                  AS rows_evaluated,
  COUNT(*) FILTER (
    WHERE description ~* '(cta|cuenta|nro|n°)\.?\s*[0-9]{8,}'
       OR description ~ '[0-9]{16,20}'
  )                                                         AS rows_with_account,
  ROUND(
    100.0 * COUNT(*) FILTER (
      WHERE description ~* '(cta|cuenta|nro|n°)\.?\s*[0-9]{8,}'
         OR description ~ '[0-9]{16,20}'
    )::numeric / NULLIF(COUNT(*), 0),
    1
  )                                                         AS pct_with_account,
  CASE
    WHEN ROUND(100.0 * COUNT(*) FILTER (WHERE description ~* '(cta|cuenta|nro|n°)\.?\s*[0-9]{8,}' OR description ~ '[0-9]{16,20}')::numeric / NULLIF(COUNT(*), 0), 1) >= 90 THEN 'COMPLETO'
    WHEN ROUND(100.0 * COUNT(*) FILTER (WHERE description ~* '(cta|cuenta|nro|n°)\.?\s*[0-9]{8,}' OR description ~ '[0-9]{16,20}')::numeric / NULLIF(COUNT(*), 0), 1) >= 30 THEN 'PARCIAL'
    ELSE 'NO'
  END                                                       AS playbook_score
FROM classified
WHERE txn_class = 'KEEP'
GROUP BY bank, code, direction
ORDER BY bank, direction;



-- =====================================================================
-- Q8 — Sub-type breakdown for a single bank (count + value + RIF rate)
-- =====================================================================
-- The headline aggregate % from Q3-K can hide important sub-types. The
-- canonical example: BNC CREDIT shows 2% RIF in aggregate (looks like
-- NO), but that 2% is the LBTR / inter-bank rail that carries the largest
-- single transfers by value. For B2B clients like Purolomo, LBTR rows
-- ARE the cobros that matter — high-value supplier payments.
--
-- This query splits a single bank's volume into transaction sub-types
-- and reports RIF coverage + % of count + % of $ value per sub-type.
-- Run it for any bank where the aggregate Q3-K result feels off.
--
-- Default: BNC CREDIT. Change `b.name ILIKE` and the amount-sign filter
-- to point at any other bank/direction.
--
WITH classified AS (
  SELECT
    tt.description,
    tt.amount_cents / 100.0                          AS amount_ves,
    CASE
      WHEN tt.description ~* 'TRANSFERENCIA RECIBIDA DE\s*:.*POR CUENTA DE'
        OR tt.description ~* '\mLBTR\M|\mLBTRAB\M'        THEN 'LBTR / Inter-bank (BCV rail)'
      WHEN tt.description ~* 'TRANSFERENCIA RECIBIDA DEL\s+BCO\.?\s+NACIONAL\s+DE\s+CREDITO'
                                                          THEN 'BNC Intrabank'
      WHEN tt.description ~* 'CIPOTR|Credito Inmediato Recibido|EMISOR\s*:'
                                                          THEN 'Crédito Inmediato (CIPOTR)'
      WHEN tt.description ~* 'PMPC|PMPP|Abono Pago Movil|\mPago Movil\M'
                                                          THEN 'Pago Móvil (PMPC/PMPP)'
      WHEN tt.description ~* '\mPOS\s*:|Abono Comercio por Tarjeta'
                                                          THEN 'POS / Card'
      ELSE 'Other / Boilerplate'
    END                                              AS subtype,
    tt.description ~* '[VEJGP][-]?[0-9]{6,10}'       AS has_rif
  FROM tesote_transactions tt
  JOIN tesote_accounts ta                     ON ta.id = tt.tesote_account_id  AND ta.discarded_at IS NULL
  JOIN external_service_bank_connections esbc ON esbc.id = ta.external_service_bank_connection_id AND esbc.discarded_at IS NULL
  JOIN banks b                                ON b.id = esbc.bank_id
  WHERE tt.discarded_at IS NULL
    AND tt.amount_currency = 'VES'
    AND tt.transaction_date >= CURRENT_DATE - INTERVAL '90 days'
    AND tt.amount_cents > 0                       -- <<< switch to <0 for debits
    AND tt.description IS NOT NULL
    AND tt.description <> ''
    AND b.name ILIKE 'BNC'                        -- <<< change me
)
SELECT
  subtype,
  COUNT(*)                                                                       AS rows,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)                             AS pct_of_count,
  ROUND(SUM(amount_ves)::numeric, 0)                                             AS total_ves,
  ROUND(100.0 * SUM(amount_ves)::numeric / NULLIF(SUM(SUM(amount_ves)) OVER (), 0)::numeric, 1) AS pct_of_value,
  COUNT(*) FILTER (WHERE has_rif)                                                AS rows_with_rif,
  ROUND(100.0 * COUNT(*) FILTER (WHERE has_rif)::numeric / NULLIF(COUNT(*), 0)::numeric, 1) AS pct_rif
FROM classified
GROUP BY subtype
ORDER BY total_ves DESC;
