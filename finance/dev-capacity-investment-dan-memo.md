---
title: Should we hire to accelerate revenue? — finance scenarios for Dan
tags: [finance, hiring, runway, projections, ai, 10x]
updated: 2026-05-26
status: draft
---

# Should we hire to accelerate revenue? — pre-read for Dan

**Draft — Luis to review before sending.** Pre-read for our finance meeting ahead of team planning. The goal is to agree on how to think about this *before* we turn planning into headcount decisions.

## The question, in plain terms

We have a strong product roadmap, but it's moving slower than we'd like because so much of the team's time goes to maintaining our direct bank connections. The question on the table: **should we spend an extra ~$20–30k/mo on devs and PMs to ship faster and grow revenue faster — and do we fund that from cash or raise a small round?**

To answer it I built out a set of scenarios. This memo walks through what they say.

## How to read the numbers (key terms)

A few definitions so the tables make sense:

- **MRR** — monthly recurring revenue from subscriptions. This is our stable base.
- **Implementation fees** — one-time setup/onboarding fees we charge new customers. Lumpy, tied to how many new logos we land and can onboard.
- **Monthly net** — total revenue minus all costs that month. Negative = burning cash; positive = profitable that month.
- **Runway** — how many months of cash we'd have left if that month's burn rate held. "∞" means we're cash-positive that month.

Every scenario starts from **$480k cash** and assumes **~$135k/mo of expenses** (today's level, held flat). The only things that change between scenarios are (a) how fast revenue grows and (b) whether we add the new devs.

### The revenue drivers

Each scenario uses one of four growth assumptions:

| Driver | Subscription growth | Implementation fees | What it means |
|---|---|---|---|
| **Baseline** | +$7k MRR/mo | ~$10k/mo | Our current organic trajectory, no new bets |
| **AI revenue** | +$10k MRR/mo | ~$13k/mo | The extra growth we'd expect from shipping AI capabilities (≈ +$3k/mo more than baseline) |
| **AI + Payments** | +$13k MRR/mo (from Sep) | ~$16k/mo | AI revenue *plus* a second product line (payments) adding its own revenue engine |
| **Stall** | +$3.5k MRR/mo | ~$7.5k/mo | Growth roughly halves — churn, FX, or soft demand |

### The hiring cost

Where a scenario includes **new devs**, the cost ramps as we hire: **$10k (Jun) → $15k (Jul) → $20k (Aug) → $25k (Sep)**, then holds at **$25k/mo**. Phased, so we can slow down or stop partway.

## Where we stand today (May 2026)

| | $/mo |
|---|---:|
| Subscriptions (recurring, after removing churned accounts) | ~$98k |
| Implementation fees (this month) | $16.5k |
| **Total revenue** | **~$114.5k** |
| Expenses | ~$135k |
| **Burn** | **~$20.5k** |
| Cash | $480k |

That's 20+ months of runway. We're in a comfortable spot — this is operating revenue only, nothing counted from intercompany.

## The core insight: can we deliver what AI brings in?

Here's the thing the scenarios kept surfacing. **AI can create new revenue — but only if we can deliver against it.** New AI-driven customers still need the product built out and onboarded. If demand arrives faster than the team can build and onboard, we win deals and then *lose* them: customers churn because we couldn't keep up, and the implementation fees dry up because we can't take on new work.

So the real question isn't "will AI create demand?" It's **"do we have the delivery capacity to keep what AI brings in?"** That's what the new-devs decision is actually about — not generic "more velocity," but the capacity to hold onto revenue we've already spent to win.

## The scenarios (12-month view, May 2026 → Apr 2027)

Month-by-month tables are in the appendix. Summary:

| Scenario | Hiring? | Revenue driver | Goes profitable | Lowest cash | Cash Apr '27 | Monthly net Apr '27 | Runway |
|---|---|---|---|---:|---:|---:|---|
| **No new investment** | | | | | | | |
| 1 · Baseline — current trajectory | no | Baseline | Sep '26 | $420k | $575k | +$50k/mo | safe |
| 2 · Growth stalls | no | Stall | ~Feb '27 | $350k | $357k | +$9k/mo | safe |
| **AI revenue, no new hires** | | | | | | | |
| 3 · AI revenue — team keeps up *(optimistic)* | no | AI revenue | Aug '26 | $442k | $770k | +$86k/mo | safe |
| 4 · AI revenue — team can't keep up *(demand leaks)* | no | bump → churn | ~May '27 | $358k | $357k | ~breakeven | cash-safe, but revenue lost |
| **AI revenue + new devs** | | | | | | | |
| 5 · AI revenue + new devs | $25k/mo | AI revenue | Oct '26 | $394k | $550k | +$61k/mo | safe |
| 6 · AI + Payments + new devs | $25k/mo | AI + Payments | Oct '26 | $400k | $655k | +$88k/mo | safe |
| 7 · New devs, revenue stays baseline | $25k/mo | Baseline | Jan '27 | $322k | $355k | +$25k/mo | safe |
| 8 · **New devs + growth stalls (danger)** | $25k/mo | Stall | ~Sep '27 | **$137k & falling** | $137k | −$16k/mo | **stuck ~8mo** |
| **Staged (recommended)** | | | | | | | |
| 9 · Stage in $10k now, ramp in Sep if AI works | $10k→$25k | AI revenue | Oct '26 | $409k | $565k | +$61k/mo | safe |

The big takeaway: **we survive in every scenario except one.** The business isn't fragile. The whole decision comes down to a few specific comparisons below.

## What the scenarios tell us

### 1. New devs are about *keeping* the revenue AI brings in

Compare what happens when AI creates demand and we *can't* deliver (Scenario 4) vs. when we add the capacity to deliver (Scenarios 5–6):

| Path | Apr '27 subscriptions | Apr '27 total rev | Monthly net | Customer base |
|---|---:|---:|---:|---|
| AI revenue, **no devs** — demand leaks (S4) | ~$126k | ~$134k | ~breakeven | churned, hard to win back |
| AI revenue **+ devs** — we deliver (S5) | $208k | $221k | +$61k/mo | healthy |
| AI + Payments **+ devs** (S6) | $232k | $248k | +$88k/mo | healthy, compounding |

In plain terms: **$25k/mo of extra capacity protects roughly $60–75k/mo of revenue that we'd otherwise lose** — and that gap grows over time. The devs roughly pay for themselves 2–3x over by next year, and more after. That's the case for hiring.

(Scenario 3 — "AI revenue, team keeps up with no new hires" — looks like the best outcome on paper. But it assumes the current team can build and onboard *all* the new AI demand with zero extra help. That's the optimistic edge of the range; Scenario 4 is the more realistic version of "AI revenue without hiring.")

### 2. There's exactly one dangerous outcome — and it's avoidable

The only scenario that puts us at risk is Scenario 8: we hire the devs *and* growth stalls anyway. Same disappointing revenue as Scenario 2 — the only difference is the dev spend:

| | Cash Apr '27 | Runway | What happens |
|---|---:|---|---|
| Growth stalls, **no devs** (S2) | $357k | safe, >18 months | drifts gently to breakeven |
| Growth stalls, **+ devs** (S8) | $137k | stuck ~8 months | keeps draining, dips below $100k in Q3 '27 |

So hiring turns a perfectly safe stall into the one scary outcome. The fix isn't "don't hire" — it's **don't ride a losing bet**: hire in a way we can unwind quickly (contractors/probation first), and agree up front on a trigger to stop. If by **August** new MRR is tracking +$3.5k instead of +$10k, we freeze the ramp. The phased hiring cost *is* the safety valve.

### 3. Judge this over 18–24 months, not 8

Hiring costs land immediately; the revenue they unlock shows up later. Even the best hiring scenario (S6) ends *December* with less cash than doing nothing — then pulls ahead in Jan–Feb 2027 as the new revenue compounds. If we only look at this year, we'll undersell the exact decision we're making. The 12-month view above already shows the crossover.

## The balanced path (recommended)

There's a version of this that captures the upside while keeping the downside tiny: **commit only the first $10k/mo now, hold it through the summer, and use September as a decision gate** — by then we'll have ~3 months of evidence on whether AI is actually lifting revenue.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Total revenue | 114.5 | 121 | 131 | 141 | 151 | 161 | 171 | 181 | 191 | 201 | 211 | 221 |
| New devs | — | 10 | 10 | 10 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −24 | −14 | −4 | −9 | +1 | +11 | +21 | +31 | +41 | +51 | +61 |
| Cash | 480 | 459.5 | 435.5 | 421.5 | 417.5 | 408.5 | 409.5 | 420.5 | 441.5 | 472.5 | 513.5 | 564.5 |

At the September gate:

- **If AI is working** (demand is real and growing) — ramp to the full team ($25k/mo). We *have* to, or we start losing the demand we won (Scenario 4). By then the revenue is proven and largely paying for it: the path stays profitable from October and never drops below ~$409k cash.
- **If AI isn't working** — stop. We've risked only ~$30k total (Jun–Aug), and we fall back to the baseline trajectory, which is profitable on its own by September.

The striking part: **staging in costs us nothing versus committing the full team in June.** Same end-state team, same revenue — but because we defer the bigger spend until we have proof, this path actually ends with *more* cash than hiring everyone up front (~$565k vs. ~$550k in Scenario 5) and a higher cash floor. There's no version where committing the full ramp in June beats staging. The only mistake to avoid is the opposite: seeing the demand work in September and *not* ramping — that's how we'd leak it.

## My recommendation / what I'd want us to align on

1. **Do the staged path above.** Add $10k/mo now, measure through August, and decide in September: ramp if AI is working, stop if it isn't.
2. **Get the free AI lift first.** How much faster can the *current* team move just by using AI tooling, before we add anyone? Let's bank that and then size what's genuinely capacity-constrained.
3. **Frame the hire as capacity to hold revenue, tied to the bottleneck.** The thesis: get new/mid devs onto direct-connection maintenance so senior eng can move to the payments/cobros roadmap (the 10x bet).
4. **Bring delivery capacity online *with* the demand push, not after.** If we turn on AI-driven demand before we can deliver, we get Scenario 4 — we win customers and lose them. So line up capacity we can ramp fast on signal.
5. **Hire in a structure we can unwind.** Severance isn't free — contractors/probation keep the September stop-or-go option real.
6. **Look 18–24 months out** when we evaluate this.
7. **The raise is optional.** We can fund this from cash in every scenario except the un-cuttable stall. A $250–300k round at $10m+ (~3% dilution, raised from strength) is only needed if we commit to hires we can't unwind, or want to keep the cash cushion fully intact. It's not a precondition.

## Assumptions worth challenging

- Expenses held flat at $135k/mo — no cost creep, no FX shock. (A chunk of our revenue is in bolívares; getting it to USD at scale carries real risk that isn't separately modeled here.)
- Growth shown as flat monthly dollar increases, not compounding percentages.
- No intercompany inflows counted — this is operating-only.
- Implementation fees rise and fall with how many new customers we land and can onboard.

## What I need from you (Dan) before the meeting

- **The key question:** can direct-connection maintenance actually be handed to new/mid devs, or is it senior-only knowledge? If new hires can't take it off senior eng, the whole thesis falls apart.
- **Throughput:** roughly how much new product/onboarding work can the current team absorb, vs. how much an AI push would generate? That's what decides whether we're really in the "deliver" case (S5/S6) or the "leak" case (S4).
- Realistic ramp time for a new dev to be productive in the codebase, plus hiring lead time — that's the sequencing risk in point 3.

## Related

- [[analysis-may-2026]] — underlying burn/revenue/runway analysis
- [[ar-and-cobros-2026-05]] — the cobros/payments work the hires would accelerate
- [[cash-flow-king/index|cash-flow-king/]] — budget-vs-actual baseline

---

## Appendix — full 12-month tables

Cash = balance at the **start of each month** (after prior months' net); May = $480k. Runway = cash ÷ that month's burn if it held; **∞** = cash-positive that month. All figures $k.

### 1 · Baseline — current trajectory (no hires)

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 105 | 112 | 119 | 126 | 133 | 140 | 147 | 154 | 161 | 168 | 175 |
| Implementation fees | 16.5 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Total revenue | 114.5 | 115 | 122 | 129 | 136 | 143 | 150 | 157 | 164 | 171 | 178 | 185 |
| Monthly net | −20.5 | −20 | −13 | −6 | +1 | +8 | +15 | +22 | +29 | +36 | +43 | +50 |
| Cash | 480 | 459.5 | 439.5 | 426.5 | 420.5 | 421.5 | 429.5 | 444.5 | 466.5 | 495.5 | 531.5 | 574.5 |
| Runway | 23 | 23 | 34 | 71 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ |

### 2 · Growth stalls (no hires)

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 101.5 | 105 | 108.5 | 112 | 115.5 | 119 | 122.5 | 126 | 129.5 | 133 | 136.5 |
| Implementation fees | 16.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 |
| Total revenue | 114.5 | 109 | 112.5 | 116 | 119.5 | 123 | 126.5 | 130 | 133.5 | 137 | 140.5 | 144 |
| Monthly net | −20.5 | −26 | −22.5 | −19 | −15.5 | −12 | −8.5 | −5 | −1.5 | +2 | +5.5 | +9 |
| Cash | 480 | 459.5 | 433.5 | 411 | 392 | 376.5 | 364.5 | 356 | 351 | 349.5 | 351.5 | 357 |
| Runway | 23 | 18 | 19 | 22 | 25 | 31 | 43 | 71 | 234 | ∞ | ∞ | ∞ |

### 3 · AI revenue — team keeps up, no hires (optimistic)

Assumes the current team delivers all the new AI demand with no extra help.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 108 | 118 | 128 | 138 | 148 | 158 | 168 | 178 | 188 | 198 | 208 |
| Implementation fees | 16.5 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| Total revenue | 114.5 | 121 | 131 | 141 | 151 | 161 | 171 | 181 | 191 | 201 | 211 | 221 |
| Monthly net | −20.5 | −14 | −4 | +6 | +16 | +26 | +36 | +46 | +56 | +66 | +76 | +86 |
| Cash | 480 | 459.5 | 445.5 | 441.5 | 447.5 | 463.5 | 489.5 | 525.5 | 571.5 | 627.5 | 693.5 | 769.5 |
| Runway | 23 | 33 | 111 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ |

### 4 · AI revenue — team can't keep up, no hires (demand leaks)

AI brings demand for ~2 months, then onboarding breaks (fees fall first), and customers churn out with a lag. Tail months are illustrative.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 108 | 117 | 121 | 121 | 118 | 116 | 115 | 117 | 120 | 123 | 126 |
| Implementation fees | 16.5 | 13 | 11 | 8 | 6 | 6 | 5 | 5 | 6 | 6 | 7 | 8 |
| Total revenue | 114.5 | 121 | 128 | 129 | 127 | 124 | 121 | 120 | 123 | 126 | 130 | 134 |
| Monthly net | −20.5 | −14 | −7 | −6 | −8 | −11 | −14 | −15 | −12 | −9 | −5 | −1 |
| Cash | 480 | 459.5 | 445.5 | 438.5 | 432.5 | 424.5 | 413.5 | 399.5 | 384.5 | 372.5 | 363.5 | 358.5 |
| Runway | 23 | 33 | 64 | 73 | 54 | 39 | 30 | 27 | 32 | 41 | 73 | 359 |

The runway row never breaks, so this isn't a *cash* problem — the cost is the lost revenue and churned customers. We spend to win demand, then can't hold it, and limp into 2027 shrinking instead of growing.

### 5 · AI revenue + new devs

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 108 | 118 | 128 | 138 | 148 | 158 | 168 | 178 | 188 | 198 | 208 |
| Implementation fees | 16.5 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| Total revenue | 114.5 | 121 | 131 | 141 | 151 | 161 | 171 | 181 | 191 | 201 | 211 | 221 |
| New devs | — | 10 | 15 | 20 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −24 | −19 | −14 | −9 | +1 | +11 | +21 | +31 | +41 | +51 | +61 |
| Cash | 480 | 459.5 | 435.5 | 416.5 | 402.5 | 393.5 | 394.5 | 405.5 | 426.5 | 457.5 | 498.5 | 549.5 |
| Runway | 23 | 19 | 23 | 30 | 45 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ |

### 6 · AI + Payments + new devs

AI revenue plus a second product line (payments) coming online from September.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 108 | 118 | 128 | 141 | 154 | 167 | 180 | 193 | 206 | 219 | 232 |
| Implementation fees | 16.5 | 13 | 13 | 13 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| Total revenue | 114.5 | 121 | 131 | 141 | 157 | 170 | 183 | 196 | 209 | 222 | 235 | 248 |
| New devs | — | 10 | 15 | 20 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −24 | −19 | −14 | −3 | +10 | +23 | +36 | +49 | +62 | +75 | +88 |
| Cash | 480 | 459.5 | 435.5 | 416.5 | 402.5 | 399.5 | 409.5 | 432.5 | 468.5 | 517.5 | 579.5 | 654.5 |
| Runway | 23 | 19 | 23 | 30 | 134 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ |

### 7 · New devs, but revenue stays at baseline

We hire, but the extra capacity doesn't lift growth above the baseline rate.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 105 | 112 | 119 | 126 | 133 | 140 | 147 | 154 | 161 | 168 | 175 |
| Implementation fees | 16.5 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Total revenue | 114.5 | 115 | 122 | 129 | 136 | 143 | 150 | 157 | 164 | 171 | 178 | 185 |
| New devs | — | 10 | 15 | 20 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −30 | −28 | −26 | −24 | −17 | −10 | −3 | +4 | +11 | +18 | +25 |
| Cash | 480 | 459.5 | 429.5 | 401.5 | 375.5 | 351.5 | 334.5 | 324.5 | 321.5 | 325.5 | 336.5 | 354.5 |
| Runway | 23 | 15 | 15 | 15 | 16 | 21 | 33 | 108 | ∞ | ∞ | ∞ | ∞ |

### 8 · New devs + growth stalls (the danger case)

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 101.5 | 105 | 108.5 | 112 | 115.5 | 119 | 122.5 | 126 | 129.5 | 133 | 136.5 |
| Implementation fees | 16.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 | 7.5 |
| Total revenue | 114.5 | 109 | 112.5 | 116 | 119.5 | 123 | 126.5 | 130 | 133.5 | 137 | 140.5 | 144 |
| New devs | — | 10 | 15 | 20 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −36 | −37.5 | −39 | −40.5 | −37 | −33.5 | −30 | −26.5 | −23 | −19.5 | −16 |
| Cash | 480 | 459.5 | 423.5 | 386 | 347 | 306.5 | 269.5 | 236 | 206 | 179.5 | 156.5 | 137 |
| Runway | 23 | 13 | 11 | 10 | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 9 |

Runway falls to ~8 months and **stays stuck** — the stall means we can't climb out before cash runs low (dips below $100k in Q3 '27 before slowly recovering, with no margin for any other bad news). This is the only outcome that forces a raise-from-weakness or a hard cut, which is exactly why we hire in a way we can unwind and set a stop rule in advance.

### 9 · Staged — $10k now, ramp to $25k in Sep if AI works (recommended)

Shows the "AI is working, so we ramp" branch. If AI isn't working at the September gate, we stop the spend and the path reverts toward Scenario 1.

| | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar | Apr |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Subscriptions (MRR) | 98 | 108 | 118 | 128 | 138 | 148 | 158 | 168 | 178 | 188 | 198 | 208 |
| Implementation fees | 16.5 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| Total revenue | 114.5 | 121 | 131 | 141 | 151 | 161 | 171 | 181 | 191 | 201 | 211 | 221 |
| New devs | — | 10 | 10 | 10 | 25 | 25 | 25 | 25 | 25 | 25 | 25 | 25 |
| Monthly net | −20.5 | −24 | −14 | −4 | −9 | +1 | +11 | +21 | +31 | +41 | +51 | +61 |
| Cash | 480 | 459.5 | 435.5 | 421.5 | 417.5 | 408.5 | 409.5 | 420.5 | 441.5 | 472.5 | 513.5 | 564.5 |
| Runway | 23 | 19 | 31 | 105 | 46 | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ | ∞ |

Versus hiring the full team in June (Scenario 5): same revenue and same end-state team, but staging holds a **higher cash floor ($409k vs. $394k)** and **ends with more cash ($565k vs. $550k)** — and keeps the option to stop in September for only ~$30k at risk.
