---
title: Tesote AI — How to pitch it today (v2 — launch narrow)
tags: [product, ai, pitch, sales, gtm, today]
updated: 2026-06-05
status: draft
supersedes: pitch-today.md (2026-05-20)
audience: Luis + future sales hire; the operational playbook for prospect conversations, rebuilt against the 2026-06-03 live capability audit
---

# How to pitch Tesote AI — today (v2)

> **The job of this doc.** Same as v1: pitch-ready playbook for the next 30–60 days. **What changed:** v1 was written from aspiration; v2 is written from the [[capability-audit-2026-06-03]] and [[qa-pre-created-reports-2026-06-03]]. Decision (2026-06-05): **launch narrow now** — pitch only what's live-verified, put the eng fixes on a dated 30-day slide. The goal is to launch something that WORKS, even if limited.

---

## The diff from v1 — read this first

| v1 claimed | Reality (audit 06-03) | v2 move |
|---|---|---|
| "Categoriza los últimos 3 meses" (per-tx mass op via chat) | `transaction.search` hard-capped at 100 rows, no pagination, no truncation signal → silent wrong results on any real workspace | **Cut.** Replaced by the rules reframe (below) |
| "Hazme el flujo de caja" (free-form reports) | Category cash flow structurally impossible; free-form aggregation routes through the capped search | **Narrowed** to saved report definitions, which run correctly |
| "Las posibilidades son casi infinitas" | The 100-row cap makes half the menu produce confident wrong numbers | **Cut.** Worst possible claim for a finance AI |
| "Concilia todos los movimientos de Banesco" | BSL reads ✅ but cross-system link still string-parsed; no scheduled pass | **Demoted** to supervised/scoped, not headline |
| Odoo mass workflows | `erp_console` is the strongest verified surface: reads, VE-fiscal bill creation, dry-run, audit trail, Mariel dogfooding | **Promoted** to a headline pillar |

---

## The reframe — the line that replaces "mass operations"

The mass story doesn't die; it moves from the AI to the engine. The only mass mechanism that doesn't route through the capped read path is the **rules engine** — server-side, retroactive, unbounded.

> **"No categorizas 10.000 transacciones. Le enseñas a Tesote 20 reglas en una conversación — y el motor categoriza todo: el histórico completo y todo lo que llegue mañana."**

Why this is a *stronger* pitch than per-row AI edits:

- **It's true today.** Rules CRUD verified live; retroactive application is engine behavior, not a chat read.
- **Deterministic engines are what finance people trust.** "The AI guessed 10,000 categories" is scary. "The AI wrote 20 rules you reviewed, the engine applied them" is auditable.
- It matches the doctrine already locked in [[use-case-taxonomy]]: deterministic work → engine; chat → judgment + setup.

The AI's identity in v2: **the setup brain that builds your machine in one conversation** — not the bulldozer that touches every row.

---

## Launch v1 — the three pillars (all live-verified 2026-06-03)

### Pillar 1 — Setup en masa (Tesote workspace)

One conversation replaces weeks of manual setup:

- *"Mira mis movimientos sin categorizar, proponme las reglas que cubren la mayoría del volumen, y créalas."* → AI reverse-engineers rules from patterns; engine applies retroactively to all history ✅
- *"Crea las categorías que le faltan a mi operación."* ✅
- *"Encuentra contrapartes duplicadas y consolídalas; resuelve los RIF que faltan."* ✅ (counterparty CRUD + RIF in external_identifier, 438-record workspace verified)

**Wedge:** *"El primer día con Tesote no es un proyecto de implementación. Es una conversación."*

### Pillar 2 — Reports = saved definitions, run + narrated

- *"Córreme el Flujo de Caja mensual"* → `report.run` against a saved definition, verified correct (multi-account VES rollup, respects config dates) ✅
- AI narrates the output, compares periods, flags movements — **on top of a deterministic report**, never aggregating rows itself
- Requires **seeded definitions per workspace** (the agent can only run what `list_definitions` returns) — see launch checklist

**Wedge:** *"Tus reportes corren igual todos los meses. La AI te los explica, no los inventa."*

### Pillar 3 — Odoo mass workflows (for Odoo customers)

The strongest surface we have, and the one with a live design partner:

- VE-fiscal-fluent bill/invoice operations: `control_number`, `conversion_rate` doctrine, ISLR per-line — the `shape_hints` moat artifact ✅★
- **Dry-run preview on every mutation + audit trail** (`recent_audits` verified — quietly a customer-facing feature: "every action the AI took, dry-run/live split")
- BSL enumeration works → scoped reconciliation grooming, supervised
- Proof point: Mariel actively dogfooding (dry-run `account.move` creates June 1–3)

**Wedge:** *"La AI nunca toca tu Odoo a ciegas. Todo es preview primero, y todo queda auditado."*

### The moat moment still works — scoped

The factura-fiscal prosecution (*"¿cuáles facturas de mayo no tienen factura fiscal anexa y qué riesgo SENIAT tengo?"*) runs on Odoo console reads, not the capped tx search. Keep it as the ChatGPT-can't-do-this moment — **always scoped to a period** (a month of bills, not "everything ever").

---

## What we no longer say (until the eng gate ships)

- ❌ *"Categoriza los últimos 3 meses"* as a chat operation → say the rules line instead
- ❌ Free-form totals or aggregate questions on transactions ("¿cuánto gasté en X?") → only via saved reports
- ❌ *"Las posibilidades son casi infinitas"* → the narrow-and-true menu above
- ❌ Deep-dive investigations over >100-row slices
- ❌ Headline reconciliation ("concílialo todo") → supervised, scoped grooming only
- ❌ Anything that depends on `inbox.*` / Tesote-side invoices / subscriptions — shipped but never exercised; no sandbox to demo safely

Everything in v1's "What NOT to claim" list still applies on top of this.

---

## The dated 30-day slide (the eng gate)

Three small server fixes flip most of the cut claims back on — spec'd in [[qa-pre-created-reports-2026-06-03]] §Fix-spec and [[capability-audit-2026-06-03]] §6:

1. **`cash_flow_by_category` report type** (mirror `cash_flow_by_counterparty` 1:1) → unblocks the category cash flow ask with zero pagination work
2. **`transaction.search` pagination + envelope** (`has_more` signal) → re-enables honest deep dives; the AI can say "showing 100 of 1,432 — I'll write a rule instead"
3. **`cash_flow.statement` date handling** (honor dates without `preset: custom`; error on unknown params instead of silent no-op) → kills the plausible-wrong-answer class

Plus: `bank_connection.status` real `last_synced_at` (so the AI can answer *"¿están al día mis bancos?"*) and the BSL `tesote_transaction_id` structured field (last blocker of the headline recon demo).

On the customer slide these are **named features with a month**, not "soon": *"En 30 días: flujo de caja por categoría, análisis profundo sin límite de filas, conciliación de punta a punta."*

→ This punch list is eng-facing: PRD-ify with the intake block + PRO-* ticket + `/tesote-plan` in treasury (skills: `database-design`, `product-management`). Don't let it ride as a QA log.

---

## The 15-minute demo — v2 script

**Min 0–1 — posture (unchanged from v1):** the chief line still opens. The persona survives the narrowing; only the scope claim changes.

**Min 1–4 — the setup-en-masa moment (NEW headline):**
> *"Proponme las reglas que cubren la mayoría de mi volumen sin categorizar, y créalas."*

What lands: AI reads patterns, proposes ~10 rules with the volume each covers, creates them, engine applies to all history. The buyer watches months of backlog resolve **without the AI touching a single row**. Deliver: *"No categorizó 5.000 transacciones. Escribió 10 reglas que tú aprobaste — y el motor hizo el resto. Eso es auditable."*

**Min 4–8 — the moat moment (scoped):** factura-fiscal audit on a month of Odoo bills + SENIAT risk framing. Deliver: *"Esto no lo hace ChatGPT."*

**Min 8–12 — the trust moment (NEW):** an Odoo mutation in dry-run — show the preview, show `recent_audits` with the dry-run/live split. Deliver: *"Todo lo que la AI hace en tu Odoo: preview primero, auditado siempre. Tú apruebas; él trabaja."*

**Min 12–14 — the dated slide** (the 3 fixes, with the month).

**Min 14–15 — hand over the keyboard.** Keep this — it's still the wedge. But seed them with prompts from the verified menu; a free-form aggregate question as their first prompt is the worst possible first impression.

**The historic close ("antes y después de finops en Venezuela"):** park it. v2's narrowed demo doesn't earn it yet — it earns *"esto funciona hoy, y no te miente"*, which for a finance buyer is worth more. Bring the historic line back when the eng gate ships and the full mass story is real.

---

## Launch checklist (before the first v2 pitch)

- [ ] **Seed report definitions** in every demo/customer workspace (Flujo de Caja VES + USD at minimum) — Pillar 2 is empty without them
- [ ] **Seeded sandbox workspace** for demos — today verifying flows means mutating Tesote Finance prod ([[capability-audit-2026-06-03]] §5.6)
- [ ] **System-prompt guardrails match the pitch**: AI must refuse free-form totals and offer the report/rule path instead — the product must enforce what the pitch promises
- [ ] **File the eng-gate PRD** → `/tesote-plan` (above)
- [ ] **Ask Mariel why dry-runs aren't flipping live** (Jun 1–3 all dry-run, none confirmed) — cheapest design-partner signal available; directly informs the trust-moment demo

---

## Cross-links

- [[pitch-today]] — v1 (2026-05-20), superseded by this doc; demo mechanics + objection bank still mostly valid
- [[capability-audit-2026-06-03]] — the ground truth this doc is built on
- [[qa-pre-created-reports-2026-06-03]] — the reports failure analysis + fix spec
- [[pitch-agents-plus-ai]] — the capability catalog (aspirational; read with the audit beside it)
- [[positioning-the-finance-chief]] — the posture (unchanged)
- [[use-case-taxonomy]] — the deterministic-vs-judgment doctrine the reframe leans on
