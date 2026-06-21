---
title: Saldos — Implementation Brief
audience: Engineering lead / Dan / tech reviewer
status: promoted
updated: 2026-05-14
version: 1.0
---

> **Promoted to KB** 2026-05-14 → `knowledge-base/product/bank-connectivity/saldos/spec-eng.md`. Edit the KB copy from this point forward.

# Saldos — Implementation Brief

A focused brief for the human eng reviewer. The full granular implementation spec lives in [[spec-agent]] alongside this file — read that for data shapes, edge cases, acceptance criteria, telemetry, etc.

This brief covers **why**, **what's in scope**, **what's not**, and **what to watch for**.

---

## What we're building

A redesign of the Saldos page (formerly *Cuentas* / *Panel de Sincronización*) under Tesote Connect.

**This is the operational trust dashboard for Tesote** — where users go every day to answer two questions: "How much cash do I have, right now?" and "Can I trust this number?" The stakes are unusually high. If users don't trust the saldos on this page, they don't trust anything downstream — cashflow forecast, Pagos decisions, Cobros reconciliation. The whole product loses.

## Why now

Today's UI does the job but accretes confusion:

- 9-column table that crams treasury read + diagnostic + action into one row
- Two trust signals per row (`Estado` dot + `Validación` badge) that the user has to mentally compose
- Per-row sync icons that misrepresent what they trigger (sync is per-connection only, not per-account — clicking sync on one Bancamiga account triggers all three)
- "Validación" column on Saldos is actually about transaction completeness, not balance accuracy — saldos are 99% reliable, so the column dilutes the trust signal where it doesn't apply

The redesign:

- Leads with **cash position** (multi-currency summary cards) — answers the daily question first
- Collapses three per-row trust signals into **one composite Estado badge** with three states
- Surfaces **broken connections at page-level** (banner), not just per-row dots — one connection breaks = many rows affected, so signal once loudly
- Honors the **system constraint** that sync is always per-connection
- **Removes the data-certification badge from Saldos** entirely — it belongs on Transacciones, where transaction completeness is a real concern

## Visual reference

Open the canonical prototype in your browser:

```
luis-brain/product/connect/saldos/prototypes/saldos-v3.html
```

**The HTML is the design contract.** Lunour brand tokens, locked Tesote pill family, system-level archetype rules from `archetypes.md`. Build against this; don't redesign.

## Scope boundary

> **This work touches the Saldos page content area only.** Sidebar, topbar, app shell, global navigation, and any other routes are pre-existing and **must not be modified**. The prototype HTML shows the full app shell for visual context only — slot the new page into the existing layout, don't rebuild around it.

See [[spec-agent]] § "SCOPE BOUNDARY" for the explicit in/out list.

## Scope — what ships in v1

- Saldos page with two views: **Cuentas** (default) and **Conexiones bancarias** (toggle)
- **Cuentas view:** flat list (no grouping in v1), 7 columns, multi-select filters + search, multi-currency totals that recalculate live on filter
- **Conexiones view:** 7 columns including 2FA tag and per-row sync button
- **Attention banner** at page-level aggregating all problematic connections
- Sync triggered per-connection only; button disabled when not applicable
- **3-state Estado on Cuentas:** Sincronizada / Sincronizando / Requiere atención
- **Richer Estado vocabulary on Conexiones:** Activa / Sincronizando / Cambio credenciales / Requiere 2FA / Banco caído / En revisión / Sync falló / Manual

## What doesn't ship — deferred to v2+

- Drill-in slide-over panel (Cuenta detail + Conexión detail with sync history, programación, re-auth, manual notes)
- Empty state full design (first-time user, 0 banks) — render minimal placeholder only
- Connect-new-bank flow, add-manual-account flow, edit-connection flow
- Group-by-banco view (see `saldos-v1.html` for prior exploration; revisit when volume warrants)
- Sticky header, pagination, virtualization, dark mode, mobile

Full out-of-scope list in [[spec-agent]] § "Out of scope".

---

## Key decisions already locked

| Decision | Locked on | Source |
|---|---|---|
| Name = **Saldos** (not "Cuentas" or "Panel de Sincronización") | 2026-05-14 | design.md |
| Validación de data lives on Transacciones, not Saldos | 2026-05-14 | design.md ("Critical clarification") |
| Estado on Cuentas = **3 states** composite | 2026-05-14 | design.md decisions log |
| Sync is **per-connection only**; no per-account sync button | 2026-05-14 | Luis (system constraint — would overload servers) |
| Saldos page has **no global sync CTA**; refresh lives only on Conexiones via per-row buttons | 2026-05-14 | Option A discussion |
| **No sync-all** button anywhere — individual syncs only | 2026-05-14 | Luis (system constraint) |
| Density = **44px standard rows** (manage-a-set archetype) | 2026-05-14 | archetypes.md |
| Visual chrome + tokens = Lunour palette + Inter Tight + Aspekta (Inter fallback) | 2026-05-03 | design.md |

If you want to revisit any of these, do it before kickoff — they have downstream effects.

---

## User context that affects the build

Per Luis (2026-05-14):

- **Volume:** typical customer has **10 connections × 30+ accounts** = 300+ accounts on screen.
- **Multi-currency is the default**, not the exception. VES + USD common; EUR / PAB / DOP possible.
- **Sync API is per-connection only.** No per-account sync exists or will exist.
- **Bank flakiness is the operating reality** — connections expire, banks go down, 2FA gets stuck, syncs fail. Make these first-class states, not edge cases.
- **Trust is the value prop.** Validation, sync recency, connection health all converge on "can I trust this number?" — the design pulls those threads together.

---

## Risks and tradeoffs to flag

| Risk | Mitigation |
|---|---|
| 300+ rows in a flat list could feel overwhelming at higher tiers | Filters + search are first-class; group-by-banco is the v2 escape valve |
| Polling for sync state could overload backend at customer scale | Confirm acceptable polling load with eng; consider SSE/WebSocket if 3s polling is too much |
| Currency cards must stay in sync with table filters — easy to forget | AC-2 and AC-3 in spec-agent.md test for this explicitly; add unit + integration tests |
| Multi-currency totals during partial-failure can confuse users | Banner pattern + "filtrado" badge handle the v1 case; per-currency confidence indicators deferred to v2 |
| 2FA "Auto" tag implies Tesote automates 2FA — confirm we actually do for the connections shown | Validate with Dan / Connect eng before promising this in UI |
| Per-row sync button can be smashed repeatedly causing duplicate jobs | Server-side: 409 on concurrent sync. Client-side: immediate disable + polling reuses existing job |

---

## Open questions to resolve before kickoff

1. **Framework / styling solution** — presumably matches existing `tesote-workspace`. Confirm the stack with Dan.
2. **Exact API endpoint paths** — confirm against treasury repo (`/api/v1/saldos`, `/api/v1/connections/:id/sync`, `/api/v1/sync-jobs/:id` are placeholders).
3. **Polling vs SSE/WebSocket** for sync state updates.
4. **EUR card behavior** when zero accounts — show with `€0.00` or hide entirely?
5. **BCV rate source** — served alongside `/api/v1/saldos` or fetched separately?
6. **Row click behavior in v1** (drill-in is deferred — does click do nothing, or show a "próximamente" tooltip)?
7. **Telemetry destination** — Segment, PostHog, GA4?
8. **Feature flag** for staged rollout?
9. **Is "Tesote automates 2FA"** an actual capability for the connections we'd show as "Auto"? Confirm with Connect eng before that label ships.

---

## Suggested phasing

Not prescriptive — Dan decides. But a reasonable cut:

1. **Phase 1 — static rendering** (this branch): both views, view toggle, banner, currency strip rendering, no interactivity logic
2. **Phase 2 — filters + search + currency recalculation**
3. **Phase 3 — sync interactions** (trigger, poll, state transitions, toasts)
4. **Phase 4 — telemetry + performance validation**
5. **v2+** — drill-in, empty state, grouping

Each phase is independently shippable behind a feature flag.

---

## Related artifacts

- [[design]] — page design rationale, state model, wireframes, decisions log
- [[prototypes/saldos-v3]] — **canonical visual reference** (open in browser)
- [[prototypes/saldos-v1]] — earlier exploration with grouping (reference for v2)
- [[../../design/archetypes]] — list/table archetype + density rules
- [[../../design/design]] — Lunour tokens, pill family, typography
- [[spec-agent]] — full implementation spec for AI agents (granular: data contracts, state machines, acceptance criteria, telemetry)

---

## Review and sign-off

Dan reviews this brief, then dives into [[spec-agent]] for the granular detail. Open questions get resolved with Luis before kickoff. Once locked, this folder gets promoted to the team KB at `knowledge-base/product/bank-connectivity/saldos/`.

---

*Drafted 2026-05-14. Update version + changelog at top when material changes land.*
