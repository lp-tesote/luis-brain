---
title: Session 2026-05-10 — Banesco rails kickoff
tags: [cobros, banesco, payments, session-log]
updated: 2026-05-10
status: complete
---

# Session 2026-05-10 — Banesco rails kickoff

## Context

Luis attached the 3 PDFs Banesco sent post the 2026-05-08 call (Yeisy Gómez + Grecia Patiño) and asked for a review against the Fireflies transcript. Goal: figure out if the bundle is enough to start the cobros integration and decide how to move.

## What we worked through

- Reviewed the 3 PDFs (Botón de Pago Instructivo V26, Recomendaciones V10, Presentación BanescoPagos Interbancario) + Fireflies transcript of the call.
- Verdict: bundle is sufficient for **Botón de Pago Standard + Funcionalidad Interbancaria** end-to-end. Polar uses this in prod across paying banks; Grecia led their implementation. Replicate.
- Caveats surfaced: apificada interbancario marked "próximamente"; Solicitar Pagos API referenced in the call but spec not in the bundle (Luis later confirmed: the 3 PDFs *are* the bundle); clean Débito Inmediato product = June 2026 horizon, pilot slot offered.
- Strategic moves Luis decided:
  - Start build now, **both rails** (Banesco-Banesco + Interbancario) from day one — not the sequential cert-then-masificación path the doc suggests.
  - Trust live behavior over potentially-stale docs (Polar is the proof point).
  - Dan's UI bypass thesis: flag to Dan but de-prioritize. **Rails working > Tesote-owned UX.** Default to standard JS embed if bypass isn't trivial.
  - QA cadence: same as BNC.

## Artifacts produced

- [[banesco-rails-readiness]] — working note: verdict, what's shippable today, gaps, Dan's bypass thesis, per-bank UX friction, action items.
- **PAY-5** closed (Done) — superseded by PAY-8 + PAY-9. Closing comment summarizes the cross-call resolution.
- **PAY-8** created — Daniel (eng), High, Payments team. Start integration: read 3 docs, assess UI bypass, integration plan + ETA. Heads-up on static-IP + ~15-day BBU authorization for callback URL.
- **PAY-9** created — Luis, High, Payments. Bank-side coordination: email kickoff (sent), planilla, sesión técnica, credentials, OTP matrix follow-up, ficha técnica, Débito Inmediato pilot tracking.
- Slack draft in `#payments` — kickoff announcement linking to PAY-8.
- Email to Yeisy + Grecia — **sent**. Asks: per-bank OTP matrix for interbancario, formal onboarding (planilla + sesión técnica + credenciales QA), path to prod creds for TST or VDT account testing.

## Memory updates

- `project_banesco_cobros_status.md` — Banesco rails are the cobros build path, Polar in prod, replicate.
- `reference_vdt_testing_entity.md` — VDT is cousin company (Roberto), holds accounts at most VE banks, default for cross-bank prod testing.

## Open loops

- Banesco response on the email — matrix + onboarding + prod path
- Dan's read on docs + integration plan
- Ficha técnica still owed to Yeisy (PAY-9)
- Débito Inmediato Q3 2026 pilot list — send Central Portuguesa / Puro Lomo profile when program opens

## Notes for future-me

- Polar's setup per Grecia = standard JS embed ("va inmerso dentro de las páginas web"). If Dan validates the bypass, we go further than Polar.
- Yeisy asked twice for the ficha técnica — own the lead-routing problem on her side, it's downstream goodwill + lead quality.
- "TST or VDT" prod-testing pattern is reusable across other bank rails too.
