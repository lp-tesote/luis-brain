---
title: QA — Pre-created Reports in Tesote AI (running log)
tags: [product, ai, reports, qa]
updated: 2026-06-03
status: draft
---

# QA — Pre-created reports in Tesote AI

Running log of issues from Luis's test session 2026-06-03. Convo IDs from prod. Root causes verified by replaying the same MCP tool surface (`tesote-workspace`) the agent uses — not guesses.

## The headline finding

**A category-based cash flow report is structurally impossible for the agent today.** Every path is blocked:

| Path the agent can try | What happens |
|---|---|
| `report.run` `report_type: cash_flow` | Returns inflow/outflow/net per period only. No category dimension exists. |
| `report.run` with `group_by: "category"` | **Silently ignored** — same uncategorized output, no error. Worst failure mode for an agent: it can believe the result is grouped when it isn't. |
| `report.run` `report_type: cash_flow_by_category` | Doesn't exist. Valid types: `cash_flow`, `balance_over_time`, `balance_changes_by_bank`, `cash_flow_by_counterparty`. |
| Fall back to `transaction.search` + aggregate by hand | Hard 100-result cap, **no pagination, no category filter, no aggregation**. Last 30d across just 3 USD accounts = 116 txns — already over the cap. |

The data is there — `transaction.search` returns `transaction_category_ids` / `names` per row, and `cash_flow_by_counterparty` proves the grouped-report shape already exists server-side. The category variant is just missing.

## Convo-by-convo

### `5a192f50-b3e0-43fd-9d73-65e363c349b2` — did not produce the cash flow reports
Likely compounding causes (couldn't pull the transcript; internal-ops MCP has no ai_conversation resource — gap worth fixing for QA itself):
- **Only 1 saved definition exists** in the workspace ("Flujo de Caja VES - Mensual", created today 12:51 — probably during this same test session). If the convo predates it, "pre-created reports" = zero definitions to run.
- **Mixed-currency default failure**: `report.run` with no `account_ids` errors `"account_ids must share one balance_currency"`. Workspace has 33 accounts across USD/VES/EUR, so the naive call always fails. Error says what's wrong but not what to do next (list accounts → pick same-currency subset).
- **Preset naming trap**: `period: "last_month"` rejected; only `7d/30d/90d/365d/mtd/qtd/ytd/custom`. Natural-language periods don't map; agent must already know the enum.

### `f9003145-249a-48e2-9e95-01cf047f633e` — succeeded but only money in/out
Not an agent failure — that's the ceiling of the tool. `cash_flow` returns `{inflow, outflow, net, tx_count}` per period and nothing else. Also note: Luis had to be very specific to get even that → prompt/UX gap on top of the capability gap.

### `71ec2c5d-0317-4b87-b78f-a6121a2602c9` — pulled from report.run, no categories; 100-tx cap killed the fallback
Exactly reproduces the headline finding above. The agent did the right things in the right order; the surface can't deliver.

## Fix spec (ranked)

1. **Add `cash_flow_by_category` report type** to `report.run` + saved definitions. Mirror `cash_flow_by_counterparty` 1:1 (`top_n`, `direction`, share-of-total %, `null` bucket for uncategorized). One server-side report type unblocks the entire use case — no pagination work needed. *Watch the `null` bucket: in my counterparty run, uncategorized was 70% of volume; same will be true for categories. Surface it loudly, don't hide it.*
2. **Unknown params must error, never silently no-op.** `group_by: "category"` returning ungrouped data without complaint is how the agent confidently reports wrong numbers.
3. **Mixed-currency ergonomics**: when `account_ids` is omitted, either group by currency and return all, or convert via `workspace_exchange_rate` (the override table exists precisely for this). At minimum: actionable error ("pass account_ids of one currency; accounts: …").
4. **`transaction.search`**: add `category_id` filter + `page`/`per_page`, or a `transaction.aggregate` action (`group_by: category|counterparty|month`). Secondary if #1 ships, but the 100-cap with no pagination will bite every other deep-dive use case too.
5. **Period preset aliasing**: accept `last_month`/`this_month` etc., or document the enum in the tool description so the agent sees it before calling.
6. **Pre-created definitions seeding**: if "pre-created reports" is the product promise, workspaces need seeded definitions (the agent can only run what `list_definitions` returns).

## Next move

Eng-facing → this goes through `/tesote-plan` in treasury, not KB promotion. PRD-ify with `product/_prd-template.md` intake block + file PRO-* ticket. Skills the run should pull: `database-design` (report type + aggregation), `product-management`.

— *(append new convo IDs below as testing continues)*
