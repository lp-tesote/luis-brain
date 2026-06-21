---
title: AR Tackle & Cobros Product Experiment — May 2026
tags: [finance, cobros, 10x, discovery]
updated: 2026-05-11
status: draft
---

# AR Tackle & Cobros Product Experiment — May 2026

## Why this doc exists

Mariel wants to hire someone in Finance because AR collection is painful. Roberto and I (Luis) are getting involved directly instead — both to take stress off her plate and to *understand the system* before adding people to it. The wedge: Tesote is building a cobros product anyway. Our own AR book becomes the highest-conviction beta.

**Operating principle:** discovery before staffing. Triangulate before chasing. System fix before hire.

## Twin goals

1. **Operational:** trustworthy AR snapshot, then collect the biggest outstanding receivables (VE).
2. **Product:** validate the Tesote cobros workflow (channels, timing, incentives, Odoo-native flows) on real Tesote AR before we ship it to clients.

If the operational fix works without a hire, Mariel's AR pain disappears *and* we ship cobros with real evidence. Two birds.

## Context map

| Entity | ERP | Currency | Rails | Notes |
|---|---|---|---|---|
| Delaware C-Corp (US) | QuickBooks | USD | Stripe (cards), wires, Zelle, USD cash (Caracas office) | Mariel owns books |
| Venezuelan entity | Odoo VE | BS | VE bank accounts | **Biggest AR pile** (gut) |
| DR entity | Odoo DR | DOP | DR bank accounts | Smallest, newest |

Mariel maintains an **isolated AR spreadsheet** alongside the three ERPs. We trust Mariel 100% — this is not an audit, it's us getting involved.

Cross-entity clients: rare per Luis. Not the prime suspect here.

## Tracks

### Track 1 — Pick up the phone (this week, starting tomorrow)

Roberto and I directly call the largest outstanding invoices in VE Odoo, prioritized by $ × days outstanding. Goals:
- Take call load off Mariel immediately
- Each call doubles as field research for cobros
- Document what each call reveals about *why* payment hasn't happened

**Log per client:**

| Client | Invoice # | Amount | Days outstanding | Channel (call/WA/email) | What they said | Promise | ETA |

Output: by end of week, a 15-20 row call log + a first read on the qualitative patterns (e.g., "always says next week", "lost the invoice", "wants payment plan", "claims already paid").

**Who:** Luis + Roberto
**When:** starts 2026-05-12

### Track 2 — Validate Mariel's spreadsheet vs. ERPs

Mariel's AR spreadsheet has to tie 1:1 with each of the three ERPs. If it doesn't, *that's* where "data feels incomplete/incorrect" comes from.

For each entity:
- Pull AR aging from the ERP (QB / Odoo VE / Odoo DR) as of today
- Compare to Mariel's spreadsheet
- Flag every delta

**Reconciliation table per entity:**

| Client | Invoice # | Spreadsheet $ | ERP $ | Δ | Why |

For each Δ, root cause: payment not matched? Stale balance? Item missing from one side? FX revaluation? Manual edit she made and didn't push to ERP?

**Who:** Luis + Roberto pull cold from the ERPs, then compare with Mariel's sheet
**When:** this week
**Output:** reconciled snapshot per entity + ranked list of root causes

### Track 3 — Identify the biggest bottlenecks

Once the data is trustworthy, sort:
- By entity (confirm VE is biggest by USD-equivalent)
- By client (top 10 oldest / largest outstanding items)
- By root cause:
  - **A.** Paid, not matched (system: payment-matching is broken)
  - **B.** Shouldn't have been invoiced (system: invoicing hygiene)
  - **C.** Real collections (behavior: client paying habits)
  - **D.** FX / revaluation (system: BS not revalued in Odoo VE)

**Hypothesis to test:** the VE pile is dominated by some mix of A (BS payments not matched), C (slow-paying VE clients with no consequence for being slow), and D (FX revaluation stale). Each has a different fix.

**Output:** ranked bottleneck list with $ impact + diagnosis (system vs. behavior vs. staffing).

### Track 4 — Map the subscription → invoice creation process

Upstream of AR. Tesote sells subscriptions on varying cadences — monthly, quarterly, custom. Each billing cycle, Mariel manually creates invoices in the right ERP for the right entity in the right currency. We believe this is one of the biggest time-sinks in her week, and a likely root cause of late or missing AR.

If invoices don't get created on time, the entire downstream collections workflow starts from behind. Fixing invoice creation is upstream of fixing collections — and probably the single biggest lever for getting hours back on Mariel's calendar.

**Discovery questions:**
- Walk us through: when a quarterly client's next invoice is due, how does it get generated? Step by step.
- How does she know *when* to create each invoice? Calendar? List? Memory?
- Where do the billing terms live — is there a contract repository, or are terms in her head / scattered files?
- Have there been cases where an invoice was generated late, with the wrong amount, for the wrong period, or in the wrong currency? How often?
- Is Odoo's native subscription module in use (VE / DR)? QB's recurring invoices (US)? If not, why not?
- Roughly what % of her week goes to invoice creation?

**Likely fixes to evaluate:**
- Turn on Odoo native subscription functionality (VE + DR)
- Turn on QB recurring invoices (US C-Corp)
- Build a thin Tesote-side scheduler that fires the right invoice on the right day into the right ERP, sourced from a single contract registry
- Eliminate manual data entry as a category of Mariel's work

**Connection to cobros:** invoice-on-time is a prerequisite for reminder-on-time. The cobros product likely needs an invoicing/billing layer as a sibling, not just a collections layer — they're two halves of the same revenue ops surface.

**Who:** Luis + Roberto with Mariel
**When:** parallel with Tracks 2-3 (this week + next); feeds into Track 5
**Output:** documented current process per entity, identified time-sinks, automation moves ranked by effort/impact.

### Track 5 — Tesote cobros on Tesote (product experiment)

Use the VE entity's AR book as the live dataset for testing Tesote cobros. Tesote is the highest-conviction beta customer because we own both sides — we know our own AP/AR habits, we can move fast, we can break things, we can measure honestly.

**What to test:**

- **Reminder channels:** WhatsApp vs. email vs. phone call vs. SMS. Measure response rate + days-to-payment per channel.
- **Reminder timing:** N days before due, on due date, N days after. Find the inflection.
- **Reminder tone:** friendly nudge / firm reminder / transactional. A/B on similar client profiles.
- **Incentives native to Tesote + Odoo:**
  - Pay-by-link directly in the reminder (lean on Banesco rails — see [[project_banesco_cobros_status]])
  - Early-payment discount baked into Odoo
  - Auto-escalation if no response in N days
  - Payment plans for stuck cases
- **Per-client tracking:** channel that worked, # of touches, what closed it, lessons.

**Hypothesis:** the AR problem isn't unique to Tesote. Every business in VE has it — the whole country runs on slow-paying receivables, across every sector and size. The workflow that solves it for us solves it for everyone else. The product features we discover are real because they're battle-tested on our own painful AR.

**Who:** Luis + Roberto run the experiment; learnings feed [[project_product_taxonomy]] → `product/business/cobros/`.
**When:** starts once Tracks 1-4 produce a clean target list and a sane invoicing baseline (likely week 2-3).
**Output:** dataset of what works for VE collections + concrete spec for the cobros product.

## Decision gates

- **Gate 1 (after Track 2):** Does Mariel's spreadsheet tie to the ERPs? If no → we now know what's broken on the data side, fix it first.
- **Gate 2 (after Tracks 3 + 4):** Is the staffing need real? If invoice creation is automatable **and** the collections bottleneck is system/behavior → no hire, fix the systems. Otherwise revisit hire scope, but with a much sharper job description.
- **Gate 3 (after Track 5):** Has the cobros workflow demonstrably shortened days-to-payment on a meaningful sample? If yes → productize and roll out features. If no → iterate the experiment, not the staffing.

## Open questions for Mariel (when we sit down)

- Does her spreadsheet cover all 3 entities, or just VE?
- Is the spreadsheet her source of truth (above the ERPs)? Or just a working file?
- How often does she update it, and from what inputs?
- For subscription clients: how does she track *when* the next invoice is due? Where do the contract terms actually live?
- Does Odoo VE / DR have any reminder/dunning workflow today? Email templates? Anything automated?
- Are BS-denominated invoices revalued at any cadence? Or aged at original BS amounts?
- Who in the client orgs typically pays us — finance, ops, the CEO directly?
- Top 3 most painful clients to chase — who and why?
- One thing she'd fix tomorrow if she could.
- One thing she does that she thinks a machine or another person should do.

## Message to Mariel (draft when this doc stabilizes)

Goals for the message:
- Acknowledge her stress is real — the AR pile is painful and shouldn't be hers alone.
- Tell her Roberto and I are stepping in this week to take call load directly.
- Frame: we want to understand the system before we add a person. Discovery before staffing.
- Specifically flag invoice creation as a place we want to dig — we suspect it's eating a lot of her week.
- Bonus: this is also field research for the cobros product — her pain becomes Tesote's product wedge.
- Be clear: **not** cutting her hire request. Re-sequencing. Let's see what we find first.
- Tone: we trust her completely. This is us showing up, not auditing.
- Ask: time this week to walk us through her process, ERP by ERP.

Length: short. 6-8 lines max. Spanish.

## Promote to KB (eventually)

- **Tracks 4-5 learnings** → `product/business/cobros/` in the shared KB once the invoicing + cobros workflow has real evidence behind it.
- **Tracks 1-3** stay in brain (sensitive — internal AR, client names, Mariel context).
