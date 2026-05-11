---
title: Odoo PRD — Tesote as the Intelligent Cockpit for Odoo
tags: [product, automations, odoo, erp, 10x]
updated: 2026-05-11
status: draft
---

# Odoo PRD — Tesote as the Intelligent Cockpit for Odoo

> Vision-first draft. Repo/Notion/Linear material gets folded in later — first job is to get the big picture right.

## TL;DR

We started by building a one-way bank-data uploader into Odoo. We're going to end up replacing the Odoo UI for the people who actually do the accounting work.

Tesote becomes the cockpit. Odoo runs silently in the background as the system of record. Finance teams (controllers, CFOs, AP/AR clerks) live inside Tesote — propose, review, approve, post — and Odoo just receives clean, structured, auditable entries.

This is a much bigger product than "ERP connector." It's an **AI-first finance operations layer** that happens to use Odoo as its accounting backend. That reframe changes pricing, positioning, target customer, and competitive set.

## The reframe (what changed)

| | Before | Now |
|---|---|---|
| **Product** | Bank data → Odoo connector | AI cockpit on top of Odoo |
| **Surface area** | Push-only, one Odoo object | Read + write across the accounting graph |
| **User** | Whoever turns the connector on | The whole finance team, daily |
| **Time saved** | Bank import clicks | The whole month-end close |
| **Defensibility** | Integration plumbing | Workflow + AI learning loop + per-client mapping config |
| **Pricing logic** | Per connection | Per finance seat or % of work automated |
| **Source of truth** | Odoo for everything | Odoo = books; Tesote = operational layer (counterparties, categories, comments, rules, AI training) |

What unlocked the reframe: Odoo's API exposes way more than we initially targeted. The full accounting graph is reachable both ways — `account.move`, `account.move.line`, `account.account`, `account.bank.statement(.line)`, `res.partner`, `account.analytic.account/.tag`, `account.tax`, `product.template`. Once you can read and write the whole graph, the connector framing is too small.

## Vision (what "won" looks like in 18 months)

A controller at a Venezuelan mid-market company opens her laptop on the 1st of the month. Her Tesote dashboard shows:

- 96% of last month's transactions were auto-coded and auto-posted to Odoo. The 4% that weren't are queued, each with an AI-suggested account + reasoning. She approves them in 12 minutes.
- 14 vendor invoices arrived overnight via email/WhatsApp. Tesote OCR'd them, matched against open POs, and queued draft `account.move` entries. She approves 11, kicks 3 back to the AP clerk with comments.
- Bank reconciliation is at 98% — Tesote matched bank lines against open Odoo entries automatically. She clicks through the 2% exceptions.
- Month-end accruals are pre-drafted with AI-suggested amounts based on the trailing 6 months. She approves the package.
- The CFO sees a real-time P&L vs. budget in his Tesote view, asks "why is COGS up 14% in Caracas?" in plain language, and gets back the 3 transactions driving it.

She has not opened Odoo this month. She doesn't need to. **Odoo runs the books; Tesote runs the team.**

## Who this is for

**Primary users**
- **Controller** — owns the close, owns the books. Lives in the cockpit daily.
- **CFO** — wants visibility, wants the close to be fast and clean, wants AI leverage without losing audit trail.
- **AP/AR clerks** — do the volume work. Code transactions, key invoices, chase reconciliations. Tesote turns this into a review-and-approve job instead of a data-entry job.
- **Finance analysts** — query data, build reports, spot anomalies.

**Primary buyer**: CFO or Controller. Bought as a finance-team productivity tool, not as IT/integration software.

**ICP for v1**: VE-based mid-market companies (50–500 FTEs) that already run Odoo Accounting and have a 2–8 person finance team drowning in manual coding/reconciliation work. Multi-bank, high transaction volume.

**Why this ICP**: they have enough volume to feel the pain, enough finance staff to use the cockpit, and Odoo deep enough to make the bidirectional integration valuable. Smaller companies don't have the volume; larger ones outgrow Odoo.

## Why now

- **Odoo adoption is accelerating in LATAM** — it's the practical default for mid-market companies that can't afford SAP/Oracle.
- **LLMs are finally good enough at accounting reasoning** — coding transactions, matching invoices, drafting accruals — at a price point where they can run on every transaction, not just batch jobs.
- **Tesote already owns the bank data pipe** — Connect gives us the cleanest possible source of truth on what actually happened in the bank. That's the moat: most competitors start from the ERP side and have to fight for clean bank data. We start from clean bank data and walk up into the ERP.
- **Manual accounting work in VE is brutal** — multi-bank, multi-currency, manual reconciliation, no good banking APIs. Pain is acute, willingness-to-pay is high.

## Phasing

### Phase 1 — Bank data → Odoo (LIVE)
Tesote pushes formatted bank transaction records into Odoo as `account.bank.statement.line`s. One-way. Already in production with at least one client.

**What this proves**: we can write to Odoo reliably. We own the bank data layer.

**What this doesn't do**: nothing intelligent. Just an upload pipe.

### Phase 2 — Pull from Odoo (IN PROGRESS)
Tesote reads the full Odoo accounting graph: chart of accounts, vendors/customers (`res.partner`), invoices (`account.move`), journal entries (`account.move.line`), bank statements, reconciliation status, analytic accounts, taxes, products.

**What this unlocks**: the cockpit can finally render Odoo state. We can show what the books look like, what's reconciled, what's open, what's coded vs. uncoded. Without read access we're blind; with it, we can build any UI on top.

**What this doesn't do**: we can show, but not yet act.

### Phase 3 — Write back from the cockpit (PLANNED — this is the big bet)
Tesote becomes the place where finance work happens. Every action — code a transaction, post a vendor bill, confirm a reconciliation, draft an accrual — originates in Tesote and gets written into Odoo as the appropriate object.

This is where the product stops being a connector and becomes the cockpit.

## What Tesote owns vs. what Odoo owns (source-of-truth model)

The cockpit framing forces a question we've been ducking: **where does each piece of data actually live?** This is the most consequential architectural decision in the PRD. Get it wrong and we end up either (a) a thin UI on top of Odoo with no leverage, or (b) a parallel system that constantly drifts from the books.

The right model is the **Ramp model**: Tesote owns the operational taxonomy and workflow layer. Odoo owns the legal/GAAP record. The integration is a *mapping* layer between them, not a sync layer.

Why this matters:
- **Thin-UI model** (everything lives in Odoo, Tesote is a face) — every action requires Odoo to be set up correctly first. Vendor must exist in Odoo before you can code a transaction. Account must exist in the CoA before you can categorize. The friction kills the cockpit experience.
- **Parallel-system model** (Tesote and Odoo each have their own truth, with sync) — two sources of truth, every conflict is a support ticket, audit trails diverge.
- **Ramp model** (Tesote owns workflow, Odoo owns books, mapping in between) — the finance team works in Tesote's language, Odoo gets clean translated entries. The mapping config IS the integration.

**Tesote is the source of truth for how the finance team thinks. Odoo is the source of truth for what the books say. The export is a translation.**

### Primitive-by-primitive

#### Counterparties (today: Tesote-native)
Tesote already has counterparties as first-class objects.

**Call**: stay Tesote-native. Counterparty in Tesote = the business entity ("Movistar"). Maps to one or more `res.partner` records in Odoo (in Odoo a single business may have multiple partner records per VAT entity, per branch, etc.). The mapping is M:N and configured per client during onboarding.

**What this unlocks**: AP clerks can create counterparties in Tesote on the fly when a new vendor invoice arrives, without round-tripping to Odoo. The first time a counterparty is used in a posted transaction, Tesote auto-creates the matching `res.partner` in Odoo (or attaches to an existing one).

**Edge case**: counterparties created directly in Odoo (by another tool, or by the accountant). Pull-and-reconcile flow runs on each sync; controller resolves duplicates.

#### Categories (today: Tesote-native, hierarchical with levels)
Tesote has its own category system with multiple levels. Odoo has `account.account` (the GAAP chart of accounts).

**Are they the same thing? No.** This is the most important distinction in the whole product.

- **Categories (Tesote)** = how the *business* thinks about money. "Marketing > Paid Ads > Meta", "Operations > Logistics > Combustible". Hierarchical, business-language, designed for a non-accountant to navigate.
- **Chart of accounts (Odoo)** = how the *accountant* thinks about money. "5.1.2.3 Gastos de Publicidad", "6.2.1 Combustible". Flat numeric structure, GAAP-aligned, often opaque to non-accountants.

**Call**: keep them separate. Tesote categories are the daily workflow primitive. They map to Odoo CoA accounts (typically M:1 — many Tesote categories collapse into one GL account; sometimes 1:M when a category needs to split across accounts). The mapping is configured during onboarding and editable by the controller.

**Why this is the Ramp move**: Ramp employees categorize spend in Ramp's UI using Ramp's taxonomy. They never see QuickBooks accounts. The controller defines the mapping once. This is a big part of why Ramp is pleasant to use and why it won.

**Implication for AI Transaction Coding**: the AI suggests *Tesote categories*, not Odoo accounts. The Tesote→Odoo mapping happens at posting time, deterministically. This is dramatically easier to get right and dramatically easier to explain to users than "the AI guessed account 6.1.2.3."

**What we may need to rewrite**: today's category model in Tesote was built without this framing. If it was designed assuming "one day this becomes the CoA" or "this is a 1:1 mirror of CoA," that needs to flip to "this is the operational taxonomy; the CoA is downstream."

#### Comments at transaction level (today: Tesote-native)
Tesote has comments per transaction. Odoo has `mail.message` (chatter) attachable to almost any record.

**Call**: stay Tesote-native, with optional one-way sync. The full conversation lives in Tesote (where the team-internal back-and-forth happens). When the transaction posts to Odoo, the *latest comment* (or a controller-configured summary) gets pushed as the narration on the journal entry. Audit trail in Odoo, conversation in Tesote.

**Why not full chatter sync**: most comments are operational ("ask vendor for receipt", "is this OK?", "double-check with Maria"). They're not relevant to the GAAP record. Polluting Odoo's chatter with this noise makes Odoo *worse* for the people who do live there (auditors, external accountants).

#### Auto-rules (today: Tesote-native, for both categories and counterparties)
Pure Tesote layer. Odoo has its own reconciliation rules but they're inferior and configured per-client-per-Odoo-instance.

**Call**: stay Tesote-only. Auto-rules apply *before* the Tesote→Odoo mapping. The rules engine operates on Tesote primitives (categories, counterparties), not Odoo primitives. This keeps rules portable across clients and decoupled from any individual client's CoA structure.

**Where this is heading**: today's rules engine is presumably keyword/pattern based. The future state is the AI Transaction Coding loop (Phase 3 capability #1) — at maturity, rules become a fallback for the AI, plus a power-user mechanism for hard constraints ("anything from this counterparty always goes to this category, no AI override").

### The mapping layer (the thing we haven't built yet)

Per client, configured during onboarding, stored in Tesote, editable, **versioned**:

- **Counterparty mapping** — Tesote counterparty → Odoo `res.partner`(s)
- **Category mapping** — Tesote category → Odoo `account.account`
- **Tax mapping** — Tesote category × jurisdiction → Odoo `account.tax`
- **Analytic mapping** — Tesote tags / cost centers → Odoo `account.analytic.account`

Versioning matters: when an auditor asks "why did this transaction post to account X?", we need to replay the mapping that was in effect at posting time, not the current mapping.

This mapping config is also a **massive defensibility asset**. Six months of mapping refinements + AI training on the client's corrections + a custom auto-rule library = enormous switching cost. Going back to bare Odoo (or to a competitor) means rebuilding all of that from zero.

### Walking back one non-goal

Earlier I said "Tesote does not store the GL." That's still true — Odoo holds the legal GL.

But Tesote DOES own the **operational ledger**: every transaction tagged with a Tesote category, a counterparty, comments, audit trail, AI confidence scores, mapping version, approval history. That's its own first-class data model. It is not a copy of Odoo. It's the layer Odoo doesn't have and never will.

## Phase 3 capabilities (priority order)

Numbered = build order. Each one stands alone and ships value, but stacking them is what turns this into the cockpit.

**v1 scope: ship capabilities #1, #2, #3, #5.** The other three (#4 Accruals, #6 Reporting, #7 Approvals) are post-v1 — important, but not what the cockpit needs to be valuable on day one. The four v1 caps stack cleanly: counterparty hygiene (#5) is the foundation, AI Transaction Coding (#1) is the workhorse, AP Automation (#2) is the wedge for AP clerks, Bank Reconciliation (#3) is the close-blocker we kill.

### 1. AI Transaction Coding
**What**: Every transaction (from bank, from invoice, from anywhere) lands in a Tesote queue with an AI-suggested **Tesote category**, counterparty, analytic tag, and cost center. Reasoning shown ("matched 92% of similar past transactions to 'Operaciones > Servicios > Internet'"). Finance team approves, edits, or rejects. On approval, the Tesote→Odoo mapping translates category to `account.account` and counterparty to `res.partner`, then posts the journal entry to Odoo. The model learns from corrections.

**Critical**: AI suggests in *Tesote's taxonomy*, not in Odoo's CoA. This makes suggestions explainable to non-accountants and decouples the AI quality from the cleanliness of any specific client's CoA. See "What Tesote owns vs. what Odoo owns" above.

**Why this is #1**: it's the highest-frequency manual task in any finance team. If we automate this well, we've earned the right to do everything else. It's also the most natural showcase for the assisted→automated learning loop. Today's auto-rules engine is the proto-version of this; Phase 3 #1 is what it grows up into.

**Auto-pilot graduation**: high-confidence routine transactions (recurring SaaS payments, payroll, utilities) auto-post after N successful human approvals. Configurable per client, per category, per counterparty.

**Role-aware visibility of category vs. CoA**: the Ramp principle is "clerks shouldn't think in GL accounts" — but that doesn't mean hide the mapping from everyone. Per role:

- **Clerk queue** — Tesote category only. CoA hidden. If clerks see the CoA, they get tempted to "fix" the wrong field.
- **Controller queue + transaction detail** — toggle to show a CoA column (default off). Always visible in the drill-down detail panel. Controllers are the ones who verify mappings are working.
- **Mapping config UI** — both side by side. That's the whole point of that screen.
- **Audit / export view** — both. External accountants and auditors want to see the GL account.

**Why this matters**: when something posts wrong in Odoo, the first question is always "what category did this come from, and what did that category map to *on the day it posted*?" Having that adjacent in the controller view turns investigation from a 10-minute job into a 5-second one. Combined with mapping versioning, the audit story basically writes itself.

**Edit affordances per role**: clerks can edit the category only. Controllers can edit category OR the mapping itself — but doing one shouldn't silently override the other. The UI must make clear which action is being taken (fix this single transaction's category vs. fix the rule for all transactions like it).

### 2. Invoice Processing & AP Automation
**What**: Vendor invoices arrive via email/WhatsApp/upload. Tesote OCRs + AI-extracts vendor, line items, amounts, taxes. Matches vendor against `res.partner` from Odoo, line items against open POs (if Purchases module is in use), tax against `account.tax`. Drafts an `account.move` of type `in_invoice`. One-click post to Odoo.

**Why this is #2**: AP is the second-biggest time sink for clerks and the most error-prone. Also a strong wedge — clients can adopt this even if they don't yet trust auto-coding.

### 3. Bank Reconciliation Engine
**What**: Each bank line is auto-matched against open Odoo journal entries using amount, date, counterparty, reference. High-confidence matches presented for one-click confirmation. Reconciliation gets posted to Odoo. Unmatched items trigger queues for investigation.

**Why this is #3**: reconciliation is the close-blocker. It's also where Tesote's bank-data ownership gives us an unfair advantage — we have cleaner bank data than Odoo would on its own.

### 4. Automated Accruals & Month-End Close — *post-v1*
**What**: Tesote identifies accrual candidates (recurring expenses not yet booked, deferred revenue, prepaids amortizing). Drafts journal entries with AI-suggested amounts based on history. Posts on approval with auto-reversal scheduled. A close checklist tracks every step (sub-ledger close, bank rec done, accruals booked, FX revaluation, GL close).

**Why this is #4 but post-v1**: month-end close is the single most stressful event in any finance team's month. Compressing close from 10 days to 3 is a CFO-level value prop. But it depends on #1–#3 being mature first — accruals on top of unreliable coding is a mess. Ship after v1 stabilizes.

### 5. Counterparty Management & Mapping
**What**: Counterparties are Tesote-native (already built today). New counterparties get created in Tesote on the fly — first time one is referenced in a posted transaction, Tesote auto-creates or attaches to the matching `res.partner`(s) in Odoo per the mapping config. Duplicate detection across name/RIF/CI in Tesote (one cleanup point, not two). Customer AR aging and vendor spend analysis live in Tesote, computed from the operational ledger.

**Why this is #5**: not a wedge on its own, but the foundation that makes #1 and #2 trustworthy. Bad counterparty data → bad coding suggestions, broken reconciliation, audit problems. Building counterparty hygiene into Tesote (not Odoo) means it's solved once across all clients instead of per-client-per-Odoo-instance.

**Mapping work**: this is also where the per-client counterparty mapping config gets surfaced and edited. Controllers can review/override mappings and resolve conflicts when the same business entity has multiple `res.partner` records in Odoo.

### 6. Intelligent Reporting & Alerts — *post-v1*
**What**: Plain-language queries against Odoo data ("show me COGS by branch for Q1"). Anomaly alerts (vendor spend up 40% MoM, unusual journal entry posted, missing invoices). GL trend visualizations. LATAM-formatted exports (Libro Mayor, Diario, etc.).

**Why this is #6 but post-v1**: the analytics layer makes the cockpit sticky for CFOs/analysts, but it depends on the underlying data being clean — which #1–#5 provide. Build after v1 has a stable operational ledger to query.

### 7. Approval Workflows & Role-Based Access — *post-v1*
**What**: Configurable approval thresholds (clerk can post up to X, controller up to Y, CFO above Z). Role-based permissions across all the above. Full audit trail of who proposed, who approved, who posted, what AI suggested. WhatsApp/email notifications for pending approvals.

**Why this is #7 but post-v1**: critical for enterprise readiness but not a v1 wedge. Smaller clients live without it; bigger clients require it. Add when we go upmarket past the v1 ICP.

## Automation philosophy: Assisted → Automated

Three operating modes. Every capability above moves through them in sequence.

1. **Assist** — AI suggests, human always approves. Builds trust, generates training data. Default starting state for any new client/account.
2. **Auto-with-review** — AI auto-applies, human reviews after the fact (daily/weekly digest). For routine, low-risk transactions where the model has earned confidence.
3. **Autonomous** — AI handles end-to-end, exceptions only escalate. Reserved for high-volume, low-variance, low-stakes flows (e.g. recurring SaaS bills coded to a single account).

**Configurable per client, per account, per transaction type.** Conservative clients can stay in mode 1 forever. Aggressive clients can graduate quickly.

This is also our defensibility: every approval is training data. The longer a client uses us, the better our model gets at *their specific* chart of accounts, vendor list, and conventions. Switching cost compounds.

## From signup to cockpit: the productized onboarding flow

The onboarding flow IS the product. If we can't get a new client from "signed contract" to "AI is coding their daily transactions" in 30 days, the cockpit narrative is broken. This section is the operational playbook for making that promise repeatable across clients — not a custom project every time.

### The 30-day promise

By end of day 30 with an engaged client, they have:

- ✅ Odoo connected, full read-pull complete
- ✅ Banks connected via Connect, 90 days of history pulled
- ✅ Tesote category taxonomy live, mapped to their Odoo CoA
- ✅ Counterparties cleaned, deduped, mapped to `res.partner`
- ✅ Auto-rules library seeded from historical data, reviewed by controller
- ✅ AI Transaction Coding running on daily bank flow (assist mode)
- ✅ Bank Reconciliation Engine running on daily bank flow
- ✅ AP Automation inbox live, processing forwarded invoices
- ✅ Controller doing daily work in Tesote, not in Odoo

**30 days is the SLA we sell against.** Anything longer is implementation cost we eat. Anything we ask the customer to do beyond what's listed below is wasted relationship capital.

### Roles in the flow

- **Customer Controller** — the decision-maker. Makes the calls that only they can make (which categories, which mappings, which counterparties are duplicates).
- **Customer AP/AR clerk(s)** — joins in Stage 5+. Daily users of the queue and AP inbox.
- **Tesote CS** — the driver. Owns the 30-day clock. Does everything *not* on the Controller's plate.
- **Tesote product (the cockpit itself)** — does the automated work: pulls, dedups, suggests, syncs.

The split matters: **CS drives, customer decides, product executes.** If CS is making decisions, we're not productized. If the customer is doing work the product could do, we're not productized either.

### The journey (stage by stage)

#### Stage 0 — Pre-flight (Day -7 to Day 0)
**Who**: Sales → CS handoff
**What happens**:
- Signed contract + pricing tier locked
- Discovery: Odoo version (must be 17/18/19), modules in use (Accounting required; Purchases/Inventory/Sales noted as nice-to-have), bank list, finance team size, monthly transaction volume, pain points
- Pilot scope agreed: which entities, which banks, which capabilities go live first
- Customer designates a Controller point person and an AP clerk

**Customer effort**: 1 discovery call, 1 hour.
**Productization assets needed**: pre-call questionnaire (auto-filled with whatever we know from Connect), CS kickoff template.

#### Stage 1 — Connect Odoo (Day 0–1)
**Who**: Customer IT/Controller, guided by Tesote CS
**What happens**:
- Customer installs the Tesote Odoo module (already on apps.odoo.com — `tesote_connector`)
- API credentials provisioned in Odoo; entered into Tesote admin via the Setup Wizard
- Connection validated end-to-end
- **Initial pull**: chart of accounts, all `res.partner` records, journal entries from the last 90 days, bank statements, taxes, analytic accounts, products

**Customer effort**: 30 minutes, guided by CS on a screenshare.
**Productization assets needed**: Setup Wizard (exists today, needs hardening), connection-test diagnostics with clear error messages when Odoo permissions are misconfigured, automated initial-pull job with progress UI.

#### Stage 2 — Map the world (Day 1–5)
**Who**: Tesote CS (driver) + Controller (decision-maker)
**What happens** — four mapping decisions, in order:

1. **Category taxonomy** — Tesote presents a starter category tree based on the customer's industry. Controller accepts or customizes.
2. **Category → Account mapping** — For each Tesote category, pick the Odoo `account.account` it maps to. Tesote suggests based on CoA name matching; controller confirms. M:1 typical.
3. **Counterparty dedup** — Tesote runs duplicate detection on the pulled `res.partner` list (fuzzy name match + exact RIF/CI match + email signal). Controller reviews and resolves. **This is the messiest step.** Most clients have 30–40% duplicate counterparties in Odoo (every accountant has created "Movistar", "MOVISTAR C.A.", "Movistar Venezuela" as three separate partners).
4. **Counterparty consolidation** — Clean Tesote counterparties are created, each pointing to one or more `res.partner` records. Future txs reference the Tesote counterparty; Tesote handles the Odoo-side mapping invisibly.
5. **Tax + analytic mapping** — Usually defaults work. Only edit if customer has a non-standard setup.

**Customer effort**: 3–4 working sessions with CS, ~6 hours of controller time total.
**Productization assets needed**: vertical taxonomy templates (Retail, Services, Hospitality, Manufacturing — start with these four), AI-assisted mapping suggestions, counterparty dedup engine, mapping UI with versioning baked in.

#### Stage 3 — Connect banks (Day 3–7, parallel with Stage 2)
**Who**: Customer Controller/CFO, via existing Connect onboarding
**What happens**:
- Banks linked via Connect (existing product, no new flow needed)
- 90 days of historical bank transactions pulled
- Per-bank → per-Odoo-bank-account binding configured (which Tesote bank account feeds which Odoo `account.bank.statement`)

**Customer effort**: depends on how many banks. Connect handles the heavy lifting.
**Productization assets needed**: the per-bank-to-Odoo-account binding UI (new), the rest is Connect-as-is.

#### Stage 4 — Seed the auto-rules + AI training (Day 5–10)
**Who**: Tesote product (does the work) + Controller (reviews)
**What happens**:
- Tesote analyzes the 90 days of pulled bank transactions + 90 days of historical Odoo journal entries
- **Auto-rules suggestion engine** proposes a starter rule library — e.g. "txs with description containing 'NETFLIX' → category Software > Subscriptions, counterparty Netflix"
- Controller does a batch review — mostly approve, sometimes edit, occasionally reject
- AI model trains on whatever historical coding patterns existed in Odoo (if the customer was coding manually before, that's training data — it learns *their* conventions)

**Customer effort**: 1–2 hours of controller batch review.
**Productization assets needed**: rules-suggestion engine, batch-review UI, training-data pipeline.

#### Stage 5 — Soft launch: coding + recon live (Day 10–20)
**Who**: Controller + AP clerks + CS shadow
**What happens**:
- **Cap #1 (AI Transaction Coding)** turns on for daily bank flow in **assist mode**. Every transaction lands in the queue with AI-suggested Tesote category, counterparty, analytic tag, plus reasoning. Clerks approve, edit, or reject.
- **Cap #3 (Bank Reconciliation)** turns on. High-confidence auto-matches presented for one-click confirmation. Unmatched items queue for investigation.
- **Cap #5 (Counterparty management)** is implicitly live — when a transaction references a counterparty not yet in the system, clerks create it on the fly in Tesote; the system handles the Odoo `res.partner` side.
- CS sits in on the first 3–5 days of daily work, helps refine rules and mappings, surfaces edge cases.

**Customer effort**: daily work begins. Clerks spend ~1 hour/day in the queue (will drop as auto-pilot kicks in).
**Productization assets needed**: queue UI (Cap #1), recon UI (Cap #3), counterparty quick-create flow (Cap #5), in-app onboarding tooltips, "why did the AI suggest this?" explainability UI.

#### Stage 6 — AP automation live (Day 15–25)
**Who**: AP clerk(s) + Controller
**What happens**:
- AP inbox provisioned: a forwarding email address like `ap-{client}@tesote.com`
- Vendor invoices forwarded by email (suppliers send to a customer alias that auto-forwards); AP clerk uploads any non-email invoices via UI/WhatsApp
- OCR + AI extraction: vendor name, line items, amounts, taxes, due date
- Vendor matched against (now-clean) Tesote counterparty list
- Draft `account.move` `in_invoice` created, queued for clerk approval
- One-click post to Odoo

**Customer effort**: each AP clerk learns the inbox flow. ~30 min training. Then it replaces manual data entry.
**Productization assets needed**: email parsing pipeline, OCR vendor, extraction model, AP inbox UI, draft preview, post-to-Odoo confirmation flow.

#### Stage 7 — Steady state + first close (Day 20–30 and the first month-end)
**Who**: Controller + AP clerks + Tesote CS (weekly check-in initially)
**What happens**:
- All four v1 capabilities running daily
- First month-end close happens primarily in Tesote, with Odoo still open as a safety net
- **Trust calibration begins**: which category × counterparty combos have been approved without edit 10+ times? Those become candidates for auto-pilot.
- Weekly CS review: % auto-coded, % auto-reconciled, queue depth, time-to-close projection, customer satisfaction signals

**Customer effort**: normal finance work, but inside Tesote. Should feel *faster* than before by day 30, even though some manual review continues.
**Productization assets needed**: per-client health dashboard, CS weekly review template, first-close playbook.

#### Stage 8 — Graduation to auto-pilot (Month 2+)
**Who**: Controller (decides what graduates) + CS (advises)
**What happens**:
- Specific category × counterparty combos move Assist → Auto-with-review (AI posts, controller reviews daily digest)
- Highest-confidence flows (recurring SaaS, payroll, fixed monthly vendors) move to Autonomous
- Customer scope expands: more entities, more banks, more users, eventually post-v1 capabilities

**This is where the 80%+ north-star metric becomes real.** Until Stage 8, we're still at "AI assists humans." After Stage 8, we're at "humans handle exceptions while AI runs the books."

### Configuration moments — where the customer MUST decide

These are the only points where progress depends on customer input. Everything else is automated or CS-driven. Make each one fast and obvious:

| Stage | Decision | Time required |
|---|---|---|
| 0 | Pilot scope (entities, banks, caps) | 30 min in discovery |
| 2 | Approve/edit category taxonomy | 1 hour |
| 2 | Approve category → account mappings | 1–2 hours |
| 2 | Resolve counterparty duplicates | 2–3 hours (the messy one) |
| 4 | Approve starter auto-rules | 1–2 hours |
| 8 | Graduate flows to auto-pilot | ongoing, 15 min/week |

**Total customer time over the 30-day onboarding: ~15 hours of Controller attention.** Anything we ask beyond this is a productization failure.

### What we need to build to make this repeatable

The capabilities (Caps #1, #2, #3, #5) are the user-facing product. These are the *productization* investments that turn the capabilities into a repeatable 30-day onboarding instead of a custom project every time.

**Internal-facing (Tesote CS tools)**
- **CS onboarding console** — single pane showing every client's stage progression, with red/yellow/green per stage and CS interventions logged
- **Discovery questionnaire** — replaces ad-hoc kickoff calls; outputs a structured pilot scope
- **Vertical taxonomy templates** — Retail, Services, Hospitality, Manufacturing (start with these four; expand based on client mix)
- **Auto-rules suggestion engine** — runs on 90-day pull, proposes a starter rule library
- **Counterparty dedup engine** — fuzzy name + exact RIF/CI + email-signal matching

**Customer-facing**
- **Setup Wizard** (Odoo connection) — exists, needs hardening
- **Unified mapping UI** — category, counterparty, tax, analytic — all in one place, editable forever, versioned
- **Daily-work surfaces** — queue (Cap #1), recon (Cap #3), AP inbox (Cap #2), counterparty manager (Cap #5)
- **Role-aware visibility** — clerks see Tesote categories only; controllers can toggle a CoA column and see both in the transaction detail panel; auditors/exports always show both. Edit affordances scoped to role so clerks can't accidentally edit mappings.
- **Health dashboard** — % auto-coded, % auto-reconciled, queue depth, time-to-close trend, training progress

**SLA + process**
- **30-day implementation SLA** — published, sold against, measured
- **CS playbook** — checklist + decision tree per stage; same playbook used for every client
- **Health-check cadence** — weekly first month, biweekly second, monthly thereafter
- **Escalation paths** — when an onboarding falls behind schedule, what triggers a save

### Packaging implications

The onboarding flow naturally produces three packaging tiers:

- **Starter** — Caps #1 + #3 only (coding + recon). One entity, one bank. Lowest tier. Cheap way to test the cockpit thesis with a smaller client.
- **Pro** — Caps #1 + #2 + #3 + #5 (all of v1). One entity, multi-bank. The "real" cockpit — this is what we sell against.
- **Enterprise** — Pro + multi-entity + custom taxonomy work + priority CS + (later) the post-v1 capabilities. Sold as a managed service.

The differentiator across tiers is: **how many capabilities × how many entities × how much CS attention**. Pricing TBD (see Open Question #6), but the packaging axis is clear.

## Non-goals (v1)

- **We are not replacing Odoo.** Odoo stays as the system of record. We do not store the GL ourselves.
- **We are not building accounting software for non-Odoo customers.** The cockpit is Odoo-native in v1. (Future: same cockpit on top of SAP, Dynamics, Profit. But not v1.)
- **We are not handling tax filing.** Reports/exports yes; filing no.
- **We are not building a banking product inside Tesote** (that's Payments/Cobros). The cockpit consumes payment data; it doesn't initiate payments.
- **We are not doing payroll** (separate system, not worth bundling).
- **We are not building a self-serve product in v1.** This is sold + onboarded by Tesote ops/sales. Self-serve comes later if at all.

## Success metrics

**North star**: % of finance work that happens in Tesote vs. Odoo. Measured as % of journal entries originated/approved in Tesote ÷ total entries posted to Odoo. Target: 80%+ within 6 months of go-live for an active client.

**Tier 1 (product health)**
- Time-to-close (days from period end to books closed). Target: cut by 50% vs. pre-Tesote baseline.
- % transactions auto-coded with no human edit (proxy for AI quality). Target: 70%+ at maturity.
- Reconciliation rate (bank lines matched / total bank lines). Target: 95%+.

**Tier 2 (business)**
- ARR per client (pricing tier × seats). Target: minimum $X/mo per client (TBD).
- Net revenue retention. Target: 120%+ (expansion via more accounts, more seats, higher tiers).
- Client logo count for "cockpit tier" (Phase 3 capabilities). Target: TBD.

**Tier 3 (defensibility)**
- Volume of training data per client (# corrections logged, # approvals).
- Time from client onboarding → mode 2 graduation (faster = stronger product).

## Open questions (decisions needed)

These are the unresolved forks. Each blocks something.

1. **Self-service vs. managed-service** — does the client finance team operate the cockpit themselves, or does Tesote ops run it on their behalf? Current default seems to be managed-service. Long-term, self-serve is needed for scale, but it changes pricing, hiring, and product surface dramatically. **Decide before pricing.**

2. **Which Odoo modules do we depend on?** — Accounting confirmed for everyone. Inventory, Purchases, Sales, HR — varies by client. We need to spec what minimum module set the cockpit requires, what it gracefully degrades without.

3. **AI model strategy** — three options: (a) LLM API (Claude / GPT-4) for everything, (b) proprietary fine-tuned models for transaction coding + LLM for reasoning/explanations, (c) hybrid (LLM for cold start, proprietary for hot accounts). Affects margin, latency, defensibility. **Big decision, needs Dan + AI lead input.**

4. **Odoo credential management** — how do we securely hold and rotate API credentials per client? OAuth where supported, API keys otherwise? Self-hosted Odoo vs. Odoo.sh vs. Odoo Online — different models. **Security review needed before scaling.**

5. **Rollback** — if Tesote posts an incorrect entry, how do we reverse it cleanly without breaking Odoo's audit trail? Reversal entries vs. cancellation? What state can/can't be undone (e.g. once a period is closed)?

6. **Pricing model** — per seat? per transaction processed? % of finance work automated? Flat tiers? Bundled with Connect/Payments? **Strategic decision, depends on (1) above.**

7. **What's the relationship between this and the Notion "Managed Accounting Data Pipeline" framing?** — there's a parallel ERP-agnostic API spec that frames Tesote as sending JEs to ANY ERP. The cockpit framing is the opposite — Odoo-native, deep integration. Are these the same product with different surfaces, or two products? **Need to reconcile.**

8. **What do we do when the client uses Odoo features the cockpit doesn't yet support?** (e.g. they use Inventory, we don't surface inventory in the cockpit). Do we hide it, link out to Odoo, or build it?

## Risks

- **Odoo API rate limits / version drift** — Odoo 17/18/19 differ. Module customizations differ per client. Cockpit becomes brittle if not architected for this.
- **AI errors are catastrophic in accounting** — wrong account on a high-value entry → audit nightmare. The assisted→autonomous graduation curve must be conservative.
- **Client doesn't trust AI coding** — if approval rate stays at 60% forever, we never graduate to auto-pilot, value prop weakens. Need to measure trust progression and intervene.
- **Odoo itself moves up-market with AI features** — Odoo is shipping its own AI assistance. We need to be 10x better at the LATAM/finance-cockpit job than Odoo's generic assistant, or we get crushed. The bank-data-first wedge is our defense.
- **Sales motion** — selling "AI cockpit for your finance team" requires a different conversation than "ERP connector." Marketing, sales enablement, and demo flow all need to be rebuilt.
- **Build cost** — this is a 12–18 month roadmap, not a quarterly project. Need to think about what gets resourced when.

## What we're going to figure out next

In rough order:

1. **Reconcile the cockpit framing with the existing Notion API spec / Treasury plans / Linear projects.** Either the cockpit is the v2 framing of MDP, or they're separate products. Decide.
2. **Audit today's category + counterparty + auto-rules models** against the Ramp-style source-of-truth design above. Identify what needs to be rewritten vs. extended.
3. **Pick the pilot client for v1.** Casagri is already on the connector — natural candidate. Or El Dorado, where we have a deep integration spec already. Whoever it is becomes the test of the 30-day onboarding SLA.
4. **Spec the four v1 capabilities** (#1, #2, #3, #5) at engineering-shippable detail. One sub-PRD per capability.
5. **Spec the productization investments** (CS onboarding console, vertical taxonomy templates, dedup engine, unified mapping UI, health dashboard) — these are as important as the capabilities themselves.
6. **Pricing model decision** for Starter / Pro / Enterprise tiers.
7. **AI model strategy decision** with Dan + whoever owns AI.
8. **Build the cockpit UI prototype** — Figma at minimum. Words don't sell this; the experience does. The onboarding flow above is the script for the prototype.

---

## Appendix: existing material to fold in (next pass)

When I clean this up, pull from:

- **Notion**: Managed Accounting Data Pipeline API Spec, Managed Pipeline Ops, Strategic Necessity Memo, Data Pipeline SLA, Tesote ↔ Odoo Recon project (Grupo Oriand)
- **Treasury repo**: `docs/plans/odoo-journal-entries/`, `docs/plans/erp-accounting-integration/`, `app/clients/erp_client/odoo_client.rb`
- **Knowledge-base**: `product/erp-integrations/odoo/` (connector v0.3.6 reference, integration flow)
- **Linear**: Odoo Connector project, Odoo Phase 1 BASE Journal Entries project, Casagri (Odoo) project, PRO-32 MDP epic
- **luis-brain**: `sales/clients/el-dorado/integration-spec-odoo.md` (most detailed client-side spec)
- **People to talk to**: Daniel (eng lead on Odoo work), Andrés (Odoo kickoff), Sebastian (push architecture)
