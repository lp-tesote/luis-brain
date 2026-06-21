---
title: B2C rail while B2B is gated — sell what's live
tags: [tesote-pay, customer-research, b2c, icp, 10x]
updated: 2026-05-05
status: draft
---

# B2C rail while B2B is gated — sell what's live

> Note recording where my head is at today on Tesote Pay segmentation. Not a plan yet — a setup for "find the names this week."

## The frame

Three segments in the market, grouped by who the Tesote customer **collects from**:

1. **B2B** — they collect from other companies. Rail = juridico → juridico interbank. **Blocked at the bank level today** (BNC biz-account OTP not yet enabled). We're working through the maze.
2. **Retail** — collections are physical/retail-flavored, mixed counterparty types. Mostly leans juridico → juridico interbank too.
3. **B2C** — they collect from individuals. Rail = juridico → natural interbank. **Live, tested end-to-end, working smoothly via BNC débito inmediato.**

Most of our customer base sits in B2B or Retail. That's where we've grown as a SaaS company. The natural reflex is to wait until juridico → juridico opens and then turn the firehose on.

But that's leaving money on the table for as long as the bank takes.

## The thing I don't want to ignore

The juridico → natural interbank rail is **already alive**. Validated. Not theoretical. We have a debit flow that works today, on production BNC, end-to-end, against any BCV-participating bank for the natural-person side.

Sleeping on that while we wait for juridico → juridico would be dumb. Even if B2C is a smaller slice of our base, it's:

- the only segment where revenue can start **today**, not after the bank moves
- a way to harden the product (recon, comprobantes, dispute flow, support patterns) under real volume before we open the floodgates on B2B
- proof to BNC that the rail works at scale → leverage when we push them on biz OTP
- proof to **the next bank** (Banesco, Banco Exterior) that there's already volume we'd point at them once they enable

So the question isn't "should we do B2C?" — it's **"who in our existing book or near-pipeline collects from individuals, and how fast can we put them on the rail?"**

## ICP for the live B2C rail

Rough cut, sharpen later:

- Tesote customer (or near-fit prospect) whose end-customer is a **natural person**
- Recurring or semi-recurring collections (so débito inmediato beats Pago Móvil/transfer ergonomics meaningfully)
- Has an **active BNC account** (per existing live-product gate — doesn't need to be primary receivables bank, just active)
- Volume meaningful enough that the operational lift (comprobantes, support) pays back

Verticals that come to mind off the top of my head — to validate, not commit:

- Education (colegios, institutos) — monthly tuition, payer is a parent/individual
- Health (clínicas, médicos, planes de salud) — copays, plans, monthly fees
- Subscription services (gym, software, streaming-like, suscripciones de servicios)
- Memberships & clubs
- Consumer services with recurring billing (mantenimiento, condominios where billed individually, seguros)
- Anything B2B2C where the **ultimate payer is an individual** even if our customer is a company

## What's next

This is a "starting the work" note, not a finished plan. Next moves:

1. **Pull the list.** Cross-reference our customer base against this ICP — who already fits? Sales + CX know this faster than I do; ask them.
2. **Pull the prospect list.** Same screen on the near-pipeline / inbound — anyone we've been talking to who fits this profile gets bumped.
3. **Sequence the outreach.** B2C rail is live; we should be able to onboard fast. The pitch is simple: "your customers are individuals, our rail to individuals works today, plug in."
4. **Track learnings here.** As we sell, capture which sub-verticals convert, which ops break, which ICP cuts hold up, which don't.
5. **Feed back into the B2B push.** Every B2C deal we close = a data point for BNC and the next bank that biz OTP would unlock more of the same.

## Why this matters

If we can sell this **today** while the juridico → juridico work plays out, it'd be gigantic. Time-to-revenue on the live rail is weeks, not quarters. Every month we wait for B2B is a month of compounding lost on a rail that's already paid for.

This isn't instead of the B2B fight — it's in parallel. B2B is still the bigger ceiling. But B2C is the only one that converts effort into revenue **right now**.

## Related

- [[../../strategy/product-strategy-execution-plan]] — overall payments execution plan
- [[../rails/bnc/index]] — BNC rail status (the rail powering this)
- [[../../drafts/bnc-ach-status]] — B2B (juridico → juridico) BNC enablement tracker
