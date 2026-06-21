---
title: Tesote US Odoo — Week of 2026-05-18 Commitment
tags: [finance, odoo, us-entity, week-2026-05-18, ws-6]
updated: 2026-05-18
status: scoping
owner: Luis (drive) → Dan (eventual wire-up)
---

# Tesote US Odoo — Week of 2026-05-18 Commitment

> **Why this is its own workstream.** Delaware C-corp (TESOTE TECHNOLOGIES INC.) currently runs on Stripe + QuickBooks. To complete the multi-jurisdiction Tesote-runs-Tesote story, the US needs to switch to Odoo as system of regulatory record. **This week = unblock the 5 open questions; full migration happens later.**

Workstream: [[../../strategy/week-2026-05-18-product-sprint]] · WS-6

Folder context: [[index]] · [[setup-thinking]] (2026-05-12 scoping)

---

## This week's narrow goal

**Move from "paused" to "ready to scope a real plan."** Setup-thinking was paused 2026-05-12 on 5 open questions. Answer them this week.

Not this week:
- Actual Odoo.sh provisioning
- Stripe → Odoo data migration
- QuickBooks → Odoo cutover
- Bank feed wiring

Those land in v1.2 of WS-3 (subscriptions) + a future setup runbook.

---

## The 5 open questions (from [[setup-thinking]])

| # | Question | Who answers | This-week target |
|---|----------|-------------|------------------|
| 1 | What's the source of truth for US-Inc books today? (QuickBooks / spreadsheet / nothing) | Luis | Confirm. Likely QuickBooks. |
| 2 | W-2 employees on US-Inc, or contractors only? | Luis | Confirm. Determines payroll scope. |
| 3 | Cutover date (fiscal-year boundary ideal) | Luis (after Q1+Q2) | Propose a target. |
| 4 | Which US bank(s) hold Tesote Inc accounts today (Mercury? SVB?) | Luis | Confirm. |
| 5 | Is US-Inc the merchant of record on Stripe, or VE? | Luis | Confirm. |

Once these are answered, write a follow-up doc `us-odoo-setup-plan.md` and (depending on shape) either run `/tesote-plan` on it (if it touches new code paths) or treat it as pure ops.

---

## Why this is mostly ops, not a build

- Standing up Odoo.sh = vendor onboarding, not Tesote code
- Stripe/QB → Odoo data migration = scripts + manual reconciliation, mostly one-shot
- Tesote integration only kicks in after the US Odoo exists and has data — that's a workspace-source config (same path as WS-5 DR)
- The actual building work in treasury will likely be:
  - **Multi-jurisdiction MCP** — already in scope per [[setup-thinking]]; this workstream is the trigger to verify the MCP works against a 3rd Odoo instance (after VE + DR)
  - **US subs via the WS-3 surface** — once Odoo US exists and has products configured

---

## Acceptance criteria (this week)

- 5 open questions answered, written into [[setup-thinking]] or a successor doc
- Cutover date proposed (even if tentative)
- Decision on Odoo.sh trial: start the free trial this week, or wait until cutover plan is firm?

---

## Sequencing reminder

WS-6 does **not** block the internal demo this week. The demo runs on VE workspace. WS-6 is the unlock for:
- Including US books in the dogfood story (week 2-3+)
- Running Tesote's US subs through Tesote (depends on WS-3 v1.2)

If WS-6 slips, the demo still holds — just framed as "VE-first, US/DR rolling next."

---

## References

- [[index]]
- [[setup-thinking]] — the 2026-05-12 scoping that this builds on
- [[../../strategy/week-2026-05-18-product-sprint]]
- [[../../daily/2026-05-18]]

### Memory references

- [[reference_tesote_legal_entities]] — TST (VE), TESOTE TECHNOLOGIES INC. (US)
- [[project_tesote_command_center]] — multi-jurisdiction architecture
- [[project_connect_multi_jurisdiction]]
