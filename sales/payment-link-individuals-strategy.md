---
title: Payment Link for Individuals — Sales Strategy v0
tags: [sales, payments, 10x, icp]
updated: 2026-04-19
status: draft
---

# Payment Link for Individuals — Sales Strategy v0

First draft of Tesote's GTM for the "Payment Link for Individuals" product. Built from Q1 2026 (Jan–Mar) VES inbound transaction data across the 19 Venezuelan banks we aggregate.

USD conversions throughout at **550 VES/USD** (spot rate as of 2026-04-19).

Related: [[payments-10x-bet]] · [[product-strategy-execution-plan]]

---

## TL;DR

- Tesote has a clear, repeatable **individual-payer ICP**: Venezuelan **wholesale food/agro distributors**, plus smaller but real clusters in **healthcare** and **insurance**.
- **23 workspaces** qualify as Tier 1 or Tier 2 ICP. Combined Q1 2026 individual-payer volume ≈ **$77M USD** (annualized ≈ **$300M USD**). Of that, **$50M USD in Q1 is directly confirmed** (not extrapolated).
- **Grupo UP** is the archetype: 8,625 unique individual-payer cedulas, 100% bank visibility, 35% of their total VES inbound is individual-transfer flow. The filter is working.
- **Grupo Carabobo** is the single biggest prize ($29M USD in Q1 alone) — food miller with massive wholesale flow — but half its volume is extrapolated. Needs a per-workspace deep-dive before banking on the number.
- GTM: **start with food distributors**, sell on collection-reconciliation pain, use Grupo UP or Alvarigua as a case-study prospect (or customer if already on the product).

---

## The product: what Payment Link for Individuals is

Short version: a shareable URL that a merchant gives to an individual customer. The customer opens it, pays via any Venezuelan rail (transfer, Pago Móvil, card), and the payment auto-reconciles against the merchant's invoice in Tesote.

Why merchants care: today they receive hundreds–thousands of individual payments per month via bank transfer, then someone on their team manually matches each payment to an invoice by eyeballing the bank description. As we learned building this analysis, **that description is often blind** — many banks don't even show who paid. Merchants rely on the customer forwarding proof, phoning the office, or emailing "I just paid, reference 12345."

The Payment Link kills that loop:
- Customer pays → Tesote identifies them via the link, not the bank description
- Auto-matches to the invoice
- Works across all 19 banks (including the 14 "dark" ones where description-based ID is impossible)
- Merchant sees the paid invoice within minutes, not days

The customers in the ICP below are **already receiving high volumes of individual payments** — they've just been paying the manual-reconciliation tax on every transaction.

---

## How we identified the ICP — methodology

### The bank landscape: who shows the payer, who doesn't

Venezuela has 19 banks where Tesote aggregates VES inbound activity. They split cleanly into two groups based on whether their transaction descriptions carry payer identity (cedula + often name):

**Identity-exposing banks (5)** — description reveals the individual payer:

| Bank | Example description | Payer info captured |
|---|---|---|
| Banco de Venezuela (BDV) | `TRANSF RECIBIDA BDV V15505367 ADRIANA ACOSTA` | cedula + name |
| Banco Exterior | `9742 TRANSF REC V26500259` | cedula |
| Banco Fondo Común | `TRF 0134 V011093313 SOLORZANO` | cedula + surname |
| Banesco | `TRF.MB 0134 V013537468 D ANGELO SAITTA L 0312` | cedula + name |
| BBVA Provincial | `TRAV0007083066000017000` (compressed format) | cedula only |

**Dark banks (14)** — description shows only generic labels, no payer identity:

Bancamiga, Bancaribe, Banco Activo, Banplus, Bangente, Banco Del Tesoro, Banco Plaza (mostly J-entity), BNC, Mercantil, R4 (100%Banco), Venezolano de Crédito, Bancrecer, 100% Banco, Cuenta Manual.

Typical dark-bank descriptions: `"NC Credito Inmediato"`, `"Pago movil recibido"`, `"CRÉDITO INMEDIATO RECIBIDO"`, `"Pago Plus Comercios Recibido Otros Banco"`. Useful for aggregate amounts, useless for identifying who paid.

This asymmetry is the core challenge — and it's also part of the Payment Link value prop. Tesote's product sidesteps the bank-description problem by identifying the payer at click-time, independent of which bank rail they pick.

### Venezuelan identifier conventions

- **V**: Venezuelan natural person (cedula) → **individual payer**, our target
- **E**: Foreign resident (extranjero) → also an individual
- **J**: Legal entity (RIF) → **exclude** (this is B2B)
- **G**: Government entity → exclude
- **P**: Passport → rarely appears

So our core signal is: description contains `[VE]<7-10 digits>`, and does NOT contain `J<7-10 digits>`.

### Filter stack — how rows got included or excluded

Applied to every transaction in the 19-bank dataset:

1. **Scope:** VES currency, Q1 2026 (2026-01-01 to 2026-04-01), inbound (amount > 0), non-discarded.
2. **Bank in identity-exposing set:** one of BDV, Exterior, Fondo Común, Banesco (VE, not Panama), BBVA.
3. **Contains V/E cedula pattern:** `description ~ '[VE][0-9]{7,}'`
4. **Does NOT contain J-RIF pattern:** `description !~ 'J[0-9]{7,}'`
5. **Does NOT contain `PJ` marker** (Persona Jurídica in Pago Móvil flows).
6. **Does NOT contain literal `RIF`.**
7. **Does NOT contain noise patterns:** POS liquidations, reversals, government programs, bond yields, etc. The exclusion regex accumulated over multiple hand-inspection passes:

```
L/POS, LIQUIDACI, LIQ., LIQ TDD, LIQ TDC, LIQ ELE,
INTERESES, PROVEEDOR, N/C CRED, INCENTIVO,
RECEPCION DE PAGO TERCERO, FONDOS RECIBIDOS, P2C,
REINTEGRO, DEPOS.ELECTRONI, MONEDERO PATRIA,
COMPRA EN PUNTO DE VENTA, TITULOS DE COBERTURA, COBERTURA,
RENDIMIENTO, PAGO DE INTERES, AB.LOTE, PAC APP REC,
TDY PAGO DE, REV.PAGO, REV.COM, DEVOLUCION RECIBIDA,
TRANSF CUENTAS PROPIAS, TRANSF A TERCEROS MB
```

These patterns are specific to Venezuelan banking — they represent POS card settlements (`L/POS`, `LIQUIDACI`, `TDY`, `DEPOS.ELECTRONI`), reversals (`REV.`, `REINTEGRO`), government programs (`MONEDERO PATRIA`), bond instruments (`TITULOS DE COBERTURA`), and internal aggregations (`AB.LOTE`, `PAC APP REC`). None are individual-payer signal.

### Discovery process — how the filter evolved

The filter wasn't top-down. It emerged from iterative hand-inspection:

1. **Q2a (pattern discovery):** Pulled 1000 VES transactions per bank and eyeballed the descriptions. First pass revealed: many banks never carry payer identity; the POS/liquidation patterns generate massive noise.
2. **Noise filter iteration:** Added exclusion patterns based on what kept showing up.
3. **Bank mapping:** Catalogued which banks show V/E cedulas vs which only show aggregator labels → the 5-vs-14 split above.
4. **Q2b (workspace ranking):** Required `[VE][0-9]{7,}`, excluded J-patterns, ranked workspaces by confirmed individual-payer tx count.
5. **Q2b validation:** Hand-inspected 1,000 sample rows across the top 20 workspaces. Critical finding: **the filter was clean**. The 48M, 30M, 20M VES "suspicious" amounts I initially flagged as B2B leakage turned out to be legitimate large individual payments — a Venezuelan informal-economy pattern where bodega owners pay wholesalers from personal cedula accounts, often millions of bolívares at a time.
6. **Q2c (volume extrapolation):** For each workspace, applied the "individual concentration ratio" observed on identity-exposing banks to the dark-bank volume, producing a full-prize estimate per workspace.
7. **Q2d (diversity + tiering):** Added `unique_cedulas` and `top10_cedula_pct` to kill false positives like EOODI (90% of volume from one cedula — likely the owner self-funding), Crixto Venezuela (11 cedulas — was actually a legal entity slipping through), konecta (24 cedulas, 89% top-10 — tiny sample, extrapolation unreliable). Workspaces then fall into T1 / T2 / T3 by confidence.

### The key extrapolation assumption

For dark-bank volume we don't see payer detail. We assume: **a given workspace's payer population is the same across all its bank rails.** If 30% of Workspace X's volume on BDV / Exterior / Banesco is confirmed individual, we assume ~30% of their Bancamiga / Mercantil / BNC volume is also individual.

This holds if the *customer base* drives the bank choice, not the *transaction type*. Reasonable for retail wholesale (bodegas just use whatever bank they happen to have). Less reliable for workspaces that route different payment types through different rails (e.g., POS via one bank, transfers via another).

The confidence dial is **`identity_coverage_pct`**: what % of a workspace's total VES inbound sits on identity-exposing banks (i.e., is directly observable):

- **≥80%** — estimate is essentially confirmed; extrapolation is a small tweak
- **50–80%** — directional; trust the order of magnitude
- **30–50%** — speculative; needs per-workspace validation before sizing
- **<30%** — flying blind; flag, don't plan on the number

### ICP tier assignment

A workspace makes Tier 1 only if **all four** hold:

- `individual_concentration_pct ≥ 15%` (of visible volume, 15%+ is individual)
- `identity_coverage_pct ≥ 50%` (extrapolation is small)
- `unique_cedulas ≥ 100` (real diversity, not single-payer)
- `top10_cedula_pct ≤ 50%` (no single cluster dominates)

Tier 2 relaxes to: concentration ≥10%, coverage ≥30%, cedulas ≥30, top-10 ≤70%.

Tier 3 = everything else. Most Tier 3 entries are noise (EOODI-style self-funding, Crixto-style legal entities, konecta-style near-zero-coverage), but a few are **rescue candidates** — they might be real ICP but our visibility is too thin to be sure. Flagged below.

---

## The ICP: tiered workspace list

Source data: `data/payments_icp_q2d_workspace_tiered_with_diversity.sql`.
All volumes are Q1 2026 VES inbound. USD at 550 VES/USD.

### Tier 1 — High-confidence ICP (11 workspaces, ~$35M USD Q1)

| Workspace | Prize USD | Confirmed USD | Conc% | Cov% | Cedulas | Top10% | Industry / notes (TODO) |
|---|---:|---:|---:|---:|---:|---:|---|
| Alimentos Alvarigua | $8.76M | $7.94M | 32.7 | 90.7 | 3,421 | 10.2 | Food/agro distributor |
| AVICOLA LAS TUNAS | $7.65M | $3.92M | 19.2 | 51.2 | 387 | 29.9 | Poultry distributor |
| CORPORACION BEL | $7.46M | $6.93M | 26.7 | 93.0 | 2,912 | 5.5 | ? |
| **Grupo UP** | $3.52M | $3.52M | 35.1 | **100.0** | **8,625** | **1.1** | ? — archetype, cleanest signal |
| ALIMENTOS DOÑA EMILIA | $2.37M | $1.86M | 20.8 | 78.5 | 374 | 30.9 | Food brand |
| alimentosmunchy | $1.79M | $1.38M | 16.3 | 77.0 | 1,189 | 27.7 | Snack manufacturer (Munchy) |
| Alimentos Global | $1.26M | $1.15M | **51.7** | 91.9 | 1,091 | 13.8 | Food wholesaler |
| Grupo Ramvall | $0.75M | $0.49M | 17.5 | 64.9 | 203 | 46.7 | ? |
| Grupo Del Este | $0.55M | $0.48M | 19.7 | 86.7 | 239 | 48.9 | ? |
| Grupo Da Silva | $0.44M | $0.22M | 29.4 | 50.9 | 286 | 42.9 | ? |
| Empresas Tapa Amarilla | $0.43M | $0.40M | 24.2 | 92.9 | 494 | 36.8 | ? |
| **Totals** | **$34.98M** | **$28.29M** | | | | | |

**Observation:** Food/agro distribution dominates. 7–8 of the 11 are directly food-adjacent. This is the **anchor ICP segment**.

### Tier 2 — Medium-confidence (12 workspaces, ~$42M USD Q1)

| Workspace | Prize USD | Confirmed USD | Conc% | Cov% | Cedulas | Top10% | Industry / notes (TODO) |
|---|---:|---:|---:|---:|---:|---:|---|
| **Molinos Carabobo** | **$29.33M** | $14.19M | 19.1 | 48.4 | 2,125 | 18.6 | Milling (food processor) — biggest single prize |
| Grupo Leiros | $3.17M | $1.78M | 14.9 | 56.2 | 1,932 | 20.2 | ? |
| ALIMENTOS LPRADO | $3.08M | $1.67M | 14.4 | 54.3 | 796 | 32.7 | Food brand |
| Disbattery Lubricantes | $1.56M | $1.56M | 11.3 | **100.0** | 2,351 | 18.2 | Battery/lubricant wholesale |
| CAMOR INTERNACIONAL | $1.47M | $1.24M | 15.0 | 84.1 | 2,029 | 12.9 | Trade/import |
| Grupo Maralac | $1.08M | $0.50M | 12.9 | 46.4 | 97 | 58.6 | Dairy? (Maralac) |
| Protinal | $0.84M | $0.73M | 11.2 | 87.0 | 438 | 39.5 | Protein feed distributor |
| **Centro Medico de Oncologia** | $0.51M | $0.24M | **42.2** | 48.1 | 182 | 27.9 | **Healthcare — patients paying** |
| ALMACENADORA ASOPORTUGUESA | $0.44M | $0.29M | 11.7 | 66.4 | 144 | 35.6 | Warehouse/storage |
| Grupo NSM | $0.29M | $0.09M | 13.2 | 32.2 | 102 | 37.3 | ? |
| TAMAYO & CIA. | $0.11M | $0.05M | 13.6 | 47.2 | 97 | 47.4 | ? |
| Corporación JSL | $0.05M | $0.05M | 10.5 | 95.0 | 388 | 22.2 | ? |
| **Totals** | **$41.93M** | **$22.40M** | | | | | |

**Observation:** Molinos Carabobo is a category by itself — it's 70% of the entire Tier 2 prize. A Q2c-style per-bank drill-down on Carabobo specifically would be worth doing before sizing it in any strategic deck. The rest is more food distribution (Leiros, LPrado, Protinal) plus the first healthcare entry (Centro Medico de Oncologia).

### Tier 3 — Rescue candidates worth a second look

Most Tier 3 entries are correctly filtered noise (single-payer workspaces, legal entities, <30% coverage speculation). A few, however, are flagged here because they *might* be real ICP but we don't have enough visibility to be sure.

| Workspace | Prize USD | Why flagged | What's needed |
|---|---:|---|---|
| Grupo Landa | $16.25M | 14.8% concentration — plausibly real, but only 6.9% coverage | Per-workspace bank-mix pull to see what's on dark banks |
| Grupo Mimesa | $7.06M | 78% coverage BUT only 8% concentration | Likely a mixed B2B+individual workspace — would need payer-name analysis |
| SEGVEN | $5.86M | 13.7% concentration, 8.8% coverage | Insurance — premium collection pattern; needs deeper validation |
| Molinos Nacionales | $4.37M | 92% coverage but just 5.6% concentration | Food miller mostly billed B2B, limited individual flow |
| Estar Seguros | $2.94M | 36.7% concentration (strong!) but 29.8% coverage | Insurance — rescue candidate |
| Real Seguros | $2.26M | 55.6% concentration, only 2.6% coverage | Insurance — tiny sample, strong signal, speculative |
| COSEIMPA | $2.47M | 30.7% concentration, 23.2% coverage | Distributor — worth a look |
| Hispana de Seguros | $0.79M | 52% concentration, 29% coverage | Insurance — rescue candidate |
| Cruz Roja | $0.46M | 51% concentration, 2.3% coverage | **Red Cross — donors!** Different ICP — nonprofit donation collection |

The insurance cluster (SEGVEN, Estar, Real, Hispana) is noteworthy. All show high concentrations but low coverage — classic "most of the payment action happens on dark banks" pattern. That matches the intuition that insurance collections are handled through specific operational banks. **Insurance is a Tier-2-adjacent secondary ICP** pending deeper validation.

---

## Patterns observed

### 1. Food/agro wholesale is the anchor ICP

Across Tiers 1 and 2 combined, 9+ workspaces are in food/agro distribution (Alvarigua, AVICOLA, BEL?, Doña Emilia, munchy, Alimentos Global, Molinos Carabobo, Leiros, LPrado, Protinal, Maralac, etc.). This is the single clearest segment pattern in the data.

**Why it fits:** Venezuelan mayoristas (wholesalers) sell to thousands of small bodegas, kioscos, abastos. Those small shops are typically single-proprietor operations where the owner pays from their personal cedula bank account — not a company RIF account. That's how a food distributor ends up with 3,000+ unique individual payers in a quarter.

**The individual transfers are often large** (millions of VES) because they represent wholesale orders, not retail purchases. This is what confused the initial interpretation — "individuals" here aren't consumers, they're small-merchant-owners paying in personal capacity.

### 2. Healthcare — emerging small ICP

Centro Medico de Oncologia (Tier 2, 42% concentration) and Cruz Roja (Tier 3 speculative, 51% concentration) show healthcare as a meaningful segment. Patients paying for treatment, donors giving to nonprofits — different use case, same technical need (identify individual payers and auto-reconcile).

### 3. Insurance cluster (Tier 3, needs rescue)

SEGVEN, Estar, Real, Hispana — all high concentration, low coverage. Insurance premium collection is an obvious payment-link use case (send renewal link, customer clicks, pays, auto-matches to policy).

### 4. Retail chains are NOT the ICP for Payment Link

Supermercados Rio Vida, VIVA SUPERCENTRO, Farmacias San Ignacio, Tiendas Traki, Cines Unidos — all ranked high on raw individual-tx count (hundreds of thousands of transactions) but fell to Tier 3 because their `individual_concentration_pct` is tiny (3–5%). Why: retail revenue is POS/card dominant, routed through merchant acquirers, not direct bank transfers. Tesote's Payment Link value prop for them is different (e-commerce / delivery / remote collection), not the mass-individual-transfer pain solved here.

---

## Sales strategy

### Value proposition (per segment)

**For food/agro distributors (Tier 1 anchor):**
> "You receive thousands of individual payments per month from bodegas and small shops, and your team spends hours each day matching bank deposits to invoices by hand. Many of those payments come from banks that don't tell you who paid. Payment Link solves that: one URL per invoice, payer clicks and pays, auto-matched in Tesote, done. We've measured your inbound: you received $X of individual-payer volume last quarter. Most of it was reconciled manually. Stop."

**For healthcare (Tier 2 secondary):**
> "Patients paying for treatment / donors giving to your cause currently transfer to your bank account and then call/email with 'I paid, here's my reference.' Payment Link gives them a URL, payment is auto-matched to the patient chart / donation campaign, and you get a real-time dashboard of who paid what."

**For insurance (Tier 3 rescue — needs validation):**
> "Premium collection is currently manual reconciliation of thousands of bank transfers against policies. Payment Link per renewal notice. Auto-match. Reduce DSO from weeks to hours."

### Priority sequence

1. **Phase 1 (this month):** Tier 1 outbound to the 11 workspaces. CEO/CFO-level conversations. Lead with the volume number ("you received $X of individual-payer payments in Q1"). Use **Grupo UP or Alvarigua as the proof-point prospect** — both have cleanest signal; if they're already Tesote Payments customers, ask for a testimonial.
2. **Phase 2 (next month):** Tier 2 outbound, with Molinos Carabobo as a bespoke campaign given the size. Validate Carabobo's per-bank mix first via a targeted Q2c-equivalent drill-down before sending a deck.
3. **Phase 3:** Insurance cluster discovery — pull a per-workspace detail report from SEGVEN/Estar/Real/Hispana banks to confirm the individual-payer assumption before outbound.
4. **Ongoing:** Re-run the Q2a→Q2d pipeline monthly. Track churn/growth of workspaces in/out of tiers. Watch for new workspaces entering Tier 1.

### Outreach angles that should work

- **The volume number is the hook.** "$X of individual-payer transfers in Q1" is concrete and specific; CEOs respond to their own numbers.
- **The reconciliation pain is universal.** Every one of these workspaces has at least one person doing description-matching manually. Ask the question directly in discovery.
- **The bank-description problem is a free wedge.** We can demonstrate — "here are 10 of your recent individual payments on Bancamiga; tell me the payer for each" — they can't. We can, because our product identifies at click-time.

### Qualifying questions for discovery calls

1. How many individual payments do you receive per month? (We already know; compare their answer to our number — tells us data-awareness.)
2. How do you currently match those to invoices? (Manual? Which team? How long does it take?)
3. Which banks do you use for this? (Tells us if they're on the dark banks we can't see today.)
4. Have you tried other payment-collection tools? (Competitive context.)
5. What % of your individual-payer revenue comes from repeat customers? (Sets up the "track individual-payer LTV" cross-sell.)

---

## Open questions / risks

- **Single-quarter data (Q1 2026 only).** Stability across quarters unknown. Should re-run for Q4 2025 to see how ranks shift quarter-over-quarter.
- **Some banks' cedula parsing is imperfect.** BBVA's compressed format (`TRAV00070830660...`) truncates cedulas at the 10-digit cap — `unique_cedulas` count is slightly inflated there. Not material for tiering, possibly material for payer-LTV analysis later.
- **Pago Móvil is a separate problem.** BDV's Pago Móvil flows carry phone numbers (`04127097254`) not cedulas. Same individuals, different identifier. Handling Pago Móvil properly is a Q2 project — BDV alone has ~14% of its inbound volume as Pago Móvil.
- **No customer-status join yet.** We don't know which of the 23 Tier 1+2 workspaces are already Tesote Payments customers vs. prospects. **Q2e is the next query** — joining against the payments-product-adoption table (schema TBD). Critical before sales outreach.
- **Need business-context fill-in.** Several Tier 1+2 workspaces are unfamiliar (Grupo UP, Grupo Ramvall, Grupo Del Este, Grupo Da Silva, Empresas Tapa Amarilla, Grupo Leiros, CAMOR, Grupo NSM, TAMAYO, JSL). Luis to annotate.
- **Tier 3 insurance and Grupo Landa deserve rescue attempts.** The <30% coverage is blocking them, but if we can pull per-workspace detail reports from their dominant banks, several could graduate to Tier 2.

---

## Next steps

- [ ] **Q2e:** Customer-status join — which of the 23 are current Tesote Payments customers. Depends on schema discovery.
- [ ] **Q2f:** Molinos Carabobo per-bank drill-down — validate the $29M extrapolation before using it strategically.
- [ ] **Business-context fill:** Luis to annotate the "Industry / notes" column in Tier 1 and Tier 2 tables.
- [ ] **Insurance rescue pass:** pull per-bank detail for SEGVEN, Estar, Real, Hispana.
- [ ] **Pago Móvil handling:** separate workstream — add phone-pattern extraction to complement the cedula-based pipeline.
- [ ] **Monthly refresh:** productionize the Q2a→Q2d pipeline; track tier transitions over time.
- [ ] **Promote to KB when ready** — this doc is currently `status: draft` in brain. Once the Tier 1 outreach hits the field and returns first learnings, refactor and copy to `knowledge-base/sales/`.

---

## Data sources

All queries in `data/`:

- `payments_icp_q2a_individual_payer_pattern_discovery.sql` — noise-filtered per-bank sample (the dataset that revealed the 5-vs-14 bank split)
- `payments_icp_q2b_individual_payer_by_workspace.sql` — workspace ranking by confirmed individual-payer transactions
- `payments_icp_q2b_validation_rows.sql` — top-workspace row-level hand-inspection
- `payments_icp_q2c_workspace_full_volume_estimate.sql` — volume extrapolation to dark banks via concentration ratio
- `payments_icp_q2d_workspace_tiered_with_diversity.sql` — payer-diversity checks + tier assignment (the source-of-truth query for this doc)
