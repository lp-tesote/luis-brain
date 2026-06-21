---
title: Tesote AI — Day-One Launch PRD
tags: [product, ai, prd, launch, banking-data]
updated: 2026-06-05
status: draft
audience: anyone — written self-contained, no prior context assumed
author: Luis Pulgar (synthesis with Claude)
linear: [URL once filed]
notion: https://app.notion.com/p/3761ee04eee18109888cd5af95638e45
tesote_plan_dir: [path once /tesote-plan run]
---

# Tesote AI — Day-One Launch PRD

> **One-line purpose.** Define what Tesote AI does for **every user in every workspace** on launch day: the product promise on banking data, the first-session experience, and the conditions that must be true before we flip the switch.

---

## Background — what you need to know, in five paragraphs

**Tesote** is a finance platform for businesses operating in Venezuela (and expanding). It connects to a company's bank accounts — Venezuelan banks via scrapers, US banks via APIs — and gives the finance team one place to see balances, transactions, categories, counterparties, and reports. Most customer workspaces hold **two currencies at once**: bolívars (Bs) and US dollars. That dual-currency reality shapes everything in this document.

**Tesote AI** is a chat assistant built into the product. The user types questions and instructions in Spanish; the AI reads the workspace's banking data through internal tools and can also *act* — create categorization rules, fix counterparty records, run reports. This launch puts the AI in front of **every user of every workspace** for the first time. Until now only internal users and one design partner have touched it.

**Two standing assumptions this whole document is built on:**

1. **Queries work at any scale.** Today the AI's transaction-reading tool returns at most 100 rows with no signal that more exist — so any total or percentage computed over a real workspace is silently wrong. We are assuming engineering ships the fix before launch: pagination, an explicit "there is more data" signal, and — most importantly — **server-side aggregation**, meaning when a user asks "how much did I spend on X this year?", the *database* computes the sum and the AI reports it. The AI never does arithmetic over row dumps. **If this work slips, this launch plan is invalid** and we fall back to a narrower launch (saved reports + rules only, no free-form questions).

2. **Permissions are inherited, not designed here.** The AI sees exactly what the asking user's existing workspace permissions grant — no more, no less. Users in workspace A can never see data from workspace B. Conversations are private to their user. Every AI action is audited. Dan and Sebastián own this layer; this PRD takes it as given and focuses on the product.

**One piece of finance doctrine you need:** in Venezuela, converting bolívars to dollars honestly means converting **each transaction at the official BCV exchange rate of the day that transaction occurred** (BCV = Banco Central de Venezuela, publisher of the official rate). Applying *today's* rate to six months of history doesn't measure the business — it measures currency devaluation. Every dollarized figure the AI produces must follow this rule and say so.

---

## Tesote-Plan Intake

### Actor & Problem

As **any user of any Tesote workspace** — CFO, business owner, accountant, AP/AR analyst — I need to **ask Tesote AI any question about my banking data and have it set up and run my financial operation** because **today every analytical question means exporting to Excel, and every setup task (categorizing months of transactions, cleaning vendor records) is manual work measured in days**.

### The Test

This solves **"I have months of bank data and no fast way to interrogate it"** for **every finance user** in the AI surface. Without it: users keep exporting to Excel for every question, the AI launch lands as a demo toy instead of a daily tool, and the AI revenue line for 2026 stays theoretical.

### V0 — Simplest thing that works (day-one definition of done)

- [ ] **Free-form analytical questions answer correctly and completely** — totals, percentages, comparisons, arbitrary periods, top-N — computed in the database, never by the model summing rows
- [ ] **Every numeric answer states its own scope**: period covered, accounts included, currency, row count — e.g. *"sobre 1.432 movimientos, enero–mayo, 3 cuentas USD"*. If coverage is partial, the AI says so **before** the number, never only when challenged. When the user doesn't state a period, the default is **"este mes"** — the current calendar month, first of the month through today — and the scope line names it
- [ ] **Mass setup works end-to-end in chat**: the AI proposes categorization rules from the workspace's uncategorized volume → shows every transaction each rule would touch → user excludes/approves → the rules engine applies them to all history and everything arriving in the future
- [ ] Every workspace ships with **3–5 pre-built report definitions** (final list pending — Luis is testing candidates on real data now), so "córreme el flujo de caja" works in the very first session of a brand-new workspace. Today the report library is empty for every customer — the feature exists but nobody has ever seen it work
- [ ] The AI can **save any good ad-hoc question as a new report definition** ("guárdamelo como reporte mensual")
- [ ] **Currency discipline holds without being asked**: no amount ever appears without its currency; bolívars and dollars never mix in one column, total, or chart series; aggregations are per-currency by default; dollarization on demand follows the BCV-rate-of-each-transaction's-date rule, with the basis stated
- [ ] **Every action previews before executing**: any mutation (rules, categories, counterparty edits) renders the affected rows with per-row exclude, executes exactly what was approved, and lands in the audit trail
- [ ] **Dates mean what they say**: "mayo" returns May 1–31. (Today one reporting tool silently substitutes a trailing-30-day window unless called with a specific extra parameter — that bug must be dead.) And a tool asked for an option it doesn't support must return an error, never silently ignore the option and answer as if it complied
- [ ] **Numbers render in European format everywhere** — `1.234.567,89`, both currencies (`Bs. 5.445.475,00` / `$1.234,56`), in prose, tables, charts, and tooltips
- [ ] All copy in **Venezuelan Spanish** (`tú`, never `vos`)
- [ ] **Platform stability proven**: no chat query can degrade or take down the app (this happened — one report request made all of Tesote unreachable; root cause must be fixed and guard-railed). A pending approval never dies because a conversation hit its length limit (also happened, mid-confirmation). The AI never claims it finished when it produced nothing

### Out of Scope (explicit "Not Doing" on day one)

- **The Odoo ERP connector** — a separately-installed integration some customers use for invoices and accounting. Its known bug class (currency mix-ups between Bs and USD fields at posting time) is wave 2 and irrelevant to day-one users, none of whom have the connector
- **The AP email inbox** — built (each workspace has an email address that receives vendor bills for the AI to draft) but switched off and never exercised; enabling it is its own decision
- **Scheduled / autonomous agents** — day one is chat-only; "send me this report every Monday" is the natural next release
- **Forecasting** — nothing exists for projections; the AI must not improvise forward-looking numbers from historical data
- **Full bank reconciliation** ("concíliame todo") — the cross-system transaction link still depends on string-parsing; only supervised, user-scoped reconciliation grooming
- **Per-account visibility tiers, conversation sharing, retention policy** — the permissions workstream (assumption 2)

### Technical Requirements

- [ ] **Pre-condition: the query-scale work shipped and re-verified against production** before flag-flip (assumption 1) — pagination, the "more data" signal on the chat path, server-side aggregation
- [x] **Historical BCV rate lookup by date** plus per-transaction USD-equivalents computed server-side — so dollarized aggregates also come from the database. **Solved (confirmed 2026-06-05)** — include in the pre-launch re-verification
- [ ] Feature-flagged rollout (confirm flag name with Dan)
- [ ] Permissions inherited from the existing model (assumption 2)
- [ ] Multi-tenant safe; audit trail on every AI mutation; soft delete only
- [ ] Seeding mechanism for the default report definitions + a "save as report" action callable from chat

### Rollout Plan

1. **Internal** — the Tesote Finance workspace (33 accounts, both currencies, live scrapers — the hardest case we have): re-verify every tool against production on the final build, then run the full first-session script below with Luis and Mariel
2. **Beta** — 3–5 named customer workspaces, hand-held; watch what users actually ask first; log every wrong or scope-less answer
3. **GA** — flag flipped for all workspaces; in-product announcement; the demo script doubles as onboarding content

---

## The product, in one paragraph

**Tesote AI on day one is the finance chief you can ask anything — and the setup brain that builds your machine.** Ask any question about your banking data — totals, trends, comparisons, "¿en qué se me va la plata?" — and get a complete, database-computed answer that states its own scope. Teach it your operation in one conversation: it proposes the categorization rules, you review and approve, the engine applies them to all history. Run your reports and have them narrated; turn any good question into a saved report with one sentence. Everything previews before it executes; everything is audited. Identity: *el jefe de finanzas que responde cualquier pregunta — y arma tu máquina*.

---

## The three pillars

### Pillar 1 — Ask anything

Free-form analytical Q&A over all the data the user can access: totals, percentages, period comparisons, top counterparties, spend breakdowns, arbitrary date ranges.

- Numbers come from the **database** (server-side aggregation), never from the model adding up rows
- Every answer carries the **scope line** — what was counted, what was filtered or excluded, which currency
- Multi-currency questions split per currency by default; dollarized views on demand, each transaction at the BCV rate of its own date, basis named

**Wedge:** *"Pregúntale a tus bancos lo que quieras. Te responde con los números completos — y te dice exactamente de dónde salieron."*

### Pillar 2 — Setup en masa

The AI doesn't categorize ten thousand transactions one by one — it writes the **rules** and the engine does the mass work. This is a deliberate division of labor: ad-hoc judgment goes through chat; recurring, deterministic work goes through the rules engine, which runs server-side, applies retroactively to the full history, and keeps applying to everything that arrives later. Finance people trust this more than per-row AI edits, and they're right to: "the AI guessed 10,000 categories" is scary; "the AI wrote 20 rules you reviewed, the engine applied them" is auditable.

The two surfaces feed each other: when an analytical answer exposes a gap ("$40k sin categorizar"), the AI offers the rules that would close it.

**Wedge:** *"El primer día con Tesote no es un proyecto de implementación. Es una conversación."*

### Pillar 3 — Reports: seeded, runnable, growable

- Every workspace starts with 3–5 pre-built definitions — the library is never empty on first contact
- The AI runs them, narrates the output, compares periods — always on top of deterministic report numbers
- Any ad-hoc question can be promoted to a saved definition on request, so each workspace's library grows out of its own real usage instead of our guesses

**Wedge:** *"Tus reportes corren igual todos los meses — y cada buena pregunta se convierte en uno nuevo."*

---

## The first session (the make-or-break 10 minutes)

Adoption is decided in the first session. Choreograph it:

1. **Open** — greeting plus 4–6 suggested prompts ("chips"). Every chip is a question we have verified succeeds on production data — nothing aspirational. Candidates:
   - *"¿Cuánto gasté este mes y en qué?"* — free-form breakdown
   - *"Córreme el flujo de caja de mayo"* — seeded report
   - *"Proponme reglas para mis movimientos sin categorizar"* — mass setup
   - *"¿Quiénes son mis 10 contrapartes más grandes este año?"* — top-N, database-computed
2. **First answer lands with its scope line.** The number is right, the currency is clean, and the *"sobre N movimientos, periodo X, cuentas Y"* line teaches the user from message one that this AI shows its work. That line is the product's trust signature.
3. **First action builds trust.** On the rules path: preview table with per-row exclude → approve → *"el motor aplicó 14 reglas a 3.847 movimientos históricos"*. The user watches months of backlog resolve and can audit every step.
4. **First follow-up converts to permanence.** When the user re-asks or refines a question, the AI offers: *"¿te lo guardo como reporte mensual?"* The session should end with the user owning an artifact, not just answers.

**The anti-goal:** a right number with no scope. To a CFO checking the answer against their own spreadsheet, an unscoped correct number whose period doesn't match theirs is indistinguishable from a wrong one — and one "wrong" number is all it takes. The user never asks again and tells their team why. The scope line is not formatting; it *is* the launch.

---

## User stories

### Ask anything (Pillar 1)

**US-1 — The total.** As a business owner, I ask *"¿cuánto le pagué a [proveedor] este año?"* and get the complete figure, computed in the database, with the scope line.
*Acceptance:* matches a manual export to the cent; works on workspaces with 10,000+ movements; never silently partial.

**US-2 — The breakdown.** As a CFO, I ask *"¿en qué se me va la plata?"* and get spend by category for a stated period — with the uncategorized bucket shown loudly (it's commonly ~70% of volume in a new workspace) and an offer to fix it via rules.
*Acceptance:* grouped server-side; per-currency split; "sin categorizar" never hidden or netted away — it's the hook into setup, not an embarrassment.

**US-3 — The comparison.** As an accountant, I ask *"compárame mayo contra abril"* and get both calendar months exactly, deltas, and the biggest movers.
*Acceptance:* "mayo" = May 1–31, never a trailing window; any grouping or option a tool doesn't support produces a loud error, never a silently different answer.

**US-4 — The dollarized view.** As a user with bolívar accounts, I ask for any of the above *"en dólares"* and each transaction converts at the BCV rate of its own date, with the basis stated on the answer (*"al BCV de la fecha de cada transacción"*).
*Acceptance:* today's rate is never applied retroactively; dollarized aggregates are computed server-side from per-transaction USD-equivalents.

**US-5 — The deep dig.** As an analyst chasing an anomaly, I drill from a total → category → counterparty → individual movements, and every step keeps its scope visible.
*Acceptance:* no depth limit a real workspace can hit; the drill path is reproducible from the conversation.

### Setup en masa (Pillar 2)

**US-6 — Teach the machine.** As an owner with six months of uncategorized movements, I say *"proponme las reglas que cubren la mayoría del volumen"* and get 10–20 proposed rules, each with the transaction volume it covers; I review, exclude, approve; the engine applies them to all history.
*Acceptance:* preview shows match counts per rule with per-rule and per-row exclude; post-approval summary states what was applied; the audit trail records proposed-versus-executed.

**US-7 — Fix my master data.** As an AP analyst, I ask for duplicate counterparties and missing tax IDs (RIF); the AI proposes consolidations, I approve, it executes — same preview → approve → audit pattern. Nothing merges without explicit approval.

**US-8 — Question becomes rule.** When my analytical question exposes a categorization gap, the AI offers the rules that would close it.
*Acceptance:* the offer is contextual, not nagging; declining takes one word.

### Reports (Pillar 3)

**US-9 — Run my cash flow.** As any user of a brand-new workspace, *"córreme el flujo de caja de mayo"* works in my first session: seeded definition, narrated against April, multi-currency handled by per-currency split, output as table plus chart (or my stated preference).

**US-10 — Save my question.** After any good ad-hoc answer, *"guárdamelo como reporte mensual"* creates a saved definition that reproduces the query.
*Acceptance:* the saved report re-runs deterministically and matches the original answer over the same period.

### Trust & platform (every interaction)

**US-11 — Currencies never blur.** Every amount carries its currency; no column ever mixes Bs and USD; per-currency by default; European format everywhere.

**US-12 — Nothing executes blind.** Every mutation previews; approval executes exactly what was previewed; a pending approval survives conversation length limits; all of it is audited.

**US-13 — The AI can't hurt Tesote.** No chat query can degrade the platform for anyone — including users who never open the AI. Worst case is the AI apologizing, never downtime. And it finishes what it starts, or says explicitly that it couldn't and what state things are in.

---

## What the AI says no to on day one

These are genuine scope edges — each refusal is honest about why and offers what *does* work:

| User asks | Day-one posture |
|---|---|
| "Concíliame todo" (full reconciliation) | Supervised, user-scoped grooming only; full automation comes with the structured cross-system link |
| Forecasts / projections | *"Te muestro la historia; proyecciones vienen después"* — no improvised forward numbers |
| Anything ERP/Odoo, in a workspace without the connector | *"Disponible con la conexión Odoo"* — clean upsell, not confusion |
| Anything involving the email inbox / invoicing | Not surfaced; chips never advertise it |
| Questions touching accounts outside the user's permissions | Answers on permitted scope and states that scope — without revealing more about what's excluded than the product UI itself would |

---

## Surfaces affected

- **The AI chat surface** — suggested-prompt chips, the scope-line answer template, the save-as-report action, the universal preview pane, narration templates
- **Workspace settings / reports** — seeded and user-promoted report definitions; audit trail visibility
- **No new screens.** Day one is choreography, seeding, and guardrails on the existing surface, plus the query plumbing underneath

---

## Data model implications

Three schema-significant builds, each carried by its own engineering spec; this PRD sequences them:

1. **Per-transaction USD-equivalent at the historical BCV rate** — the dollarization primitive (also needed by the planned daily cash-position report). **Solved (confirmed 2026-06-05)**; verify in the pre-launch re-audit
2. **Report definitions creatable from chat** — the definition shape must capture an ad-hoc query faithfully enough to re-run deterministically
3. **The server-side aggregation action** — the heart of assumption 1

---

## AI / automation implications

The conversion loops are the compounding asset:

- **Question → saved report** — the library personalizes itself from real demand
- **Question → rule** — analysis exposes gaps, setup closes them, data quality compounds
- **Repeated report → scheduled delivery** — the natural next release once scheduled agents exist

Day one plants all three loops; the first two ship.

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | The seeded default report list (3–5) | Luis (testing candidates now) | Open — the last open item |
| 2 | **The gate**: query-scale work shipped + re-verified against production before flag-flip | Dan → Luis sign-off | Confirmed as the gate (Luis, 2026-06-05) |
| 3 | Historical-rate dollarization | — | **Resolved 2026-06-05 — solved.** The capability exists; include in the pre-launch re-verification like everything else |
| 4 | AP email inbox: in or out of this launch | Luis | **Resolved 2026-06-05 — out** |
| 5 | Default period when the user doesn't state one | Luis | **Resolved 2026-06-05 — "este mes"** (current calendar month, first of the month through today), always named in the scope line |
| 6 | Beta workspace shortlist | Luis | Handled by Luis directly — not tracked in this doc |
| 7 | Permission assumptions (user-inherited access, workspace isolation, private conversations, full audit) | Dan / Sebastián | **Resolved 2026-06-05 — confirmed as given** |

---

## Path forward

### V1 wedge

The wedge is the pair **scope line + database-computed answers** — what makes "ask anything" trustworthy instead of impressive-until-checked. Mass setup and report-running are already verified working; the new build is the query plumbing (assumption 1) and the answer discipline (this document).

### What sequences after v1

```
pre-launch — query-scale work lands (historical-rate dollarization already solved); full re-verification against production
day 1      — this PRD: ask anything, all users, all workspaces
v1.1       — scheduled report delivery; analytics on what users save as reports
wave 2     — ERP-connector workspaces (after the currency-handling fixes on that side)
later      — a dedicated automations surface absorbs recurring/scheduled jobs
```

### Discipline calls

- **If assumption 1 slips, do not launch this.** Fall back to the narrow launch (saved reports + rules only, free-form questions politely declined) — that plan exists and is ready
- The scope line is non-negotiable on every numeric answer — no "clean answer" exceptions
- Forecasting stays out until it has its own spec; the temptation to improvise projections from clean history will be strong
- Inbox / invoicing stay dark until they can be exercised in a sandbox workspace that isn't our real books

---

## Appendix — glossary

- **Workspace** — one company's environment in Tesote: its bank connections, transactions, users
- **BCV** — Banco Central de Venezuela; publishes the official Bs/USD exchange rate daily
- **Rules engine** — Tesote's server-side categorization system: a rule = conditions (text match, amount band, account) + a category; applies retroactively and to all future transactions
- **Saved report definition** — a stored report configuration (type, accounts, currency, period logic) that re-runs deterministically
- **Counterparty** — the other party of a transaction (vendor, client); carries the RIF (Venezuelan tax ID)
- **Scope line** — the one-line statement of coverage that accompanies every numeric answer: period, accounts, currency, row count
- **Dry-run / preview** — the AI's proposed action rendered for inspection before anything executes
