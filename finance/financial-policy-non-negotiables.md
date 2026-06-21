---
title: Financial Policy — The Non-Negotiables
tags: [finance, runway, treasury, policy]
updated: 2026-06-09
status: draft
---

# Financial Policy — The Non-Negotiables

The point of this doc: stop running finances by feel. Set the **hard rules** the business operates under no matter what — how much cash is untouchable, what we cap burn at, how much operating cash we hold, and how we cover the gap between expenses and when receivables actually become spendable USD.

These are meant to be *constraints*, not targets. A target is something we hope to hit. A non-negotiable is a line we don't cross — and if we're about to, that itself triggers an action (cut or fund).

> **Working numbers, not final.** Built on `[[analysis-may-2026]]` + `[[cash-flow-king/index|cash-flow-king]]`. Several inputs flagged ⚠️ need a real number before this locks — see [Open data to confirm](#open-data-to-confirm).

---

## The five questions, answered

| # | Question | Answer |
|---|---|---|
| 1 | How much cash untouchable? | **$480k**, held in USD, board-locked |
| 2 | Burn cap? | **$40k/mo net**, measured trailing-3-month |
| 3 | How much operating cash? | **2–3 months gross outflow ≈ $250–375k** on top of the reserve |
| 4 | Credit line / financing vs. raise equity? | **Both, sequenced** — revolver for the timing/FX gap, equity to fund the float. See [pros/cons](#4--credit-vs-financing-vs-equity) |
| 5 | What's the real monthly deficit? | Not the ~$30k accounting net — it's a **USD-liquidity gap** driven by the AR→payment→USD-conversion cycle. See [the real deficit](#the-real-deficit-the-only-number-that-actually-runs-the-business) |

---

## 1 — Untouchable reserve: $480k

- **Rule:** `burn cap ($40k) × 12 months = $480k`. This is the floor. We do not operate below it without a board-level decision.
- **Held in USD.** This is non-negotiable and it's the whole point — see the deficit section. Our binding constraint is USD liquidity, not total FX-adjusted net worth. A reserve denominated in Bs is not a reserve.
- **Physically separated.** Its own account, not commingled with operating cash, so "untouchable" is structural, not willpower.
- **Only touched on a defined trigger** (revenue collapse + inability to raise). Touching it = the company is in a declared crisis, not a bad month.

**What "12 months no matter what" actually means.** It does *not* mean 12 months if revenue goes to zero — that's ~$1.5M (12 × gross $125k) and we shouldn't hold that idle. It means **12 months at a defined stress burn, assuming we cut discretionary spend if revenue stalled.** Write the stress scenario down (next section). The $40k cap *is* that stress burn.

## 2 — Burn cap: $40k/mo net

- **Measured on trailing-3-month net burn**, not single months. April was −$98k and May 1–11 was +$20k — single months are noise (Multiplier timing, payroll cycles, tax bombs). The 3-month average is the truth.
- **Net, not gross.** Today: rev ~$95k vs recurring outflow ~$120–127k → net burn ~$24–32k/mo. So $40k is a **ceiling with ~$8–15k of headroom**, not our run rate. Good — a cap should have slack.
- **Breaching the cap two months running = forced action**: renegotiate, cut, or fund. Not a discussion — a trigger.

**The stress-burn / cut list (define once, keep current).** If revenue stalls, what comes out to hold burn at/under $40k? Candidates, ranked by $/mo:
- Multiplier renegotiation ($30k/mo — biggest single line, structural)
- Contractor ROI review ($21k/mo post-severance)
- Million Web scope ($12k/mo)
- SaaS sprawl (~$10k/mo combined)

Easily $30–50k/mo of flex exists. That's what makes the $40k cap a *defensible* stress number rather than wishful.

## 3 — Operating cash: 2–3 months gross ≈ $250–375k

- **Separate from the reserve, on top of it.** Reserve is the floor you never touch; operating float is the working buffer that absorbs normal timing swings — the gap between when expenses hit and when receivables clear into USD.
- **Sized on *gross* outflow (~$125k/mo)**, not net — because in a timing crunch you owe the full payroll, not the net-of-revenue number.
- **Why 2–3 months:** that's the realistic length of the AR→USD cycle (see deficit section). The float has to cover one full cycle plus a bad month, or the reserve becomes the de-facto operating account — which defeats the purpose.

## 4 — Credit vs. financing vs. equity

These solve **different problems**. The instinct to pick one *or* the other is the error.

| | What it's for | Pros | Cons |
|---|---|---|---|
| **Credit line / revolver** | The **timing + FX-conversion gap** — expenses due now, receivables (esp. Bs) not yet converted to USD | No dilution; pay only when drawn; cheapest money; matches a short-term problem with a short-term instrument; preserves equity for growth | Hard for a VE-linked entity to get; needs the US C-corp (Tesote Technologies Inc.) as borrower; covenants; rate; we don't have one today (Rho $631k was a mislabel — **not** a real line) |
| **Venture debt / financing** | Extending runway without dilution when there's a clear path to revenue/raise | Less dilutive than equity; can be sized larger than a revolver | Interest + warrants; usually wants an equity round alongside it; covenants; aggressive in a downside |
| **Equity (SAFE)** | Funding **structural burn** and **provisioning the operating float** — absorbing losses, funding growth bets (e.g. the Dan dev-capacity memo) | Permanent capital; no repayment pressure; right tool for losses you can't bridge | Dilution; using it to plug a 60-day receivables gap is the most expensive money for the cheapest problem |

**Recommendation:**

1. **Revolver first**, for the timing/FX gap. It's textbook working-capital territory. Borrow against the US C-corp. Start the conversation now — we have *no* committed line today and the gap is real and recurring.
2. **SAFE only to provision the float**, not to bridge receivables. Sized to fund operating float on top of the reserve (see gap below). Framing for investors: *"We run on a $480k locked reserve and a 2–3 month float; we're raising to provision the float so the reserve is never the thing between us and payroll."* Clean, disciplined, fundable.
3. **Don't dilute for a timing problem.** If the revolver covers the gap and we hit breakeven on schedule, we may not need a SAFE this year at all.

---

## The real deficit — the only number that actually runs the business

The accounting net (~−$30k/mo) is **not** the number that can kill us. The number that can kill us is the **USD-liquidity gap**, because of how money moves through the business:

### The cash conversion cycle, currency-aware

```
  Invoice issued
      │  ← VE clients slow-pay; "next week" is the national sport
      ▼  (T + ? days)   ⚠️ days-to-collect — NEED REAL NUMBER
  Payment received (mostly Bs)
      │  ← Bs is not spendable on US payroll
      ▼  (T + ? days)   ⚠️ days-to-convert — NEED REAL NUMBER
  Bs converted to USD (GANESH OTC / BNC Subasta / GGBRDB vehicle)
      │  ← batchy, not continuous; FX spread + commission
      ▼
  USD available to pay Multiplier / Gusto / contractors / SaaS
```

**Why this matters more than the net number:**

- **Most expenses are hard-USD.** Multiplier ($30k), Gusto ($27k), contractors ($21k), Million Web ($12k), SaaS ($10k) = **~$100k/mo that *must* be paid in USD**, on a fixed calendar.
- **Most revenue arrives as Bs.** VES cobros trending ~$135k/mo equivalent (95%+ of inflows are VES, concentrated in BNC). That Bs cannot pay US payroll until it's converted.
- **Conversion isn't instant or free.** It happens in batches through OTC/Subasta windows (we saw swaps on 2/10, 2/12, 4/13, 4/15, 4/23 — sporadic, not daily), carries a spread/commission, and depends on counterparty availability.

So even in a month where total FX-adjusted revenue ≈ expenses, **USD-out can exceed USD-in** because the Bs revenue hasn't finished becoming USD yet. *That's* the real deficit — and it's why the reserve and float are held in USD.

### How to actually measure it (monthly)

Track three deficits separately — they have different fixes:

1. **Accounting deficit** = revenue − expenses (FX-adjusted). Today ~−$30k/mo. Fix = growth + cost discipline.
2. **Timing deficit** = USD owed this month − USD available this month (before any conversion). This is the working-capital hole. Fix = revolver + faster collection.
3. **Conversion deficit** = Bs collected − Bs converted to USD, expressed in days of lag + spread cost. Fix = a real FX conversion cadence/strategy, not ad-hoc Subasta runs.

The monthly "deficit we operate on" = the **timing deficit**, funded by operating float (and ultimately a revolver). The reserve protects against the accounting deficit running unchecked.

### ⚠️ The numbers we don't have yet (and must)

This whole section is directional until we measure:

- **Days-to-collect**: invoice issued → payment received. (Track 1 of `[[ar-and-cobros-2026-05]]` is literally collecting this.)
- **Days-to-convert**: Bs received → USD available.
- **Currency split of revenue**: what % of the ~$95k arrives USD vs. Bs.
- **FX spread cost**: what we lose per conversion (commission + rate vs. official).
- **Hard-USD obligation calendar**: exact USD due per week, so we can see the intra-month USD low point — that low point, not the month-end balance, is what the float must cover.

**Once we have these, the operating float number stops being "2–3 months gross" hand-wave and becomes "the largest intra-month USD gap × a safety factor."** That's the real, defensible operating-cash figure.

---

## Current position vs. the policy (the uncomfortable part)

| Layer | Target | Today (May 11) | Gap |
|---|---:|---:|---:|
| Reserve (untouchable, USD) | $480k | — | — |
| Operating float (2–3 mo gross) | $250–375k | — | — |
| **Total provisioned** | **$730–855k** | **~$470k USD** | **−$260–385k** |

- We're at **~$470k total USD** — basically the reserve target *alone*, with **zero operating float on top**, and ~$10k *under* the reserve line.
- Every burn month pushes us further under the floor we just declared sacred.
- **This is the real size of the raise/financing need: ~$260–385k** to be fully provisioned (reserve + float) — *not* a vague "fund the burn" number.

The choice is concrete: **(a)** grow into the float by hitting breakeven (~Aug–Sep if 7% MoM holds) while running 2–3 months at/below the reserve floor with no margin for a bad month — and April proves bad months happen; or **(b)** secure ~$300–400k (revolver + modest SAFE) to provision the float now and stop running thin. I lean **(b)** — conviction isn't a cash buffer.

---

## Open data to confirm

- [ ] ⚠️ Days-to-collect, days-to-convert, FX spread, revenue currency split, USD obligation calendar (above)
- [ ] Confirm GGBRDB treatment is "FX vehicle" everywhere — `[[analysis-may-2026]]` still calls it intercompany cushion in places, which overstates runway. **Reconcile: real full-year drawdown is the −$360k figure, not −$170k.**
- [ ] Exact current USD position (refresh from workspace — $470k is May 11)
- [ ] Which entity borrows for the revolver (US C-corp confirmed?)
- [ ] Reserve account — where does $480k physically sit, and is it walled off?

## Related

- [[analysis-may-2026]] — burn/revenue/runway source (mind the GGBRDB correction)
- [[cash-flow-king/index|cash-flow-king]] — categorization rules + April baseline
- [[ar-and-cobros-2026-05]] — the days-to-collect data this doc needs
- [[dev-capacity-investment-dan-memo]] — the growth bet a SAFE would fund
- [[project_payments_10x_bet]] — VES cobros scaling = the revenue side of the conversion problem
