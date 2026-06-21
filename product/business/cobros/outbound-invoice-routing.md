---
title: Outbound Invoice Routing + Customer Payment Portal
tags: [product, cobros, counterparties, payments, banesco]
updated: 2026-05-12
status: one-pager
---

# Outbound Invoice Routing + Customer Payment Portal

> **Purpose.** The outbound half of the command center loop. Subscription cycle triggers → Tesote instructs Odoo to emit → invoice flows back to Tesote → Tesote routes to the customer with a payment link → customer pays in the Tesote portal → Tesote reconciles → writes back to Odoo. Sister doc to [[../counterparties/system-of-record]].

---

## Why it exists

Two findings drove this surface into v1 scope:

1. **Tesote — not Odoo — owns the customer relationship.** The user (Mariel; eventually our customers' AR clerks) routes invoices through Tesote. Odoo emits the legal artifact, but the customer never sees Odoo. They see Tesote, they pay through Tesote, the transaction lives in Tesote.
2. **Stripe was the manual workaround.** Discovered 2026-05-12: Mariel was duplicating prior Stripe invoices to maintain a parallel ledger. Tesote replacing this role is cheaper than first modeled — we're replacing manual labor, not a working system.

This surface is the joining of three already-on-the-roadmap pieces:
- [[../counterparties/counterparty-portal-prd]] — the customer-facing portal (where the link lands)
- [[cobros-spec]] — the chase/dunning workflow on unpaid AR
- [[../pagos/rails/]] — Banesco rails for the actual debit (B2C live, B2B bank-gated)

What's net-new here is the **routing + reconciliation loop** — the connective tissue that makes the three pieces operate as one product.

---

## The flow

```
Counterparty + subscription in Tesote → cycle trigger fires
        ↓
Tesote instructs Odoo to emit invoice
        ↓
Odoo emits invoice (legal + tax structure, fiscalización applied)
        ↓
Odoo returns invoice (PDF + metadata) to Tesote
        ↓
Tesote routes to customer:
  - Email with "Ver factura →" CTA (matches PRO-112 framing)
  - WhatsApp message with link
  - Both — depending on counterparty preference
        ↓
Customer enters Tesote portal (counterparty-portal-prd)
        ↓
Customer pays via Tesote rails:
  - Banesco direct debit (BNC ACH today via PRO-112 v1)
  - Future: Banesco Botón de Pago (replicate Polar pattern)
  - Future: card / wire / cash on hand
        ↓
Payment lands in bank → flows into Tesote via Connect rails
        ↓
Tesote auto-reconciles (bank txn ↔ invoice) via shared payment_batch_id
        ↓
Tesote writes reconciled invoice + payment back to Odoo
```

---

## What's net-new vs. existing

| Already specced | Net-new for this surface |
|---|---|
| Counterparty portal UI ([[../counterparties/counterparty-portal-prd]]) | The **routing engine**: Tesote decides when to send, which channel, which template |
| Pay flow (BNC ACH OTP, multi-pay) | The **Odoo emission trigger**: Tesote tells Odoo to emit on the right cadence with the right FX |
| Cobros spec (chase/dunning) | The **reconciliation back-write**: bank txn → Tesote → Odoo journal |
| Banesco rails (Polar pattern) | The **FX-aware invoicing**: BCV + differential template applied per subscription |

---

## FX-aware invoice generation

The biggest unlock identified in the 2026-05-12 sync. Today Mariel calculates the rate manually in Excel for paralelo/Binance/euro billing. The Tesote-side invoicing engine:

1. Reads `fx_rate_rule` from the subscription record ([[../counterparties/system-of-record]] schema)
2. For `BCV+differential`: pulls live BCV, applies the differential (default 30% bps), computes the BS amount
3. Instructs Odoo to emit with the right base imponible in USD + BS conversion
4. At payment time, auto-adjusts the BCV-converted total to current BCV — base imponible (USD) stays constant; IVA stays constant; only the BCV total updates

Result: Mariel never opens Excel for FX again. Numbers always land round.

---

## Routing channels (v1)

**In scope:**
- **Email** — with the "Ver factura →" CTA from PRO-112, attached scanned PDF (until e-invoicing comes online), payment data inline (RIF, account, amount).
- **WhatsApp** — optional, per counterparty preference. Same link to the portal.

**Out of scope (v2):**
- SMS
- Direct vendor-portal integration (large customers who use Ariba etc.)
- Bulk-send scheduling beyond the per-subscription cycle

---

## Reconciliation engine

The piece that closes the loop. Inputs:
- **Outbound side:** invoice in Tesote (with ID, amount, currency, customer, expected payment method)
- **Inbound side:** bank transaction arriving via [[../../connect]] (with amount, sender, reference)

Match logic:
- Exact match on `payment_batch_id` (when paid via Tesote portal → guaranteed match)
- Heuristic match: amount + sender RIF + invoice reference in memo
- Fallback: surface in a reconciliation queue for human matching

Once matched, Tesote:
1. Marks invoice as paid in its own state
2. Pushes paid status + reconciled payment record to Odoo
3. Triggers Odoo journal entry for the cash receipt
4. (If applicable) Pulls in the retention voucher when received via [[../../automations/accounting-automation/inbound-inbox]] and links it

---

## User reality

**Mariel** (workspace user, our internal dogfood case):
- Sees the upcoming subscription cycle in her Tesote dashboard
- Confirms the batch (or lets it auto-run)
- Watches invoices route out — no print, no scan, no manual Stripe duplication
- Sees payments land in real time as bank rails confirm
- AR aging stays current automatically

**Counterparty** (the customer paying us, our dogfood example):
- Receives "Ver factura →" email or WhatsApp
- Lands in the Tesote portal (counterparty-portal-prd)
- Pays via BNC ACH OTP (current) or Banesco Botón de Pago (future)
- Gets confirmation and stored history

Same loop applies when our customers run it for their own customers — that's the product.

---

## Open questions

- **Fiscalización timing** — when does Odoo emit vs. when does Tesote route? If e-invoicing isn't on yet (it isn't, per 2026-05-12), there's still a print/scan step. Either Tesote orchestrates the print (printer integration) or Mariel keeps a residual physical workflow until SENIAT e-invoicing arrives. Likely the latter for v1; revisit when SENIAT path opens.
- **Re-emission on rate change** — if the BCV moves materially between emission and payment, do we re-emit or just adjust the BCV-converted total at payment? Latter, per the 2026-05-12 alignment, but corner cases (>20% moves) might need re-emission.
- **Multi-currency portal display** — when a customer has both a VE BS subscription and a US USD subscription with us, do they see both in one portal view or per-entity? Likely unified; entity shown as a tag.
- **Chase integration** — at what point does an unpaid invoice flow into the [[cobros-spec]] chase queue? Probably: payment terms elapsed + N grace days. Configurable per counterparty.

---

## Status

One-pager. Builds on existing PRDs ([[../counterparties/counterparty-portal-prd]], [[cobros-spec]]) and rails work ([[../pagos/rails/]]). Pending product/eng scoping conversation.

## Related

- [[../counterparties/system-of-record]] — spine doc + schema
- [[../counterparties/counterparty-portal-prd]] — customer-facing portal PRD
- [[cobros-spec]] — chase/dunning workflow
- [[../pagos/rails/]] — bank-side rails per provider
- [[../../../finance/ar-and-cobros-2026-05-team]] — discovery trail
