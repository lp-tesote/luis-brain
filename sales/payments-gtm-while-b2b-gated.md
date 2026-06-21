---
title: Payments GTM While B2B Direct Debit Is Bank-Gated
tags: [sales, payments, 10x, strategy]
updated: 2026-04-19
status: draft
---

# Payments GTM While B2B Direct Debit Is Bank-Gated

Umbrella strategy for the Payments product while the B2B direct-debit (debito directo) leg is bank-gated. Frames the two-segment sales pivot and links to the segment-specific strategy docs.

Related: [[payments-10x-bet]] · [[bnc-ach-status]] · [[caracas-trip-2026-04-26]]

---

## Situation

- **Payments is the 10x bet for 2026.** The product has two legs: B2C collection (receiving from individuals) and B2B direct debit (pulling from business accounts).
- **The B2B direct-debit leg is partially bank-gated.** BNC business-account OTP debit (Track B.1) and related rails are still in activation with the banks. We cannot sell that product as a closed motion until the rails are live.
- **The B2C leg is live and ready to sell.** Payment Link for Individuals (inbound collection from cedula-holding payers) is available now.
- **The outbound-automation motion is also live.** Customers who already run high-volume outbound via BNC accounts are candidates for Tesote's outbound-payments / batch-payout orchestration — independent of the blocked direct-debit rail.

## Pivot

Sell what's live. Two customer segments, both derived from real Q1 2026 transaction data across Tesote's aggregated bank feeds:

### Segment 1 — Individual-payer collection (Payment Link)

Workspaces that **receive high volumes of individual payments** (from natural persons, not legal entities). Their pain is manual bank-description reconciliation — many banks don't show who paid.

- **Anchor ICP:** Venezuelan wholesale food/agro distributors.
- **Secondary clusters:** healthcare, insurance.
- **23 Tier 1+2 workspaces**, combined Q1 prize ≈ **$77M USD** (annualized ≈ $300M).
- **Archetype:** Grupo UP — 8,625 unique individual-payer cedulas, 100% bank visibility.
- **Single biggest single-workspace prize:** Molinos Carabobo at ~$29M Q1.

Full detail: [[payment-link-individuals-strategy]]

### Segment 2 — BNC-heavy senders (Outbound automation)

Workspaces that **send high volumes of outbound payments** through their BNC accounts. Their pain is manual batch uploads, multi-account juggling, no unified reconciliation.

- **Anchor ICP:** high-velocity outbound businesses — BNPL fintech, retail AP, delivery/gig payouts, insurance claim payouts.
- **101 workspaces total**, Q1 BNC outbound ≈ **$572M USD** (annualized ≈ $2.3B).
- **Whale:** Grupo cashea — $267M Q1 alone, 47% of segment volume.
- **Single biggest single-workspace prize:** Molinos Carabobo at ~$32M Q1 sending (plus $29M receiving — see double-qualified below).

Full detail: [[bnc-heavy-senders-strategy]]

### Double-qualified workspaces (highest-leverage prospects)

17 workspaces qualify as ICP in both segments. One sales conversation can surface two products:

- **Molinos Carabobo** — combined ~$61M Q1 prize. The heavyweight of the entire GTM. Bespoke treatment.
- **Grupo Leiros, AVICOLA LAS TUNAS, Grupo Maralac** — food/ag distributors with solid volume on both sides.
- **CORPORACION BEL, CAMOR, Alvarigua, alimentosmunchy, Doña Emilia, LPrado, Alimentos Global, Empresas Tapa Amarilla, Ramvall, Da Silva, ASOPORTUGUESA, JSL, TAMAYO, Centro Medico de Oncologia** — primarily Seg-1 weighted; Seg-2 pitch as secondary.

Full double-qualified matrix: see [[bnc-heavy-senders-strategy]] § Double-qualified prospects.

---

## Caracas trip (2026-04-26 → 2026-05-09) — priority targets

With ~1 week of prep time, the target stack for on-site deal closure:

1. **Molinos Carabobo** — double-qualified, combined $61M Q1 prize. Dedicated account brief needed.
2. **Food/ag distributor cluster** (double-qualified and Seg 1 anchors): Alvarigua, AVICOLA, BEL, Leiros, LPrado, Doña Emilia, munchy, Global, Maralac.
3. **Grupo cashea** — Segment 2 whale, marquee logo potential.
4. **Grupo UP** — cleanest individual-payer signal in the dataset; either already a customer (testimonial/case study) or top prospect.
5. **Healthcare cluster** — Centro Medico de Oncologia (Tier 2) as the insertion point; Cruz Roja (Tier 3 rescue) as secondary.
6. **Insurance rescue pass** — SEGVEN, Estar, Real, Hispana (Tier 3 rescue in Seg 1, Tier 1 in Seg 2 for SEGVEN). Need per-bank detail pull to solidify before pitching.

---

## This week's prep plan

Goal: arrive in Caracas on 2026-04-26 with ready-to-deliver pitches, account briefs, and a tight target list.

- **Mon–Tue (2026-04-21/22):** Business-context fill on unknown workspaces (Luis annotates both segment docs). Customer-status join (Q2e) — flag current Tesote Payments customers vs prospects across the combined list.
- **Tue–Wed:** Pitch deck per segment (two decks: Payment Link, BNC Outbound) plus a combined version for double-qualified conversations.
- **Wed–Thu:** Bespoke account briefs for Molinos Carabobo and Grupo cashea. One-pager per target for the top 10 double-qualified + top 5 Seg-2-only.
- **Thu:** Insurance rescue pass — pull per-bank detail for SEGVEN / Estar / Real / Hispana before any outreach.
- **Fri (2026-04-24):** Dry-run pitches with the team. Finalize the meeting schedule.
- **Sat: fly out.**

---

## Open questions / risks

- **Product SKU clarity.** What exactly do we call each offering? "Tesote Payment Link" and "Tesote Outbound Payments"? Or bundled under a single umbrella? Affects positioning and pricing.
- **Customer-status gap.** We don't yet know who's already on which Tesote product. Q2e is blocking the outreach list.
- **B2B direct-debit unblock timing.** If BNC Track B.1 activates during Caracas week, pitch dynamics shift mid-trip. Contingency: have a B2B direct-debit pitch ready too, even if not leading with it.
- **Segment 2 concentration risk.** Grupo cashea = 47% of segment volume. Critical conversation.
- **Molinos Carabobo extrapolation.** $29M Seg 1 prize is 48% extrapolated. Needs Q2c-style per-bank drill-down to validate before sizing in the pitch.

---

## Data sources

All queries in `luis-brain/data/`:

- **Segment 1 pipeline (Q2a → Q2d):** pattern discovery, workspace ranking, volume extrapolation, diversity-checked tiering.
- **Segment 2 pull:** BNC outflow Q1 2026 (spreadsheet — pending promotion to saved SQL).
- **Pending (Q2e, Q2f, Q3b):** customer-status join, Molinos Carabobo per-bank drill-down, non-BNC outbound analysis.

## Notion

- Umbrella (this doc) — to be pushed to Notion as parent of both segment docs.
- [[payment-link-individuals-strategy]] — already in Notion ([URL in memory reference](../../memory/reference_payment_link_individuals_strategy_notion.md)).
- [[bnc-heavy-senders-strategy]] — to be pushed to Notion alongside Segment 1.
