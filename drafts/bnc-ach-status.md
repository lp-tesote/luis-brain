---
title: BNC Debit Rail Status
tags: [bnc, payments, debito-directo, bank-connectivity, draft]
updated: 2026-04-19
status: draft
---

# BNC Debit Rail Status

Working doc for where BNC's biz-account OTP-authorized debit stands. Feeds Track B.1 of [[../strategy/product-strategy-execution-plan#12-rollout-plan--the-three-parallel-tracks]].

## Why this matters

BNC-side biz-account debit enablement is the unlock for Tesote Payments going biz-to-biz — which is where the real B2B commerce volume lives (food, ag, pharma, distribution). The individual-payer leg is already live; the biz-payer leg is blocked at the bank level, not at BCV.

Earlier framing for this doc called it "ACH pull." That was a narrower lens. The real category is **BCV rail OTP-authorized debit**, which includes the individual flow that is already live. Renamed accordingly.

## Current state (as of 2026-04-19)

### Confirmed
- **BCV rails work point blank.** Julian (BNC tech) confirmed the rail itself is not the blocker.
- **Individual-account debit via OTP works end-to-end in production.** Tesote has tested this with a live payer.
- **Bank-level enablement is the gating factor** for biz accounts. Analogous to Pago Móvil's history: individual-only at launch, then banks independently enabled biz accounts. Expect the same arc here.
- **BNC has a defined requirement for biz enablement:** each business must go through a process to select which phone number will receive the OTP and authorize the debit.

### Pending (BNC-side)
- BNC's biz-account OTP flow is not yet enabled. Tesote is actively pushing for it.
- Design open question: how to support **businesses that require multi-signatory approvals** (e.g., 2 people needed to release a transfer). The OTP flow must mimic existing internal permissioning or finance/compliance teams will not approve it. This is a product requirement, not a nice-to-have.

### Unknown (other banks)
- Which other Venezuelan banks have enabled biz-account OTP debit.
- Whether Tesote needs to carry the narrative bank-by-bank, or whether other banks are already moving on their own.
- Per-bank enablement path, tech contacts, agreement structure.

## Rollout posture

- **Now:** fully exploit BNC individual-payer debit (live, no blockers) — see Track A in the [[../strategy/product-strategy-execution-plan]].
- **In parallel:** keep pushing BNC to turn on biz-payer debit. Deliver a product design that handles multi-sig biz permissioning so when it flips on, we're not blocked on UX.
- **Next:** build the other-banks matrix and the bank-facing pitch deck. Treat bank #2 as the proof point that this is a multi-bank network, not a BNC-exclusive feature.

## Key contacts

- **Julian** — second-in-command on BNC's tech team. Primary escalation for biz-account enablement.

## Open questions

- [ ] Is BNC's current license/partnership agreement with Tesote sufficient to cover biz-account debit once BNC flips the switch, or do we need an amendment?
- [ ] What do other banks currently support for biz-account OTP debit? (Discovery before pitching.)
- [ ] Who on our side owns the bank-facing pitch deck and 1-pager?
- [ ] Does BNC expect us to be BNC-exclusive during the initial rollout period, or is multi-bank expansion understood to be the plan?
- [ ] How does biz OTP multi-sig work on BNC's side — does their rail support multiple OTP requests tied to one transaction, or do we need to sequence them at the Tesote application layer?

## Assignment decision

This doc stays in `drafts/` while the state is this fluid. Once Track B.1 lands (BNC enables biz debit in production), promote:
- The biz OTP multi-sig design → `product/` as a real spec.
- The bank-pitch narrative → `sales/` or `marketing/` depending on who owns it.
- The legal/compliance output → the master checklist in `strategy/product-strategy-execution-plan.md`.
