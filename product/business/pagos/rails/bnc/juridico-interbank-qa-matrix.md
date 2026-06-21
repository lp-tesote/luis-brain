---
title: BNC — Jurídico Débito Inmediato Interbank QA Matrix
tags: [bnc, payments, debito-inmediato, qa, interbank]
updated: 2026-05-10
status: promoted
---

# BNC — Jurídico Débito Inmediato Interbank QA Matrix

> **Promoted to KB on 2026-05-04** (canonical: `knowledge-base/product/tesote-pay/rails/bnc/juridico-interbank-qa-matrix.md`, currently on branch `kb/bnc-qa-matrix`).
>
> ⚠️ **2026-05-10:** brain copy updated with first batch of test runs. KB canonical is on a feature branch and not yet on `main` — propagate the run log to the KB version next time the branch is touched.

Live tracker for the production QA campaign agreed on 2026-05-04 with Julian and BNC. Mirrors the BNC track of [PAY-4](https://linear.app/tesote/issue/PAY-4).

## Why this exists

Meeting decision (2026-05-04, with Julian + BNC team): both flows — **OTP** and **domiciliación** — should work for any payer bank, for both PJ and PN payers. BNC wants Tesote to validate this against the live network. We agreed to run QA in **production**.

This doc is the matrix we'll use to run those tests. Priority is **PJ → PJ interbank pulling** (Tesote Pay's main B2B use case). PN payers are included so we have full coverage of the rail's behavior across the network.

## Scope

- **Recaudador (puller):** Tesote PJ account at BNC.
- **Payers tested (per bank):** one PJ test account, one PN test account.
- **Flows tested:** `OTP` (per-transaction one-time password) and `Domiciliación` (mandate-based recurring debit).
- **Environment:** production.
- **Priority order:** PJ-OTP → PJ-Domic → PN-OTP → PN-Domic.

## Banks under test

Top banks by Tesote relevance + market share, in priority order:

1. Banco de Venezuela (BdV) — the large state-owned bank; not to be confused with Mi Banco / R4
2. BBVA Provincial
3. Mercantil
4. Banesco
5. BNC (intrabank baseline — sanity-check the rail with BNC ↔ BNC before reading interbank results)
6. Bancamiga

## QA matrix

Status legend: `pending` · `pass` · `fail` · `partial` · `blocked`

| #  | Payer bank          | PJ — OTP                              | PJ — Domiciliación | PN — OTP | PN — Domiciliación |
|----|---------------------|---------------------------------------|---------------------|----------|---------------------|
| 1  | Banco de Venezuela  | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 2  | BBVA Provincial     | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 3  | Mercantil           | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 4  | Banesco             | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 5  | BNC (intrabank)     | pass — OTP recibido (2026-05-w1)      | pending             | pending  | pending             |
| 6  | Bancamiga           | pass — OTP + settled (2026-05-w1)     | pending             | pending  | pending             |
| 7  | Bancrecer           | pass — OTP recibido (2026-05-w1)      | pending             | pending  | pending             |
| 8  | Banco Plaza         | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 9  | 100% Banco          | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 10 | Banco Activo        | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |
| 11 | Banplus             | partial — ACCP, sin OTP (2026-05-w1)  | pending             | pending  | pending             |

> **Nota sobre el conteo "12":** se ejecutaron 12 requests contra 11 bancos distintos (Mercantil y BBVA Provincial fueron probados con dos cuentas PJ cada uno; ambas cuentas de cada banco mostraron el mismo comportamiento ACCP sin OTP).

## What we're observing per cell

For every test run, capture:

- **Result:** pass / fail / partial / blocked, with timestamp.
- **OTP delivery:** whether the payer received the OTP, on what channel (SMS / app / email), and from whom (payer's bank vs. BNC).
- **Latency:** time from debit request → OTP received → debit confirmed.
- **Settlement:** whether funds actually moved to the Tesote BNC account, and how long until they were available.
- **Multi-firmante behavior (PJ only):** if the test PJ account has firmas mancomunadas, capture how the flow handled it (which signer got the OTP, whether one OTP was sufficient).
- **Domiciliación enrollment friction:** for `Domic` cells, capture how the mandate is created, who authorizes it, and whether re-authorization is needed per debit.
- **Error codes / rejection reasons** if the test fails or returns unexpected behavior.

## Test runs (log)

> One subsection per executed test. Append as we go.

### Run template

```
**Date:** YYYY-MM-DD HH:MM
**Cell:** [Bank] — [PJ/PN] — [OTP/Domic]
**Tester:** [name]
**Payer account:** [bank, account type, mancomunada y/n]
**Result:** pass / fail / partial / blocked
**OTP channel + sender:**
**Latency (request → OTP → confirm):**
**Settlement (funds visible at):**
**Notes / error codes:**
**Decision impact:**
```

### Batch 1 — PJ → PJ — OTP — semana del 2026-05-04 al 2026-05-10

**Cell:** 11 bancos pagadores PJ (12 cuentas) — todos cell `PJ — OTP`
**Tester:** equipo Tesote
**Recaudador:** cuenta PJ Tesote en BNC
**Environment:** producción

**Resumen de resultados:**
- **Estatus retornado por el riel:** `ACCP` en los 12 requests.
- **OTP recibido por el pagador:** 3 bancos — BNC (intrabank), Bancamiga, Bancrecer.
- **ACCP sin OTP:** 8 bancos — BdV, Mercantil, BBVA Provincial, Banesco, Banco Plaza, 100% Banco, Banco Activo, Banplus.
- **Settlement end-to-end confirmado:** Bancamiga (PJ → PJ interbancario completado, abono visible en cuenta recaudadora BNC).

**Cuentas probadas (con códigos BCV):**
- 0102 Banco de Venezuela — `01020235370000608800` → ACCP, sin OTP
- 0105 Mercantil — `01050632841632133040` → ACCP, sin OTP
- 0105 Mercantil (alt) — `01050632805632097668` → ACCP, sin OTP
- 0108 BBVA Provincial — `01080948780100080448` → ACCP, sin OTP
- 0108 BBVA Provincial (alt) — `01080027760100992431` → ACCP, sin OTP
- 0134 Banesco — `01340031800311161469` → ACCP, sin OTP
- 0138 Banco Plaza — `01380010330100293158` → ACCP, sin OTP
- 0156 100% Banco — `01560030680300985389` → ACCP, sin OTP
- 0168 Bancrecer — `01680001525101139345` → ACCP, **OTP recibido**
- 0171 Banco Activo — `01710011466003199517` → ACCP, sin OTP
- 0172 Bancamiga — `01720902709028169234` → ACCP, **OTP recibido + settled** ✅
- 0174 Banplus — `01740126281264197623` → ACCP, sin OTP
- 0191 BNC (intrabank) — ACCP, **OTP recibido**

**Observaciones / hipótesis:**
- El riel acepta uniformemente (ACCP en 100% de los casos), pero la entrega del OTP es heterogénea entre bancos pagadores. Hipótesis de trabajo: el patrón ACCP-sin-OTP es config del lado del banco pagador (habilitación/configuración del SMS-OTP para PJ), no falla del riel.
- Bancamiga es el primer caso de settlement PJ → PJ interbancario confirmado end-to-end. Convierte la pregunta de "¿este riel funciona para B2B?" a "¿por qué funciona disparejo entre bancos?".
- Bancrecer recibió OTP pero no se confirmó settlement (pendiente de log el siguiente paso).

**Acción tomada (2026-05-10):** mensaje al equipo técnico de BNC por WhatsApp con resumen + 4 preguntas: (1) habilitación per-bank en bancos top, (2) trazabilidad del SMS-OTP del lado de BNC vs receiver, (3) cómo conmutar a domiciliación, (4) documentación BCV de estatus. Mensaje completo en `followup-julian-qa-results-2026-05-10-whatsapp.md`.

**Próximos pasos:**
- Esperar respuesta de BNC para diagnosticar el ACCP-sin-OTP.
- Confirmar settlement con Bancrecer.
- Replicar el batch para PN (persona natural pagadora) en los mismos 11 bancos.
- Apenas se aclare cómo invocar domiciliación, abrir batch de domiciliación PJ.

## Open questions to resolve during QA

- Does BNC's domiciliación require a per-payer enrollment step before the first debit, or is the first OTP-authorized debit also the mandate-creation event?
- For PJ payers with firmas mancomunadas, does BNC's flow currently support multi-OTP, or does it deliver one OTP to a designated signer? (Tied to the multi-sig design question on the [BNC status doc](../../../../drafts/bnc-ach-status.md).)
- Are there bank-specific quirks (e.g., one bank's OTP comes via app push only, another via SMS) that change Tesote's UX?
- For each `fail` cell, is the failure at the BNC rail layer, the payer-bank layer, or BCV/CCE? Determines who we escalate to.

## Next steps

1. Review this matrix with Julian + BNC team — confirm the test list and priority order.
2. Identify Tesote-controlled test accounts (or willing client accounts) at each of the 6 banks for both PJ and PN.
3. Schedule the first batch of QA runs starting with PJ-OTP across the priority banks.
4. **Update [PAY-4](https://linear.app/tesote/issue/PAY-4)** with: meeting outcome, this matrix as the validation plan, and the priority order.

## Related

- Status tracker: [BNC Debit Rail Status](../../../../drafts/bnc-ach-status.md)
- Strategy track: [Product Strategy Execution Plan — Track B.1](../../../../strategy/product-strategy-execution-plan.md)
- Ticket of record: [PAY-4](https://linear.app/tesote/issue/PAY-4)
- Parallel rail validation (Banco Exterior cobros): [cobros-validation-ticket.md](../banco-exterior/cobros-validation-ticket.md)
