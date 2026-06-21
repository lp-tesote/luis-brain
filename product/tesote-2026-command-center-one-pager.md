---
title: Tesote 2026 — Command Center (One-Pager)
tags: [product, pitch, command-center]
updated: 2026-05-13
status: draft
source: [[tesote-2026-command-center-prd]]
---

# Tesote 2026 — Command Center

> **Tesote is the command center. Odoo is the execution layer. The end user never sees Odoo.**

**The bet.** One workspace that sits above the customer's ERPs (Odoo VE, DR, US-eventually) and runs every flow that touches money or counterparties — inbound documents, outbound billing, payment execution, reconciliation. The user opens Tesote. Never Odoo.

## Who it's for

Multi-entity LATAM operators (VE + DR + US) where no single ERP sees the whole picture. Finance teams drowning in manual reconciliation, multi-currency FX, fiscalización, and chase work. **Companies that look like Tesote ourselves** — our pain = our customer's pain.

## Why now

- **On the rails.** Banesco + BNC + Connect's multi-jurisdiction footprint make bank-side reconciliation mechanical, not forensic.
- **The pain is dogfooded.** Mariel runs Tesote's three-entity books on Stripe + Excel + Odoo + QB. Every customer with overseas entities lives this. Odoo can't fix it; QB can't fix it; Stripe pretends to.
- **AI collapses the cost.** OCR, extraction, categorization, anomaly detection, chase prioritization — cheap utilities now. Three years of feature work compresses into 2026.

## What it does — four flows

| Flow | One sentence |
|---|---|
| **Inbound** | Docs (invoices, contracts, receipts, retentions) land in Tesote → AI extracts → user approves → pushed to Odoo. |
| **Outbound** | Subscription triggers → Odoo emits → Tesote routes to customer → customer pays in portal → Tesote auto-reconciles → writes back. |
| **Pagos** | Workspace pays its vendors via Tesote rails; auto-generates retention vouchers. |
| **Counterparty journey** | PRO-112 Tier 0 → 1 → 2 progression; passive row → portal user → full workspace. |

## The moat

The **counterparty spine**: multi-entity, subscription-aware, FX-aware, contract-rooted. One counterparty = N billing relationships across our entities. Tesote owns commerce; Odoo executes accounting. Bank rails feed continuous reconciliation. The differentiated dataset (invoices + retentions + two-sided payment data) is the precondition for Tesote Capital — generic underwriting can't catch up.

## Network effects already in the data

- **72%** of active workspaces already have BNC connected
- **85%** of intra-Tesote counterparty pairs are BNC-ready on both sides
- **18%** of SENIAT-resolved counterparties are themselves Tesote entities

When both sides are on Tesote, invoice → pay → reconcile → retention → ledger collapses into one transaction.

## The wedge (this quarter)

Outbound loop end-to-end for **ONE** VE customer:

1. Subscription cycle triggers in Tesote
2. Tesote → Odoo emits invoice
3. Tesote routes via Banesco payment link (existing portal)
4. Customer pays via live BNC ACH OTP rail
5. Tesote reconciles → writes paid status back to Odoo

Every architectural piece is touched. Then N customers, then DR, then US (post-QB migration).

## 2026 sequence

- **Q3** — Outbound loop live for VE; FX-aware invoicing productized
- **Q4** — Inbound inbox v1 (vendor invoices, receipts); contracts auto-spawn subscriptions; DR onto the loop
- **2027** — US entity onto the loop; Tesote Capital activated

---

Deep PRD: [[tesote-2026-command-center-prd]] · Spine: [[business/counterparties/system-of-record]] · Customer side: [[business/pagos/plans/pro-112-dan-super-app]]
