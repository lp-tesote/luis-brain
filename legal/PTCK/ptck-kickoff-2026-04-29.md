---
title: PTCK Legal Kickoff — 2026-04-29
tags: [legal, ptck, kickoff, payments, regulatory, corporate]
updated: 2026-05-04
status: draft
---

# PTCK Legal Kickoff — 2026-04-29

48-min discovery/scoping with PTCK, our new Venezuelan legal firm. Goal of this note: distill the meeting into action items, cross-reference the [master brief](../tesote-legal-affairs-april-2026.md), and capture what each side owes before the next round.

[Fireflies recording](https://app.fireflies.ai/view/01KQDD896TK5RW762G8QXW5YWJ).

## Attendees

- **Tesote**: Luis + one other co-founder/exec
- **PTCK**: 3 lawyers (one of them likely the senior partner driving structure/fiscal questions; another driving regulatory/fintech; a third on commercial/territoriality)

## PTCK's framing of priorities

PTCK reorganized our three-bucket priority list slightly:

1. **Corporate basics** — US ↔ VE entity relationship, societario, fiscal, IP. (Maps to my P2.1, P2.2, P2.3.)
2. **Connect / Automations** — current live data-extraction business. (Maps to my P0.2, P0.3.)
3. **Payments** — incoming launch. (Maps to my P0.1.)

Notable: PTCK collapsed the corporate items *up* in priority — they see them as foundational, not "later." They didn't disagree that product items are urgent; they want corporate basics treated as parallel-track-with-equal-urgency.

→ **My call: accept their framing.** The fact that the VE entity has zero connection to the C-corp is genuinely weird and they're right to flag it. But P0 product items still must not slip behind corporate work — corporate is parallel, not blocking.

## Key insights from PTCK

- **VE fintech regulation (Sudeban) is intentionally broad.** Drafted as a magnet to capture every financial-services-with-tech offering. **Flow of funds is not the only trigger.** Regulatory implications can attach even without custody — depends on how the product is structured. → My current "Tesote never custodies" defense (P0.1 fund-flow diagram) is necessary but not sufficient.
- **Data protection in VE is underdeveloped.** Constitutional article + one ruling. Far behind LATAM peers. *Good news for Tesote.* PTCK will still review our contract data-handling language, but the regulatory floor is low.
- **Domiciliación is BCV-regulated, not Sudeban fintech.** Different regulatory bucket than OTP-debit. *In principle* friendlier, but how we implement matters — bad design could pull it back into fintech scope.
- **OTP-debit is the gray zone** that needs the most regulatory work.
- **Alianza vs partner-tecnológico with BNC matters legally.** Signing a referral-fee or partnership contract with BNC could pull us *into* fintech classification (vs. our current "we are a tech provider to the customer; BNC has no commercial relationship with Tesote" posture). → This changes how I should think about the BNC-commission idea (see open questions below).
- **VE entity protagonismo is itself a regulatory risk vector.** The more visible/active the VE entity is, the more "territoriality" exposure → the more fintech regulation exposure. PTCK's instinct: keep the VE entity in a constrained role (e.g., agente de cobro) and run main operations through US/Panamá. **But** — we already have ~10 employees, an office, sales team, marketing, sponsorships in VE. The footprint is real. → Tension to resolve.
- **Licenses grant specific *atribuciones*, not blanket coverage.** Each product needs its own analysis on which atribuciones any given license unlocks. → Reinforces P2.4 (licensing matrix), but it needs to be product-by-product rigorous.
- **One regulatory supuesto under fintech regs is "prestación de servicios en materia de legitimación de capital"** — ML-services-prevention. PTCK flagged this as an example of how broadly the regs reach (no obvious connection to fintech, but it's in scope).

## Decisions / way-of-working

1. **Phase 1 deliverable from PTCK**: regulatory memo covering
   - Per-product regulatory analysis (Connect, Automations, Payments)
   - Commentary on data-handling language in current customer contracts
   - US ↔ VE entity relationship recommendation + fiscal angle (with possible Panamá holding option)
2. **Phase 2** (later, separate scope): full contract review — TOS, customer contracts, payer-facing terms, OTP screen wording.
3. **Future / separate**: labor advisory with **Enrique Castillo** (PTCK labor partner, plugged into Fede Cámara's labor-reform working group). VE labor reform incoming → preempt.
4. **Working artifact = the *flujograma*.** PTCK wants a detailed flow diagram per product: who does what, what message goes where, what data flows, what the user sees at each step. They use the diagram to pattern-match against regulatory triggers. They explicitly said clients sometimes discover their own product is structured differently than they thought once they actually draw it. They keep these flujogramas + memos as a long-term reference; clients dust them off years later.
5. **Anticipo**: I pay the retainer per the proposal they sent. Tactical question they raised: do I want a *factura formal* (with IVA) or not? No factura saves cost; factura preserves the deduction.

## What I owe PTCK (next deliverables)

- [ ] **Flujograma — Connect** (data extraction): customer onboarding → credential capture → consult-only user creation → encrypted storage → robotic extraction → DB delivery. Include: BNC API path vs. portal-scraping path, ERP read paths.
- [ ] **Flujograma — Automations** (ERP read/write): which actions Tesote takes inside customer ERP, with what authorization, what logs.
- [ ] **Flujograma — Payments**: Collect via OTP and via domiciliación, end-to-end. Include the second-layer approval pattern (we hold the debit until our portal confirms even if domiciliación is pre-authorized at the bank). Send flow can come in v2.
- [ ] All current customer contracts / TOS for them to review the data-handling language.
- [ ] **Pay the anticipo** + decide factura formal yes/no.
- [ ] **Confirm trademark filing entity.** I told them VE entity, but I wasn't sure — confirm with whoever filed (likely Majo or external IP counsel).

## What PTCK owes me (Phase 1 memo)

- Per-product regulatory analysis (Connect, Automations, Payments) — green / yellow / red with reasoning
- US/VE structure recommendation + fiscal commentary (Panamá holding option to be explored)
- Risk/red-flag list per product
- → I should explicitly ask for: a per-product matrix of regulation-trigger × license-needed-if-any × workarounds. Otherwise the licensing question (P2.4) doesn't get a structured answer.

## Open strategic questions I need to answer before sending flujogramas

- **VE entity protagonismo.** Do I want VE to grow into a real subsidiary (with all the regulatory exposure that brings), or do I want to consolidate operations at the US/Panamá level and keep VE small (agente de cobro)? My instinct: I want VE to be real — that's where the team lives, where the brand operates, where customer trust accrues, and we're already loud (Startup Summit, ODY, Innovation Forum). But PTCK's territoriality argument could materially change the risk picture. → **Decision pending; impacts the corporate-structure recommendation directly. Worth a longer think before I respond to PTCK.**
- **BNC commission/alianza.** Should I keep pursuing the idea of a kickback/commission from BNC for the volume we drive? PTCK's framing suggests **no** — a formal alianza could pull us into fintech classification. → **Default: drop the commission idea, stay strictly partner-tecnológico, until counsel confirms a safe structure.** Confirm in Phase 1 memo.
- **Factura formal yes/no on the anticipo.** Small but recurring decision. Probably yes for deductibility. → Confirm with finance and tell PTCK.

## Cross-references

- [Master brief: tesote-legal-affairs-april-2026.md](../tesote-legal-affairs-april-2026.md) — what we sent PTCK
- [ES version: tesote-asuntos-legales-abril-2026.md](../tesote-asuntos-legales-abril-2026.md)
- [KYC customer-collection design: kyc-customer-collection-design.md](../kyc-customer-collection-design.md) — PTCK-delivered KYC docs (or prior counsel, confirm) re-organized for customer-facing collection
- [[../strategy/product-strategy-execution-plan]] — the underlying 10x plan PTCK's work supports
- [[../drafts/bnc-ach-status]] — operational status of the BNC payments push that PTCK now needs to bless

## Next concrete action for me

Three flujogramas to draft. Suggest starting with **Payments** (highest stakes, most regulatory ambiguity, and the one PTCK is best positioned to add value on). Connect + Automations flujogramas can borrow heavily from existing internal docs.
