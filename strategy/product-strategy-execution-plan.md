---
title: Product Strategy — Execution Plan (2026)
tags: [strategy, 10x, payments, product, legal, compliance]
updated: 2026-04-19
status: draft
---

# Product Strategy — Execution Plan (2026)

Companion to the [vision memo](https://www.notion.so/tesote/vision-memo-tesote3-v2-3411ee04eee1809dbfc4e702f624332f). The vision memo says *what* and *why*. This doc says *how, in what order, under what constraints, with what fallbacks.*

Raw working doc. Will be refactored and promoted to the KB once the plan stabilizes.

---

## TL;DR

- **Payments is the 10x bet and it ships first.** Everything else in this doc waits behind it. Customers move billions USD$/month today on our SaaS — we expect Payments revenue to be multiples of SaaS revenue once volume ramps.
- **BNC has green-lit the product and we're live in prod.** The B2C-facing leg of Payments is already running (BNC debit via OTP to individual accounts, tested end-to-end), and BNC-side send-payments is available via API. Onboarding gate is small: BNC docs + BNC prod API access.
- **Next iteration is ICP work, not product work.** The filter for Track A/C inside our existing customer base: *must have an active BNC account* — but not necessarily using BNC as their primary receivables bank. That broadens the pool meaningfully; it's everyone who has any BNC relationship at all, not just BNC-primary customers.
- **The B2B-facing leg is blocked at the bank level, not at BCV.** BNC's tech team (Julian) confirmed the rails work point blank period — the gap is per-bank enablement of biz-account OTP debit. Pago Móvil followed the same path (individual → biz, bank-driven). We ride that wave.
- **Parallel workstream: BNC send payments** via BNC's APIs. Tesote becomes the UX layer for outbound payments from BNC business accounts, tied to recon + ERP push. This is where the moat compounds.
- **We are currently operating under BNC's licenses.** That carries us through quiet rollout but is not sufficient for the loud public launch. Legal/compliance work is on the critical path for marketing, not just for product.
- **Sequencing:** Payments (Q2 2026) → deepen Connect + Automations attach (Q2–Q3) → Business network layer (Q3–Q4) → Capital + AI (H2 2026 and beyond).

---

## Cross-cutting: Regulatory & Legal Posture

Before product-by-product, the question that dominates everything: *what is Tesote, regulatorily?*

### Working assumption (today)

Tesote operates as a **technology provider** riding on BNC's banking licenses. Money never sits on a Tesote balance sheet. We orchestrate the transaction (link, OTP flow, status, recon) but the rail, settlement, and regulatory obligations are BNC's.

This is fine for quiet rollout. It is not fine for a loud public launch — and almost certainly not fine when we expand beyond BNC.

### Open questions (get counsel on)

- [ ] Does BNC's license agreement with Tesote explicitly cover: (a) onboarding BNC customers to a Tesote interface, (b) debiting their accounts via our branded payment link, (c) us marketing the combined product publicly?
- [ ] Sudeban's posture: does Sudeban view Tesote as a regulated entity, a tech provider, or unclassified? Is there a registration we should pursue *proactively* before it's demanded *reactively*?
- [ ] AML/KYC: who owns the obligation on each transaction — BNC (who has KYB on the debited account) or Tesote (who has the commercial relationship with the payee)? Probably BNC, but it needs to be in writing.
- [ ] LOPPCI / data protection: customer financial data flowing through Tesote. What's the data processing agreement structure with BNC? With each partner bank once we expand?
- [ ] Anti-evasion / foreign exchange: none of the current flows touch FX, but any future crypto/stablecoin/USD rail will. Scope that separately before launch.
- [ ] "Tesote the brand" in comms: when we go loud, what disclosures are required? "Powered by BNC"? A Sudeban disclaimer?
- [ ] Multi-bank future: when we turn on bank #2, does Tesote need its own payment-processor-equivalent registration, or do we stack additional per-bank agreements?

### What must be true before we go loud

1. Written confirmation from BNC legal that our current product falls inside our agreement.
2. Customer-facing TOS + privacy policy reviewed by counsel, live on the product.
3. Data processing / AML responsibility allocation documented between Tesote and BNC.
4. Clear answer on Sudeban registration posture — either "not required, here's why" in writing, or a registration in motion.
5. Marketing claims pre-cleared with counsel (we cannot call ourselves things we are not licensed to be called).

Until 1–5 are done, every growth channel works *word-of-mouth* but not *loud*. That's fine for 4–8 weeks. Past that it bottlenecks the 10x bet.

---

## Product 1: Payments — PRIORITY

Two product surfaces, one rail layer.

- **Collect (pull):** payment request link → OTP → debit from payer's account → settle to payee. Today works for individual payer accounts end-to-end on BNC.
- **Send (push):** Tesote as the UX surface for outbound payments from a BNC business account. BNC's API supports it. Not yet productized.

### 1.1 State today

| Surface | Rail | Payer side | Status |
|---|---|---|---|
| Collect | BCV rails via BNC | Individual account | **LIVE in prod**, tested end-to-end |
| Collect | BCV rails via BNC | Business account | **Blocked** — BNC needs to enable biz OTP flow |
| Collect | BCV rails via other banks | Individual or biz | **Unknown** — need to learn which banks have enabled what |
| Send | BNC API | Business account (outbound) | **Available but not productized** — BNC APIs support it |

### 1.2 Rollout plan — the three parallel tracks

**Track A — Collect from individuals (ship now).**
- Who: Tesote customers whose customers are individuals (any retail-flavored B2B2C: subscription services, memberships, education, health, consumer services, etc.).
- **ICP filter (hard requirement):** the Tesote customer has an **active BNC account**. They do **not** need to use BNC as their primary receivables bank — just any active BNC account where collected funds can land. This expands the candidate list well beyond our BNC-primary customers.
- Onboarding: BNC docs + BNC prod API access per customer. Simple.
- KPI: payment volume ($) per week, number of active payee customers, number of unique payers per payee.
- Target: onboard [N] customers in the first 30 days post-plan-approval. (Number to commit once we agree on the ICP list.)
- Marketing: *quiet* — customer-by-customer, human-to-human, CS-led. Not public yet. See [[#cross-cutting-regulatory--legal-posture]] for why.

**Track B — Unblock Collect from business accounts (push BNC + map the other banks).**

This is the bigger prize. Two parallel sub-tracks:

- **B.1 — BNC biz-account enablement.** Push Julian and his team to stand up biz OTP flow on BNC's side. Product design constraint: **the OTP authorization workflow must mimic the business's existing internal permissioning** (e.g., if the business requires 2 signatories to release a wire today, the OTP flow must require 2 approvals too). Without this, finance teams won't trust it and compliance teams will block it.
- **B.2 — Other-bank discovery & enablement.** We don't yet know which other banks have enabled biz OTP debit. First step is discovery, not pitching. Build a matrix: Bank × rail status × enablement path × contact. Then pitch bank-by-bank where needed.

See [[#15-bank-strategy--unblock-biz-collect]] for the pitch plan.

**Track C — Send from BNC business accounts (productize the API).**
- BNC's API allows outbound payments. Tesote becomes the best UX layer for them.
- Value prop: *every outgoing payment auto-reconciles against the ERP because Connect + Automations is already wired in.* This is the moat — a bank's own app cannot do this because the bank doesn't have your ERP.
- **ICP filter (hard requirement):** the Tesote customer has an **active BNC account** (not necessarily their primary operating bank). Any BNC account balance they send from qualifies.
- Ideal ICP: Tesote customers who have an active BNC account AND are already Connect/Automations customers. Upsell to the existing book first.
- Secondary ICP: BNC business customers we don't have yet — *Tesote + BNC co-sell*.

### 1.3 Rail/infra feasibility — the key insight

BCV rails work. The question has never been "does the rail exist." It's "which bank has flipped which switch."

Julian's framing: *rails work point blank, enablement is at the bank level.* Pago Móvil's history is the proof point: individual-only at launch → banks added biz support → today it's just expected functionality. Biz OTP debit will likely follow the same arc. We should accelerate the arc, not wait for it.

**Implication for our bank strategy:** we are not asking banks to build something new. We are asking them to flip a switch they already have infrastructure for, with a product story they can show their own regulators and customers.

### 1.4 Bank strategy — unblock biz Collect

If we're the ones carrying the narrative to other banks (likely), we need a bank-facing pitch that is dead simple to digest. Rough structure:

1. **What it is:** BCV-standard OTP debit for business accounts, already live for individual accounts. Same rails, same security, biz UX adapted to biz permissioning.
2. **Proof:** Live on BNC (target). Transaction volumes, error rates, security posture, compliance attestations.
3. **What the bank gets:** (a) deposit stickiness — biz payees who settle into your bank's accounts, (b) fee revenue, (c) a modern product story for CFO customers who are tired of wire transfers, (d) zero build cost — Tesote is the UX layer.
4. **What the bank has to do:** enable biz OTP debit at the switch level + sign a Tesote partnership agreement.
5. **Timeline & risk:** what rollout looks like, what's piloted vs. production, what the compliance allocation looks like.

Deliverable: a ~10-slide bank pitch deck + a 1-pager. Owner: TBD (Luis + someone on marketing/partnerships). Draft target: end of April.

### 1.5 Legal/compliance framework — Payments

Below is the master list specifically for Payments. Cross-reference with [[#cross-cutting-regulatory--legal-posture]].

- [ ] **BNC partnership agreement review** — does it cover our current product and the rollout we're planning? Escalate ambiguities.
- [ ] **Customer TOS** — Tesote Payments–specific terms for payees using our link to collect.
- [ ] **Payer-facing disclosures** — what the individual (or business, later) sees on the OTP screen. Must disclose who's debiting, from where, via what rail. Counsel should bless the wording.
- [ ] **Privacy policy / LOPPCI** — data we capture from payers (phone, account identifiers, OTP attempts) and our retention + processing posture.
- [ ] **AML posture** — confirm in writing that AML monitoring on the underlying transaction is BNC's obligation. Tesote should still implement transaction pattern surveillance as a best practice.
- [ ] **KYB on payees** — we have this already through the SaaS relationship. Confirm sufficiency for the payment product.
- [ ] **Fund flow documentation** — produce the auditable diagram: money flows from payer's BNC account → payee's BNC account via BCV rails. Tesote never custodies. This is the single most important slide in any regulatory conversation.
- [ ] **Sudeban posture letter / memo** — counsel's written view of our regulatory status. Either "no registration required because X" or "we're pursuing Y."
- [ ] **Marketing claims review** — before any public launch, pre-clear the words we're allowed to use.
- [ ] **Multi-bank expansion template** — generic partnership / data / AML agreement that we can put in front of Bank #2, #3, #4 without a redraft each time.

### 1.6 Monetization

Two revenue lines from day one:

- **Transaction fee** on Collect (percentage or flat, TBD — model it before turning Track A loud).
- **Transaction fee or bundled SaaS uplift** on Send (tie it to the Automations/Connect product bundle).

Secondary, later: float economics if/when we custodize (probably never intentionally), capital marketplace spread (Capital product), data monetization (Business network graph).

Pricing exercise is not in this doc. Separate workstream: `finance/payments-pricing-model.md` (doesn't exist yet — create when we're ready to price Track A publicly).

### 1.7 Dependencies & product bundling

Payments is most valuable when sold *with* Connect + Automations, because that is what turns a payment into a reconciled ledger entry. The go-to-market pitch for any Payments customer — whether Collect or Send — should lead with: *"every transaction here auto-reconciles in your ERP."* This is the differentiator vs. the bank's own channels.

- **Connect** must be live for that customer (real-time bank data).
- **Automations** must be wired to their ERP (or at least their recon export).
- **Business** is not a prerequisite yet, but Payments-in-production is the prerequisite for Business.

### 1.8 Open questions / risks — Payments

- **Other banks' OTP status.** Unknown. Discovery first, pitch second. Owner: TBD.
- **Biz OTP UX design.** Multi-sig, multi-phone, role-based approvals. Needs a product spike — probably 1–2 weeks of design + validation with 3–5 reference customers.
- **BNC exclusivity vs. openness.** Does BNC expect us to be BNC-exclusive, or is multi-bank expansion in the spirit of the agreement? Must clarify before pitching Bank #2.
- **Fraud / chargeback model.** OTP-authenticated debits are generally final, but we should document dispute handling explicitly.
- **Concentration risk.** If BNC is our only rail for the first 12 months, any BNC outage = 100% of Tesote Payments down. Comms playbook for outages.
- **Pago Móvil analogue risk.** The "banks will follow" thesis is strong but not guaranteed. If only BNC enables biz debit, the TAM is capped at BNC's biz customer base until someone else moves. Worth modeling the pessimistic scenario.

### 1.9 Next actions — Payments (next 30 days)

Concrete enough to commit to. Dates are targets, not promises.

- [ ] **Week 1 (by 2026-04-26):** lock the Track A + Track C ICP list. Filter our existing book for: (a) active BNC account on file, regardless of whether BNC is their primary receivables bank, AND (b) for Track A, customers whose customers are individuals. Target 5–10 names to start onboarding.
- [ ] **Week 1:** draft the BNC legal review request — what clauses we need confirmed before we go loud.
- [ ] **Week 1–2:** draft the bank pitch deck + 1-pager (see §1.4). Land a v1 before the Caracas trip if possible — see [[caracas-trip-2026-04-26.md]].
- [ ] **Week 2–3:** biz OTP UX design spike — talk to 3–5 reference finance teams about their current multi-signatory flows, produce a wireframe that mimics them.
- [ ] **Week 2–4:** productize Track C (Send) — scope, eng estimate, pick 2–3 pilot customers from the existing book.
- [ ] **Week 3–4:** build the other-banks matrix — which banks, which rails, which contacts, which enablement path.
- [ ] **Week 3–4:** engage counsel on the legal/compliance checklist in §1.5. Parallel track, don't let it block Track A rollout.
- [ ] **Ongoing:** weekly payment volume reporting. From day one.

---

## Product 2: Connect — foundation, mostly built

*Stub — flesh out when Payments plan is locked.*

State today: live bank connectivity across ~95% of Venezuelan banks (per vision memo). Already the foundation under every other product.

Plan work needed:
- Inventory gaps vs. the remaining 5% of banks.
- Reliability / SLA posture — if Payments is going to ride Connect, what's the uptime commitment and how do we measure it?
- Pricing positioning as Payments arrives (Connect-alone vs. Connect-as-infrastructure-for-Payments).

**Need from Luis:** current state of Connect reliability metrics, known gaps, and whether any deprecation/refactor work is planned. Stub.

---

## Product 3: Automations — force multiplier for Payments

*Stub — flesh out once we know Payments attach motion.*

Key role in this plan: **every Payments transaction should push a clean journal entry to the ERP, automatically.** That is the moat vs. bank-native UX. Automations is what delivers that.

Plan work needed:
- ERP coverage matrix (Odoo, SAP, Dynamics, what's next).
- Reconciliation rule engine — current capabilities, what's needed for Payments-driven volume.
- Bundling with Payments — do we sell as one SKU or separate with a discount?

**Need from Luis:** current ERP support matrix, biggest gaps, and whether Automations has a backlog that Payments will expose. Stub.

---

## Product 4: Business — the network layer, follows Payments

*Stub — defer until Payments has meaningful volume.*

Strategic logic: the payment link is the entry point to the network. Every counterparty that receives a link is a potential user of the Business portal. We don't need to build the full Business product before Payments has enough link-traffic to seed the network.

Plan work needed:
- What the minimal "payer portal" looks like — the natural next step after "payer receives a link and pays."
- AR unified view vs. AP unified view — which side we build first. Probably AR (sellers are our customers).
- Network effects metrics — what does "network is working" look like in numbers.

**Need from Luis:** point of view on sellers-first vs. buyers-first and when we should start scoping this (after Payments hits what volume?). Stub.

---

## Product 5: Capital — data-driven, H2 2026 and beyond

*Stub — premature to plan in detail.*

Strategic logic: the data moat from Connect + Automations + Business is what makes Capital possible. Without it, we're just another factoring broker. Capital is a 2027 product at earliest.

Plan work needed:
- Capital-partner conversations (factoring cos, banks, family offices, DFIs) — discovery only, not committing to anything.
- Data product — what we'd expose to capital partners, with what privacy posture.
- Marketplace mechanics — how we avoid becoming a lender while still orchestrating the match.

**Need from Luis:** whether any investor/partner conversations in 2026 are expected to touch this. If so, we plan; if not, we defer. Stub.

---

## Product 6: AI — layer, not a product

*Stub — runs alongside everything.*

Strategic logic: AI is the power-user interface on top of the stack. It's a quality-of-product investment, not a separate product motion. Ship small slices as each underlying product comes online.

Plan work needed:
- First AI use case to ship. Candidate: natural language query over Connect + Automations data (already exists in stated vision). Tied to Payments: "which customers are paying late?" / "which invoices should I send a collection link to today?"
- Model choice, data posture, customer privacy.
- Pricing (included in base vs. premium tier).

**Need from Luis:** is there an AI feature that should ship *alongside* Payments to strengthen the Payments wedge? If yes, that pulls it onto the critical path. Stub.

---

## Legal/Compliance — Master Checklist

Consolidated from every section above. This is the list that gates the loud public launch.

### Entity & licensing
- [ ] BNC partnership agreement — scope review covering current Payments flows
- [ ] Sudeban posture memo from counsel
- [ ] Multi-bank expansion agreement template
- [ ] Determination on whether Tesote needs any proactive registration

### Customer-facing
- [ ] Tesote Payments TOS (payee-facing)
- [ ] Payer-facing OTP screen disclosures
- [ ] Privacy policy / LOPPCI compliance posture
- [ ] Marketing claims pre-clearance

### Operational
- [ ] AML obligation allocation, documented with BNC
- [ ] KYB sufficiency confirmation for payees
- [ ] Data processing agreements (Tesote ↔ BNC, future Tesote ↔ Bank N)
- [ ] Fund-flow diagram (the auditable one-pager)
- [ ] Outage / incident communication policy

### Expansion-ready
- [ ] Other-bank agreement template
- [ ] Cross-border / FX posture (for any future crypto/stablecoin/USD rails — out of scope for v1 but scope before the first conversation)

---

## Sequencing & milestones (rough)

| Horizon | Payments | Connect / Automations | Business | Capital | AI | Legal |
|---|---|---|---|---|---|---|
| Now – end of April | Track A live customers onboard; bank pitch deck v1 | — | — | — | — | Engage counsel, draft checklist items |
| May – June | Track A volume scale; Track B (BNC biz) push; Track C (Send) productize | Attach motion refined | — | — | — | TOS, disclosures, fund-flow doc |
| July – September | Multi-bank biz debit (Bank #2) | Reliability hardening | Start seller-side portal scoping | Partner discovery | First AI use case live | Clear path to loud launch |
| Q4 2026 | Loud public launch if legal cleared | Continued | Beta | Continued | Continued | — |
| 2027+ | — | — | GA | MVP | Mature | — |

This table is directional. Real milestones get tracked separately (Linear / OKRs), not in this doc.

---

## Open questions (for Luis)

Answer these and the plan sharpens up:

1. **Track A ICP list** — which 5–10 Tesote customers go first? Name them.
2. **Bank pitch ownership** — who drafts the pitch deck and the 1-pager? Marketing? Partnerships? You personally?
3. **BNC exclusivity** — is the partnership explicitly non-exclusive or do we need to ask?
4. **Caracas trip overlap** — should any BNC Payments conversation ride on the Caracas trip, or is that trip strictly about closing CAPCA?
5. **Counsel** — who's our Venezuela counsel on fintech/banking? Internal, or do we need to retain someone for this?
6. **Pricing authority** — who decides Payments pricing? You, or a committee?
7. **Launch-loud trigger** — is the gate purely legal/compliance, or also a volume threshold ("we don't go loud until $X/month")?

---

## Notes & links

- [Vision memo (Notion)](https://www.notion.so/tesote/vision-memo-tesote3-v2-3411ee04eee1809dbfc4e702f624332f)
- [[caracas-trip-2026-04-26]]
- [[../drafts/bnc-ach-status]] — related BNC enablement work
- BNC contact: Julian, second-in-command on BNC tech team
