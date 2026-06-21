---
title: Ask a Dan — Arquitectura Fospuca
tags: [sales, fospuca, engineering, architecture, ask]
updated: 2026-04-27
author: Luis Pulgar
status: draftc

---

# Ask a Dan — Arquitectura Fospuca

## TL;DR

Fospuca is a logo we want — multi-municipal utility in VE, big footprint, two clear upsell vectors (Payments + Portal). Their integration ask is **non-standard for us**: custom Oficina Virtual + Sage as a reconciliation engine + Microsoft Dynamics GP as ERP. I need your read on architecture options, effort, and what compounds into the platform vs. what we'd be eating as a one-off.

## Why we should pursue this even though it's atypical

- **Logo + vertical anchor.** One of the biggest aseo-urbano operators in VE. Winning them is a wedge into the utilities / multi-municipal vertical, where we don't yet have a flagship account.
- **Upsell path 1 — Payments.** Their OV literally does payment intake from end-customers (clients self-report transfers, upload comprobantes). That's our Payments product territory. Once we're inside their stack, replacing the OV payment leg with Tesote Payments / Payment Link is a natural follow-on.
- **Upsell path 2 — Portal.** Longer-term, Tesote Portal could replace their entire OV. If we win the conciliation engagement, we're positioned to pitch the portal play later.
- **Possible reusable scaffolding.** Some of what we'd build (GP integration, multi-stream ingestion, reconciliation rules engine, manual-review UX) is plausibly reusable for future utility/municipal clients.

## What they have today

- **Intake.** Customers self-report payments in a custom **Oficina Virtual (OV)** — amount, date, bank ref, comprobante upload, distribution across proformas.
- **First-pass validation.** OV calls **Megasoft** to validate online, but only against **BNC + Banca Amiga**.
- **Online-validated stream.** Validated payments → txt `pagos en línea` → loaded manually into **GP** (their ERP is Microsoft Dynamics GP).
- **Unvalidated stream → Sage.** Everything else → separate txt → loaded into **Sage** (their reconciliation engine, not their ERP).
- **Bank extracts.** Tesorería downloads extracts manually and runs them through a homegrown **"convertidor"** to reach the format Sage expects.
- **Auto-match in Sage.** Sage matches on ref / date / amount / description.
- **Manual review in Sage.** What doesn't auto-match is reconciled by Tesorería/Cobros by hand, inside Sage.
- **Reconciled stream → GP.** Sage's reconciled output → txt → uploaded to GP. GP invoices and applies cobros.
- **Out of scope.** Caja / IGTF is carved out of the interface entirely.

(Full notes: [[fospuca-meeting-2026-04-20]])

## Architecture options I want your read on

### Option A — Sage replacement (full reconciliation play)
Tesote owns end-to-end: bank extract ingestion → reconciliation engine (rules + manual-review UX) → GP feed for both streams. Sage goes away.
- **Pros:** Highest value capture; cleanest end-state; positions us as the reconciliation layer for the next utility client.
- **Cons:** Highest scope. We'd need to replicate Sage's rule logic + a manual-review UI for Tesorería/Cobros. GP integration on us.

### Option B — Sage-alongside (narrow play)
Tesote replaces only the upstream piece: bank extracts download + the "convertidor" + initial auto-match. Sage stays for manual review and GP feed.
- **Pros:** Smaller scope, faster to quote, lower risk on first project.
- **Cons:** Lower contract value. Doesn't displace Sage. Weakens the upsell narrative.

### Option C — Full-stack vision (multi-phase)
Phase 1 = Option A. Phase 2 = replace OV payment intake with Tesote Payments. Phase 3 = replace OV entirely with Tesote Portal.
- **Pros:** Largest LTV, clearest expansion roadmap, makes Fospuca a flagship reference account.
- **Cons:** Sequencing risk. Phase 1 alone is already non-trivial.

**My instinct:** sign **A as the contract**, frame **C as the roadmap** to anchor the relationship. But I want your engineering read before committing.

## Specific questions for you

1. **GP integration.** Have we integrated with Microsoft Dynamics GP before? If not, what's the lift? Is it stable enough to support as a product capability or strictly a one-off?
2. **Reconciliation engine.** How much of what Sage does (rule-based match + manual-review UI) overlaps with what we already have or are building? Is this a real platform investment or pure custom code?
3. **Bank extracts ingestion.** Their "convertidor" handles the long tail of banks. Do we know which banks are involved? Any we don't already cover?
4. **IGTF / caja.** They carve out caja because of IGTF formatting. Anything in our stack that handles this, or do we leave it out of scope?
5. **Effort estimate.** Rough OOM on Option A vs. B — eng-weeks, not precise.
6. **Reusable vs. one-off.** What % of Option A do you think compounds into the platform, vs. what we'd be eating as custom? This is the call I most need your read on.
7. **Red flags.** Anything in the meeting notes that gives you pause before we re-quote?

## What I need from you

- Initial gut on options + effort — doesn't need to be precise.
- Flag which Fospuca-side follow-up to prioritize:
  - (a) intro to the Sage-side owner inside Fospuca (offered by Adriana), or
  - (b) Tesorería/Cobros demo of the manual conciliation step (offered by Carlos Canache).

## Strategic guardrail

I'm willing to take a one-off-shaped project here **if** the upsell to Payments + Portal is real and we have a credible path to it. If your read is that Option A is mostly custom code with little compounding, we fall back to Option B — keep the relationship, don't overcommit eng — and revisit the full-stack play later.
