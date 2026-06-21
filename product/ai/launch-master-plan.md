---
title: Tesote AI — Launch Master Plan (the all-functions operation)
tags: [strategy, ai, launch, sales, marketing, legal, cx, pricing, 10x]
updated: 2026-06-11
status: draft
target_launch: 2026-06-22
owner: Luis (orchestrator); function leads own workstreams
audience: function leads (Dan, Majo, Vero, Estefy, Esteban) + their teams
---

# Tesote AI — Launch Master Plan

> **What this doc is.** The orchestration layer **above** the product docs. The product family ([[pitch-today-v2]], [[launch-contract-2026-06-05]], [[launch-readiness-plain-2026-06-05]], [[bug-register]], [[launch-day-one-prd-v2]], [[pricing]]) answers *"what is the product and is it ready."* This doc answers *"how do all five functions land it on the same day so we can upsell 100% of customers in week 1."*
>
> **How to use it.** Find your function in the **JTBD board** below — that's your one job and your definition of done. Then read your workstream section (§7–§10) for the detail. The shared mechanics (§1–§6) are the context everyone needs.
>
> **Target launch: ~June 22** (penúltima semana de junio). Source: Luis ↔ Esteban call, 2026-06-08. The frame is *todo el campo controlado* — every part of the field accounted for before kickoff.

---

## Who owns what — the JTBD board

Every function has **one job** for this launch. If you only read one thing, read your row.

| Function | Lead(s) | The one job (JTBD) | Done when (by Jun 22) |
|---|---|---|---|
| **Sales** | Esteban (+ Nicolás) | Turn the usage signal into signed upsells, fast and with zero friction. | Pitch + demo + objection bank locked per bucket; Bucket A has a zero-ceremony price→contract→sign→live path; Bucket C demos still running. (§7) |
| **Marketing** | Vero (+ Maria Alesia) | Manufacture demand + the VIP "internal launch" narrative, and make the new website the destination. | Intrigue→launch→arsenal assets live; per-bucket comms calendar owned; landing page merged + live. (§8) |
| **CX** | Estefy | Turn a "yes" into a live paid seat in minutes, absorb the day-one surge, surface the champions. | Instant-onboard path exists; surge/triage plan ready; champion list flows from the meter (§6). (§9) |
| **Product / Eng** | Dan (CTO) + Majo | Ship AI **inside** the redesigned app, blockers closed, meter live. | Redesign (Saldos / Movimientos / Dashboard) production-ready; 6 AI blockers closed; instrumentation engine live. (§10) |
| **Legal** | Vero drafts · PTCK approves | A click-to-sign subscription + T&C/privacy that never pulls in the customer's lawyers. | PTCK green-lights the template + T&C + privacy policy before Jun 22. (§5) |
| **Data / Instrumentation** | Dan (CTO) | The usage meter — per-tenant + per-user telemetry + limit-hit trigger — **live on day one.** This is the engine the whole plan rests on. | Telemetry live; limit-hit event fires; watch-dashboard ready for the day-1 standup. (§6) |
| **Orchestration** | Luis | Lock the numbers (price / tiers / trial), lock the Dashboard design, lock the trigger mechanic; run the kickoff. | The four open decisions in §12 are closed this week. |

**Per-person jobs** where a function has more than one owner:

- **Sales** — *Esteban* owns the overall motion + Bucket C (active pipeline) demos. *Nicolás* runs the Bucket A/B speed-runs (instant-yes → contract → live).
- **Marketing** — *Vero* owns the campaign, the website-as-destination, and the comms calendar. *Maria Alesia* (starts Jun 22; half-in the week before) ramps onto asset production + the launch-day sends.
- **Product / Eng** — *Dan* owns eng delivery, the instrumentation engine, and the landing-page security sign-off. *Majo* owns the in-app product surfaces (redesign) and shepherds the 6 blockers to closed.

---

## 1. The success definition (reverse-engineered)

**North star:** the day we launch, usage spikes, and within **week 1 we *could* upsell 100% of current customers** — not because every one says yes, but because **nothing on our side is improvising.** Pricing, pitch, contract, materials, and the usage signal are all pre-built and sitting loaded.

That goal is deliberately irrational. The point isn't to actually convert 100% — it's that **if we wanted to, we could**, because every piece of the machine exists before day one. We measure *readiness* against that bar.

**The real number we're booking: $21k MRR in upsells** (≈ 14 logos at entry, fewer at higher tiers). The 100% bar drives readiness; $21k is the launch's actual revenue target. Full scoreboard in §15.

**Decomposed — for the goal to be literally true, all of these must be true at launch:**

1. Every customer's workspace has AI **turned on** with their permissions, behind a trial limit.
2. We can **see, per workspace and per user, who is using it and who hit the limit** — in near-real-time. *(The engine. §6.)*
3. There is **one simple price** we can quote in the same breath as the demo. *(§4 — open decision.)*
4. There is a **5-bullet, sign-by-email subscription contract** — no "my legal team will review" loop. *(§5.)*
5. Sales has a **pitch + demo + objection bank** ready for each customer bucket. *(§3, §7.)*
6. Marketing has **intrigue → launch → arsenal** materials live, and the **new website is the destination.** *(§8.)*
7. CX can **onboard a yes in minutes**, not a re-implementation. *(§9.)*
8. The **6 product blockers are closed** and the launch ships **bundled with the redesign** (Saldos / Movimientos / new Dashboard + landing page) so it lands as one big statement. **Bundling is locked (decided 2026-06-08) — the redesign launches with the AI, full stop.** *(§10.)*

If any of these is missing on June 22, the "100% upsell-ready" claim is false — that's the readiness scoreboard.

---

## 2. The launch model — give → watch → bucket → upsell

The mechanic, as a funnel:

```
GIVE      → AI on for all workspaces/users, permissions intact, trial limit (e.g. 2–3 prompts/workspace)
WATCH     → per-tenant + per-user usage telemetry from minute one (§6 — the linchpin)
BUCKET    → sort customers/users by behavior (§3)
UPSELL    → "you already hit the limit and look at the work you did → here's the price → here's the
             contract → sign by email → you're live next week"  (fast, no friction)
```

The whole thing only works if **WATCH is live on day one.** Without usage data there's no trigger, no bucketing, no evidence to put in front of the CFO. **Build the meter first.** (§6.)

Framing to customers: **"this is an internal launch, not public yet."** Makes them feel chosen/VIP, and lets us point them at the new site ("look at everything coming") — they see the arsenal (AI first, then pagos/cobros) and write back "están dementes, los felicito."

---

## 3. The four buckets + the play for each

| Bucket | Who | The play | Owner |
|---|---|---|---|
| **A — Instant yes** | Hits the limit fast, high engagement, "cuánto cuesta? dale" | Same-day: price → contract → sign by email → live next week. Zero ceremony. | Nicolás (Esteban backs) |
| **B — Warm, needs selling** | Moderate usage, interested but wants the pitch | Demo + ROI framing ("look at what your team already did") + the simple price. A bit more touch. | Esteban / Nicolás |
| **C — Active pipeline (non-customers)** | Dorado, Corpalmar, El Tunal, Capca, Coca-Cola, Santa Teresa, etc. | Keep running demos in parallel; AI becomes the lead wedge in the existing motion. | Esteban (continues) |
| **D — Closed-lost** | Was 50/50 at proposal/negotiation; incl. Odoo-already customers | Reactivation comms — "new product, internal launch, come see." Separate sequence; needs a message. | Esteban + Vero |

Bucketing is **driven by the usage data**, not by gut — that's why §6 gates §3. Per-user matters too: the heaviest individual user inside a workspace is often the internal champion who sells the CFO for us.

---

## 4. Pricing & packaging — **DECISION #1 (blocks the whole upsell motion)**

The plan needs **one number you can say out loud during a demo** — and a clear, defensible reason it goes *up* from there. ~$1.5k is the **entry point, not the ceiling.** Decided 2026-06-08: price scales on data + users, and the escalation is baked into the equation, not bolted on later.

**The pricing equation (variables, decided):**

| Variable | Why it scales price | Notes |
|---|---|---|
| **Data volume per workspace** | More tx / accounts / history = more context the AI loads, more tokens burned, more value delivered. The dominant cost *and* value driver. | Rhyme with whatever tx-volume tiering Tesote core already uses ([[pricing]] open Q) — don't make customers learn a new mental model. |
| **# of active users with AI on** | Per-seat is the natural "this goes higher" lever and the cleanest escalation story ("you added 4 people to it → here's the new tier"). | Need a hard definition of **"active user"** (provisioned vs actually-used) — see §6 measurement scope. |
| **(internal) token burn** | The 80%-margin guardrail behind both of the above. Stays invisible to the customer; informs which tier the data/user combo lands in. | Communicated as **"AI tasks/mo"** not tokens. |

**Structure:** **~$1.5k entry** (light data, small user count) → climbs by **data tier × seats**. The $1.5k must be a number Bucket A says yes to without thinking; the climb is what we earn from the heavy/wide accounts. Overage = **soft / sales conversation** for now ([[pricing]]) — *hitting the limit is the upsell trigger, not an auto-bill.*

**Trial scope (decided 2026-06-08):** **both per workspace AND per user — across all workspaces and all users.** Everyone gets a taste, every workspace gets a taste; the limit bites at both levels (a workspace can exhaust its allowance *and* an individual user can). Lock the exact free-prompt/task count + duration with Esteban.

→ **Luis + Esteban lock the entry number + the tier multipliers + the trial counts this week.** Everything downstream (contract, pitch, marketing CTA, the meter in §6) hardcodes these. Full tier table gets re-validated after 30–60d of the real usage data this launch finally generates at scale.

---

## 5. Legal / Contract — the frictionless subscription agreement

**JTBD (Vero drafts · PTCK approves):** a contract that signs like an online subscription — **"spray-forward,"** never an invitation to a legal review and a two-week stall.

**Owner (decided 2026-06-08): Luis + Vero draft it, PTCK approves.** Vero starts now and lays it out so PTCK's role is a **green-light pass, not a redlining exercise** — the whole point is that *the customer's* lawyers never get pulled in either. PTCK approves the template once; after that it's click-to-sign, every time.

**Requirements:**
- **5 bullet points**, plain terms — what you get, the price, the cadence, the term, cancellation.
- **Click-to-sign / sign-by-email**, authorized signer named (we're already on their email). For existing customers this is a **quick amendment** to their current Tesote subscription — *not* a fresh MSA. No wet signature, no redlines round-trip.
- Reads like Stripe/Notion checkout terms.

**Also in scope (decided 2026-06-08) — and PTCK should own these:**
- [ ] **Terms & Conditions** for the AI products.
- [ ] **Privacy Policy** — must cover the AI specifically: that it reads their bank/financial data, who the model providers are (OpenRouter/Anthropic etc.), data retention, confidentiality, no-training-on-their-data commitment. This is a *finance* AI touching sensitive books — the privacy/data story is part of the trust pitch, not just compliance boilerplate.

→ **Done when:** Vero kicks off the contract template + T&C/privacy with PTCK this week, and PTCK green-lights all three before Jun 22.

---

## 6. Data / Instrumentation — **the upsell engine (linchpin, easy to under-build)**

**JTBD (Dan):** stand up per-tenant + per-user usage telemetry — with a limit-hit trigger — **live on day one.** This is the one workstream that silently sinks the plan if it's not ready. The entire "watch → bucket → upsell" thesis is load-bearing on it.

Already on two lists:
- [[pricing]] flags **per-tenant token accounting** as a *hard prerequisite* (for caps/unit-economics).
- [[../../strategy/current-initiatives-2026-06]] CX#1 flags **user + workspace usage tracking + PostHog**.

This launch **promotes it from "nice infra" to "the engine."** Posture (decided 2026-06-08): **assume we measure everything.** The work isn't *whether* to measure — it's **scoping what and how** so the data actually drives the upsell motion and the pricing equation (§4).

**Measurement scope — what to capture (day-one):**

| Layer | Metrics | Drives |
|---|---|---|
| **Workspace** | active? first-use date, # prompts/tasks, distinct users active, tasks by type (query / report / rule / action), data volume (tx, accounts, history depth), **hit the limit? when?** | bucketing (§3) + data tier (§4) |
| **User** | who, role, # prompts/tasks, last-active, **hit the limit?**, is this the workspace's heaviest user (champion signal) | per-seat pricing (§4) + champion-spotting (§9) |
| **Engagement quality** | repeat use (came back day 2/3/7), depth (did they go past one prompt), which use-cases stick | activation health + what's actually valuable |
| **Cost / unit-economics** | tokens by workspace/user/task-type, model used (Haiku vs Sonnet routing) | 80% margin guardrail; what the free trial actually costs us at full rollout |

**The trigger mechanics — the glue between WATCH and UPSELL (don't leave this implicit):**
When a workspace or user **hits the limit**, something has to *happen*, automatically — that's the moment the upsell starts. Decide the mechanic: (a) auto-notify the account exec ("Workspace X hit the cap, 3 users active"), and/or (b) in-app "you've hit your trial — talk to your exec" nudge, and/or (c) it surfaces on the watch-dashboard for the day-1 standup. Recommend **all three**. The limit-hit event is the single most important thing the engine emits.

**Customer-facing usage meter** — % of limit used, visible to them so the cap is earned not surprising ([[pricing]] op-req #2). Day-one if it fits; fast-follow otherwise.

→ **Done when:** telemetry is live, the limit-hit event fires into at least one of the three channels, and the watch-dashboard is ready for the day-1 standup.

→ **This is `/tesote-plan` material in treasury** (per CLAUDE.md eng bridge). Touches data model + services + multi-tenant accounting + the limit-hit event. **Flag to Dan now** — if it's not scoped this week it won't be live June 22 and the launch loses its engine. Pulls in `database-design` + `product-management`. Note overlap with the existing CX#1 / PostHog initiative ([[../../strategy/current-initiatives-2026-06]]) — same instrumentation, fold them together rather than build twice.

---

## 7. Sales workstream — owner: Esteban (+ Nicolás)

**JTBD:** turn the usage signal into signed upsells — fast, per bucket, zero friction on the yes.
**Done when (Jun 22):** pitch + demo + objection bank locked per bucket; Bucket A has a zero-ceremony close path; Bucket C demos still running.

- [ ] **Launch pitch** per bucket — built on [[pitch-today-v2]] (launch-narrow, rules-engine reframe). Sales is *already* soft-offering AI in demos; formalize it.
- [ ] **Demo flow** — the 15-min demo from [[pitch-today-v2]], swap one chat moment for a delegation/Automations "while you slept…" moment ([[winning-vs-horizontal-ai]] pattern).
- [ ] **Pricing in hand** (§4) + the **one-line close**: "send the contract, sign, you're live next week."
- [ ] **Objection bank** — incl. the **payments/cobros FOMO holding message** (§11).
- [ ] **Bucket A speed-run** — the zero-ceremony path for instant-yes customers. *(Nicolás runs this.)*
- [ ] Keep Bucket C demos running in parallel (Coca-Cola, Santa Teresa, Capca prioritized — close before quarter-end). *(Esteban.)*

---

## 8. Marketing workstream — owner: Vero (+ Maria Alesia, new marketing hire, starts Jun 22; half-in next week)

**JTBD:** manufacture demand and the VIP "internal launch" narrative, and make the new website the destination people land on.
**Done when (Jun 22):** intrigue→launch→arsenal assets live; the per-bucket comms calendar is owned and scheduled; the landing page is merged and live.

Three beats:
- [ ] **Intrigue (pre-launch):** "algo va a pasar el 22" teaser to existing + new customers. Build the curiosity.
- [ ] **Launch day:** "new feature — try it free here, 2–3 prompts, ask your account exec." One-tap-easy.
- [ ] **Arsenal / destination:** the **new website** ([[../../marketing/landing-page-argument]], v41 already ported to Rails on `redesign-homepage-v41`) is where they land and see everything coming. The redesigned landing was step 1 of this launch — by design.
- [ ] **Tesote AI video** (already in flight per current-initiatives) — internal-launch hero asset.
- [ ] **"Internal launch / not public yet"** messaging woven through — the VIP framing.
- [ ] **Comms calendar** — own the day-by-day send schedule across buckets A–D (see §15.6), not just the assets.

> The landing page ships to **marketing.tesote.com** on merge; Dan still owes the security-claims sign-off and the PR needs opening (see [[../../daily/2026-06-08]]). That's now on the launch critical path — surface it.

---

## 9. CX / Onboarding workstream — owner: Estefy

**JTBD:** turn a "yes" into a live paid seat in minutes, absorb the day-one surge, and surface the champions for sales.
**Done when (Jun 22):** the instant-onboard path exists; a surge/triage plan is ready; the champion list flows out of the §6 meter.

- [ ] **Onboard-a-yes in minutes** — when Bucket A signs, turning the trial into a paid seat must be near-instant, not a re-implementation.
- [ ] **Handle the usage surge** — support load when hundreds of users start poking the AI day one.
- [ ] **Champion-spotting** — feed off §6: the heaviest user per workspace is the internal seller; CX should know who they are and hand them to sales.
- [ ] Closed-lost (Bucket D) often needs a real re-implementation (e.g. desconectados like la Santé) — scope that separately from the fast path.

---

## 10. Product / Eng workstream — owner: Dan (CTO) + Majo

**JTBD:** ship AI *inside* the redesigned app, with the blockers closed and the meter live — so the launch lands as "one big statement," not a feature bolted onto the old app.
**Done when (Jun 22):** the redesign (Saldos / Movimientos / Dashboard) is production-ready, the 6 AI blockers are closed, and the instrumentation engine (§6) is live.

Three critical requirements, all gating Jun 22: **(A) the new web app redesign**, **(B) the 6 AI blockers closed**, **(C) the instrumentation engine.**

*Split:* **Dan** owns eng delivery + instrumentation (§6) + the landing-page security sign-off. **Majo** owns the in-app product surfaces below and shepherds the 6 blockers to closed.

### 10A. New web app design — **CRITICAL REQUIREMENT (decided 2026-06-08)**

Finishing and launching the redesigned in-product surfaces is non-negotiable for Jun 22 — it's the visual proof that "estos panas transformaron esta vaina." This is the **web app**, distinct from the marketing landing page (§8, already ported).

- [ ] **Saldos** (sync at *connection* level — the long-standing design fix) — *status: done per [[../../daily/2026-06-08]] (v4).*
- [ ] **Movimientos** — *status: v7, largely there.*
- [ ] **New Dashboard / Inicio** — **the long pole.** Still being iterated (v2 base, locking the Posición box first, "lots TBD" per [[../../daily/2026-06-08]]). AI must be **front-and-center** on this home surface. → this is the piece most at risk of slipping the date; it needs a hard "design-locked by" milestone *this week* so eng has runway.
- [ ] **One coherent design family** across app + landing (shared vocab already pulled from v41).

→ **Dashboard is the critical-path item on the redesign.** Lock the Posición box → rebuild v2 around it → `dashboard-prd.md` → PRO ticket → `/tesote-plan` with `redesign-2026-design-system`. If it can't be production-ready by Jun 22, that's the one thing that forces a hard conversation (we said bundling is locked — so the move is to *protect the Dashboard timeline*, not unbundle).

### 10B. The 6 AI blockers
- [ ] **Close the 6 blockers** in [[launch-readiness-plain-2026-06-05]] (P1 outage, P2 die-mid-action, W1+W2 100-tx limit, W3 silent-ungrouped, W4 silent-date-shift, W7 empty report library). → approve verdicts, file P1/P2, re-rank ENG-4016.
- [ ] **Seed the default reports** (W7) — *we* owe the 3–5 report list.

### 10C. Instrumentation
- [ ] **Instrumentation** (§6) — the engine. Bundle its `/tesote-plan` run with the Dashboard + any blocker that's really a PRD.

Wave 2 (Odoo Bs/USD class) stays out of scope — 100% of day-one users are workspace-only.

---

## 11. The payments/cobros FOMO message — small but explicit

When customers ask about payments/cobros (not ready), we need a deliberate answer that **creates FOMO and leaves them wanting more** — not "it's not ready." Frame as "next chapters of the arsenal, you're seeing it first." Owner: Vero + Esteban, one paragraph, in the objection bank.

---

## 12. Decisions still open — Luis's call this week

**Decided 2026-06-08:** pricing variables (data + seats, $1.5k = entry not ceiling, §4) · contract owner (Luis+Vero draft, PTCK approves, §5) · T&C + privacy in scope (§5) · measure-everything posture (§6) · redesign bundling **locked** · trial scope = **both per workspace and per user, all workspaces all users** (§4).

**Still open — need Luis's call this week:**
1. **The exact entry number + tier multipliers + trial counts** (§4) — lock with Esteban. The *variables* are decided; the *numbers* aren't. Blocks contract, pitch, marketing CTA, the meter.
2. **Is the instrumentation engine scoped in time?** (§6) — needs the Dan conversation *this week* or it won't be live June 22. The one thing that quietly kills the launch.
3. **The limit-hit trigger mechanic** (§6) — auto-notify exec / in-app nudge / standup dashboard. Recommend all three; confirm.
4. **Lock the new-Dashboard design** (§10A) — Luis is the designer here and it's the long pole on the redesign. Needs a design-locked milestone this week or it threatens Jun 22.

---

## 13. Timeline

| When | What |
|---|---|
| **This week (Jun 9–13)** | Cross-functional **kickoff** (§14). Lock price + trial (§4). Dan scopes instrumentation (§6) + confirms blocker close + redesign date. **Lock the new-Dashboard design** (§10A — the long pole) so eng has runway. Maria Alesia half-in. |
| **Jun 16–19** | Contract finalized. Pitch/demo/objection bank locked. Intrigue campaign goes out. Landing page merged + Dan security sign-off. Instrumentation in QA. |
| **Jun 22 (launch)** | AI on for all workspaces. Launch-day marketing. Usage meter live. Sales standing by per bucket. |
| **Week 1 post (Jun 22–28)** | Watch usage → bucket → upsell. Daily standup on who lit up / who hit the cap → fire the upsell sequence toward **$21k MRR** (≈14 logos). |
| **+30–60d** | Real usage data → lock the full pricing tier table ([[pricing]]). |

---

## 14. The kickoff meeting (this week)

Esteban asked for it (~5pm this week). Agenda:

1. **The goal, stated boldly** — "we want to be *able* to upsell 100% of customers in week 1, and we're booking **$21k in new MRR** off this launch (≈14 logos). Reverse-engineer everything from there."
2. **The model** — give → watch → bucket → upsell (§2). Everyone sees the funnel.
3. **Owners confirmed** — read the JTBD board: Sales/Esteban, Marketing/Vero, CX/Estefy, Product/Dan+Majo, Legal/contract (Vero+PTCK), Data/Dan. Each lead restates their one job + done-when.
4. **The three things that gate everything** — (a) the launch price, (b) the instrumentation engine (§6), (c) the **new web app design finished + launched** (§10A, Dashboard is the long pole). Don't leave the room without a path on all three.
5. **The June 22 date** — and what each lead owes by Jun 16 and by Jun 22.
6. **Bucket D + payments-FOMO** — assign the two comms pieces.

---

## 15. Gaps to close (added 2026-06-08)

Not in the original call, but a launch this aggressive needs them:

1. **A launch scoreboard (KPIs).** "Upsell-ready for 100%" is the readiness *bar*; the **headline target is $21k MRR in upsells** (decided 2026-06-08). It rounds clean against the entry price: **$21k ÷ $1.5k = 14 upsells** — 14 logos at entry tier, *fewer* if accounts land on higher data/seat tiers (§4). That's the number the whole launch points at. Supporting metrics the §6 engine produces: % of workspaces activated, % that hit the limit, # upsell conversations triggered, # contracts signed, day-2/7 retention. The 100% bar keeps us honest on *readiness*; **$21k is what we're actually trying to book.**
2. **Internal enablement before day one.** Sales and CX have to know the product *cold* — including its limits (the 6 blockers, what it refuses, the currency edges) so nobody overpromises into a trust-killer. A short internal training + a "what it can/can't do today" one-pager, the week before. Dogfooding ≠ enablement.
3. **Launch-day war-room / triage rotation.** Hundreds of users poking a finance AI on day one *will* surface bugs ([[bug-register]] is proof it happens). Who's on call, how fast we triage, and a **per-workspace + global AI kill-switch** if P1 (the outage bug) recurs at scale. Decide the rollback before we need it.
4. **Free-trial cost exposure.** Giving AI to *all* users and *all* workspaces — even capped — is real token spend. Back-of-envelope the worst-case burn and confirm **model routing (Haiku for routine, Sonnet for hard)** is on, or margins bleed from minute one ([[pricing]] op-req #3). The trial limit is the cost cap — size it with this in mind.
5. **"Active user" definition.** Now that seats are a pricing variable (§4), we need one hard definition (provisioned vs actually-used) before the meter counts them — or the pricing conversation gets fuzzy.
6. **Comms calendar / sequencing.** Buckets A–D get *different* messages at *different* times (intrigue → launch → bucket-specific upsell; closed-lost is its own track). One owner (Vero) holds the actual day-by-day send calendar, not just the assets.

Items 2, 3, 5 are cheap and easy to forget. Item 1 (targets) and 4 (cost) want a number from Luis/Dan.

---

## Terminal move

This plan = (a) keep drafting in brain, *and* it spawns (c) `/tesote-plan` in treasury for the **instrumentation engine (§6)** — the single most launch-critical eng item that isn't already in flight. Next move after the kickoff: file the PRO ticket for per-tenant/per-user AI usage telemetry + customer-facing meter, then run `/tesote-plan` with `database-design` + `product-management`.
