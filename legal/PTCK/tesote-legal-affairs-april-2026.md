---
title: Tesote's Legal Affairs — April 2026
tags: [legal, compliance, 10x, payments, licensing, corporate]
updated: 2026-04-22
status: draft
---

# Tesote's Legal Affairs — April 2026

Master brief for the new legal team. The point of this doc: **outline everything, but make crystal clear what blocks product launches and what doesn't.** Product launches are the forcing function for Q2 2026 ([[../strategy/product-strategy-execution-plan]] — the 10x bet). Anything that doesn't gate a launch can sit in a slower lane if counsel prefers.

Priority buckets below. Within each bucket, items are roughly ordered by urgency.

- **P0 — Product-launch critical path.** Cannot go loud without these.
- **P1 — Next-wave products.** Not live yet, but scoping and legal posture need to start in parallel so we're not blocked in H2.
- **P2 — Corporate / strategic.** Real work, real money on the table, but *product launches should not wait on P2*. If counsel has bandwidth constraints, P2 slips before P0/P1.

See the [product strategy execution plan][psep] and its [master legal checklist][psep-legal] for the product-side framing — this doc is the counsel-facing version of the same work, re-sorted by priority and expanded with the corporate/org items that didn't belong there.

[psep]: ../strategy/product-strategy-execution-plan.md
[psep-legal]: ../strategy/product-strategy-execution-plan.md#legalcompliance--master-checklist

---

## P0 — Product-launch critical path

**These items gate the loud public launch of Payments + Business (network).** Until they're done, we sell quietly, customer-by-customer. That's fine for 4–8 weeks. Past that, it caps the 10x bet.

### P0.1 — Payments (Collect + Send) — launching now, loud by Q3

Currently operating under BNC's licenses. Works for quiet rollout. Will not hold up for a loud launch or when we expand beyond BNC.

- [ ] **BNC partnership agreement — scope review.** Does it cover: (a) onboarding BNC customers into a Tesote interface, (b) debiting their accounts via our branded payment link, (c) us marketing the combined product publicly, (d) Send flows (outbound) from BNC business accounts via their API?
- [ ] **BNC exclusivity question.** Is the partnership explicitly non-exclusive? Do we need written non-exclusivity before pitching Bank #2?
- [ ] **Sudeban posture memo.** Counsel's written view: is Tesote a regulated entity, a tech provider, or unclassified? Either "no registration required because X" or "we're pursuing Y, here's the timeline." This memo is the single most important deliverable of this engagement.
- [ ] **AML / KYC obligation allocation.** Confirm in writing with BNC that AML monitoring on each transaction is BNC's obligation (they hold KYB on the debited account). Tesote will still implement transaction pattern surveillance as best practice, but the *regulatory* obligation needs to sit clearly.
- [ ] **KYB sufficiency for payees.** We already have KYB on payees via the SaaS relationship. Confirm sufficient for Payments.
- [ ] **Fund-flow diagram (the auditable one-pager).** Money flows: payer's BNC account → BCV rails → payee's BNC account. **Tesote never custodies.** Produce the diagram, have counsel bless it. This is the slide we show in any regulatory conversation.
- [ ] **Customer TOS (payee-facing).** Tesote Payments–specific terms for customers using our link to collect.
- [ ] **Payer-facing OTP screen disclosures.** What the individual (and later, business) sees on the OTP screen. Must disclose who's debiting, from where, via what rail. Counsel to bless exact wording.
- [ ] **Privacy policy / LOPPCI compliance.** Data we capture from payers (phone, account identifiers, OTP attempts, device/IP metadata) — retention, processing posture, data processing agreement with BNC.
- [ ] **Marketing claims pre-clearance.** Before any public launch, counsel pre-clears the words we're allowed to use. We cannot call ourselves things we're not licensed to be called. "Powered by BNC" disclosures — required? Optional? What's the exact wording Sudeban would accept?
- [ ] **Multi-bank expansion template.** Generic partnership / data-processing / AML-allocation agreement we can put in front of Bank #2, #3, #4 without a redraft each time. Needed before we start pitching other banks.
- [ ] **Fraud / chargeback / dispute handling.** OTP-authenticated debits are generally final, but we should document dispute handling explicitly. What's our exposure if a payer claims non-authorization despite OTP?
- [ ] **Outage / incident communication policy.** If BNC goes down, 100% of our Payments volume goes with it. What are we obligated to communicate, to whom, by when?

### P0.2 — Tesote Connect (LIVE, part of core product)

Live bank connectivity across ~95% of Venezuelan banks. Already the foundation under every other product, now including Payments.

- [ ] **Data handling posture.** We pull bank data on behalf of customers. Confirm our legal basis (customer consent + bank TOS compliance) is bulletproof per bank. Is there exposure if any bank's TOS forbids programmatic access?
- [ ] **Customer TOS coverage for Connect.** Does our existing customer agreement actually cover what Connect does? Data access, storage, retention, customer's right to revoke.
- [ ] **LOPPCI / data protection** for bank-account-level data flowing through Tesote.
- [ ] **SLA / uptime language.** If Payments rides Connect, our SLAs become real. What commitments can we contractually make? What's our liability posture when Connect is degraded?
- [ ] **Any regulatory exposure from aggregating bank data** (open banking–adjacent posture in Venezuela). Does counsel see a path where Sudeban could reclassify this activity?

### P0.3 — Tesote Automations (LIVE, part of core product)

ERP-side automation, reconciliation, journal-entry push. The moat that makes Payments defensible.

- [ ] **Data handling posture.** We read + write customer ERP data. Confirm customer TOS covers scope, retention, audit log obligations.
- [ ] **ERP partner agreements.** Any vendor agreements with ERP providers (Odoo, SAP, Dynamics, etc.) — are we in compliance with their API terms, partner programs?
- [ ] **Accuracy / correctness liability.** If an Automation pushes a wrong journal entry and a customer's books are wrong, what's our liability ceiling? Should be limitation-of-liability language in TOS, needs review.
- [ ] **Audit trail sufficiency.** For any customer that gets audited (fiscal or otherwise), our audit log needs to hold up. Is there a standard we should be meeting?

### P0.4 — Tesote Business (network layer)

The payment link is the entry point to the network. Every counterparty that receives a link is a potential network user. Launches alongside (or shortly after) Payments. Legal posture should be ready when product is.

- [ ] **Payer/counterparty TOS.** Lightweight terms for a payer who lands on our portal after receiving a link. Not a SaaS customer, but they're using our surface — we need a TOS that covers them.
- [ ] **Data posture for counterparties** we've never onboarded directly. What data are we collecting from them, with what legal basis?
- [ ] **Network-data usage rights.** As the network grows, aggregate data becomes valuable. Our TOS should reserve appropriate rights to use aggregated/anonymized data (while being clean on privacy).

---

## P1 — Next-wave products (scope in parallel, don't block P0)

Not launching yet, but the legal posture needs shape before the product team gets too far in. Counsel can work these in parallel with P0 if bandwidth allows; otherwise, queue after P0.

### P1.1 — Tesote Capital

Capital is a 2027 product at earliest. We're not a lender, we're a marketplace. The legal posture determines whether that's actually viable in Venezuela.

- [ ] **Structural question: can we orchestrate capital matching without being classified as a lender, bank, or regulated financial intermediary?** This is the make-or-break question for the product. Answer shapes the entire design.
- [ ] **Licensing analysis.** If orchestration-only doesn't work, what license(s) would we need to operate Capital? See P2.4 for the VE licensing overview — Capital is a key driver of that analysis.
- [ ] **Partner agreements.** Template for capital partners (factoring cos, banks, family offices, DFIs). We need a template that's clean on: data-sharing with partners, our fee model, our liability as the orchestrator, exclusivity posture.
- [ ] **Data-use rights for underwriting.** Using Connect + Automations + Business data to feed Capital underwriting — what customer consent / TOS language do we need today so we're not re-papering later?
- [ ] **Cross-border considerations.** Any capital coming from outside Venezuela (DFIs, foreign family offices) — FX, remittance, anti-evasion exposure.

### P1.2 — AI layer

AI runs across the stack (power-user interface on top of Connect + Automations + Business). Not a separate product motion, but the legal posture is distinct and arguably under-thought.

- [ ] **Training-data posture.** Are we using customer data to train models? If so, does TOS cover that? (Default answer should probably be "no, we don't train on customer data" — confirm and bake into TOS.)
- [ ] **Third-party model provider agreements.** Whoever we use (Anthropic, OpenAI, etc.) — data flow agreements, what's sent to them, retention on their side, whether that's disclosed to our customers.
- [ ] **Output liability.** AI suggests a collection action / a journal entry / a customer-facing message. If it's wrong and a customer relies on it, what's our exposure? Limitation-of-liability language.
- [ ] **Regulatory posture on AI in financial services.** Nothing Venezuela-specific today, but scan for any Sudeban / BCV guidance that could affect AI-in-the-loop decisions. Stay ahead of this.
- [ ] **Privacy / LOPPCI extension.** AI processing of customer financial data — does our existing privacy posture cover it or do we need to update?

---

## P2 — Corporate / strategic (important, but can wait behind P0/P1)

**Explicit guidance to counsel: do NOT let P2 gate product launches.** These are meaningful items with real dollars attached, but if we slow-walk them another quarter while P0 ships, that's fine. If speeding them up *helps* product launches (e.g., a license that unlocks Capital), escalate that — but don't invent dependencies.

### P2.1 — Corporate structure: Delaware C-corp ↔ Venezuelan entity

Today's state: Delaware C-corp and a Venezuelan legal entity that are **not legally connected in any way.** Zero ownership relationship, zero IP assignment chain, zero service agreement. This is wrong and has been for a while.

- [ ] **Recommend a structure that connects the two entities.** Typical options: (a) VE entity becomes wholly-owned subsidiary of C-corp; (b) services agreement between independent entities (cost-plus, transfer-pricing compliant); (c) something else counsel recommends given VE/US tax treaty posture (or lack thereof).
- [ ] **IP ownership and assignment.** Who owns the IP today — the C-corp, the VE entity, both, neither? Get clean IP assignment chain from every contributor → the C-corp (or whichever entity holds IP in the target structure).
- [ ] **Revenue booking.** Where does Tesote revenue land today, where *should* it land under the new structure, what's the transition plan.
- [ ] **Investor/board implications.** Current cap table lives at C-corp level. Any restructure has to be clean for future rounds — counsel should flag landmines before they're landmines.
- [ ] **Timing.** What's the fastest clean restructure, what's the fully-optimized restructure, and what's the delta in cost/time? Pick based on fundraise timeline.

### P2.2 — Employment: Venezuelan team currently classified as contractors

Today's state: our VE team members are paid as **contractors of the Delaware C-corp.** This is likely wrong on multiple fronts (VE labor law, US tax classification, benefits obligations).

- [ ] **Risk assessment.** Exposure in VE (labor law reclassification, retroactive benefits) + exposure in US (contractor misclassification, 1099 issues, withholding).
- [ ] **Target state.** Should VE team members be employees of the VE entity (which then gets paid by the C-corp under a services agreement — ties into P2.1)? Or an employer-of-record solution? Or continue as contractors with tighter agreements? Counsel to recommend.
- [ ] **Transition plan.** If we restructure, do it cleanly — retroactive risk mitigation, new contracts, benefits setup. Sequence matters.
- [ ] **Equity / stock option plan.** C-corp has (or will have) an option plan. VE employees need a clean path to participate — tax-efficient on both sides. Counsel to advise on structure.

### P2.3 — Fiscal / tax strategy

Driven largely by P2.1 + P2.2 but worth being a first-class item.

- [ ] **Overall tax posture.** Where does Tesote's profit *actually* accrue today, where *should* it accrue given the business, and what's the clean structure to get there? (US ↔ VE, no treaty, crypto/FX considerations.)
- [ ] **VAT / IVA / VE-side indirect taxes.** Our SaaS revenue, Payments revenue, Capital revenue (future) — what's taxable where, at what rate, with what invoicing obligations (imprenta fiscal considerations — see P2.4).
- [ ] **Transfer pricing.** If C-corp ↔ VE entity is the chosen structure, the intercompany services agreement needs transfer-pricing-defensible economics.
- [ ] **Payments-specific tax question.** When we take a transaction fee on Payments, where does that fee book and what's the tax treatment? Worth confirming explicitly — Payments revenue could dwarf SaaS revenue.
- [ ] **Fundraising tax efficiency.** Whatever we restructure to, it should not create friction for the next raise.

### P2.4 — Venezuelan licensing strategy

Currently operating under BNC's licenses. Works for Payments-on-BNC-only-quietly. As we expand (multi-bank Payments, Capital, loud launch), the license question gets real.

**Lay out every viable option + its ROI for each product on the roadmap.** Counsel deliverable: a matrix — license × what it unlocks × cost × time × difficulty. From that, we pick.

Options to analyze (not exhaustive — counsel to add any we're missing):

- [ ] **PSP license** (payment service provider). What would this give us? Does it let us operate Payments independently of BNC's licenses? Does it let us custody funds? Cost / timeline / Sudeban relationship required.
- [ ] **Fintech license** (whatever the current Sudeban / SUDEFIN / BCV equivalent is). Broader scope, higher bar. Worth it?
- [ ] **Buying an "imprenta"** (imprenta digital authorized to issue electronic tax invoices / comprobantes fiscales, SENIAT-authorized). Utility: we'd own the invoice-issuance infrastructure instead of depending on third parties. Relevant for Tesote-the-product and potentially resellable to customers.
- [ ] **Casa de bolsa / brokerage license.** Relevant for Capital — does this unlock marketplace-style intermediation? Cost/barriers usually high; evaluate.
- [ ] **Operador cambiario / exchange operator license.** Relevant if we ever touch FX, stablecoin, or USD rails. Out of scope for Payments v1 but scope before we plan v2.
- [ ] **Existing-entity acquisitions.** Sometimes the fastest path is buying a company that already holds the license. Counsel to flag any active opportunities.
- [ ] **No-license alternatives.** For each product, is there a "ride another licensed entity" option (like our current BNC posture)? What are the trade-offs vs. getting our own license?

Deliverable from counsel: one matrix, one recommendation per product (Payments, Capital, Connect/Automations, AI), one ordering.

### P2.5 — Brand / name usage

Lowest urgency of the P2 items. Worth surfacing because it's in the same bucket of "things we should get right before we get big."

- [ ] **Trademark posture.** "Tesote" + product names (Connect, Automations, Payments, Business, Capital) — registered where, in which classes, with what enforcement posture. VE + US at minimum.
- [ ] **Brand-in-marketing compliance.** When we say "Tesote Payments" publicly, what disclosures are required (per P0.1)? This sits at the P0.1 / P2.5 intersection — if a disclosure is a hard launch blocker, it goes in P0.
- [ ] **Domain / handle squatting.** Not legal in a strict sense, but counsel often has a view. Defensive registrations.

---

## What we need from counsel — sequencing ask

1. **First, confirm the priority sort.** If counsel disagrees with anything above being P0 vs. P1 vs. P2, flag now.
2. **Start P0 immediately.** Especially the Sudeban posture memo (P0.1) and the BNC agreement review (P0.1) — those are on the critical path for Q2 Payments rollout.
3. **Scope P1 in parallel.** Deliverables can lag, but we need the scope-of-work defined so we're not scrambling in H2.
4. **P2.4 (licensing matrix)** is the P2 item most likely to be *pulled forward* into P0/P1 — if a license unlocks Capital or multi-bank Payments materially faster, we want to know before we over-commit to workarounds.
5. **P2.1 + P2.2 + P2.3** are a package. Scope together, plan together, execute together. Don't solve one without the others.

---

## Open questions / to discuss in kickoff

- Who specifically on the new legal team is our day-to-day point of contact for each bucket?
- Any items above where counsel thinks we're already too exposed and they want action *this week* regardless of priority sort?
- Anything in our current operations we *haven't* listed here that counsel would want us to know is a risk?
- Engagement model — hourly, monthly retainer, per-deliverable? Impacts how aggressively we load them up.
- Relationship with any existing outside counsel (US-side, VE-side) — who stays, who's replaced, who coordinates.

---

## Notes & links

- [[../strategy/product-strategy-execution-plan]] — product-side framing and the master legal checklist extracted from the product plan
- [[../strategy/caracas-trip-2026-04-26]] — if any of this work needs Caracas-side counsel meetings, fold into trip planning
- [[../drafts/bnc-ach-status]] — current state of the BNC biz-debit enablement push
