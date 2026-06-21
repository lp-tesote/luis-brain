---
title: The Confirmation Ladder — how Tesote designs cash-confirmation solutions
tags: [product, connect, pagos, cobros, strategy, bank-apis]
updated: 2026-06-16
status: draft
---

# The Confirmation Ladder

How Tesote scopes and designs a cash-confirmation solution for any company, in the
world of the bank-API transition. This is the operating model behind every future
solution-design conversation — not a single client's spec.

The core question every B2B company is really asking us is: **"how do I know I got
paid, fast enough and cleanly enough to act on it?"** Releasing product, extending
credit, reconciling, reporting position — all of it rides on the quality of that
confirmation. This framework is how we answer it honestly.

## The decision underneath everything: scraping is off the menu

Today, scraping is how Tesote fakes uniform coverage — "we connect every bank." Going
forward we trade that pitch for **integrity**: we only confirm cash through mechanisms
that are sanctioned and durable (real bank APIs, botón de pagos), and we are honest
where a structural gap exists.

This is a deliberate positioning decision, with a real tradeoff:

- **We lose** the "we cover everything in real-time" line.
- **We gain** durability (no portal-change breakage, no silent data rot), an SLA we can
  actually stand behind, and a **botón attach on every deal where there's a real-time
  gap.** Scraping is a cost center and a liability; botón is a revenue line and a moat.

The moment we promise a scraping-backed "real-time" for a bank that doesn't offer it,
we are back in today's fragility. We don't. We name the constraint and sell the botón
as the answer to it.

## The ladder — the menu we design against

Every collection channel a company has lands on exactly one rung. Two axes people
conflate: **latency** (real-time vs T-1) and **integrity** (immutable at source vs
provisional-then-finalized).

| Rung | Mechanism | Latency | Integrity | Use for |
|---|---|---|---|---|
| 1 | **Botón de Pago / C2P** | Real-time | Immutable — authorization tied to your invoice | Release decisions. Bank-agnostic. The only mechanism that is both real-time *and* clean. |
| 2 | **Real-time bank API** | Real-time | Provisional → Tesote absorbs the drift via a stable canonical ID | Fast detection where payer-ID is present; release on a confidence policy. |
| 3 | **T-1 bank API** | Next-day | Settled / clean | Reconciliation, cash position, posting — *not* release. |
| 4 | ~~Scraping~~ | — | Fragile | **Off the menu.** |

Two properties of the ladder that matter when designing:

- **Real-time ≠ immutable.** Rung 2 banks deliver fast but the line is still
  provisional until overnight settlement (reference number, cents, description can all
  change at T-1). Tesote absorbs that drift behind a stable canonical record so the
  client's downstream system never sees the mutation or a duplicate — but the *release
  decision* on a rung-2 detection is still a risk call, not a certainty. Only rung 1 is
  truly immutable at the moment of confirmation.
- **Timely data is not the same as matchable data.** A real-time API with no payer-ID
  (RIF) in the feed is still a manual match. Confirmation needs *both* — fast and
  identifiable. Always overlay payer-ID availability on top of the rung.

## The diagnostic — how to scope any company

Five questions, in order.

**1. What's their collection footprint?**
Which banks, what % of value through each, what instrument mix (LBTR / transferencia /
pago móvil). Per-bank nomenclature/payer-ID scoring is part of this step — institutionalize it.

**2. What does the data *trigger*?**
The question nobody asks. Release product? Extend credit? Just reconcile? Report
position? The trigger sets the *real* latency requirement. People ask for "real-time"
when they mean "fast enough not to block fulfillment" — those are different specs.

**3. What's the cost of being wrong vs. late?**
Release-before-confirmed = credit risk (sized per customer). Reconcile-late = ops
friction (cheap). This tells you where real-time is worth paying for and where T-1 is
genuinely fine.

**4. Map footprint × ladder × payer-ID.**
Place each channel on its rung and mark whether the feed carries payer-ID. The **gap** =
real-time-need channels that run through T-1 banks, no-API banks, or no-payer-ID feeds.

**5. The gap is botón territory.**
This is where you co-design. *"Here's where you get clean real-time today. Here's where
the bank structurally can't give it to you. For those collections, here's the botón — or
you accept T-1 plus a per-customer risk policy. Which do you want?"*

## Why this "just works" as a motion

It flips the conversation from *"can you cover bank X?"* — a coverage arms race we lose
to scraping-based competitors — to *"what are you actually optimizing for, and what's the
cost of latency?"* — a consultative diagnostic where the botón is the natural answer to
the gap we just made visible.

We don't hide the constraint. We make the constraint the reason they need the botón. That
is a stronger and more defensible position than pretending it doesn't exist.

## The integrity mechanism (rung 2, briefly)

For real-time API channels, Tesote maintains a **canonical transaction record with a
stable ID** and a **provisional → confirmed lifecycle**: ingest the provisional intraday
line, match on stable keys + tolerance (payer-ID + amount band + account, never on the
fields banks mutate — reference / cents / description), emit a provisional signal; at T-1
re-match the settled line back to the *same* canonical record across the drift, finalize
the fields, promote to confirmed. The downstream system (ERP) sees one stable record that
gets enriched, never a mutation or a duplicate. This is what lets us put a rung-2 bank to
work for fast detection without inheriting its volatility.

> Eng note: the canonical-record + provisional→confirmed lifecycle + cross-drift
> re-matching is real schema/services work — a `/tesote-plan` candidate when a concrete
> client solution needs it (pulls in `database-design`, `product-management`).
