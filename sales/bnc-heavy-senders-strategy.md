---
title: BNC-Heavy Senders — Sales Strategy v0 (Segment 2)
tags: [sales, payments, 10x, icp, bnc]
updated: 2026-04-19
status: draft
---

# BNC-Heavy Senders — Sales Strategy v0 (Segment 2)

Second of two Payments sales strategy docs. Companion to [[payment-link-individuals-strategy]] (Segment 1). Both sit under [[payments-gtm-while-b2b-gated]].

Segment 2 targets workspaces that **send high volumes of outbound payments through their BNC accounts**. The product fit is outbound-payment automation / batch payouts / multi-account consolidation — a non-blocked use case Tesote can sell today while the biz-biz direct-debit rail is bank-gated.

Data source: BNC outflow query, Q1 2026 (Jan–Mar). USD at 550 VES/USD.

Related: [[payments-10x-bet]] · [[bnc-ach-status]]

---

## TL;DR

- **$572M USD** of outbound payment volume flowed through BNC accounts across 101 Tesote workspaces in Q1 2026 — **1.27M transactions**.
- **Grupo cashea dominates**: $267M Q1 alone (47% of total volume, 16 BNC accounts). Category-of-one whale.
- **Top 8 workspaces** represent ~$470M of the $572M total (82%). The long tail is thin.
- **17 of the 23 Segment 1 Tier 1+2 workspaces also appear in Segment 2** — these are the **double-qualified prospects**, fit for both Payment Link (receiving) and BNC automation (sending). Molinos Carabobo is the heaviest: ~$32M Q1 outflow + ~$29M individual-payer prize.
- Net-new-from-Seg-1 prospects include Grupo cashea, KAIZEN, Avila, SEGVEN, Supermercados Luxor, Crixto, GRUPO FUTURA, konecta, Canguro, Curiara.
- GTM: **start with the double-qualified set** (single conversation, two products). Then whales (cashea, KAIZEN, Avila). Insurance (SEGVEN) and retail (Luxor) as secondary clusters.

---

## The product framing

Segment 2 customers already do high-volume outbound via BNC — today, usually via BNC's web portal or spreadsheet-driven manual batch uploads, one-by-one confirmations, manual reconciliation of sent payments.

The Tesote value prop for them isn't "pull money from your clients" (that's the blocked direct-debit product) — it's **"orchestrate your outbound BNC payments, across all your BNC accounts, with auto-reconciliation and a unified dashboard."** Concretely:

- Batch-upload outbound payments across one or many BNC accounts
- Auto-verify counterparty, handle duplicates, track status
- Reconcile sent payments against supplier/employee/driver/customer records
- Multi-entity consolidation for companies with 10+ BNC accounts (several on the list have 20–130)
- Reporting / audit trail / reversal handling

This is a different product from Payment Link for Individuals (Segment 1), but sold by the same sales team, often to the same workspace. Where a prospect qualifies for both, run one discovery conversation and pitch both.

---

## Data: Q1 2026 BNC outbound by workspace

### Tier-1 (whales) — >$10M Q1 USD outflow (8 workspaces, ~$447M)

| Workspace | BNC accts | Q1 tx | Q1 USD out | MoM trend (USD) | Notes (TODO) |
|---|---:|---:|---:|---|---|
| **Grupo cashea** | 16 | 84,019 | **$267.8M** | $71.7M → $100.0M → $96.0M | BNPL — whale; paying merchants post-BNPL settlement |
| KAIZEN | 18 | 24,058 | $51.9M | $15.6M → $15.3M → $20.9M | ? |
| Avila | 132 | 1,352 | $41.3M | $16.1M → $14.2M → $11.0M | 132 BNC accounts — multi-entity / holding? |
| **Molinos Carabobo** | 10 | 310 | $31.9M | $4.7M → $12.0M → $15.1M | **Also Seg 1 Tier 2** — double-qualified |
| SEGVEN | 10 | 99,661 | $30.7M | $6.7M → $9.5M → $14.5M | Insurance — claim payouts (high tx count matches) |
| Supermercados Luxor | 16 | 27,181 | $20.1M | $7.0M → $6.7M → $6.3M | Retail — supplier payments |
| Crixto Venezuela | 5 | 11,656 | $13.8M | $5.1M → $5.0M → $3.7M | ? |
| GRUPO FUTURA | 9 | 38,016 | $10.2M | $3.0M → $3.4M → $3.9M | ? |
| **Total Tier 1** | | | **$467.7M** | | |

### Tier-2 (strong) — $2M–$10M Q1 USD outflow (~15 workspaces)

| Workspace | BNC accts | Q1 tx | Q1 USD out | Overlap with Seg 1? |
|---|---:|---:|---:|---|
| konecta de occidente | 3 | 373,863 | $9.5M | — (high tx, low ticket) |
| **Grupo Leiros** | 29 | 9,638 | $7.6M | **Seg 1 Tier 2** |
| Canguro Venezuela | 25 | 161,459 | $7.2M | — (delivery driver payouts likely) |
| Curiara | 1 | 93,867 | $5.6M | — |
| **Molinos Nacionales** | 11 | 501 | $5.5M | Seg 1 Tier 3 rescue candidate |
| VIVA SUPERCENTRO | 8 | 11,901 | $4.8M | Seg 1 Tier 3 (retail) |
| MangoCenter | 2 | 8,374 | $4.8M | — |
| Procesadora Marsoca | 6 | 3,324 | $4.6M | Seg 1 Tier 3 |
| **Grupo Maralac** | 29 | 2,233 | $3.8M | **Seg 1 Tier 2** |
| ARMI | 3 | 179,952 | $3.0M | — |
| Bandecorp | 43 | 11,508 | $2.8M | — |
| **AVICOLA LAS TUNAS** | 10 | 1,997 | $2.8M | **Seg 1 Tier 1** — double-qualified |
| **Grupo Landa** | 21 | 750 | $2.4M | Seg 1 Tier 3 rescue candidate |
| Club Puerto Azul | 4 | 5,649 | $2.3M | — (country club — member fees?) |
| FIVENCA | 9 | 537 | $2.2M | — |
| EOODI | 21 | 16,623 | $2.0M | Seg 1 Tier 3 |
| Casa Franceschi | 10 | 1,823 | $2.0M | Seg 1 Tier 3 |

### Tier-3 (long tail) — <$2M Q1 USD outflow

~78 workspaces below the $2M Q1 threshold. Notable inclusions for overlap:

- **CORPORACION BEL** — $1.1M Seg 2 but Seg 1 Tier 1 at $7.5M. Classify as Seg-1-led, Seg-2 secondary.
- **CAMOR INTERNACIONAL** — $1.0M Seg 2, Seg 1 Tier 2 at $1.5M.
- **ALMACENADORA ASOPORTUGUESA**, **Grupo Da Silva**, **ALIMENTOS LPRADO**, **alimentosmunchy**, **ALIMENTOS DOÑA EMILIA**, **Centro Medico de Oncologia**, **TAMAYO**, **Empresas Tapa Amarilla**, **Grupo Ramvall**, **Corporación JSL**, **Alimentos Global** — all Seg 1 Tier 1+2 workspaces with light BNC outflow. They qualify on receiving, not sending.

---

## Double-qualified prospects (priority set)

These workspaces appear in both Segment 1 (Tier 1+2) and Segment 2. One conversation, two pitches, two revenue lines:

| Workspace | Seg 1 prize (receiving) | Seg 2 Q1 outflow (sending) | Tier combo |
|---|---:|---:|---|
| **Molinos Carabobo** | $29.3M | $31.9M | **S1-T2 · S2-T1** — the heavyweight of the whole analysis |
| **Grupo Leiros** | $3.2M | $7.6M | S1-T2 · S2-T2 |
| **AVICOLA LAS TUNAS** | $7.6M | $2.8M | **S1-T1 · S2-T2** |
| **Grupo Maralac** | $1.1M | $3.8M | S1-T2 · S2-T2 |
| **CORPORACION BEL** | $7.5M | $1.1M | S1-T1 · S2-T3 (Seg-1-led) |
| **CAMOR INTERNACIONAL** | $1.5M | $1.0M | S1-T2 · S2-T3 |
| ALMACENADORA ASOPORTUGUESA | $0.4M | $0.8M | S1-T2 · S2-T3 |
| Grupo Da Silva | $0.4M | $0.7M | S1-T1 · S2-T3 |
| ALIMENTOS LPRADO | $3.1M | $0.6M | S1-T2 · S2-T3 |
| alimentosmunchy | $1.8M | $0.5M | S1-T1 · S2-T3 |
| ALIMENTOS DOÑA EMILIA | $2.4M | $0.4M | S1-T1 · S2-T3 |
| Centro Medico de Oncologia | $0.5M | $0.3M | S1-T2 · S2-T3 |
| TAMAYO & CIA. | $0.1M | $0.2M | S1-T2 · S2-T3 |
| Empresas Tapa Amarilla | $0.4M | $0.1M | S1-T1 · S2-T3 |
| Grupo Ramvall | $0.7M | $0.1M | S1-T1 · S2-T3 |
| Corporación JSL | $0.05M | $0.03M | S1-T2 · S2-T3 |
| Alimentos Global | $1.3M | $0.01M | S1-T1 · S2-T3 |

**Molinos Carabobo is the single biggest target of the entire Payments GTM.** Combined prize (receiving + sending) ≈ $61M Q1. Bespoke pitch warranted.

---

## Segment 2-only prospects (net-new from Seg 1)

Key net-new opportunities worth standalone pitch:

1. **Grupo cashea** ($267M) — BNPL fintech. Existing 16 BNC accounts. Most sophisticated potential buyer on the list; likely already thinking about automation. Strong outbound-velocity growth Q1. Would be a marquee logo.
2. **KAIZEN** ($52M, 18 accounts) — unknown to me. Luis?
3. **Avila** ($41M, **132 accounts**) — huge account count suggests holding company / multi-entity group. Consolidation value prop is strongest here.
4. **SEGVEN** ($31M, 99,661 tx) — insurance. Claim payout automation is the pitch. Pairs with Segment 1 insurance-cluster rescue candidates.
5. **Supermercados Luxor** ($20M) — retail chain. Supplier payments.
6. **konecta de occidente** (373k tx, $9.5M) — high-tx, low-ticket pattern strongly suggests delivery/gig-worker payouts.
7. **Canguro Venezuela** (161k tx, $7.2M) — logistics/delivery, driver payouts.
8. **Curiara** (93k tx on 1 BNC account, $5.6M) — high-volume single-account, interesting edge case.

---

## Sales strategy

### Value proposition

**Generic pitch (Tier 1+2):**
> "You moved $X USD through your BNC accounts last quarter across Y accounts and Z transactions. Most of that was done by hand or via the BNC web portal, one batch at a time. Tesote consolidates all your outbound BNC flows into one interface — batch uploads, auto-verification, unified dashboard, full reconciliation. If you're managing this across 10+ BNC accounts today, the consolidation alone is worth the switch."

**For retail chains (Luxor, VIVA):**
> Supplier AP automation — standardized payment runs, receipt generation, automated confirmations back to suppliers.

**For delivery/gig (konecta, Canguro):**
> Driver/courier payout automation — handle thousands of low-value payouts per day, batch confirmation, failure handling, payroll-style reporting.

**For insurance (SEGVEN):**
> Claim payout automation — tie payment to claim record, track per-policy spend, audit trail.

**For BNPL / merchant-facing (cashea):**
> Merchant settlement automation — automated daily/weekly payout runs to merchants based on ledger positions.

### Priority sequence (for Caracas 2026-04-26 trip)

1. **Double-qualified whale: Molinos Carabobo.** Bespoke prep. Pitch both Payment Link (~$29M prize) and BNC outbound automation (~$32M). Combined this is the single biggest conversation of the trip.
2. **Segment 2 whales with S1 footprint — Grupo Leiros, AVICOLA, Maralac.** These are food/ag distributors who both receive from individuals AND send heavy BNC. Dual pitch.
3. **Segment 2 net-new whales — Grupo cashea, KAIZEN, Avila, SEGVEN, Luxor.** Fresh outreach; need business-context briefing from you before Caracas.
4. **Seg-1-led workspaces with small Seg-2 footprint (BEL, CAMOR, etc.)** — lead with Payment Link, mention BNC outbound as "and we also handle this if you want."
5. **Segment 2 only, Tier 2 cluster** — konecta/Canguro/Curiara (gig/delivery), MangoCenter, FUTURA, Marsoca. Warm outreach, not priority for Caracas.

### Discovery questions specific to Segment 2

1. How are you handling your BNC outbound today — web portal, spreadsheet upload, API, other?
2. How many BNC accounts do you operate, and why that many (multi-entity, bank-redundancy, segmentation)?
3. Who on your team manages the outbound flow, and how much of their week is it?
4. Have you looked at automation tools before — what blocked adoption?
5. Are the outbound payments primarily to (a) suppliers, (b) employees, (c) customers/refunds, (d) drivers/gig workers? (Answer shapes the pitch.)

---

## Open questions / risks

- **Grupo cashea concentration is risky.** $267M is 47% of the total Segment 2 volume. If cashea does not convert, the segment size halves. Mitigant: cashea is a marquee target where even a pilot at 10% of their volume is a significant deal.
- **"Through BNC accounts" may not equal "stays on BNC."** Some of this volume is BNC → other-bank payouts (outbound ACH to Bancamiga, etc.). Need to confirm this is in-scope for whatever Tesote product we're selling.
- **Other banks also move outbound money.** We only analyzed BNC because it's the major business rail. A Q3b-style analysis for Banesco Empresa / Mercantil / BBVA outbound would round out the picture — but not needed for Caracas.
- **Business context missing for ~half the Tier-1/2 list.** Especially KAIZEN, Avila, Crixto, FUTURA, Curiara, MangoCenter, ARMI, Bandecorp. Luis to annotate.
- **Same customer-status gap as Segment 1.** We don't know who's already on Tesote Payments vs. prospect.

---

## Next steps

- [ ] **Business-context fill:** Luis to annotate the unknown workspaces before Caracas.
- [ ] **Customer-status join:** a single Q2e query covers both segments — flag current Tesote customers and current Payments-product users across the combined list.
- [ ] **Caracas preparation:** pitch decks per priority segment (double-qualified whales, Seg-2 whales, retail, gig/delivery, insurance).
- [ ] **Molinos Carabobo bespoke brief.** Combined $61M prize warrants a dedicated one-pager + account plan for the trip.
- [ ] **Grupo cashea briefing.** Marquee target — need context on the existing Tesote relationship (if any), stakeholders, competing solutions they've evaluated.
- [ ] **Define the product SKU we're selling in Segment 2.** Is this "Tesote Outbound Payments", "BNC Automation", part of the core "Full Reconciliation" bundle? Needed for clean pitch positioning.
- [ ] **Monthly refresh:** rerun this query monthly, track tier movement, watch for growth signals (MoM % change on outflow).

---

## Data source

Q1 2026 BNC outflow per workspace — spreadsheet: `bnc_outflows__q1__2026-04-19T16_07_08.xlsx` (Luis's Downloads). Should be promoted into `luis-brain/data/` as a saved SQL query for reproducibility on monthly refresh.
