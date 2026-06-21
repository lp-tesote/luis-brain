---
title: Winning vs. horizontal AI — the Harvey/Legora playbook for Tesote
tags: [product, ai, strategy, 10x, harvey, legora, automations]
updated: 2026-05-24
status: draft
---

# Winning vs. horizontal AI

> The strategic anchor for Tesote AI. What we're defending against (Claude/ChatGPT + a generic Odoo MCP), what the legal-AI category figured out before us (Harvey, Legora), and how that maps onto what we've already locked.

## The frame in one line

Harvey and Legora don't beat ChatGPT on model quality — they beat it on **the wiring around the model**. That's the same play for Tesote AI vs. a horizontal Claude/Odoo-MCP setup. The moat isn't the LLM. It's the verticalized substrate: data, workflows, citations, audit, multi-player, domain language.

## The threat we're defending against

Within 12–24 months, this stack will exist and be usable:

- Claude / ChatGPT / Gemini desktop apps with MCP support (Claude already has it)
- An official or third-party Odoo MCP exposing read/write to Odoo objects
- LATAM mid-market discovering it (the window in [[project_odoo_mcp_framing]] closes)

A controller in Caracas could in principle: install Claude desktop, connect Odoo MCP, ask "¿cuánto le debo a CANTV?" — done. No Tesote required.

This is the bear case. We need to know why we still win.

## Why we win — five structural reasons a generic Odoo MCP can't match

### 1. Odoo is one system; finance is N systems

A perfect Odoo MCP only sees Odoo. It doesn't see:

- BNC, Banesco, Bicentenario, Provincial, Mercantil bank rails (we own those via Connect)
- WhatsApp threads with clients ("pago el viernes")
- Email inbox (supplier invoices arriving as PDFs)
- Payment links (Polar-style cobros)
- The DR books, the US books, the cross-entity intercompany state
- The agent-state memory ("we already emailed this client twice this week")

Tesote is the **only layer that joins them** — that's the command-center thesis ([[project_tesote_command_center]]). The MCP architecture sees a node; we see the graph.

### 2. MCP exposes data; Tesote executes work

A read-mostly MCP is a query interface. The high-value finance work is *transactional*:

- Send a Banesco botón link to a client and tag it
- Debit via BNC with OTP, post the JE, attach the receipt
- Run a 3-touch cobranza campaign with memory of prior touches
- Move money intercompany VDT → TST with both sides booked

None of these are "ask Odoo for X." They're multi-step, multi-system, action-bearing. Tesote's pagos/cobros/connect rails are the action layer. MCP isn't.

### 3. Generic chat ≠ product

A CFO doesn't want "ask Odoo anything." They want **"show me what to chase this week"** — a button, not a prompt. The work we're doing is:

- Pre-baking the joins (Odoo + bank feed + counterparty enrichment + comprobantes pending)
- Pre-baking the prompts (gallery, starter workflows)
- Pre-baking the workflows (Automations: draft-approve queues, scheduled jobs)
- Pre-baking the bank dialects (BICENTENARIO=BDT, MI BANCO=R4, etc. — [[reference_ve_bank_naming]])

A blank prompt against Odoo MCP forces the user to be the integration engineer. We do that work for them.

### 4. LATAM/VE ontology isn't in Odoo's schema

The things that make finance work *in Venezuela* live in **our** data model, not Odoo's:

- BCV vs paralelo vs contractual FX rates ([[project_payments_10x_bet]] context)
- RIF logic + SENIAT validation
- Multi-jurisdiction (VE/DR/PA/US/Caribe) — Odoo MCP per-instance doesn't see the supra-entity view
- Bank-statement dialects and alias resolution (Banco Exterior, never "Bex" — [[feedback_banco_exterior_naming]])
- Comprobantes de retención state machine
- "Deducible-eligible" tagging tied to receipt OCR

None of this is generic-ERP knowledge. It's our ontology, accumulated by the product, the customers, and the team. A horizontal MCP can't replicate it without becoming us.

### 5. Audit, multi-tenant, role-gated action

Finance actions need:

- Audit trail (who fired what, on what input, with what outcome)
- Multi-tenant isolation (one workspace can't see another's data)
- Role-gated execution (AP clerk can draft, controller approves, CFO sees aggregate)
- Reversibility / dual control on hard-undo actions

Generic chat agents have none of this. We can build it because we own the surface.

> If Odoo MCP is git for accounting, Tesote AI is the IDE.

## What Harvey and Legora figured out — and we should steal

Both are verticalized-AI category winners (legal). The patterns are portable.

### Pattern 1 — Workflows, not chat

Harvey ships "Assistant" and discrete workflow products (due diligence review, contract redlining, legal research). Legora ships review modes and structured drafting flows. Neither leads with a blank chat box.

**The architectural rule we already locked** ([[ai-use-case-taxonomy]]): if a workflow can be specified deterministically, it does not belong in chat. It belongs in **Automations** — autopilot, draft-approve, or scheduled.

Today, ~70% of the `/ai` gallery is Automations work stuffed into chat because the Automations surface doesn't exist yet. That's the gap Harvey/Legora's pattern forces us to close.

**What this means:** Automations isn't a v2 — it's the *primary* surface for most of the 12 jobs. Chat is the *secondary* surface (ad-hoc questions + configuring Automations + judgment-driven work).

### Pattern 2 — The "do this to N things" primitive

Legora's killer UX: a spreadsheet/table view where you review 100 contracts on 12 dimensions in parallel. Each row is a doc, each column is a question, every cell is a grounded AI output.

Finance is **batch-natured**. Translating directly:

- Review N transactions on M categorization rules (drafts queue)
- Review N invoices on M validation dimensions (RIF, IVA, retención, deducible-eligible)
- Review N counterparties on M enrichment dimensions
- Review N card spends on M receipt-validity dimensions (legal name, RIF, amount match)

**Our drafts queue should be a Legora-style table, not a chat history.** Build the surface once, every job-with-draft-approve-mode plugs in.

### Pattern 3 — Source-grounded outputs (citations as moat)

Every Harvey answer cites the source doc. Every Legora row points back to the contract clause. Citations aren't UX polish — they ARE the trust mechanism that lets users accept AI work in high-stakes domains.

For finance, every AI output must cite:

- The bank statement line / transaction ID
- The Odoo journal entry / invoice / bill
- The email / PDF / mobile-capture source document
- The rule that fired (if Automations)
- The FX rate snapshot used

This maps directly to our **documentary evidence management** meta-pattern ([[ai-use-case-taxonomy]] §§ 3.a, 7.a, 7.b) — the per-txn "documents expected" model isn't just about SENIAT compliance, it's about *every AI output being grounded in a specific document we can point to*.

**Citations and doc-evidence are the same primitive.** Build it once, it underwrites both compliance ROI and trust UX.

### Pattern 4 — Speak like the user

Harvey speaks lawyer. Legora speaks lawyer. The product feels native because the vocabulary, the document types, the workflows all match how the user already thinks.

Tesote speaks **controller-in-VE**: cobranza, conciliación, comprobantes, libro de compras, retenciones, BCV vs paralelo, tres bancos. Audience is the whole **finanzas** function — not "tesorería" ([[project_tesote_ai_audience]]). Spanish is `tú`, Venezuelan, never `vos` ([[feedback_product_ui_spanish_venezuelan]]).

A horizontal chatbot can't speak this dialect natively. Even if you tell it to, it doesn't know which RIF format is valid, what a comprobante de retención is, why BICENTENARIO and BDT are the same bank. We do.

### Pattern 5 — Multi-player by default

Harvey isn't a personal copilot — it's the firm's AI layer. Multiple lawyers, paralegals, partners working on the same matter, with the AI as a shared participant.

Tesote AI should be the same: **CFO + controller + AP clerk + AI agent all working on the same object surfaces.** Not a personal assistant per user. The command-center architecture ([[project_tesote_command_center]]) already enforces this — every workflow is workspace-scoped, multi-user, role-gated.

### Pattern 6 — Land-and-expand via deep reference accounts

Harvey doesn't grow bottom-up. They land firm leadership (Allen & Overy, PwC), embed deeply, become the firm's AI layer, and let logos do the marketing.

For us:

- **Mariel = design partner #1** (already locked — [[project_tesote_command_center]] dogfood pattern)
- Need 2–3 more: ideally one mid-size LATAM client per major bank profile (Banesco-heavy, BNC-heavy, multi-bank)
- Don't chase shallow logos that don't deepen — Harvey's lesson is that depth at one account > breadth across ten

This also informs the rollout plan ([[../../marketing/tesote-ai-rollout-plan]]): Stage 1 warm-list pilot is *exactly* this pattern. Stage 2 mass rollout only earns its budget after Stage 1 produces 1–2 deep reference accounts.

### Pattern 7 — Narrow + deep beats broad + shallow

Both Harvey and Legora ship a *small number* of obsessive workflows. They don't try to be "AI for everything legal." They pick due-diligence, contract review, research — and own them ruthlessly.

We have 12 jobs in the taxonomy. We should ship 3–5 with Harvey-level depth, not all 12 at chat-level superficiality.

**The first flagship pick is already implied by the taxonomy:** the documentary-evidence triplet (3.a comprobantes-chase, 7.a gastos-deducibles, 7.b comprobantes-applied) — same infrastructure, three customer surfaces, sharpest ROI story (~37% of card spend in recovered tax credits).

After that, ranked by leverage:

1. **Doc-evidence triplet** (§§ 3.a, 7.a, 7.b) — shared infrastructure, clearest ROI
2. **Reconcile banks** (§ 4) — substrate that everything else depends on
3. **Cobranza sweep** (§ 3) — leverages bank rails we already own (Banesco botón, BNC), pairs with payments 10x bet
4. **Close the books** (§ 1) — the deadline workflow that wraps everything else
5. **Report up** (§ 10) — Luis is the customer; informs product before external sale

## How this changes what we're doing

### The rollout plan (Stage 1 video)

Current draft is 3 chat demos. Harvey/Legora would say at least one slot should be an **Automations moment** — show the user delegating, not just querying.

Proposed swap for one of the three demo moments:

> *"And while you slept, Tesote chased 14 receipts, marked 12 as deducible-eligible, and recovered $2,340 in tax credit you would have lost. Here's the pre-approval queue."*

That's the Harvey "Assistant" frame applied to finance. Speed-of-query is a feature; delegation is the product.

See [[../../marketing/tesote-ai-rollout-plan]] for current draft.

### The Automations surface is the gating roadmap unlock

Until Automations exists as a real surface (drafts queue, scheduled jobs, event log, rules list), we're shipping a chat product, not the Harvey/Legora play. Today, the gallery is the workaround.

Implication: the **first `/tesote-plan` priority** should be the Automations surface IA + the doc-evidence ingestion + queue infrastructure. Not another chat feature.

### The flagship pick

Doc-evidence triplet (§§ 3.a, 7.a, 7.b) — pair into one `/tesote-plan` run since they share infrastructure. Pull in `database-design` + `product-management` + `using-linear` per [[feedback_tesote_plan_workflow]].

### Reference accounts

After Mariel, identify 2 more design partners with non-overlapping bank profiles. Coordinate with `[[../../marketing/tesote-ai-rollout-plan]]` Stage 1 warm-list pilot — the pilot list is the candidate pool for the next reference accounts.

## What's NOT in the moat

For clarity — these are things we should *not* claim as our moat, even though they sound good:

- **The model.** Anthropic / OpenAI will keep improving; whatever advantage GPT-4-class models have, the horizontal stack has equal access.
- **The chat UX itself.** A clean chat window is table stakes. Harvey/Legora's chat UIs aren't the moat; the workflow products around them are.
- **"AI-native" as a slogan.** Every vendor will claim this in 2026. It's noise.
- **Speed of any individual query.** A fast answer is a feature, not a defense.

The moat is structural: the data layer, the action layer, the ontology, the audit, the multi-player surface, the workflow products. Stuff that takes years to build and gets stronger with every customer.

## Calibration note on Harvey + Legora

The patterns above are derived from public product material and category reporting, not insider access. Before locking these into investor narrative or org strategy, run a focused teardown: [[harvey-legora-teardown]] (stub — TODO). 30–60 min of looking at their current product pages, demo videos, and pricing should confirm or refine the seven patterns.

## Open questions

- **Where does the line sit between Tesote AI and the company's broader AI roadmap?** This doc focuses on the AI surface. The same logic should apply to Automations, but the framing slightly differs (Automations is the "Agents" layer in [[pitch-agents-plus-ai]]). Worth a follow-up doc that unifies them.
- **Should we make any of this public?** "How we win vs. horizontal AI" is a real narrative for investors and the team. Some of it (the doc-evidence flagship ROI math) is also a marketing asset. TBD on what stays internal vs. promotes to KB.
- **What's the timeline pressure?** [[project_odoo_mcp_framing]] says LATAM mid-market isn't AI-native *yet*. How long is "yet"? 6 months? 18? Drives urgency on Automations build.

## Next moves

1. **Sanity-check this frame against Harvey/Legora's current product** — stub [[harvey-legora-teardown]] into a real doc
2. **Update [[../../marketing/tesote-ai-rollout-plan]]** to swap one chat demo for an Automations moment
3. **Promote when ready** — this is investor + team-leadership reading; once Luis is comfortable, promote to KB as the AI strategic anchor
4. **`/tesote-plan` priority** — Automations surface IA + doc-evidence ingestion pipeline is the gating roadmap unlock

## Related

- [[ai-use-case-taxonomy]] — the 12-jobs × 4-modes map this frame plugs into
- [[positioning-the-finance-chief]] — the *why* (LATAM finance chief posture)
- [[pitch-agents-plus-ai]] — the two-layer customer narrative
- [[pitch-today]] — the operational pitch (next 2-week version)
- [[../../marketing/tesote-ai-rollout-plan]] — the GTM container
- [[project_odoo_mcp_framing]] — the strategic call: chatbot in Tesote UI, not external
- [[project_tesote_command_center]] — the architecture this all plugs into
- [[harvey-legora-teardown]] — the deeper look at their products (TODO)
