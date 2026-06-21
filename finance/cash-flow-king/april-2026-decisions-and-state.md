---
title: April 2026 — Categorization Decisions & Open State
tags: [finance, forecasting, cash-flow-king]
updated: 2026-05-13
status: working
---

# April 2026 — Categorization Decisions & Open State

Working notes from the 2026-05-13 session that established the April baseline. Read this first when resuming Cash Flow King work — it has the categorization rules, what was decided, what's blocked, and what's still ambiguous.

## Workspace constants

- **Tesote Finance workspace_id**: `19234e69-781e-45ce-a429-f2d529575a25`
- **VES → USD rate (working)**: 550 Bs/USD
- **Tesote MCP server**: `mcp__tesote-workspace__*` (categorize works, rule create returns 500)

## Category IDs (Tesote Finance workspace)

| Category | id |
|---|---|
| Payroll | cddf9916-5681-42f2-b583-d43b0f798193 |
| Office Expenses | 236e8dd9-f36e-4e6a-ab5c-10ca975a8f66 |
| Software Expenses (created 2026-05-13) | 471a0db1-7c05-4825-b3e2-9fd505f3fc16 |
| Marketing & Sales Expenses | c541ade0-64a6-451a-8038-c57a1c90bf99 |
| Loans & Credit Cards | 561731dd-8226-4e57-9d8b-12b963752a02 |
| Exchange Operations Out | a226a69c-8d73-45a8-9326-2dd5b68ced5d |
| Exchange Operations In | fac7f7b4-f915-413d-ab99-dc87e978a983 |
| Collecting | 279cf94e-3a77-40b0-8ff0-f1388101f237 |
| Internal Transfers In | 630236ce-cb5c-4768-9c38-29a9580d2bb5 |
| Internal Transfers Out | 3dc729f7-3d64-4db7-8063-c017042700d0 |
| Bank Fees | 62a918ea-a784-41c8-9ae7-ce58197afdf0 |
| Taxes | 53b5bae1-1fe1-4b5f-854d-5e683f2acd04 |
| Travels | 067e3ff9-2bb0-4dfd-a70c-80e3c22bad38 |
| Professional Fees | f3723751-c1b9-428f-a8bf-a427989c59df |
| Other Income | 719fbf73-87ca-4ef6-a113-6a174a0ab350 |
| Other Suppliers | 89aef82d-fb37-4991-a1aa-8b115ebf702a |
| Recurring (level 2 tag, unused) | 96846b1a-df45-431b-a974-8c26b951ebe7 |
| Non-recurring (level 2 tag, unused) | a1cbaa85-e72c-42b0-b116-b634318cb3f9 |

## Counterparty → Category mapping (Luis-confirmed, 2026-05-13)

### Payroll
- **Multiplier Tech** (recurring main payroll provider)
- **Gusto** (NET + TAX + FEE, US payroll)
- **Million Web / Sebastian Buza** ($11.3K/mo recurring — was previously "Other Suppliers")
- **Cesar Suarez Luzardo** (USD wire) = **Esteban Suarez** (one person; Tesote wires Esteban's pay to his dad Cesar's account)
- **USD contractors via Rho** (month-end batch): Estefany Gonzalez, Esteban Suarez, Veronica Alvite, Carlos Diaz, Mariel Alvarez (= "Marial Alvarez" per Luis), Majo Diaz (= Maria Jose Diaz), Nicolas Rossini
- **AOFLEX SRL** — initially Payroll, then **moved to Office Expenses** (it's Colombia rent). Last month = May 2026.
- **VES Pago Honorarios** mass batch at month-end (BNC) — Luis confirmed these are payroll portion paid in VES
- **VES Pago Transporte** matched cédulas — also payroll (transport allowance)
- **VES Pago Servicio** (Teresa V010376738) — payroll
- **Rebeca Triana** (Caja Chica $450 4/30) — payroll

### Office Expenses (rent + utilities, steady-state $6.6K/mo)
- **Regus** — $2.3K/mo
- **Dicope Caracas** — $1.8K/mo amortized (actual cash hits quarterly: Apr, Jun, Sep, Dec)
- **Apriori Legal SAS** — Colombia rent. $4K/mo through June, **drops to $1.5K/mo from July** (new entity)
- **AOFLEX SRL** — also Colombia rent, $2.6K/mo through May (last month)
- Small VES recurring (~$1K combined buffer): Condominio Torre Provincial B, Parking 2942, Movistar, Fospuca, Automercado Luz
- **Wilmer Albornoz** (Caja Chica messenger/parking small ops)

### Software Expenses (category id: `471a0db1-7c05-4825-b3e2-9fd505f3fc16`)
- Anthropic family (Claude Team + API + Claude.ai) — biggest line ~$2.8K/mo
- Plaid, OVH, Cursor, Linear, GitHub, AWS, Sentry, Render, Squarespace, Heygen, Better Stack, Loom, Miro, Adobe, Zapier, Slack, Figma, Apollo, Canva, Ahrefs, Gamma, Vacationtracker, Manychat, Metabase, Coderabbit, Digital Ocean, Docusign, hCaptcha, Decodo, Skylight, Amazon (AWS)
- T-Mobile, Amazon Prime, Sejda, Weglot
- Intercom — Luis put under Software in his manual categorization

### Marketing & Sales
- LinkedIn (subs + ads)
- HubSpot
- Dripify (multiple overlapping subs)
- Google ads
- X CORP / Twitter
- Linktree
- Metricool
- Livestorm, Premium Parking (?), Ahrefs (some treat as marketing)

### Loans & Credit Cards
- Rho Card Payment (autopay lumps)
- Mercury IO Autopay (Mercury Credit autopay)
- IO AUTOPAY

### Exchange Operations Out (FX, not operating)
- **GANESH MMXXI** (OTC FX provider, Bs out → USD elsewhere)
- BNC Subasta
- **Daniel Francoeur Pago Daniel 4/30** — Luis manually categorized as Exchange Out

### Exchange Operations In
- **GGBRDB LLC** — FX provider (NOT intercompany, despite previous assumption in analysis-may-2026.md)
- **Cesar Suarez Luzardo Zelle inbound** $1,000 4/23 — employee FX swap (gave USD, got VES)

### Travels
- Castellana Hotel & Spa (Caracas trip hotel)
- Yummy Rides wallet recargas
- Trip-window restaurant/grocery debits 4/26+
- Airlines Rep Xd (Mercury Credit, $4.2K Caracas trip airfare)
- Fiorito Miami (Rho)

### Collecting
- All real customer payments (VES + USD)
- Stripe Collectin
- Curiara Financial Services
- Most "PAGEDI EMISOR" / "PAGO A PROVEEDORES" inflows
- USD wires with "PAGO A PROVEEDOR / PAGO DE FACTURAS" descriptors
- 12 Caja Chica customer collections April

### Internal Transfers In
- **TST SERVICIOS Y CONSULTORÍA** "Fondeo" — TST→TST intra-entity funding (NOT intercompany)
- **Tesote Technologies → Caja Chica** $1.1K April — actual intercompany TST(VE)↔Tesote Tech(US)

## Ambiguous — waiting on Mariel

- **Keyla Hernandez** Pago TST flows (4/7 −$248K Bs, 4/10 −$125K Bs). Currently Exchange Out. Could be payroll or FX swap.
- **Cédula V023190204** — recurring Pago TST patterns, no counterparty assigned. Who is this?
- **Esteban (cédula 26334232)** 4/23 −$310K Bs Pago TST (no CIOPPS so rule didn't match)
- **Inbound USD Zelle from individuals** (Maria de Pinto, Von Road Center, Molina Viajes, Quo Vadis, Grupo Rio Vida, Guuao) — mix of customer payments and employee FX swaps. Need to distinguish.

## Mystery vendor "Pago Factura" rows — need invoice lookup in Odoo

- Pago Factura 1364 (4/13 −$305K Bs)
- Pago Factura 1367 (4/29 −$329K Bs)
- Pago Factura 000274 (4/16 −$1M + −$211K Bs)
- Pago Factura 0510 (4/8 −$1M + −$240K Bs)
- Pago Factura 000495 (4/20 −$58K Bs, CERRAJERIA JB2 counterparty assigned)
- Pago Factura 0437 (4/13 −$64K Bs)
- Pago F000061 Chocolates (4/6 −$89K Bs)

## Blockers to a complete forecast

1. **Card account ingestion** — connect Rho Credit + Mercury Credit to Tesote so line items flow without manual CSV imports
2. **FX rate field** — capture rate per FX swap; affects Bs→USD conversion analysis
3. **MCP rule.create endpoint returns 500** — for now, use direct `transaction.categorize` per txn

## Pre-existing transaction rules that needed fixing

Discovered 5 rules misclassifying contractor "Pago TST" as Exchange Operations Out (should have been Payroll for the contractor portion). Updated to Payroll temporarily, then **reverted to Exchange Out** because Luis flagged that some employees DO swap USD for VES via Pago TST — same description, different semantics. Resolution deferred until Mariel confirms per-cédula classification.

Rules affected (currently Exchange Operations Out):
- Esteban Suarez (cédula 26334232) — rule id `59f50b6b-bd42-4689-9bab-ba27d6c8e899`
- Veronica Alvite (cédula 27111529) — rule id `cb1d4983-0f38-4327-8227-c6dfc77bcd37`
- Estefany Gonzalez (cédula 23638768) — rule id `3099e4f4-9370-493e-b7da-7674872197f3`
- Majo Díaz (cédula 25589672) — rule id `89d893cb-2af8-4839-9840-ffcf3ff9a901`
- Gabriela Pavan (cédula 27072573) — rule id `61f622a8-37f0-47c5-af54-f16a24013ffd`

## Locked April baseline numbers

- Recurring outflow: **$128.8K Apr/May, $126.2K Jun, $123.7K Jul+**
- Real revenue (cash basis April): **$69.2K** (incl. $10.7K Caja Chica)
- Open receivables (April invoiced, not yet collected): **~$20K** ballpark
- Implied April revenue (accrual): **~$89K**
- April operating gap (accrual basis): **−$40K**
- April operating gap (cash basis): **−$60K**

## One-offs in April (don't forecast forward)

- Severance Majo de Armas + Gabriela Pavan: $13K
- Caracas trip airlines: $4.2K (Mercury Credit)
- Caracas trip lodging + meals + ground: $2.7K
- Render.com $1.7K (likely annual)
- Apollo $792 (likely annual)
- Trademark filing: $1.8K
- Smaller software one-offs (Metabase, Digital Ocean, Coderabbit, Sentry, Better Stack): ~$2K
- **Total April one-offs: ~$26K**

## Categorization status

Did not finish categorizing 100% of April. Did:
- 5 misclassified rule updates → reverted to original state
- ~52 direct `transaction.categorize` calls applied (batches 1-5)
- Luis manually categorized many more in Tesote UI between sessions

Still uncategorized:
- The 7 Pago Factura mystery vendors (above)
- Some small VES P2C debits (Pago Movil, Banplus Transf Inmediata)
- The ambiguous Pago TST flows pending Mariel review
