---
title: Tesote AI — the pitch (Agents + AI)
tags: [product, ai, pitch, sales, mcp, agents, gtm]
updated: 2026-05-13
status: draft
audience: Luis (primary); template for sales conversations with VE prospects
---

# Tesote AI — The Pitch

> **The job of this doc.** Give us one page we can take into a customer conversation and have them say: *"If you can give me this MCP today, I can start using Odoo this way — that's all I need."* When that happens 3 times in a row, we have product-market fit on the AI surface.
>
> **Not** an internal architecture doc — that's [[../tesote-2026-command-center-prd]]. **Not** a feature list — that's the cockpit PRD ([[../automations/accounting-automation/odoo-prd]]) and flagship workflows ([[../automations/erp-ai/flagship-workflows]]). **This** is the narrative that ties them into a single "buy me" sentence.
>
> Internal/English here per convention; client-facing Spanish version comes after Luis signs off.

---

## The one-sentence pitch

> **Tesote gives finance teams two things on top of their Odoo: Agents that run the recurring work, and an AI that gives them superpowers on top of everything else. Install it today, run Odoo a different way tomorrow.**

---

## The two-layer frame

Every demo opens with this slide. It's the only frame the customer needs to hold.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   TESOTE AI                                                 │
│   ───────────                                               │
│   The superpower layer. Prompt-driven.                      │
│   • "Categorize the last 3 months of bank statements"       │
│   • "Cobra esta semana"  → 23 personalized WhatsApps        │
│   • "Concílialo todo"    → 84 BSLs matched in 30 seconds    │
│   • "¿Estoy lista para declarar IVA?"                       │
│   Manages large datasets with one prompt.                   │
│   Edits hundreds of invoices in one stroke.                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   TESOTE AGENTS                                             │
│   ────────────                                              │
│   The autopilot layer. Recurring, predictable, runs itself. │
│   • Smart rules + mass categorization                       │
│   • AP inbox: emails → vendor bills, automatic              │
│   • Reconciliation: bank txns ↔ invoices, continuous        │
│   • Retention auto-calc on every payable                    │
│   • Reminder cadences on every overdue invoice              │
│   The 80% that should have been automated 10 years ago.     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ODOO (execution layer — the customer barely sees it)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**The distinction matters because:**
- Agents = *trust*. You set them up once and stop thinking. They are the relief from the grind.
- AI = *leverage*. You ask, it executes, you supervise. It is the 100× moment.

Customers buy Agents. They fall in love with AI.

---

## By function — what we have, what the AI adds, what you can do today

For each function: the agents that already run (or are next to ship) + the AI prompt that turns the same data into 100× leverage + the wedge sentence the buyer should hear.

---

### 1. Receivables (Cobros / AR)

**The Agents (recurring, runs by itself)**
- Cobros pipeline: drafts → sends → tracks every invoice (sender-side)
- Reminder cadence engine: configurable per counterparty (warm / firm / chronic late-payer tone)
- Outbound routing: email / WhatsApp / both, per counterparty preference
- Reconciliation writeback: when payment lands, paid status flows back to Odoo automatically
- (Soon) FX-aware invoice generation: BCV + per-customer differential applied at emission, frozen at payment

**The AI (one prompt, massive leverage)**
- *"Cobra esta semana"* → pulls aged AR, segments by overdue band + payment history, drafts 23 personalized Spanish WhatsApps in your voice, queue with one-tap Approve/Edit/Skip per row
- *"Show me every customer that's overdue more than 30 days with > $5k outstanding"* → instant filter across N entities
- *"Re-draft this batch in a firmer tone"* → bulk edit
- *"Mark Polar's last 4 invoices as paid with this bank statement line"* → mass reconciliation by intent

**Wedge sentence**: *"You stop chasing receivables — the agents do it. When you do touch them, you do it 50 at a time, not one at a time."*

---

### 2. Payables (Pagos / AP)

**The Agents**
- Inbound inbox (Bandeja Mágica): vendor invoices arrive via email → parsed → vendor matched → retentions computed → vendor bill drafted → ready for one-tap approval
- Payment routing: vendor's preferred channel (Tesote-network instant / BNC ACH / Banesco / wire) chosen automatically from the counterparty record
- Comprobante de retención: auto-generated and delivered on every payment
- Approval queue: every drafted bill sits in a single queue, not 6 inboxes

**The AI**
- *"Pay every approved vendor bill due this week"* → composes the payment run, shows routing + retentions, one-tap execute
- *"Find every duplicate vendor across our 3 entities and merge them"* → mass counterparty cleanup
- *"Apply retention rules to these 80 historical bills"* → bulk back-application
- *"Which 10 vendors are eating most of our AP cycle time?"* → instant operational diagnostic

**Wedge sentence**: *"The agents make the bill. You don't enter data. The AI lets you pay 80 at once and answer questions about your AP that used to take a controller a day."*

---

### 3. Reconciliation

**The Agents**
- Connect bank rails feed every transaction into Tesote across VE + PA + RD + US + Caribe banks
- BSL ↔ Tesote tx linkage via `TESOTE-{uuid}` (the moat — no Odoo plugin has this)
- Auto-matching engine: bank txn ↔ invoice / vendor bill via shared payment_batch_id or pattern match
- Continuous (not periodic) reconciliation — every new bank txn checks against open AR/AP

**The AI**
- *"Concílialo todo"* → drag a bank statement, AI matches 84 BSLs against open invoices in 30 seconds, surfaces only the 6 it can't match, you one-tap the rest
- *"Reconcile every Banesco transaction from April that's still pending"* → bulk catch-up
- *"What's the residual after this match? Show me what would change in Odoo before I commit."* → dry-run preview
- *"Which transactions have I never reconciled in the last 6 months and why?"* → operational audit

**Wedge sentence**: *"What used to be 4 hours per bank-statement is now 30 seconds and a tap. And the AI lets you go back and clean up months of mess in one prompt."*

---

### 4. Categorization & Rules

**The Agents**
- Smart categories: shared library + workspace-specific
- Transaction rules: pattern-match → auto-categorize on every incoming bank txn
- Mass rule creation: build a rule from any txn, applies retroactively to all matches
- Counterparty assignment: auto-assigns when the rule has a counterparty field
- Receipt email send: triggers automatically when a categorized rule says so

**The AI**
- *"Categorize the last 3 months of uncategorized transactions"* → bulk classify with confidence scores, batch approve the high-confidence ones
- *"Create rules for the 10 most common uncategorized patterns I'm seeing"* → reverse-engineer rules from data
- *"Move every transaction tagged 'Gasolina' to 'Combustibles y lubricantes'"* → mass recategorize
- *"What's miscategorized in the last quarter?"* → anomaly detection on top of the rule engine

**Wedge sentence**: *"The rules do 80% on autopilot. The AI handles the 20% — and the mass cleanup when you migrate ERPs."*

---

### 5. Counterparties

**The Agents**
- SENIAT-resolved identity on every counterparty (RIF / RNC / EIN)
- Multi-entity billing relationships: one counterparty, N relationships across your entities, day-one
- Subscription records on the counterparty: cadence, FX rule, payment terms, contract reference
- Counterparty portal (PRO-112): your customers / vendors get a Tier 1 surface to view + pay

**The AI**
- *"Find every counterparty without a RIF and pull it from SENIAT"* → bulk identity resolution
- *"Merge these 4 duplicates into the right one"* → confident dedupe
- *"Which customers haven't paid in 60+ days and aren't on a subscription?"* → cross-table insight
- *"Build me a counterparty 360 for Polar across all 3 entities"* → composite view, no spreadsheet

**Wedge sentence**: *"One counterparty record, all entities, all subscriptions, all rates. The AI lets you query it like a database without being a DBA."*

---

### 6. Close & Reporting

**The Agents**
- Inbound inbox keeps your unposted documents at zero on a rolling basis
- Continuous reconciliation keeps unmatched bank txns visible all month, not just at close
- Productized close package: P&L, BS, cash, AR/AP aging, variance vs prior period — auto-generated from Tesote state (not pulled from Odoo at close time)
- Scheduled reports: AR aging, AP aging, retention summaries, cash position — sent to whoever should see them

**The AI**
- *"Ciérrame mayo"* → runs 18 verifications, surfaces 8 issues with proposed fixes, you tap through approvals, get a PDF close-package in 10 minutes (used to be 5 days)
- *"Hazme un brief para el CEO de mayo"* → prose memo with headline, key figures, 3 highlights, 3 watchpoints, mini-charts — drafted email ready to send
- *"Compare May this year vs May last year and tell me what's notably different"* → variance with narrative
- *"Generate the same close package for our DR entity"* → multi-entity scale-out

**Wedge sentence**: *"Month-end goes from 5 days of fire-drill to 10 minutes of supervised approval. The brief goes from 3 hours of pulling numbers to 30 seconds of prose."*

---

### 7. SENIAT / Tax compliance

**The Agents**
- Auto-detect contribuyente especial from the SENIAT profile on the counterparty record
- Auto-calculate IVA/ISLR on every payment
- Auto-generate + auto-number + deliver comprobantes de retención
- YTD ledger: every retention applied is in a single book
- Libro de compras / Libro de ventas consistent with posted invoices on a rolling basis

**The AI**
- *"¿Estoy lista para declarar IVA del período?"* → 30+ SENIAT verifications, traffic-light verdict, proposed fixes for every yellow/red, generates libros + borrador de planilla
- *"Validate the RIFs on every counterparty with activity this quarter"* → bulk integrity check
- *"Generate the libro de ventas for May in SENIAT format"* → one-shot output
- *"Find every retention I should have applied in Q1 but didn't"* → audit-the-auditor

**Wedge sentence**: *"This is the single thing ChatGPT can never do for you. VE-native, SENIAT-fluent, audit-ready in one prompt."*

---

## The "install today" sentence

The pitch lands when this becomes true:

> **The customer can install the Tesote AI MCP today on their Odoo and start running it the way the demo showed — within the same conversation.**

What "install today" actually means:
- Tesote AI surface available in Tesote UI (chat + suggested-prompt gallery) — single-tenant, scoped to their workspace
- (Optional power-user mode) Same MCP available in Claude Desktop / Cursor for the technical buyer who wants to drive from there
- Connected to: their Odoo (via existing MCP), their bank rails (via Connect if hooked up), their counterparty/subscription/retention data
- Comes with: the 6 flagship workflows live, plus free-prompt mode

What "install today" does **not** mean:
- A migration project
- An "implementation phase"
- A training engagement
- A custom build

If the demo starts to require any of those, we've failed the pitch.

---

## The customer test — the only success metric for this pitch

After the demo, the customer says — unprompted — one of these three lines:

1. *"Can you give me this MCP today? I'd start using Odoo this way right now."*
2. *"Wait, this isn't a roadmap? This works today?"*
3. *"What's it cost? When can we sign?"*

If we get any of the three from 3 prospects in a row, we have the pitch.

If we get *"interesting, let's see a roadmap"* — the pitch is wrong, recalibrate.

---

## Sequencing — what we show in which meeting

| Meeting | What we show | Primary buyer |
|---|---|---|
| **Meeting 1 (15 min demo)** | Cobranzas Autopilot + Conciliación Relámpago + Brief para el CEO | Controller + CEO |
| **Meeting 2 (CFO depth)** | Cierre Express + counterparty 360 query + multi-entity close | CFO |
| **Trial / pilot** | Bandeja Mágica (Gmail watcher) + mass-categorize-3-months + free-prompt mode | Daily operator |
| **Procurement / compliance** | Pre-Auditoría SENIAT + libros generation + audit trail | Finance director |

The 15-minute demo is the wedge. The trial is the habit. The procurement meeting closes.

---

## What we still need to build vs. show today

To deliver the pitch above without lying, we need to be honest internally about each function's readiness. Color-coded for the demo:

| Function | Agents readiness | AI readiness (v1) | Demo today? |
|---|---|---|---|
| Receivables | 🟢 cobros pipeline live, FX-aware in build | 🟡 cobranzas autopilot agent in design ([[../automations/erp-ai/flagship-workflows]]) | 🟢 yes, with copy-to-clipboard fallback on WhatsApp send |
| Payables | 🟡 inbound inbox v1 in build | 🟡 pay-run agent designed, not built | 🟡 yes with seeded inbox + Figma flow |
| Reconciliation | 🟢 Connect feed + matching engine live | 🟡 needs `bank_statement_lines` MCP action ([[tesote-workspace-mcp-feedback]] #1) | 🟢 yes once MCP gap closes (~2 wks) |
| Categorization | 🟢 rules + mass categorize live in Tesote | 🟢 prompt against existing engine works today | 🟢 yes, today |
| Counterparties | 🟢 SoR schema + multi-entity locked | 🟢 SENIAT lookup + dedupe demoable | 🟢 yes, today |
| Close & Reporting | 🟡 productized close in build | 🟡 brief workflow ~2 weeks to demo-ready | 🟡 yes with template + LLM prose |
| SENIAT | 🟡 retention engine v1 in build | 🔴 30+ checks engine is 4–6 wks | 🟡 yes with 5-check version |

🟢 demoable today / 🟡 demoable with light scaffolding / 🔴 not yet.

**Decision implied:** the demo we sell in the next 30 days = Receivables + Categorization + Counterparties + Reconciliation (once MCP gap closes). That's the wedge. Everything else is the *roadmap* we sell.

---

## What to call it (naming question)

Three candidates for the productized name; pick before the first prospect call:

1. **Tesote AI** (current default) — clean, ties to the workspace shell IA section, easy to extend (Tesote AI for Odoo, Tesote AI for Cobros, ...).
2. **Tesote AI + Agents** — explicit about the two layers; honest; verbose.
3. **Tesote Copilot** — familiar metaphor; but "copilot" is now generic; loses VE-specificity.

Recommend: **Tesote AI** as the umbrella; **Agents** is a frame inside it, not a separate SKU. The pitch slide is the only place we draw the two-layer distinction.

---

## Open calls for Luis

1. **Pick the 3 wedge workflows** for the live demo (recommend: Cobranzas + Conciliación + Categorización-en-bulk). Lock by EOW.
2. **Pick 3 prospects** for the first wave of pitch tests. Casagri? El Dorado? Fospuca? Add one current Tesote customer dogfooding for confidence.
3. **Sign off on "install today" claim** — if any of the 🟡 cells above can't be 🟢 in 30 days, we soften the line to "this week we activate the AI on your Odoo." Less crisp, but still strong.
4. **Naming** — Tesote AI as umbrella, OK?
5. **Spanish version** — when do I draft `tesote-ai-pitch-es.md` for the actual customer conversation? Suggest: after item 1 lands so we don't translate twice.

---

## Cross-links

- [[../tesote-2026-command-center-prd]] — the full architecture this pitch sits on top of
- [[../automations/erp-ai/flagship-workflows]] — the 6 workflows' deep choreography
- [[../automations/erp-ai/odoo-mcp]] — the MCP / chat surface strategy
- [[../automations/accounting-automation/odoo-prd]] — the cockpit PRD (Caps #1/#2/#3/#5 = the Agents in this pitch)
- [[../automations/accounting-automation/inbound-inbox]] — the AP / inbound inbox detail
- [[tesote-workspace-mcp-feedback]] — what we need from the MCP to deliver the demo we promise
- Memory: [[odoo-mcp-framing]], [[tesote-command-center]], [[payments-10x-bet]]
