---
title: Inicio (Dashboard) — PRD
tags: [product, prd, dashboard, connect, ai]
updated: 2026-06-11
status: filed-as-ticket
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: https://linear.app/tesote/issue/PRO-183/inicio-dashboard-banking-data-command-center-posicion-d-decomposition
tesote_plan_dir: [pending]
---

# Inicio (Dashboard) — PRD

> **One-line purpose.** The Tesote workspace home: a banking-data command center that shows a finance team its consolidated position, this week's money movement, and the few things worth knowing today — with Tesote AI reading the same data beside it.

> **How to read this PRD.** Global design rules (shell, cards, currency display, status pills, affordances, AI panel structure) are **not repeated here** — they live in [[../design/web-app-design-system]] and are cited by section (e.g. "§5 multi-currency"). This PRD is **Inicio-specific**: per-box data contracts, windows, states, interactions, edge cases, and reconciliation. The working visual is **`prototypes/dashboard-v5.html`** (frozen, signed off 2026-06-09); where this PRD and the prototype disagree, **this PRD wins**.

---

## Tesote-Plan Intake

> **Treasury's `/tesote-plan` ingests this block.** Keep tight even if the rest sprawls.

### Actor & Problem

As a **Tesote workspace finance user (Mariel — controller/CFO/AP-AR persona)**, I need to **open the app and see my real-time consolidated cash position, this week's movement, and what changed — across every bank and entity, in USD and Bs — without building it myself**, because **today that picture lives in a manual multi-tab spreadsheet rebuilt by hand: balances pulled per-bank, converted at BCV by hand, with no view of how much of a change was real cash flow vs. devaluación**.

### The Test

This solves **"what's my position and what moved" at a glance** for **a finance team** in **Connect (+ a Tesote AI surface)**. Without it: **the user keeps rebuilding a balances spreadsheet every morning, and the app's home screen is an empty shell that doesn't earn the daily open.**

### V0 — Simplest thing that works

The full dashboard ships, **including the three differentiated primitives** (Luis's call, 2026-06-09 — fuller story over faster ship):

- [ ] **Posición hero**: consolidated USD figure + 30-d delta, a 30-d position chart with beginning-balance marker, a **decomposition band** (Entró · Salió · Variación neta · Devaluación) that reconciles to the chart, **Por moneda** (USD; VES Bs-first with ≈$ beneath), and **Desglose** (por banco + por entidad).
- [ ] **Δ-decomposition engine** computing flujos vs. devaluación vs. ε residual over a window (per [[daily-position-pack-prd]] identity).
- [ ] **Tesote AI panel**: serif voice line + pre-generated week-to-date insight report + 3 prompt buttons + input (read-first; see Box 2).
- [ ] **Entró/salió** (weekly), **% categorización** (30 d), **Nuevo en tus cuentas** (new counterparties / tx types).
- [ ] **Flujo de caja por categoría** (direct method, monthly) — net-new primitive.
- [ ] **Top movimientos** (30 d) and **Saldos por cuenta** (list).
- [ ] **Recurrence detection** feeding "próximos débitos recurrentes" signals (net-new primitive).
- [ ] Workspace identity in header (logo + name), entity switcher in topbar.

### Out of Scope (explicit "Not Doing")

- **Any ERP / accounting data.** No invoices, AR aging, reconciliation-to-invoice, approvals/Bandeja. Everything on Inicio is derivable from the **bank feed** (balances, transactions, FX/BCV, categories, counterparties, sync status). Hard line.
- **Editing from the dashboard.** Inicio reads and links out; categorizing, moving money, approving all happen on their own surfaces. The AI panel is read-first (no write actions in v1).
- **User-customizable layout / drag-drop widgets.** "Personalizar" button is a v1.1+ stub. v1 ships one opinionated layout.
- **Projections / forecasting beyond recurrence.** Cash-flow *projection* (forward) is a reports-catalog item, not Inicio v1. Recurrence detection here only powers a "what's coming" signal, not a full forecast box.
- **Multi-workspace roll-up.** Inicio is scoped to the selected workspace + its entities; cross-workspace consolidation is not v1.

### Technical Requirements

- [ ] Feature-flagged: `flag_dashboard_inicio_v2` (whole redesigned home behind one flag; AI panel sub-flagged `flag_dashboard_ai_panel`).
- [ ] Permissions: respects existing account/entity visibility — a user sees only the accounts/entities they can see; totals reflect their visibility scope.
- [ ] Spanish copy — **VE dialect, `tú`** (per [[feedback_product_ui_spanish_venezuelan]]).
- [ ] Multi-tenant safe (`workspace_id` on all new tables — decomposition snapshots, recurrence signals; no cross-workspace leakage).
- [ ] Idempotent for any background job (daily balance snapshot, decomposition compute, recurrence scan — safe to re-run).
- [ ] Audit trail / soft-delete only for any persisted financial derivation.
- [ ] Design-system constraints from `redesign-2026-design-system` + [[../design/web-app-design-system]]: Lunour tokens, 4/8/12 radii, Geist Mono numbers, Inter Tight display, Instrument Serif = AI voice only, no emojis (inline SVG), borders-not-shadows.

### Rollout Plan

1. **Internal** — Tesote Finance (Mariel) dogfoods on the real Tesote workspace (2 entities: Tesote Technologies Inc. + TST Servicios y Consultoría) → verify every number reconciles to Saldos/Movimientos.
2. **Beta** — N named workspaces with hand-holding → validate decomposition + recurrence on messier real data.
3. **GA** — flag flipped for all. (Bundled into the broader app redesign ship; see [[ai-launch-master-plan]] ~Jun 22 pressure.)

---

## Context (why now)

Three drivers converge:
- **The redesign sweep.** Saldos v4 + Movimientos v7 are done; Inicio is the third and **long-pole** surface, and the AI launch bundles *inside* the redesigned app — so Inicio must design-lock (flagged in [[ai-launch-master-plan]], 2026-06-08).
- **The home screen doesn't earn the open.** Today's dashboard is thin; the daily ritual is a manual balances spreadsheet. Inicio's job is to *be* that spreadsheet, live, plus the "what moved / what's coming" the spreadsheet can't do.
- **The decomposition insight is the wedge.** "Your position went up $31k, but only $33k was real cash flow and devaluación ate $1.9k" is the kind of thing no VE finance team gets automatically and no horizontal tool computes. It's the honest differentiator (ties to [[winning_vs_horizontal_ai]]).

Prototype lineage + the 9-point content inventory: [[prototypes/README]]. Decomposition identity + worked example: [[daily-position-pack-prd]]. Report menu: [[reports-catalog]].

---

## Architecture / Design

### Page layout (dashboard-v5, frozen)

```
topbar:  [entity switcher ▾]························[Mover dinero] [bell]
─────────────────────────────────────────────────────────────────────
page-head:  (logo) Tesote Ventas

ROW 1  grid-hero (1.62fr / 1fr)
┌───────────────────────────────────────┐ ┌─────────────────────────┐
│ BOX 1 · Posición                       │ │ BOX 2 · Tesote AI        │
│  $521.840,17   ▲ +$31.290 · 30 d       │ │  (serif voice line)      │
│  [30-d gradient area chart, begin dot] │ │  Tu semana hasta hoy:    │
│  Entró · Salió · Var. neta · Devaluac. │ │   · insight              │
│  Por moneda: USD | VES(Bs-first ≈$)    │ │   · insight              │
│  Desglose: por banco | por entidad     │ │  [3 prompt buttons]      │
│                                        │ │  [pregúntale… input]     │
└───────────────────────────────────────┘ └─────────────────────────┘

ROW 2  grid-3
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ BOX 3 Entró/ │ │ BOX 4 % cate-│ │ BOX 5 Nuevo  │
│ salió (sem.) │ │ gorización   │ │ en cuentas   │
└──────────────┘ └──────────────┘ └──────────────┘

ROW 3  grid-2 (1.25fr / 1fr)
┌───────────────────────────┐ ┌─────────────────────┐
│ BOX 6 Flujo de caja por   │ │ BOX 7 Top           │
│ categoría (mes, directo)  │ │ movimientos (30 d)  │
└───────────────────────────┘ └─────────────────────┘

ROW 4  grid-1
┌─────────────────────────────────────────────────────┐
│ BOX 8 · Saldos por cuenta (list)                     │
└─────────────────────────────────────────────────────┘
```

### Cross-cutting decisions (resolved here so boxes don't relitigate)

| Decision | Resolution | Why |
|---|---|---|
| **Moneda/Entidad/Banco** — toggle vs. separate | **Separate, always-visible** sub-sections in the hero (Por moneda + Desglose banco/entidad). Toggle killed. | Per §0 always-visible affordances; a toggle hides 2/3 of the breakdown behind a click on the one screen meant for glanceability. |
| **Δ-decomposition placement** | **Hero strip, directly under the chart**, not its own box. | It explains the chart's delta; co-locating makes the reconciliation legible. |
| **Multi-window story** | **Three windows, each labeled, intentional:** position chart + band = **30 d**; Entró/salió = **week** (w/ dates); cash-flow-by-category = **month**; top movs + %cat = **30 d**. | §8 — each box states its window; a single global period would force the wrong frame on at least one box. Decided deliberately, not by query convenience. |
| **Hero ↔ AI height** | AI panel **stretches** to the hero's height; input pinned to the floor via flex spacer. | Keeps the two-column hero visually balanced regardless of breakdown length. |
| **Chart → band divider** | **Keep** the single hairline between chart and band; remove all other in-hero dividers (chrome discipline, §4). | The one divider is load-bearing (separates trend from its explanation); others are noise. |

### The three net-new primitives (gate v1 — in scope)

| Primitive | Used by | Status | Notes |
|---|---|---|---|
| **Δ-decomposition** (flujos / devaluación / ε) | Box 1 band + Por moneda; Box 2 AI insights | Net-new; **has a build path** via [[daily-position-pack-prd]] | Pure math over shipped balances + transactions + BCV history. Needs **daily balance snapshots** (history) to compute Δ over a window. |
| **Cash-flow-by-category (direct method)** | Box 6 | Net-new | créditos − débitos grouped by category, net headline. Needs category rollups over a window. |
| **Recurrence detection** | Box 5 (new types) + a "próximos débitos" signal | Net-new | Flagged missing in [[reports-catalog]]. Pattern-detect repeating debits by counterparty/amount/cadence. |

> **Shared dependency worth surfacing to Dan early:** Boxes 1, 2, 3, 8 all want **historical daily balance closes** (not just current balance) to show trend / Δ-ayer / 30-d series. If balances are only stored as "current," a **daily snapshot job** is the unlock for half the page. This is likely the single longest-lead backend item. → confirm at `/tesote-plan`.

---

## Box specs

Each box: **Purpose · Window · Data contract · Layout · States · Interactions · Edge cases · Reconciliation · Open**. Box 1 is fully specced as the reference depth; Boxes 2–8 are scaffolded and filled in subsequent passes.

---

### BOX 1 — Posición (hero) ✅ fully specced

**Purpose.** The single "where do we stand" number, its 30-day trajectory, and an honest decomposition of *why* it changed — split flows from devaluación. Plus the currency and bank/entity breakdown beneath.

**Window.** Chart + delta chip + decomposition band = **trailing 30 days**. Por moneda "Δ ayer" = **1 day** (today vs. yesterday's close). Desglose = **current snapshot**.

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| Consolidated position (USD) | Σ account balances, VES→USD at current BCV | `tesote_accounts_list` / balances + FX rate | ✅ shipped |
| 30-d position chart | daily close of consolidated USD position, 30 points | **daily balance snapshot** (history) | ⚠️ **net-new** (snapshot job) |
| Beginning-balance marker | close at t−30 | same snapshot series | ⚠️ net-new |
| Delta chip (+$X · 30 d) | today − close(t−30) | derived from series | ⚠️ net-new |
| Decomposition band — Entró / Salió | Σ credits / Σ debits over 30 d (USD-equiv) | `tesote_transactions_search` | ✅ shipped |
| Decomposition band — Variación neta | Entró − Salió | derived | ✅ |
| Decomposition band — Devaluación | FX effect on VES holdings over 30 d | **Δ-decomposition engine** | ⚠️ net-new |
| ε residual (if shown) | today − (begin + neta − devaluación) | derived; data-quality signal | ⚠️ net-new |
| Por moneda — USD cell | USD balances, account count, Δ ayer | balances + snapshot | partial (Δ ayer net-new) |
| Por moneda — VES cell | Bs balance (primary), ≈$ at BCV, Δ ayer, devaluación | balances + FX + decomposition | partial |
| Desglose por banco / entidad | balances grouped by bank / entity, % of total | `tesote_accounts_list` | ✅ shipped |

> Field-level schema is `/tesote-plan`'s job; cross-ref [[reference_finance_db_schema]]. BCV rate basis + history: confirm there's a stored rate timeseries (devaluación needs the rate *at each point*, not just today's).

**Layout (v5).** Per §4 card + §7 chart/band + §5 multi-currency. Big figure in display weight (28px+, cents smaller per §6); delta chip = green `var-chip`. Chart = gradient area, begin dot + value label (no "hace 30 d" caption), dotted end point. Band = 4 cells; **"Variación neta" is blue but same size as the others** (no size emphasis — v5). Por moneda = 2 cells, **no currency badge squares** (v5); each = name + %-share, amount, Δ-ayer. **VES shows Bs first, with the dollarized `≈ $` enlarged (14px) beneath** (v5); USD cell has **no sub-line** (v5). Devaluación shows on the VES cell only. Desglose = two bar-lists (banco / entidad), share-of-total mini-bars.

**States**
- **Loading:** skeleton — figure shimmer, chart placeholder, band/cells greyed. Don't show $0.
- **Empty (no banks connected):** replace whole box with an empty state — icon + "Conecta tu primer banco" + CTA to Conexiones. (This is the new-workspace state; AI panel beside it shows an onboarding nudge instead of a report.)
- **Short history (<30 d connected):** chart shows the **available range**, labeled honestly ("desde que conectaste · 12 d") — **never fabricate** 30 d. Begin marker = earliest real close. Delta chip uses available range.
- **Single-currency workspace:** if USD-only (e.g. a US-only entity), **hide the VES cell and the Devaluación term** entirely (devaluación = 0/N/A); band collapses to Entró/Salió/Neta. If VES-only, USD consolidated still shown (it's the protagonist) but Por moneda has one cell.
- **Stale sync:** if any account's last sync is old, the header "● En vivo" becomes "Actualizado hace Xh" (amber per pill-pending semantics) and the most-stale account is named in the AI panel (Box 2). The figure still renders — with the freshness caveat visible, not hidden.
- **FX rate stale/missing:** if no current BCV, show last-known rate with its date as meta and flag it; devaluación for the period falls back to ε (can't attribute) rather than a wrong number.

**Interactions**
- Figure / "Ver Saldos" link → Saldos page (full position).
- Chart hover → tooltip: date + consolidated close that day (Geist Mono).
- Band "Entró"/"Salió" → Movimientos filtered to credits/debits for the 30-d window.
- Desglose bank row → Saldos filtered to that bank; entity row → Saldos filtered to that entity. (Always-visible rows, hover-highlight per §11.)

**Edge cases**
- **10-digit Bs** in the VES cell → auto-step font down + ellipsis per §5.
- **Negative consolidated position** (net overdraft) → render minus, delta chip flips red/down.
- **Multiple BCV moves in the window** → devaluación integrates over the actual rate path, not a single endpoint diff (engine concern; flag for `/tesote-plan`).
- **Inter-account transfers** (e.g. USD→VES internal) → **excluded from the flow band** so they don't inflate both Entró and Salió. Connect already tags inter-account transfers today (resolved #3), so this is a filter, not new classification work.

**Reconciliation (must hold, testable)**
```
begin(t−30) + Variación neta − Devaluación  =  today        [± ε]
today − begin(t−30)                         =  delta chip
Σ Por moneda (USD-equiv)                     =  today
Σ Desglose por banco                         =  today
Σ Desglose por entidad                       =  today
```
Worked mock (from prototype + README convention): `490.550 + 33.190 − 1.900 = 521.840`; chip `+31.290 · 30 d`. If ε ≠ ~0, surface it as a data-quality signal (per daily-position-pack), don't hide it.

**Resolved (was box-level open)**
- **#1** ε shown **only when material** ("Sin explicar"); data-quality signal, not money.
- **#2** "Δ ayer" close stamped at **VE-timezone EOD** (America/Caracas).
- **#3** Internal transfers **excluded** from flows — Connect already tags them.

---

### BOX 2 — Tesote AI panel ✅ fully specced

**Purpose.** Read the same banking data and *narrate* it — turn the position + flows + sync state into a human week-to-date briefing, then let the user ask follow-ups. This is the embedded home instance of the Tesote AI product; it earns the daily open by saying "here's what you need to know" before the user reads a single number.

**Window.** Voice line + week-to-date report = **week-to-date** (Mon → today). Ask-box answers can span any window the question implies.

**Data contract** — the report is built from *derived facts*, not raw rows. v1 insight catalog (each is a template with computed slots):

| Insight type | Trigger / input | Source | Shipped? |
|---|---|---|---|
| Voice line (greeting + headline) | user first name + this-week net flow direction + position-vs-recent-high | profile + week flows + 30-d series | partial (series net-new) |
| Net-flow summary | Σ entró / Σ salió WTD + count of movements | `tesote_transactions_search` | ✅ shipped |
| Biggest cobro | max credit WTD + counterparty + auto-reconciled flag | transactions | ✅ shipped |
| Devaluación hit | BCV move WTD × VES exposure | **Δ-decomposition engine** | ⚠️ net-new |
| Stale-sync warning | account(s) with oldest `last_synced_at` > threshold | `tesote_bank_status` | ✅ shipped |
| (catalog grows) recurring debit due | next predicted recurring debit | **recurrence engine** | ⚠️ net-new |

**Generation model.** The voice line + report = a **pre-computed insight set rendered server-side** (deterministic, fast, no LLM call blocking page load). A background job assembles candidate insights → ranks → keeps top ~4. The **ask-box is live** (real LLM call on submit). → resolves Open #8 (lean pre-generated, confirmed here).

**Read/write boundary.** **Read-only in v1.** No money movement, no categorization, no writes from the panel — prompts surface *information*, they don't take actions. Write actions (categorize, move money) are v1.2 with explicit confirmation (see Path forward). This keeps the launch surface safe.

**Layout (v5).** Per §16. Header = AI mark + "Tesote AI" (no Copiloto badge). **Voice line in Instrument Serif** (~24px, italic emphasis on the key word). "Tu semana hasta hoy" report = 3–4 feed items, each an inline-SVG icon color-coded by type (up=green, fx=orange, new=blue, warn=yellow) + one sentence with the key number bolded. 3 prompt buttons under "Pregúntale…". Input pinned to the panel floor via flex spacer (stretches to hero height).

**Prompt-button selection.** **Data-aware, not static.** The 3 prompts are chosen from a catalog to match what's interesting in the user's data this week (e.g. if devaluación was material → surface "¿cuánto debería pasar de Bs a USD?"; if position dropped → "¿por qué bajó mi posición ayer?"). Fallback to 3 sensible defaults when nothing stands out. → resolves Open (prompt selection).

**States**
- **Generating / loading:** skeleton lines in the report area; voice line placeholder. Don't show a half-built report.
- **Empty (new workspace, no data / Box 1 empty state):** replace report with an **onboarding nudge** — "Conecta un banco y te resumo tu semana" + CTA. No fabricated insights.
- **Thin week (very few movements):** degrade gracefully — fewer feed items, honest ("Semana tranquila: 3 movimientos"). Never pad with filler.
- **Insight compute partial (decomposition/recurrence not ready):** render the shipped-data insights (flows, biggest cobro, stale sync); silently omit the net-new ones until their engines land. Panel still useful day one.
- **Ask-box error / timeout:** inline error in the input area, retry; never blanks the report above.

**Interactions**
- Prompt button → opens the AI conversation pre-filled with that question (full AI surface or in-panel thread — see Open #9).
- Input submit → live answer.
- Feed items are **read-only text** in v1 (no deep-links yet); v1.1 may link a finding to its source (e.g. "biggest cobro" → that movement).

**Edge cases**
- **Name missing** → greet by workspace ("Buena semana en Tesote Ventas…") rather than a blank name.
- **Multi-currency net flow** → narrate in USD-equiv (consolidated), consistent with Box 1.
- **Tone/locale** → VE Spanish `tú`; finance-function framing ("finanzas", not "tesorería") per [[project_tesote_ai_audience]].

**Reconciliation.** The numbers the AI cites **must match the boxes** — "entró $26.800 / salió $18.450 / +$8.350 neto" has to equal Box 3's weekly figures; any position/devaluación number must equal Box 1. The AI reads the *same computed facts* the boxes render, not an independent query. (This is why insights are derived server-side facts, not free-form generation.)

**Resolved / deferred (box-level)**
- **#9** Prompt click + ask-box **routes to the full Tesote AI surface**; panel stays a briefing.
- **#10** Insight ranking — **deferred, polish later**; v1 ships a simple priority/materiality order.
- **#11** Refresh cadence of the pre-computed set — daily job (ties to the snapshot job); confirm at `/tesote-plan`.

---

### BOX 3 — Entró / salió (semana) ✅ fully specced

**Purpose.** This week's money movement at a glance: total in, total out, net, and a 7-day in/out bar pair. The "did we make or lose ground this week" KPI.

**Window.** **Current week**, dates shown in the card range (e.g. "Esta semana · 02–08 jun 2026").

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| Entró (week) | Σ credits this week, USD-equiv | `tesote_transactions_search` | ✅ |
| Salió (week) | Σ debits this week, USD-equiv | transactions | ✅ |
| Neto + count | Entró − Salió; movement count | derived | ✅ |
| Daily bars (7) | per-day in/out totals | transactions grouped by day | ✅ |

**Layout (v5).** KPI card (§4). Two figures (Entró green / Salió ink, Geist Mono), "Neto +$X · N movimientos" line, 7 day-columns of paired in/out bars.

**States**
- **Loading:** skeleton figures + bar placeholders.
- **Empty (no movements this week):** "Sin movimientos esta semana" + zeroed figures (not a broken chart).
- **All-in or all-out week:** one bar series can be empty — render the present side, flat baseline for the other.
- **Stale sync:** if the week's data may be incomplete, show the freshness caveat (shared header signal from Box 1).

**Interactions**
- Card → Movimientos filtered to this week.
- (v1.1) bar/day → Movimientos filtered to that day.

**Edge cases**
- **Internal transfers excluded** (Connect-tagged, resolved #3) so they don't inflate Entró/Salió. **Consistency rule: Box 3 weekly flows and Box 1 band use the same flow definition** (same exclusion).
- **Multi-currency** → USD-equiv for the headline (consistent ranking); per the §5 rule the underlying can be mixed but the KPI consolidates.

**Reconciliation.** Box 3 Entró/Salió/Neto for the week = the weekly numbers the AI panel (Box 2) narrates. Box 3 is a *weekly* subset — must **not** equal Box 1's 30-d band (the bug guarded in §8).

**Resolved** — week = **Mon–Sun calendar week** (#6).

---

### BOX 4 — Categorización (%) ✅ fully specced

**Purpose.** Data-hygiene KPI: what share of movements are categorized, how many aren't, and a one-click path to fix the gap. Drives the categorization behavior the rest of the product (cash-flow report, AI) depends on.

**Window.** **Last 30 days** (card range "Últimos 30 días · N movimientos").

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| % categorized | categorized count / total count over 30 d | `tesote_transactions_search` + `tesote_categories_list` | ✅ |
| Uncategorized count | total − categorized | derived | ✅ |
| "Revisar" target | filter handle for `sin categoría` | Movimientos filter | ✅ |

**Layout (v5).** KPI card: big % (display, ~34px), "de N movimientos categorizados" sub, progress bar, foot line "N sin categorizar · Revisar".

**States**
- **Loading:** % shimmer + bar placeholder.
- **100% categorized:** green full bar, "Todo categorizado" (drop the warning foot).
- **Empty (no movements in window):** "Sin movimientos que categorizar" — not "0%".
- **Low %:** bar still green per design (no alarm color unless we decide a threshold → Open).

**Interactions**
- "Revisar" → **Movimientos filtered to `sin categoría`** (deep-link with the filter pre-applied — uses the Movimientos filter-builder primitive, §12).
- Card → Movimientos (all, 30 d).

**Edge cases**
- **Count basis = by transaction count**, not by amount (a single huge uncategorized tx shouldn't read as "90% uncategorized by value"). → resolves Open #5 *for this box* (count-based). Note inconsistency is fine here because it's a hygiene metric, not a money metric.
- Partial categories (split transactions, if they exist) → count as categorized only if fully categorized.

**Open** — threshold for a caution color on the bar/foot (e.g. <80% turns the count amber)? (Lean: yes, amber under a threshold — small, helps.)

---

### BOX 5 — Nuevo en tus cuentas ✅ fully specced

**Purpose.** Surface what's *new* in the account activity — first-seen counterparties and first-seen transaction types — so the user notices new payees/charges without scanning the ledger. A light anomaly/novelty signal.

**Window.** New **within the last 30 days** (first-seen relative to all prior history). Card shows a short list (3 in v5) + "Ver todo".

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| New counterparty | counterparty first appears in window, never before | transactions history (first-seen) | ✅ (derivable) |
| New transaction type | a transaction type/pattern first seen in window | transactions + **recurrence/novelty detection** | ⚠️ partly net-new |
| Per-item meta | account ··last4 + "primera vez" / "tipo nuevo" | transactions | ✅ |

**Layout (v5).** List rows: name + meta (account ··last4 · "primera vez") + a pill (`Contraparte` = pill-new, `Tipo` = pill-pending). "Ver todo" link.

**States**
- **Loading:** 3 skeleton rows.
- **Empty (nothing new):** "Nada nuevo esta semana" — a *good* empty state, not an error.
- **Many new (new/messy workspace):** cap the list at 3, "Ver todo (N)" carries the full count.

**Interactions**
- Row → Movimientos filtered to that counterparty (or that type).
- "Ver todo" → a filtered Movimientos / counterparties view of all new items in window.

**Edge cases**
- **"New" definition = first-ever appearance** (no prior history anywhere), surfaced if that first appearance falls in the window — *not* "first in window." → resolves Open #4 (first-ever). Avoids re-flagging a known counterparty just because they were quiet for a month.
- **Brand-new workspace** → everything is technically "new"; suppress the box (or show onboarding copy) until there's a baseline of history. Don't drown the user.
- Counterparty identity = however Connect resolves it today (alias/normalization is Connect's job, cross-ref [[reference_ve_bank_naming]]); this box trusts that resolution.

**Open** — overlap with the recurrence engine: "new transaction *type*" detection vs. recurrence-detected patterns — are these the same signal surfaced two ways? Align with Box 6/recurrence work.

---

### BOX 6 — Flujo de caja por categoría (mes, método directo) ✅ fully specced *(net-new primitive)*

**Purpose.** A direct-method cash-flow statement built from bank reality: group the month's movements by category, sum credits and debits per category, headline the net. The "where did the money actually come from and go" view that the manual spreadsheet can't produce automatically.

**Window.** **Current month** (card range "Este mes · método directo (créditos − débitos)").

**Data contract** — **net-new primitive.**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| Net flow (month) | Σ credits − Σ debits, all categories, USD-equiv | category rollup over month | ⚠️ net-new |
| Entradas total + per-category | credits grouped by category | transactions + categories | ⚠️ net-new (rollup) |
| Salidas total + per-category | debits grouped by category | transactions + categories | ⚠️ net-new |
| Per-row bar | category amount / group max | derived | ✅ |

**Layout (v5).** Net headline (display ~28px, green if positive) + Entradas/Salidas summary line; then two groups (Entradas, Salidas), each a header with group total + rows (category name · proportional bar · amount). In = green track, Out = clay track.

**States**
- **Loading:** headline shimmer + group skeletons.
- **Empty (no movements this month):** "Sin flujo este mes" + zero headline.
- **Uncategorized bucket:** uncategorized movements roll into an **"Sin categorizar" row** in each group (not dropped — the statement must reconcile to total flow). → resolves Open (uncategorized handling: own bucket).
- **One-sided month** (all in or all out): render the present group, show the other as empty with a zero total.

**Interactions**
- Category row → Movimientos filtered to that category + month.
- "Ver Movimientos" → Movimientos for the month.

**Edge cases**
- **USD-equiv vs. per-currency:** headline + bars in **USD-equiv** (so categories are comparable across currencies). Mixed-currency categories consolidate. → Open #5 (this box = USD-equiv).
- **Month = calendar month** (resolved #7).
- **Group ordering** = by magnitude descending within each group.
- Transfers **excluded** (Connect-tagged, resolved #3) so internal moves don't appear as category flow.

**Reconciliation.** Σ Entradas − Σ Salidas = net headline. The category sums must tie to the month's total credits/debits (incl. the Sin-categorizar bucket). Should reconcile with Movimientos filtered to the month.

**Resolved** — month = **calendar month** (#7). Open eng note (for `/tesote-plan`): can this box and Box 1's flows share one rollup service (same direct-method math over different windows)?

---

### BOX 7 — Top movimientos (30 d) ✅ fully specced

**Purpose.** The biggest individual movements of the period — the few transactions that moved the needle, ranked. Quick "what were the largest things that happened" scan.

**Window.** **Last 30 days.** Top N (6 in v5).

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| Ranked top-N | transactions sorted by |amount| in USD-equiv | `tesote_transactions_search` | ✅ |
| Per-row | rank, counterparty, bank ··last4 · date · category, amount | transactions | ✅ |
| Bs rows | Bs amount + `≈ $` USD-equiv beneath | transactions + FX | ✅ |

**Layout (v5).** Ranked list: rank number (mono, muted) + counterparty + meta (bank ··last4 · date · category) + amount (credit green, debit ink). **Bs rows show Bs first with `≈ $` USD-equiv beneath** (§5). "Ver Movimientos" link.

**States**
- **Loading:** 6 skeleton rows.
- **Empty:** "Sin movimientos en 30 días."
- **Fewer than N:** show what exists, no padding.

**Interactions**
- Row → that movement's detail (or Movimientos focused on it).
- "Ver Movimientos" → Movimientos, 30 d, sorted by amount.

**Edge cases**
- **Cross-currency ranking basis = USD-equiv** (a Bs 5.000.000 cobro and a $8.420 cobro rank correctly against each other) — but **display stays native, Bs-first** per §5. → resolves Open #5 (rank USD-equiv, display native).
- **Credits + debits mixed** in one ranked list (by absolute size), not split. Signed/colored per direction.
- Ties broken by date (most recent first).

**Reconciliation.** Each row's USD-equiv uses the same BCV basis as Box 1 (consistent conversion).

**Open** — none material; N (6) and mixed-vs-split are settled above.

---

### BOX 8 — Saldos por cuenta (list) ✅ fully specced

**Purpose.** Every connected account as a ranked list — the breakdown beneath the consolidated position. Each row: which bank/account, which entity, its balance, and its share of the total.

**Window.** **Current snapshot** (live balances).

**Data contract**

| Element | Inputs | Source | Shipped? |
|---|---|---|---|
| Per-account balance | current balance, native currency | `tesote_accounts_list` | ✅ |
| Entity name | owning legal entity (≤15-char display) | account → entity | ✅ |
| Share-of-total | account USD-equiv / consolidated total | balances + FX | ✅ |
| Per-row freshness | account `last_synced_at` | `tesote_bank_status` | ✅ |

**Layout (v5).** Full-width card, list rows: bank logo + account name + **meta (`··last4 · <entity ≤15ch, grey> · CCY`)** + share-of-total bar + value + %. Entity name truncated to 15 chars with full name on hover (v5 change). Even 16px gap above the box (v5 fix).

**States**
- **Loading:** skeleton rows.
- **Empty (no accounts):** shares Box 1's empty state — "Conecta tu primer banco."
- **Stale account:** per-row freshness indicator (subtle dot/label) when an account's sync is old; the row still shows last-known balance, flagged — never hidden (§11 always-visible).
- **Manual account:** rendered like the others, marked "manual" (no sync freshness).

**Interactions**
- Row → Saldos filtered to that account (drill to the full account view).
- "Ver Saldos" → Saldos (all).

**Edge cases**
- **Ranking + share basis = USD-equiv** (so USD and Bs accounts sort into one meaningful order), but each row's **value displays native** (Bs rows Bs-first per §5). → Open #5 (USD-equiv for ranking/% , native for display).
- **15-char entity truncation:** hard cap with ellipsis + full name in `title`/tooltip (v5: "Tesote Technolo…", "TST Servicios y…"). Real impl truncates by character, not CSS width, to honor the 15-char rule.
- **10-digit Bs balance** → §5 overflow handling.
- **Single entity** → entity name still shown (consistent), or could be omitted if redundant — minor, lean keep for consistency.

**Reconciliation.** Σ account balances (USD-equiv) = Box 1 consolidated total = Σ Desglose por banco = Σ Desglose por entidad. This list is the leaf level of the same tree.

**Open** — sort default: **by USD-equiv balance descending** (biggest first). Confirm vs. grouping-by-entity as an alternate view (lean flat-sorted for v1).

### BOX 3 — Entró / salió (semana)  *(scaffold)*
- **Purpose.** This week's money in vs. out + net, with daily bars.
- **Window.** **Current week**, dates shown (e.g. 02–08 jun 2026).
- **Primary data.** Σ credits / Σ debits this week (USD-equiv), per-day in/out for the bar pair. ✅ shipped (transactions).
- **Key open.** Week definition (Mon–Sun? vs. last 7 d); USD-equiv vs. per-currency; does it net internal transfers (ties to Box 1 #3).

### BOX 4 — Categorización (%)  *(scaffold)*
- **Purpose.** Share of transactions categorized over 30 d + count uncategorized + "Revisar".
- **Window.** 30 d.
- **Primary data.** categorized count / total count over window; uncategorized list link. ✅ shipped (categories).
- **Key open.** Count basis (by tx count vs. by amount?); does "Revisar" deep-link to Movimientos filtered `sin categoría`.

### BOX 5 — Nuevo en tus cuentas  *(scaffold)*
- **Purpose.** First-seen counterparties + new transaction types this period.
- **Window.** TBD (30 d? since-last-visit?).
- **Primary data.** counterparty first-seen detection; new-type detection. **Recurrence/novelty detection = net-new.**
- **Key open.** "New" definition (first-ever vs. first-in-window); recurrence engine overlap; pill taxonomy (Contraparte / Tipo).

### BOX 6 — Flujo de caja por categoría (mes, método directo)  *(scaffold — net-new primitive)*
- **Purpose.** Direct-method cash flow: créditos − débitos grouped by category, net-flow headline, Entradas/Salidas groups with bars.
- **Window.** **Current month.**
- **Primary data.** category-grouped credit/debit sums over month. **Net-new primitive.**
- **Key open.** Uncategorized handling (own bucket vs. excluded); USD-equiv vs. per-currency; group ordering (by magnitude); month = calendar vs. trailing 30.

### BOX 7 — Top movimientos (30 d)  *(scaffold)*
- **Purpose.** Largest movements by absolute size, ranked.
- **Window.** 30 d.
- **Primary data.** top-N transactions by |amount|. ✅ shipped.
- **Key open.** Cross-currency ranking basis (**rank by USD-equiv**, display Bs-first with ≈$ per §5); credits + debits mixed or split; N (6 in proto).

### BOX 8 — Saldos por cuenta (list)  *(scaffold)*
- **Purpose.** Every account as a ranked list: logo + name + meta · share-of-total bar · value + %.
- **Window.** Current snapshot.
- **Primary data.** per-account balances, share of consolidated total (USD-equiv). ✅ shipped.
- **Key open.** Sort (by USD-equiv desc?); per-row stale-sync indicator; VES rows Bs-first or USD-equiv for ranking consistency; drill to Saldos filtered to account.

---

## Surfaces affected

- **Connect** sidebar section gets the rebuilt **Inicio** as the workspace home (top of nav, above Connect group per dashboard-v4).
- **Tesote AI** surface — the panel is an embedded instance of the AI product on the home; shares the AI backend.
- New components (map to the design system): position-hero, decomposition-band, currency-cell, desglose-bar-list, ai-panel, kpi-flow, kpi-progress, new-items-list, cashflow-category-report, top-movements-list, account-list. Several are landing-page-derived (hero-panel, IA subcard, stat-grid) — keep product ↔ marketing one family.

## Data model implications

- **Daily balance snapshots** (new): per account, EOD close + FX rate at close → powers chart/Δ-ayer/30-d series across Boxes 1,2,3,8. *Longest-lead item.*
- **Decomposition derivations** (new, possibly materialized): flujos/devaluación/ε per window, per workspace.
- **Recurrence signals** (new): detected recurring debits (counterparty + cadence + expected amount/date).
- **BCV rate timeseries** (confirm exists): devaluación needs rate-at-time, not just current.
- All new tables: `workspace_id` scoped, soft-delete, idempotent writes. Cross-ref [[reference_finance_db_schema]], [[project_tesote_vs_odoo_split]] (all of this is **bank-reality / SoR = Tesote**, not Odoo).

## AI / automation implications

- **Box 2 (AI panel):** read-first, no write actions v1. Insight report = pre-computed insight set (deterministic, fast), ask-box = live. Reuses decomposition + recurrence as structured inputs so the model narrates facts, not raw rows.
- **Background jobs:** daily snapshot, decomposition compute, recurrence scan — all idempotent, all flagged.

---

## Open decisions

> **All decisions resolved 2026-06-09 (Luis), except #10 (deferred).** Recorded below as the master; the spec text above reflects these.

| # | Decision | Resolution (Luis, 2026-06-09) |
|---|----------|------------|
| 1 | ε residual display (Box 1) | **Show "Sin explicar" only when material.** ε = `today − (begin + neta − devaluación)` — a data-quality signal (feed lag / missing tx / FX path approximation / rounding), not money. Small ε = noise; large ε = flag a sync check. |
| 2 | Daily-snapshot EOD timezone | **VE timezone** (America/Caracas). EOD close stamped in VE time across all accounts. |
| 3 | Internal-transfer exclusion from flows (Boxes 1, 3, 6) | **Resolved — Connect already tags inter-account transfers today.** Flows (band, weekly KPI, cash-flow) **exclude tagged transfers**; no new classification work needed. *De-risks every flow number.* |
| 6 | Week definition (Box 3) | **Mon–Sun calendar week.** |
| 7 | Cash-flow month (Box 6) | **Calendar month.** |
| 9 | AI prompt-click + ask-box (Box 2) | **Routes to the full Tesote AI surface** (panel stays a briefing; real answers happen in the full surface). |
| 10 | AI insight ranking rule (Box 2) | **Deferred — polish later.** v1 ships a simple priority/materiality order; tune post-launch. |
| 4 | "Nuevo" definition (Box 5) | First-ever appearance, surfaced if it falls in window; suppress box for brand-new workspaces. |
| 5 | USD-equiv vs. per-currency (Boxes 3/6/7/8) | Rank/share/headline in USD-equiv; display native, Bs-first (§5). Box 4 = by tx count. |
| 8 | AI report generation (Box 2) | Pre-computed server-side insight set; ask-box live. |
| — | AI read/write boundary (Box 2) | Read-only in v1; write actions defer to v1.2. |
| — | Uncategorized in cash-flow (Box 6) | "Sin categorizar" bucket in each group (never dropped). |
| — | Box 8 sort default | By USD-equiv balance descending. |

**Net effect on the build:** with #3 resolved (transfers already tagged), the **daily balance snapshot job is now the single longest-lead backend item** — it gates the trend/Δ-ayer/series across Boxes 1/2/3/8. Sequence it first with Dan at `/tesote-plan`.

---

## Path forward

### V1 wedge

See Intake — V0 is the full dashboard incl. the three primitives. The **wedge inside it** is the **Posición hero + decomposition band**: it's the screenful that proves the differentiated insight (flows vs. devaluación) and reuses the daily-position-pack math. If anything must ship first to dogfood, it's Box 1 + Box 2 on the real Tesote workspace.

### What sequences after v1

```
v1   — full Inicio (8 boxes + 3 primitives) behind flag, Mariel dogfood → beta → GA
v1.1 — "Personalizar" (layout/widget customization); forward cash-flow projection box
v1.2 — AI write actions from the panel (move money / categorize) with confirmation
v2   — multi-workspace roll-up; DR/US-entity-aware once VE proves out
```

### Discipline calls

- **No ERP data, ever, on Inicio** — the moment an invoice or AR-aging number appears, scope has slipped. Hard line.
- **One opinionated layout** in v1 — "Personalizar" waits. Customization is a tar pit before the default is proven.
- **Snapshot job is the critical path** — if it slips, Boxes 1/2/3/8 degrade to "current-only" (no trend). Sequence it first with Dan.

---

## References

### Internal source docs
- [[prototypes/README]] — series lineage, content inventory, mock-data convention
- [[daily-position-pack-prd]] — decomposition identity + worked example + ε residual
- [[reports-catalog]] — the banking-report menu; recurrence flagged missing
- [[../design/web-app-design-system]] — global page rules (cited by §)
- [[../design/archetypes]], [[../design/design]] — density + tokens

### External
- Linear ticket: [pending]
- Treasury plan dir: [pending `/tesote-plan`]
- Prototype: `prototypes/dashboard-v5.html` (frozen, signed off 2026-06-09)

### Memory references
- [[project_dashboard_redesign]], [[project_daily_position_pack]], [[feedback_tesote_ai_naming]], [[project_tesote_ai_audience]], [[project_filter_system_primitive]], [[feedback_product_ui_spanish_venezuelan]], [[project_tesote_vs_odoo_split]]

---

## Appendix

**Mock-data convention** (keep consistent across prototype + PRD examples): consolidated **$521.840,17**; USD **$457.109** (Mercury Checking $312.400 + Treasury $144.709); Bs **36.161.741,48 ≈ $64.731** at BCV **558,6436**; entities Tesote Technologies Inc. (US/USD) + TST Servicios y Consultoría (VE/VES); banks Mercury (US), BNC/Mercantil/Banesco/Bancamiga (VE); BNC worked row +$8.950 flow / −$271 devaluación. All breakdowns reconcile to the total.

---

*Template: `product/_prd-template.md`. Workflow: [[../../_workflows/brain-to-treasury]]. All 8 boxes specced against frozen `dashboard-v5.html` (2026-06-09). Next: resolve the 7 open decisions, then file PRO-* + run `/tesote-plan`.*
