---
title: Tesote AI — Pricing Thinking
tags: [product, ai, pricing, finance]
updated: 2026-06-14
status: draft
---

# Tesote AI — Pricing Thinking

Working notes on how to price Tesote AI SKUs. Not yet locked. Come back to this once we have ~30-60 days of Mariel + first-cohort token usage data.

---

## Update 2026-06-14 — launch model: volume-primary, single SKU, margin-bounded

> **Supersedes the 3-SKU "Current best guess" table at the bottom.** Launch (June 22) is **Tesote MCP / Workspace only** — Odoo is wave 2 ([[launch-day-one-prd-v2]]). So launch pricing = **one SKU**, not three. The Workspace/Odoo/Bundle table is parked for the multi-connector future (see "Connector layering" below). This section reconciles [[pricing-references-legora-harvey-basis]] + [[launch-master-plan]] §4 with the cost reality.

### Price on banking-data volume; make seats a cap, not a headline

Two reasons, and they point the same way:

1. **Cost.** COGS has two terms — `tasks/mo × tokens/task × blended $/token`. Transaction volume drives *tokens per task* (a 2M-tx customer loads 1000× the context of a 2k-tx customer for the same "reconcile last month"), so tx-volume is a real **cost** proxy, not just a value proxy. But tx-volume alone doesn't bound cost — *frequency* does. So split the job: **tx-volume tier sets price + bounds tokens/task; per-user / usage cap bounds tasks/mo.** The seat cap is the **margin circuit breaker**, not a pricing axis.
2. **Positioning.** Competitors are per-seat and cheap-per-seat: **Claude Max $100–200/user/mo**; **Gemini now bundled into Google Workspace at $7–22/user** (AI effectively free in the suite). Price per seat → the CFO builds that spreadsheet and we lose, because we look like expensive horizontal AI. Price on workspace/volume/outcome → the comparison becomes a **finance-analyst FTE** (~$1.5–4k/mo loaded, VE) or Harvey-class vertical AI. **Never quote $/seat out loud.**

The moat line ([[winning-vs-horizontal-ai]]): Claude/Gemini are empty boxes the customer must feed. Tesote AI is pre-wired to their live bank data with the security + VE reconciliation context + connectors already built. We sell **integration + context + outcome on their actual books**, not intelligence (commoditized at $20/mo). That's what justifies 5–10× the horizontal per-seat price.

### The cost function & the 80% guarantee (extrapolatable per tier)

You don't price the customer, you price the **tier**, and each tier has a COGS ceiling pre-solved for 80% margin:

> **Worked, Starter $1,500/mo:**
> - 80% margin → COGS budget = **$300/mo**
> - Blended rate w/ aggressive routing (Haiku routine, Sonnet only for hard reasoning) ≈ **$2/M tokens**
> - $300 ÷ $2/M = 150M tokens/mo → at ~30k tokens/task → **~5,000 included tasks/mo** across all seats
> - As long as Starter's included allowance ≤ ~5,000 tasks/mo, **margin holds at 80% even at full consumption.** That number *is* the circuit breaker.

Only two ways a customer escapes its margin envelope, each plugged by one variable:

| Failure mode | What plugs it |
|---|---|
| `tokens/task` explodes (huge data) | **tx-volume tier reassignment** — a heavy-data customer isn't *allowed* on Starter; their per-task cost is priced into Scale |
| `tasks/mo` explodes (power users) | **the usage cap** — hitting it triggers the upsell conversation (= the §6 launch motion) |

There's **no path to <80% that doesn't trip a guard.** Worst case per tier = `included allowance × max tokens/task for the tier × worst-case all-Sonnet rate`, solved ≤ 20% of price *when the tier is defined*. Lock that math once per tier; never wonder per-customer.

- **Precondition:** routing must be live. All-Sonnet pushes blended to ~$5–8/M and shrinks allowance 3–4× — the 80% becomes fiction. Single biggest margin lever; confirm with Dan.
- **Intentional negative-margin zone:** the free trial to all users/workspaces is pure COGS, zero revenue. The trial count is the cost cap — size for worst case (every user × allowance) before June 22.

### Named tiers (one number per quote — the formula stays internal)

Don't quote a live formula in a demo — resolve seats × data into named tiers so the exec says one number:

| Tier | Lands here when | Quote |
|---|---|---|
| **Starter** | ≤10k tx/mo, ≤3 active seats | **$1,500/mo** ← Bucket-A instant-yes |
| **Growth** | 10–100k tx **or** 4–8 seats | ~$3,000/mo |
| **Scale** | 100k–1M tx **or** 9+ seats | ~$5–6k/mo |
| **Enterprise** | 1M+ tx | custom |

- $1,500 entry ÷ $21k MRR target = 14 logos at entry, fewer if accounts land higher.
- **Month-to-month at launch** (frictionless click-to-sign, "live next week"); convert happy users to annual at renewal, or "2 months free for annual prepay" as the upsell-on-the-upsell. Don't gate the launch yes behind an annual commitment (≠ Harvey/Legora, who can demand it).
- **Open input:** entry number must be a sane *ratio* to existing core MRR (~30–50% uplift = yes; doubling = no). Need typical core ACV to finalize.

### Connector layering (future-proofs the MCP roadmap)

Volume pricing is **connector-agnostic** — each new MCP lit up (Odoo, Gmail, next ERP) increases data/context, naturally pushing the customer up tiers, so we capture expansion **without a new SKU per connector.** Three layers, no more — don't nickel-and-dime per MCP (it fragments the one-number demo):

- **Base meter = banking-data volume** (Tesote MCP) — launch.
- **Premium modules = high-value ERP connectors** (Odoo, wave 2) — touches the regulatory record, a bigger value unlock; price it for **value** as a tier step-up / named module, not metered. This is the built-in upsell-on-the-upsell.
- **Commodity connectors** (Gmail, calendar) — included; just push volume.

## The SKUs we're considering

Three feature SKUs:

- **Tesote AI for Workspace** — $1-2k/mo (currently leaning $1.5k starter)
- **Tesote AI for Odoo only** — $1-2k/mo (currently leaning $1.5k starter)
- **Tesote AI for Workspace + Odoo (bundle)** — $3-4k/mo (currently leaning $2.5k starter to drive bundling; 17% discount vs standalone)

These are **starter-tier** prices. Customers vary 1000x in transaction volume (2k tx/mo to 2M tx/mo), so a flat price across all customers loses money on the heavy users and overcharges the light ones.

**Decouple feature SKU from price tier.** Same feature, different price band by tx volume:

- Starter (≤ 10k tx/mo) → 1.0x
- Growth (10k-100k tx/mo) → 1.5x
- Scale (100k-1M tx/mo) → 2-3x
- Enterprise (1M+ tx/mo) → custom quote

(Multipliers are guesses — anchor to whatever the core Tesote product already uses for tx-volume tiering so customers don't learn a new mental model.)

## Margin target: 80%

The anchor: every AI SKU should run at 80% gross margin against OpenRouter cost.

What that implies for token budgets:

- $1.5k SKU × 20% COGS = **$300/mo token budget per workspace**
- $3k bundle × 20% COGS = **$600/mo token budget per workspace**

At OpenRouter rates ($3/M input + $15/M output for Sonnet, ~5x cheaper for Haiku):

- $300/mo = ~30-50M Sonnet tokens, OR ~150-250M Haiku tokens, OR some mix
- Per "AI task": recon suggestion ~10k tokens, full agent loop 50-200k tokens
- So $300/mo budget = ~3-20k tasks/mo depending on complexity

We don't yet know what real customer usage looks like. **Mariel's workspace is the first data point** — track her token burn through end of June 2026 before locking caps.

## Overages — the 30% premium has a problem

Original idea: if customers exceed their cap, they pay overage tokens at +30% over our cost.

The math:

- **Inside the cap**: customer pays $5 of price for every $1 of token cost (80% margin)
- **Above the cap at +30%**: customer pays $1.30 for every $1 of cost (23% margin)

Overage tokens become **4x cheaper per-token than included tokens**. A 2M-tx customer rationally stays on the starter plan forever and overages, rather than upgrading tiers. The premium accidentally becomes a discount mechanism for heavy users.

### Two cleaner options

**Option A — Punitive overage (2-2.5x cost markup)**
Industry standard (Twilio, AWS, Stripe). Keeps margin healthy. Real intent isn't to earn on overage — it's to push customers into upgrading tiers. Frame as "fair use exceeded, let's talk tier upgrade."

**Option B — Soft overage + sales motion** *(probably right for first 6-12 months)*
No automatic billing. Hitting the cap triggers a conversation: "you're a heavier user, here's the next tier." Less mechanical, more relationship-driven. Better fit for fintech B2B with high-touch sales, and avoids surprise-bill churn while we still don't know real cost/customer.

Leaning B for now. Revisit when we have enough data to defend a specific overage rate.

## Communicating caps to customers

**Don't communicate token caps.** "Tokens" is invisible to customers and creates anxiety.

Better framings:

- "AI tasks per month" — a categorization, a recon suggestion, a draft email = 1 task each
- Or peg AI usage to transaction volume: "AI included up to your tx tier"

Set internal token budgets per task type — keep the math invisible.

## Three operational requirements (day 1, regardless of pricing structure)

1. **Per-tenant token accounting** — every OpenRouter call tagged by workspace/customer. Without this, we can't enforce caps, learn unit economics, or even bill overage if we want to. **Hard prerequisite.**
2. **Real-time customer-facing usage dashboard** — % of cap used this month, with 80% / 100% alerts. Surprise overage = NPS killer in B2B.
3. **Aggressive model routing** — 80% margin is realistic only if we route to Haiku/DeepSeek for routine tasks and reserve Sonnet/Opus for hard reasoning. If everything runs on Sonnet, 80% is hard to hit.

## Open questions before we lock

1. **What's Mariel actually burning?** Need 30-60 days of token data from her workspace to validate the $300/mo budget assumption.
2. **What's the routing strategy?** Is everything Sonnet today, or is there already a Haiku/Sonnet split by task type? This is the single biggest lever on margin.
3. **What does "Workspace AI" actually share with "Odoo AI"?** If the underlying model + tool calls are 80% shared, the bundle is the real product and the two standalone SKUs are anchoring devices. If they're genuinely two engines, the bundle math is different.
4. **What's a "workspace"?** If a customer has 5 workspaces, is each metered separately? Defines whether the $1.5k is per-customer or per-workspace.
5. **Does Tesote core already use tx-volume tiering?** AI pricing should rhyme with it, not invent a new mental model.

## Current best guess (subject to data) — ⚠️ SUPERSEDED 2026-06-14

> Parked. This 3-SKU view (Workspace / Odoo / Bundle) predates the launch decision to ship **Workspace-only** with **volume-primary** pricing. See the "Update 2026-06-14" section at the top. Kept for the multi-connector future.

| SKU | Starter (≤10k tx) | Growth (10k-100k) | Scale (100k-1M) |
|---|---|---|---|
| Workspace AI | $1,500 | $2,250 | $3,750-4,500 |
| Odoo AI | $1,500 | $2,250 | $3,750-4,500 |
| Bundle | $2,500 | $3,750 | $6,250-7,500 |

- Margin target: 80% gross
- Overage: soft (sales conversation) for first 6-12 months, revisit
- Caps communicated as "AI tasks/mo" not tokens
- Hard prereqs: per-tenant accounting + customer dashboard + model routing

## Next moves

- [ ] Get 30-60 days of Mariel's token usage data → validate $300/mo budget assumption
- [ ] Confirm tx-volume tiers match core Tesote product
- [ ] Decide: is Workspace AI + Odoo AI one engine or two? (talk to Dan)
- [ ] Build per-tenant token accounting (prereq, treasury work — likely `/tesote-plan` material)
- [ ] Sketch customer-facing usage dashboard
- [ ] Vero: align pricing communication with the [[pitch-agents-plus-ai]] narrative
