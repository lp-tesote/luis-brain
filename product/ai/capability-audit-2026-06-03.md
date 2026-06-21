---
title: Tesote AI — live capability audit
tags: [product, ai, mcp, erp, audit]
updated: 2026-06-03
status: draft
---

# Tesote AI — live capability audit (2026-06-03)

Every resource on the `tesote-workspace` MCP probed live against the **Tesote Finance** workspace (33 accounts, active Odoo pipeline at 3mit-org-tesote-v17). Read-only — zero mutations fired. Purpose: ground truth for (a) what we can put in front of customers today, (b) what to fix first, (c) how the [[use-case-taxonomy]] maps to shipped reality.

Companion docs: [[tesote-ai-design]] (surface, 2026-05-20) · [[tesote-workspace-mcp-feedback]] (gap list, 2026-05-12) · [[use-case-taxonomy]] (the 12 jobs).

---

## 1. Verified working today (live-tested)

### Workspace side (bank data)

| Resource | Status | Notes |
|---|---|---|
| `workspace.info` | ✅ | Name, plan, account count |
| `account.list` | ✅ | 33 accounts, **legal-entity tagging works** (TST vs Tesote Technologies Inc filterable in one call) |
| `bank_connection.status` | ✅⚠️ | Works, but every VE webscraper connection shows `last_synced_at: null` while data clearly flows (BSLs through 2026-06-01). Only API connections (Mercury/Chase/Rho) show timestamps. Field bug or genuinely stale — needs eng answer either way, because **the AI can't honestly answer "¿están al día mis bancos?" with this field as-is** |
| `transaction.search` | ✅⚠️ | Rich shape (cents, display strings, category names, counterparty). **But:** returns a bare 100-row array via `manage_resource` — NOT the documented `{items, returned, total, has_more}` envelope. No truncation signal → silent wrong totals on >100-row questions. See § 3 |
| `transaction_rule.list/show` | ✅ | 20+ active rules, full condition shapes (contains / not_contains / amount bands, per-account scoping) |
| `category.list` | ✅ | 26 categories, hierarchical |
| `counterparty.list` | ✅ | 438 counterparties, RIF in `external_identifier` |
| `exchange_rate.current` | ✅ | BCV 558.6436 USD→VES today, `source: global` |
| `workspace_exchange_rate.current` | ✅ | Falls back to global when no override — single-source-of-truth design works as spec'd |
| `cash_flow.statement` | ✅⚠️ | Works **only** with the right incantation. Two traps in § 3 |
| `report.list_definitions / run` | ✅ | Saved "Flujo de Caja VES - Mensual" definition ran correctly: multi-account VES rollup, May totals, respects config dates |
| `erp_console.shape_hints` | ✅★ | Outstanding. VE-fluent: `control_number` vs `ref`, `conversion_rate` multi-currency doctrine, ISLR per-line, command triples, studio-field guards, copy-from-prior-bill pattern. **This is the moat artifact** — no horizontal AI + generic Odoo MCP has this |

### ERP side (Odoo console)

| Action | Status | Notes |
|---|---|---|
| `list_pipelines` | ✅ | 1 active Odoo connection |
| `invoices` | ✅ | Real rows: out_invoice / in_invoice / out_refund, payment_state, residuals |
| `read` (generic) | ✅★ | **BSL enumeration now works** — `account.bank.statement.line` with domain + `fields` + `order` returns clean rows incl. `is_reconciled`. The #1 gap from 2026-05-12 is closed. `fields` selector also works (was a paper cut) |
| `journals` | ✅ | Returns 20 bank journals mapped to chart accounts |
| `stats` | ✅ | Fixed (was empty 05-12). Now: op counts by type × dry_run |
| `recent_audits` | ✅ | Fixed (was empty 05-12). Shows **Mariel actively dogfooding**: dry-run `account.move` creates June 1–3, none flipped live yet |

### Built but unexercised (can't verify end-to-end — no data)

| Resource | State |
|---|---|
| `inbox.*` | Address exists (`bills-{ws-uuid}@automate.tesote.com`) but **`enabled: false`** and zero items. The AP-ingestion flagship is wired and switched off |
| `invoice.*` (Tesote-side) | 0 invoices. Full lifecycle shipped per schema (create defaults `live:false` preview) but never used in this workspace |
| `billing_subscription.*` | 0 subscriptions. Recurring-invoice engine shipped, unused |

---

## 2. The 2026-05-12 gap list — scorecard

| # | Gap | Status today |
|---|---|---|
| 1 | BSL list/search | ✅ **Fixed** via generic `erp_console.read` |
| 2 | Dry-run on read-only tokens | ❓ Untestable with my token (has write scope). Dry-run mechanism itself is alive (`stats` splits by dry_run) |
| 3 | `TESOTE-{uuid}` as structured field | ❌ **Still open.** Confirmed: `tesote_transaction_id` → `Invalid field` on `account.bank.statement.line`; the uuid is still buried in narration HTML |
| 4 | `kanban_dashboard` typed fields | ❌ Still open — `journals` returns minimal fields, no reconcile-count / balance typed fields |
| 5 | `stats` empty | ✅ Fixed |
| 6 | `recent_audits` empty | ✅ Fixed |
| 7 | `fields` selector broken | ✅ Fixed |

Net: **the reconciliation demo blockers are ~70% cleared.** What's left of the killer demo ("find unreconciled payments, match each to its invoice, preview before commit") is #3 — the cross-system link is still string-parsing.

## 3. New defects found today

1. **`cash_flow.statement` fails bare on multi-currency workspaces.** `{workspace_id}` alone → `"account_ids must share one balance_currency"`. And its real filters (`preset`, `start_date`, `end_date`, `granularity`, `account_id`) are **undocumented** — `list_resources` advertises `filters: []`. Any model calling it the obvious way errors out.
2. **`cash_flow.statement` silently ignores `start_date`/`end_date` unless `preset: "custom"` is set.** Asked for May, got a default trailing-30d window (May 5 → Jun 3) — wrong numbers, no warning. With `preset: "custom"` it's correct. This is the worst class of bug for an AI surface: *plausible wrong answer*.
3. **`transaction.search` envelope mismatch.** Typed tool docs promise `{items, returned, total, has_more, next_cursor}`; the `manage_resource` path returns a bare 100-row array. Without `has_more`, the model can't know it's truncated → understated totals. (System prompt says "never use for totals," but the envelope was the belt-and-suspenders.)
4. **`bank_connection.status` → `last_synced_at: null` on all webscraper connections** (data demonstrably flowing). Freshness is unanswerable from the API.
5. *(Self-documented in shape_hints, worth tracking)*: `apply_rate_to_usd_invoice` overwrites `price_unit` instead of setting `conversion_rate` — the hint itself tells the model to avoid the wrapper. Fix or retire.

## 4. Taxonomy → reality map

What the [[use-case-taxonomy]]'s 12 jobs can actually do **today**, on-demand-chat mode only (Automations surface doesn't exist yet — as the taxonomy already concluded):

| Job | Serviceable today | What's blocking the rest |
|---|---|---|
| 1 Close the books | ◐ | BSL read ✅ + match actions exist; cross-system link (#3) still string-parsed; no draft queue |
| 2 Pay vendors (AP) | ◐ | Odoo bill create/post/send all wired with VE fiscal fields; **inbox disabled** = no ingestion leg |
| 3 Collect (AR) | ◐ | Invoice gen + send ✅ (Odoo side); Tesote-side invoice + subscriptions shipped-but-unused; dunning = manual chat |
| 4 Reconcile banks | ✅◐ | Best-covered job: search, categorize, rules CRUD, BSL read, match-to-invoice/bill. Missing: structured link (#3), scheduled pass |
| 5 Cash & FX | ✅ | Rates, overrides, fallback, balances — all verified. Strongest job today |
| 6 Forecast | ✗ | Nothing dedicated; chat can improvise from search+cash_flow but date-filter bug (#2 above) poisons it |
| 7 Tax (SENIAT) | ◐ | shape_hints carries the fiscal fluency (control_number, ISLR, IVA triples); no libros, no receipt-chase infra |
| 8 Regulatory | ✗ | Nothing |
| 9 Master data | ✅ | Counterparty CRUD + external-partner linking + partner resolution doctrine in hints |
| 10 Report up | ◐ | cash_flow + saved reports work (with § 3 caveats); no scheduled assembly |
| 11 Investigate | ◐ | Reads are good enough for ad-hoc; 100-row cap + no envelope hurts deep digs |
| 12 Payroll | ◐ | Rules infra handles the categorization half (the CIOPPS rules are exactly this) |

## 5. What this means for surfacing to customers

1. **Sell jobs 4, 5, 9 today; demo job 2 end-to-end the moment inbox flips on.** Cash/FX, reconciliation grooming, and master data are verified-solid. The AP inbox is the highest-leverage switch sitting at `enabled: false`.
2. **Fix the "plausible wrong answer" class before any external user touches reporting.** Defects 1–3 in § 3 all produce confident wrong numbers, which is fatal for a finance AI's trust story. These are small server fixes (default `preset: custom` when dates present; return the envelope; document filters).
3. **The capability catalog (empty-state chips) should be generated from this audit's ✅ column, not from aspiration.** Anything ◐ gets a chip only for the verified sub-flow.
4. **`recent_audits` is quietly a customer-facing feature.** "Every action my AI took, with dry-run/live split" — that's the audit-trail pitch, already working. Surface it.
5. **Mariel's dry-runs never flipped live (Jun 1–3).** Either trust gap or workflow gap at the confirm step — ask her which before assuming the gate UX is fine. That's the single cheapest piece of design-partner signal available right now.
6. **No sandbox workspace exists to exercise invoice/inbox/billing flows safely.** Verifying them today means mutating Tesote Finance prod. Seeded demo workspace = prerequisite for both QA and sales demos.

## 6. Punch list (handoff candidates)

Eng (small, server-side):
- [ ] `cash_flow.statement`: multi-currency default behavior + honor dates without `preset` + document filters in `list_resources`
- [ ] `transaction.search`: return the envelope on the `manage_resource` path
- [ ] `bank_connection.status`: real `last_synced_at` for webscraper connections
- [ ] BSL `tesote_transaction_id` structured field (gap #3 — last blocker of the recon demo)
- [ ] `apply_rate_to_usd_invoice`: set `conversion_rate` instead of overwriting `price_unit`

Product/ops:
- [ ] Decide inbox enablement (who flips `enabled: true`, for which workspaces)
- [ ] Seeded sandbox workspace for invoice/inbox/subscription QA + demos
- [ ] Ask Mariel why dry-runs aren't being confirmed live
