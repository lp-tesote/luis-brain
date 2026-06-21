---
title: AR & Cobros — Finance Team Plan, May 2026
tags: [finance, cobros, ar]
updated: 2026-05-12
status: draft
audience: finance team
---

# AR & Cobros — Finance Team Plan, May 2026

## Context

Tesote's AR pile has grown to where it deserves a focused, structured push. Luis and Roberto are joining Mariel directly on this work, with three intentions:

1. Bring the AR balance down on the biggest outstanding items, starting in VE.
2. Map the full revenue-ops process — subscription invoicing, payment matching, reminders, collections — to understand where the friction lives.
3. Use the work as live input into the Tesote cobros product roadmap.

After two syncs with Mariel on 2026-05-12, the architecture is now locked (see next section). The Finance function will look different on the other side — process, tooling, team shape, or some combination. The work itself surfaced the answer.

## System of record — architectural decision (locked 2026-05-12)

**Tesote = command center. Odoo = execution layer.**

- Tesote is the **first landing place** for everything: invoices (inbound + outbound), contracts, retention vouchers, receipts — anything with finance metadata.
- Tesote is where Mariel (and every future user) works. **Odoo becomes invisible to the end user.**
- Tesote **controls and executes** Odoo: legal invoices, journal entries, tax compliance, fiscalización.
- Applies to: Odoo VE, Odoo DR, eventually Odoo US (post-QB migration).
- Stripe drops out of the cross-entity role entirely; stays only as US card processor.

### Two canonical flows

**Inbound — anything external lands in Tesote first:**

```
Document arrives (email, upload, integration, scan)
        ↓
Lands in Tesote inbox
        ↓
AI extracts + categorizes (vendor, amount, period, GL coding)
        ↓
Mariel reviews / approves (single-step) in Tesote UI
        ↓
Tesote pushes to Odoo with accounting metadata
        ↓
Odoo records the journal entry / vendor bill
```

Applies to: vendor invoices (AP), contracts, retention vouchers, receipts, expense reports, sales orders.

**Outbound — subscription billing loop:**

```
Counterparty + subscription in Tesote → cycle trigger
        ↓
Tesote instructs Odoo to emit invoice
        ↓
Odoo emits → returns invoice to Tesote
        ↓
Tesote routes to customer (email/WA) with payment link
        ↓
Customer pays via Tesote portal (Banesco rails for VE)
        ↓
Payment lands → Tesote reconciles (bank txn ↔ invoice)
        ↓
Tesote writes reconciled state back to Odoo
```

### Mariel's daily reality

- She opens **Tesote**, never Odoo.
- New customer / contract? Created in Tesote → synced to Odoo.
- Vendor invoice email? Lands in Tesote inbox → reviews → pushes to Odoo.
- New contract? Uploaded to Tesote → terms configure the Odoo subscription.
- Billing cycle? Tesote triggers → Odoo emits → Tesote routes.
- Payment arrives? Tesote reconciles → writeback to Odoo.
- AR aging? Tesote dashboard.

Odoo runs the legal/compliance machinery underneath. Mariel never sees it unless she chooses to.

### Mapping to existing product surfaces

```
┌──────────────────────────────────────────────────────────────────┐
│  business/counterparties                                         │
├──────────────────────────────────────────────────────────────────┤
│  The spine: customers + vendors. Entity, subscriptions,          │
│  payment terms, FX rate, contract metadata.                      │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  business/pagos                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Outbound payment execution (Tesote pays vendors via VE rails).  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  business/cobros                                                 │
├──────────────────────────────────────────────────────────────────┤
│  Outbound invoice routing + chase workflow + customer payment    │
│  portal (Banesco rails, Polar pattern).                          │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  automations                                                     │
├──────────────────────────────────────────────────────────────────┤
│  Inbound document inbox + AI extraction + push-to-Odoo.          │
│  The "first landing place" surface. Odoo cockpit framing         │
│  graduates into the command center.                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  connect                                                         │
├──────────────────────────────────────────────────────────────────┤
│  Bank rails feeding the reconciliation engine.                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  ai                                                              │
├──────────────────────────────────────────────────────────────────┤
│  Inbound extraction (invoices, contracts), chase prioritization, │
│  anomaly detection.                                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  dashboard                                                       │
├──────────────────────────────────────────────────────────────────┤
│  Mariel's unified operating view across the whole stack.         │
└──────────────────────────────────────────────────────────────────┘
```

### Resolved architectural decisions

| # | Question | Decision |
|---|---|---|
| 1 | Electronic invoicing in VE — is it on? | **Not yet.** Print/scan/save IS the absence of e-invoicing. The Tesote command center has to accommodate fiscalización compliance through an orchestrated workflow (store the PDF as legal record; physical print + scan if/while still required) until SENIAT e-invoicing is feasible. |
| 2 | Inbound channel design | Email-as-inbox + upload portal for v1. Vendor portal integrations as v2. |
| 3 | AP approval workflow | Single-step. Mariel approves → push to Odoo. Multi-step is v2 if needed. |
| 4 | Contract → subscription translation | AI suggests, human confirms. |
| 5 | Subscription SoR placement | Tesote (counterparty owns subscriptions). Odoo executes accounting. |
| 6 | Multi-entity counterparty | Day-one requirement. One counterparty, N entity-billing relationships. |

### Net-new product work this surfaces

1. **Inbound document inbox** — one-pager: [[../product/automations/accounting-automation/inbound-inbox]]
2. **Outbound invoice routing + customer payment portal** — one-pager: [[../product/business/cobros/outbound-invoice-routing]]
3. **Per-subscription FX rate field** — BCV+differential template, lives on the subscription, not the counterparty.
4. **Multi-entity counterparty schema** — one counterparty, N billing relationships across entities.
5. **Odoo writeback engine** — reconciled invoice + payment posted back to Odoo's journal.

### Spine doc

Architectural commitment + counterparty schema lives in [[../product/business/counterparties/system-of-record]].

## Three buckets

1. **Reduce.** Direct push on the largest outstanding receivables, starting in VE. Already underway (Track 1).
2. **Build the command center.** Architecture locked above. Execution lives in product/ — see the surface map. (Track 2)
3. **Pilot cobros on ourselves.** Use Tesote's own AR as the live dataset for the Tesote cobros product. Highest-conviction beta — we own both sides. (Track 3)

## Context map

| Entity | ERP | Currency | Rails |
|---|---|---|---|
| Delaware C-Corp (US) | QuickBooks (transitioning to Odoo eventually) | USD | Stripe (cards), wires, Zelle, USD cash (Caracas office) |
| Venezuelan entity (TST Servicios) | Odoo VE | BS (BCV-anchored with differential) | VE bank accounts (Banesco rails primary) |
| DR entity | Odoo DR | DOP | DR bank accounts |

Mariel owns the books across all three entities and maintains an AR working spreadsheet ("account forcival" — originally built by Roberto, polished by Mariel) alongside the ERPs.

## Tracks

### Track 1 — Direct outreach on top outstanding invoices (underway)

Luis and Roberto make direct calls and messages on the largest outstanding invoices in VE Odoo, prioritized by $ × days outstanding. Mariel coordinates the prioritized list and tracks outcomes. Each conversation doubles as field research for the cobros product.

**Categorization Luis is applying to the current AR pile:**
- **Current** — recurring active subs, expected to pay (e.g., Mocasas)
- **Pending confirmation** — uncertain status (e.g., UP — usage unclear, no clear invoice agreement)
- **Pending information** — need more context before action
- **Uncollectible** — write-off (Dimasi, MiTiquera, UCI, Consulpagos)
- **Via commercial** — handed to commercial team (Seleccionar el Sur)

**Current scope:** ~$42k base; ~$106k including items under commercial follow-up. Roberto running Euromercado / Sea Bica / Avanti / Forum / UP / Dimasi conversations. Euromercado meeting Wednesday with Chicho + Roberto.

**Call log:**

| Client | Invoice # | Amount | Days outstanding | Channel (call/WA/email) | What they said | Promise | ETA |

Output: a live log + qualitative read on the most common patterns ("always says next week", "lost the invoice", "wants payment plan", "claims already paid").

**Who:** Luis + Roberto, with Mariel
**When:** started 2026-05-12, ongoing

### Track 2 — Build the command center

The "map current state" half is done as of 2026-05-12. We know:

**Sources of truth today (pre-command-center)**
- **Stripe** — manual mirror Mariel maintains by duplicating prior invoices and modifying period/date, then marking paid + payment method. Stripe is NOT doing master record-keeping for VE — it's hand-maintained aggregation labor.
- **Odoo VE** — subscription mechanics + accounting (always calcs at BCV).
- **Mariel's "account forcival" Excel** (Roberto-built, Mariel-maintained) — active client list with action column ("facturar / no facturar", red when overdue). Reviewed daily. Payment-status column NOT current — that lives in Stripe.

**Discovered: current VE subscription invoicing flow** (8 manual steps)

1. Create contact in Odoo VE (mobile + email from sales)
2. Create subscription in Odoo (quote-like; negotiated terms)
3. Generate invoice from the subscription
4. Manual Excel FX calc (paralelo/Binance/euro adjustments — biggest daily pain point)
5. Print the invoice (physical talonario)
6. Scan it
7. Save the scan (fiscalización record)
8. Email client with scanned PDF + payment data (RIF, account info, amount)

**Payment behavior (VE):** ~20% pay within 7 days; majority within ~15 days. Most clients run weekly payment-planning cycles.

**FX standardization (aligned 2026-05-12):**
- Standardize on BCV rate with rate differential pre-baked into the billed USD figure (e.g., $1000 subscription → bill USD equivalent that yields the right BS amount at BCV+differential).
- Auto-calc the BCV adjustment between emission and payment date. Base imponible in USD stays constant; BCV-converted total adjusts at payment.
- Mariel: "ya tienes doble diferencia cambiario" — BCV + differential, both indexed.

**Build half** = the command center, per the System of record section above. Mariel operates Tesote; Odoo runs underneath. The product-side execution lives in:
- [[../product/business/counterparties/system-of-record]] (spine + schema)
- [[../product/automations/accounting-automation/inbound-inbox]] (inbound flow)
- [[../product/business/cobros/outbound-invoice-routing]] (outbound flow)

**Who:** Luis + Roberto + Mariel (Mariel as design partner); product team executes.
**When:** v1 lands in waves through Q3 2026; Track 3 pilot uses earliest workable iteration.

### Track 3 — Pilot Tesote cobros on Tesote AR (product experiment)

Use the VE entity's AR book as the live dataset for testing Tesote cobros. Highest-conviction beta — we own both sides, can move fast, measure honestly, feed every learning straight into the product.

**Refinements from 2026-05-12 sync:**
- **Human chase is non-negotiable.** Bots alone don't move VE clients (Maralak example: María Elena, 5 invoices outstanding, requires personal chase). The cobros workflow needs a human-in-the-loop tier.
- **Bad-payer offer pattern:** for clients who require chase every cycle, offer quarterly/semi-annual billing with a 5% discount instead of monthly. Reduces chase tax.
- **Mariel will deliver:** per-client payment-behavior categorization (Avodon 7-15d, Aragua 15d, etc.) to seed the pilot.

**What to test:**

- **Reminder channels:** WhatsApp vs. email vs. phone call vs. SMS. Measure response rate + days-to-payment per channel.
- **Reminder timing:** N days before due, on due date, N days after. Find the inflection.
- **Reminder tone:** friendly nudge / firm reminder / transactional.
- **Incentives native to Tesote + Odoo:**
  - Pay-by-link directly in the reminder (Banesco rails)
  - Early-payment discount baked into Odoo
  - Auto-escalation if no response in N days
  - Payment plans for stuck cases
- **Per-client tracking:** channel that worked, # of touches, what closed it, lessons.

**Context for the product:** the AR problem isn't unique to Tesote. Every business in VE has it — the whole country runs on slow-paying receivables, across every sector and size. The workflow that solves it for us should solve it broadly.

**Who:** Luis + Roberto run the experiment; Mariel feeds dataset; learnings feed the cobros product roadmap.
**When:** starts as soon as Tracks 1-2 produce a clean target list and a sane invoicing baseline.
**Output:** dataset of what works for VE collections + concrete spec for the cobros product.

## Decision gates

- **Gate 1 (Track 1):** Has AR materially reduced on the prioritized list? Documentation of what worked / what didn't.
- **Gate 2 (Command center v1):** Mariel operating entirely in Tesote for at least one full subscription cycle, end-to-end (inbound + outbound) for the VE entity.
- **Gate 3 (Track 3):** Has the cobros workflow demonstrably shortened days-to-payment on a meaningful sample? If yes, productize and roll out.

## Hiring

**Catherine hire paused 2026-05-12.** Get involved, restructure the systems, then decide what role we actually need. Same playbook as Stefi in implementation. Not a no — just a hold until the foundations are sorted.

## Questions to align on

(Most resolved 2026-05-12 — keeping the open ones)

Resolved:
- ✓ Does the working sheet cover all 3 entities? — Mariel's "account forcival" covers VE active subscriptions. Stripe holds cross-entity (manually maintained mirror).
- ✓ Is the working sheet the source of truth? — No. Stripe is the manual mirror; "account forcival" is the action-trigger working file. The new SoR will be Tesote.
- ✓ How often is it updated? — Daily.
- ✓ How is the next invoice date tracked? — "account forcival" action column, red flag when overdue.
- ✓ Do Odoo VE / DR have reminder/dunning workflow? — No. Currently all manual.
- ✓ Are BS-denominated invoices revalued? — Manual today; auto-calc with BCV + differential is the design move.

Still open:
- Who in client orgs typically pays us — finance, ops, the CEO directly?
- Top 3 most painful clients to chase — Maralak called out; full list TBC from Mariel.
- One thing the Finance team would fix tomorrow if it could.
- One thing the team does today that should be done by a machine or a different person.

## Meeting notes

### 2026-05-12 first sync (Luis + Mariel) — ~30 min

Walked the AR pile + the current invoicing process. Key alignments:

- **Priority:** AR → bank recon → AP. AP in VE is small/manageable (few providers, few invoices). Only annoyance is loading them into Odoo with retentions.
- **Catherine:** paused (see Hiring section).
- **VE invoicing — standardize on BCV with rate differential pre-baked.** Mariel had been juggling BCV/paralelo/Binance/euro manually with ugly conversions (e.g., 2785.90) that looked suspect. Both aligned.
- **Discovered the 8-step manual invoicing flow** (above in Track 2).
- **Payment behavior pattern**: contract says 7 days, Mariel sets immediate in Odoo. ~20% pay within 7 days, majority within 15.
- **Bot-only chase won't work** — must have a human calling. Maralak / María Elena cited as canonical example.

### 2026-05-12 second sync (Stripe deep-dive) — ~6 min

Mariel walked through her Stripe workflow:
- Emits BS invoice in Odoo VE
- Goes into Stripe → duplicates a similar prior invoice → modifies period/date → finalizes as "informational"
- When payment lands, reconciles in BOTH Odoo (real) and Stripe (mirror) — marks paid + adds payment method ("Binance Bench") + date

**Implication:** Stripe is not doing master record-keeping for VE. It's hand-maintained aggregation labor. The "duplicate prior invoice → modify" pattern is itself a manual workaround for recurring subscriptions.

Mariel pointed to the Tesote product directly: "tienes un módulo de facturación, también tienes las transacciones" — the surfaces Tesote needs to replace Stripe's aggregator role already exist on the product side. This confirms Path A (Tesote-as-SoR) is cheaper than initially modeled, because we're not replacing a working system — we're replacing manual labor.

### Open items from the syncs

- Luis to digest "account forcival" sheet and propose how Tesote sits above it as the unified layer (now resolved by the System of record section above).
- Roberto running outreach conversations on Euromercado / Sea Bica / Avanti / Forum / UP / Dimasi.
- Mariel will deliver per-client payment-behavior categorization for Track 3 pilot seeding.
