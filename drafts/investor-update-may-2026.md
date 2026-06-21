---
title: Investor Update — May 2026 (standard monthly)
tags: [finance, investors]
updated: 2026-06-01
status: draft
---

# Investor Update — May 2026

**Audience:** standard monthly to all investors. NOTE: for competitor-adjacent investors, send the [[investor-update-q1-april-snapshot|high-level snapshot]] instead — this version names specific banks (GTM/infra signal). Strip bank specifics or swap to snapshot for that segment.

**Carries a restatement:** April recurring revenue was overstated last month (churn not netted out). Footnoted below — never restate quietly.

---

## Email draft

Dear investors,

Here's Tesote's May 2026 update:

**KPIs**

- Paying Customers: 130 logos (up from 128 at the start of the month)
- Logo Churn Rate: 1.56% (2 customers lost out of 128 starting)
- Subscriptions MRR: $108.8K (+5.91% MoM)
- Gross Revenue Churn: 2.54% ($2.6K in lost subscriptions MRR)
- One-Time Implementation Fees: $18,000
- Total Monthly Revenue: $126.8K (-4.90% MoM)
- Team: 24 FTEs
- Cash: $600K
- Monthly Net Burn: ~$30K
- Runway: 20+ months

**Recurring MRR grew +5.91% to $108.8K — an acceleration over April's +3.27%.** Total revenue is down MoM only because April carried an unusually heavy one-time implementation load ($30.6K vs $18K in May); implementation fees are lumpy month to month — recurring is the durable number.

|                              | March        | April        | May          |
|------------------------------|--------------|--------------|--------------|
| Recurring Revenue            | $99,459.25   | $102,711.25  | $108,779.25  |
| MoM % change                 | 6.42%        | 3.27%        | 5.91%        |
| One-Time Implementation Fees | $11,400.00   | $30,600.00   | $18,000.00   |
| Total Revenue                | $110,859.25  | $133,311.25  | $126,779.25  |
| MoM % change                 | 6.64%        | 22.96%       | -4.90%       |

> *Note: April recurring revenue has been restated from $105.7K to $102.7K. Last month's figure did not net out churn; this correction is now reflected consistently across all months. April total revenue restated accordingly to $133.3K.*

---

### Key Events

**The Good**

**Launched Tesote AI.** We shipped a standalone Tesote AI product with its own UI and began rolling it out to our first customers. Early signal is strong — customers are using it to set up workflows, generate reporting, and more, and it's proving genuinely powerful. We'll go deeper in the quarterly report on what prompted the launch, with quantitative and qualitative feedback after 30+ days in customers' hands.

**Payments.** Progress continues on the new payments portal. Candidly, it's taking a bit longer than we'd planned — the Tesote AI launch pulled some focus, and we're testing on fairly new rails, which adds time we want to take to get right. We expect a more substantial update by the end of the quarter.

**The Bad**

**Bank connection reliability.** Banks ramped up anti-bot detection sharply this month, materially affecting two of the top banks we support via scrapers. This hit some customers' ops directly, and we've been working alongside them to resolve issues as fast as possible. The good news: one of these banks just rolled out an official API, and we'll be transitioning our high-volume customers onto it over the next few weeks. More broadly, we've been working more closely with banks as they roll out API capabilities, with the intention of beginning a larger transition to bank APIs wherever they're available.

Best,
Luis

---

## Open items

- Confirm whether the April update already shipped with old numbers. If yes, the footnote is required. If still catchable upstream, fix at source instead.
- Propagate the restated April ($102.7K recurring / $133.3K total) to any deck / data room / investor dashboard so two Aprils don't float around.
- Competitor-adjacent recipients → snapshot variant or strip bank specifics.
- Payments is "more next quarter" for the 2nd month running — make sure the quarterly lands a concrete milestone before it reads as slipping.
