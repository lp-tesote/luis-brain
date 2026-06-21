# Banesco

Evaluating Banesco's **Cargo en Cuenta** as a B2B cobros rail.

## Current state (as of 2026-05-04)

- ✅ **PJ→PJ intrabank (Banesco→Banesco)**: live in production today. Cargo en Cuenta works with PJ payers. Single-OTP via Clave Dinámica handles mancomunadas accounts (validates against the client's registered devices).
- ❌ **PJ→PJ interbank**: not available via API today. Banesco's path forward is **Débito Inmediato**, currently in analysis by TI BBU, ETA Q3 2026 (not committed).
- 🆕 **New product live since week of 2026-04-27**: "Pagos por notificaciones push" / "Solicitar Pago Móvil" — bulk push-notification payment requests via API. Not a true debit pull; complementary collection mechanism with no per-transaction OTP friction. Docs received from Banesco, pending review.

## Implications for Tesote Pay

- Cargo en Cuenta is validated as the B2B intrabank cobros rail at Banesco. Ready to scope integration.
- Interbank debit at Banesco is a gap. Either wait for Débito Inmediato (Q3 risk) or route through another bank.
- Push-notification product worth evaluating separately as a softer collection UX.

## Pointers

- Linear ticket of record: [PAY-5 — Validate Banesco Cargo en Cuenta as B2B cobros rail](https://linear.app/tesote/issue/PAY-5)
- Banesco contact: Grecia
- Email exchange (2026-05-03 → 2026-05-04): [banesco-response-2026-05-04.md](banesco-response-2026-05-04.md)
- Vendor docs (in `~/Downloads/minuta_api_banesco__tesote_.../`):
  - Cargo en Cuenta v3.3 (May 2025)
  - Manual de Consumo API — Solicitud Pago Masivo
  - Manual de Consumo API — Consulta de Solicitudes de Pagos
  - Presentación del producto — Cobro por notificaciones push

## Next

- [ ] **Pick a slot for the Wed 2026-05-06 call with Grecia** (9:00 AM or 11:00 AM offered) and send meeting link
- [ ] Prep the call: agenda is strategic — does Banesco want to be the consolidator (interbank PJ debit), or do we design around them? Decide what signals would keep them in the running.
- [ ] Read the three new docs (Solicitar Pago Móvil + Cobro por notificaciones push)
- [ ] Decide whether to scope Cargo en Cuenta integration for B2B intrabank cobros
- [ ] Track Débito Inmediato Q3 ETA with Grecia
