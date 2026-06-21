---
title: Cobros + Pagos Powered by Odoo Invoices (Week of 2026-05-18)
tags: [product, prd, business, cobros, pagos, odoo, mcp, week-2026-05-18, ws-2]
updated: 2026-05-18
status: draft
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: [TBD]
tesote_plan_dir: [TBD]
---

# Cobros + Pagos Powered by Odoo Invoices

> **One-line purpose.** Make Cobros and Pagos pages live by surfacing real Odoo invoices (AR + AP) and exposing the full action layer on top of them — so Tesote Finance can run its day-to-day collections and payables from Tesote, not Odoo.

Workstream: [[../../strategy/week-2026-05-18-product-sprint]] · WS-2 (heaviest of the week)

---

## Tesote-Plan Intake

> Tight block — `/tesote-plan` reads it mechanically.

### Actor & Problem

As a **Tesote workspace admin running finance ops (Mariel — internal dogfood)**, I need to **see all unpaid AR invoices in Cobros and all open AP bills in Pagos, and take action on them from inside Tesote** because **today the documents live in Odoo, the action (send, follow up, pay, reconcile) happens in WhatsApp / email / bank portals, and nothing is connected — reconciliation is a manual Excel after-the-fact**.

### The Test

This solves **document-action disconnect** for **finance ops** in **Cobros + Pagos**. Without it: **Mariel keeps living in Odoo + bank portals + Excel, the "Tesote = command center" demo doesn't hold, and we have no credible AR/AP story to sell**.

### V0 — Simplest thing that works

**Cobros (AR side):**

- [ ] Cobros lists all open Odoo AR invoices for the workspace, with: counterparty, invoice number, fecha, monto, moneda, status, days outstanding
- [ ] Reuse Movimientos table primitives — filter system (11 dims adapted to invoice context), stacked totals strip, sticky paperplane action
- [ ] Click row → drill-in slide-over with invoice detail (line items, payment terms, contact info, send history)
- [ ] Paperplane action: send invoice as PDF + payment instructions via WhatsApp / Email / Link (reuse existing send modal pattern)
- [ ] Mark-as-collected affordance — writes back to Odoo to apply payment (manual entry of amount + date + bank account)

**Pagos (AP side):**

- [ ] Pagos lists all open Odoo AP bills for the workspace, with: vendor, bill ref, fecha, monto, moneda, status, due date
- [ ] Same table primitives as Cobros (mirror pattern)
- [ ] Drill-in slide-over with bill detail (line items, vendor bank info if present)
- [ ] Mark-as-paid affordance — writes back to Odoo to apply payment (amount + date + source bank account)
- [ ] **Approval state** before mark-as-paid — single-approver workflow (Luis or Mariel approves; record who approved)

**Shared infra:**

- [ ] Odoo MCP exposes `list_invoices(type, status, workspace)`, `get_invoice(id)`, `apply_payment(invoice_id, amount, date, bank_account_id)`
- [ ] Tesote read-through caches recent invoice list for snappy UI; writes go through to Odoo synchronously
- [ ] Send-history events written to Tesote (not Odoo — per [[project_tesote_vs_odoo_split]], outbound communication is system-of-action)

### Out of Scope (explicit "Not Doing")

- Auto-payment / scheduled payment from a bank rail (Pagos rail integration is WS-2.1+, not V0)
- Bulk payment runs (one-at-a-time mark-as-paid is V0)
- Multi-approver workflows / approval routing (single approver V0)
- AR aging buckets / dunning automation (the UI shows days-outstanding; automation is later)
- FX revaluation (display monto + moneda as Odoo stored; no live BCV math at this layer)
- Partial payments — V0 assumes full-amount mark-as-paid; partial splits deferred
- Bidirectional reconciliation against Movimientos (Connect-side bank txn ↔ AR invoice match) — separate workstream

### Technical Requirements

- [ ] Feature-flagged: `cobros_odoo_live`, `pagos_odoo_live`
- [ ] Permissions: `cobros:read`, `cobros:send`, `cobros:mark_collected`, `pagos:read`, `pagos:approve`, `pagos:mark_paid`
- [ ] Spanish copy throughout
- [ ] Idempotent writes to Odoo — `apply_payment` must be safe to retry (idempotency key = `tesote_payment_event_id`)
- [ ] Multi-tenant safe — every Odoo MCP call scoped by `workspace_id` → Odoo instance + company
- [ ] Audit trail — every send + every payment application = immutable event row in Tesote (`workspace_action_events` or similar)
- [ ] Apply `redesign-2026-design-system` and `database-design` skill checks in `/tesote-plan` session
- [ ] Index planning — invoice list query needs `(workspace_id, type, status, due_date)` composite

### Rollout Plan

1. **Internal** — Tesote Finance VE workspace (Mariel + Luis); verify end-to-end on real Odoo VE data
2. **Beta** — Mariel-equivalent at 1-2 friendly customers (Genica, etc.)
3. **GA** — flag flip, requires per-workspace Odoo connection (covered separately in onboarding)

---

## Context (why now)

This is the load-bearing piece for the "Tesote runs Tesote" dogfood story this week. Per [[../tesote-2026-command-center-prd]], the canonical thesis: **Odoo = system of regulatory record (posted facts), Tesote = system of action (campaigns, agent state, drafts, send events)** — codified in [[project_tesote_vs_odoo_split]]. Cobros and Pagos are the two highest-value action surfaces, and the only way to credibly demo the command-center thesis is to show real Odoo invoices flowing through Tesote with real actions written back.

Existing brain doc: [[cobros/cobros-spec]] (39KB — pre-existing spec, mostly about Banesco rails and AR mechanics). [[cobros/outbound-invoice-routing]] is the closest existing thinking on routing AR invoices to customers. Pagos has less brain coverage; this PRD is the first heavy pass on the AP side.

Trigger for this week: Dan launched **Tesote AI** in the internal workspace (Odoo MCP-backed chatbot). That MCP layer is the spine — Cobros + Pagos extends it from "read-only chat" to "structured read + structured write."

---

## Architecture / Design

```
┌──────────────────────────────────────────────────────────────┐
│  TESOTE (system of action)                                   │
│                                                              │
│   Cobros page          Pagos page                            │
│      │                    │                                  │
│      ├─ table (Movimientos-pattern)                          │
│      ├─ filters (11-dim adapted)                             │
│      ├─ drill-in slide-over                                  │
│      ├─ paperplane (send) / mark-as-collected                │
│      └─ approval / mark-as-paid                              │
│             │                    │                           │
│             ▼                    ▼                           │
│      send_events           payment_application_events        │
│      (Tesote rows)         (Tesote rows — idempotent)        │
│             │                    │                           │
│             └─────── Odoo MCP ───┘                           │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  ODOO (system of regulatory record)                          │
│                                                              │
│   AR invoices    AP bills    Payments    Journal entries     │
│   (live data — Tesote reads + applies payments)              │
└──────────────────────────────────────────────────────────────┘
```

Per-page anatomy mirrors Movimientos v4: filter pills row → totals strip (stacked layout) → table (Manage density, 11/16 padding) → row drill-in.

Cobros-specific columns:

```
Fecha · Counterparty · Factura # · Monto · Moneda · Días vencidos · Status · Envía (✈)
```

Pagos-specific columns:

```
Vencimiento · Vendor · Bill # · Monto · Moneda · Status · Pagar (▶)
```

---

## Surfaces affected

- Negocios → Cobros (new — replaces stub)
- Negocios → Pagos (new — replaces stub)
- Tesote AI chat (no UI change — leverages same Odoo MCP write methods)
- Connect → Movimientos (no change this PRD; future reconciliation link)

---

## Data model implications

**New Tesote tables (per [[project_tesote_vs_odoo_split]] — action state lives in Tesote, not Odoo):**

- `outbound_send_events` — `workspace_id`, `odoo_invoice_id`, `channel` (email/whatsapp/link), `recipient`, `sent_at`, `payload_snapshot`, `sender_user_id`
- `payment_application_events` — `workspace_id`, `odoo_invoice_id`, `direction` (ar/ap), `amount`, `currency`, `bank_account_id`, `applied_at`, `approver_user_id`, `idempotency_key`, `odoo_payment_id` (writeback ref)

**Existing tables impacted:** Counterparty join needed (Odoo partner_id → Tesote counterparty_id) — per [[counterparties/system-of-record]]. May surface a gap if the mapping isn't complete.

**Cross-reference:** [[reference_finance_db_schema]] for canonical Postgres schema; **read before writing SQL** per memory.

---

## AI / automation implications

- Tesote AI gets the new Odoo MCP write methods → user can say *"send invoice 1234 to Genica via WhatsApp"* or *"mark bill 5678 as paid from Banesco Ops"* and the agent calls the same backend the UI does. **Same write path, two surfaces.**
- Future: dunning automation rules (configurable per workspace) → lives in Automatizaciones, fires sends via the same path. Out of scope V0.
- Future: AI-suggested counterparty matching when Odoo partner data is messy. Out of scope V0.

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | Single Odoo MCP for read + write, or separate read/write services? | Dan | Open |
| 2 | Approval workflow — required for V0 or deferred to V1.1? | Luis | Open — recommend: required for Pagos V0 (single approver, low friction) |
| 3 | Counterparty mapping gap — auto-create on first-seen, or block until manually mapped? | Luis / Dan | Open |
| 4 | Send-event channel: actual delivery via Tesote (build the WhatsApp/email rails) or generate-and-share-link (user pastes into their own channel)? | Luis | Open — recommend: generate-and-share-link for V0, real rails in V1.1 |
| 5 | Status taxonomy — adopt Odoo statuses verbatim, or normalize to Tesote vocab (open / partial / paid / overdue)? | Luis / Majo | Open |
| 6 | FX display when invoice currency ≠ workspace base currency — show both, or just invoice currency? | Luis | Open |

---

## Path forward

### V1 wedge

See Intake — V0 covers both pages with the shared infra. The wedge is **one workspace (Tesote Finance VE) demonstrating end-to-end read + send + apply-payment for both AR and AP**.

### What sequences after v1

```
v1   (this week)     — V0 from Intake: list + drill-in + send + apply-payment, single approver
v1.1 (next sprint)   — Partial payments, bulk apply, real WhatsApp/email send rails
v1.2 (post-DR/US)    — Multi-jurisdiction (DR Odoo + US Odoo) — depends on WS-5, WS-6
v2   (post-Movimientos reconciliation) — Bidirectional link: Connect movimiento ↔ AR/AP invoice
v3   (post-rule engine)  — Dunning automation, auto-payment scheduling
```

### Discipline calls

- AR rails integration (Banesco / BNC payment links auto-marking invoices as paid) → defers to V2 reconciliation work. This PRD is **document-action layer only**.
- Don't build a new approval engine — single-approver V0 is hard-coded; multi-approver is V1.1+.
- Don't normalize counterparty data this pass — surface the gap, fix it in counterparty workstream.
- Don't redesign Cobros from scratch — reuse Movimientos primitives.

---

## References

### Internal source docs (this PRD draws from)

- [[cobros/cobros-spec]] — pre-existing AR spec
- [[cobros/outbound-invoice-routing]] — AR routing thinking
- [[cobros/banesco-rails-readiness]] — AR rail layer (out of scope V0, but converges later)
- [[counterparties/system-of-record]] — counterparty mapping
- [[../tesote-2026-command-center-prd]] — architecture root
- [[../ai/tesote-workspace-mcp-feedback]] — MCP design context

### External

- Linear ticket: [TBD]
- Treasury plan dir: [TBD]
- Treasury skills to invoke in `/tesote-plan`: `database-design`, `redesign-2026-design-system`, `product-management`, `using-linear`

### Memory references (load-bearing context)

- [[project_tesote_vs_odoo_split]] — the SoR/SoA rule
- [[project_tesote_command_center]] — architecture root
- [[reference_finance_db_schema]] — schema-first
- [[project_filter_system_primitive]] — table/filter reuse
- [[feedback_no_emojis]]
- [[reference_dan_francoeur_eng]] — Dan for arch decisions

---

## Appendix — Why split Cobros + Pagos in ONE PRD

They share the Odoo MCP plumbing, the table primitive, the drill-in pattern, and the event-row data model. Splitting into two PRDs duplicates planning effort and risks the two surfaces drifting in UX. `/tesote-plan` can phase implementation into AR-first / AP-second within the same plan dir.

Counter-argument considered: different domain experts (Cobros = customer-facing finance, Pagos = vendor-facing). For V0 the JTBD is symmetric (list + drill + action + writeback). Domain divergence kicks in at V1.1 (dunning vs approval routing); split PRDs then.
