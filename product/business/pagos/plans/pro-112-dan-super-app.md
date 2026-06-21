---
title: PRO-112 — Dan's Super-App / Counterparty Portal Spec (mirror)
tags: [product, tesote-pay, super-app, pro-112, dan]
updated: 2026-04-23
author: Daniel Francoeur (mirrored by Luis)
source: https://linear.app/tesote/issue/PRO-112/tesote-super-app-counterparty-portal-workspace-funnel-spec-wireframes
status: Backlog — Urgent
created_by: Daniel Francoeur
assignee: Luis Pulgar
created_at: 2026-04-23T00:16:15Z
---

> **Note on scope.** This doc is a **verbatim mirror** of Dan's Linear ticket PRO-112, preserved as a separate thread from `plans/user-stories.md` (Luis's existing Tesote Pay V1/V2 plan). The two framings diverge — don't merge until an explicit reconciliation pass. See `product/tesote-pay/plans/README.md` for the split rationale (if/when created).
>
> **Keep the source of truth in Linear.** Edit PRO-112 there; re-mirror here only when the ticket changes materially.

---

## Context

The BNC-powered payments launch opens the door to a broader super-app: invoices, retentions (IVA/ISLR), Tesote Capital, and the B2B network — all on rails we already operate.

Supporting data analysis (run 2026-04-22): `.debugging/bnc-payments-network-thesis-2026-04-22.md`

**Headline evidence:**

* 72% of active workspaces already have BNC connected
* 78% of VES-active workspaces transacted through BNC in the last 90d
* 85% of identifiable intra-Tesote counterparty relationships are already BNC-ready on both sides
* 116 of 629 SENIAT-resolved counterparty identities (18%) are themselves Tesote legal entities — the network already exists, we just need to instrument it

## The thesis

Tesote becomes a three-tier B2B super-app:

```
Tier 0: Counterparty (current state)
  → row in another workspace's counterparty table. Passive.

         ↓ receives invoice/payment from a Tier 2 workspace

Tier 1: Portal user (NEW)
  → claims their SENIAT-verified profile
  → upgrades a BNC account to "Powered by Tesote"
  → view invoices, receive/send payments, see comprobantes
  → monetized on per-payment fees

         ↓ graduates when they want more

Tier 2: Workspace (existing, expanded)
  → multi-entity, team roles, batch ops, full retentions engine
  → Tesote Capital, ERP import, multi-currency, API
  → subscription + reduced per-payment fees + capital revenue
```

The invoice is the acquisition channel. The BNC "Powered by Tesote" upgrade is the Tier 0→1 conversion wedge. Natural graduation — no sales motion — drives Tier 1→2.

## Why this is defensible (for Tesote specifically)

1. **We already own the ledger.** 7M+ VES transactions, 1,085 legal entities, 149 workspaces, SENIAT counterparty resolution — the invoice/retention/capital/payments loop is the same data viewed four ways.
2. **Retentions are the lock-in.** IVA/ISLR compliance is mandatory, painful, monthly. Auto-applied retentions = switching-cost territory.
3. **The two-sided graph is real today.** 85% of identifiable intra-Tesote pairs are already BNC-ready.
4. **Capital underwrites itself.** Invoice + retention + payment data = cashflow predictability on both sides of every trade. Differentiated underwriting dataset in Venezuela.

## Epics (user stories)

### A. Tier 0 → Tier 1: "Claim your portal"

Invite/activation — the network-growth engine.

* A.1 Tier 2 workspace sends invoice to non-Tesote counterparty → email with claim link
* A.2 Counterparty lands on pre-filled claim page (SENIAT-verified RIF + legal name + waiting invoice)
* A.3 Minimal-friction identity verification → portal account created
* A.4 Post-claim: portal home shows this invoice + all historical transactions against this RIF across Tesote
* A.5 Direct invite path (without invoice)
* A.6 Self-signup at `portal.tesote.com` — proactive claim
* A.7 Tier 2 sender sees "counterparty is now on Tesote" and payment UX upgrades to instant

### B. Tier 1: "View and pay invoices in my portal"

* B.1 Unified inbox across all Tesote senders
* B.2 Full invoice detail (line items, IVA, retentions applicable, net due)
* B.3 Single-user approve/dispute
* B.4 Payment timeline (due, overdue, upcoming)
* B.5 Invoice PDF + SENIAT XML download
* B.6 Comprobantes de retención received
* B.7 Search/filter

### C. Tier 1: "Upgrade my BNC account to Powered by Tesote"

The monetization event.

* C.1 Connect BNC account (OAuth/credentials)
* C.2 Upgrade proposal: cost + benefits (instant payments, auto-reconciliation, comprobantes in-app)
* C.3 Account becomes payment-enabled
* C.4 See balance, recent tx, pending payments
* C.5 Multiple BNC accounts supported (multi-entity is Tier 2)

### D. Tier 1: "Make payments from my portal"

* D.1 Pay against approved invoice — net of retentions
* D.2 Tesote-network routing (instant) when payee is on platform
* D.3 Standard BNC rails when payee is off-platform
* D.4 Pre-payment summary (gross, retentions, fee, net)
* D.5 Auto-generated comprobante delivered to payee
* D.6 Ad-hoc payment (RIF + amount + concepto)
* D.7 Payment history + exports

### E. Tier 1: "Handle retentions correctly without being an expert"

* E.1 Detect contribuyente especial from SENIAT profile
* E.2 Auto-calculate IVA/ISLR on payment
* E.3 Auto-generate, number, deliver comprobantes
* E.4 YTD issued/received ledger
* E.5 Simplified monthly SENIAT XML export
* E.6 Graceful escalation to "upgrade for advanced retention handling"

### F. Tier 1 → Tier 2: "Graduate to a full workspace"

* F.1 Usage-based upgrade prompts at thresholds
* F.2 Transparent "what changes" page
* F.3 One-click upgrade — all data migrates
* F.4 Workspace onboarding checklist kicks in
* F.5 Billing switches from per-payment to subscription + reduced fees
* F.6 Downgrade possible — no trap

### G. Tier 2 workspace-only features (upgrade gates)

* G.1 Multi-entity consolidated view
* G.2 Team roles (AP clerk, CFO, auditor)
* G.3 Multi-approver workflows
* G.4 Batch operations across entities/accounts (extends PRO-99 wizard)
* G.5 ERP import/export (Odoo, SAP, CSV)
* G.6 Full retentions engine (concepto-level rules, YTD ISLR, all period types)
* G.7 Tesote Capital (factoring, credit lines, reverse factoring)
* G.8 Advanced reconciliation
* G.9 Multi-currency (VES + USD + USDT)
* G.10 Custom reports, dashboards, API

### H. Network mechanics (cross-tier)

* H.1 Tier 1 payment from Tier 2 → auto-linked to invoice
* H.2 Tier 1 payment to Tier 2 → comprobante flows to retention ledger
* H.3 Payment requests (cobro) across any tiers
* H.4 Shared identity layer — verify once, trusted across workspaces
* H.5 Tier 2 sees "X counterparties on Tesote, Y not" with one-click invites

## Wireframe priority (in order)

Designers should sequence these because the decisions cascade hardest:

1. **Claim-your-portal landing page** (A.2 → A.4) — every counterparty arrives here
2. **Tier 1 portal home** (B.1 + D.7 + C.2) — first login, "Upgrade BNC" CTA placement
3. **"Powered by Tesote" BNC upgrade flow** (C.1 → C.3) — the revenue moment
4. **Tier 1 payment composer** (D.1 → D.5) — simpler than Tier 2 but routing logic still applies
5. **Graduation flow** (F.1 → F.4) — must feel like unlocking, not starting over
6. **Tier 2 "invite counterparties" surface** (H.5 + A.1) — growth loop from sender side
7. **Counterparty 360, tier-aware** — Tier 0/1/2 badging + interaction changes

## Open product decisions (lock before wireframing)

1. **Minimum viable Tier 1:** view invoices + pay invoices + Powered-by-Tesote BNC upgrade. Retentions (E) likely v1.1 — can we ship without?
2. **Multi-RIF handling at Tier 1:** one business owner with personal cédula + company RIF — one login with multiple profiles, or two accounts?
3. **Domain strategy:** `portal.tesote.com` separate shell vs. login-mode on `app.tesote.com`. Recommendation: separate subdomain, same backend, radically simpler Tier 1 UX.

## Supporting data

* Full analysis memo: `.debugging/bnc-payments-network-thesis-2026-04-22.md`
* Top VES movers not on BNC: Grupo Abreu ($1.7B/90d, 0% BNC), Tesote Ventas ($518M/90d, 0% BNC) — named-account push before launch
* Top intra-Tesote pairs already both-sides BNC-ready: APB GROUP ↔ KAIZEN ($800k each way), Canguro Venezuela → Krece ($651k), MARCAS PROPIAS → Grupo cashea ($391k), ALMACENADORA ASOPORTUGUESA → Asoportuguesa ($440k) — closed-loop corridors for day-one instrumentation

## Acceptance criteria

- [ ] Product spec written for each epic A–H with story-level detail and edge cases
- [ ] Wireframes delivered in priority order above
- [ ] Three open decisions above resolved and documented
- [ ] GTM plan: Tier 0→1 activation motion + Tier 1→2 graduation triggers
- [ ] Pricing model defined for each tier
- [ ] Engineering scoping estimate for Tier 1 MVP (epics A, B, C, D minimum)
- [ ] Named-account plan for top VES movers not yet on BNC

## Owner

Luis Pulgar (product lead on Payments project)
