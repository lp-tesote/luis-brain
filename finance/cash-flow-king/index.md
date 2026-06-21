---
title: Cash Flow King
tags: [finance, forecasting, product]
updated: 2026-05-13
status: draft
---

# Cash Flow King

Internal budgeting + forecasting practice, with intent to graduate into a Tesote product. See [[../analysis-may-2026]] and the founding conversation framing in [[../../strategy/product-strategy-execution-plan]] (if filed).

## What this is

The forecasting engine: **cadence + amount + category** for each (counterparty, category) pair. April 2026 is the seed dataset. The play is:
1. Build the model internally
2. Dogfood for monthly close + budget vs actual
3. Productize as **Cash Flow King** — forward-looking cash visibility for LATAM SMBs

## Artifacts

- [[april-2026-baseline.html]] — main one-page baseline. Recurring buckets, card breakdown, FX flows, revenue, locked assumptions
- [[april-2026-caja-chica.csv]] — petty cash items pending manual entry into Tesote (Caja Chica account)
- [[april-2026-decisions-and-state]] — categorization decisions, open items, blockers, working assumptions

## Open work threads (state at 2026-05-13)

1. **Card account ingestion** — Rho Credit + Mercury Credit aren't connected to Tesote. ~$14K/mo lump sits in "Credit Cards" bucket. CSVs were imported manually to compute the April breakdown. **Action: connect both accounts to Tesote.**
2. **FX rate tracking** — GANESH OTC rates vary day-to-day. Need a place to capture rate per swap (txn note or separate table). Deferred.
3. **Pago TST ambiguity** — some "Pago TST" rows are payroll, others are employee FX swaps (employee gives USD, gets VES). Waiting on Mariel to confirm per-cédula.
4. **Software Expenses category** — created in Tesote UI 2026-05-13. id: `471a0db1-7c05-4825-b3e2-9fd505f3fc16`.
5. **MCP rule create endpoint** — returns 500. Skip rule creation; use direct `transaction.categorize` for now.

## Related memories

- [[project_payments_10x_bet]] — VES cobros scaling story
- [[reference_finance_db_schema]] — for deeper SQL analysis
- [[project_tesote_command_center]] — where Cash Flow King fits architecturally
