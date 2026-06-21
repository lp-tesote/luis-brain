---
title: Scenario — $400k Reserve + $150-250k Line + $250-500k Equity Option
tags: [finance, runway, scenario, treasury]
updated: 2026-06-09
status: draft
---

# Scenario: $400k Reserve + Credit Line + Equity Option

Crunching Luis's proposed structure (2026-06-09):
- **Begin reserve at ~$400k** (down from the $480k = $40k×12 policy floor)
- **Ability to tap a $150–250k credit line**
- **Option to raise $250–500k equity**
- **Assume breakeven in Q3 2026**

> Numbers are directional. Starting cash needs a workspace refresh — using **$450k as of ~June 1** (≈ $470k on May 11 minus ~$30k of intervening burn). Net-burn paths come straight from `[[analysis-may-2026]]`.

---

## Starting point

| | $ |
|---|---:|
| USD position (May 11, actual) | ~$470k |
| Est. position ~June 1 (after ~1 mo burn) | **~$450k** |
| Proposed reserve floor | $400k |
| **Usable cushion above reserve, today** | **~$50k** |

**That ~$50k is ~1.5 months of net burn.** So under this structure, you are *already* down to a month and a half of float before the reserve is the only thing left. The line isn't optional — it's the bridge.

---

## Burn-to-breakeven, three speeds

Net burn/mo from `[[analysis-may-2026]]`. "Cum." = cumulative burn from June.

### A — Growth case (7% MoM rev growth, breakeven ~Sep/Oct)

| Mo | Rev | Out | Net | Cum. | Cash (start $450k) |
|---|---:|---:|---:|---:|---:|
| Jun | 102 | 126 | −24 | −24 | 426 |
| Jul | 109 | 122 | −13 | −37 | 413 |
| Aug | 116 | 122 | −6 | −43 | 407 |
| Sep | 125 | 126 | −1 | −44 | 406 |
| Oct | 133 | 122 | **+11** | −33 | 417 |

**Bottoms at ~$406k — just above the $400k reserve. Self-funds to breakeven. Zero draw. Equity = pure growth optionality.**

### B — Mid case (flat $95k rev, no 2026 breakeven)

| Mo | Net | Cum. | Cash | vs $400k reserve |
|---|---:|---:|---:|---|
| Jun | −31 | −31 | 419 | ok |
| Jul | −27 | −58 | 392 | **breach** |
| Aug | −27 | −85 | 365 | draw $35k |
| Sep | −31 | −116 | 334 | draw $66k |
| Oct | −27 | −143 | 307 | draw $93k |
| Nov | −27 | −170 | 280 | draw $120k |
| Dec | −31 | −201 | 249 | **draw $151k** |

**Breaches reserve in July. Needs ~$151k drawn by year-end to keep the reserve whole — inside the $150–250k line. Credit alone bridges the full year. Equity not required for survival.**

### C — Conservative case (low $88k rev, breakeven 2027)

| Mo | Net | Cum. | Cash | Draw to hold $400k |
|---|---:|---:|---:|---:|
| Jun | −38 | −38 | 412 | — |
| Jul | −34 | −72 | 378 | 22 |
| Aug | −34 | −106 | 344 | 56 |
| Sep | −38 | −144 | 306 | 94 |
| Oct | −34 | −178 | 272 | 128 |
| Nov | −34 | −212 | 238 | 162 |
| Dec | −38 | −250 | 200 | **200** |

**Maxes the line (~$200k drawn) by December and is still burning into 2027 → equity becomes required.**

---

## What the structure actually buys you

| | Growth (A) | Mid (B) | Conservative (C) |
|---|---|---|---|
| Reserve breached? | No (bottoms $406k) | Yes, July | Yes, July |
| Credit drawn by Dec | $0 | ~$151k | ~$200k (near max) |
| Equity needed for survival? | No | No | **Yes** |
| Equity role | Growth fuel | Insurance | **Survival + growth** |

**The stack is correctly sized.** $400k reserve + $250k line + $250–500k equity option covers all three cases. The line carries the base/mid case; equity is the downside insurance and the upside accelerant. You don't raise to survive — you raise to *not slip into case C unfunded* and to push growth.

---

## The defense stack, summed

| Layer | $ | Months at $40k cap |
|---|---:|---:|
| Reserve (untouchable) | $400k | 10.0 |
| + Credit line (committed) | $250k | +6.3 |
| **Reserve + line** | **$650k** | **16.3** |
| + Equity (mid of range) | $375k | +9.4 |
| **Full stack** | **$1.03M** | **~26 months** |

At your *real* net burn (~$30k/mo, not the $40k cap), the same stack is **~22 / 35 months.** This is a genuinely strong position — *if the line is committed.*

---

## Honest take

1. **Do it — but the line is load-bearing and you don't have it yet.** "Ability to tap" ≠ committed facility. Until a bank signs, the $400k reserve is fiction in case B/C, because you'd be dipping into it by July. **Securing the line is priority #1**, on the US C-corp (Tesote Technologies Inc.). Banks lend when you don't need it — start now while the breakeven story is intact.

2. **$400k is fine, but only because the line restores the cushion.** You're trading $80k of idle reserve (480→400) for a drawable line — correct capital efficiency. Don't lower the reserve *without* the line in hand; that's just running thin and calling it policy.

3. **Don't raise equity to survive — raise from strength.** Base and mid cases never touch equity. Treat the $250–500k as (a) insurance against breakeven slipping past ~Sep, and (b) fuel for a deliberate growth bet (e.g. the dev-capacity memo). If you raise, do it *early* — while you can credibly say "we don't need this, we want it to go faster." That's the round that prices well.

4. **Keep the line open past breakeven.** Q3 breakeven is *accounting* breakeven. ~$100k/mo of costs are hard-USD; revenue is mostly Bs with a conversion lag. USD-liquidity breakeven trails accounting breakeven — the line covers that gap structurally, not just the bridge.

5. **Watch case C's tell.** If trailing-3-mo revenue is tracking $88k (not growing) by **end of August**, you're in case C: open the equity round then, before the line is >50% drawn. Don't wait for the line to max.

### Triggers, concretely

| Trigger | Action |
|---|---|
| Now | Secure the $150–250k line (US C-corp). Until then, treat $480k — not $400k — as the real floor. |
| Cash approaches $430k (reserve + ~1 mo float) | Begin drawing the line. Never touch the $400k reserve first. |
| End-Aug: trailing-3-mo rev flat at ~$88k **and** not bending toward breakeven | Open the equity round (case C path). |
| Line >50% drawn at any point | Open the equity round regardless. |
| Growth bet (dev capacity) approved | Raise equity to fund it — proactively, from strength, not from the burn line. |

---

## Related
- [[financial-policy-non-negotiables]] — the policy this scenario stress-tests
- [[analysis-may-2026]] — burn/revenue paths (mind the GGBRDB = FX, not cushion, correction)
- [[dev-capacity-investment-dan-memo]] — the growth bet equity would fund
