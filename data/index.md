---
title: Data
tags: [data, sql, finance]
updated: 2026-04-19
---

# Data

Scratch space for running queries against Tesote's production DB and capturing data-driven findings. Raw SQL, one-off analyses, hunches to verify with data.

## Canonical schema references (outside this repo)

Source of truth lives in `tesote_notebook`, not here:

- **Query context / join graph / conventions:** `/Users/luispulgar/Programming/tesote_notebook/Finance/CLAUDE_CODE_QUERY_CONTEXT.md`
- **Full schema (every column, index, FK):** `/Users/luispulgar/Programming/tesote_notebook/Finance/schema.rb`
- **Example queries:** `tesote_notebook/Analysis/*.sql`, `tesote_notebook/Finance/*.sql`, `tesote_notebook/Product/Liquidity_Pool/*.sql`

Claude: read both files when writing any non-trivial SQL. Don't guess columns.

## Quick orientation (for fast recall — full details in the files above)

- **Engine:** Postgres, Rails app, UUID PKs on most tables.
- **Join backbone:** `workspaces` → `tesote_accounts` → `tesote_transactions`; `tesote_accounts` → `external_service_bank_connections` → `banks`.
- **Money:** `amount_cents` bigint; divide by `100.0` for units. Inflows `> 0`, outflows `< 0`. Currency in `amount_currency` (ISO, e.g. `VES`, `USD`).
- **Time:** `transaction_date` on `tesote_transactions` for windows.
- **Soft deletes:** always `discarded_at IS NULL` unless the question is historical.
- **"Live" accounts:** typically `discarded_at IS NULL`, `archived` false/NULL, `syncable = true`, `account_type != 'manual'`.
- **Sync reliability:** `bank_sync_sessions` joined via `external_service_bank_connection_id`.

## What goes here

- `*.sql` — ad-hoc queries Luis is running or wants Claude to write
- `*.md` — findings, anomalies, "what the data says about X"
- Subfolders by theme if it gets busy (e.g. `data/bnc/`, `data/workspaces/`)

## What does NOT go here

- Polished dashboards / team-facing analyses → promote to the shared KB
- Payment-rail tracker docs → `drafts/` or function folders (e.g. `drafts/bnc-ach-status.md`)
- Production queries the app itself runs → live in the app repo, not here
