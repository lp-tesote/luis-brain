---
title: Tesote as System of Record — the command center spine
tags: [product, counterparties, architecture, sor]
updated: 2026-05-12
status: draft
---

# Tesote as System of Record — the command center spine

> **Purpose.** Capture the architectural decision locked on 2026-05-12: Tesote becomes the system of record on top of Odoo (VE, DR, eventually US post-QB). Counterparties is the spine of that layer. This doc holds the canonical loops, the schema, and the cross-surface map.
>
> **Origin.** Two syncs with Mariel (finance, VE) on 2026-05-12 surfaced that Stripe was acting as a hand-maintained mirror — not a working SoR. Replacing it with Tesote is cheaper than first modeled because we're replacing manual labor, not a functioning system. See [[../../../finance/ar-and-cobros-2026-05-team]] for the full discovery trail.

---

## The architectural decision

**Tesote = command center. Odoo = execution layer.**

- Tesote is the **first landing place** for everything: invoices (inbound + outbound), contracts, retention vouchers, receipts — anything with finance metadata.
- Tesote is where the user (Mariel, in our dogfood case; the customer's controller / CFO / clerk in production) actually works. **Odoo becomes invisible to the end user.**
- Tesote **controls and executes** Odoo: legal invoices, journal entries, tax compliance, fiscalización.
- Applies to: Odoo VE, Odoo DR, eventually Odoo US (post-QB migration).
- For ICP customers: same shape — Tesote sits above whatever ERP(s) they run.
- Stripe drops out of the cross-entity role entirely for VE; stays only as US card processor where relevant.

### Why this works now

- Tesote is on the payment rails (Banesco etc. via [[../../connect]])
- VE banking transactions flow through Tesote already
- Near-immediate reconciliation against Odoo becomes mechanical, not human

### Why not centralize in Odoo

- Odoo UI/UX doesn't work for multi-entity, multi-jurisdiction operators
- Our ICP is exactly this profile — overseas-entity operators who need one place to see everything
- **Our pain = our customer's pain.** Dogfooding the command center on Tesote's own books IS the product validation.

---

## Two canonical flows

### Inbound — anything external lands in Tesote first

```
Document arrives (email, upload, integration, scan)
        ↓
Lands in Tesote inbox
        ↓
AI extracts + categorizes (vendor, amount, period, GL coding)
        ↓
User reviews / approves (single-step) in Tesote UI
        ↓
Tesote pushes to Odoo with accounting metadata
        ↓
Odoo records the journal entry / vendor bill
```

**Applies to:** vendor invoices (AP), contracts, retention vouchers, receipts, expense reports, sales orders, anything else external with finance meaning.

**Detailed spec:** [[../../automations/accounting-automation/inbound-inbox]]

### Outbound — subscription billing loop

```
Counterparty + subscription in Tesote → cycle trigger
        ↓
Tesote instructs Odoo to emit invoice
        ↓
Odoo emits → returns invoice (with legal + tax structure) to Tesote
        ↓
Tesote routes to customer (email/WA) with payment link
        ↓
Customer enters Tesote portal → pays via Tesote rails
        ↓
Payment lands → Tesote reconciles (bank txn ↔ invoice)
        ↓
Tesote writes reconciled invoice + payment back to Odoo
```

**Applies to:** subscription billing, one-off billing, anything Tesote (or our customer) needs to invoice out.

**Detailed spec:** [[../cobros/outbound-invoice-routing]]

---

## Counterparties as spine

The counterparty record is the connective tissue of the whole loop. Every flow above reads from and writes to it.

### Schema (v1 working spec)

A **counterparty** is an entity (company or individual) we transact with. It can be a customer, a vendor, or both. It has:

**Identity**
- Legal name (razón social)
- Commercial name (if different)
- Tax ID (RIF for VE, RNC for DR, EIN for US)
- Country of registration
- Default contact (email + phone/WhatsApp)
- Roles: `customer`, `vendor`, `both`

**Billing relationships** (1 counterparty → N billing relationships)

Each billing relationship links the counterparty to one of *our* entities:

| Field | Notes |
|---|---|
| `our_entity` | TST Servicios (VE) / Tesote Technologies (US) / TST DR (DR) |
| `relationship_role` | `customer_of`, `vendor_of`, `both` |
| `payment_terms_default` | e.g., "immediate", "7 days", "15 days", "EOM+30" |
| `preferred_payment_channel` | wire, ACH, Zelle, Banesco, Stripe card, cash |
| `legal_address` | per-jurisdiction billing address |
| `notes` | free text |

This is the **multi-entity counterparty schema** — one counterparty (e.g., a group like Polar) can bill from both VE and US entities. Day-one requirement.

**Subscriptions** (1 billing relationship → N active subscriptions)

| Field | Notes |
|---|---|
| `product` | what they're paying for (links to product catalog when that exists) |
| `cadence` | monthly / quarterly / semi-annual / annual / custom |
| `next_invoice_date` | computed; the action-trigger field |
| `base_amount` + `base_currency` | the canonical amount + currency negotiated |
| `fx_rate_rule` | how to convert at invoice time — see FX section below |
| `terms_override` | overrides the billing-relationship default if needed |
| `status` | active / paused / cancelled |
| `contract_ref` | pointer to the source contract (see Contracts) |

Subscription is **owned by Tesote**, not Odoo. Odoo executes the accounting; Tesote owns the commercial relationship.

**FX rate (per-subscription field)**

Lives on the subscription, not the counterparty, because the same customer can have different rate terms on different subscriptions.

| Field | Notes |
|---|---|
| `fx_source` | `BCV`, `BCV+differential`, `paralelo`, `custom`, `none` (single-currency) |
| `fx_differential_bps` | when `BCV+differential`: the markup in basis points (e.g., 3000 = 30%) |
| `fx_freeze_at` | `emission` / `payment` — when the rate is locked |

VE default: `BCV+differential`, `fx_freeze_at: payment` — auto-calc the adjustment between invoice emission and payment date, base imponible in USD stays constant, BCV-converted total adjusts at payment. Aligned with Mariel 2026-05-12.

**Contracts** (1 counterparty → N contracts)

| Field | Notes |
|---|---|
| `file` | the uploaded contract PDF |
| `extracted_terms` | AI-extracted: parties, scope, term length, renewal, payment terms, FX |
| `status` | draft / active / expired / terminated |
| `generated_subscriptions` | back-references to subscriptions this contract spawned |

Contracts land in Tesote first → AI extracts terms → user confirms → subscription(s) are spawned with the contract as their source.

---

## User reality (Tesote's own case: Mariel)

- She opens **Tesote**, never Odoo.
- New customer / contract? Created in Tesote → synced to Odoo (contact + supplier records).
- Vendor invoice email? Lands in Tesote inbox → reviews → pushes to Odoo (vendor bill).
- New contract? Uploaded to Tesote → AI extracts terms → Mariel confirms → Tesote spawns subscription(s) → Odoo gets the contact + subscription setup.
- Billing cycle? Tesote triggers → Odoo emits invoice → Tesote routes to customer with payment link.
- Payment arrives via Banesco rails? Tesote reconciles (bank txn ↔ invoice) → writeback to Odoo journal.
- AR aging, AP queue, cash position? Tesote dashboard, never Odoo.

Odoo runs the legal/compliance machinery underneath. The end user never sees it unless they want to.

---

## Cross-surface map

```
┌──────────────────────────────────────────────────────────────────┐
│  business/counterparties                                         │
├──────────────────────────────────────────────────────────────────┤
│  This doc. The spine: customers + vendors. Entity,               │
│  subscriptions, payment terms, FX rate, contract metadata.       │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  business/pagos                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Outbound payment execution (Tesote pays vendors).               │
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
│  The "first landing place" surface. Odoo cockpit graduates       │
│  into the command center.                                        │
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
│  Unified operating view across the whole stack.                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Resolved architectural decisions (2026-05-12)

| # | Question | Decision |
|---|---|---|
| 1 | Electronic invoicing in VE — is it on? | **Not yet.** Print/scan/save is the absence of e-invoicing today. The command center accommodates fiscalización via orchestrated workflow (store PDF as legal record, physical print + scan if/while still required) until SENIAT e-invoicing is feasible. |
| 2 | Inbound channel design | Email-as-inbox + upload portal for v1. Vendor portal integrations as v2. |
| 3 | AP approval workflow | Single-step. User approves → push to Odoo. Multi-step is v2 if needed. |
| 4 | Contract → subscription translation | AI suggests, human confirms. |
| 5 | Subscription SoR placement | Tesote (counterparty owns subscriptions). Odoo executes accounting. |
| 6 | Multi-entity counterparty | Day-one requirement. One counterparty, N entity-billing relationships. |

---

## Net-new product work

Surfaced by this architecture (not previously on the roadmap as explicit work items):

1. **Inbound document inbox** — [[../../automations/accounting-automation/inbound-inbox]]
2. **Outbound invoice routing + customer portal** — [[../cobros/outbound-invoice-routing]]
3. **Per-subscription FX rate field** — BCV+differential as a productized template (spec'd above in Schema)
4. **Multi-entity counterparty schema** — spec'd above
5. **Odoo writeback engine** — reconciled invoice + payment → Odoo journal

---

## Dogfooding as the North Star

The first instance of this command center runs on Tesote's own books, with Mariel as the design partner. We ship the loop end-to-end for VE first, then DR, then US (after QB → Odoo migration).

Our pain = our customer's pain. Same architecture, same surfaces, same UX. Mariel is our pilot customer.

---

## Related

- [[../../../finance/ar-and-cobros-2026-05-team]] — the discovery trail and finance-team plan
- [[counterparty-portal-prd]] — the counterparty-facing portal (where their customers transact with them)
- [[../cobros/cobros-spec]] — current cobros spec
- [[../../automations/accounting-automation/odoo-prd]] — Cockpit PRD (now sub-bucket of command center)
- [[../../automations/erp-ai/odoo-mcp]] — Tesote AI for Odoo (the chat surface on top)
