---
title: Inbound Document Inbox — the first landing place
tags: [product, automations, accounting-automation, inbox, ai]
updated: 2026-05-12
status: one-pager
---

# Inbound Document Inbox — the first landing place

> **Purpose.** The surface where anything external lands first. Vendor invoices, contracts, retention vouchers, receipts, expense reports, sales orders — they all arrive in Tesote, get extracted by AI, reviewed by a human, and pushed to Odoo with proper accounting metadata. Sister doc to [[../../business/counterparties/system-of-record]].

---

## Why it exists

Two findings drove this surface into v1 scope:

1. **Tesote is the command center.** If the user (Mariel today; controller / clerk in production) operates in Tesote and never opens Odoo, then anything they need to act on has to land in Tesote first. Otherwise they're back in Odoo to file documents.
2. **AP and contract handling ride the same rails.** Same inbound pipeline (arrive → AI extract → review → push to Odoo) handles vendor invoices, contracts, retention vouchers, receipts. Cheap once the pipeline exists. Pulls AP into v1 scope without extra surface area.

This is the natural graduation of the AP-automation capability in the [[odoo-prd]] (Cap #2). The "AP inbox" was already there; the inbound inbox generalizes it to all external document types.

---

## What lands here

| Doc type | Source | What happens after extraction |
|---|---|---|
| **Vendor invoice** | Email, upload | → Odoo as vendor bill with GL coding |
| **Contract** | Upload | → Counterparty + spawns subscription(s) ([[../../business/counterparties/system-of-record]]) |
| **Retention voucher (comprobante de retención)** | Email, upload | → Linked to the corresponding outbound invoice; reconciliation completes |
| **Receipt** | Email, upload, WhatsApp photo | → Odoo expense entry |
| **Expense report** | Upload | → Odoo expense entries (batch) |
| **Sales order / quote** | Upload, email | → Counterparty + draft subscription / invoice |

---

## Flow

```
Document arrives (email, upload, integration, scan, WhatsApp)
        ↓
Lands in Tesote inbox (typed: invoice / contract / receipt / ...)
        ↓
AI extracts + categorizes:
  - For invoices: vendor, RIF, amount, currency, period, GL coding suggestion
  - For contracts: parties, term, payment terms, FX terms, subscription shape
  - For receipts: vendor, amount, category, date
        ↓
Routed in Tesote queue (by type, by entity)
        ↓
User reviews / corrects in Tesote UI (single-step approval)
        ↓
Tesote pushes to Odoo:
  - Invoice → vendor bill (with retentions applied per VE rules)
  - Contract → counterparty + subscription records
  - Receipt → expense entry
        ↓
Odoo records the journal entry / accounting object
```

---

## Channel design (v1)

**In scope:**
- **Dedicated inbox email address per entity** — e.g., `inbox-ve@tesote.com`, `inbox-us@tesote.com`. Vendors and internal team forward here.
- **Upload portal** — drag-and-drop in the Tesote UI for documents that aren't email-attached.
- **WhatsApp photo capture** — receipts only for v1; same AI pipeline.

**Out of scope (v2):**
- Vendor portal integrations (SAP Ariba etc.)
- Bank-statement auto-attachment (handled separately by [[../../connect]])
- Inbound API for partner integrations

---

## Approval workflow

**v1: single-step.**

User opens the queue → reviews each item → approves (or edits + approves) → Tesote pushes to Odoo. No multi-step routing, no department-head approval chain.

Rationale (Mariel sync 2026-05-12): VE entity has few vendors and few invoices; multi-step would be overengineering. Add multi-step in v2 if larger customers need it.

---

## AI extraction model

- **Invoices** — vendor name, RIF/tax ID, amount, currency, period, line items, IVA, retentions. Suggested GL coding from prior history.
- **Contracts** — parties, scope, term length, renewal terms, payment cadence, payment terms, FX terms. Suggested subscription configuration.
- **Receipts** — vendor, amount, date, category suggestion.

**Confidence-gated:** high-confidence extractions auto-fill; the user only sees what needs eyes. Low-confidence flags surface the field for manual entry.

**Read-first, write-with-confirmation** (per [[../erp-ai/]] working principles) — the AI never pushes to Odoo without human approval in v1.

---

## Relationship to existing work

- **[[odoo-prd]] (Cockpit PRD)** — Cap #2 (AP automation) is the foundational case for this inbox. The inbox generalizes it.
- **[[../erp-ai/odoo-mcp]] (Tesote AI for Odoo)** — chat surface that can answer queries about the inbox state, but the inbox itself is a structured product surface (not chat).
- **[[../erp-workspace-ai/]]** — the workspace bridges (Gmail → AP, WhatsApp → receipt) are the *plumbing* that feeds documents into this inbox. Conceptually, this inbox is the consolidation point for all workspace-AI flows.
- **[[../../business/counterparties/system-of-record]]** — contracts processed here populate the counterparty + subscription records there.

---

## Open questions

- **Fiscalización compliance for inbound** — VE may require physical retention of inbound invoices too. Confirm what the legal record must look like (PDF in Tesote storage vs. physical archive).
- **Duplicate detection** — same vendor invoice forwarded twice or auto-routed from multiple email addresses. Probably hash-based dedup at extraction.
- **Per-entity routing** — when a document arrives at a generic inbox, how do we decide which entity it belongs to? AI inference from vendor + RIF context, with user confirmation if ambiguous.

---

## Status

One-pager. Not yet a PRD. Pending product/eng scoping conversation, post-VE-e-invoicing reality check.

## Related

- [[../../business/counterparties/system-of-record]] — spine doc
- [[../../../finance/ar-and-cobros-2026-05-team]] — discovery trail
- [[odoo-prd]] — Cockpit PRD (contains Cap #2 AP automation, the seed of this inbox)
