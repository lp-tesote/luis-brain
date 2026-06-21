---
title: Banesco Rails — Cobros Readiness
tags: [cobros, banesco, payments, 10x]
updated: 2026-05-10
status: draft
---

# Banesco Rails — Cobros Readiness

Source: 2026-05-08 call with Banesco (Yeisy Gomez — product head; Grecia Patiño — technical, led the Polar implementation) + 3 docs sent post-call:

- BBU BanescoPagos - Botón de Pago - Instructivo V26 (Jun 2025)
- Instructivo de Recomendaciones y Preguntas frecuentes V10 (Dec 2024)
- Presentación BanescoPagos Interbancario

## Verdict

**Run with it. Build now, QA on the same cadence we're using for BNC.**

The docs cover Botón de Pago Standard + Funcionalidad Interbancaria end-to-end. Empresas Polar — one of the largest food cos in VE — is already using this in production to charge large facturas across multiple bancos pagadores. Grecia led their launch. **Whatever Polar built, we replicate.**

Caveats are real but not blockers:

- Docs may be stale. Trust live behavior over the page. If Polar is pulling juridico → juridico across banks today, the Sudeban "no BB pago móvil" classification gap Yeisy flagged is mostly working in practice. Exceptions will be a handful of banks, not the design.
- Apificada Interbancario is marked "próximamente" in the deck. Doesn't matter if Dan is right that we can inject the same requests directly without rendering Banesco's popup. That bypass is what unlocks Tesote-owned UX in our cobros portal.

## What's actually shippable today

**Botón de Pago Standard + Funcionalidad Interbancaria.** Interbancario activates as a flag flip after Banesco-Banesco certification + masification — **no additional dev** for the interbancario leg per doc 1.

- HMAC-SHA256 signed transactions, API-KEY + SECRETO issued by Banesco
- Sync POST to gateway → async callback POST + optional redirect URLs (callback URL requires static IP + ~15-day BBU authorization)
- API Consulta a Demanda (mandatory) — max 30 req/min, post-pago reconciliation
- Módulo de Transacciones (admin-side batch query) — 3x/day, 6mo retro, 30-day windows per call
- ID Inteligente for matching in estado de cuenta
- QA + Prod environments live (URLs in doc 1, p.19)

Integration playbook from doc 2 — adopt verbatim:

- 3-status state machine: `pending → confirmed/rejected` on callback. Fall back to API Consulta polling every 10min (max 5 retries) when callback doesn't arrive
- Persist callback + consulta responses separately, discriminate by source
- Cédula format `V022772485` — letter + zero-pad to 10 chars
- Don't run client-local; 192.168.x.x kills the callback path

## What we don't have yet

- **Solicitar Pagos API** — launched ~2 weeks before the call, used by Banesco Seguros. Push-style, individual or masivo via API; archivo via BOL/BOLE for non-API clients. **Spec is not in the 3 PDFs.** Grecia owes us these. Pago móvil rails → monto limits → useful for B2C (NET, seguros), not for Central Portuguesa-style B2B.
- **Proper Débito Inmediato** as a clean apificado product (not via botón) — June 2026 target. Yeisy explicitly offered piloting. This is the rail for clean B2B cobros where Tesote owns end-to-end UX without per-bank OTP friction.
- **Domiciliación** — file-based, "arcaico" per Yeisy. Skip.

## Dan's UI bypass thesis

The standard botón embeds Banesco's popup for the auth flow (login → preguntas → clave / OTP). Dan's read: we can probably inject the same backend requests from our own UI, signing the same way `banesco.js` does, and skip the popup.

If true, we lift the UX constraint and own the cobros experience inside Tesote's portal — same advantage Polar got, but on our own canvas. Worth confirming with Grecia in the next technical follow-up. The "apificada" modality presumably already exposes this; question is whether we need to wait for "apificada interbancario" or can do it now over the standard endpoints + interbancario flag.

## Per-bank UX friction (the real tax)

For the interbancario leg, each non-Banesco banco pagador delivers the OTP/clave differently:

- BNC: ingresar al portal y generar clave
- Banesco: SMS, or "Mis Solicitudes" pre-genera 5 claves con TTL 24h
- Mercantil, BBVA Provincial, etc.: each its own flow

Yeisy called this out as the main friction. We can't hide it, but the cobros UX should branch by paying-bank and walk users through it. Polar lives with this; so can our clients.

## Action items

- [ ] Reply to Grecia: thank + request Solicitar Pagos API spec + any other emails Yeisy referenced
- [ ] Draft ficha técnica banco–Tesote–cliente (Yeisy explicitly asked — for her banca comercial and our sales team; doubles as anti-confusion artifact for clients like Abreu)
- [ ] Get Tesote on the Débito Inmediato pilot list — send Yeisy candidate clients (Central Portuguesa, Puro Lomo profile)
- [ ] Spec the integration internally. Mirror the BNC QA cadence Luis already runs
- [ ] If reachable, talk to Polar's eng — fastest path to "what worked, what didn't"
- [ ] Decide upfront: standard JS embed first, or go straight at Dan's direct-injection approach? Lean toward injection if we can validate it cheaply — same code path, much better UX
- [ ] Plan the Banesco-Banesco → masificación → Interbancario activation sequence (the cert step is gating)

## Notes for promotion

Once we start the build and validate Dan's bypass, this becomes promotion candidate for [[knowledge-base/product/cobros/banesco-rails]]. Stays here while in motion.
