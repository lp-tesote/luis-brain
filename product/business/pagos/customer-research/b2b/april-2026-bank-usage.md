---
title: April 2026 — Bank Usage Across 24 B2B Workspaces
tags: [tesote-pay, b2b, banks, customer-research]
updated: 2026-05-05
status: draft
---

# April 2026 — Bank Usage Across 24 B2B Workspaces

**Question:** for a representative slice of B2B Tesote customers (food, agro, consumer goods — mostly Portuguesa/Lara/Carabobo industrial belt), which banks are they actually using to transact, and at what volume?

**Why it matters:** Tesote Pay B2B rail is bank-gated. Knowing which banks dominate B2B flows tells us which integrations are table-stakes vs. nice-to-have, and which clients are big enough to move the needle if they adopt.

**Method:** April 2026, VES only, top 5 banks per workspace by absolute volume (in + out). Volume dolarized at 500 VES/USD. Source: [april-2026-bank-usage.csv](april-2026-bank-usage.csv). Queries in `data/april_2026_workspace_top5_banks*.sql`.

**Caveats:**
- 2 of 24 workspaces returned no rows: **Casa Franceschi** and **Corporación JSL, C.A.** — either the name pattern missed an active workspace, or they had zero VES April activity. Worth investigating before treating this as a complete picture of the segment.
- "Bank" here = the workspace's own account bank, not the counterparty's bank. So this is "which rails do they sit on," not "who their customers/suppliers bank with."
- Inflow + outflow combined for ranking. The CSV breaks them apart so you can spot collection-banks vs payment-banks.

---

## TL;DR

1. **Five banks cover the segment.** BBVA, Banesco, Mercantil, Banco de Venezuela, BNC. These appear in 13–19 of 22 workspaces' top 5 and account for the overwhelming majority of volume. **If Tesote Pay B2B supports these five, it's credibly "covered" for VE B2B.** Without them, it isn't.
2. **BNC is a real B2B rail, not just B2C.** It's top-5 for 13 workspaces and #1 or #2 for several large ones (Protinal #2 / $6.5M, Maralac #2 / $3.3M, Marsoca #2 / $2M, Molinos Carabobo #3 / $25.9M, ASOPRODUCTOS #1). Validates the existing BNC investment as load-bearing for B2B, not a single-segment bet.
3. **Volume is wildly concentrated in a handful of giants.** Just five workspaces — Molinos Nacionales, Molinos Carabobo, Grupo Mimesa, Protinal, Alimentos Alvarigua — represent the bulk of the dollarized volume in this list. **These are the priority logos for B2B GTM.**
4. **Diversification is universal.** Every workspace uses 4–5 banks actively. Single-bank Tesote Pay is a non-product for B2B.
5. **Outflow ≈ Inflow.** Collections-only Tesote Pay won't cut it for this segment — outbound payments (payroll, suppliers, tax) are roughly half the use case across the board.

---

## The "Big 5" rails

Frequency of appearance in workspaces' top-5 (out of 22 with data):

| Bank | Top-5 appearances | Comment |
|---|---|---|
| BBVA (Provincial) | 19 | Most ubiquitous; #1 for several giants (Molinos Nacionales does $102M / month essentially single-bank on BBVA) |
| Banesco | 18 | Present almost everywhere; rarely the absolute #1 by volume but a high-frequency hub |
| Mercantil | 18 | Punches above its weight — top-3 for many; #1 for Molinos Carabobo, Procesadora Marsoca, ARAWAK, Protinal |
| Banco de Venezuela (BdV) | 14 | Often inflow-skewed (gov-owned, easy for customers to send to) — e.g., Avicola Las Tunas BdV: 1,088 in / 2,457 out, but for Mimesa it's the #1 bank at $22.7M |
| BNC | 13 | See TL;DR — actively used B2B-to-B2B, not just for individual collection |

Long tail (specific to a few clients, not generally worth supporting):

- **Banplus** — #1 for PASTCA ($1.3M), top-5 for suvica and TORONDOY. If we want PASTCA, we need Banplus.
- **Banco Exterior** — top-5 for CAMOR ($802K) and Procesadora Marsoca ($758K).
- **Banco Fondo Común** — top-5 for Almacenadora Asoportuguesa ($702K) and Asoportuguesa ($57K).
- **Venezolano de Crédito** — top-5 for Casagri de Lara ($1.5M) and PASTCA ($577K).
- **100% Banco**, **Banco Del Tesoro**, **Bancaribe**, **Banco Plaza**, **Bancamiga** — single-workspace appearances; treat as client-specific asks, don't build for them generally.

---

## Volume concentration — the priority logos

Approximate top-5 volume per workspace (April 2026, USD-equivalent at 500):

| Workspace | Top-5 vol (USD) | Top bank |
|---|---|---|
| Molinos Carabobo SA | ~$129M | Mercantil ($42M), Banesco ($41M), BNC ($26M) |
| Molinos Nacionales CA | ~$105M | **98% on BBVA alone** — extreme single-bank concentration |
| Grupo Mimesa | ~$59M | BdV ($23M), BBVA ($18M) |
| Protinal | ~$28M | Mercantil ($9.5M), BNC ($6.5M), BdV ($5.4M), BBVA ($5.2M) — diversified |
| Alimentos Alvarigua | ~$24M | BBVA ($10M), Banesco ($8M) |
| Casagri de Lara | ~$24M | Banesco ($9.8M), BBVA ($7.3M) |
| AVICOLA LAS TUNAS | ~$22M | Mercantil ($9.1M), BdV ($7.8M) |
| ALIMENTOS LPRADO | ~$15M | Banesco ($5.8M) |
| Asoportuguesa | ~$11M | BdV ($5.4M), BBVA ($5.2M) |
| Grupo Maralac | ~$10M | Banesco ($4M), BNC ($3.3M) |
| Alimentos Doña Emilia | ~$10M | BBVA ($3M), Banesco ($2.3M) |
| CAMOR Internacional | ~$10M | Banesco ($6.9M), BNC ($1M) — high-velocity (~53k tx in April) |
| alimentosmunchy | ~$9M | BBVA ($2.5M), Banesco ($2.3M) |
| Procesadora Marsoca | ~$8M | Mercantil ($4.1M), BNC ($2M) |
| Almacenadora Asoportuguesa | ~$5M | BdV ($2.1M) |
| PASTCA | ~$4M | **Banplus #1** ($1.3M) |
| Capitalfoods | ~$2.5M | Mercantil ($1.2M) |
| Alimentos Global | ~$2.4M | Banesco ($1.1M) |
| suvica | ~$2.3M | Banesco ($1M) |
| ARAWAK | ~$0.4M | Mercantil ($200K) |
| TORONDOY | ~$0.1M | BBVA ($50K) |
| ASOPRODUCTOS | ~$0.05M | BNC ($40K) |

**Rough rule:** the top 5 logos in this list (Molinos Nacionales, Molinos Carabobo, Mimesa, Protinal, Alvarigua) hold the bulk of the dollarized B2B volume in this sample. If they adopt Tesote Pay's B2B rail at any meaningful share, it moves the 10x revenue needle on its own. Everyone else is supporting cast — useful for product validation, breadth, and cycle, but not GTM priorities.

---

## Direction insights (collection vs. payment)

A handful of patterns worth noting from the in_tx / out_tx splits in the CSV:

- **AVICOLA LAS TUNAS — Banco de Venezuela skews heavily inbound** (1,088 in / 2,457 out by tx count, but inflow $1.97M vs outflow $1.94M VES — balanced by volume). BdV often plays the role of "where customers send money in," because gov-owned + ubiquitous retail accounts.
- **CAMOR Internacional — extreme volume on Banesco and BNC** (Banesco 18.8k tx, BNC 17.1k tx — these look more like high-frequency collection patterns, possibly retail/distribution touching B2B). Worth a closer look — they may not be pure B2B.
- **Procesadora Marsoca — outflow-heavy on every bank** (Mercantil 334 in / 1,150 out, BNC 98 in / 397 out, Marsoca is paying suppliers more than collecting). They're a vendor in the chain, not a final-mile collector.
- **Molinos Nacionales — perfectly balanced on BBVA** (1,447 in / 800 out by count, but inflow $25.7M vs outflow $25.4M — basically balanced by value). Operating-account behavior on a single bank.

Read it as: BdV/Mercantil tilt toward inflow for some clients; BNC and Banesco are full-stack (in + out); Banplus / Banco Exterior / Venezolano Crédito show up where there's a long-standing client relationship, often outflow-heavy.

---

## Implications for Tesote Pay B2B

- **Required rail set:** BBVA, Banesco, Mercantil, BdV, BNC. Ship without these and the product is incomplete for VE B2B.
- **BNC is a load-bearing B2B rail**, not just a B2C one. Continued investment justified by usage, not just by it being the rail we have access to.
- **Concentration → focus the GTM motion.** Pursue Molinos Nacionales, Molinos Carabobo, Mimesa, Protinal, Alvarigua first. A 10–20% rail-share on any one of these moves more revenue than 100% of the bottom half.
- **Single-bank Tesote Pay is not viable** for this segment — every workspace uses 4–5 banks. Multi-bank UX has to be table stakes.
- **Outbound matters as much as inbound.** Pay-out flows (payroll, supplier, tax) need to be in v1, not v2. Collections-only ≠ a full B2B product.
- **Long-tail banks are deal-breakers per-client.** PASTCA needs Banplus; Almacenadora Asoportuguesa benefits from BFC. Treat these as client-specific asks during sales, not roadmap items.

## Open questions

- Why do **Casa Franceschi** and **Corporación JSL** show no rows? Pattern miss or genuine zero April VES activity? Re-run resolve query with looser patterns.
- Is **CAMOR** really B2B or B2B+retail? The transaction velocity (~53k tx in April) is much higher than peers and warrants a sanity check before treating it as a clean B2B data point.
- How does this compare to Q1 2026 volume (in `data/payments_icp_q4_workspace_sizing_all_banks.sql`)? April-vs-Q1 trend would tell us whether this concentration is structural or seasonal.
- For the giants (Molinos Nacionales, Mimesa, Protinal): what's the current Tesote relationship status? Are these workspaces we already serve operationally, or distant prospects?
