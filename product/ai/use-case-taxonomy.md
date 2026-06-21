---
title: Tesote AI — use-case taxonomy (v0.1)
tags: [product, ai, automations, finance, taxonomy]
updated: 2026-05-22
status: draft
---

# Tesote AI — use-case taxonomy

> Internal map. Not a gallery, not a spec. The thing we use to decide **what to build next** and **on which surface**.

## Frame

Two axes:

- **Job-to-be-done** — what the finance team is actually trying to accomplish (not "department", because VE finance teams are 1-3 people wearing all hats).
- **Execution mode** — how the work gets done. This is the axis the current gallery hides.

The four execution modes:

| Mode | Trigger | Human in the loop? | Lives on which surface |
|---|---|---|---|
| **Autopilot** | Event (txn arrives, invoice posted, etc.) | No — fully trusted rule | **Automations** ([[../automations/]]) |
| **Draft & approve** | Event | Yes — system pre-stages a draft, human approves | **Automations** (queue) + AI chat (configure) |
| **Scheduled** | Cron / calendar | Optional — depends on output | **Automations** (jobs) |
| **On-demand chat** | User asks | Yes (the user is *driving*) | **AI chat** ([[../ai/]]) |

**Architectural rule:** if a workflow can be specified deterministically, it should *not* live as a chat prompt. It should be a rule in Automations. The chat is for (a) ad-hoc questions, (b) configuring/inspecting the rules in Automations, and (c) genuinely judgment-call work that can't be specified in advance.

Most of what's in the current gallery (BCV lookup, recurring invoices, "post bill", "categorize CANTV") is actually Automations work that's been awkwardly stuffed into chat because Automations isn't built yet.

## Jobs-to-be-done

Twelve jobs. Each one is a section. Within a section, workflows are listed by execution mode.

The same workflow can appear under multiple jobs (e.g., "match bank txn to Odoo entry" shows up under both *Reconcile banks* and *Close books*). I'm OK with that for now — taxonomy is a graph, not a tree.

---

### 1. Close the books

Monthly close. The single biggest pain point in VE finance teams — wraps up bookkeeping, FX, reconciliation, and reporting into a deadline.

**Autopilot**
- Auto-categorize transactions matching saved rules (description, counterparty, amount band)
- Auto-link bank movements to existing Odoo entries when amount + date + counterparty match exactly
- Auto-create accrual JE for recurring monthly expenses (rent, software subs)

**Draft & approve**
- On new transaction with no rule: draft a categorization + counterparty assignment based on history; queue for approval
- On unreconciled bank movement: draft a matching Odoo entry; queue for approval
- Month-end: draft FX revaluation JE for VES-denominated balances at month-end BCV; queue for approval
- Month-end: draft closing entries (depreciation, accruals); queue for approval

**Scheduled**
- Daily: run reconciliation pass, flag exceptions
- Day -3 / day 0 of close: pre-build the close checklist with current exception count

**On-demand chat**
- "¿Qué falta para cerrar mayo?" → checklist of unreconciled txns, missing invoices, pending approvals
- "¿Por qué el saldo de la cuenta X no cuadra?" → diff bank vs Odoo, list discrepancies
- "Cerrá mayo" → run the full close sequence, surface exceptions, ask for decisions

---

### 2. Pay vendors (AP)

Bill ingestion → validation → approval → payment execution → confirmation.

**Autopilot**
- On supplier email with PDF: extract bill, match to existing PO, draft `account.move` in Odoo as `in_invoice`
- Apply IVA + retenciones based on supplier RIF + line items (rule-based, deterministic in VE)
- Auto-attach the source PDF to the Odoo bill record

**Draft & approve**
- Draft bill posted → notify approver → on approval, post to Odoo
- Draft payment batch for vendors with bills due in next N days
- Draft remittance email to vendor with payment confirmation + invoice reference

**Scheduled**
- Weekly: AP aging report; flag bills approaching due date
- Daily: scan supplier inboxes (if configured) for new bills

**On-demand chat**
- "Cargá esta factura en Odoo" (PDF attached) — already shipped
- "¿A quién le debo más?" → top creditors by outstanding amount
- "¿Qué facturas vencen esta semana?"
- "Pagale a [vendor] $X" → draft payment, route through approval, execute on bank rail (when payments shipped)

> **Card spend is AP-adjacent but lives under [[#7-tax-compliance-seniat-ve|Tax compliance § Gastos deducibles]]** — because the binding constraint is the SENIAT receipt (legal name + RIF), not the payment mechanics. Every corporate-card or debit-card purchase triggers the receipt-chase workflow described there.

---

### 3. Collect from clients (AR + cobros)

Invoice generation → delivery → payment matching → dunning → cash application.

**Autopilot**
- Generate recurring invoice on subscription anniversary; apply BCV rate of the day; post to Odoo
- Email the invoice PDF to client billing contact on post
- On incoming payment matching invoice amount + reference: auto-apply to invoice, mark paid

**Draft & approve**
- On incoming payment with partial match (amount but not reference): draft cash application against most-likely invoice; queue for approval
- On overdue invoice (day 7, 15, 30, 45, 60): draft dunning email tailored to client tier + history; queue for approval
- On client requesting credit note: draft credit note in Odoo with calculation + reason; queue for approval

**Scheduled**
- Weekly: AR aging report by client tier
- Monthly: collections forecast based on payment history
- Daily: scan incoming bank movements for client payments

**On-demand chat**
- "Postá la factura de [client]" — already shipped
- "¿Quién me debe más?" → top AR balances
- "Mandale recordatorio a [client]" → draft dunning email in [[feedback_client_email_spanish_voice|Luis's Spanish voice]]
- "¿Cuánto facturé en mayo?" — already shipped

#### 3.a Comprobantes de retención (when client is contribuyente especial)

When you invoice a contribuyente especial, they pay you net of an IVA/ISLR retention — but the retention is only usable as a fiscal credit if they send you the formal *comprobante de retención*. No comprobante = the withheld amount becomes a real loss, not a credit. So there's a chasing workflow that runs in parallel with normal AR.

**Autopilot**
- Tag each invoice issued to a contribuyente especial with "comprobante expected" + expected retention % (IVA / ISLR per VE rules)
- On bank receipt of net payment from contribuyente especial: detect the short-pay vs invoice face value = implied retention
- Open a pending "comprobante expected" record linked to the invoice + payment

**Draft & approve**
- Within N business days of payment receipt with no comprobante: draft follow-up email to client AP contact
- On comprobante PDF/XML arrival (email/upload): match to the pending record; draft the cash application that books retention as fiscal credit; queue for approval

**Scheduled**
- Weekly: list of pending comprobantes by client, days outstanding, amount at risk
- Pre-close: blocking list of paid invoices missing comprobante

**On-demand chat**
- "¿Qué comprobantes de retención me deben?"
- "Mandale recordatorio a [client] por el comprobante de la factura X"
- "¿Cuánto crédito fiscal estoy esperando en comprobantes pendientes?"

---

### 4. Reconcile banks

Daily ops. Bank movement ↔ Odoo entry matching. The single most automatable job in VE finance.

**Autopilot**
- Apply category from rule (description match, counterparty match)
- Auto-match to Odoo invoice/bill when amount + counterparty + date all align
- Skip / auto-mark internal transfers (bank A → bank B same workspace) so they don't get double-counted

**Draft & approve**
- Draft a category + counterparty for any txn matching prior patterns (history-based, not a hard rule)
- Draft a new rule when the same un-ruled pattern appears N times
- Draft a counterparty record when an unknown name appears repeatedly

**Scheduled**
- Hourly / 4×daily: pull fresh bank movements (already a [[../connect/|Connect]] job)
- Daily: reconciliation pass + exception count to user

**On-demand chat**
- "¿Cuántas transacciones sin categorizar tengo?"
- "Categorizá todas las de CANTV" — already shipped
- "Creá regla: NOMINA → Sueldos" — already shipped
- "Mostrame las transacciones raras de mayo" → anomaly detection (amount outside normal band for that counterparty, new counterparty above threshold, etc.)

---

### 5. Manage cash & FX

Daily treasury. Balances, FX rates, conversions, intercompany.

**Autopilot**
- Refresh BCV rate daily from official source; store in `exchange_rates`
- Apply current rate to all USD-equivalent calculations workspace-wide
- Re-value VES balances to USD on every dashboard load
- Lock historical rates per-transaction (already a treasury invariant — never re-compute)

**Draft & approve**
- On manual FX rate override (paralelo, contractual): draft `workspace_exchange_rate` entry with audit row; require explicit confirmation
- On large intercompany transfer (e.g., VDT → TST): draft both sides of the JE; queue for approval

**Scheduled**
- Daily: balance snapshot per bank + currency
- Weekly: FX rate history report (BCV vs paralelo vs contractual delta)

**On-demand chat**
- "¿Cuál es la tasa BCV de hoy?" — already shipped
- "Mostrame mis saldos por banco hoy" — already shipped
- "Guardame la paralelo a 47.5" — already shipped
- "¿Qué tasa usé el lunes pasado?" — already shipped

---

### 6. Forecast cash

Treasury / CFO. The "do we have runway?" question, weekly and monthly.

**Autopilot**
- *(Almost nothing — forecasting is inherently judgment-driven)*
- Maintain rolling 13-week cash projection from confirmed AP + AR aging + recurring revenue

**Draft & approve**
- *(Forecasts are user-driven; system drafts scenarios but never commits them)*

**Scheduled**
- Monday morning: 13-week cash forecast snapshot delivered to CFO inbox
- Month-end: projected vs actual variance report

**On-demand chat**
- "¿Cuánto cash me queda?"
- "Si pago todas las facturas vencidas, ¿con cuánto me quedo?"
- "Simulá: ¿qué pasa si [client] paga 15 días tarde?"
- "¿Cuándo me quedo sin caja al ritmo actual?"
- "Compará cash flow real vs proyectado de los últimos 3 meses"

---

### 7. Tax compliance (SENIAT, VE)

IVA, ISLR, retenciones, libros de compras/ventas. Highly deterministic — the rules are codified. Mostly automatable.

**Autopilot**
- Calculate IVA per invoice (debit 16%, credit 16%) based on line items and supplier/client RIF status
- Calculate ISLR retention on supplier payment based on RIF type + payment band
- Maintain libro de compras and libro de ventas as txns post

**Draft & approve**
- Monthly: draft declaración de IVA (forma 30) from libros; queue for review before submission
- Monthly: draft declaración de retenciones (forma 99074); queue for review
- Quarterly / annually: draft ISLR; queue for review

**Scheduled**
- 1st of month: assemble prior-month libros for review
- Filing deadlines: alert user N days before due date

**On-demand chat**
- "¿Cuánto IVA debo este mes?"
- "Mostrame el libro de ventas de mayo"
- "¿Qué facturas no tienen retención cargada?"
- "Validá los RIFs de mis clientes nuevos" → scrape SENIAT registry, flag mismatches

#### 7.a Gastos deducibles (card spend → SENIAT-valid receipt)

**The economic stakes:** every USD of card spend either (a) reports a deducible gasto with a SENIAT-valid receipt (legal name + RIF) and yields a ~37% tax credit at year-end, (b) reports a deducible gasto without a valid receipt and exposes us to a SENIAT audit blow-up, or (c) skips reporting and loses the 37% credit outright. The whole job is making sure every card spend lands in (a).

A SENIAT-valid receipt for a corporate expense must carry **the company's legal name + RIF**. No name = invalid. No RIF = invalid. Wrong name = invalid. The vast majority of card spend in the wild has none of this unless someone asks the merchant at point of sale.

**Autopilot**
- On any card-account txn (debit/credit): create a pending "receipt required" record linked to the txn (merchant, amount, date)
- On receipt arrival (email forward, photo, PDF upload, mobile capture): OCR + extract legal name + RIF + amount + date
- Validate: if (a) name matches one of our legal entities exactly and (b) RIF matches → mark `deducible-eligible: yes`, attach to txn, route into libro de compras
- If name or RIF mismatch / missing → mark `deducible-eligible: no`, log reason, keep the file attached for audit trail
- Match receipt to the txn by amount + date + merchant + cardholder

**Draft & approve**
- For card txns with no receipt N days after the spend: draft outreach to the cardholder ("send receipt for $X on $date at $merchant — needs to have [legal name] and RIF [J-XXXXXXXX-X]")
- For ambiguous OCR (low confidence on RIF or name): draft a "is this our company?" verification before marking deducible
- Pre-close: draft a single approval batch of all card spends with valid receipts → flip to deducible in one shot

**Scheduled**
- Daily: list card spends with no receipt, surfaced to the cardholder + finance lead
- Weekly: receipt-chase digest by cardholder (who's behind, by how much $)
- Pre-close: blocking list of card spends with no SENIAT-valid receipt; quantify the lost tax credit if we close without them

**On-demand chat**
- "¿Qué compras con tarjeta no tienen recibo?"
- "¿Qué tan deducible es mi gasto del mes?" → ratio of deducible-eligible / total card spend, in $
- "¿Cuánto crédito fiscal estoy dejando sobre la mesa este año?" → ~37% × non-deducible card spend YTD
- "¿A quién le falta enviar recibos?" → grouped by cardholder
- "Mostrame los recibos con nombre/RIF incorrecto" → recoverable: ask merchant to re-emit
- "¿Cuál es la exposición SENIAT de mi gasto deducible actual?" → reported-as-deducible-but-missing-valid-receipt

> **Why this is a Tesote AI killer use case:** the company is *already* losing 37% on every dollar of card spend without a valid receipt. Finance teams know it and don't fix it because chasing receipts is the worst job in the building. Tesote knows the txn the moment it hits the bank feed and can chase the receipt automatically — turning "receipt management" from a manual nightmare into a background process. The ROI math sells itself: customer spends $50k/year on cards, recovers 37% of it (~$18.5k) in tax credits they were already entitled to but losing.

#### 7.b Comprobantes de retención (received side — pairs with [[#3a-comprobantes-de-retención-when-client-is-contribuyente-especial|3.a]])

This is the *consumption* side of the comprobantes flow. § 3.a chases the document from the client; this section applies the document to our fiscal position once received.

**Autopilot**
- On validated comprobante de retención arrival: apply the retention as a credit against IVA debit (or ISLR liability) in the relevant period
- Update the libro de ventas with the comprobante reference
- Reduce open AR balance on the originating invoice by the retention amount (so the invoice closes cleanly)

**Draft & approve**
- Pre-close: surface invoices with retentions expected but no comprobante received → quantify the at-risk fiscal credit

**On-demand chat**
- "¿Cuánto crédito fiscal por retenciones aplicado este mes?"
- "Mostrame las retenciones aplicadas pero sin comprobante todavía" → at-risk credits
- "Mostrame el reporte de retenciones del mes" → libro-style summary

---

### 8. Regulatory compliance (BCV, banks, AML)

Bank-side reporting, FX compliance, KYC touchpoints. Lower volume than tax, higher stakes per event.

**Autopilot**
- Flag transactions above reporting thresholds (per BCV / per bank rules)
- Tag operaciones cambiarias for separate reporting bucket

**Draft & approve**
- Draft bank-side regulatory submission (when applicable) for large or cross-border movements
- Draft KYC update packet when client/vendor info ages past N months

**Scheduled**
- Monthly: regulatory checklist surfaced to CFO / compliance owner
- Per-bank: submission deadlines tracked

**On-demand chat**
- "¿Qué movimientos del mes pasan el umbral de reporte?"
- "Buscame la última carta KYC que mandé a [bank]"

---

### 9. Maintain master data

Vendors, clients, chart of accounts, RIFs, bank accounts. Boring but critical — bad master data is what breaks everything else.

**Autopilot**
- On new counterparty detected in bank feed: create stub `res.partner` in Odoo with name + RIF (when extractable) — flagged as "auto-stub, needs review"
- Dedupe candidates on insert (fuzzy name + RIF match)

**Draft & approve**
- Draft a merge proposal when two counterparties look like the same entity
- Draft an enrichment pass: RIF validation, bank info validation, address standardization

**Scheduled**
- Weekly: master data hygiene report (missing RIF, missing bank info, duplicate candidates)

**On-demand chat**
- "Buscame el partner de [client] en Odoo" — already shipped
- "Creá el partner para [new client] con estos datos"
- "Estos dos contactos son el mismo, fusionalos"
- "Validá los datos bancarios de mis top 20 vendors"

---

### 10. Report up

CEO, board, investors. The deliverables Luis personally consumes / sends. Includes the cash flow reporting that the CFO/controller produces for the CEO.

**Autopilot**
- *(Nothing for narrative reports — they need framing)*
- Maintain rolling cash-in / cash-out totals by category (the underlying data for the reports below — fed by the categorization rules from § 4)

**Draft & approve**
- Draft monthly investor snapshot (per [[../../drafts/investor-update-q1-april-snapshot|the current investor-update format]]); queue for Luis to edit
- Draft board memo from KPI snapshot
- Draft Q&A appendix from common investor questions + current numbers

**Scheduled**
- 1st of month: assemble prior month numbers (recurring + total revenue, MoM %, runway, cash, AR/AP) into draft snapshot
- 1st of month: cash flow statement (money in / money out by category) for prior month, auto-built from categorized transactions
- Quarterly: assemble board pack drafts (incl. quarterly cash flow rollup)
- Weekly: CEO Monday briefing (cash, top exceptions, decisions needed)

**On-demand chat — narrative reports**
- "Armame el investor update de mayo" → pull KPIs, draft narrative, attach charts
- "¿Cómo vamos vs el último update?"
- "Compará abril vs mayo en una tabla"
- "¿Qué le digo a [investor] sobre [topic]?" → use [[feedback_investor_comms_competitor_adjacent|investor-comms rules]] + memory of what was already shared

**On-demand chat — cash flow by category**
- "Mostrame entradas y salidas de mayo por categoría"
- "¿En qué gasté más este mes?" → top expense categories with absolute $ and % of total
- "Compará gastos de mayo vs abril por categoría" → variance table, biggest movers first
- "¿Cuánto gasté en [category] año a la fecha?"
- "Armame el cash flow statement de mayo" → full money-in / money-out by category, ready to ship
- "¿Cuáles son mis gastos recurrentes vs one-off?" → split fixed-cost base from discretionary
- "¿Qué categorías están creciendo más rápido?" → MoM growth rate per category, ranked

---

### 11. Investigate / audit

Controller, CFO. "Why is this off?" The genuinely judgment-driven, probabilistic work.

**Autopilot**
- *(None — investigation is the user driving)*

**Draft & approve**
- *(Rare — maybe surface suspicious patterns for review)*

**Scheduled**
- Weekly: anomaly digest (txns outside historical norms, unusual counterparties, large rounding patterns)

**On-demand chat**
- "¿Por qué el saldo de [account] cambió tanto este mes?"
- "Mostrame todas las transacciones con [vendor] del último año"
- "¿Qué pasó con [invoice ID]?"
- "Compará margen por categoría: este mes vs hace 3 meses"
- "Sospecho que hay duplicados en [account]; encontralos"
- "¿Cuál fue el cambio más grande en mi P&L este mes vs el pasado?"

---

### 12. Payroll touchpoints

*(Not full payroll — HR / nómina software owns the calculation. Finance touches the bookkeeping side.)*

**Autopilot**
- On nómina-tagged bank movement: split into employee-level entries per rule; book to Sueldos / cargas sociales
- Reconcile aggregate nómina disbursement to the source nómina run

**Draft & approve**
- Draft month-end nómina accrual (vacaciones, utilidades, prestaciones)
- Draft retención de ISLR sobre nómina entries

**Scheduled**
- Monthly: nómina recon checklist before close

**On-demand chat**
- "¿Cuánto pagué en nómina este mes?"
- "¿Cuánto debo en prestaciones acumuladas?"

---

## Cross-cutting meta-patterns

A few patterns repeat across multiple jobs and deserve naming, because they imply shared infrastructure rather than per-job builds:

### Documentary evidence management

Surfaced explicitly in §§ 3.a, 7.a, 7.b — but also implicit in § 2 (supplier invoices), § 7 (libros), § 9 (RIF docs). The pattern: a transaction or claim exists in our books, and a *specific document* with *specific fields* (legal name, RIF, signature, comprobante number, etc.) must be on file for the transaction to be defensible to SENIAT / a bank / an auditor.

Tesote AI's job is: (1) know what document is expected for each transaction, (2) chase it when missing, (3) validate it when received, (4) attach it to the transaction record, (5) make it retrievable on demand. This is the core of "we're SENIAT-fluent."

**Shared infrastructure this implies:**
- Per-txn "documents expected" model (who/what/when/why a doc is expected)
- Receipt/document ingestion pipeline (email forward, mobile photo, PDF upload) with OCR + field extraction
- Validation rules per document type (gasto deducible = name+RIF match; comprobante de retención = match invoice + amount + period; supplier invoice = RIF + IVA breakdown; etc.)
- A single "documents at risk" surface across all the workflows above — pre-close blocking list

This is probably the single highest-leverage thing to build in Automations, because it unblocks the financial-stakes workflows (§§ 7.a, 7.b, 3.a) that have the cleanest customer ROI story.

### Categorization as substrate

§§ 1, 4, 5, 6, 10 all depend on transactions being categorized correctly. The rules system (§ 4) is the substrate; everything else is reporting on top. Worth treating categorization rules as the first thing to ship cleanly in Automations — every other automation degrades if this is weak.

### Reconciliation as substrate

§§ 1, 2, 3, 4, 5, 7, 12 all assume bank movements have been matched to Odoo entries. Reconciliation isn't really a "job" the user does — it's an invisible substrate that, when working, makes every other report trustworthy. Probably belongs as background autopilot, never as a primary chat surface.

## Cross-cutting tags

Each workflow above should carry these tags in the eventual ticketed version. Not adding them inline yet (would clutter the draft); list lives here as a checklist for v0.2:

- **Trust level** — `deterministic` (rule, fully specified) / `mostly-deterministic` (rule + lookup) / `probabilistic` (LLM judgment)
- **Reversibility** — `easy-undo` (delete a draft, override a rate) / `hard-undo` (post to Odoo, send an email, execute a payment)
- **Data dependencies** — bank feed / Odoo / SENIAT scrape / FX feed / email inbox / external CRM
- **Multi-tenant** — workspace-scoped / global (BCV rate is global, paralelo override is workspace)
- **Jurisdiction** — VE-only / cross-jurisdiction (per [[project_connect_multi_jurisdiction|Connect supports VE+PA+RD+US+Caribe]]; most of the above is VE-only, but reconciliation + master data + reporting are jurisdiction-agnostic)
- **Owner role** — AP / AR / treasury / controller / tax / CFO (secondary axis — useful when sizing a feature against a customer's org chart, not as a primary organization)

## Surface decisions implied by this taxonomy

1. **Automations needs to exist as a real surface.** Right now everything is being forced into chat. Most of jobs 1-9 above are 70%+ Automations work, not chat work. This taxonomy makes that obvious.

2. **The Automations surface needs at minimum:**
   - Rules list + activation status (current gallery has "¿Qué reglas tengo activas?" — that's chat-as-a-debug-tool; should be a first-class UI)
   - Drafts queue (the "draft & approve" mode needs a real queue; today it's implicit in chat history)
   - Scheduled jobs view (cron-style — what's running, when, last result)
   - Event log / audit trail (what fired, on what input, with what outcome)

3. **The AI chat is left with:**
   - Genuinely ad-hoc analytical questions (jobs 6, 11, big chunks of 10)
   - Configuring/inspecting Automations (the natural language → rule path stays here)
   - Document-driven workflows (PDF in, action out) — these are user-driven by definition

4. **Gallery cards should be derived from this list, not the other way around.** The gallery surfaces the *common entry points* into chat — not the catalog of capabilities. If a workflow's primary home is Automations, the gallery card for it should route the user to "configure this rule" not to "do this once".

## Open questions

- **Job 6 (forecast)** — does this need its own UI surface (a forecast / scenario tool) rather than living in chat? Most CFOs want a model, not a chat. Park for later.
- **Job 10 (report up)** — Luis is *the customer* here. Is the goal to ship this to other CFOs, or keep it as Luis's internal usage that informs the product later?
- **Cross-jurisdiction tagging** — Connect spans VE+PA+RD+US+Caribe but most automation logic (IVA, retenciones, SENIAT) is VE-only. Should the taxonomy carry a column for jurisdiction, or do we ship VE-first and refactor when PA/RD/US customers ask?
- **Owner-role axis** — worth adding once a customer with a 5+ person finance team asks "who in my team uses what?". Until then it's overhead.
- **Anomaly detection (jobs 4, 11)** — does this belong in Automations as scheduled, in chat as on-demand, or both? Probably both with shared underlying detector.

## Next moves

- (a) Validate this list with a real finance team member (Mariel? someone at PTCK / VDT?) — what's missing, what's duplicated, what's the most painful job not yet listed
- (b) Pick 1-2 jobs to deepen into the [[../automations/erp-ai/flagship-workflows|flagship-workflows]] format — fully-choreographed end-to-end specs ready for `/tesote-plan`
- (c) Once Automations surface scope is locked, derive its IA from this taxonomy

## Related

- [[../automations/erp-ai/flagship-workflows]] — the deeper 6-workflow choreography (where this taxonomy points for "ready to build")
- [[pitch-agents-plus-ai]] — the customer-facing version of the two-layer Agents+AI frame
- [[positioning-the-finance-chief]] — the *why* (what posture this taxonomy is serving)
- [[tesote-ai-design]] — the current chat surface dossier (what's already built)
- [[../tesote-2026-command-center-prd]] — the architecture this all plugs into
