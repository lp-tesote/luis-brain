---
title: Tesote Workspace MCP — feedback & feature requests
tags: [product, ai, mcp, erp, odoo]
updated: 2026-05-12
status: draft
---

# Tesote Workspace MCP — feedback & feature requests

Context: I've been kicking the tires on the `tesote-workspace` MCP server (specifically the `erp_console` resource that drives Odoo). Goal: figure out what's needed to sell this as a standalone product (not just a Tesote feature). Below are the gaps and additions that would unblock the killer demos.

## Summary of what works today

**Reads — solid.**
- `workspace.info`, `account.list`, `transaction.search` (bank-side)
- `bank_connection.status`
- `category.list`, `counterparty.list`, `transaction_rule.list/show`
- `erp_console.list_pipelines`, `invoices`, `partner(s)`, `journals`, `find` (generic by id), `stats`, `recent_audits`

**Writes — mostly works, except ERP mutations are gated.**
- `transaction.categorize`, `assign_counterparty`, `send_receipt_email`
- `transaction_rule.create/update/archive/unarchive`
- `counterparty.create/update/archive/unarchive`
- `sync.trigger`
- `erp_console.*_mutations` (generate_subscription_invoice, post_invoice, send_invoice, match_bsl_to_invoice, match_bsl_to_bill, apply_rate_to_usd_invoice, localize_invoice_periods_es) — **all require `manage_workspace_settings` scope; read-only tokens get blocked.**

## Top-3 gaps blocking "kill it as a standalone product"

### 1. No way to list/search bank statement lines (`account.bank.statement.line`)

This is the single biggest gap. The reconciliation workflow is the centerpiece demo — *"show me unreconciled BSLs from the past N days"* — and today it's impossible to answer without already knowing the BSL IDs.

What exists:
- `erp_console.find` requires a specific `id`.
- `match_bsl_to_invoice` *requires* a `bsl_id` to act on, so the IDs exist server-side — they're just not enumerable.
- I successfully reverse-engineered BSL IDs by walking integer guesses (e.g. 1500, 1700, 1900…), but it's brittle, ~50% of guesses hit `null`, and it doesn't scale past a handful of records.
- `account.bank.statement` returns HTTP 500 on `find` — would have given me `line_ids` to walk.

What's needed:

```yaml
action: erp_console.bank_statement_lines
required:
  - workspace_id
  - pipeline_connection_id
filters:
  - journal_id
  - is_reconciled (bool)
  - partner_id
  - start_date / end_date
  - amount_min / amount_max
  - statement_id
  - limit (default 100)
returns:
  - id, date, amount, currency, partner_id, payment_ref
  - journal_id, statement_id, internal_index, is_reconciled
  - move_id (the underlying account.move)
  - narration (carries the Tesote workspace UUID — see #3)
```

This single action unlocks: reconciliation queues, treasury anomaly detection, FX gain/loss reporting, and end-of-month close workflows.

### 2. Read-only tokens should allow dry-run of mutations

Today, `match_bsl_to_invoice` blocks even when called with `live: "false"`. From the demo / sales angle this is a problem: a prospect on a read-only trial token can't see what *would* happen if they ran a match. They have to take the demo presenter's word that the mutation will work.

Two options to fix:

- **Option A (preferred):** Read-only tokens are allowed to call mutation actions when `live: "false"` is set explicitly. Response returns a structured preview of the diff (which lines would reconcile, which accounts would move, what the residual would be after).
- **Option B:** Add a separate `preview_match_bsl_to_invoice` action that's classified as a read and returns the same diff.

Either gets the killer "watch this match happen" demo working without giving away write access.

### 3. Surface the `TESOTE-{uuid}` linkage as a structured field

Right now every BSL carries `TESOTE-{workspace-tx-uuid}` inside its `narration` HTML — this is the bridge between the Odoo BSL and the Tesote workspace transaction. This is a genuine moat (no Odoo plugin has this) but it's hidden inside an HTML string.

Asks:

- Add `tesote_transaction_id` as a top-level field on BSL records (parse it server-side from narration on import).
- Add the inverse mapping on Tesote workspace transactions: `odoo_bsl_id` field that points to the BSL after import.
- Allow filtering both ways: "find the Tesote tx for this BSL" and "find the BSL for this Tesote tx".

This makes the cross-system reconciliation prompts trivial:
> *"For BSL 1949, show me the original Tesote workspace transaction side-by-side."*

### 4. (Bonus) Surface the `kanban_dashboard` JSON as typed fields

When I pulled bank journals, the actually-useful data was buried inside a JSON-encoded string on `kanban_dashboard`:
- `number_to_reconcile` (unreconciled BSL count for this journal)
- `account_balance` / `last_balance` (current and previous closing)
- `outstanding_pay_account_balance` (suspense account)
- `nb_lines_outstanding_pay_account_balance`
- Daily balance time series (`kanban_dashboard_graph`)

These should be first-class fields on the journal response, or exposed as a `journal.dashboard` action. Today every demo has to JSON-parse a string-encoded blob.

## Smaller asks / paper cuts

- **`stats` returns empty array.** It's listed in `list_resources` but produces nothing useful. Either document what it's supposed to do, fix it, or drop it.
- **`recent_audits` returns empty array.** Same — undocumented, returns nothing.
- **`account.bank.statement.find` returns HTTP 500.** Should be a real read. Even just returning the statement record with its `line_ids` would solve the BSL enumeration problem without #1.
- **`journals` with no `types` filter returns only bank + cash.** Default seems narrow. Default should be all journal types, or at minimum the param's default behavior should be documented.
- **The `find` action's optional `fields` param is documented but I never found a working invocation.** Letting callers request specific fields would massively reduce response size (each `find` on `account.move` is ~6 KB; we usually want ~10 fields).

## Why this matters for the GTM

For Tesote internal use, none of this is blocking — Mariel can click around in Odoo. But to **sell this MCP as "Cursor for accounting"** the killer demo is:

> *"Find every unreconciled customer payment from the past week, match each to its open invoice, and show me what would change in Odoo before I commit."*

That demo needs all four asks above to land:
1. BSL search to find the candidates
2. Dry-run on read-only tokens so prospects can run it
3. Cross-system link (Tesote ↔ Odoo BSL) to show the "MCP is a layer above your stack" pitch
4. Typed dashboard fields so the LLM doesn't fumble parsing JSON strings

## Suggested rollout order

1. **Week 1:** Add `bank_statement_lines.list/search` action (#1). This alone unlocks 80% of the reconciliation demos.
2. **Week 2:** Surface `tesote_transaction_id` on BSLs (#3 — schema-only change, no new logic).
3. **Week 3:** Allow `live: false` mutations on read-only tokens with structured preview (#2).
4. **Week 4:** Convert `kanban_dashboard` JSON to typed fields (#4).
5. **Cleanup:** Fix `stats`, `recent_audits`, `account.bank.statement.find`, and the `fields` selector.

Once #1 + #3 land, the reconciliation demo I tried to do today goes from "10+ guess-the-id `find` calls + null results" to a single clean call.
