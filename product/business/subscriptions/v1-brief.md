---
title: Subscriptions v1 — Run Tesote's Own Subs From Tesote (Week of 2026-05-18)
tags: [product, prd, business, subscriptions, dogfood, week-2026-05-18, ws-3]
updated: 2026-05-18
status: draft
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: [TBD]
tesote_plan_dir: [TBD]
---

# Subscriptions v1 — Run Tesote's Own Subs From Tesote

> **One-line purpose.** Stand up a Subscriptions surface in Tesote that owns the commerce layer (plan, counterparty, billing cadence, FX terms) and emits invoice cycles into Odoo for accounting — so Tesote can run its own subscriptions from Tesote first, then sell the same surface.

Workstream: [[../../../strategy/week-2026-05-18-product-sprint]] · WS-3

---

## Tesote-Plan Intake

> Tight block — `/tesote-plan` reads it mechanically.

### Actor & Problem

As a **Tesote workspace admin (internal — Mariel; later a multi-entity customer's finance lead)**, I need to **create, manage, and bill recurring subscriptions tied to counterparties — and have Odoo automatically emit the resulting invoices on the right cadence with the right FX** because **today subscriptions live in spreadsheets, Stripe (for US), and ad-hoc Odoo recurring invoices — there's no single subscription record per counterparty, no FX-aware emission, and no way to manage the lifecycle from one place**.

### The Test

This solves **subscription-lifecycle fragmentation** for **finance ops** in **Negocios → Subscriptions**. Without it: **we keep running our own subs through Stripe + spreadsheets, the dogfood demo doesn't include subscriptions, and the canonical Command-Center claim ("counterparty owns subscriptions, Odoo executes accounting") stays a slide instead of working software**.

### V0 — Simplest thing that works

- [ ] Subscriptions page lists all active subs in the workspace, with: counterparty, plan name, monto, moneda, cadence (monthly / quarterly / annual), next billing date, status (active / paused / cancelled)
- [ ] Reuse Movimientos/Cobros table primitives (filter system, stacked totals, drill-in)
- [ ] Create-subscription flow: pick counterparty → pick plan (or define custom) → set monto + moneda + cadence + start date + FX terms (BCV+differential or flat rate) → save
- [ ] **Billing cycle trigger** — scheduled job runs daily, finds subs with `next_billing_date <= today`, generates an invoice draft in Odoo via MCP, marks the cycle emitted in Tesote
- [ ] FX resolution at emission time — if subscription is FX-templated, pull live BCV (per [[../../tesote-2026-command-center-prd]] FX-aware invoice generation), apply differential, set Odoo invoice's base imponible + currency correctly
- [ ] Drill-in: cycle history (every emission), next-N upcoming emissions, lifecycle events (created / paused / resumed / cancelled)
- [ ] Pause / Resume / Cancel actions on a subscription
- [ ] Created subscription invoices show up automatically in **Cobros** (WS-2) — they're AR invoices in Odoo, surfaced same as any other

### Out of Scope (explicit "Not Doing")

- Prorations on plan change mid-cycle (V0 = cancel + recreate)
- Dunning automation on overdue cycle invoices (handled in Cobros surface)
- Self-serve customer portal (customers can't manage their own subs yet)
- Stripe migration of existing US subs (separate workstream — depends on WS-6)
- Auto-collection / auto-charge from a stored payment method (V0 = invoice-only)
- Plan catalog management UI (V0 = plans defined inline per subscription; catalog comes later)
- Tier-based pricing / usage-based pricing (V0 = flat per cycle)
- Multi-entity billing on a single subscription (V0 = one subscription = one billing entity)

### Technical Requirements

- [ ] Feature-flagged: `subscriptions_v1`
- [ ] Permissions: `subscriptions:read`, `subscriptions:create`, `subscriptions:edit`, `subscriptions:cancel`
- [ ] Spanish copy throughout
- [ ] Idempotent billing-cycle emission — `(subscription_id, cycle_number)` is a unique key; job is safe to re-run
- [ ] Multi-tenant safe — every subscription scoped by `workspace_id`; Odoo emission scoped by workspace's Odoo instance + company
- [ ] Audit trail — every lifecycle event + every emission = immutable event row
- [ ] Background job runs in a Sidekiq queue with `lock: :until_executed` per subscription (concurrency safety)
- [ ] Apply `database-design`, `redesign-2026-design-system`, `product-management` skill checks in `/tesote-plan` session
- [ ] Index planning — `(workspace_id, status, next_billing_date)` partial index on active subs for daily trigger query

### Rollout Plan

1. **Internal** — Tesote Finance VE workspace (Mariel + Luis); migrate Tesote's own active VE subs into the new surface; run real billing cycle through Odoo VE
2. **Beta** — 2-3 customers with simple recurring billing (Genica, etc.)
3. **GA** — flag flip; requires Odoo connection per workspace

---

## Context (why now)

Subscriptions is one of the three explicit product targets for this week's dogfood sprint ([[../../../daily/2026-05-18]]). Per the Command Center PRD ([[../../tesote-2026-command-center-prd]] lines 130-131, 277-280, 468-470):

> "Subscription SoR placement: **Tesote (counterparty owns subscriptions). Odoo executes accounting.**"
> "Per-subscription FX rate — BCV+differential template (or custom) as a first-class field."
> "Contract-rooted — contracts uploaded via Inbound flow spawn subscription records here."

The architecture is locked. This PRD is the V1 cut of that architecture — small enough to ship this week, complete enough to dogfood Tesote's own subs through it.

Trigger: we need to demo subs as part of the "Tesote runs Tesote" story. Until our own subs run through Tesote, the demo has a gaping hole.

DR + US subs are gated by WS-5 (DR Odoo access) and WS-6 (US Odoo migration). **V0 ships VE-only** — VE subs is the wedge, DR/US extend after access lands.

---

## Architecture / Design

```
┌──────────────────────────────────────────────────────────────┐
│  TESOTE (system of action — owns subscription state)         │
│                                                              │
│   Subscriptions page                                         │
│      │                                                       │
│      ├─ list (Movimientos-pattern table)                     │
│      ├─ create-subscription wizard                           │
│      ├─ drill-in (cycle history, next-N upcoming, events)    │
│      └─ pause / resume / cancel actions                      │
│             │                                                │
│             ▼                                                │
│      subscriptions table       cycle_events table            │
│      lifecycle_events table   (idempotent per cycle)         │
│             │                                                │
│             ├──> Daily Sidekiq job: find due cycles          │
│             │       resolve FX (BCV + differential)          │
│             │       → Odoo MCP: create_invoice_draft         │
│             │       → mark cycle emitted                     │
│             │                                                │
└─────────────┼────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────┐
│  ODOO (system of regulatory record — executes invoicing)     │
│                                                              │
│   AR invoices (from cycle emission)                          │
│   ↑                                                          │
│   Surfaced back into Tesote Cobros (WS-2)                    │
└──────────────────────────────────────────────────────────────┘
```

Subscription entity (fields, V0):

```
id, workspace_id, counterparty_id
plan_name, plan_description
amount, currency
cadence (monthly | quarterly | annual), cadence_day_of_period
start_date, next_billing_date, end_date (nullable)
status (active | paused | cancelled)
fx_template (bcv_plus_differential | flat_rate | none), fx_params (JSONB)
odoo_product_id (the line item Odoo posts against)
created_at, updated_at, discarded_at
```

---

## Surfaces affected

- Negocios → **Subscriptions** (new top-level page)
- Negocios → Cobros (no UI change — generated invoices flow in via WS-2 list query)
- Counterparty detail page (future) → active subscriptions list (cross-link)
- Tesote AI chat — gains the subscription MCP methods

---

## Data model implications

**New Tesote tables (V0):**

- `subscriptions` (per schema sketch above)
- `subscription_cycle_events` — `subscription_id`, `cycle_number`, `period_start`, `period_end`, `emitted_at`, `odoo_invoice_id`, `amount_emitted`, `currency_emitted`, `fx_rate_applied`, `idempotency_key`
- `subscription_lifecycle_events` — `subscription_id`, `event_type` (created / paused / resumed / cancelled / plan_changed), `actor_user_id`, `occurred_at`, `payload` (JSONB)

**Counterparty schema impact:** counterparty must expose `active_subscriptions` association (read-side). Per [[../counterparties/system-of-record]].

**Cross-reference:** [[reference_finance_db_schema]] for canonical Postgres; **read before writing migration**.

---

## AI / automation implications

- Daily Sidekiq job is the automation engine — pure rule-based, no AI in V0
- Tesote AI chat gets subscription read methods + create / pause / resume (V1.1). V0 = read-only chat
- Future: AI parses an uploaded contract → suggests a subscription record → Mariel confirms → save. Per PRD line 131 ("Contract → subscription translation. AI suggests, human confirms"). **V0 = manual create only**

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | Pricing model V0: flat per cycle only, or include tiered/usage hooks? | Luis | Open — recommend: flat only |
| 2 | FX templates V0: BCV+differential + flat_rate, or richer (BCV-USD, paralelo, custom curve)? | Luis | Open — recommend: BCV+diff + flat_rate; richer is V1.1 |
| 3 | Plan catalog: V0 inline-per-sub, or build catalog day one? | Luis / Majo | Open — recommend: inline V0 |
| 4 | Counterparty must exist before creating subscription, or auto-create? | Luis / Dan | Open — recommend: must exist (forces clean counterparty hygiene) |
| 5 | What happens to upcoming cycles when a subscription is paused mid-period? Skip the next emission or just pause new ones? | Luis | Open |
| 6 | Cycle-day-of-period semantics — "1st of month" vs "30 days from start"? | Luis / Mariel | Open |
| 7 | Emission timing — first-of-period (advance billing) vs end-of-period (arrears)? | Luis / Mariel | Open — recommend: advance billing default, configurable |

---

## Path forward

### V1 wedge

See Intake — V0 is the wedge. **Ship VE-only, manual create only, flat-per-cycle, FX-aware emission, invoice-only collection (no auto-charge).** That's enough to dogfood Tesote's own subs.

### What sequences after v1

```
v1   (this week)         — V0 from Intake (VE-only, manual create, flat pricing, FX-aware emit)
v1.1 (next sprint)       — Plan catalog, contract→sub AI flow, AI lifecycle methods, DR (depends on WS-5)
v1.2 (post-WS-6)         — US subs via new US Odoo instance; Stripe migration starts
v2   (post-Cobros recon) — Auto-collection via stored payment methods + bank rails
v3                       — Prorations, plan changes mid-cycle, dunning rules, self-serve portal
```

### Discipline calls

- No prorations V0 — cancel + recreate covers edge cases
- No auto-collection V0 — invoice-emission is enough for the dogfood demo
- No catalog UI V0 — defining plans inline is fine for our own subs (~handful)
- No multi-entity billing V0 — single entity per subscription
- DR + US subs **explicitly slip** to v1.1+ — they're gated by access/migration, not by this PRD's velocity

---

## References

### Internal source docs (this PRD draws from)

- [[../../tesote-2026-command-center-prd]] — esp. Flow 2 (outbound subscription billing), Subscription owned by Tesote section
- [[../counterparties/system-of-record]]
- [[../cobros/cobros-spec]]
- [[../cobros/outbound-invoice-routing]]
- [[../../../daily/2026-05-18]] — week's priorities

### External

- Linear ticket: [TBD]
- Treasury plan dir: [TBD]
- Treasury skills to invoke in `/tesote-plan`: `database-design`, `redesign-2026-design-system`, `product-management`, `using-linear`

### Memory references (load-bearing context)

- [[project_tesote_command_center]] — architecture root
- [[project_tesote_vs_odoo_split]] — Tesote owns subs, Odoo executes accounting
- [[reference_finance_db_schema]] — canonical schema
- [[project_filter_system_primitive]] — table reuse
- [[reference_dan_francoeur_eng]] — Dan for FX + idempotency calls

---

## Appendix — V0 dogfood inventory

Before the daily-billing-cycle job is turned on for real, inventory Tesote's own active VE subscriptions and create them by hand in the new surface. Use that count + complexity to validate V0 scope. If we have 5 subs all flat-monthly, V0 holds. If we have 30 subs with weird FX + half-year cycles + tiered pricing, V0 doesn't, and we should adjust before building.

**Action for Luis:** list current Tesote VE subs (count, cadence, FX, plan diversity) before `/tesote-plan` runs. This is the cheap pre-flight.
