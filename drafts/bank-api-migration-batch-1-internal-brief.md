---
title: Bank API Migration — Batch 1 (internal brief draft)
tags: [product, payments, connect, bank-apis, draft]
updated: 2026-06-03
status: draft
---

# Bank API Migration — Batch 1 (internal brief)

Draft message to send internally to the team. Frames the bank-API migration project (moving customers off credential-scraping onto official bank APIs for BBVA / Banesco / Mercantil / Bancaribe). Companion artifact: [[../data/bank-api-batch-1-client-rollup.csv]] (the spreadsheet to attach).

Methodology + supporting data: `data/bank-api-migration-batch-1-prioritization.sql`, `data/bank-api-batch-1-full.csv`, `data/bank-api-batch-1-client-rollup.csv`.

---

**Project: Bank API Migration — Batch 1 (first-draft framing, want your input)**

Team — kicking off the framing for moving customers off credential-scraping and onto official bank APIs, starting with **BBVA, Banesco, Mercantil, and Bancaribe, in that order**. This is a rough first draft — the goal here is to align on *how we're thinking about it* and the data behind it, then break it into smaller pieces (process design, automate-vs-manual, owners, KPIs) in follow-ups.

**Why this matters.** Scraping is our most fragile, most expensive way to connect to a bank — proxies, breakage, maintenance load. Moving the right accounts to bank APIs is both a reliability/cost win for us and foundational for where we're taking the product.

**How I scoped it.** I pulled every workspace with an active account at the four target banks, broken down by: entities per bank, connected (scraper) accounts per entity per bank, and transactions per entity per bank. The grain matters — **bank API access is granted per legal entity, per bank**, so the entity-per-bank count *is* the number of API access requests we'd have to file. That's our effort/cost driver. Two things I want this to drive:

1. **Cost-to-deliver → pricing.** Project the man-hours, decide how we price this, and decide which workspaces get it for free.
2. **System impact.** Quantify how much scraper load we relieve by pulling this off.

**The headline: pressure is extremely concentrated.** A small set of customers carries the vast majority of the load. So this isn't a 100+ customer slog — it's a focused first batch plus a few special cases.

**How I'd bucket it:**

**1. Priority batch — 65 workspaces, ~$57.5k MRR.** The core of the migration. ~495 entity-level API requests, ~1,170 connected accounts, ~450k transactions/month. This is where speed-to-relief is highest.

**2. Flagship campaigns — Grupo Abreu + Farmacias San Ignacio (~$4.2k MRR).** Huge relief and high value, but request-heavy (FSI alone is ~130 entity applications and ~65% of *all* our BBVA load). Too big to fold into the main batch — I'd run each as its own dedicated campaign with the bank.

**3. Broken-sync — Grupo Canaima (177 entities, $750 MRR).** Their syncs are currently failing, so we can't pull their transactions at all — the data understates them massively; if it worked it'd look very different. An API could be the actual fix here, but it's 177 entity applications. Needs its own assessment: is the effort worth it, and do we charge for it?

**4. Resource drain / commercial review — Cines Unidos & Grupo UP.** These two are consuming significant sync resources with low or uncertain return, and they're commercial questions, not migration questions:
   - **Cines Unidos** — ~56k transactions/month across ~22 connected accounts for **$225 MRR**. We're losing money serving them. Decision needed: reprice or offboard?
   - **Grupo UP** — scheduled syncs still running (~39k tx/mo), but we don't actually know if they're still using Tesote. **Are they continuing with us?** We need to confirm they're active *before* we invest any migration effort in them.

**5. Deferred — ~$30k MRR.** Churning, minimal transactions through these banks, or low pressure to move. Deferred, not abandoned — we revisit.

**The prize.** Across the priority batch + flagships, we're talking **~690k transactions/month flowing across ~1,600 connected bank accounts**. That's the scale of scraper load this initiative takes off the system — the impact on reliability and cost should be significant.

**A pricing principle I want to propose:** base free-vs-paid on *relief-to-us vs cost-to-serve*, not just MRR. Where moving a customer relieves a lot of scraper load, the migration pays for itself in ops savings — those should be subsidized/free. Where it's high-effort and low-relief (Canaima-type), it's a cost with no payback — we charge for it or decline.

**This is the very first draft.** Next we break it into smaller pieces: how the process actually works end-to-end, what we automate vs. keep manual, who leads what, and the KPIs we want to watch. Please take a look at the attached spreadsheet to review the workspaces in question and give me your feedback on how you're thinking about prioritizing these.
