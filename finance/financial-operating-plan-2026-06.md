---
title: Tesote — Financial Operating Plan & Financing Recommendation
tags: [finance, runway, treasury, financing, policy]
updated: 2026-06-09
status: draft
---

# Tesote — Financial Operating Plan & Financing Recommendation

**Date:** June 2026
**Purpose:** Define the non-negotiable financial rules Tesote operates under, model the next 6 months honestly given how money actually moves through the business, and recommend a financing structure that lets the team run on a tracked plan instead of month-to-month anxiety.

This document is self-contained. It assumes no prior context.

---

## Executive summary — the recommendation

**Do both, deliberately sized: secure a credit line now, and raise a modest equity round now. They solve two different problems, and together they convert a fragile plan into one we can simply track.**

1. **Credit line — ~$250k, secured on the US entity.** This is the workhorse. It funds (a) the permanent working-capital float created by collecting revenue in bolívars but paying most costs in USD, and (b) the bridge to breakeven. It is non-dilutive and you only pay for what you draw. **We do not have one today — securing it is the single most important action.**

2. **Equity (SAFE) — ~$250–400k, now.** Not to fund routine burn (the line does that), but to **rebuild an operating buffer above the untouchable reserve** and **insure the downside** (slower growth, a delayed breakeven, a lumpy collection month, or the line coming in smaller than hoped). Today the company sits with essentially **zero buffer above its own reserve floor** — that is the entire source of financial stress, and the equity is what removes it.

**Why both, and not one:**
- *Line alone* leaves no margin — the company would run at or near its reserve floor until breakeven, so any single bad month forces a choice between maxing the line and breaking the reserve. That is the stressful path.
- *Equity alone* would mean funding a permanent, revolving working-capital need with permanent dilutive capital — the most expensive way to solve the cheapest problem. A revolver is the right tool for a revolving need.

**The end state:** a $400k reserve that is never touched, a $250k line that absorbs the currency float and the bridge, and an equity buffer that absorbs surprises. Under the base-case growth path this is comfortable, and under the downside it still holds.

---

## 1. The business in one paragraph (why currency is the whole story)

Tesote operates across a US entity (Delaware C-corp) and a Venezuelan entity. **Roughly $40k/month of recurring revenue is collected in USD; the remainder — and effectively all of the growth — is collected in bolívars (Bs).** Meanwhile, **the large majority of costs (~$120k/month: US payroll, contractors, core vendors, software) must be paid in USD**, on a fixed calendar. Bolívar revenue is not spendable on USD obligations until it is converted, and that conversion takes time. **So the binding constraint on the business is not total net worth — it is USD liquidity.** Every rule below follows from that fact.

### Current monthly run-rate

| | USD | Bs (USD-equiv) | Total |
|---|---:|---:|---:|
| Recurring revenue (MRR) | $40k | $55k | $95k |
| Implementation fees | — | $7k | $7k |
| **Revenue** | **$40k** | **$62k** | **$102k** |
| Expenses | $120k | $12k | $132k |
| **Net** | **−$80k** | **+$50k** | **−$30k** |

The −$80k USD line and +$50k Bs line are the heart of it: there is a structural **$80k/month USD shortfall** that must be filled by converting the bolívar surplus into dollars. *(Bolívar amounts are shown as USD-equivalent; a working exchange rate is intentionally not fixed in this document.)*

---

## 2. The non-negotiables (the rules we operate under)

These are constraints, not targets — lines we don't cross, and crossing one is itself a trigger to act.

### a) Untouchable reserve — $400k, in USD

- Twelve months of survival at a capped burn. Held **in USD** (the binding constraint) in a **separate, walled-off account**.
- Touched only on a declared crisis (revenue collapse plus inability to raise) — never for a routine bad month.
- *Note on sizing:* a strict reading (a $40k/month cap × 12) would put this at $480k. We set it at **$400k** because a committed credit line restores the difference — an undrawn line is contingency capital, which means we don't need to hold as much idle cash. **The $400k figure is only sound if the line is actually committed.** Until then, treat $480k as the real floor.

### b) Burn cap — $40k/month net

- Measured on a **trailing-three-month average**, not single months (individual months are noisy — payroll cycles, tax timing, one-offs).
- Net burn today is ~$30k/month, so $40k is a ceiling with headroom, not the run-rate.
- **Breaching the cap two months running triggers forced action** (renegotiate, cut, or fund). The largest discretionary levers — vendor renegotiation, contractor review, software consolidation — represent meaningful monthly flex and are what make the cap defensible as a stress number.

### c) Operating buffer — above the reserve

- A working buffer that sits **on top of** the reserve and absorbs normal timing swings, so the reserve is never the de-facto operating account.
- With a committed line as the deeper contingency, this buffer can be modest — enough to cover two to three months of net burn plus one lumpy collection month. **Target: roughly $150–250k above the reserve.**

---

## 3. How money actually moves — the currency mismatch

This is the mechanism that makes the plan non-obvious. Even at accounting breakeven, a cash gap remains, because of the cycle below:

```
  Invoice issued (mostly Bs)
      │   days to collect   (slow-paying market)
      ▼
  Bolívars received
      │   days to convert   (batch FX operations, not continuous)
      ▼
  USD in hand  ──►  pays US payroll, contractors, vendors, software
```

**The full clock — invoice to spendable USD — runs an estimated 45–60 days.** During that window, USD obligations keep hitting on schedule while the matching revenue is still in transit. The amount of USD perpetually "in flight" is a **working-capital float** the business must finance continuously.

**Two distinct gaps result, and they need different instruments:**

| Gap | Nature | Instrument |
|---|---|---|
| **Conversion float** | Permanent, revolving — survives breakeven | Credit line (revolver) |
| **Burn bridge** | Temporary — closes at breakeven | Credit line + equity buffer |

Critically: because the USD revenue is flat at $40k and USD costs are flat at $120k, **the monthly USD shortfall is pinned at $80k**, and *all* growth arriving in bolívars means the conversion volume only rises until it hits that $80k ceiling. **The float is therefore a permanent ~$120–160k draw** (the $80k shortfall × the 1.5–2.0 month cycle). That is the standing cost of a bolívar-led growth engine.

---

## 4. The 6-month projection (June–December 2026)

**Assumptions:** total MRR grows 5%/month with all growth landing in bolívars (USD MRR held flat at $40k); implementation fees flat at $7k/month in Bs; expenses flat at $120k USD + $12k Bs; conversion cycle 45–60 days.

| Month | Revenue | USD shortfall (gap − converted) | **Net** | Cumulative |
|---|---:|---:|---:|---:|
| **Jun** (today) | $102k | $30k | −$30k | −$30k |
| Jul | $107k | $25k | −$25k | −$55k |
| Aug | $112k | $20k | −$20k | −$76k |
| Sep | $117k | $15k | −$15k | −$91k |
| Oct | $122k | $10k | −$10k | −$100k |
| Nov | $128k | $4k | −$4k | **−$104k** |
| **Dec** | $134k | $0 | **+$2k** | −$102k |

- **Breakeven ≈ December 2026** (~6 months out).
- **Total cash burned to get there ≈ $104k**, bottoming end of November.

### When the credit line gets tapped

Starting from an estimated ~$450k in USD cash — which, against a $400k reserve, leaves only ~$50k of free operating cash today:

| Month | Free cash above reserve | Line drawn (bridge) |
|---|---:|---:|
| Jun | $50k → $20k | $0 |
| **Jul** | $20k → $0 | **$5k ← first draw** |
| Aug | $0 | $26k |
| Sep | $0 | $41k |
| Oct | $0 | $50k |
| **Nov** | $0 | **$54k ← peak** |
| Dec | begins repaying | $52k |

- **First draw: July 2026.** **Peak bridge draw ~$54k in November**, self-repaying once cash-positive.
- The first-draw date is sensitive to the actual current cash balance — every extra $25k of starting buffer delays it ~1 month.

### Total facility required

The bridge draw and the permanent conversion float stack:

| | 45-day cycle | 60-day cycle |
|---|---:|---:|
| Peak bridge draw | ~$54k | ~$54k |
| Conversion float (permanent) | ~$120k | ~$160k |
| **Peak total facility use** | **~$170k** | **~$212k** |

**A $250k line covers the peak under both cycle lengths, with the reserve untouched.**

### Caveats that argue for the top of the range

- **Lumpy collections.** Many customers pay quarterly or semiannually. Normalizing to monthly hides the troughs — in a dry month, USD bills still hit but bolívar inflow is thin, lengthening the effective cycle and pushing the float toward the 60-day figure. **Size the line to the 60-day case ($250k), not the average.**
- **Slower growth or delayed breakeven** extends the bridge and keeps the line drawn longer — this is precisely what the equity buffer insures.

---

## 5. The financing decision — pros and cons

### Credit line (revolver, ~$250k, US entity)

**Pros**
- Non-dilutive — preserves ownership.
- Pay only for what's drawn.
- The *correct* instrument for a permanent, revolving working-capital float — matches a recurring need with a revolving facility.
- Also absorbs the temporary bridge to breakeven.

**Cons**
- Not yet in place — must be secured, with the US entity as borrower; may carry covenants, a rate, or a guarantee.
- Drawn amounts must be serviced; if breakeven slips badly, a maxed line while still burning is dangerous (this is where equity is the backstop).
- Sizing risk — if collection lumpiness runs the float past expectations, $250k could tighten.

### Equity (SAFE, ~$250–400k, now)

**Pros**
- **Removes the existential stress directly** — it rebuilds a real buffer above the reserve, which the company does not have today.
- **Insurance** against the downside scenarios (slower growth, delayed breakeven, a bad lumpy month, a smaller-than-hoped line).
- **Raising from strength** — a clean story with a credible ~6-month breakeven path prices better than a raise done under pressure later.
- Permanent capital, no repayment schedule.
- Optional upside: a portion can fund growth that increases USD-denominated revenue, which structurally shrinks the $80k gap.

**Cons**
- **Dilution** — and if growth holds and the line proves sufficient, some of it may not have been strictly necessary.
- **Timing of valuation** — proving breakeven first could make later capital cheaper; raising now prices off today's metrics.
- Founder time and focus.
- Risk of raising more than is deployed ("dead equity").

### Why the combination is the financially smart answer

- The line handles the **predictable, revolving** piece cheaply and without dilution.
- The equity handles the **buffer and the downside** — the part that, if unfunded, forces stressful decisions.
- Splitting the job this way means **the reserve is never touched, the line is never maxed under duress, and a bad month is absorbed rather than a crisis.** That is the definition of a plan you track rather than worry about.

---

## 6. Recommended structure and sequence

1. **Now — secure the ~$250k credit line** on the US entity. Until it is committed, the reserve floor is effectively $480k (not $400k), because the company would otherwise dip into it by July.
2. **Now — raise a ~$250–400k SAFE**, framed precisely: *"We run on a $400k locked reserve and a 2–3 month operating buffer; this round provisions the buffer and insures the path to breakeven, so the reserve is never what stands between us and payroll."* Clean, disciplined, fundable.
3. **Target end-state liquidity:** ~$400k reserve (locked) + ~$150–250k operating buffer + a $250k line available. Roughly $800–900k of total liquidity, of which only $400k is untouchable — comfortable under the base case and resilient under the downside.

### The two structural levers to pursue in parallel (they shrink everything)

Both reduce the permanent float, the financing need, and the FX exposure at once:
1. **Grow USD-denominated revenue.** The $80k monthly shortfall is pinned only because USD revenue is flat. Pricing more customers in USD lifts the ceiling down.
2. **Smooth payment cadence toward monthly.** Migrating quarterly/semiannual payers to monthly billing flattens the collection troughs, shortening the effective conversion cycle and shrinking the float.
3. *(Secondary)* **Shift cost base toward bolívars** where sensible — bolívar-paid local hires reduce the $120k USD obligation from the cost side.

---

## 7. The tracking dashboard (so this runs without stress)

Review monthly. The plan is healthy as long as these stay in range; the triggers tell you exactly when to act.

| Metric | Why it matters | Trigger to act |
|---|---|---|
| USD cash position | The binding constraint | Approaches reserve + 1 month buffer → draw the line |
| Trailing-3-month net burn | The real burn | Breaches $40k cap for 2 months → cut or fund |
| % of revenue in USD | Shrinks the structural gap | Falling → push USD-priced sales |
| Conversion cycle (days) | Drives the float size | Lengthening → smooth cadence / convert more often |
| Credit line drawn | Capacity remaining | Exceeds 60% → open or accelerate the equity round |
| Breakeven tracking | Plan vs. reality | Slips past December → activate downside (equity) plan |

**The single most important number to drive down over time is the $80k monthly USD gap** — via more USD revenue and a lower USD cost base. Everything else (line size, float, FX exposure) shrinks with it.

---

## 8. Open items to confirm (turns estimates into facts)

- **Current USD cash balance** — sets the exact first-draw date (using a ~$450k estimate).
- **Payment-cadence mix** (share of MRR billed monthly vs. quarterly vs. semiannual) — sets how far toward the 60-day float the business really runs.
- **Days-to-collect and days-to-convert** — the actual conversion cycle length.
- **Current % of revenue in USD** — confirmed at ~40% of MRR; track monthly.
- **Credit line terms** — committed amount, rate, covenants, borrowing entity.

---

## Supporting detail

The models behind each section live in companion documents:
- Reserve / cap / operating-cash policy and the currency-deficit framing
- Reserve + line + equity scenario stress-test across growth speeds
- USD-liquidity float sizing (the formula behind the conversion float)
- Currency cash calendar and matching model (revenue & expenses by currency)
- The 6-month numerical projection (the source of §4)
