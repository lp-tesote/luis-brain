---
title: Tesote AI — Bug Register (by conversation)
tags: [product, ai, qa, bugs]
updated: 2026-06-05
status: draft
---

# Tesote AI — Bug register, by conversation

One entry per convo ID so bugs can be called out by pointing at the specific chat (the convo-ID feature from PR #7154). Root causes verified by replaying the `tesote-workspace` MCP surface where noted — see [[qa-pre-created-reports-2026-06-03]] for full repro evidence + the ranked fix spec.

**Append new chats at the bottom. Template at the end.**

---

## `5a192f50-b3e0-43fd-9d73-65e363c349b2`

- **Date:** 2026-06-03
- **Symptom:** Did not produce the cash flow reports at all.
- **Root cause (verified):** compounding tool-surface traps —
  - Workspace had ~zero saved report definitions at convo time (the only one, "Flujo de Caja VES - Mensual", was created mid-test 2026-06-03 12:51). "Pre-created reports" had nothing to run.
  - `report.run` without `account_ids` always errors on mixed currencies (`account_ids must share one balance_currency`) — workspace has 33 accounts across USD/VES/EUR, so the naive call can never succeed. Error says what's wrong, not what to do next.
  - `period: "last_month"` rejected — presets are enum-only (`7d/30d/90d/365d/mtd/qtd/ytd/custom`), natural-language periods don't map.
- **Class:** tool ergonomics + missing seeded definitions (fix-spec items 3, 5, 6)
- **Status:** open

## `f9003145-249a-48e2-9e95-01cf047f633e`

- **Date:** 2026-06-03
- **Symptom:** Had to be very specific to get a cash flow report; succeeded but only money in/out data points — I wanted category-level in/out.
- **Root cause (verified):** that's the tool's ceiling, not an agent failure. `report.run` `cash_flow` returns `{inflow, outflow, net, tx_count}` per period and nothing else; no category dimension exists anywhere in the report surface. Secondary: the "very specific" prompting needed → UX/prompt gap on top of the capability gap.
- **Class:** missing capability — `cash_flow_by_category` (fix-spec item 1)
- **Status:** open

## `71ec2c5d-0317-4b87-b78f-a6121a2602c9`

- **Date:** 2026-06-03
- **Symptom:** Tried to run a category cash flow via `report.run`, which has no categories; fell back to pulling transactions and hit the 100-tx cap. Report never completed correctly.
- **Root cause (verified):** agent did the right things in the right order; the surface can't deliver —
  - `group_by: "category"` is **silently ignored** by `report.run` (no error, same ungrouped output) — agent can believe the result is grouped when it isn't.
  - `cash_flow_by_category` report type doesn't exist (valid: `cash_flow`, `balance_over_time`, `balance_changes_by_bank`, `cash_flow_by_counterparty`).
  - `transaction.search`: hard 100 cap, no pagination, no category filter, no aggregation. 30d across just 3 USD accounts = 116 txns — already over.
- **Class:** missing capability + silent param no-op + tx search limits (fix-spec items 1, 2, 4)
- **Status:** open

## Conv ending `…CDDC` (full ID not captured)

- **Date:** 2026-06-03, dogfood session w/ Mariel
- **Symptom:** Token expiry mid-conversation — recovered on its own once (reads), but blocked confirmation of an adjustment execution.
- **Root cause:** unverified; expiry handling recoverable on reads, fatal on action-confirmation.
- **Class:** session/auth lifecycle
- **Status:** open — ticket for Dan pending (see [[../../daily/2026-06-03]])

## No ID captured — AP diffs report outage

- **Date:** 2026-06-03, dogfood session w/ Mariel
- **Symptom:** <100-record AP diffs report → long "thinking," claimed done with no output, then **the whole app stopped loading on both machines** incl. main page. Looks server-side.
- **Root cause:** unknown — sev-high; one agent query shouldn't make Tesote unreachable.
- **Class:** stability / blast radius
- **Status:** open — ticket for Dan pending (timestamps in [[../../daily/2026-06-03]])

## `b3c6d51f-88ca-45d1-b208-61e386ffe757`

- **Date:** 2026-06-05
- **Symptom:** Things keep getting left hanging — agent starts work / promises output and doesn't close the loop.
- **Root cause:** unverified — candidates: token/turn limits cutting execution mid-task (same family as `…CDDC`?), or agent claiming done without producing output (same pattern as the AP diffs outage convo).
- **Class:** silent failure / task completion
- **Status:** open — earmarked for the consolidated "problem convos" ticket

---

## Template

```md
## `<convo-id>`

- **Date:** YYYY-MM-DD
- **Symptom:** what I saw / expected vs got
- **Root cause:** (verified / hypothesis)
- **Class:** capability gap | tool ergonomics | silent failure | stability | auth/session
- **Status:** open | ticketed (PRO-*) | fixed (PR #)
```
