---
title: Tesote AI — Context Pack for Vero
tags: [ai, marketing, gtm, launch, handoff]
updated: 2026-06-11
status: handoff
audience: Vero (marketing lead) — everything Luis has been thinking about Tesote AI, in one place
---

# Tesote AI — Context Pack for Vero

> **What this is.** Everything I've been working through on Tesote AI — strategy, positioning, the pitch, the use-case map, pricing, the launch plan — collapsed into one self-contained brief. You don't need to chase a dozen files; the substance and the key passages are inlined here, organized so you can read top-to-bottom or jump to what you need.
>
> **Why now.** AI launch (~June 22) is an all-functions operation and marketing owns a big chunk of it. This gives you the full backstory of *how I've been thinking about it* so your work doesn't have to reverse-engineer my head.
>
> **How to read it.** Part 1 is the 90-second thesis. Part 2 is how the thinking evolved (so you can tell current from superseded). Parts 3–4 are the ideas and the docs. Part 5 is the decisions ledger (locked vs. open). Part 6 is your workstream specifically. Part 7 is the voice/terminology guardrails — read that before you write a single line of copy.
>
> Snapshot as of **2026-06-11**. Where two versions of a doc exist, I flag which one is current.

---

## Part 1 — The thesis in 90 seconds

Tesote AI is **the operating system for Venezuelan finance teams.** It's a general-purpose AI — it can answer *any* question and hold a normal conversation — but everything about how we frame, demo, and price it says **built for enterprise finance.** It sits on top of the customer's unified financial data in Tesote and works in two layers:

- **Tesote Automations** — the autopilot. Deterministic rules that run the repeatable ~80% of finance work (categorization, reconciliation, reminder cadences, bank syncs). Set up once, runs while you sleep.
- **Tesote AI** — the superpower. You ask, it executes, you supervise. The judgment-driven 20% that actually decides whether the company wins.

> **⚠️ Day-one scope — this is the launch's load-bearing messaging fact (corrected 2026-06-11).** Version 1 (June 22) runs **strictly on the Tesote MCP**: the customer's **banking data** unified across all their banks, plus **categories, counterparties, rules, and reports**. That's the surface **100% of our customers and users can use on day one** — no Odoo required. **The Odoo MCP** (reading/writing the ERP — bills, invoices, journal entries) is the **next chapter, not the launch.** We lead Tesote-MCP-first *because* it's universal; Odoo is the wave-2 expansion story. Anywhere older docs say "two layers on top of your Odoo," read it as **"on top of your unified Tesote data first; Odoo next."**

The posture is **not "a copilot."** It's **a finance chief** — opinionated, SENIAT-fluent, proactive, never sleeps. It doesn't wait to be asked; it walks into your books and tells you what's broken.

**Why we win** (the moat): a horizontal Claude/ChatGPT only sees what you paste in. We join every VE bank rail + categorization + counterparties + (later) the ERP and the email inbox, and we *act* across them — VE-native (RIF, SENIAT, comprobantes, BCV), audited, multi-player. This is the Harvey/Legora playbook (vertical AI beat horizontal AI on the wiring around the model, not the model). Yes, it can also just answer general questions — that's table stakes; the moat is the finance substrate underneath.

**The proof that makes it real:** we run our own books on it. No other vendor in this market can say that sentence honestly.

**The launch mechanic:** give → watch → bucket → upsell. Turn AI on for every workspace behind a trial limit, watch per-user/per-workspace usage from minute one, sort customers by behavior, and upsell the moment they hit the limit. Target ~June 22, booking **$21k MRR** in upsells (≈14 logos at entry tier).

---

## Part 2 — How the thinking evolved (the arc)

Read this so you can tell what's load-bearing today from what's been superseded. The thinking moved from *aspiration* → *category* → *posture* → *reality-check* → *launch operation*.

| Date | Milestone | What it locked |
|---|---|---|
| **2026-05-12/13** | First pitch: **Agents + AI** two-layer frame | The capability catalog + the "install today" test |
| **2026-05-18** | Tesote AI shipped live in our own internal workspace (Dan) | Dogfood = demo. Real proof moments start accruing |
| **2026-05-20** | **Finance-chief positioning** + **Dunford category work** | Posture = *chief, not copilot*. Category = *"the operating system for Venezuelan finance teams"* (locked) |
| **2026-05-22** | **Use-case taxonomy** (12 jobs × 4 execution modes) | The "what to build, on which surface" map. Most work = Automations, not chat |
| **2026-05-24** | **Winning vs. horizontal AI** (the moat doc) | The 7 Harvey/Legora patterns + why a generic Odoo MCP can't match us |
| **2026-06-03** | **Live capability audit** — probed the product against prod | Hard truth: several claims were aspirational (100-tx cap, free-form totals) |
| **2026-06-05** | **Pitch v2 (launch-narrow)** | Pitch only what's live-verified; rules-engine reframe; dated 30-day eng slide |
| **2026-06-08** | **Launch master plan** (Luis↔Esteban) | The all-functions June-22 operation; give→watch→bucket→upsell; $21k target |
| **2026-06-09** | **Pricing references** (Harvey/Legora/Basis research) | Category norm = per-seat annual + seat minimum, value-metric not price |

**The single most important inflection:** the 06-03 audit. Before it, the pitch promised "categoriza los últimos 3 meses" and "las posibilidades son casi infinitas." The audit found the transaction search was hard-capped at 100 rows — meaning those claims produced *confident wrong numbers* on any real workspace. We pivoted to **launch narrow**: pitch only what works today, put the fixes on a dated slide. For a finance AI, "it works and doesn't lie" beats "it does everything."

---

## Part 3 — The four load-bearing ideas

Everything else is detail on top of these four.

### Idea 1 — The category: "the operating system for Venezuelan finance teams"

(Locked 2026-05-20, via April Dunford's *Obviously Awesome* method.) We deliberately do **not** let people slot us into "AI for finance" or "ERP automation" — there we lose to Ramp/Brex/Vic.ai on their terms. We pick a category where global tools are structurally absent: Venezuela. The competitive alternative isn't other software — **it's a payroll line** (5–10 humans + Excel + WhatsApp + 8 bank portals). We're displacing headcount, not a competitor.

The old-way/new-way diptych that anchors the pitch:

| Dimension | Old way | New way (Tesote) |
|---|---|---|
| People required | 5–10 humans | 2 humans + agents |
| Tools | Excel + WhatsApp + 8 bank portals + email | One workspace, one prompt |
| Reconciliation | Monthly nightmare | Continuous, agentic |
| AR / Cobros | One-by-one drafting | "Cobra esta semana" → 23 personalized WhatsApps |
| Visibility | Owner finds out at month-close | Owner sees it the moment it breaks |
| Build velocity | Months of eng per surface | Spec → PR in 24 hours |

### Idea 2 — The posture: a finance chief, not a copilot

"Copilot" is generic — every fintech shipped one. **"Chief" is a category move.** The chief *grades* (every function gets a running grade), *prosecutes* (names the counterparty, the dollar, the owner), *diagnoses* (connects symptoms across functions), *recommends with teeth* (pre-built action, not advice), and *owns the calendar* (IVA is due Friday, here's what's blocking it).

The line that lands in a 15-minute demo: **"You can't afford a CFO of this caliber. We'll be one for you."**

Why it's defensible: opinions require a *rubric*, and the rubric — "this is what good LATAM books look like" — takes months to encode. Anyone can wire GPT to Odoo; almost nobody will build the rubric + the LATAM tax intelligence (SENIAT, factura fiscal, comprobante de retención, contribuyente especial, BCV diferencial).

Spanish landing tagline candidate: **"El chief financiero que tu empresa no puede contratar. Trabaja 24/7. Habla SENIAT."**

### Idea 3 — The moat: why we beat horizontal AI

Within 12–24 months, a controller could install Claude desktop + an Odoo connector and ask "¿cuánto le debo a CANTV?" — done, no Tesote. That's the bear case. Five structural reasons we still win:

1. **Odoo is one system; finance is N systems.** We're the only layer joining Odoo + bank rails + WhatsApp + email inbox + payment links + cross-entity state. The MCP sees a node; we see the graph.
2. **MCP exposes data; Tesote executes work.** The high-value finance work is transactional (send a botón link, debit + post + attach, run a 3-touch cobranza). Not "ask Odoo for X."
3. **Generic chat ≠ product.** A CFO wants "show me what to chase this week" — a button, not a blank prompt. We pre-bake the joins, prompts, workflows, and bank dialects.
4. **LATAM/VE ontology isn't in Odoo's schema.** BCV vs. paralelo, RIF/SENIAT, comprobantes de retención, bank alias resolution. Our ontology, accumulated by the product.
5. **Audit, multi-tenant, role-gated action.** Finance actions need an audit trail, isolation, role gating, reversibility. Generic chat has none.

> *If Odoo MCP is git for accounting, Tesote AI is the IDE.*

**The 7 patterns we steal from Harvey & Legora** (legal-AI category winners): (1) workflows, not chat; (2) the "do this to N things" table primitive; (3) source-grounded citations as the trust mechanism; (4) speak the user's dialect; (5) multi-player by default; (6) land-and-expand via deep reference accounts; (7) narrow + deep beats broad + shallow.

### Idea 4 — Two kinds of work (and why it justifies two layers)

There are **two distinct types of work** in every finance department, requiring completely different tools:

- **Type 1 — Repeatable work.** Rules-based, same shape every day. ~80% of the volume, eats ~80% of the team's time. → **Tesote Automations** (the engine).
- **Type 2 — Impossible work.** Judgment calls, one-off puzzles. The 20% that actually moves the company. → **Tesote AI** (the chief).

The trap: today the senior controller spends the day re-typing invoices (Type 1) and the work that moves the company (Type 2) is the part that never gets done. No single product has ever handled both. ERPs ship 60% of Type 1; Excel handles Type 2 and breaks. **Tesote handles both, in two integrated layers** — at launch, on the customer's unified banking data + categorization/counterparty layer; the ERP (Odoo) leg is the next chapter.

---

## Part 4 — The docs, mapped

Grouped by purpose. For each: what it is, status, and the passages worth knowing. (These all live in my private brain — this pack is so you don't need them, but I'm naming them so we can talk in shorthand.)

### A. Strategy & moat

**`winning-vs-horizontal-ai`** — *the strategic anchor.* The moat argument above (5 reasons + 7 Harvey/Legora patterns). Most marketing-load-bearing implication: **at least one demo moment should be a delegation / "while you slept" moment, not a query** — e.g. *"And while you slept, Tesote chased 14 receipts, marked 12 deducible-eligible, and recovered $2,340 in tax credit you'd have lost."* Speed-of-query is a feature; delegation is the product.

### B. Positioning

**`positioning-the-finance-chief`** — *the posture (the why).* Idea 2 above. Contains a full **"rant menu"** — the lines the chief says unprompted, in my voice, in Spanish. These go straight into demo/deck/landing. A few:
- *"¿Por qué llevamos 4 meses sin conciliar Banesco? Hay 312 BSLs sin emparejar."*
- *"Polar te debe $47k desde febrero. No le hemos enviado un solo recordatorio en 6 semanas."*
- *"Estás perdiendo 2.8% por factura en el diferencial cambiario. En lo que va del año son $34k."*
- *"¿Estás lista para declarar IVA? Corrí 32 verificaciones. 4 en rojo, 6 en amarillo. ¿Empiezo a arreglarlas?"*

Pitch lines stocked for surfaces: *"A copilot does what you ask. A chief tells you what you should have asked." · "El chief financiero que tu empresa no puede contratar. Trabaja 24/7. Habla SENIAT."*

**`tesote-ai-positioning`** (Dunford) — *the upstream category work.* Where the category got chosen and the old-way/new-way diptych + 5-component grid live. **Category LOCKED: "the operating system for Venezuelan finance teams."** Holds two full pitch drafts (V0 and the active V0.1) — the V0.1 spine is: shift → old-way + 80/20 trap → two kinds of work → both layers → why only us → proof (last 72h) → close ("a new chapter"). *Caveat: the V0.1 pitch was written before the 06-03 audit, so its scope claims ("posibilidades casi infinitas") are softened in the current pitch — see C.*

### C. The pitch (three docs — know which is current)

**`pitch-today-v2`** — ✅ **THIS IS THE CURRENT PITCH** (2026-06-05, launch-narrow). The reframe that matters for every piece of copy:

> **"No categorizas 10.000 transacciones. Le enseñas a Tesote 20 reglas en una conversación — y el motor categoriza todo: el histórico completo y todo lo que llegue mañana."**

The AI's identity in v2 = **the setup brain that builds your machine in one conversation**, not a bulldozer that touches every row. The two day-one pillars (Tesote MCP, universal to all customers): (1) **Setup en masa** — "el primer día con Tesote no es un proyecto de implementación, es una conversación" (rules, categories, counterparties built from patterns in one chat, applied retroactively to all history); (2) **Reports = saved definitions, run + narrated** — "tus reportes corren igual todos los meses; la AI te los explica, no los inventa."

> **Reframe for launch (2026-06-11):** the v2 doc lists a third pillar — **Odoo mass workflows** ("la AI nunca toca tu Odoo a ciegas; todo es preview primero, y todo queda auditado"). That pillar is now **wave 2**, not day one — it requires the Odoo MCP, which not all customers have. Hold it as the expansion chapter. Day-one launch messaging = the two banking-data/setup pillars above, plus general Q&A on the customer's own financial data.

**What we no longer say** (until the eng gate ships): ❌ "categoriza los últimos 3 meses" as a chat op · ❌ free-form totals ("¿cuánto gasté en X?") · ❌ "las posibilidades son casi infinitas" · ❌ "concílialo todo" as headline. The dated 30-day slide names the three fixes *with a month* (flujo de caja por categoría, deep dive sin límite de filas, conciliación de punta a punta).

**`pitch-agents-plus-ai`** — *the capability catalog (aspirational; read beside the audit).* The original two-layer frame + the by-function walkthrough (Receivables / Payables / Reconciliation / Categorization / Counterparties / Close / SENIAT) with the AI prompt + wedge sentence for each. Great source of *language* and *per-function proof prompts*; just don't treat its scope claims as live — v2 is the source of truth for what's real today.

**`pitch-today`** — v1 (2026-05-20), **superseded.** Demo mechanics + objection bank still mostly valid; scope claims aren't.

### D. The use-case map

**`use-case-taxonomy`** — *the internal "what to build next" map.* 12 jobs-to-be-done (close books, pay vendors, collect from clients, reconcile, manage cash/FX, forecast, tax compliance, regulatory, master data, report up, investigate, payroll touchpoints) × 4 execution modes (autopilot / draft-approve / scheduled / on-demand chat). Marketing takeaway: **most of this is Automations work, not chat** — so when we show capability, lead with delegation. The sharpest ROI story sits in the documentary-evidence triplet (gastos deducibles + comprobantes): a customer spending $50k/yr on cards is *already* losing ~37% in tax credits they're entitled to but lose because chasing receipts is the worst job in the building. That ROI math sells itself.

### E. Pricing

**`pricing-references-legora-harvey-basis`** — *category benchmarking (deep research, 06-09).* All three vendors run **enterprise contact-sales, no published price.** Category norm = **per-seat annual + seat minimum**, value sold on **hours-saved / % efficiency**, *not* consumption metering. Harvey ≈ "$1,000–1,200/lawyer/mo" (estimate only) and frames "37 hours saved/month." Implications for us: (1) opacity is normal — we're not obligated to publish; (2) per-seat annual is the reference architecture; (3) sell a **value metric** we can stand behind (reconciliation hours saved / cobros accelerated / FTE-equivalent), not a price; (4) none operate in LATAM — willingness-to-pay localization is ours to figure out.

**`pricing` (SKU draft)** — current internal thinking: ~$1.5k entry, climbs by **data tier × seats**, 80% margin target, soft overage. **$1.5k is the entry point, not the ceiling.** (Exact numbers still being locked with Esteban — see Part 5.)

### F. The launch

**`launch-master-plan`** — *the orchestration layer above everything* (2026-06-08, Luis↔Esteban). Target ~June 22. The model: **give → watch → bucket → upsell.** North star = "be *able* to upsell 100% of customers in week 1" (a readiness bar); real target = **$21k MRR** (≈14 logos at entry). Four buckets: A = instant yes (same-day close), B = warm/needs selling, C = active pipeline non-customers, D = closed-lost reactivation. The linchpin is **usage telemetry live on day one** — without it there's no trigger, no bucketing, no evidence for the CFO. Bundled with the redesign (Saldos / Movimientos / new Dashboard + landing page) so it lands as one big statement. VIP framing throughout: "this is an internal launch, not public yet."

### G. Marketing (your turf — some already yours in Notion)

**`tesote-ai-rollout-plan`** — GTM container. Two stages: Stage 1 = warm-list pilot (2-min Luis-narrated Loom-style video, Venezuelan `tú`, 3 demo moments), Stage 2 = mass rollout (dedicated `/ai` landing, social cutdowns, webinar, sales enablement, Odoo partner channels). Several open decisions wait on you: demo moments, CTA, hook angle, list assembly, distribution mechanism, Mariel case-study angle.

**`landing-page-argument`** — the new tesote.com homepage narrative. **Villain: la conciliación. Structure: el ciclo de vida de la plata** (Ver → Pagar → Cobrar → Contabilizar → Entender). **AI is the crescendo (Act III)** — earned by the stack beneath it: "ChatGPT can't reconcile your Banesco account against your ERP; the thing that can is the thing already connected to both." Live candidate is v11; ported to Rails on `redesign-homepage-v41`. (Security claims still need Dan's sign-off.)

**`function-map-ai-roadmap`** + **`roles-in-ai-augmented-team`** — *already promoted to Notion; these are yours.* The AI-augmented marketing operating model (Tier 1 = Customer Advocacy / Product Marketing / Founder-Led Content / Lifecycle & Expansion; you as editor-in-chief of the skill system, #2 as writer-operator). Listed here for completeness — no new context, you own the source.

---

## Part 5 — Decisions ledger (locked vs. open)

So you don't reopen settled questions or build on sand.

**Locked:**
- Category: "the operating system for Venezuelan finance teams"
- **Day-one scope = Tesote MCP only** (banking data + categories + counterparties + rules + reports — universal to 100% of customers). **Odoo MCP = wave 2.** *(corrected 2026-06-11)*
- **It's a general-purpose AI** (answers anything, normal conversation) **framed as built for enterprise finance.** *(corrected 2026-06-11)*
- Posture: finance chief, not copilot
- Product name: **Tesote AI** (English "AI", not "IA"; "La IA" only in marketing/colloquial register)
- Two-layer frame: Tesote Automations (autopilot) + Tesote AI (superpower)
- Pitch is **launch-narrow** (v2) — pitch what's verified, dated slide for the rest
- "We run our own books on it" — true today, keep the claim hard, no softening
- Launch bundled with the redesign (not unbundling)
- Trial scope: both per-workspace AND per-user, all workspaces/users
- Pricing *variables*: data volume × seats; $1.5k = entry not ceiling
- Contract: Luis + Vero draft, PTCK green-lights (you start this)

**Still open (need Luis/Esteban this week):**
- Exact entry price + tier multipliers + trial counts
- Is the instrumentation engine scoped in time for June 22 (the thing that quietly kills the launch)
- Limit-hit trigger mechanic (auto-notify exec / in-app nudge / standup dashboard)
- New-Dashboard design lock (the long pole on the redesign)
- Rollout-video open decisions (demo moments, CTA, hook angle, list, distribution, Mariel)
- Landing page: hero H1, public product names (Spanish vs. English), security claims (Dan)

---

## Part 6 — Your workstream for the launch

From the master plan, marketing (you, + Maria Alesia starting Jun 22) owns three beats plus two comms pieces:

1. **Intrigue (pre-launch)** — "algo va a pasar el 22" teaser to existing + new customers. Build curiosity.
2. **Launch day** — "new feature — try it free here, 2–3 prompts, ask your account exec." One-tap-easy.
3. **Arsenal / destination** — the new website is where they land and see everything coming (AI first, then pagos/cobros). The redesigned landing was step 1 of this launch by design.
4. **Tesote AI video** — the internal-launch hero asset (in flight).
5. **"Internal launch / not public yet"** messaging woven through — the VIP framing.

Plus two specific comms pieces assigned to you:
- **Bucket D (closed-lost) reactivation sequence** — "new product, internal launch, come see." Its own track (co-owned with Esteban).
- **The payments/cobros FOMO message** — when customers ask about payments (not ready), the answer must create FOMO and leave them wanting more: "next chapters of the arsenal, you're seeing it first" — *never* "it's not ready." One paragraph in the objection bank (co-owned with Esteban).
- **The comms calendar** — buckets A–D get different messages at different times; one owner (you) holds the day-by-day send calendar, not just the assets.

And the legal kickoff: you start the **frictionless subscription contract** (5 bullets, click-to-sign, reads like Stripe/Notion checkout terms) + **T&C + Privacy Policy** (the privacy story for a finance AI touching bank data is part of the *trust pitch*, not just compliance) — laid out so PTCK does a green-light pass, not a redline round.

---

## Part 7 — Voice & terminology guardrails (read before writing copy)

These are non-negotiable conventions baked across everything above:

- **Audience = the whole *finanzas* function** (CFO, controller, AP/AR, contador) — frame as "finanzas", **never "tesorería"** (except verbatim client quotes who say it themselves).
- **Spanish is Venezuelan `tú`, never `vos`** (that's Argentine). Sweep whole screens/assets for dialect consistency, not just one line.
- **Product name is "Tesote AI"** (English "AI"). "La IA" is fine in marketing/colloquial register only. Don't add a "Copiloto" badge.
- **Bank names**: always "Banco Exterior", never "Bex". (Internal alias map exists for matching: BICENTENARIO=BDT, MI BANCO=R4, PROVINCIAL=BBVA — not for public copy.)
- **Don't say "Claude/OpenAI is blocked in VE."** Frame positively: *"la IA más avanzada, aplicada a tus finanzas, disponible aquí."*
- **No pricing on the homepage** — sales-led, single CTA "agenda una demo." (Pricing shows up in the pitch/upsell motion, not the public site.)
- **The network thesis stays internal** — the visitor buys "te pagan y se concilia solo"; the network is our consequence, not their pitch.
- **Security claims must be verified with Dan before shipping** — anywhere they appear.
- For a finance AI, **"it works and doesn't lie" > "it does everything."** Never let copy promise scope the product can't back today (the whole reason for the launch-narrow pivot).
- **Day-one = Tesote banking data, not Odoo.** Launch copy demos banking data + categories/counterparties/rules/reports. Don't lead with ERP/Odoo workflows — that's the wave-2 chapter. (Internally we run on Odoo; that's a *proof* point, not the day-one customer surface.)
- **General-purpose, enterprise-framed.** It's fine — good, even — that it can answer anything; but the copy, demos, and examples should always be *enterprise finance* ones. "Talks like ChatGPT, but it's your finance team's" — never position it as a general chatbot.

---

## One thing I'd flag

A lot of the sharpest *language* is already written — the rant menu in the finance-chief doc, the per-function wedge sentences in the capability pitch, the V0.1 pitch slides. That's raw material for the video script, the landing crescendo, and the intrigue campaign. The judgment call that's yours: which 3 wedge moments are the *hero* ones for a VE CFO. **Pick from what's day-one true (Tesote MCP):** the cross-bank Q&A ("todos tus bancos, una sola pregunta"), the setup-en-masa moment ("escribió 10 reglas que tú aprobaste — el motor hizo el resto, y es auditable"), the counterparty cleanup, the report-narration moment. The Odoo-flavored prosecutions (SENIAT/factura-fiscal, "esto no lo hace ChatGPT") are *killer* — but hold them for the wave-2 / Odoo-customer story, not the universal launch. That day-one/wave-2 split is exactly the taste layer you own.

If anything here is stale by the time you read it, the master plan and pitch-today-v2 are the two that move fastest — ping me and I'll re-sync.
