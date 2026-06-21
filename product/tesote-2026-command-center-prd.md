---
title: Tesote 2026 — Command Center PRD
tags: [product, prd, command-center, architecture, vision, system-of-record]
updated: 2026-05-12
status: draft v1
audience: Luis (primary), Dan, Majo, leadership
author: Luis Pulgar (synthesis with Claude)
---

# Tesote 2026 — Command Center PRD

> **Purpose.** Synthesize the architecture, surfaces, flows, schema, AI strategy, and rollout sequence of the new Tesote into one document. Not a replacement for the deep specs underneath; a synthesizing layer that ties them together. For Luis to digest, for Dan to scope, for the team to align.
>
> **Source of the framing.** Locked 2026-05-12 after two syncs with Mariel (finance, VE) surfaced that the existing architecture treated Stripe as a system of record when it was actually hand-maintained manual labor. The cheapest path forward is Tesote replacing it — as the command center on top of Odoo. This PRD captures that decision and everything it implies.

---

## Part I — Executive Summary

### What the new Tesote is

**Tesote is the command center for finance operations of LATAM-anchored multi-entity businesses.** One workspace that sits above the customer's ERPs (Odoo VE, Odoo DR, eventually Odoo US) and runs every flow that touches money or counterparties — inbound documents (invoices, contracts, receipts, retentions), outbound billing (subscriptions, payment links, reconciliation), payment execution (Pagos + Cobros via Banesco / BNC rails), and the AI assistance layered across all of it.

The user opens Tesote. Never Odoo.

### Who it's for

The same profile as Tesote today, sharpened:

- **Multi-entity LATAM operators** (VE + DR + US-anchored entities at minimum), where no single ERP sees the whole picture.
- **Finance teams** drowning in manual reconciliation, multi-currency FX, fiscalización compliance, and chase work.
- **Companies that look like Tesote ourselves.** Our pain = our customer's pain. The dogfooding is the product validation.

### Why now

Three forces aligned to make this the right move in 2026:

1. **Tesote is already on the payment rails.** Banesco, BNC, and the broader Connect footprint (VE + Panamá + RD + EEUU + Caribe banks) make near-immediate bank-side reconciliation mechanical, not human.
2. **The customer pain is the same on both sides.** We discovered this dogfooding: Mariel runs Tesote's books across three entities with manual Stripe + Excel + Odoo + QB. Every Tesote customer that has overseas entities lives this. Odoo's UI doesn't solve it. QuickBooks doesn't solve it. Stripe pretends to but is just a manual mirror.
3. **AI changes the cost structure.** OCR + extraction + categorization + anomaly detection + chase prioritization are no longer dedicated product surfaces — they're cheap utilities we layer across every workflow. That collapses what would have been three years of feature work into something we can ship inside 2026.

### What's new vs. what existed

| Already on the path | Sharpened or net-new |
|---|---|
| Tesote Connect (bank rails, multi-jurisdiction) | Connect feeds the reconciliation engine in both directions |
| Cobros + Pagos (workspace + customer portal) | Outbound invoice routing + customer payment portal as one productized loop |
| Counterparty data model | Becomes the **spine** — multi-entity, subscription-aware, FX-aware, contract-rooted |
| Accounting Automations (Cockpit on Odoo) | Graduates from cockpit framing into the full command center |
| Tesote AI for Odoo (chat surface) | Stays as the conversational lane; AI also lives as a utility everywhere else |
| PRO-112 super-app + counterparty portal | Becomes the customer-facing half of the same loop |
| QB → Odoo US migration | Now a strategic dependency for unifying the US entity into the command center |

### The single architectural sentence

> **Tesote is the command center. Odoo is the execution layer. The end user never sees Odoo.**

Everything below is a consequence of that sentence.

---

## Part II — The Architecture

### The decision (locked 2026-05-12)

**Tesote = command center. Odoo = execution layer.**

- Tesote is the **first landing place** for everything: invoices (inbound + outbound), contracts, retention vouchers, receipts — anything with finance metadata.
- Tesote is the **only UI** the end user sees. Odoo becomes invisible to Mariel today, to our customers tomorrow.
- Tesote **controls and executes** Odoo: legal invoices, journal entries, tax compliance, fiscalización.
- Applies to: Odoo VE (today), Odoo DR (today), eventually Odoo US (post-QB migration).
- Stripe drops out of the cross-entity SoR role entirely; stays only as US card processor where relevant.

This is the inversion of the prior framing. Before: Tesote was a workspace alongside the customer's ERP. After: Tesote is the operating layer; the ERP is plumbing the operating layer drives.

### Why this works now

- **We're on the rails.** Banesco, BNC, plus the broader Connect footprint mean bank-side reconciliation is mechanical.
- **VE banking transactions flow through Tesote already.** Near-immediate reconciliation against Odoo becomes a 1:1 match, not a forensic exercise.
- **AI handles the parts that were too expensive before.** Inbound extraction. Anomaly detection. Chase prioritization. None require a custom team to build.

### Why not centralize in Odoo

- Odoo's UI / UX doesn't work for multi-entity, multi-jurisdiction operators (Mariel's daily experience).
- Our ICP is precisely this profile.
- **Our pain = our customer's pain.** Mariel is our pilot customer.

### Roles in the new model

```
┌─────────────────────────────────────────────────────────────────────┐
│  TESOTE — Command Center                                            │
│  ───────────────────────────────────────────────────────────────    │
│  • System of record (counterparties, contracts, subscriptions)      │
│  • First landing place (inbound documents)                          │
│  • Outbound routing + customer payment portal                       │
│  • Reconciliation engine                                            │
│  • The only UI the user sees                                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               │  Commands + writebacks
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ODOO (and successors) — Execution Layer                            │
│  ───────────────────────────────────────────────────────────────    │
│  • Legal invoice emission                                           │
│  • Journal entries                                                  │
│  • Tax compliance (IVA, ISLR, fiscalización)                        │
│  • General ledger of record (for legal purposes)                    │
│  • Never directly touched by end users                              │
└─────────────────────────────────────────────────────────────────────┘
                               ▲
                               │
                               │  Bank rails feed reconciliation
                               │
┌─────────────────────────────────────────────────────────────────────┐
│  TESOTE CONNECT — Bank Rails                                        │
│  ───────────────────────────────────────────────────────────────    │
│  Banesco, BNC, multi-jurisdiction VE/DR/PA/US/Caribe                │
└─────────────────────────────────────────────────────────────────────┘
```

### Resolved architectural decisions (2026-05-12)

| # | Question | Decision |
|---|---|---|
| 1 | Electronic invoicing in VE — is it on? | **Not yet.** Print/scan/save IS the absence of e-invoicing. Tesote orchestrates the workflow (store PDF as legal record; physical print + scan if/while still required) until SENIAT e-invoicing arrives. |
| 2 | Inbound channel design | Email-as-inbox + upload portal for v1. Vendor portal integrations as v2. |
| 3 | AP approval workflow | Single-step. User approves → push to Odoo. Multi-step is v2 if needed. |
| 4 | Contract → subscription translation | AI suggests, human confirms. |
| 5 | Subscription SoR placement | Tesote (counterparty owns subscriptions). Odoo executes accounting. |
| 6 | Multi-entity counterparty | Day-one requirement. One counterparty, N entity-billing relationships. |

### Source docs feeding this section

- [[business/counterparties/system-of-record]] — the architectural spine + canonical schema
- [[../finance/ar-and-cobros-2026-05-team]] — discovery trail and finance-team plan

---

## Part III — The Workspace Shell

The architecture in Part II is invisible. What the user actually sees is the **workspace shell** — the chassis built in PRO-112 — with the command-center scope folded into its existing sidebar IA.

### Sidebar IA (canonical, from PRO-112)

The workspace-shell prototype (`product/business/pagos/prototypes/pro-112/workspace-shell.html`) defines the IA the command center plugs into. Five sections from top:

```
┌──────────────────────────────────────────────────────────────────┐
│  Tesote Connect                                                  │
├──────────────────────────────────────────────────────────────────┤
│  • Saldos                                                        │
│  • Transacciones                                                 │
│  • Conexiones bancarias                                          │
│                                                                  │
│  Role: bank rails layer — the input feed for everything that     │
│  involves money moving. Feeds the reconciliation engine.         │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Tesote Negocios                                                 │
├──────────────────────────────────────────────────────────────────┤
│  • Pagos ↑                                                       │
│  • Cobros ↓                                                      │
│  • Contrapartes                                                  │
│                                                                  │
│  Role: counterparty + money-movement surface. Where the user     │
│  manages who they transact with and runs outbound/inbound        │
│  payment flows.                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Tesote Automatizaciones                                         │
├──────────────────────────────────────────────────────────────────┤
│  • Contabilidad                                                  │
│  • Reportes                                                      │
│                                                                  │
│  Role: the structured-workflow product. Inbound document inbox,  │
│  reconciliation queues, mapping config, productized close.       │
│  Where the cockpit framing lives — graduated into command        │
│  center.                                                         │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Tesote IA                                                       │
├──────────────────────────────────────────────────────────────────┤
│  Role: the conversational surface for the command center.        │
│  Tesote-branded chatbot, MCP under the hood, zero coupling to    │
│  Tesote core. Talks to Odoo, reads from Tesote state.            │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  Espacio de Trabajo                                              │
├──────────────────────────────────────────────────────────────────┤
│  • Mi equipo                                                     │
│  • Permisos                                                      │
│  • Configuración                                                 │
│                                                                  │
│  Role: workspace administration. Multi-entity, team roles,       │
│  permissions. Stays out of the daily operating loop.             │
└──────────────────────────────────────────────────────────────────┘
```

### How the command center maps onto the shell

Every flow in Part IV traces through specific sections of this sidebar. The user's eye moves naturally:

- **Inbound document arrives** → lands in Automatizaciones (Contabilidad inbox)
- **Subscription cycle triggers** → originates from Negocios (Contrapartes + Cobros)
- **Payment arrives** → flows through Connect (Transacciones) → reconciled in Automatizaciones (Contabilidad)
- **AI ask** → IA pulls context from all four upper sections

The shell doesn't change shape. The *power* behind each section deepens.

### What's locked vs. open in the shell

**Locked** (PRO-112 prototype 2026-05-01):
- Sidebar IA structure (the five sections above)
- Visual system (Mercury pastel pills, 96px uniform widths, 5px radius)
- The Negocios split (Pagos with up arrow / Cobros with down arrow / Contrapartes)
- The Espacio de Trabajo section at the bottom

**Open / shifting** (this PRD):
- Each section's content depth — the command center expands what lives inside Contabilidad, Contrapartes, Cobros, etc.
- The IA surface — chat is one expression; AI as utility appears across all sections too

### Source docs feeding this section

- `product/business/pagos/prototypes/pro-112/workspace-shell.html` — the canonical shell prototype
- `product/business/pagos/prototypes/pro-112/README.md` — engineering handoff packet
- [[business/pagos/plans/pro-112-dan-super-app]] — the three-tier super-app spec
- `product/business/pagos/prototypes/pro-112/claim-flow.html` — the counterparty side of the same shell

---

## Part IV — The Canonical Flows

Four flows describe everything the command center does. Every feature, every screen, every line of code in the new Tesote should be locatable on one of these four.

### Flow 1 — Inbound documents (the "first landing place")

Anything external with finance metadata lands in Tesote first, gets extracted, gets routed.

```
Document arrives via:
  • Email (dedicated inbox per entity)
  • Upload (drag-and-drop in Tesote UI)
  • WhatsApp photo (receipts only, v1)
  • Integration (vendor portals — v2)
        ↓
Lands in Tesote inbox (typed: invoice / contract / receipt / retention voucher / ...)
        ↓
AI extracts + categorizes:
  • Invoices → vendor, RIF, amount, currency, period, line items, IVA, retentions
  • Contracts → parties, term, payment terms, FX terms, subscription shape
  • Receipts → vendor, amount, date, category suggestion
        ↓
Routed in Tesote queue (by document type, by entity)
        ↓
User reviews / corrects in Tesote UI (single-step approval)
        ↓
Tesote pushes to Odoo:
  • Invoice → vendor bill (with retentions applied per VE rules)
  • Contract → counterparty + subscription records
  • Receipt → expense entry
        ↓
Odoo records the journal entry / accounting object
```

**Where in the shell:** Automatizaciones → Contabilidad.
**Sister doc:** [[automations/accounting-automation/inbound-inbox]] (one-pager).
**Applies to:** vendor invoices (AP), contracts, retention vouchers, receipts, expense reports, sales orders.

### Flow 2 — Outbound subscription billing

The subscription lifecycle: trigger → emit → route → pay → reconcile → writeback.

```
Counterparty + subscription in Tesote → cycle trigger fires
        ↓
Tesote instructs Odoo to emit invoice (with legal + tax structure, fiscalización)
        ↓
Odoo emits invoice → returns PDF + metadata to Tesote
        ↓
Tesote routes to customer:
  • Email with "Ver factura →" CTA (PRO-112 framing)
  • WhatsApp message with link
  • Both, per counterparty preference
        ↓
Customer enters Tesote portal (counterparty-portal-prd / PRO-112 claim flow)
        ↓
Customer pays via Tesote rails:
  • BNC ACH OTP debit (live today via PRO-112 v1)
  • Banesco Botón de Pago (next — replicate Polar pattern)
  • Future: card / wire / cash
        ↓
Payment lands in bank → flows into Tesote via Connect rails
        ↓
Tesote auto-reconciles (bank txn ↔ invoice) via shared payment_batch_id
        ↓
Tesote writes reconciled invoice + payment back to Odoo
        ↓
(If retention voucher arrives later → Inbound flow links it to the invoice)
```

**Where in the shell:** Negocios → Cobros (sender-side) + counterparty portal (payer-side).
**Sister doc:** [[business/cobros/outbound-invoice-routing]] (one-pager).
**Key net-new:** FX-aware invoice generation (BCV + per-customer differential), Odoo writeback engine, routing engine that decides channel + template.

### Flow 3 — Outbound payment execution (Pagos)

When the workspace pays its own vendors / counterparties.

```
Vendor invoice received (Inbound flow above) → approved → flagged for payment
        OR
Ad-hoc payment created in Pagos UI
        ↓
Tesote composes the payment (gross, retentions, fee, net)
        ↓
Routes through the appropriate rail:
  • Tesote-network instant (when payee is on Tesote)
  • BNC ACH (when payee is off-network)
  • Banesco rails
  • Cash / Zelle / wire (manual, recorded)
        ↓
Payment executes via Connect rails
        ↓
Tesote auto-generates comprobante de retención
        ↓
Delivered to payee + recorded
        ↓
Pushed to Odoo (journal entry)
```

**Where in the shell:** Negocios → Pagos.
**Status today:** B2C rail LIVE and sellable; B2B juridico-to-juridico rail bank-gated (pending bank activation).
**Source docs:** [[business/pagos/plans/pro-112-dan-super-app]], [[business/pagos/rails/]] per provider.

### Flow 4 — Counterparty journey (the customer-facing half)

How the people we (and our customers) transact with experience Tesote. PRO-112's three-tier model.

```
Tier 0 — Counterparty (passive)
   → Row in a Tesote workspace's counterparty table
   → Receives an invoice → "Ver factura →" email
        ↓
Tier 1 — Portal user (NEW)
   → Claims SENIAT-verified profile via signed-URL flow
   → Views invoices across all Tesote senders (unified inbox)
   → Pays via 4-step OTP debit flow (BNC ACH today, Banesco next)
   → Optionally upgrades a BNC account to "Powered by Tesote" (the monetization event)
        ↓
Tier 2 — Workspace (existing, expanded)
   → Multi-entity, team roles, retentions engine, Tesote Capital
   → Full command center capabilities (everything in this PRD)
   → Subscription billing + reduced per-payment fees + capital revenue
```

**Where in the shell:** counterparty portal (separate brand `tesotenegocios.com`, same backend).
**Source doc:** [[business/counterparties/counterparty-portal-prd]] + PRO-112 super-app spec + claim-flow.html prototype.

### How the four flows compose

A given customer's day touches several flows simultaneously:

- Mariel uploads a vendor invoice (Flow 1) while reviewing an outstanding receivable (Flow 2 in mid-state) and approving a payment run (Flow 3), with chat in IA pulling context across all of them (Flow 4 from the workspace side).

The shell hides the boundaries; the architecture makes them coherent.

---

## Part V — The Surfaces

This section walks each sidebar surface in detail. Each subsection: what it does, what's net-new from the command-center reframe, source docs to drill into.

### V.1 Tesote Connect

```
┌──────────────────────────────────────────────────────────────────┐
│  Tesote Connect                                                  │
│  Saldos · Transacciones · Conexiones bancarias                   │
│  ───                                                             │
│  Multi-jurisdiction bank connectivity. Feeds reconciliation in   │
│  both directions (inbound payments received; outbound payment    │
│  status). The clean-bank-data moat.                              │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Pulls bank transactions across the customer's entire banking footprint (VE + Panamá + RD + EEUU + Caribe), normalizes, surfaces saldos + transacciones, manages connections.

**Net-new for command center:**
- Becomes the *input feed* for the reconciliation engine. Every bank txn that arrives is a candidate match against an outstanding invoice (outbound) or a pending vendor payment (outbound).
- Continuous (not periodic) reconciliation becomes possible.

**Status:** Multi-jurisdiction support already in scope per project memory ([[connect-multi-jurisdiction]]). Banesco rails operational ([[banesco-cobros-status]]); BNC rails in active integration.

**Source docs:** `product/connect/` — multi-jurisdiction bank inventory.

---

### V.2 Tesote Negocios — Pagos

```
┌──────────────────────────────────────────────────────────────────┐
│  Negocios · Pagos ↑                                              │
│  ───                                                             │
│  Outbound payment execution. The workspace pays its vendors /    │
│  counterparties via Tesote rails.                                │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Composes and executes outbound payments. Routes through Tesote network (when both sides on platform → instant) or external rails (BNC, Banesco, wire). Auto-generates retention vouchers.

**Net-new for command center:**
- Inbound flow feeds Pagos directly: approved vendor invoice → payment composition → execution. One loop instead of two disconnected workflows.
- Counterparty record carries preferred payment channel — Tesote knows automatically.

**Status:** B2C rail LIVE. B2B (juridico → juridico) bank-gated. Mission-critical 2026 priority per project memory ([[payments-10x-bet]]).

**Source docs:** [[business/pagos/]] (index), [[business/pagos/plans/pro-112-dan-super-app]], [[business/pagos/rails/]] per provider.

---

### V.3 Tesote Negocios — Cobros

```
┌──────────────────────────────────────────────────────────────────┐
│  Negocios · Cobros ↓                                             │
│  ───                                                             │
│  Outbound invoice routing + chase workflow + customer payment    │
│  portal. The collection loop.                                    │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Sender-side experience for outbound invoices (PRO-112 workspace-shell Cobros stream). The sender creates / sends / tracks / reconciles invoices. The payer side lives in the counterparty portal.

**Net-new for command center:**
- The **outbound invoice routing engine** — Tesote (not Odoo) routes the invoice to the counterparty. Odoo emits the legal artifact; Tesote owns the customer relationship.
- **FX-aware invoice generation** — pulls live BCV, applies per-subscription differential, instructs Odoo to emit with the right base imponible + BS conversion. Kills the Excel calc.
- **Reconciliation back-write** — bank txn matched in Tesote → paid status pushed back to Odoo.

**Status:** Cobros spec exists ([[business/cobros/cobros-spec]], frozen 2026-04-23 review). PRO-112 workspace-shell prototype is the visual canonical. Outbound routing one-pager ([[business/cobros/outbound-invoice-routing]]) layers the command-center scope on top.

**Source docs:** [[business/cobros/cobros-spec]] (deep spec), [[business/cobros/outbound-invoice-routing]] (command-center additions), [[business/cobros/banesco-rails-readiness]], `prototypes/pro-112/workspace-shell.html`.

**Merge note (per 2026-05-12 alignment):** outbound-invoice-routing + cobros-spec to be consolidated into one canonical spec in subsequent iteration. Original cobros-spec preserved; routing one-pager preserved; merged successor TBD.

---

### V.4 Tesote Negocios — Contrapartes (Counterparties)

```
┌──────────────────────────────────────────────────────────────────┐
│  Negocios · Contrapartes                                         │
│  ───                                                             │
│  The spine of the command center. Customers + vendors. Entity,   │
│  subscriptions, payment terms, FX rate, contract metadata.       │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** The canonical record of everyone the workspace transacts with. Per counterparty: identity (legal name, commercial name, RIF/RNC/EIN), country, contact info, role (customer/vendor/both), billing relationships across N entities, active subscriptions, contracts, payment behavior history.

**Net-new for command center:**
- **Multi-entity counterparty** — one counterparty, N billing relationships across our entities (e.g., Polar group billed from both VE and US entities). Day-one schema.
- **Subscription ownership** — subscriptions live on the counterparty record in Tesote, not in Odoo. Odoo executes accounting; Tesote owns commerce.
- **Per-subscription FX rate** — BCV+differential template (or custom) as a first-class field.
- **Contract-rooted** — contracts uploaded via Inbound flow spawn subscription records here.

**Status:** Schema spec'd in [[business/counterparties/system-of-record]]. Counterparty-facing portal PRD exists ([[business/counterparties/counterparty-portal-prd]]) and remains canonical for the payer-side experience.

**Source docs:** [[business/counterparties/system-of-record]] (spine doc), [[business/counterparties/counterparty-portal-prd]] (portal PRD), [[business/counterparties/]] (index).

---

### V.5 Tesote Automatizaciones — Contabilidad

```
┌──────────────────────────────────────────────────────────────────┐
│  Automatizaciones · Contabilidad                                 │
│  ───                                                             │
│  Inbound document inbox + AI extraction + push-to-Odoo. The      │
│  daily operating UI for the command center. Where Mariel lives.  │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** The structured-workflow product. Inbound document queues (vendor invoices, contracts, retentions, receipts), reconciliation engine, mapping config, productized monthly close. AI suggests; human approves; Tesote pushes to Odoo.

**Net-new for command center:**
- The **inbound inbox surface** generalizes Cap #2 (AP automation) from the Cockpit PRD to all external document types.
- The cockpit framing was directionally right — this is its full expression.
- Caps #1/#2/#3/#5 from the Cockpit PRD re-bucket cleanly under here:
  - **Cap #1 (AI transaction coding)** — reconciliation side of inbound + outbound flows
  - **Cap #2 (AP automation)** — graduates into the broader inbound inbox
  - **Cap #3 (Bank reconciliation)** — the reconciliation engine in the outbound loop
  - **Cap #5 (Counterparty management)** — owned by V.4 above

**Status:** Cockpit PRD ([[automations/accounting-automation/odoo-prd]]) remains the foundational PRD. Inbound inbox one-pager ([[automations/accounting-automation/inbound-inbox]]) layers command-center scope. Prototypes folder has interactive HTML for preflight, mapping, banks, rules, queue, AP inbox, dashboard, recon.

**Source docs:** [[automations/accounting-automation/odoo-prd]] (Cockpit PRD), [[automations/accounting-automation/inbound-inbox]] (command-center additions), `prototypes/` (interactive HTML).

---

### V.6 Tesote Automatizaciones — Reportes

```
┌──────────────────────────────────────────────────────────────────┐
│  Automatizaciones · Reportes                                     │
│  ───                                                             │
│  Scheduled / on-demand outputs to clients. The reporting layer.  │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Generates the recurring outputs finance teams produce — AR aging, AP aging, retention summaries, cash position, monthly close reports, custom dashboards.

**Net-new for command center:**
- Reads from the SoR (Tesote) — not from Odoo. Reports are instant because the data is already in Tesote.
- AI-assisted custom report generation (post-v1).

**Status:** Scaffolding in the workspace-shell prototype. No deep spec yet.

**Source docs:** [[automations/]] (index).

---

### V.7 Tesote IA

```
┌──────────────────────────────────────────────────────────────────┐
│  Tesote IA                                                       │
│  ───                                                             │
│  The conversational surface for the command center.              │
│  Chatbot in Tesote UI. MCP under the hood. Zero coupling to      │
│  Tesote core. Ship-fast product.                                 │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Customer talks to AI; AI reads from Odoo + Tesote state and writes back with confirmation. Tesote-branded chatbot in Tesote UI (only surface — no external MCP, no Claude-desktop dependency until the market matures). Curated use-case gallery + suggested prompts.

**Net-new for command center:**
- Becomes the conversational lane *into* the command center. Same actions available in the UI are askable in chat.
- AI also lives as utility under the hood (see Part VI) — but the chat surface here is its productized expression.

**Status:** Tesote AI for Odoo is the active draft ([[automations/erp-ai/odoo-mcp]]). Per project memory ([[odoo-mcp-framing]]): chat-only, gallery v1, LATAM-native by default (Spanish, VE/LATAM compliance, local tax codes), read-first / write-with-confirmation.

**Source docs:** [[automations/erp-ai/odoo-mcp]] (active draft), [[automations/erp-ai/]] (index).

---

### V.8 Capital (future)

```
┌──────────────────────────────────────────────────────────────────┐
│  Capital (placeholder)                                           │
│  ───                                                             │
│  Financing / lending / treasury. Tier 2 gating in PRO-112.       │
│  Underwriting moat: invoice + retention + payment data           │
│  combined.                                                       │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Tesote Capital — factoring, credit lines, reverse factoring — underwritten on the differentiated dataset the command center accumulates (invoices, retentions, payments, two-sided counterparty graph).

**Status:** Placeholder per project memory ([[product-taxonomy]]). Tier 2 gate in PRO-112 super-app spec ([[business/pagos/plans/pro-112-dan-super-app]] epic G.7).

**Defensibility note:** The command center is the precondition for credible capital. Without owning the operating data on both sides, underwriting is generic.

---

### V.9 Taxes / Retenciones

```
┌──────────────────────────────────────────────────────────────────┐
│  Taxes / Retenciones                                             │
│  ───                                                             │
│  VE retention engine (IVA/ISLR). SENIAT XML export.              │
│  Lock-in territory.                                              │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Detects contribuyente especial from SENIAT profile, auto-calculates IVA/ISLR on payment, auto-generates + numbers + delivers comprobantes, YTD ledger, simplified monthly SENIAT XML export.

**Net-new for command center:**
- Both inbound (retention vouchers we receive) and outbound (vouchers we issue) flow through the same machinery.
- Counterparty record carries SENIAT profile + retention metadata.

**Status:** Epic E in PRO-112 super-app spec. Tier 1 v1.1 (deferred from initial v1 to keep scope contained).

**Source docs:** `product/taxes/` index, PRO-112 super-app spec epic E.

---

### V.10 Espacio de Trabajo

```
┌──────────────────────────────────────────────────────────────────┐
│  Espacio de Trabajo                                              │
│  Mi equipo · Permisos · Configuración                            │
│  ───                                                             │
│  Workspace administration. Out of the daily operating loop.      │
└──────────────────────────────────────────────────────────────────┘
```

**What it does:** Multi-entity workspace setup, team roles (AP clerk, controller, CFO, auditor), permissions, configuration. Tier 2 gates per PRO-112.

**Status:** Section locked in the workspace-shell prototype. Tier 2 capabilities defined in PRO-112 epic G.

---

## Part VI — The Data Model

### Counterparty (the spine)

A **counterparty** is an entity (company or individual) the workspace transacts with. One counterparty can be a customer, vendor, or both, across multiple billing relationships with our entities.

```
Counterparty
├── id
├── legal_name
├── commercial_name (if different)
├── tax_id (RIF / RNC / EIN)
├── country_of_registration
├── default_contact (email + phone/WhatsApp)
├── roles: [customer, vendor, both]
└── billing_relationships: [BillingRelationship, ...]
```

### BillingRelationship (multi-entity link)

One counterparty has **N billing relationships** — one per our-entity that transacts with them. This is the multi-entity counterparty schema; day-one requirement.

```
BillingRelationship
├── id
├── counterparty_id → Counterparty
├── our_entity (TST Servicios VE / Tesote Technologies US / TST DR)
├── relationship_role (customer_of / vendor_of / both)
├── payment_terms_default (immediate / 7d / 15d / EOM+30 / ...)
├── preferred_payment_channel (wire / ACH / Zelle / Banesco / Stripe / cash)
├── legal_address (per-jurisdiction)
├── notes
└── subscriptions: [Subscription, ...]
```

### Subscription (owned by Tesote, executed by Odoo)

```
Subscription
├── id
├── billing_relationship_id → BillingRelationship
├── product (what they're paying for)
├── cadence (monthly / quarterly / semi-annual / annual / custom)
├── next_invoice_date (computed — the action trigger)
├── base_amount + base_currency
├── fx_rate_rule (see below)
├── terms_override (overrides BillingRelationship default if needed)
├── status (active / paused / cancelled)
└── contract_ref → Contract
```

### FX rate rule (per-subscription)

Lives on the subscription because the same counterparty can have different FX terms on different subscriptions.

```
FXRateRule
├── fx_source (BCV / BCV+differential / paralelo / custom / none)
├── fx_differential_bps (when BCV+differential — e.g., 3000 = 30%)
└── fx_freeze_at (emission / payment)
```

**VE default:** `fx_source = BCV+differential`, `fx_freeze_at = payment`. Auto-calc adjustment between emission and payment dates; base imponible (USD) stays constant; BCV-converted total updates at payment. Aligned with Mariel 2026-05-12.

### Contract

```
Contract
├── id
├── counterparty_id → Counterparty
├── file (uploaded PDF)
├── extracted_terms (AI-parsed: parties, scope, term, renewal, payment, FX)
├── status (draft / active / expired / terminated)
└── generated_subscriptions: [Subscription, ...] (back-refs)
```

Contracts land in Tesote via Inbound flow → AI extracts → user confirms → subscriptions spawn with the contract as their source.

### Document (the inbound queue object)

Every inbound document becomes a typed record:

```
Document
├── id
├── type (vendor_invoice / contract / retention_voucher / receipt / sales_order / ...)
├── source (email / upload / whatsapp / integration)
├── arrived_at
├── entity (which of our entities it belongs to)
├── extracted (AI-parsed structured fields per type)
├── status (pending_review / approved / pushed / rejected)
├── counterparty_id → Counterparty (when matched)
└── pushed_to_odoo_at (when applicable)
```

### Cobro (outbound invoice — from cobros-spec)

```
Cobro
├── id
├── workspace_id
├── counterparty_id → Counterparty
├── subscription_id → Subscription (when generated from a subscription)
├── amount_ves + amount_usd
├── invoice_number (Odoo's legal number)
├── origin (subscription / directo / odoo_manual)
├── state (borrador / enviada / vista / aprobada / vencida / link_expirado /
│          cancelada / procesando / pagada / fallida)
├── timestamps
├── payment_link_token
└── receiving_account_id
```

### Cross-entity invariants

- **One counterparty = one identity.** Same RIF/RNC/EIN resolves to one counterparty even if it appears in multiple billing relationships.
- **Subscriptions cannot exist without a billing relationship.** Contract may be optional in v1 but the billing relationship is mandatory.
- **FX rate is always known at invoice emission time.** Even when frozen at payment, the rule + rate-at-emission are recorded for audit.
- **Every document push to Odoo is reversible / re-emittable.** Odoo writeback is idempotent.

### Source docs feeding this section

- [[business/counterparties/system-of-record]] (canonical schema)
- [[business/cobros/cobros-spec]] (Cobro entity, EmailRecord, Reminder, Event)
- PRO-112 super-app spec (Tier 0/1/2 progression on counterparty)

---

## Part VII — The AI Strategy

### Principle: AI is a utility everywhere; a product surface in one place

Per the 2026-05-12 alignment: AI extraction is a workflow utility — "it's just OCR" — not a standalone product. The pattern applies broadly:

- **Where AI is utility (no separate surface):** inbound extraction (invoices, contracts, receipts), counterparty resolution, suggested GL coding, anomaly detection, chase prioritization, retention auto-calc, FX rate rule suggestion.
- **Where AI is a product surface:** Tesote IA (the chatbot). One conversational lane into the command center.

This avoids the trap of building an "AI Surface" as competition to every other surface. AI runs in the workflows where it adds value; the chatbot is its conversational expression.

### AI utility — capabilities by surface

| Surface | AI capability | Status |
|---|---|---|
| Contabilidad / inbound inbox | Document extraction (invoices, contracts, receipts) | Active design |
| Contabilidad / inbound inbox | Auto GL coding suggestion | Cockpit PRD Cap #1 |
| Contabilidad / reconciliation | Bank txn ↔ invoice matching | Cockpit PRD Cap #3 |
| Contrapartes | SENIAT lookup + identity resolution | Cockpit PRD Cap #5 |
| Cobros | Chase prioritization (bad-payer detection) | New — from 2026-05-12 sync |
| Cobros | Reminder cadence + tone selection | Active design |
| Pagos | Payment-channel suggestion | Future |
| Taxes / Retenciones | Auto contribuyente-especial detection | PRO-112 epic E |
| Reportes | Custom-report generation | Future |

All operate **read-first, write-with-confirmation**. AI never pushes to Odoo without human approval in v1.

### AI surface — Tesote IA

The conversational expression. Per [[odoo-mcp-framing]]:

- Chatbot in Tesote UI only (no external MCP, no Claude Desktop dependency until the market matures)
- Zero coupling to Tesote core (Connect / Pagos / Cobros not in critical path — IA reads via MCP)
- LATAM-native by default (Spanish, VE/LATAM compliance, local tax codes)
- Guided experience: use-case galleries, suggested prompts, curated wow-moment
- Read-first / write-with-confirmation

**Source doc:** [[automations/erp-ai/odoo-mcp]].

### Workspace AI (multi-surface bridges)

Per [[automations/erp-workspace-ai/]]: AI that spans the ERP and workspace tools (email, Drive, Slack, WhatsApp). These are *plumbing* into the command center — they feed documents into the inbound inbox, push notifications out from ERP signals.

Examples in scope:
- Email → AP entry (vendor invoice from Gmail → inbound inbox)
- WhatsApp → expense capture (receipt photo → inbound inbox)
- Drive → batch import (folder of PDFs → inbound inbox)
- ERP → Slack notification (cash position, AR aging alerts)

**Source doc:** [[automations/erp-workspace-ai/]] (index, placeholder for active product thinking).

---

## Part VIII — The Customer Experience

### PRO-112 super-app — the customer-facing half of the command center

When our customer (a Tesote workspace) sends an invoice via the outbound flow, *their* counterparty experiences the command center from the outside in. PRO-112's three-tier model:

```
Tier 0 — Counterparty (passive)
   • Row in a Tesote workspace's counterparty table
   • Receives "Ver factura →" email/WhatsApp

         ↓  (claim flow — signed URL access)

Tier 1 — Portal user
   • Pre-filled SENIAT-verified profile
   • Unified inbox across all Tesote senders (B.1)
   • Full invoice detail (line items, IVA, retentions, net due) (B.2)
   • Native 4-step pay flow (BNC ACH OTP, per-tx OTP) (D.1-D.5)
   • Auto-generated comprobante delivered to payee (D.5)
   • "Powered by Tesote" BNC upgrade — the monetization event (C.1-C.5)
   • Multi-invoice pay (locked 2026-04-29)
   • Counterparty 360 (read-only)

         ↓  (graduation when ready)

Tier 2 — Workspace (existing, expanded)
   • Multi-entity, team roles, retentions engine (E)
   • Tesote Capital (G.7)
   • Multi-currency, ERP import/export, API (G)
   • Subscription + reduced fees + capital revenue
```

### What changes with the command-center reframe

The PRO-112 model itself stays. What changes is what the workspace side (Tier 2) sees:

- **Same shell** (workspace-shell.html chassis)
- **Deeper surfaces** (Contabilidad now has the inbound inbox; Contrapartes carries the multi-entity SoR schema; Cobros has FX-aware routing)
- **More that's "Powered by Tesote"** — Pagos rails reach further, Capital underwrites on the richer dataset, Taxes auto-handles retentions

For the Tier 0 → Tier 1 counterparty, very little changes — the claim flow + portal + pay flow remain as-specified. The lock-ins from 2026-04-25 (email-only first-time auth, OTP returning, BNC ACH per-tx OTP, comprobante delivery) hold.

### Network effects

PRO-112's headline data still holds:

- 72% of active workspaces already have BNC connected
- 85% of identifiable intra-Tesote counterparty pairs are already BNC-ready on both sides
- 116 of 629 SENIAT-resolved counterparty identities (18%) are themselves Tesote legal entities

The command center makes these connections operate at full bandwidth — once both sides are on Tesote, the entire loop (invoice → pay → reconcile → retention → ledger) collapses into a single transaction.

### Source docs feeding this section

- [[business/pagos/plans/pro-112-dan-super-app]] (super-app spec)
- [[business/counterparties/counterparty-portal-prd]] (portal PRD v1)
- `product/business/pagos/prototypes/pro-112/claim-flow.html` (canonical claim-flow prototype)
- `product/business/pagos/prototypes/pro-112/README.md` (engineering handoff packet)

---

## Part IX — The Path Forward

### Dogfooding as the North Star

The first instance of this command center runs on Tesote's own books. Mariel is the design partner. We ship the loop end-to-end for VE first, then DR, then US (after QB → Odoo migration).

The discovery trail and finance-team plan live at [[../finance/ar-and-cobros-2026-05-team]]. The three tracks running today:

- **Track 1** — Direct AR outreach on the largest outstanding VE invoices (Luis + Roberto, underway 2026-05-12)
- **Track 2** — Build the command center (this PRD's execution plan)
- **Track 3** — Pilot Tesote cobros on Tesote AR (waits for v1 outbound)

### The v1 wedge — outbound loop end-to-end for ONE VE customer

The smallest cut that proves the architecture:

```
Subscription cycle triggers in Tesote
  ↓ Tesote → Odoo emit (use existing Odoo capability; just trigger from Tesote)
  ↓ Tesote routes invoice with Banesco payment link (existing portal — claim-flow.html)
  ↓ Customer pays via portal (live B2C rails — BNC ACH OTP)
  ↓ Tesote reconciles bank txn → writes paid status back to Odoo
```

If this ships for ONE VE customer this quarter, every architectural piece has been touched. Then expand to N customers, then to other flows, then to other entities.

### What sequences after v1

```
v1 (Q3 2026)   — Outbound loop, ONE VE customer, end-to-end
v1.1 (Q3 2026) — N VE customers; FX-aware invoicing productized
v1.2 (Q4 2026) — Inbound inbox v1 (vendor invoices + receipts for VE)
v2 (Q4 2026)   — Contracts in the inbound flow; subscription auto-spawn
v2.1 (Q4 2026) — DR entity onto the loop
v3 (2027)      — US entity onto the loop (post-QB → Odoo)
v3.1+ (2027)   — Capital surface activated; multi-step approval; v2 inbound channels
```

This is provisional sequencing — actual cadence depends on engineering capacity and the discipline calls below.

### Discipline calls — what slips to free bandwidth

The command center is a lot of net-new work. Candidates to delay or cut:

- **Capital surfaces** (placeholder anyway — defer to v3+)
- **DR / US command center** (VE first; others later)
- **Multi-step AP approval** (single-step is v1 per resolved Q #3)
- **Vendor-portal inbound integrations** (v2 — email + upload is v1)
- **QB → Odoo US migration** (strategic dependency, but doesn't block VE v1)
- **Retentions engine** (Tier 1 v1.1 in PRO-112; defer per existing plan)

### Open decisions to make

Some are open in source PRDs; others are surfaced by this synthesis.

| # | Decision | Owner | Status |
|---|---|---|---|
| 1 | Brand split for counterparty portal (tesotenegocios.com vs subdomain vs same app) | Luis | Open (PRO-112) |
| 2 | First-login portal empty state | Luis | Open (PRO-112) |
| 3 | Multi-RIF at Tier 1 | Luis | Deferred unless blocking |
| 4 | Codebase split (portal as separate service vs logged-out view) | Dan | Open |
| 5 | Inbox data model (invoice on sender vs dedicated counterparty inbox) | Dan | Open |
| 6 | Cobros §9 — 10 product Qs | Luis | Open in spec |
| 7 | VE e-invoicing path (when SENIAT path is feasible) | TBD | Watch |
| 8 | How fast does QB → Odoo US migration land? | Luis + Dan | Schedule |
| 9 | Reconcile Cobros spec ↔ outbound-invoice-routing one-pager | Luis | Merge per 2026-05-12 |
| 10 | Reconcile Cockpit PRD with command-center framing (amend, not rewrite) | Majo + Luis | Amend per 2026-05-12 |

### Who needs to weigh in next

In order:

1. **Majo (PM)** — biggest impact on her work. She owns the Cockpit PRD; reframing affects scope, sequencing, prototypes. Walk her through this PRD.
2. **Dan (eng)** — architecture sign-off, counterparty schema, the Odoo writeback engine. Walk him through this PRD + the spine doc.
3. **Mariel (finance)** — confirm design partner role; current workflow stays for now; she'll touch UI in a few weeks.
4. **The broader team** — once Majo + Dan are in, share more widely.

### What I'd do this week

- **Today/tomorrow:** review this PRD, redirect anything that's off
- **This week:** walkthrough with Majo and Dan; capture their feedback
- **This week:** confirm the v1 wedge scope; lock the engineering ticket sequence
- **Next week:** start the Track 2 build (counterparty schema upgrade is likely first; everything else hangs off it)
- **Continuously:** Tracks 1 and 3 run in parallel

---

## References

### Internal source docs (this PRD synthesizes from)

**Spine + architecture**
- [[business/counterparties/system-of-record]] — the spine; architectural commitment + canonical schema
- [[../finance/ar-and-cobros-2026-05-team]] — discovery trail + finance-team plan

**Counterparties**
- [[business/counterparties/counterparty-portal-prd]] — counterparty-facing portal PRD v1
- [[business/counterparties/]] — index

**Cobros**
- [[business/cobros/cobros-spec]] — workspace Cobros deep spec (frozen 2026-04-23)
- [[business/cobros/outbound-invoice-routing]] — command-center additions (one-pager)
- [[business/cobros/banesco-rails-readiness]]
- [[business/cobros/2026-05-10-session-banesco-kickoff]]
- [[business/cobros/]] — index

**Pagos**
- [[business/pagos/plans/pro-112-dan-super-app]] — three-tier super-app spec (Dan, mirrored)
- `product/business/pagos/prototypes/pro-112/workspace-shell.html` — canonical workspace prototype
- `product/business/pagos/prototypes/pro-112/claim-flow.html` — canonical counterparty prototype
- `product/business/pagos/prototypes/pro-112/README.md` — engineering handoff packet
- [[business/pagos/]] — index
- `product/business/pagos/rails/` — bank-side plumbing per rail

**Automations**
- [[automations/accounting-automation/odoo-prd]] — Cockpit PRD (Caps #1/#2/#3/#5)
- [[automations/accounting-automation/inbound-inbox]] — first-landing-place one-pager
- [[automations/accounting-automation/]] — index
- [[automations/erp-ai/odoo-mcp]] — Tesote AI for Odoo (active draft)
- [[automations/erp-ai/]] — index
- [[automations/erp-workspace-ai/]] — multi-surface bridges (placeholder)
- [[automations/]] — index

**Other surfaces**
- [[connect/]] — multi-jurisdiction bank rails
- [[dashboard/]] — workspace cockpit
- [[capital/]] — financing (placeholder)
- [[taxes/]] — retenciones / SENIAT
- [[ai/]] — AI-native surface (placeholder)
- [[design/]] — design system

### External sources

- Linear PRO-112 — `https://linear.app/tesote/issue/PRO-112/tesote-super-app-counterparty-portal-workspace-funnel-spec-wireframes`
- Treasury Rails app at `~/Programming/tesote/treasury` — data-model source of truth (per project memory [[treasury-repo]])

### Memory references (load-bearing context)

- [[tesote-command-center]] — the 2026-05-12 architectural lock-in
- [[odoo-cockpit-framing]] — superseded; cockpit graduated into command center
- [[odoo-mcp-framing]] — Tesote AI for Odoo working principles
- [[product-taxonomy]] — surface map
- [[payments-10x-bet]] — 2026 mission-critical priority
- [[connect-multi-jurisdiction]] — Connect scope (VE + PA + RD + US + Caribe)
- [[banesco-cobros-status]] — Banesco rails as the cobros build path

---

## Appendix A — Glossary

| Term | Meaning |
|---|---|
| **Command center** | Tesote's role as the operating layer + system of record on top of the ERP(s) |
| **System of record (SoR)** | Tesote owns counterparties, subscriptions, contracts, payment status. Odoo owns the legal GL. |
| **Execution layer** | The ERP (Odoo today, others later) that handles legal invoicing, accounting, fiscalización |
| **Inbound flow** | External document → Tesote inbox → AI extract → user approve → push to Odoo |
| **Outbound flow** | Subscription cycle → Odoo emit → Tesote route → customer pay → Tesote reconcile → Odoo writeback |
| **BCV** | Banco Central de Venezuela — the official VE exchange rate |
| **BCV+differential** | The standardized invoicing rate Mariel and Luis aligned on 2026-05-12 |
| **Fiscalización** | VE tax-audit compliance; the legal-record requirement for invoices |
| **Comprobante de retención** | VE-mandated retention voucher; IVA/ISLR proof of withholding |
| **Counterparty** | Any entity the workspace transacts with (customer, vendor, or both) |
| **Billing relationship** | The link between a counterparty and one of our entities, with its own terms |
| **Tier 0/1/2** | PRO-112 super-app graduation model (passive → portal user → full workspace) |
| **"Powered by Tesote"** | BNC account upgrade flow that becomes payment-enabled inside Tesote |

---

*This PRD is a draft v1, dated 2026-05-12. Iteration expected. Source docs above remain canonical for their respective surfaces; this PRD synthesizes them under the command-center architecture.*
