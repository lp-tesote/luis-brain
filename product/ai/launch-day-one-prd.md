---
title: Tesote AI — Day-One Launch PRD (all users, all workspaces)
tags: [product, ai, prd, launch, banking-data]
updated: 2026-06-05
status: draft
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: [URL once filed]
tesote_plan_dir: [path once /tesote-plan run]
---

# Tesote AI — Day-One Launch PRD (all users, all workspaces)

> **One-line purpose.** Define exactly what Tesote AI does for **every user in every workspace** on day one of the rollout — the product promise on banking data, the first-session experience, and the readiness conditions — so launch is a checklist, not a vibe.

> **How this fits the launch-doc family.** [[launch-contract-2026-06-05]] = the 7 behaviors (correctness). [[launch-readiness-plain-2026-06-05]] = the bug verdicts (what's broken). **This doc = the product** (what day one *is*, who it's for, what the user experiences). The three reference each other; this one leads.

---

## Tesote-Plan Intake

### Actor & Problem

As **any user of any Tesote workspace** (CFO, owner, contador, AP/AR analyst — the whole finance function, per [[positioning-the-finance-chief]]), I need to **ask Tesote AI about my banking data and have it set up and run my financial machine** because **today that work is manual (Excel exports, hand-categorization, reports built by hand monthly) and the AI we ship must be useful in the first session or it never gets a second one**.

### The Test

This solves **"the AI is live for everyone but nobody knows what it's for, and the first thing they try fails"** for **all day-one users** in **IA / Workspace**. Without it: rollout happens, first sessions hit empty report libraries and refused/wrong answers, adoption dies in week one and the AI line of the 2026 pitch is dead on arrival.

### V0 — Simplest thing that works (day-one definition of done)

- [ ] Every workspace ships with **3–5 seeded report definitions** `[list pending Luis dogfood — feeds from qa-pre-created-reports findings]`; "córreme el flujo de caja" works in the first session of every workspace, never an empty library (kills W7)
- [ ] A new user opens the AI and sees **capability chips generated from the verified-✅ column** of [[capability-audit-2026-06-03]] — every suggested prompt is one we know succeeds
- [ ] **Setup en masa works end-to-end in chat**: propose rules from uncategorized volume → preview affected matches → user approves → engine applies retroactively (Pillar 1 of [[pitch-today-v2]], verified live)
- [ ] **Reports run + narrated**: AI runs saved definitions, narrates the output, compares periods — never aggregates raw rows itself (Pillar 2)
- [ ] **The AI never gives a confident wrong number**: free-form totals over transactions are refused with a redirect to the report/rule path until the eng gate ships (system-prompt guardrail matches the pitch)
- [ ] **Every mutation previews before executing** (rules, categories, counterparties): affected rows visible, per-row exclude, approve → execute → audit trail
- [ ] **Currency doctrine holds without being asked**: no bare amounts, no mixed Bs/USD columns, per-currency aggregation by default, European format everywhere (behaviors 2+6 of the contract)
- [ ] All copy in **Venezuelan Spanish** (`tú`), full-screen dialect consistency
- [ ] The six scoreboard blockers are closed or explicitly overridden by Luis: P1, P2, W1+W2, W3, W4, W7

### Out of Scope (explicit "Not Doing" on day one)

- **Odoo connector flows** — wave 2, manual install only; the entire Bs/USD Odoo bug class rides with it ([[bug-register]] Part 2)
- **Free-form analytical Q&A over transactions** ("¿cuánto gasté en X este año?") — gated until pagination/aggregation ships; day one = saved reports + the rules reframe
- **AP inbox** (`enabled: false`) — separate enablement decision (W11), not bundled into this launch
- **Automations surface / scheduled agents** — taxonomy says deterministic work goes there eventually; day one is chat-only
- **Per-account visibility tiers, conversation sharing, retention policies** — assumed handled by the security workstream (below), not designed here
- **Headline reconciliation** ("concílialo todo") — supervised, scoped grooming only until the BSL structured link ships

### Technical Requirements

- [ ] Feature-flagged rollout: `tesote_ai_workspace` (or existing flag — confirm with Dan)
- [ ] **Security/permissions: ASSUMED OWNED BY DAN/SEBASTIÁN.** Working assumption this PRD builds on: the AI inherits the asking user's exact permissions, hard workspace isolation on every tool call, conversations private to their user, all actions audited. If any of these assumptions is false, this PRD needs a revision pass — flag it.
- [ ] Spanish copy (VE, `tú`)
- [ ] Multi-tenant safe (`workspace_id` on all new tables; no cross-workspace leakage)
- [ ] Audit trail on every AI mutation (soft delete only)
- [ ] Seeding mechanism for report definitions (eng builds the seeder; product picks the list)

### Rollout Plan

1. **Internal** — Tesote Finance workspace (Luis + Mariel) on the final build: run the entire first-session script below, verify every V0 checkbox against prod
2. **Beta** — 3–5 named customer workspaces with hand-holding; watch first sessions live (what do they actually type first?)
3. **GA** — flag flipped for all workspaces; in-product announcement + the [[pitch-today-v2]] menu as onboarding content

---

## Context (why now)

Decided 2026-06-05: **launch narrow now** — don't gate on the full eng fix list. The pitch was rebuilt against the live capability audit (v2), the bugs were consolidated into one register, and the launch contract inverted the bug list into 7 behaviors. What was missing: the **product definition of day one itself** — when every user in every workspace gets the AI, what exactly do they get? This doc is that definition. Security/permissioning is explicitly **assumed handled** by Dan/Sebastián's workstream so this doc can stay focused on product.

The strategic frame ([[winning-vs-horizontal-ai]]): day one is the first move in the moat game. A horizontal AI can't run your saved Tesote reports, can't write rules into your engine, doesn't know your 33 accounts. Day one has to *demonstrate* that, not claim it.

---

## The day-one product, in one paragraph

**Tesote AI on day one is the setup brain and the report narrator for your banking data.** It builds your machine in conversation (rules, categories, counterparties — previewed, approved, applied by the engine to all history) and it runs and explains your reports (saved definitions, deterministic numbers, AI narration on top). It does **not** pretend to be an analyst over raw rows yet — that ships with the 30-day eng gate, as a dated promise, not a silent gap. Identity: *el jefe de finanzas que arma tu máquina* — not a chatbot bolted onto a bank feed.

---

## The first session (the make-or-break 10 minutes)

Adoption is decided in the first session. Choreograph it:

1. **Open** — greeting (rotating headline per [[greeting-rotating-headline-prd]]) + 4–6 capability chips. Chips come from the verified-✅ column only. Candidate set:
   - *"Córreme el flujo de caja de mayo"* (seeded report — guaranteed to exist)
   - *"Proponme reglas para mis movimientos sin categorizar"* (setup en masa)
   - *"¿Qué contrapartes duplicadas tengo?"* (master data)
   - *"¿Cómo cerró mayo vs abril?"* (report comparison, narrated)
2. **First answer must land** — whichever chip they tap, the result is correct, currency-clean, European-formatted, and states its scope (*"sobre el reporte Flujo de Caja VES, mayo, 12 cuentas"*).
3. **First mutation must build trust** — if they go the rules path: preview table with per-row exclude → approve → *"el motor aplicó 14 reglas a 3.847 movimientos históricos"*. The user watches mass work happen without the AI touching a row.
4. **First refusal must convert, not frustrate** — when they ask the inevitable free-form total: *"Para responder eso con números completos necesito correrlo como reporte — ¿te creo uno guardado de gastos por categoría?"* The refusal IS a feature pitch. Never a dead "no puedo".

Anti-goal: the user's first free-form aggregate question producing a confident wrong number. That single event costs the workspace — the user tells their team why they stopped using it.

---

## User stories

### Reports (Pillar 2 — every user, every workspace)

**US-1 — Run my cash flow.** As a CFO, I ask *"córreme el flujo de caja de mayo"* and get the saved definition's output — table + chart — with a narration comparing against April and flagging the biggest movements.
*Acceptance:* works on a brand-new workspace (seeded definitions); May means May 1–31, never a trailing window (W4); multi-currency workspace doesn't error (W8) — output splits per currency.

**US-2 — Explain, don't invent.** As a contador, when I ask *"¿por qué bajó el flujo en mayo?"*, the AI's answer is grounded in the report it just ran — named categories, named counterparties, stated scope — never a number it computed from raw rows.
*Acceptance:* every numeric claim cites its source report + period + accounts (behavior 1's transparency rule).

**US-3 — The honest no.** As any user, when I ask a free-form total ("¿cuánto le pagué a X este año?"), the AI tells me it can't answer that completely yet, says why in one line, and offers the saved-report or rule path — and the 30-day slide items are the dated fix.
*Acceptance:* zero free-form totals over `transaction.search` reach the user; refusal always carries a next step.

### Setup en masa (Pillar 1 — the wedge)

**US-4 — Teach the machine.** As an owner with 6 months of uncategorized movements, I say *"proponme las reglas que cubren la mayoría del volumen"* and get ~10–20 proposed rules with the volume each covers; I review, exclude, approve; the engine applies retroactively to all history.
*Acceptance:* preview shows match counts per rule; per-row/per-rule exclude; post-approve summary states totals applied; audit trail records proposed-vs-executed.

**US-5 — Fix my master data.** As an AP analyst, I ask for duplicate counterparties and missing RIFs; the AI proposes consolidations, I approve, it executes.
*Acceptance:* same preview→approve→audit pattern; nothing merges without explicit approval.

**US-6 — Build my categories.** As a new workspace admin, I describe my operation and the AI proposes a category tree, creates it on approval, and immediately offers the rules that would populate it.
*Acceptance:* the "sin categorizar" bucket is shown loudly in any report it appears in — it's the hook into this story, not something to hide.

### Trust & currency (every interaction)

**US-7 — Currencies never blur.** As a user in a dual-currency workspace (almost every VE workspace), every amount carries its currency, no column ever mixes Bs and USD, and dollarization happens only on request — at the BCV rate of each transaction's date, basis stated.
*Acceptance:* behavior 2 verbatim; P3-class tables are impossible.

**US-8 — Numbers read like Venezuela.** As any user, every amount renders `1.234.567,89` — chat prose, tables, charts, tooltips, both currencies.
*Acceptance:* behavior 6 sweep complete; zero hand-formatted money.

**US-9 — Nothing executes blind.** As any user, every mutation shows me exactly what will change before it changes; approving executes exactly what was previewed; everything lands in an audit trail I can read.
*Acceptance:* behavior 5 universal; a pending approval survives conversation limits (P2).

### Platform (the pre-conditions)

**US-10 — The AI can't hurt Tesote.** As any user (including ones who never open the AI), no chat query can degrade the platform; worst case is the AI apologizing.
*Acceptance:* P1 root-caused + guardrailed (timeouts/limits); load test the heavy-query path.

**US-11 — It finishes or it says so.** As a user mid-task, the AI never silently dies or claims completion without output; if it can't finish, it tells me what state things are in.
*Acceptance:* P2 + P5 closed; no hanging threads.

---

## What the AI says no to on day one (product behavior, not a bug list)

The cut list from [[pitch-today-v2]] enforced in product — the system prompt must hold the same line the pitch does:

| User asks | Day-one response posture |
|---|---|
| Free-form totals/percentages over transactions | Refuse + offer saved report or "te lo dejo como reporte guardado" |
| "Categoriza los últimos 3 meses" (per-row) | Reframe to rules: *"mejor: te propongo las reglas y el motor lo hace todo, histórico incluido"* |
| Deep dives over >100-row slices | Scope to a period/account it can cover honestly, say what's excluded |
| "Concíliame todo" | Supervised, scoped grooming; no headline promises |
| Anything Odoo (for non-Odoo workspaces) | "Disponible con la conexión Odoo" — clean upsell, not confusion |
| Anything inbox/invoicing (until W11 flips) | Not surfaced; chips never advertise it |

Each refusal carries the dated 30-day items where applicable — *"en semanas, no algún día"*.

---

## Surfaces affected

- **IA** (the `/ai` surface) — chips/empty state, system-prompt guardrails, refusal copy, narration templates, preview-pane universality
- **Espacio de Trabajo** — seeded report definitions land here; audit trail surfacing
- No new screens; day one is choreography + seeding + guardrails on the existing surface ([[tesote-ai-design]])

---

## Data model implications

Minimal by design — this is a launch-definition PRD, not a schema PRD:

- Seeded report definitions: template + per-workspace instantiation (eng's seeder)
- Everything schema-heavy lives in the three sibling PRDs already planned (queries-at-scale, currency-doctrine, reports-v2) — this doc sequences them, doesn't duplicate them

---

## AI / automation implications

This whole doc. One addition: the **refusal-to-report conversion** ("¿te lo creo como reporte guardado?") quietly grows each workspace's report library from real demand — by the time the eng gate ships free-form queries, every active workspace has a personalized report set. Day-one constraint becomes data.

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | The seeded default report list (3–5) | Luis (dogfooding now) | Open — gates W7 |
| 2 | Approve/override the six blocker verdicts | Luis | Open ([[launch-readiness-plain-2026-06-05]] scoreboard) |
| 3 | W11 — AP inbox enablement (in or out of this launch) | Luis | Open — this PRD assumes OUT |
| 4 | Day-one chips final copy (VE Spanish) | Luis + Majo | Open |
| 5 | Beta workspace shortlist (3–5 names) | Luis | Open |
| 6 | Confirm security assumptions hold (inherits-user-permissions, workspace isolation, private convos, full audit) | Dan/Sebastián | Open — assumption box above |

---

## Path forward

### V1 wedge

See Intake — V0 is the wedge. The single highest-leverage item: **seed the reports** (decision #1 + the seeder). Everything else on the list is guardrails and fixes; the seeded library is the only thing that makes the first session *positively* good rather than just not-broken.

### What sequences after v1

```
day 1        — this PRD: narrow launch, all users, all workspaces
+30 days     — eng gate ships (queries-at-scale + currency-doctrine + reports-v2 PRDs):
               free-form totals, category cash flow, honest deep dives flip ON;
               refusal copy swaps to capability copy
wave 2       — Odoo connector workspaces (gated on Mariel walkthrough + Bs/USD fix class)
later        — Automations surface absorbs the deterministic/scheduled jobs per taxonomy
```

### Discipline calls

- No new capabilities sneak into day one — anything not in the verified-✅ column waits for its PRD
- The 30-day slide is a **commitment with a date**; if the gate slips, the refusal copy stays honest rather than the date staying put
- Inbox, subscriptions, Tesote-side invoices stay dark until exercised in a sandbox (W12)

---

## References

### Internal source docs

- [[pitch-today-v2]] — the promise this launch keeps
- [[launch-contract-2026-06-05]] — the 7 behaviors (correctness contract)
- [[launch-readiness-plain-2026-06-05]] — blocker verdicts
- [[bug-register]] — consolidated issues, Part 1 = day-one surface
- [[capability-audit-2026-06-03]] — the verified-✅ ground truth
- [[qa-pre-created-reports-2026-06-03]] — reports fix spec
- [[use-case-taxonomy]] — deterministic-vs-judgment doctrine
- [[positioning-the-finance-chief]] — persona/posture
- [[greeting-rotating-headline-prd]] — first-open moment

### External

- Linear ticket: [pending]
- Treasury plan dir: [pending]

### Memory references

- [[project_ai_pitch_launch_narrow]] · [[project_winning_vs_horizontal_ai]] · [[project_tesote_ai_audience]]
