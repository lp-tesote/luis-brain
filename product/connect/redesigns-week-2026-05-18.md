---
title: Connect Redesigns — Workstream Umbrella (Week of 2026-05-18)
tags: [product, workstream, connect, redesign, week-2026-05-18, ws-1]
updated: 2026-05-18
status: workstream-umbrella
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
---

# Connect Redesigns — Workstream Umbrella

> **Workstream framing.** Close out the Connect redesign sweep (Saldos retrofit + Movimientos drill-in + adjacent polish) so the page-set looks like a shipped product in the internal demo.

Workstream: [[../../strategy/week-2026-05-18-product-sprint]] · WS-1
**This is not itself a PRD** — it's the umbrella. Each child PRD goes through `/tesote-plan` independently.

---

## Child PRDs (one `/tesote-plan` run each)

| PRD | Status | Trigger |
|-----|--------|---------|
| [[saldos/saldos-prd]] | ready-for-tesote-plan | First dry-run target ([[../../daily/2026-05-18]]) |
| [[movimientos/movimientos-prd]] | PRO-152 filed · ready-for-tesote-plan | Drafted 2026-05-19 after reading production `transactions` page; surgical retrofit mirroring saldos discipline. Visual contract locked at [[movimientos/prototypes/movimientos-v7-retrofit]] (40px density, Mercury cents-deemphasis, no avatars/logos, compact totals). Drill-in slide-over + Mercury filter builder deferred to v1.2 / v2. Linear: PRO-152, assignee Dan, parent PRO-57, sibling PRO-145. |
| `empty-states-prd.md` *(maybe)* | not started | Defer until Saldos + Movimientos shipped; may not warrant own PRD |

Each PRD uses `product/_prd-template.md` with the **Tesote-Plan Intake** block filled.

---

## Why these are separate PRDs (and not one bundle)

Per Luis's 2026-05-18 mid-session decision: **smaller surface = cleaner first `/tesote-plan` run, lower review cost.** Saldos is a visual/styling pass — architecture-review checklists should mostly come back as "n/a — read-only surface." That's a low-risk way to validate the workflow before stacking on more complex PRDs.

Bundling Saldos + Movimientos drill-in + empty states into one PRD would force `/tesote-plan` to run architecture review across three different surfaces with different concerns. Separating them keeps each plan dir focused.

---

## Workstream-level framing (what done looks like for the week)

The Connect page-set in the internal demo shows:

1. **Saldos** retrofitted to canonical table-padding tokens (`11/16` Manage density), stacked totals strip (handles 10-digit Bs / 9-digit USD), filter primitive consistent with Movimientos
2. **Movimientos** drill-in slide-over shipped — full description, refs, rail metadata, send history, action affordances
3. **Empty states** acceptable across both pages (first-time / no-data / filtered-to-zero) — quality bar = "no jank in demo"

Not required this week (deferred to next sprint):

- New Connect surfaces (KYC onboarding stays as-is)
- Real bank-stamped description data validation
- Server-backed saved views (localStorage holds for internal demo)
- Drill-in AI affordances ("describe this", "find similar")

---

## Shared context for child PRDs

Every child PRD should reference these as load-bearing:

- [[../design/archetypes]] — canonical table-padding tokens (per-density)
- [[movimientos/design]] — canonical filter system, stacked totals, drill-in pattern (reference impl)
- [[saldos/design]] — Saldos design doc (where v3 left off)
- [[project_filter_system_primitive]] — design-system primitive
- [[feedback_no_emojis]] — inline SVGs only

Treasury skills to pair in the `/tesote-plan` session:

- `redesign-2026-design-system` — catch any drift to Mercury pastels / Tailwind defaults / wrong radii / Inter-without-Tight
- `using-linear` — link the PRD to its PRO ticket
- `product-management` — for the V0 / out-of-scope discipline

---

## Status / next action

- [ ] Luis runs the Saldos dry-run prompt in a fresh brain session → produces `saldos-prd.md`
- [ ] Luis resolves the "Before I run /tesote-plan" decisions
- [ ] File PRO ticket (Linear MCP)
- [ ] `/tesote-plan <URL>` in treasury
- [ ] Review `.debugging/plans/saldos-redesign/CONTEXT.md` + `TODO.md` with Dan
- [ ] If clean → pattern-copy prompt for Movimientos drill-in PRD

---

## References

- [[../../daily/2026-05-18]] — week priorities + workflow codification
- [[../../_workflows/brain-to-treasury]] — how the bridge works end-to-end
- [[../_prd-template]] — the PRD scaffold every child uses
- [[../../daily/2026-05-14]] — Saldos session log
- [[../../daily/2026-05-16]] — Movimientos session log

### Memory references

- [[feedback_tesote_plan_workflow]]
- [[project_filter_system_primitive]]
- [[project_tesote_command_center]]
