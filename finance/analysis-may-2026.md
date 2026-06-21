---
title: Finance Analysis — May 2026
tags: [finance, burn, runway, projections]
updated: 2026-05-12
status: draft
revenue_implied_ytd: $95K/mo
ar_to_recoup: $100K
untracked_cash_ytd: $37K
ytd_adjusted_burn: -$107K
fy26_midcase_burn: -$360K
---

# Tesote Finance Analysis — May 2026

Working analysis built from Tesote Finance workspace data (Jan 1 – May 11, 2026), plus user-supplied adjustments for receivables, untracked cash, severance, and forward-looking expense changes.

## Workspace snapshot (May 11, 2026)

- **33 accounts** across Mercury, Rho, Chase, BNC, and VE retail banks (Bancamiga, Banplus, Banco Activo, Banco Exterior, Banco Plaza, BdV, BBVA, López de Haro) plus manual entries
- **USD position (active accounts)**: ~$469.7K total
  - Rho Cash Checking: $163K
  - Unnamed USD account: $151K
  - Mercury Checking: $67.6K
  - Cuenta Manual: $30K
  - BNC USD: $23.4K
  - Chase BUS COMPLETE: $14.1K
  - Caja Chica: $12K
  - Otro activo manual: $6.8K
  - Smaller: López de Haro, Bancamiga USD, etc.
- **VES position**: ~29.4M Bs, **97% concentrated in BNC** (28.4M)
- **Credit lines (draft, not cash)**: Rho Credit $631K, Mercury Credit $13.7K

## Bank-connection health

| Bank | Status | Sync |
|---|---|---|
| Mercury, Rho, Chase | active API | syncing daily |
| BNC | active API | transactions flowing |
| BdV, BBVA, Banplus, Bancamiga, Activo, Exterior, Plaza, López de Haro | active webscraper | `last_synced_at: null` — coverage uncertain |
| Banesco | **draft** | not connected (relevant for [[project_banesco_cobros_status]]) |
| Santander MX, Bancrecer, BBVA(2), 100% Banco | draft | not connected |

## YTD cash flow (Jan 1 – May 11, 2026)

### Workspace numbers (real, ex-intercompany)

| Bucket | Amount |
|---|---:|
| USD inflows | ~$135K |
| VES inflows @ 550 (~148M Bs) | ~$148K |
| **Total real inflows** | **~$283K** |
| USD outflows | ~$443-458K |
| VES outflows @ 550 (~75M Bs ex-FX/GANESH) | ~$75K |
| **Total real outflows** | **~$520-525K** |
| **Workspace net burn** | **~-$244K** |

### Adjusted YTD (adding what workspace doesn't capture)

Confirmed 2026-05-12: AR = $100K, untracked cash = $37K.

| Adjustment | $ |
|---|---:|
| Workspace YTD net | -$244K |
| + $100K AR to be recouped | +$100K |
| + $37K untracked cash payments | +$37K |
| **Adjusted YTD net burn** | **~-$107K** |

### Implied real revenue

| | $ | $/mo |
|---|---:|---:|
| Workspace inflows | $283K | $64K |
| + AR + untracked cash | $137K | $31K |
| **Adjusted real revenue YTD** | **$420K** | **~$95K** |

Lands in the middle of the $80-100K/mo real revenue range.

### Burn velocity

- Workspace pace: -$1.86K/day
- **Adjusted pace: -$0.82K/day**
- **Operating burn ≈ ~$24K/month**

## Monthly burn trend (real, ex-intercompany)

| Month | Real net | $/day |
|---|---:|---:|
| Jan | -$77K | -$2.5K |
| Feb | -$33K | -$1.2K |
| Mar | -$55K | -$1.8K |
| Apr | -$98K | -$3.3K |
| May 1-11 | +$20K | +$1.8K |

April was the worst month (Multiplier outlier + 2 payroll cycles + Caracas trip costs + GANESH FX timing). February was the best non-partial month.

## Confirmed intercompany inflows (~$128K YTD)

Separate from operating revenue:

| Source | Date | $ |
|---|---|---:|
| GGBRDB LLC | 1/13 | $40,900 |
| GGBRDB LLC | 2/20 | $44,775 |
| GGBRDB LLC | 4/14 | $21,950 |
| TESOTE TECHNOLOG ACH | 5/4 | $20,000 |
| **Total** | | **$127,625** |

Intercompany has covered ~52% of cash needs YTD.

## FX swaps excluded (not real outflows)

- **2/10**: BNC Subasta — bought $15K @ 550 = 8.25M Bs out + 41K commission
- **2/12**: BNC Subasta — bought $8K @ 550 = 4.4M Bs out + 22K commission
- **4/13**: GANESH MMXXI OTC — 12.5M Bs out (~$22.7K USD received off-platform)
- **4/15**: BNC Subasta — bought $400 @ 570.75 = 228K Bs
- **4/23**: GANESH MMXXI OTC — 6.27M Bs out (~$11.4K USD received off-platform)

GANESH transactions are FX OTC; corresponding USD landed in unsynced accounts.

## April deep dive (full month example)

**Total April outflows: ~$164.5K** ($139.5K USD + $25K VES equiv, ex-GANESH FX)

### By category (ranked)

| Category | $ | % | Pattern |
|---|---:|---:|---|
| Multiplier Tech | $39.0K | 24% | Recurring; **4/22 outlier $32K is the bulk** |
| Direct contractors (Rho) | $33.4K | 20% | Batches 4/9-10 + 4/29 — **$12.5K was severance for 2 employees** |
| Gusto payroll (2 cycles) | $27.0K | 16% | Recurring |
| Million Web | $11.3K | 7% | Recurring monthly |
| VES honorarios + Pago TST | $7.9K | 5% | Recurring |
| Big VE vendors (Fact 0510, 000274, 1367) | $5.1K | 3% | Vendor-specific |
| Marketing/sales SaaS (LinkedIn, HubSpot, Dripify, ads) | $5.1K | 3% | Recurring |
| Apriori Legal | $4.0K | 2% | Will drop to $1.5K from June |
| Dicope rent (Apr 15 – Jun 15 prepay) | $3.6K | 2% | Quarterly |
| Caracas trip lodging | $2.6K | 2% | One-off |
| AOFLEX SRL | $2.7K | 2% | Last run May |
| Regus + Roam HQ | $2.6K | 2% | Recurring |
| Plane tickets (within trip costs) | ~$3K | 2% | One-off |
| Trademark registration anticipo | $1.8K | 1% | One-off |
| Anthropic Claude Team spike | $1.6K | 1% | Appears monthly (~$1-1.6K) |
| OVH (4/2 big charge) | $1.3K | 1% | Recurring |
| Tax payments (BNC impuestos) | $1.0K | 1% | Variable |
| Lorena Gonzalez Reina | $0.9K | 1% | Possibly recurring |
| Other infra/SaaS (Sentry, Render, Intercom, Cursor, Plaid, Linear, etc.) | ~$10K | 6% | Recurring |
| Remitly/Uber/Rappi/misc | $0.7K | <1% | Operational |
| Bank fees, P2C, debit misc | ~$1K | <1% | Recurring |

### One-offs in April (~$23K)

- Severance: $12.5K
- Caracas trip lodging: $2.6K
- Plane tickets: $3K
- Trademark anticipo: $1.8K
- Production test cobros: $0.3K
- Dicope quarterly prepayment timing: $2.4K extra vs monthly average

### Multiplier pattern (recurring at $30-39K/mo — not a one-off)

- Feb: $34K total (3 charges including $20.6K + $13.5K)
- Mar: $38K total ($20.6K + $13.5K cycle)
- Apr: $39K total ($18.6K + $13.5K cycle on 4/22)

**This is the single biggest spend line — bigger than Gusto.** Confirmed as structural, not one-off.

## Going-forward outflow projection (May–Dec 2026)

### Monthly base (post-adjustments)

| Line | $/mo |
|---|---:|
| Gusto payroll (2 cycles) | $27K |
| Direct contractors (post-severance) | $21K |
| Multiplier (recurring) | $30K |
| Million Web | $12K |
| Apriori (May $4K → Jun+ $1.5K) | $1.5-4K |
| AOFLEX (May $2.7K → Jun+ $0) | $0-2.7K |
| Marketing/sales SaaS | $5K |
| Co-working (Regus + Roam) | $2.6K |
| Infra/SaaS recurring | $10K |
| Anthropic Claude Team monthly spike | $1.5K |
| Other USD misc | $1K |
| VES honorarios + taxes + utilities + fees | $10-12K |
| Dicope rent (quarterly: Jun, Sep, Dec) | $3.6K those months |
| **Total** | **$120-127K/mo** |

### Per-month outflow projection

| Month | Outflows | Notes |
|---|---:|---|
| May | $127K | AOFLEX last, full Apriori, no rent (prepaid Apr-Jun) |
| Jun | $126K | AOFLEX gone, Apriori $1.5K, Dicope rent renewal |
| Jul | $122K | Steady state |
| Aug | $122K | Steady state |
| Sep | $126K | Dicope rent renewal |
| Oct | $122K | Steady state |
| Nov | $122K | Steady state |
| Dec | $126K | Dicope rent renewal |
| **May–Dec total** | **$993K** | $124K/mo avg |

## Revenue scenarios

Real revenue implied YTD at $95K/mo. Three scenarios:

| Scenario | Mo rev | Logic |
|---|---:|---|
| Low | $88K | Below YTD pace |
| Mid | $95K | YTD pace continues |
| High | $100K | Modest growth (VES cobros keep scaling) |

### Net per month by scenario

| Month | Out | Net @ $88K | Net @ $95K | Net @ $100K |
|---|---:|---:|---:|---:|
| May | $127K | -$39K | -$32K | -$27K |
| Jun | $126K | -$38K | -$31K | -$26K |
| Jul | $122K | -$34K | -$27K | -$22K |
| Aug | $122K | -$34K | -$27K | -$22K |
| Sep | $126K | -$38K | -$31K | -$26K |
| Oct | $122K | -$34K | -$27K | -$22K |
| Nov | $122K | -$34K | -$27K | -$22K |
| Dec | $126K | -$38K | -$31K | -$26K |
| **May-Dec sum** | $993K | **-$289K** | **-$233K** | **-$193K** |

### Full-year 2026 (incl. YTD)

YTD Jan-Apr adjusted = YTD Jan-May11 adjusted (-$107K) minus May 1-11 net (+$20K) = **-$127K**

| | Low ($88K) | Mid ($95K) | High ($100K) |
|---|---:|---:|---:|
| YTD Jan-Apr adjusted | -$127K | -$127K | -$127K |
| May-Dec projection | -$289K | -$233K | -$193K |
| **Full year 2026** | **-$416K** | **-$360K** | **-$320K** |

## Growth scenario: 7% MoM revenue from $95K (May)

| | May | Jun | Jul |
|---|---:|---:|---:|
| Revenue | $95.0K | $101.7K | $108.8K |
| Outflows | $127K | $126K | $122K |
| **Net** | **-$32.0K** | **-$24.3K** | **-$13.2K** |

At sustained 7% MoM growth: **breakeven crossover ~August-September 2026** ($116-124K revenue vs $122-126K outflows).

More conservative 3-4% MoM growth pushes breakeven to Q4 / early 2027.

## Projection evolution through analysis

| Iteration | Full-year burn |
|---|---:|
| Initial unadjusted (workspace only) | -$680K |
| + $80K AR + $25K cash | -$575K |
| + trip/severance/AOFLEX/Apriori/rent adjustments (Multiplier non-recurring — incorrect) | -$291K |
| + Multiplier + Anthropic recurring (corrected) | -$534K |
| + Revenue at $80-100K/mo confirmed | -$382K |
| Prior mid-case (Rev $94K, AR $80K, cash $25K) | -$400K |
| **Final mid-case (Rev $95K, AR $100K, cash $37K — confirmed 2026-05-12)** | **-$360K** |

## Leverage points (ranked by $/year impact)

1. **Multiplier** ($30K/mo recurring = $360K/yr) — 20% cut = $72K/yr saved. Biggest single line. Worth a serious renegotiation conversation.
2. **Million Web** ($12K/mo = $144K/yr) — confirm scope and necessity. If finite project ends mid-year, cuts $50-80K.
3. **Direct contractors via Rho** ($21K/mo post-severance = $250K/yr) — per-contractor ROI review.
4. **GGBRDB intercompany pace** — $107K YTD, ~$255K annualized. Absorbs most of projected burn if it continues.
5. **VES cobros → USD conversion** — May trending toward $135K/mo equivalent. Need Subasta/OTC strategy to make VES revenue deployable for US payroll.
6. **SaaS sprawl** (~$10K/mo combined: LinkedIn, HubSpot, Render, Sentry, Intercom, Plaid, Linear, Cursor, Anthropic baseline, etc.) — small individually, meaningful collectively.

## Key sensitivities / risks

- **The Multiplier story is load-bearing.** If those $30K+ monthly charges keep coming, the picture is -$400 to -$450K full year. If they're renegotiated down or capped, picture drops to -$300K range.
- **VES revenue at 550 is not USD-fungible at scale.** FX conversion plan needed.
- **GGBRDB cadence assumption** — if it stops, financing side rethinks even if operating burn improves.
- **Tax timing** — March had $13K USD-equiv tax bomb. If quarterly hits Jun/Sep/Dec, add $10-15K those months.
- **Hiring** — current projection assumes flat headcount. Each hire ~$3-5K/mo loaded.
- **VE webscraper banks have null `last_synced_at`** — VES totals weighted toward BNC (API-synced). Some Bancamiga/Banplus/Banco Exterior activity may be undercounted.

## Bottom line

- **Real cash drawdown YTD: ~$107K** (adjusted with confirmed $100K AR + $37K cash).
- **Operating burn: ~$24K/mo adjusted pace.**
- **Full-year 2026 mid-case: ~-$360K burn**, range -$320K to -$415K.
- **With $128K intercompany already received** and likely continuing, **net cash drawdown 2026 plausibly only -$170K to -$225K** — the number that should drive runway planning.
- **Path to breakeven by Aug-Sep 2026** if revenue sustains 7% MoM growth from $95K base.

## Related

- [[project_payments_10x_bet]] — VES cobros scaling story
- [[reference_finance_db_schema]] — for deeper SQL analysis
- [[ar-and-cobros-2026-05]] — AR/cobros details for the $80K receivables figure
- [[project_caracas_trip_april_2026]] — April trip context for one-off expenses
