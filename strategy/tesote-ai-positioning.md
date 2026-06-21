---
title: Tesote AI — Dunford-style positioning
tags: [strategy, tesote-ai, positioning, pitch, 10x]
updated: 2026-05-20
status: draft
---

# Tesote AI — Dunford-style positioning

> **Goal.** Build the pitch that positions Tesote AI as the most transformative tool any VE finance team has ever interacted with — using April Dunford's *Obviously Awesome* method.
>
> **Not a replacement** for [[../product/ai/pitch-agents-plus-ai]] (2026-05-13). That doc already nails the *narrative* (Agents + AI on top of Odoo, two-layer frame, function-by-function wedges). This doc is the *upstream* work Dunford insists on before any deck: **insight → category → old-way/new-way → 5-component grid → pitch sequence**. Once locked, the existing pitch gets retrofit to it.

---

## Why Dunford (not "build a deck")

Positioning > messaging > pitch > deck. Most founders skip the first two and end up with beautiful slides that say nothing distinctive. Dunford's discipline: choose your category deliberately, mine real customer insight, then everything downstream snaps to it.

**The single highest-leverage decision is the category we put Tesote AI in.** If we let people slot it into "AI for finance" or "ERP automation," we lose to Ramp / Brex / Vic.ai on their terms. We need a category where global tools are structurally absent — and Venezuela is exactly that environment.

---

## Phase 0 — Mine the last 3 days (the insight)

You've been *living it* since 2026-05-18 (Dan launched Tesote AI in the internal workspace). The Dunford pitch lives or dies on a hard-earned point of view. Before writing anything else, surface the **impossible-before-now** moments.

### Prompt — fill in raw, no editing (15 min)

For each, jot the moment when you went *"wait, this is different."* Speak in scenes, not abstractions.

**1. Crecer workspace audit (2026-05-20)** — pulled a full health read in minutes via `tesote-internal-ops` MCP. Surfaced Scotia dark for 22 days, no retries scheduled, Banesco creds broken, Promerica never scheduled, 40k txns sitting raw with zero taxonomy. *Half the customer's banking surface was silently broken and nobody knew.* What's the moment? What would have happened without Tesote AI? What did it take to discover this *before*?
> *[Luis: ...]*

**2. Marcas Propias MTD audit (2026-05-20)** — 20 minutes before the Futura meeting. Caught Mercantil at 1/10 days sync, Banesco scheduler 3 strikes from auto-disable, 0 counterparties on a Tier 3 Premium reference account. *You walked into the call knowing exactly what to defend.* What's the moment?
> *[Luis: ...]*

**3. Saldos PRD → PR in <24h (2026-05-18 → 19)** — `/tesote-plan` validated end-to-end on the first run. Brain spec → Linear ticket → treasury plan → committed PR by Dan-can-merge stage. Was this just velocity, or did something structurally change about *how product gets shipped now*? Could a competitor — even with the same engineers — close that loop?
> *[Luis: ...]*

**4. Tesote AI live in your own workspace (2026-05-18)** — Dan shipped the chatbot on Odoo, running against real Tesote financials. What changed in your day-to-day? What stopped being painful? What do you now do that you literally couldn't do a week ago?
> *[Luis: ...]*

**5. The 5th moment** — any moment from these 3 days that surprised you, that you didn't expect to be possible. Pick the one that's stuck in your head.
> *[Luis: ...]*

### Synthesis — the insight statement (10 min, after the 5 moments)

Read the 5 moments back. The **pattern across them** is the insight.

Candidate (placeholder — we rewrite together once the 5 moments are in):

> *AI agents have just crossed the threshold where they can operate inside the chaos of VE banking — multi-bank rails, multi-currency, sanctions-aware, Odoo as system of record. Until now, VE finance teams have done the work of a 10-person tech-enabled team manually, with humans + Excel + WhatsApp + 8 portals. Tesote AI is the first finance OS instrumented to that reality — and it doesn't summarize, it acts.*

Final insight statement (Luis to draft):
> *[Luis: ...]*

---

## Phase 1 — Lock the category

The category is the **frame of reference**. Everything else in Dunford's framework snaps to this choice.

| Candidate | What it implies | Who we compete with under this frame | Risk |
|---|---|---|---|
| "The finance team's autopilot for Venezuela" | Bold, localized, agentic | Nobody — category we own | Feels small if we expand to LATAM |
| "AI-native finance operations for the markets global software forgot" | Big, vision-led | Future competitors (none today) | Vague, harder to demo |
| "The first finance OS built for Venezuelan operating reality" | Operator-flavored | Excel + the 5-person team | "OS" is overused |
| "The system of action for LATAM finance" | Ties to the Odoo split philosophy | Conceptually positions us above ERPs | Inside-baseball language |
| *[your candidate]* | | | |

**Decision deferred** until insight is locked (Phase 0). The insight chooses the category, not the other way around.

When ready, Luis picks:
> *[category: ...]*

---

## Phase 2 — Old-way / new-way diptych

The visual core of every Dunford pitch. Draft below (to be refined after insight + category lock):

| Dimension | Old way (today, for most VE finance teams) | New way (Tesote AI) |
|---|---|---|
| **People required** | 5–10 humans | 2 humans + agents |
| **Tools** | Excel + WhatsApp + 8 bank portals + email | One workspace, one prompt |
| **Sync cadence** | "When someone remembers to log in" | Continuous, instrumented, alerting |
| **Cross-bank reality** | Each bank a silo, manual reconciliation | Unified across all rails |
| **Visibility** | Owner finds out at month-close | Owner sees it the moment it breaks |
| **Speed of action** | Days to weeks | Minutes |
| **Reconciliation** | Monthly nightmare, weeks of pain | Continuous, agentic |
| **AP** | Inbox → re-type into ERP | Inbox → vendor bill automatically |
| **AR / Cobros** | One-by-one drafting, manual follow-ups | "Cobra esta semana" → 23 personalized WhatsApps |
| **Demo proof to a new prospect** | "We promise it works" | "We run Tesote's own books on it" |
| **Build velocity** | Months of eng work per surface | Spec → PR in 24 hours (`/tesote-plan` loop) |

The last row is **load-bearing**. It's the only one that proves *this isn't aspirational* — Tesote ships its own product faster than competitors can spec theirs. That's a separate moat we don't talk about enough.

---

## Phase 3 — The 5-component grid (Dunford's *Obviously Awesome*)

To fill out only after Phase 0–2 are locked. Drafted below as a starting point.

### 1. Competitive alternatives
*What would they do if Tesote AI didn't exist?*

- 5–10 humans + Excel + WhatsApp + 8 bank portals + email
- Per-bank consultants stitching reports together
- Pirated SAP / handmade Power BI dashboards
- Outsourced accounting firms running parallel ledgers

**Not** other software. That's the wedge. We're not displacing Ramp — Ramp doesn't operate here. We're displacing **a payroll line**.

### 2. Unique attributes
*What only Tesote has.*

- Instrumented to the actual VE banking stack (Banesco, BNC, Mercantil, Exterior, Bicentenario, BBVA, BdV, …)
- Multi-currency / multi-jurisdiction-aware ([[../product/connect]] spans VE + Panamá + RD + EEUU + Caribe)
- AI that **acts inside Odoo as system of record** — not a summarizer bolted on
- Sanctions / cash-control conscious by default
- Dogfood-first: Tesote runs its own books on it (Mariel is design partner, Luis audits clients with it)
- `/tesote-plan` → 24h spec-to-PR build velocity (compounding moat)

### 3. Value (the "so what")
*What those attributes enable.*

- Team of 5 → team of 2 (operator economics)
- Days → minutes (decision economics)
- Monthly close → continuous close (control economics)
- Half-broken bank rails surfaced *before* the customer notices (CX economics — see Crecer 2026-05-20)
- Pre-meeting health audits in 20 minutes (sales economics — see MP / Futura 2026-05-20)

### 4. Best-fit customer
*Who cares the most.*

- VE finance teams operating across **4+ banks**, multi-currency, monthly-close pain
- Mid-market: too big for Excel, too small / too local for global ERPs
- Already on (or open to) Odoo as SoR
- Profile: Fospuca, Polar, Crecer, Marcas Propias, Futura prospects

### 5. Market category
*See Phase 1.*

---

## Phase 4 — The pitch (V0 draft, 2026-05-20) — *superseded by V0.1 below; preserved for diff*

> **Status:** V0.1 is the active draft. V0 preserved here per [[../feedback_versioning_progression]] so you can see the reframe arc — V0 led with "agents stopped being demos," V0.1 leads with the **two-layer Automations + AI frame** and the 80/20 work-vs-time trap.

Drafting directly from the last 3 days of dogfood evidence + memory + the [[../product/ai/pitch-agents-plus-ai]] two-layer frame. Reverse-engineering the insight, category, and old/new from real moments rather than waiting for Phase 0 input. Read fast, push back hard — anything that doesn't sound like you, kill.

**Audience:** VE CFO / finance head / founder-CEO of a mid-market operator (Crecer profile, Marcas Propias profile, Futura profile). Delivered in ~5 minutes, in person or on Zoom. English working draft; Spanish version after lock-in (per [[../feedback_client_email_spanish_voice]] tone).

**Working category bet:** *"The first AI co-pilot built for Venezuelan finance teams."* Localized, ownable, demo-able. Doesn't shrink us — the same chaos exists across LATAM at lower intensity, so we expand without rewriting.

---

### Slide 1 — The shift (the insight)

> Something changed in the last 12 months that hasn't shown up yet in any finance team in Venezuela. **AI agents stopped being demos. They became operators.** They read a bank statement, post a journal entry, send a payment, reconcile a transaction, draft a customer reminder — at production quality, in seconds. Globally, this is rewriting what a finance team looks like.
>
> For Venezuelan finance teams — the most operationally over-burdened finance teams on earth — it doesn't just rewrite the team. **It rewrites the company.**

### Slide 2 — The old way (paint their world back to them)

> You live this every day:
>
> - **5–8 people** in your finance function
> - **Two of them** spend their day in WhatsApp and 8 bank portals — Banesco, BNC, Mercantil, Banco Exterior, BBVA, BdV, Bicentenario — copying balances into Excel
> - **One person** chases customers for payment, invoice by invoice
> - **One person** processes AP — printing PDFs from email, re-typing them into your ERP
> - **Reconciliation** happens once a month, painfully, by hand
> - **You close the month a week after the month is over**
> - You report numbers to your CEO that were true two weeks ago
> - Half the time, a bank rail has been silently broken for 22 days and nobody knows
>
> Globally, almost none of this is still true. In Venezuela, all of it still is — because **no one ever built the software for you**.

### Slide 3 — What the new bar looks like (raise the requirements)

> Until last year, the gap between a Venezuelan finance team and a US mid-market finance team was the absence of software. Today, the gap is the absence of **agents**.
>
> - Software gives you a dashboard. Agents do the work.
> - Software shows you the bank balance. Agents reconcile it, flag the discrepancy, draft the journal entry, and notify the controller — before your morning coffee is cold.
> - Software is *something the team uses*. Agents are *members of the team*.
>
> Every CFO in Venezuela has one question to answer in the next 12 months: **am I going to be a team of 8 humans, or a team of 2 humans plus agents?**

### Slide 4 — The fork (two kinds of finance teams now)

> The answer divides every finance team in this country into two camps.
>
> - **The teams that adopt agentic AI on top of their banking reality** — running their operation with a fraction of the headcount, ten times the visibility, and same-day close.
> - **The teams that don't** — uncompetitive in 18 months. Slower. More expensive to run. Blind to half their own data.
>
> This is not a productivity slide. This is a survival slide.

### Slide 5 — Why Tesote (the only one delivering it)

> Tesote AI is the only product built for this reality. Not adapted. **Built for it.**
>
> **1. Instrumented to every Venezuelan bank at the rail level.** Banesco, BNC, Mercantil, Banco Exterior, BBVA, BdV, Bicentenario. Live in production. Not screen-scraping, not "we'll build it if you sign."
>
> **2. Sits on top of your Odoo as system of record.** Your CPA still posts the official ledger. Tesote is the system of action on top — agents that draft, propose, reconcile, send. (See [[../project_tesote_vs_odoo_split]] philosophy.)
>
> **3. The AI doesn't summarize. It acts.**
> - *"Cobra esta semana"* → 23 personalized WhatsApp messages to overdue customers
> - *"Concílialo todo"* → 84 bank lines matched to invoices in 30 seconds
> - *"¿Estoy lista para declarar IVA?"* → the check runs end-to-end
>
> **4. Multi-jurisdiction out of the box.** VE, Panamá, RD, USA, Caribbean. Multi-currency, sanctions-aware, regulation-aware. The day you expand, your finance stack already came with you.
>
> **5. We run our own books on it.** Every payment Tesote makes, every invoice we issue, every reconciliation we do — runs on Tesote. There is no other vendor in this market who can say this sentence honestly.

### Slide 6 — Proof (last 72 hours, real)

> Three things happened in my last three days using Tesote AI inside our own workspace:
>
> **One.** I asked it for a health audit on Crecer, a customer onboarded weeks ago. In 2 minutes, I learned their Scotia rail had been silently broken for 22 days, their Banesco credentials were dead, and 40,000 transactions were sitting uncategorized. Without Tesote AI, this would have surfaced when they churned.
>
> **Two.** Twenty minutes before a reference call to a Futura prospect, I ran a full month-to-date audit on Marcas Propias' workspace. I walked into the call knowing exactly what to defend and what to flag. The call went better because of it.
>
> **Three.** I specced a redesign of a major page on Sunday night. By Monday afternoon, the code was in a pull request, ready to ship. **Spec to production-ready PR in under 24 hours.** That is not just an internal velocity story — that is the rate at which your feature requests will land on your screen.
>
> A team of 5 cannot do any of these things. A team of 50 cannot do these things. Only a team of **2 humans plus Tesote AI** can.

### Slide 7 — Close

> Tesote AI exists today. It runs our books. It runs Mariel's books at Polar. It's pricing at **$1.5k per workspace per month, or $2.5k bundled** — less than half the fully-loaded cost of one of the people it replaces.
>
> The question for you isn't *whether* this is coming. It's whether you're the **first finance team in Venezuela** to run on it — or the tenth.

---

## Phase 4.1 — The pitch (V0.1, 2026-05-20) — *active draft*

> **What changed from V0:**
> - **Two-layer frame is now the structural spine** (was buried in Slide 5). Aligns with [[../product/ai/pitch-agents-plus-ai]]: **Tesote Automations** = deterministic autopilot; **Tesote AI** = infinite-possibility superpower. Both on Odoo.
> - **80/20 work-vs-time trap** added as the CFO-grade punch in Slide 2 — the part that makes the CFO say "you've watched me work."
> - **"Endless possibilities" / combinatorial** framing is the hero of Slide 4's AI half — "you cannot enumerate what Tesote AI can do, because the answer multiplies."
> - **Close (Slide 7) rewritten** with the "new chapter / finance department will never operate the same" landing.
> - Old Slide 4 (the fork) merged into the close — the survival framing is still there but lighter.

**Category — LOCKED 2026-05-20:** *"The operating system for Venezuelan finance teams."* Captures both layers (Automations + AI), broader than "AI co-pilot," still localized. The two-layer story is the differentiator and "OS" is the frame that earns it. All downstream messaging snaps to this.

---

### Slide 1 — The shift (insight)

> Something changed in the last 12 months that hasn't shown up yet in any finance team in Venezuela.
>
> **AI agents stopped being demos. They became operators.** They read a bank statement, post a journal entry, send a payment, reconcile a transaction — at production quality, in seconds.
>
> But the real shift is bigger than just AI. There are **two distinct kinds of work** inside every finance department. One is repeatable. One is impossible. Both have always been broken in Venezuela, for two different reasons.
>
> For the first time, **both are solvable at the same time.**

### Slide 2 — The old way + the 80/20 trap

> You live this every day:
>
> - 5–8 people in your finance function
> - Two of them spend their day in WhatsApp and 8 bank portals — Banesco, BNC, Mercantil, Banco Exterior, BBVA, BdV, Bicentenario — copying balances into Excel
> - One chases customers for payment, invoice by invoice
> - One processes AP — printing PDFs from email, re-typing them into your ERP
> - Reconciliation happens once a month, painfully, by hand
> - You close the month a week after the month is over
> - You report numbers to your CEO that were true two weeks ago
>
> **Here's the trap.** The repeatable, mechanical work is roughly **80% of the volume** — and it eats roughly **80% of your team's time**. The hard work — the cash flow puzzle, the fraud catch, the IVA decision, the cross-bank reconciliation — is the **20% that should be the headline**.
>
> Most days, it's the leftovers. Your senior controller is re-typing invoices. Your CFO is staring at Excel reconciling Mercantil by hand. **The work that actually moves the company is the part that doesn't get done.**
>
> *(Speaker note: the 80/80 is a mental model, not a measured statistic. If a CFO pushes, agree: "It's a heuristic — but every finance head I've shown this to has nodded.")*
>
> Globally, almost none of this is still true. In Venezuela, all of it still is — because **no one ever built the software for you.**

### Slide 3 — The two kinds of work

> Step back. There are two distinct types of work happening in your finance department, and they require **completely different tools**.
>
> **Type 1 — Repeatable work.** Predictable. Rules-based. Same shape every day. Reconciliation, categorization, AP routing, payment reminders, status reports, bank syncs. The volume.
>
> **Type 2 — Impossible work.** Judgment calls. One-off puzzles. The questions you can't answer until you ask. *"Why is my Mercantil cash position weird this month?"* *"Can I make payroll if Banesco's rail is still down on Friday?"* *"Walk me through everything we sent to Polar in March, then draft the WhatsApps."* The combinations.
>
> No single product has ever handled both. ERPs try to handle Type 1 and ship 60%. Excel handles Type 2 and breaks. Consultants stitch the gap with humans. **Both have always been broken, for two different reasons.**

### Slide 4 — Tesote = both layers, integrated

> Tesote handles both. **In two distinct layers, built to work together.**
>
> **Layer 1 — Tesote Automations.** The autopilot. Smart rules. Mass categorization. AP inbox → vendor bills, automatic. Continuous reconciliation. Retention auto-calc on every payable. Reminder cadences on every overdue invoice. Scheduled bank syncs across all 8 of your rails. Deterministic. Predictable. **Runs while you sleep.**
>
> This is the 80% off your team's plate. The part you set up once and stop thinking about.
>
> **Layer 2 — Tesote AI.** The superpower. You ask, it executes.
>
> - *"Cobra esta semana"* → 23 personalized WhatsApp messages to your overdue customers, sent.
> - *"Concílialo todo"* → 84 bank lines matched to invoices in 30 seconds.
> - *"¿Estoy lista para declarar IVA?"* → the check runs end-to-end.
> - *"Audita la salud de Crecer ahorita"* → a 22-day Scotia outage surfaced in 2 minutes.
>
> **And here's where it gets interesting.** Tesote AI doesn't have a feature list. The combinations are infinite. Payments + ERP + tax compromisos + bank reports + reconciliation + cash flow + audit + reporting + counterparty intelligence + supplier negotiation — **every combination is a new possibility.** Every week, your team invents a new prompt that solves a problem we never built a feature for.
>
> **You cannot enumerate what Tesote AI can do, because the answer multiplies.**
>
> Both layers sit on top of your Odoo as system of record. Both are live in production. Both are running on Tesote's own books today.

### Slide 5 — Why we're the only ones

> Tesote is the only product built for this two-layer reality in Venezuela. **Not adapted. Built for it.**
>
> **1. Instrumented to every Venezuelan bank at the rail level.** Banesco, BNC, Mercantil, Banco Exterior, BBVA, BdV, Bicentenario. Live in production. Not screen-scraping, not "we'll build it if you sign."
>
> **2. Odoo as system of record stays untouched.** Your CPA still posts the official ledger. Tesote is the system of action on top — agents that draft, propose, reconcile, send. Compliance unchanged. Operations transformed.
>
> **3. The AI acts. It doesn't just summarize.** That's the difference between a chatbot and an operator.
>
> **4. Multi-jurisdiction out of the box.** VE, Panamá, RD, USA, Caribbean. Multi-currency, sanctions-aware, regulation-aware. The day you expand, your finance stack already came with you.
>
> **5. We run our own books on it.** Every payment Tesote makes, every invoice we issue, every reconciliation we do — runs on Tesote. **There is no other vendor in this market who can say this sentence honestly.**

### Slide 6 — Proof (last 72 hours)

> Three things happened in my last three days using Tesote AI inside our own workspace:
>
> **One.** I asked it for a health audit on Crecer, a customer we'd onboarded weeks ago. In 2 minutes I learned their Scotia rail had been silently broken for 22 days, their Banesco credentials were dead, and 40,000 transactions were sitting uncategorized. Without Tesote AI, this would have surfaced when the customer churned.
>
> **Two.** Twenty minutes before a reference call to a Futura prospect, I ran a full month-to-date audit on Marcas Propias' workspace. I walked into the call knowing exactly what to defend and what to flag. The call went better because of it.
>
> **Three.** I specced a redesign of a major page on Sunday night. By Monday afternoon, the code was in a pull request, ready to ship. **Spec to production-ready PR in under 24 hours.** That isn't just an internal velocity story — that's the rate at which your feature requests will land on your screen.
>
> A team of 5 cannot do these. A team of 50 cannot do these. Only a team of **2 humans plus Tesote** can.

### Slide 7 — Close: a new chapter

> Look at what this actually means.
>
> The finance department in Venezuela has been operating the same way for 30 years. Spreadsheets. WhatsApp. Bank portals. People in seats doing manual work because the software was never built for them.
>
> **A new chapter is starting right now.** Automations take the 80% off your team's plate. AI gives your team superpowers on the 20% that actually decides whether the company wins. Both, in one product, instrumented to your reality, running on your Odoo, live today.
>
> **This is the operating system Venezuelan finance teams have always needed. It's the first one. And it exists today.**
>
> **The finance department in Venezuela will never operate the same way again.**
>
> Tesote runs our books. It runs Mariel's books at Polar. We're pricing it at **$1.5k per workspace per month, or $2.5k bundled** — less than half the fully-loaded cost of one of the people it replaces.
>
> The question isn't *whether* this is coming. It's whether you're the **first finance team in Venezuela to run on it — or the tenth.**

---

## What to push on (open questions for Luis) — *V0.1 cut*

### Resolved 2026-05-20

- ✓ **Category** → *"The operating system for Venezuelan finance teams"* (locked).
- ✓ **"We run our own books on it"** → confirmed true today, end-to-end. Keep the claim hard, no softening.
- ✓ **80/20 framing** → keep it. Positioned as a mental model, not a stat. Speaker note added in Slide 2 for CFO pushback.

### Still open

1. **Slide 4 — is "you cannot enumerate what Tesote AI can do" the right hero line**, or do you want a single concrete capability anchoring it? Risk of the abstract claim: it sounds like marketing fluff to a skeptical CFO. My bet: keep the abstract claim *but* end the slide with 1 concrete "what one of our clients did with this last week" to inoculate.
2. **Slide 4 — should the AI prompts (Cobra esta semana, Concílialo todo, etc.) move up to Slide 3** so the buyer hears actual prompts earlier? Current placement makes them feel like proof; earlier placement makes them feel like the product itself. Worth A/B testing live.
3. **Slide 6 stories are personal to you.** Mariel will need her own proof story (close-day-7 → close-day-2, or whatever the real number is). Polar reference story needs to be locked before any external delivery.
4. **Pricing on the close slide** — $1.5k anchors the conversation around price. Some founders argue this kills negotiating room. Alternative: leave price for the second meeting, close on "less than half a salary." Your call.
5. **Spanish translation** — once locked, who owns it? You / Vero / both? Per [[../feedback_client_email_spanish_voice]] tone conventions.

---

## What I (Luis) need to do next

- [ ] React to V0.1 slides 1, 3, 4, 5, 6 — slide by slide, kill / sharpen / reframe (slides 2 + 7 already incorporate the latest decisions)
- [ ] Resolve the 5 still-open questions above
- [ ] Decide: one CEO-delivered pitch, or a 1-slide *and* 5-slide *and* 15-slide variant?
- [ ] Get Mariel's real close-time number for Slide 6
- [ ] Once English V0.1 is locked → draft Spanish + retrofit [[../product/ai/pitch-agents-plus-ai]] (its Agents + AI frame already matches; just sync the OS positioning, the 80/20, and the close)
- [ ] Phase 0 (the 5 moments) is now optional — backfill only if a Phase 0 insight changes what's in Phase 4.1

---

## Related

- [[../product/ai/pitch-agents-plus-ai]] — the existing two-layer pitch (2026-05-13) — this doc is the upstream Dunford work behind it
- [[../product/ai/pricing]] — pricing draft (proof slide material)
- [[../product/ai/tesote-ai-design]] — design surface
- [[product-strategy-execution-plan]] — the 10x execution plan; Payments is the parallel bet
- [[week-2026-05-18-product-sprint]] — this week's anchor (dogfood = demo)
- [[../daily/2026-05-18]] — Tesote AI launched in internal workspace
- [[../daily/2026-05-19]] — Saldos PR loop closed, AI pricing drafted
- [[../daily/2026-05-20]] — Crecer + Marcas Propias audits (proof moments)
