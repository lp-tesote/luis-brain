---
title: Week of 2026-05-18 — Product sprint (dogfood = demo)
tags: [strategy, weekly-sprint, product, dogfood, command-center, workstreams]
updated: 2026-05-18
status: active
---

# Week of 2026-05-18 — Product sprint

> **Thesis:** The internal Tesote Finance workspace IS the demo. Sequence: **dogfood → demo → sell.** Everything else is secondary this week.

Daily anchor: [[../daily/2026-05-18]]
Strategy roots: [[../product/tesote-2026-command-center-prd]] · [[project_tesote_command_center]] · [[project_tesote_vs_odoo_split]]

## Workstream map

| # | Workstream | Type | Brief | Owner candidate |
|---|---|---|---|---|
| WS-1 | Finish Connect redesigns | Build | [[../product/connect/redesigns-week-2026-05-18]] | Luis + design |
| WS-2 | Cobros + Pagos on Odoo invoices | Build (heavy) | [[../product/business/odoo-invoices-cobros-pagos]] | Dan + Majo |
| WS-3 | Subscriptions v1 | Build (new) | [[../product/business/subscriptions/v1-brief]] | Dan + Majo |
| WS-4 | VE reconciliation cleanup | Data ops | [[../finance/ve-reconciliation-cleanup]] | Finance (TBD) |
| WS-5 | DR Odoo access + subs routing | Ops + config | [[../ops/dr-odoo-access]] | Luis (access) → Dan (wire) |
| WS-6 | US Odoo + Stripe/QB migration | Ops + setup | [[../finance/tesote-us-odoo/index]] | Luis (drive) |

## Sequencing logic

- **WS-1, WS-2, WS-3** can run in parallel — different surfaces, different code paths
- **WS-4 (VE recon)** is independent and long-tail — start now, run alongside
- **WS-5 (DR access)** is a blocker for **WS-3 part 2** (running our DR subs through Tesote) — start the access request immediately
- **WS-6 (US migration)** is the longest pole; doesn't block this week's internal demo but is required before US subs run through Tesote

## What "done" looks like for the week

Internal demo on Tesote Finance workspace shows:

1. Polished Saldos + Movimientos (Connect) — page-set looks like a product, not a prototype
2. Cobros page lists real Odoo AR invoices, with paperplane to send + status tracking
3. Pagos page lists real Odoo AP bills, with action to mark paid
4. Subscriptions page lists Tesote's own VE subs, billing cycles emitting correctly
5. VE ledger reconciled enough to credibly show Saldos/Movimientos to a prospect without "trust me, the data's behind"

Not required this week: US Odoo live, DR subs migrated. Those are unlocks for week 2-3.

## Treasury integration (the bridge protocol)

Per CLAUDE.md (brain → treasury bridge) and [[feedback_tesote_plan_workflow]]:

1. **Mature the PRD in brain** using `product/_prd-template.md`. The **"Tesote-Plan Intake"** block at top is the contract — `/tesote-plan` reads it mechanically. Status moves `draft → ready-for-tesote-plan` when Open Decisions resolve.
2. **File the Linear PRO-* ticket** (Linear MCP works from anywhere — file from brain, no need to switch repos).
3. **Run `/tesote-plan <Linear URL>` in treasury** → produces `.debugging/plans/<slug>/` with `CONTEXT.md` / `TODO.md` / `DEPENDENCIES.md`.
4. **For prototypes:** pair `/tesote-plan` with `redesign-2026-design-system` in the same treasury session to catch design-system drift.
5. **Then `/implement`** (or hand the plan to Dan).

Build workstreams below are filed as PRDs against the template. Each frontmatter tracks `status`, `linear` URL, and `tesote_plan_dir`. Update those fields as the workstream progresses.

## Open questions (week-level)

- Who owns the VE reconciliation cleanup operationally? Finance lead? Mariel?
- Demo date — internal end-of-week, or rolling-as-ready?
- Subs v1 scope — monthly flat billing only, or do we need prorations + FX from day one (since our own clients have FX'd subs)?
- Tier numbering convention call ([[project_tesote_tier_convention]]) — flag if it shows up in any redesigned page this week

## Update protocol

- Mark workstream `status` in its brief frontmatter: `draft → ready-for-plan → planned → in-progress → done`
- When a workstream's `/tesote-plan` runs, drop the plan path back into the brief
- End-of-week retro lands in [[../daily/2026-05-22]] (or whatever the close-out date is)
