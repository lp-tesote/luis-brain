---
title: Banking-Data Reports Catalog — what a pro finance team consumes
tags: [product, dashboard, reports, finance, ai]
updated: 2026-06-03
status: draft
---

# Banking-data reports catalog

> First-principles map of every report a professional finance team derives from **banking data alone** (no ERP/accrual data), by consumption cadence. The "what to build" menu for Dashboard + Automations + AI. Verified against shipped primitives in [[../ai/capability-audit-2026-06-03]].

## The frame

Banking data is the only dataset in finance that is **settlement truth** — everything else (ERP entries, invoices, forecasts) is *claims about money*; the bank feed *is* money. A pro finance team uses that truth for exactly five things:

| # | Use | Nature | Question |
|---|---|---|---|
| 1 | **Position** | stock | How much, where, what currency, which entity? |
| 2 | **Flow** | movement | What moved and why (categorized)? |
| 3 | **Control** | assurance | Is anything wrong — anomalies, duplicates, leaks, stale data? |
| 4 | **Projection** | forward | What happens to position if known patterns continue? |
| 5 | **Evidence** | proof | Prove all of the above to an auditor / board / SENIAT |

Cadence determines the mix:

- **Daily = position + control** — operator ritual (treasurer/analyst), <5 min
- **Weekly = flow + projection** — manager review (controller/CFO)
- **Monthly = flow + evidence + projection** — CFO/CEO/board pack

## Daily pack — "Posición Diaria"

➡️ Spec'd in [[daily-position-pack-prd]] — first build.

| Report | Content | VE twist |
|---|---|---|
| Posición de caja | Balance by bank × currency × legal entity, USD-consolidated at today's BCV, Δ vs yesterday | **Δ decomposed into flows vs FX revaluation** — a VES balance loses USD value daily with zero transactions. Separating "we spent money" from "the bolívar moved" is the single most valuable daily number in VE |
| Movimientos de ayer | Txns above threshold, new counterparties | Multi-bank: 10+ VE banks in one view is itself the product |
| Excepciones | Uncategorized count, unknown counterparties, out-of-band amounts, duplicate suspects | Feeds the rule-creation loop |
| Frescura de datos | Per-connection sync recency, stale banks flagged | Blocked by the `last_synced_at: null` bug ([[../ai/capability-audit-2026-06-03]] § 3.4) |

## Weekly pack — controller review

| Report | Content |
|---|---|
| Semana en revisión | In/out/net by category vs prior week, biggest movers first |
| Próximos 7–14 días | Expected recurring debits/credits (detected from history) → projected balance trajectory, minimum-balance warnings |
| Top counterparties | Concentration both directions |
| Hygiene digest | % categorized, rule coverage, "pattern seen N× — make it a rule?" |

## Monthly pack — CFO/CEO/board

| Report | Content |
|---|---|
| Cash flow statement (direct) | By category, per currency + USD-consolidated, MoM variance. What Mariel hand-builds today; what [[../../finance/analysis-may-2026]] approximates |
| Burn & runway | Net burn ex-internal-transfers ex-exchange-ops; fixed vs variable via recurrence detection; runway at current burn |
| FX & fees | Devaluation cost on VES holdings, exchange-operation spread cost, **total bank commissions** (VE banks nickel-and-dime — comisión mantenimiento, SMS, resguardo efectivo are real rows in our own data). Nobody totals this; great "Tesote found this" moment |
| Counterparty ledger | Per-vendor/client monthly + YTD totals — negotiation ammo, dedupe input |
| Internal-transfer recon | Transfers-out ≡ transfers-in across own accounts; residual = miscategorization. Integrity check that makes every other report trustworthy |
| Close/audit export | Full categorized ledger CSV with rule provenance per txn |

## Primitives: have vs missing

**Shipped & verified (2026-06-03):** `balance_over_time` (daily per-account series), `exchange_rate.history` (BCV daily), `transaction.search`, `cash_flow` / `balance_changes_by_bank` / `cash_flow_by_counterparty` report types, categories, rules, counterparties, legal-entity tagging on accounts.

**Missing (each unlocks multiple reports):**

1. **Δ-decomposition (flows vs FX)** — pure math over shipped data; not exposed anywhere. → daily pack header
2. **Recurrence detection** — → weekly look-ahead, fixed/variable burn split, forecast bridge (job 6)
3. **Anomaly/exception detection** — → daily control loop, weekly digest
4. **Fee + exchange-op analytics** — category-filtered view, nearly free
5. **Scheduled delivery** — everything is pull-only today; daily/weekly packs only create habit if they *arrive*. This is the Automations surface again

**Engine constraints to design around** (from the audit): report engine is per-currency (`account_ids must share one balance_currency`) — consolidation math happens in the pack layer, not the report engine. Date filters ignored without explicit `period`/`preset` param (bug class, filed).

## Build order

1. **Daily position pack** — retention hook (daily habit > monthly report), mostly assembly of verified pieces → [[daily-position-pack-prd]]
2. **Monthly cash flow statement correctness** — fix the § 3 audit bugs so the canonical report is trustworthy
3. **Recurrence detection** — bridge from reporting to forecasting; where the CFO conversation gets strategic

Dogfood loop: Tesote Finance is customer #1 for all three packs — the May analysis + investor-update numbers Luis assembled by hand *are* the monthly pack.

## Tesote AI — Report Library v1 (seed) — 2026-06-14

> The **W7 launch deliverable** (seed the report library so it's non-empty June 22 — "we owe the 3–5 list"). Selection rule: **high-value × buildable on today's MCP surface** ([[../ai/qa-pre-created-reports-2026-06-03]]). A seed set full of blocked reports ships empty — so this leans on what works *now*. Hand to Majo/Dan.

**Seed set (✅ buildable now):**

1. **Posición de caja consolidada** — balance by bank × currency × entity, USD at BCV, Δ vs yesterday. *(base ✅; Δ-decomposition ⚙️ fast-follow)* — the flagship daily habit.
2. **Money in/out by bank** — `balance_changes_by_bank`; multi-bank-in-one-view *is* the product. *(intercompany separation ⚙️ fast-follow)*
3. **Cash flow by currency** — per-currency native; run per currency, present side-by-side. Nearly free.
4. **Top counterparties** — `cash_flow_by_counterparty`, both directions.
5. ⭐ **Bank fees & commissions total** — category-filtered sum; the "Tesote found this" delight + recurring ROI proof (VE banks nickel-and-dime).
6. **% auto-categorized** (health) — surfaces the `null` bucket honestly (~70% in the 2026-06-03 test); drives the rule-creation loop.

**The one eng call — pull `cash_flow_by_category` into launch scope:** highest-value blocked report (a direct cash-flow statement *is* by-category; Luis hit it 2026-06-03). Fix = mirror `cash_flow_by_counterparty` 1:1 ([[../ai/qa-pre-created-reports-2026-06-03]] fix #1). Recommend **launch, not fast-follow.**

**Fast-follow (⚙️ via the `/tesote-plan` PRO ticket the QA doc routes):** anomaly/duplicate detection · internal-transfer detection (→ intercompany separation + recon) · Δ-decomposition (→ FX-vs-flows) · recurrence detection (→ look-ahead, burn/runway) · new-transfer-types.

## Demo "wow" prompts — "this is serious shit"

> Complicated, multi-step, judgment-flavored queries for the **in-room demo** — where the CFO watches the agent do days of work in seconds. Distinct from the seed reports (canned, repeatable); these show *agency*. **Demo rule (close-playbook beat 0): pre-run on the account's real data the night before — never let the magic misfire live.**

**Tier 1 — demo-safe today (run these in the room):**

| Prompt | Why it lands |
|---|---|
| *"¿Por qué me bajó la caja $X el día 15?"* | Agent traces it across banks to the exact transactions. Reliable + shows reasoning live. |
| *"En todos mis bancos y entidades, ¿cuál es mi posición real en USD ahorita — y dónde tengo caja ociosa que debería mover o convertir?"* | Consolidation + idle-cash judgment in one shot. |
| *"¿Cuánto le he pagado a cada banco en comisiones este año, por tipo — y cuál me está sangrando más?"* | Totals the invisible nickel-and-diming nobody tracks. |
| *"Dame mis 10 proveedores por total pagado este año y cómo viene la tendencia — ¿de cuáles dependo más?"* | Concentration + trend = negotiation ammo. |
| *"Mira mis transacciones sin categorizar y propón reglas que yo apruebe."* | Agent does the work + the rule loop; ends with the customer clicking *approve* = engagement, not just watching. |

**Tier 2 — the killers, need the eng unlock** (tease as "esto cae en semanas," or pull `cash_flow_by_category` in). Every one maps 1:1 to a fast-follow primitive above — **the demo roadmap and the report roadmap are the same backlog:**

| Prompt | Why it's a killer | Needs |
|---|---|---|
| *"¿Cuánto de mi cambio de caja este mes fue plata moviéndose de verdad vs el bolívar devaluándose?"* | The single biggest VE wow — separates real spend from FX bleed. | Δ-decomposition |
| *"Búscame cualquier pago que parezca duplicado, o montos muy fuera de lo que normalmente le pago a este proveedor."* | Live leakage catch = the ROI line made real in the room. | anomaly detection |
| *"¿Pasó algo raro en mis cuentas el mes pasado?"* | Open-ended sweep; the agent earns trust by *finding the thing*. | anomaly detection |
| *"A mi burn actual sin transferencias internas, ¿cuánto me queda hasta estar por debajo de $X — y qué débitos recurrentes lo empujan?"* | Where the CFO conversation goes strategic. | recurrence detection |
| *"Con mis saldos en Bs y la tendencia del BCV, ¿cuándo debí haber convertido el mes pasado y cuánto me costó el timing?"* | FX-timing hindsight — quantifies the exact upside you're selling. | rate math |

## Related

- [[daily-position-pack-prd]] — first build, spec'd
- [[../ai/capability-audit-2026-06-03]] — ground truth on shipped primitives
- [[../ai/use-case-taxonomy]] — jobs 5, 6, 10, 11 are the consumers of this catalog
- [[../../finance/cash-flow-king/]] — Luis's own budget/forecast baseline (internal consumer)
