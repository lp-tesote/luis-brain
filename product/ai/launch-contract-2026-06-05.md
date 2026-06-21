---
title: Tesote AI — the launch contract
tags: [product, ai, launch, requirements]
updated: 2026-06-05
status: draft
audience: Luis → the organizing frame for the eng comms. Seven behaviors the AI must get right at launch; every bug/fix is derived from one of them.
---

# The launch contract — what Tesote AI must do

> **The inversion.** Instead of leading with 25 bugs, lead with the **7 behaviors** the AI must get right. Every fix in [[bug-register]] is the reverse-engineering of one of these. Eng gets a contract, not a complaint list — and anything that doesn't serve one of these behaviors isn't pre-launch work.

---

## 0. It stays up, and it finishes what it starts

The pre-behavior. No behavior below matters if the surface itself is unreliable.

**Done looks like:**
- No chat query can degrade or take down the app — worst case is "the AI apologizes," never "Tesote is unreachable"
- A pending action confirmation **never dies** — if the conversation hits its limit, the pending approval survives it
- If the AI can't finish, it says so explicitly; it never claims completion with no output

**In the way today:** P1 (the outage — unfiled), P2 (token expiry mid-confirmation — unfiled).

---

## 1. It runs large queries, shows its query logic, and explains the result

The user asks any analytical question — totals, percentages, comparisons, periods — and gets a **complete** answer with the reasoning visible.

**Done looks like:**
- The AI can read past 100 rows (pagination) and, better, **aggregate server-side** — for "¿cuánto gasté en X este año?" the database sums, not the model
- Every numeric answer states its scope: period covered, accounts included, currency, row count — *"sobre 1.432 movimientos, ene–may, 3 cuentas USD"*. If coverage is partial, it says so **before** answering, not under cross-examination
- The result comes with the *why*: what was filtered, what was grouped, what was excluded

**In the way today:** W1+W2 (100-row cap, pagination half-built, "there's more data" signal never reaches the chat), ENG-4016 (re-rank to High). **New ask surfaced by this contract:** a server-side aggregation action (`group by category/counterparty/month`) — was item #4 in the QA fix spec, promotes to first-class here; and the "show your query logic" transparency rule (prompt + answer template — cheap, high trust yield).

---

## 2. It has hard currency boundaries — VES and USD never blur

Without being asked, every time.

**Done looks like:**
- An amount **never appears without its currency**. No bare numbers, anywhere
- Bs and USD are never mixed in one column, one total, or one chart series — mixed datasets split or carry a per-row currency column, automatically
- Aggregations are per-currency by default; cross-currency consolidation only happens explicitly, at a stated rate with the source named (BCV + date)
- **Bs data dollarizes on demand — at the official rate of the transaction's date.** Users will constantly want Bs datapoints/answers in USD terms. The conversion rule: each transaction converts at the **BCV rate of the day it occurred** — never today's rate applied retroactively across history. Every dollarized figure names its basis (*"al BCV de la fecha de cada transacción"*). This is how Luis himself reads the data; it's how every dollarized P&L/cash view in VE has to work to be honest — apply one current rate to old Bs and you're measuring FX drift, not the business
- Asking for a report without hand-picking same-currency accounts doesn't error — the tool groups by currency or tells the AI exactly what to do next

**In the way today:** P3 (mixed Bs/USD table — PRO-154), W8 (multi-currency report errors), the display half of #7154's money work (formatting shipped; the *boundary rules* didn't). **New ask:** dollarization needs a **historical BCV rate by date** lookup (only `exchange_rate.current` is verified on the tool surface today) — and ideally a per-transaction USD-equivalent computed server-side, so dollarized *aggregates* also come from the database (behavior 1), not from the model converting row by row.

---

## 3. The 100-transaction limit dies

Stated alone because it's the single biggest credibility ceiling. Behaviors 1 and 2 are constrained by it; nothing about "large databases" works until it's gone.

**Done looks like:** pagination param shipped (the response side already supports it), the truncation signal arrives on the chat path so the existing guardrail (#7238) can actually fire, and the aggregation action makes most large questions never touch row-by-row reads at all.

**In the way today:** W1+W2 — same fix as behavior 1; held separate here so it's unmissable in the comms.

---

## 4. Reports come out right — and in the format the user wants

**Done looks like:**
- When producing a report, the AI asks — or defaults to **both**: table + chart (both renderers already exist in the working-file system; this is choreography, not new build)
- Every workspace ships with seeded default reports so "córreme el flujo de caja" works in the first session — the library is never empty
- The natural report requests don't hit structural walls: cash flow **by category** exists; "mayo" means May, not a trailing-30-day window; grouping options that don't exist produce an error, not a silent ungrouped answer
- The "sin categorizar" bucket shows loudly (it's ~70% of volume today — and it's the hook into the rules/setup pitch, not something to hide)

**In the way today:** W6 (`cash_flow_by_category` missing), W7 (zero seeded definitions — **the default-report list is ours to pick; Luis is dogfooding today's pre-made reports right now, which IS this task**), W4 (silent date window), W3 (silent group_by no-op), W9/W10 (undocumented presets/filters). **New ask:** the table-or-chart-or-both prompt.

---

## 5. Every action shows its proposed work in the right pane before execution

The universal pattern: **AI proposes → user inspects → user approves → it executes.** Never act first.

**Done looks like:**
- Any mutation — categorizing, rule creation, counterparty edits, anything — renders a preview artifact in the right-hand pane: the table of affected rows, with per-row exclude
- Approve executes exactly what was previewed; the audit trail records proposed-vs-executed
- This pattern already exists for Odoo writes (preview→confirm gate) and in the rules-flow design (the "inspeccionar 47 matches" table with per-row Excluir) — the ask is making it **universal**, including workspace-side bulk operations

**In the way today:** partially built, unevenly applied. **New ask:** declare it the standard for every mutating tool, and audit which workspace-side actions currently skip it. (Behavior 0's P2 is the integrity guarantee this pattern depends on.)

---

## 6. Amounts always render in European format

`1.234.567,89` — periods for thousands, comma for decimals. Everywhere: chat prose, tables, charts, tooltips. Both currencies (`Bs. 5.445.475,00` / `$1.234,56`). One shared formatter, zero hand-formatted money.

**In the way today:** #7154's `Intl.NumberFormat` work is the foundation (VES already renders `Bs.` with `.`/`,` grouping) — **verify USD follows the same convention** and that no surface (prose especially) still hand-formats. Mostly done; needs a sweep, not a build.

---

## What this replaces

The scoreboard in [[launch-readiness-plain-2026-06-05]] still holds for severity calls. But the eng comms leads with this contract: **7 behaviors, each with its derived fix list.** The pitch ([[pitch-today-v2]]) and this contract are the same thing seen from two sides — what we promise customers, and what the product must do to keep the promise.

**Parked (Luis's call):** the smaller UX/UI items (P4 composer, et al.) — collected in [[feature-requests]], not part of the launch contract.

**In motion:** Luis dogfooding today's pre-made reports → output feeds behavior 4 (the seeded default list + format defaults). Append findings to [[qa-pre-created-reports-2026-06-03]].

## New asks this contract surfaced (not in any prior bug doc)

1. **Server-side aggregation action** — promote from QA-spec footnote to first-class (behavior 1/3)
2. **Query-logic transparency rule** — every numeric answer states scope + method (behavior 1)
3. **Table/chart/both choreography** on report output (behavior 4)
4. **Universal preview-pane pattern** for all mutations, incl. workspace-side bulk ops (behavior 5)
5. **European-format sweep** across all surfaces incl. USD (behavior 6)
6. **Historical-rate dollarization** — BCV rate by transaction date + server-side USD-equivalents so dollarized aggregates come from the database (behavior 2)
