---
title: Tesote 2026 — The Resequence (Reallocation Thesis)
tags: [strategy, 10x, payments, ai, connect, sequencing]
updated: 2026-06-01
status: draft
---

# Tesote 2026 — The Resequence

Working strategy note from two conversations with Daniel on 2026-06-01 (one recorded, one not + a voicenote follow-up). This **revises the sequencing** in [[product-strategy-execution-plan]] (Apr 19), which leads with *"Payments ships first, everything waits behind it."* That ordering no longer matches how Luis + Dan are thinking. This doc is the new frame.

> Status: not yet team-wide. Lock the sequence this week, then promote.

---

## The thesis (the keystone)

The pivot is **not** "new products are more scalable" (true but soft). It's a **resource-reallocation argument:**

> Web scraping isn't just unscalable — it's a **resource sink**. It consumes the dev / support / ops capacity we already have. The team is talented but **trapped servicing scrapers**, so every new product launches starved. Release scraper pressure in the medium term → reallocate that *existing* capacity to AI + Negocios → which are scalable and reliable.

The unlock is **freeing** capacity, not **buying** it. That's why neither founder wants to raise to invest (see Fundraising below).

What remains proven and true regardless of rail: **data aggregation has very strong PMF** — whether delivered via web scraping or bank APIs. We are changing the *rail and the wrapper*, not the core value.

### The risk this exposes: it's a valley-crossing bet

We spend scarce capacity **now** (migration work) to free capacity **later**. During the valley, scrapers still run AND we're building the migration AND the new products. That's the real crunch. The ~$200k cushion (below) is what carries us across the valley — **not** growth capital. Frame it that way internally.

---

## The new ICP

Data aggregation via **bank APIs** + **payments (Negocios)** + **Odoo** + **Tesote AI** on top. Lead the sales conversation with the AI tooling, then "where does the data come in, at what frequency" — which forces the rail/process change downstream.

---

## The sequence (ordered — these are not equals)

### 1. Connect: scrapers → bank APIs  *(foundation)*

This is what frees the capacity the other two workstreams need. Two **separate plans** (different economics):

- **New customers — API-first from day one.** ~zero scraper pressure. This is just the new default onboarding. Do immediately.
- **Current customers — migration.** Batch-1 transition, change management. Harder. **This is where pressure-relief gets *measured*** — the load-bearing experiment of the whole thesis.

Batch-1 selection (this week): identify the bank connections that cause the most problems → who's attached → build the transition plan. Candidate banks for the API-first stack: BBVA, Mercantil, BNC, Banesco.

**Make the hypothesis a number, not a vibe:** today a net-new customer adds ~100% of a "unit of scraper pressure." If onboarded across the API banks, does that drop to ~20% (because ~80% of their tx flow through those banks)? Measure it. Everything hangs on this.

### 2. Tesote AI  *(sell now, but mind the destination)*

Packaging is a real decision — and it's a **ladder, not a pick-one:**

- **(a) Standalone for Odoo** — biggest TAM, **zero moat**. This is the horizontal trap in [[winning-vs-horizontal-ai]]: standalone, it's just reselling what Claude/ChatGPT + Odoo MCP already do. Good as a **wedge** — reps + revenue + kills FOMO *now*. Dangerous as the *destination*.
- **(b) Add-on to Tesote core** — deepens existing base, higher ACV, defensible (tied to our aggregated data).
- **(c) Add-on to core + Odoo** — this **is** the new ICP. Highest ACV, most defensible, longest to deliver.

**Decision:** sell (a) this week for reps — but be explicit it's a wedge. The durable SKU is **(c)**. Don't let the easy sale define the product.

### 3. Tesote Negocios (pagos / payables / receivables)  *(dogfood + first customers ASAP)*

Furthest out, most bank-dependent, fuzziest revenue model (unknown bank fees, unknown WTP). Depends on capacity freed by #1.

This week's posture (Dan's steer, Luis agreed): **product-dev + dogfooding over willingness-to-pay discovery.** End-of-week bar: "tesote finance is meaningfully better with the full portal." We've priced from $100 → $7,000 subscriptions before; if the product delivers real value reliably, the revenue model works out on the other end. Don't over-optimize the model up front.

> **Unresolved tension to watch:** dogfood-first (Dan) vs. get-reps-selling-now (Luis). Agreed in tone, not actually decided which *gates* which. Force this.

---

## Arturos — the proof case for the whole thesis

Prospect. ~**300k transactions/month**. Majority of their banks already have an **API relationship** with Tesote; some only via scrapers.

This is not just workstream #3's customer — it's the **instrument that turns the "100%→20% pressure relief" hypothesis into a number.** A huge-volume logo where we can flip most banks to APIs and *measure* the pressure delta, then upsell the destination ICP in one motion:

- **Tesote Connect** — majority via bank APIs + residual via scrapers
- **Tesote AI** on top of Connect data + Odoo

If the pressure-relief shows up on Arturos, the reallocation thesis is proven and the sequence locks itself. Land it framed exactly that way.

---

## Fundraising posture

Neither founder wants to raise **to invest** in the opportunity — the thesis is reallocation, not buying capacity.

- Only reason to take money now: a **liquidity cushion** to maintain current burn (close to breakeven; Dan has quiet runway anxiety — *get the actual number from [[../finance/cash-flow-king/index|cash-flow-king]]*).
- Path: tap **Gilgamesh for ~$150–300k** — no friction, no selling required (they trust us). Not "increase burn / hire 3 devs."
- That cushion makes two near-term hires lighter: **1 dev + 1 PM (Caracas office)** — funded from a bet-on-ourselves / reinvest-from-the-business posture.
- Would only raise a *larger* amount to invest if we can confidently justify it **accelerates the timeline** — e.g. AI/payments revenue ($10–20k/mo contracts) hitting in ~2 months instead of 6–8. Not there yet.

---

## Open / load-bearing unknowns

- [ ] **Pressure-relief number** (#1 current-customer migration; Arturos is the test).
- [ ] **The actual roadmap sequence** — said "we're close" ~4× Monday but not landed. *This doc is the attempt to land it.*
- [ ] **Negocios revenue model** — bank fees + WTP. Parked behind dogfooding.
- [ ] **Dogfood-vs-sell gating** (the Dan/Luis tension above).
- [ ] **Sales-team rewrite** of the pitch.

---

## Add-on (2026-06-01) — Connection options, aggregation-first, and the Veconinter field-test

Field input from the Veconinter intro call (Luis pitched most of it; *not captured by Fireflies* — reconstructed from Luis + the internal debrief with Esteban / Roberto). First live run of the new pitch. Sharpens workstream #1 above — appended here rather than edited in.

### How we now talk about connections — two buckets

**Bucket 1 — Connection options: API vs Direct.** Pitch language validated live: *"Two options — (1) bank APIs: more reliable/stable, higher integrity across the board, but limited syncs/day; (2) Direct connections: more syncs/day, but unstable, and we can't predict when a bank's portal change forces repair work on our end."* State it honestly; let the customer own the tradeoff.

- **The reframe that matters: aggregation > real-time.** For the *majority* of customers, **once-a-day works** — the value is aggregating everything in one place, not intraday freshness. So the once-daily API tier isn't a hole in the thesis; it's fine for most.
- **API freshness tier (load-bearing):** high/unlimited syncs → **BNC, Banesco** (Exterior in the mix); once-daily → **Provincial/BBVA, Mercantil** — and those two are exactly the banks causing the most problems today.
- **Direct connections are now a per-bank sunset candidate.** Open question whether we keep *selling* Direct at all, especially for problematic banks. Lean: stop offering Direct where an API or file alternative exists (problematic banks first); keep it only where it's the sole option. Sequencing (stop-selling-to-new vs. migrate-existing) is Luis's call.
- **Cheap gut-check before committing the company to "once-daily is fine for most":** it's measurable against the base — what % of customers have *ever* needed intraday? If it's truly the majority, the whole migration de-risks. (Ties to the "make it a number" discipline.)
- Esteban's sales rule: don't offer the real-time-bank move as a *recommendation* (gets ignored — "she told me to do this, I won't") — state it as a *requirement* ("if you want it real-time, you have to open BNC/Banesco"). Bonus: every customer pushed onto BNC/Banesco becomes a payments customer.

**Bucket 2 — If aggregation is the value, satisfy more banks without scraping.** Two ideas:
- **MT940 for non-VE banks** — for future `/tesote-plan` work, or for customers willing to talk to their bank about enabling it. The coverage-completer for international/long-tail banks (no scraper, no API).
- **Seamless statement upload + Tesote AI does the rest** — the bigger lever. Make it *extremely* easy for a company to upload statements; AI parses + aggregates everything in one place. Lowers the coverage bar for *any* bank, VE or not, with zero scraping burden. (UX is make-or-break — "extremely seamless" carries the value; that's a product-design / `/tesote-plan` item, not strategy.)

### Veconinter — first field-test and first ICP filter

Customs/freight agent. Time-sensitive aduana payments — *"if we don't confirm a payment in 15 min → a day's vessel delay, a cost we eat."* Needs to **sync every hour** and push into their system. Top banks: BBVA, Mercantil, BNC → they could put **receivables on BNC** (unlimited syncs). ~**40% of ops overseas** in long-tail banks (Papua New Guinea, etc.) → the trigger for the MT940 / upload idea above.

- They're the first customer the new pitch *filters* — a real-time-everything need on once-daily-API banks. That's the pitch working, not failing: it clarifies who the ICP is.
- **Payment portal = an unproven but real hypothesis for their core problem.** We have *not* proven the portal works for them yet — but it's the textbook use case: if their clients pay *through* Tesote, real-time confirmation is solved by construction ("si quieres data en tiempo real, transacciona a través de Tesote"). Roberto's framing: supplier pays via portal → instant confirmation → client releases the aduana payment. **Hypothesis to validate, not a promise to make.**

---

## Related

- [[product-strategy-execution-plan]] — the Apr 19 plan this resequences (payments-first → reallocation-first)
- [[winning-vs-horizontal-ai]] — why standalone AI-for-Odoo is a wedge, not a moat
- [[tesote-ai-positioning]] — positioning work for the AI SKU
- [[caracas-trip-2026-04-26]] — "come back with a brand-new set of products"; this trip later in June lands a lot of this
