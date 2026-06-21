---
title: VE Reconciliation Cleanup (Week of 2026-05-18)
tags: [finance, ops, reconciliation, ve, week-2026-05-18, ws-4]
updated: 2026-05-18
status: scoping
owner: TBD (finance lead candidate)
---

# VE Reconciliation Cleanup

> **Why this is its own workstream.** Months of unreconciled VE txns mean the dogfood demo of Saldos / Movimientos / Cobros runs on top of a messy ledger. We can't credibly show "Tesote = finance command center" if reconciliation is visibly broken. This is data ops, not a treasury build — but it gates the demo.

Workstream: [[../strategy/week-2026-05-18-product-sprint]] · WS-4

---

## Job to be done

Reconcile every unreconciled VE bank transaction from the past N months against:

- Odoo journal entries (the regulatory record)
- AR invoices (where the bank movement is a customer payment)
- AP bills (where the bank movement is a vendor payment)
- Internal transfers between Tesote-owned VE bank accounts

End state: **every VE bank txn in the Tesote ledger is either matched to an Odoo entry or explicitly classified as "to investigate."** No silent gaps.

---

## What's blocking the demo today

- Movimientos page shows real bank data — but a chunk of rows have no counterparty, no category, no reconciliation status. Looks unfinished.
- Cobros (WS-2) will surface real Odoo AR invoices — but the "applied payment" link to a bank movement may be missing for months of historical invoices. Aging buckets will look wrong.
- Saldos (WS-1) shows correct balances but the per-account history can't be trusted without a clean ledger.

---

## Scope this week

- [ ] Inventory the gap: count unreconciled txns per bank account, oldest unreconciled date per account
- [ ] Identify the **dominant patterns** of unreconciled rows (e.g., "Pago Móvil receipts with no counterparty," "vendor wires with no matching bill," "BCV-related FX adjustments")
- [ ] Decide cleanup strategy per pattern:
  - **Manual**: small-N high-value rows → finance lead works them by hand
  - **Bulk**: high-N low-value rows → SQL update with rule (e.g., "match by counterparty name + amount + date window")
  - **AI-assisted**: ambiguous rows → use Tesote AI in the workspace (Odoo MCP-backed) to propose matches, human confirms
- [ ] Run cleanup in waves; verify Movimientos page improvement after each wave

---

## Out of scope

- Building new reconciliation tooling in treasury (this is a data op, not a feature build — unless a clear primitive emerges)
- Reconciling DR or US books (covered by WS-5 and WS-6)
- Defining a "reconciliation status" UI badge for Movimientos (was deferred in 2026-05-16 session; revisit only after this cleanup gives us real signal)

---

## Open questions

| # | Question | Owner |
|---|----------|-------|
| 1 | Who owns this operationally? Mariel? A dedicated finance hire? | Luis |
| 2 | What's the unreconciled count today? (need a query against [[reference_finance_db_schema]]) | Luis / Dan |
| 3 | Do we have a Tesote AI prompt template for "propose reconciliation match"? | Dan |
| 4 | How far back do we go? Last 3 months? 6? All-time? | Luis (recommend: last 6 months, surface older as a separate cleanup wave) |
| 5 | Where do we track progress? Linear OPS- ticket? Spreadsheet? | Luis |

---

## Why this isn't `/tesote-plan` material (yet)

`/tesote-plan` produces implementation plans for treasury features. This workstream is **operational** — running SQL queries, manual finance work, AI-assisted matching using existing infra. The treasury codebase mostly already supports reconciliation (per [[reference_finance_db_schema]]); the bottleneck is human + data, not code.

**If** the cleanup surfaces a need for new reconciliation tooling (e.g., a bulk-match UI, a reconciliation report page), file that as a separate PRD and run `/tesote-plan` on it.

---

## Acceptance criteria for "done enough for demo"

- ≥ 95% of VE bank txns from the last 60 days are reconciled or explicitly classified
- Movimientos page shows no obvious "row with everything blank" rows in the default view
- Cobros aging buckets look right when surfacing Odoo AR invoices (WS-2 gate)
- A query like `SELECT count(*) WHERE workspace_id = tesote_ve AND reconciliation_status = 'unmatched'` returns a number the team feels OK saying out loud

---

## References

- [[../daily/2026-05-18]] — week priorities (the plumbing problem)
- [[../strategy/week-2026-05-18-product-sprint]] — workstream map

### Memory references

- [[reference_finance_db_schema]] — read before writing recon SQL
- [[reference_ve_bank_naming]] — bank aliases (BICENTENARIO=BDT etc.)
- [[reference_dan_francoeur_eng]] — Dan for any Tesote-side schema questions
- [[project_tesote_command_center]] — why this matters for the demo
