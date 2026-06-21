---
title: Currency Cash Projection — 6 Months @ 5% MoM Total MRR (all growth in Bs), June–Dec 2026
tags: [finance, treasury, fx, projection, working-capital]
updated: 2026-06-09
status: draft
---

# Currency Cash Projection — 6 Months, 5% MoM Total MRR (all growth in Bs)

The real picture, with Luis's confirmed inputs (2026-06-09). Operationalizes `[[currency-cash-calendar-model]]`.

## Assumptions (locked for this run)

| Input | Value |
|---|---|
| USD MRR (month 0) | **$40k**, held **flat** |
| Bs MRR (month 0) | **$55k** |
| Total MRR growth | **5% MoM** — **all growth lands in Bs** (USD MRR stays $40k) |
| Implementation fees | **$7k/mo, paid in Bs**, held flat |
| USD expenses | **$120k/mo**, flat |
| Bs expenses | **$12k/mo**, flat |
| Total expenses | **$132k/mo**, flat |
| Bs→USD conversion cycle | **45–60 days** |
| FX spread | **N/A** (ignored this run) |
| Working rate | **N/A** (Bs shown as USD-equivalent) |
| Cadences (qtrly / 6-mo) | normalized to monthly — see lumpiness caveat |
| Starting USD cash | ~$450k est. → **~$50k free above the $400k reserve** ⚠️ refresh |

> **Structural feature of this run:** USD revenue is flat and USD expense is flat → the **USD gap is pinned at $80k every single month**. The only thing that closes it is Bs growth being converted. Month 0 = **June 2026**.

---

## The monthly model ($000s)

| Month | Total MRR | USD rev | Bs rev (MRR+impl) | USD gap | Bs surplus | Convert | USD residual | **Net** | Cum. net |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Jun** (today) | 95.0 | 40 | 62.0 | 80 | 50.0 | 50.0 | **30.0** | −30.0 | −30.0 |
| Jul | 99.8 | 40 | 66.8 | 80 | 54.8 | 54.8 | 25.3 | −25.3 | −55.3 |
| Aug | 104.7 | 40 | 71.7 | 80 | 59.7 | 59.7 | 20.3 | −20.3 | −75.5 |
| Sep | 110.0 | 40 | 77.0 | 80 | 65.0 | 65.0 | 15.0 | −15.0 | −90.5 |
| Oct | 115.5 | 40 | 82.5 | 80 | 70.5 | 70.5 | 9.5 | −9.5 | −100.1 |
| Nov | 121.3 | 40 | 88.3 | 80 | 76.3 | 76.3 | 3.8 | −3.8 | **−103.8** |
| **Dec** | 127.3 | 40 | 94.3 | 80 | 82.3 | 80.0 | 0.0 | **+2.3** | −101.5 |

- **USD gap = $80k flat** ($120 USD exp − $40 USD rev). Never moves — that's the all-Bs-growth signature.
- **Convert = min(gap, surplus).** You convert *every* available bolívar through November and stay short; in December Bs surplus ($82.3k) finally exceeds the $80k gap → first leftover Bs.
- **USD residual = the real burn**, shrinking $30k → $0 as Bs growth feeds conversion.

### The arc
- **Today (Jun):** convert ~$50k/mo, **$30k/mo short in USD** even after converting everything.
- **Breakeven ≈ December 2026 (month 6).** Net turns +$2.3k. (Total MRR at 5% on a $95k base adds enough absolute Bs to close a flat $80k USD gap in 6 months — that's why this beats the "5% on Bs-only" path, which slipped to ~Mar 2027.)
- **Cumulative cash burned to breakeven ≈ $104k**, bottoming end of November.

---

## ★ Exactly when you tap the line

Free cash above the $400k reserve starts at **~$50k**. Burn draws it down; once it hits zero, you draw the **line** instead of touching the reserve.

| Month | Burn | Free cash (start $50k) | **Line draw (burn bridge)** |
|---|---:|---:|---:|
| Jun | 30.0 | 50 → 20 | $0 |
| **Jul** | 25.3 | 20 → 0 | **$5.3k ← FIRST TAP** |
| Aug | 20.3 | 0 | $25.5k |
| Sep | 15.0 | 0 | $40.5k |
| Oct | 9.5 | 0 | $50.1k |
| **Nov** | 3.8 | 0 | **$53.8k ← peak** |
| Dec | +2.3 | begins repaying | $51.5k |

- **First draw: July 2026**, ~$5k.
- **Peak burn-bridge draw: ~$54k in November**, then it self-repays from December onward as you turn cash-positive.
- **Sensitivity:** every extra $25k of starting cushion above reserve pushes the first tap ~1 month later. So the first-tap date hinges on the *actual* current balance — refresh it.

### …plus the conversion float underneath

The burn bridge isn't the only USD draw. The 45–60 day cycle means you've always fronted USD that's still waiting on Bs to convert. Float ≈ `convert × (cycle ÷ 30)`:

| Month | Convert | Float @ 45-day | Float @ 60-day |
|---|---:|---:|---:|
| Jun | 50.0 | 75.0 | 100.0 |
| Sep | 65.0 | 97.5 | 129.9 |
| **Dec** (plateau) | 80.0 | **120.0** | **160.0** |

Because growth is all-Bs, convert volume climbs to the $80k gap ceiling and **plateaus there** — so the float settles at a **permanent ~$120–160k** (it caps at the USD gap, doesn't grow forever).

---

## Total facility use vs. the $250k line

The two draws stack at the worst point (Nov–Dec):

| | @ 45-day cycle | @ 60-day cycle |
|---|---:|---:|
| Peak burn-bridge draw | ~$54k | ~$54k |
| Conversion float (plateau) | ~$120k | ~$160k |
| **Peak total facility use** | **~$170k** | **~$212k** |
| vs. $250k line | ✅ ~$80k headroom | ✅ ~$38k headroom |

**The $250k line covers it under both cycle lengths, and the $400k reserve is never touched.** The structure holds for this scenario.

### But watch the permanent piece
After December the burn bridge repays — but the **~$120–160k conversion float is permanent** (it's the cost of running flat-$40k USD revenue against $120k USD expense via Bs conversion). At a 60-day cycle that's ~$160k of the $250k line drawn *forever*, leaving ~$90k of headroom. A bad lumpy month (below) can eat that fast.

---

## ⚠️ Two caveats that push you toward the top of the range

1. **Lumpiness (quarterly / 6-mo payers).** Normalizing to monthly hides it. A quarterly client pays 3× in one month, then nothing for two — but your $120k USD obligations hit *every* month. In the dry months you convert less / wait longer → effective cycle lengthens → float spikes toward (or past) the 60-day column. **Size to the 60-day case and pull the real cadence mix before locking the line.** Migrating payers to monthly (cobros work) directly shrinks this.

2. **All-Bs growth pins the USD gap at $80k forever.** This is the structural cost of a VES-led growth engine: you will *always* convert ~$80k/mo and carry ~$120–160k of float. The only levers that lower the permanent draw:
   - **Grow USD-denominated revenue** (unpins the $80k gap from the top)
   - **Cut the USD cost base** — shift US payroll toward Bs-paid VE hires (lowers the $120k)
   - **Shorten the cycle** (45-day vs 60-day = ~$40k less float)

---

## Bottom line

- **Breakeven ≈ December 2026** at 5% MoM total MRR (all-Bs).
- **First line tap: July 2026** (~$5k); **peak burn draw ~$54k in November**, self-repaying after.
- **Permanent conversion float ~$120–160k** sits under that — the standing cost of the currency mismatch.
- **Peak total facility ~$170–212k → a $250k line holds with headroom, reserve untouched.** Lean to the top because of payment lumpiness.
- **The $80k USD gap is pinned** until you grow USD revenue or cut USD costs — that's the one structural number to attack if you want the line (and the FX exposure) to shrink over time.

## Related
- [[currency-cash-calendar-model]] — the framework + fillable calendars
- [[usd-liquidity-gap-sizing]] — the float formula
- [[scenario-reserve-credit-equity-2026-06]] — reserve + line + equity structure
- [[financial-policy-non-negotiables]] — the policy frame
- [[ar-and-cobros-2026-05]] — cadence-smoothing + days-to-collect lever
