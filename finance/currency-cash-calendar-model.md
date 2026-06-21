---
title: Currency Cash Calendar — Matching Model & Capital Requirements
tags: [finance, treasury, fx, working-capital, calendar]
updated: 2026-06-09
status: draft
---

# Currency Cash Calendar — Matching Model

The operating model: **match revenue to expenses *by currency first*, finance only the mismatch.** USD revenue offsetting USD expense is a free natural hedge — no conversion, no spread, no lag. Bs revenue offsets Bs expense the same way. Only the residual needs FX conversion + capital.

> Synthesizes `[[financial-policy-non-negotiables]]`, `[[scenario-reserve-credit-equity-2026-06]]`, `[[usd-liquidity-gap-sizing]]`. Working rate: **550 Bs/USD**. All Bs shown as USD-equivalent unless noted.

---

## The waterfall (do this every month)

```
  USD revenue ──offsets──► USD expenses        → residual USD GAP  (must source/finance)
  Bs revenue  ──offsets──► Bs expenses          → residual Bs SURPLUS
                                                       │ convert (spread + lag)
                                                       ▼
                          Bs surplus covers part/all of the USD gap
                                                       │
                                                       ▼
                          TRUE residual = USD gap − converted Bs surplus
                          → if >0: financed by USD float/line (or equity if structural)
```

Two numbers fall out of this every month:
1. **Conversion volume** = how much Bs you must turn into USD = the smaller of (USD gap, Bs surplus). Drives spread cost + float.
2. **True residual deficit** = what's left after conversion = your real net burn, in USD terms.

---

## ★ ACTUALS (2026-06-09): $40k USD MRR, ~42% USD share

Luis confirmed: **~$40k/mo recurring revenue is USD**, the rest Bs. Against ~$95k total revenue → **USD share ≈ 42%**, Bs ≈ $55k. Plugging the real number through the waterfall:

| Step | $ |
|---|---:|
| USD revenue | 40 |
| USD expenses | 100 |
| **USD gap** (must source in USD) | **60** |
| Bs revenue | 55 |
| Bs expenses | 12 |
| **Bs surplus** (available to convert) | **43** |
| **Must convert** = min(gap, surplus) | **43** |
| **True USD residual deficit** = 60 − 43 | **17** ← the net burn, in USD |

**What this means concretely (today, pre-breakeven):**

- You convert **~$43k/mo** Bs→USD. That's the spread + lag exposure: ~**$15.5k/yr** in spread @ 3%.
- After converting every available Bs surplus, you're *still* **$17k/mo short in USD** — that's the real burn, and it bleeds from USD cash until breakeven.
- **Conversion float** (the permanent revolving piece): $43k/mo = $1.43k/day:

| Cycle | Float (1.25× safety) |
|---:|---:|
| 45 days | **$80k** |
| 60 days | **$107k** |
| 90 days | **$161k** |

So at a 60-day cycle, the line carries **~$107k of permanent float + ~$17k/mo of bridge burn** simultaneously. A **$250k line** covers both with real headroom. The $400k reserve stays untouched. **The structure holds at your actual mix.**

### ⚠️ The tension you have to decide on

Your 42% USD share is *healthier than I assumed* — but it's fragile, because **your 10x growth engine (VES cobros / payments) is Bs-denominated.** If growth concentrates in Bs, your USD share *falls* as you scale, the USD gap *widens*, and the conversion float + spread *grow* — even as the accounting picture improves toward breakeven.

Watch what happens to the float at breakeven ($112k revenue) depending on where growth comes from:

| Growth mix to breakeven | USD rev | USD gap | Convert/mo | Float @ 60-day |
|---|---:|---:|---:|---:|
| USD MRR flat $40k, all growth in Bs | 40 | 60 | 60 | **$150k** ▲ worse |
| USD share held at 42% | 47 | 53 | 53 | **$133k** |
| USD-led (USD MRR → ~$57k) | 57 | 43 | 43 | **$107k** ▼ better |

**Decision:** as cobros scales you must do *at least one* of —
1. **Grow USD-denominated revenue in parallel** (price cross-border/US clients in USD, push Stripe USD) so share doesn't collapse;
2. **Shift cost base toward Bs** (more VE-based hires paid in Bs vs. US payroll) to shrink the $100k USD obligation from the *cost* side;
3. **Accept a larger USD line** ($300k+) and the extra spread as the cost of a Bs-heavy growth strategy.

(1) and (2) are the capital-efficient paths. (3) is the default if you do nothing. Make it a conscious choice — track **% revenue in USD** monthly so you see it moving before it bites.

---

## a) Revenue calendar — by currency *(fill with real invoicing data)*

Expected **invoiced** revenue (accrual), split by collection currency. ⚠️ Currently estimated — replace with Mariel's invoicing schedule per entity.

| Month | USD invoiced | Bs invoiced (USD-eq) | Total | USD % |
|---|---:|---:|---:|---:|
| Jul | | | | |
| Aug | | | | |
| Sep | | | | |
| Oct | | | | |
| Nov | | | | |
| Dec | | | | |

**Also capture per line (this is the real work):**

| Client | Entity | Currency | Cadence (mo/qtr) | Amount | Typical days-to-collect |
|---|---|---|---|---:|---:|

## b) Expense calendar — by currency

| Bucket | Currency | $/mo | Fixed date? |
|---|---|---:|---|
| Multiplier | USD | 30 | recurring cycle |
| Gusto payroll | USD | 27 | 2 cycles |
| Contractors (Rho) | USD | 21 | month-end |
| Million Web | USD | 12 | monthly |
| SaaS / infra | USD | 10 | scattered |
| **USD subtotal** | | **~100** | |
| VES honorarios / transporte | Bs | 8 | month-end |
| Taxes / utilities / fees | Bs | 4 | variable |
| **Bs subtotal** | | **~12** | |
| **Total** | | **~112** | |

The asymmetry is the whole problem: **~$100k USD out vs. ~$12k Bs out**, but revenue skews Bs. USD is the binding constraint.

---

## Projections — how the answer moves with USD-revenue share

Total revenue held at **$95k/mo** (pre-breakeven). The net burn is **invariant** to currency mix (~−$17k = $95k − $112k). But everything that *costs* money — conversion volume, spread, float — shrinks as USD revenue rises. That's the lever.

| USD rev share | USD rev | Bs rev | USD gap (100−USDrev) | Bs surplus (Bsrev−12) | Must convert | True USD residual |
|---:|---:|---:|---:|---:|---:|---:|
| 15% | 14 | 81 | 86 | 69 | **69** | −17 |
| 25% | 24 | 71 | 76 | 59 | **59** | −17 |
| 35% | 33 | 62 | 67 | 50 | **50** | −17 |
| 50% | 48 | 47 | 52 | 35 | **35** | −17 |

**Read:** net burn is −$17k no matter what — but at 15% USD you convert **$69k/mo**, at 50% USD only **$35k/mo.** Half the conversion = half the spread cost and half the float.

### What that does to capital required

Float ≈ `(must-convert ÷ 30) × cycle days × 1.25 safety`. Spread @ 3%.

| USD share | Convert/mo | Float @ 60-day cycle | Spread cost/yr |
|---:|---:|---:|---:|
| 15% | $69k | **$173k** | ~$25k |
| 25% | $59k | **$148k** | ~$21k |
| 35% | $50k | **$125k** | ~$18k |
| 50% | $35k | **$88k** | ~$13k |

**Moving from 15%→50% USD revenue share cuts the required line from ~$173k to ~$88k and saves ~$12k/yr in spread — without growing revenue a dollar.** Pure capital efficiency.

---

## At breakeven (rev = exp = $112k)

Net is zero, but the float doesn't disappear — you still convert the USD gap every month:

| USD share | USD rev | USD gap | Convert/mo | Float @ 60-day |
|---:|---:|---:|---:|---:|
| 35% | 39 | 61 | 61 | **$153k** |
| 50% | 56 | 44 | 44 | **$110k** |
| 65% | 73 | 27 | 27 | **$68k** |

**The permanent line you need at breakeven = `(USD expenses − USD revenue) × cycle/30 × 1.25`.** The only way to drive it toward zero is to make USD revenue ≥ USD expenses — i.e. fund your US-denominated cost base with US-denominated revenue.

---

## Capital requirements — keeping the sequence healthy & efficient

Three distinct needs, three instruments:

| Need | Driver | Instrument | Size |
|---|---|---|---|
| **Pipeline float** (permanent) | Convert-volume × cycle | **Revolver** | $88–173k depending on USD share + cycle |
| **Burn bridge** (until breakeven) | Cumulative net loss | Revolver headroom + equity | ~$45–200k (see scenario doc) |
| **Structural reserve** | Survival | Locked USD cash | $400–480k, never touched |

The line does double duty (float **and** bridge) — so size it for the *larger* of the two at any moment, plus headroom. A **$250k committed line** covers a 60-day cycle at today's mix *and* the mid-case bridge simultaneously. That's the number to go get.

### The three levers, ranked by leverage

1. **Grow USD-revenue share.** Biggest structural win — cuts float, spread, *and* the binding-constraint risk all at once. Price cross-border / US clients in USD; push Stripe USD collections. Treat "% revenue in USD" as a tracked treasury KPI.
2. **Shorten the cycle** (days-to-collect via cobros + a standing conversion cadence). Each day = ~$0.7k–1.1k less float drawn (scales with convert volume).
3. **Size the line to the measured cycle + mix**, not a guess. Once a/b are populated and we know T, the float number is exact.

---

## What to go measure (turns this from estimate → real)

- [ ] **a) Revenue by currency** — Mariel's invoicing schedule, per client, per entity, USD vs Bs. The single highest-value input.
- [ ] **b) Expense dates by currency** — the USD obligation calendar (when, not just how much) → reveals the intra-month USD low point the float must cover.
- [ ] **Days-to-collect** (cobros Track 1 is on it) and **days-to-convert** (Subasta/OTC lead time) → the cycle T.
- [ ] **Current USD-revenue share** — confirm the real % (my projections span 15–50%; reality anchors the whole model).
- [ ] **FX spread per conversion** — measure it; at ~$50k/mo volume, 1% = ~$6k/yr.

Once a) and b) are populated with real monthly figures, this doc *is* the rolling 6-month currency cash forecast — drop in actuals each month and the float/line/deficit numbers compute themselves.

---

## Bottom line

- **Match first, finance the mismatch.** USD-rev↔USD-exp and Bs-rev↔Bs-exp are free hedges; only the residual costs money.
- **Net burn is mix-invariant, but capital efficiency is not.** Same −$17k burn can need a $173k line or an $88k line depending purely on currency mix.
- **Growing USD-revenue share is a treasury strategy, not just a sales one** — it shrinks the float, the spread, and the FX risk simultaneously. Make it a KPI.
- **A $250k committed line, sized to a 60-day cycle, covers both the float and the bridge** — and keeps the $400k reserve untouched by design.

## Related
- [[usd-liquidity-gap-sizing]] — the float formula this model operationalizes
- [[scenario-reserve-credit-equity-2026-06]] — the burn-bridge half
- [[financial-policy-non-negotiables]] — the reserve/cap/policy frame
- [[ar-and-cobros-2026-05]] — days-to-collect + the invoicing-schedule source
