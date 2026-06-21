---
title: DR Odoo Access + Subs Routing (Week of 2026-05-18)
tags: [ops, odoo, dr, access, subscriptions, week-2026-05-18, ws-5]
updated: 2026-05-18
status: blocked-on-access
owner: Luis (access request) → Dan (wire-up once unblocked)
---

# DR Odoo Access + Subs Routing

> **Why this is its own workstream.** WS-3 (Subscriptions v1) ships VE-only this week. To complete the "Tesote runs Tesote" story across all entities, we need DR subs running through Tesote too — which requires regaining access to our old DR Odoo instance and wiring it as a workspace source. **Mostly ops, not a build.**

Workstream: [[../strategy/week-2026-05-18-product-sprint]] · WS-5

---

## Job to be done

Get the DR Odoo instance reachable from Tesote — auth, configuration, MCP connection — so:

1. The DR Tesote workspace can read AR/AP/journal entries from DR Odoo
2. The DR Tesote workspace can emit subscription invoices into DR Odoo (per WS-3 architecture)
3. The DR books continue running through Odoo (regulatory record), Tesote acts on top

---

## Step-by-step

### Phase A — Access (Luis-led, this week)

- [ ] Find the DR Odoo instance URL + admin credentials (check 1Password, old emails)
- [ ] Confirm the instance is still alive (it's been dormant — verify hosting still active, no expired billing)
- [ ] Verify what's IN the DR Odoo (chart of accounts, partners, invoices) — anything stale we need to clean up?
- [ ] Reset admin password / create a dedicated Tesote service account

### Phase B — Wire-up (Dan-led, once Phase A complete)

- [ ] Configure DR Odoo as a workspace source in Tesote (per workspace-shell connection flow)
- [ ] Connect the Odoo MCP to the DR instance
- [ ] Verify read paths work (Cobros / Pagos / Movimientos can see DR data)
- [ ] Verify write paths work (test invoice creation via Tesote → DR Odoo)

### Phase C — DR subscription migration (next sprint, depends on WS-3)

- [ ] Inventory active DR subscriptions (currently where? spreadsheet? old Odoo recurring invoice config?)
- [ ] Create each in the Tesote Subscriptions surface (WS-3)
- [ ] Confirm next billing cycle emits correctly into DR Odoo
- [ ] Stop any parallel emission path (so subs don't double-bill)

---

## Out of scope (this week)

- Building a new DR Odoo instance (the existing one is the target — only build new if existing is unrecoverable)
- DR books reconciliation cleanup (parallel to WS-4 VE, but separate)
- Customer DR subscriptions (we're talking about Tesote's own DR subs)
- Migrating Stripe US subs to DR Odoo (that's WS-6 territory + a different jurisdiction)

---

## Open questions

| # | Question | Owner |
|---|----------|-------|
| 1 | Where's the DR Odoo URL + creds? | Luis |
| 2 | Is the DR Odoo instance even still running? | Luis |
| 3 | How many active DR subs do we have today (count + complexity)? | Luis |
| 4 | If the existing DR Odoo is unusable, do we stand up new or kill DR books entirely until later? | Luis (recommend: stand up new in v1.1, don't block this week) |
| 5 | Does TESOTE / TST in DR have a separate legal-entity reference? Cross-check [[reference_tesote_legal_entities]] | Luis |

---

## Why this isn't `/tesote-plan` material

Phase A is pure ops (credentials, hosting check). Phase B leverages **existing workspace-source + Odoo MCP infrastructure** — there's likely zero new code, just configuration. Phase C is a data migration (inventory + create-in-new-surface), which uses WS-3's already-built surface.

**Exception:** if Phase B reveals the workspace-source connection flow doesn't support DR Odoo's specific config (e.g., different chart-of-accounts shape, different XML-RPC quirks), file that as a PRD and run `/tesote-plan`.

---

## Acceptance criteria

- DR Tesote workspace exists, reads DR Odoo data, can create test invoice
- Path to migrating Tesote's DR subs is clear (PRD'd, not necessarily done — sequencing decides)

---

## References

- [[../strategy/week-2026-05-18-product-sprint]]
- [[../product/business/subscriptions/v1-brief]] — WS-3 depends on this for DR coverage
- [[../daily/2026-05-18]]

### Memory references

- [[project_connect_multi_jurisdiction]] — Connect supports VE + Panama + RD + EEUU + Caribe
- [[reference_tesote_legal_entities]] — entity refs
- [[project_tesote_command_center]] — multi-jurisdiction is architectural
