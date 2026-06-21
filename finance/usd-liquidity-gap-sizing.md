---
title: The USD-Liquidity Gap — Sizing the Revolving Float
tags: [finance, treasury, fx, working-capital]
updated: 2026-06-09
status: draft
---

# The USD-Liquidity Gap — Sizing the Revolving Float

The gap that **survives accounting breakeven.** This is the one we have to cover smartly so it never touches the reserve.

> Companion to `[[financial-policy-non-negotiables]]` and `[[scenario-reserve-credit-equity-2026-06]]`. Those size the *burn bridge* (temporary, closes at breakeven). This sizes the *pipeline float* (permanent, revolving).

---

## Why breakeven doesn't fix it

Two different gaps, often confused:

| | Burn bridge | USD-liquidity gap |
|---|---|---|
| Cause | Spending more than we earn | Earning in Bs, paying in USD, with a lag |
| Closes when? | At breakeven | **Never** — it's structural |
| Instrument | Line (until breakeven) + equity | **Line, permanently (revolving)** |
| Sized by | Cumulative net burn | **Daily USD outflow × cycle length** |

At breakeven, net monthly flow = zero — but there's still a **pipeline** of USD obligations that come due *before* the matching Bs revenue has finished becoming spendable USD. You must front that pipeline. That fronted amount is a permanent float. It revolves (today's collection repays last cycle's draw), but it's never zero.

## The cycle, with the clock on it

```
  Invoice issued (Bs)
      │  days-to-collect  ⚠️ (VE clients slow-pay)
      ▼
  Bs received
      │  days-to-convert  ⚠️ (GANESH/Subasta — batchy, not daily)
      ▼
  Hard USD in hand  ──►  pays Multiplier / Gusto / contractors / SaaS
```

The total clock — **invoice → spendable USD** — call it **T days.** The float we must finance ≈ **(daily hard-USD outflow) × T.**

## The inputs

| Input | Value | Source / note |
|---|---:|---|
| Hard-USD obligations / mo | **~$100k** | Multiplier $30k + Gusto $27k + contractors $21k + Million Web $12k + SaaS/infra ~$10k |
| → per day | **~$3.3k** | $100k ÷ 30 |
| Share of revenue arriving as direct USD | **~0%** ⚠️ | YTD "USD inflows" (~$135k) are dominated by the **GGBRDB FX vehicle** — i.e. *converted* Bs, not native USD revenue. So treat ~all operating revenue as originating in Bs and needing conversion. **Confirm this.** |
| VES-paid obligations / mo | ~$10–12k | Honorarios, taxes, utilities — no conversion needed, excluded from the gap |

Because almost all revenue starts as Bs, nearly the *full* $3.3k/day of USD obligations is exposed to the cycle. That's the conservative, and probably correct, read.

## Sizing the float — sensitivity to cycle length

**Float ≈ $3.3k/day × T**, with a 1.25× safety factor for batchy conversion and bad weeks:

| Cycle T | Base float | With 1.25× safety | Covered by $150–250k line? |
|---:|---:|---:|---|
| 30 days | $100k | $125k | ✅ comfortably |
| 45 days | $150k | $188k | ✅ |
| 60 days | $200k | $250k | ✅ at the top |
| 75 days | $250k | $313k | ⚠️ over |
| 90 days | $300k | $375k | ❌ under-covered |

**Read:** the $150–250k line covers a **well-run 45–60 day cycle.** If the real cycle is 75–90 days — entirely plausible for slow-paying VE clients plus sporadic Subasta windows — the line is undersized, and the overflow would hit the reserve. That's the scenario we're explicitly preventing.

## The two levers (they're substitutes)

Every day cut off the cycle frees **~$3.3k** of drawn line. So the line size and the operational fixes trade directly against each other:

1. **Shorten days-to-collect** — the cobros work (`[[ar-and-cobros-2026-05]]`). Faster collection on the VE AR book directly shrinks T.
2. **Shorten days-to-convert** — replace sporadic Subasta/OTC batches with a **standing conversion cadence** (convert on a schedule, not when someone remembers). Cuts the second half of the clock.
3. **Size the line to the *measured* cycle** — once we know T, set the line at `$3.3k × T × 1.25`, not a guessed range.

A 90→45 day improvement is worth **~$150k of line you don't have to draw** — and the interest on it.

## The cost of the gap (separate from line interest)

Running in two currencies has a standing FX cost, independent of the line:

- Converting ~$100k/mo = ~$1.2M/yr
- At a 2–4% spread (commission + rate gap on OTC/Subasta) = **~$24–48k/yr** bled on conversion alone
- That's effectively a second "interest rate" on the business. Worth measuring per-conversion and negotiating — at this volume, shaving 1% of spread ≈ $12k/yr.

## How we cover it without touching the reserve

Order of defense, every cycle:

1. **USD operating float first** (the 2–3 month layer in the policy doc) absorbs normal timing.
2. **Revolver second** — draw to front the pipeline when projected USD balance over the next ~2 weeks of obligations dips below what's owed. Revolves as Bs converts.
3. **Reserve never** — by construction. If we're reaching for it, the line was undersized or the cycle blew out → that's a trigger, not a routine.

**Operational guardrail:** maintain a rolling **USD obligation calendar** (what's due, in USD, over the next 30 days) against **projected USD-on-hand** (current USD + Bs that will convert in time). When the projection dips below obligations → draw the line. This makes "don't touch the reserve" a *mechanical rule*, not a judgment call in a stressful week.

---

## Bottom line

- The gap is **real, permanent, and unaffected by breakeven.** Plan for it as a standing revolving float, not a one-time bridge.
- **$150–250k line covers a 45–60 day cycle.** Our actual cycle is the single most important unknown — measure it (cobros work is already on it).
- **Two ways to cover it: a bigger line, or a shorter cycle.** The shorter cycle is cheaper *and* improves the business — prioritize it, size the line to whatever cycle we can't compress away.
- **The reserve stays untouched by mechanical rule** (obligation calendar → draw line), not willpower.

## Related
- [[financial-policy-non-negotiables]] — the policy; this is the "real deficit" section, sized
- [[scenario-reserve-credit-equity-2026-06]] — the burn-bridge companion (temporary gap)
- [[ar-and-cobros-2026-05]] — the lever that shortens days-to-collect
- [[project_payments_10x_bet]] — VES cobros scaling = the revenue side of the conversion problem
