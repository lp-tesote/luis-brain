---
title: Tesote AI — Customer Zero & the Right to Win
tags: [product, ai, strategy, pitch, 10x]
updated: 2026-06-20
status: draft
---

# Tesote AI — Customer Zero & the Right to Win

The spine of the pitch + the customer-education arc. tesote.ai (= Reverón) is now **the** AI product
we sell — the Claude-based treasury workspace AI was the MVP that proved the shape; this is the
ground-up build. See repo `github.com/tesote/tesote.ai`. Pairs with [[winning-vs-horizontal-ai]],
[[ai-use-case-taxonomy]], [[reveron-brand]], [[tesote-command-center]].

## 0. The one-line thesis (what we're educating the market on)

> Every company has to become AI-first this decade. Almost none have a *path*. **We are the path —
> and the rail it runs on.**

The education job: a customer's real AI journey does **not** start with "buy ChatGPT seats." It
starts with building a **model-independent operational layer** — their tools wired in, their
company brain, their governance — that *every future model plugs into*. We build that first building
block, **and they own it regardless of which model wins.** That's the durable asset; the model is a
rented, swappable input.

### The market reframe (lead the pitch with this)

1. **The bottleneck is not the model.** OpenAI and Anthropic are walking down the Fortune 500 list
   and discovering the hard part was never model quality — it's change management, implementation,
   and integration into the systems and knowledge the company already runs on. A frontier model in a
   company that hasn't done that work is a genius with amnesia who can't reach any of your tools.
   **That gap is where every enterprise AI project is currently stalling** — and it's the gap we fill.
2. **Nobody wants to bet the company on one model vendor.** The most advanced enterprises are
   deliberately building **model-agnostic** — context, integrations, and workflows in a *layer on
   top* that any model plugs into and that's cheap to switch. That is exactly our architecture (the
   Router rents/swaps the model; the brain lives in our layer). The Fortune 500 pays consultants
   millions to *attempt* this; we hand it to a company turnkey.
3. **The raw models give you no seamless way to build the KB.** Doing AI "properly" normally means a
   consulting project to assemble a wiki / RAG corpus / fine-tune — stale the day it ships, never
   maintained. Our memory layer **builds the KB itself, as a byproduct of using the tool** (see §4b).
   That's the thing we bring that the model companies don't.
4. **Land narrow, expand by gravity.** We start with the **finance team** — where Tesote already has
   the integrations wired (banks, Odoo) and the pain is sharpest — and we're honest it's the first
   room, not the whole house. But every conversation deepens the brain and every new system connected
   makes every other answer better, so the customer keeps connecting more of their systems to Reverón.
   That compounding *is* the moat and the switching cost.

## 1. What we deliver — day one vs. fast-follow vs. horizon (READ THIS FIRST)

**Pitch discipline.** The architecture (§4–§5) justifies the *vision*; it is NOT the day-one pitch.
On day one we sell ONE narrow, true thing: **Reverón wired to your Tesote workspace — talk to your
banking data.** Email, ERP, and payments are **roadmap** — name them as roadmap, never as "today,"
or we confuse the customer about what they're actually buying tomorrow.

| Phase | What's connected | What your team can do | Status |
|---|---|---|---|
| **Day one** | **Tesote workspace MCP only** (the work with Dan) | Ask your banking data in chat: today's position, movements/search, your categories, counterparties, rules, reports — in Spanish, and it **remembers your context** | **Shipping now** |
| **Fast-follow — Email** | IMAP / Gmail MCP | Inbox triage; AP invoices parsed into a queue; drafted replies | Next |
| **Fast-follow — ERP** | Odoo MCP | Reconcile bank ↔ posted records; accounting actions | Next |
| **Fast-follow — Payments** | Payment rails | The agent **moves money** (cobros / pagos) through your own rails | Next |
| **Horizon** | Your other systems / DBs, CRM, etc. | The whole company brain; AI becomes how work *and* money move | Vision |

**The day-one sentence to a customer:** *"Connect your Tesote workspace and talk to your money —
your position, your movements, your rules — and it remembers how your finance team works. Then we
add your email, your ERP, and payments, one at a time."* Day-one is the first row; everything after
the comma is the roadmap, said as the roadmap.

## 2. Customer zero — the day-one slice (and the vision behind it)

The proof we sell with is ourselves. Today the finance team logs into ~6 bank portals, exports
movements, rebuilds the Posición Diaria in a sheet, and pings Luis on Slack — hours a day, and the
*how* lives in one person's head.

**What Reverón does on DAY ONE (Tesote MCP only):**
- **"¿Cuál es la posición de hoy?"** → agent hits the Tesote workspace MCP (banking data across BNC,
  Banesco, Banco Exterior, Mercantil…) → a **live table** of cash by bank/currency. Sort it, drill
  in, filter to USD — **none of it re-asks the model** (data-bound artifact re-queries the source).
  Finance *works in it*, not reads a dump.
- **"Búscame los movimientos sobre X de este mes"** → transaction search/filter, your categories and
  counterparties, your rules, your reports — all in chat.
- And it **knows the company** — Banco Exterior is never "Bex," VDT is the test bench, BCV is the FX
  lens. The memory layer is live on day one even though only one system is connected.

**What becomes possible as fast-follows light up (say as roadmap, not today):**
- *[Fast-follow: ERP]* "Concilia las últimas 200 transacciones" → matches bank ↔ Odoo posted records,
  **stops for approval before posting** (irreversible gate).
- *[Fast-follow: Email]* Overnight invoices arrive by email to a hosted inbox (`apps/inbound`), get
  parsed, and sit in an AP queue as drafted payments awaiting an OK.
- *[Fast-follow: Payments]* The agent doesn't just flag what to pay — it **pays**, through your rails.
- *[Horizon]* "¿Dónde está el deal de CAPCA?" across a Sales Space (HubSpot + Fireflies); the brain
  spans functions.

The point of customer zero: **day one is genuinely narrow** (one connected system), but the *same
product* walks the customer up the table above, and the memory layer makes each step compound.

## 3. The primitives → how they change the way a company operates

| Building block | The operating change (what to sell) |
|---|---|
| **MCP Gateway** (3-tool lazy surface) | The company's software stops being *things people click* and becomes *things one agent operates*. No ceiling on how much you wire in — 200 tools cost the same context as 6. Employee's job shifts from "operate 8 systems" to "ask + approve." |
| **Memory (gravity layer)** | Institutional knowledge stops walking out the door. Onboarding collapses. The brain compounds monthly and is expensive to leave. *"Your team's hard-won knowledge becomes an asset that appreciates, not a liability that quits."* |
| **Live data-bound artifacts** | AI gives you a working spreadsheet wired to the live source, not a screenshot. Kills the stale-Excel problem — people operate *on* the output. |
| **Background / headless agent runs** | The agent is staff, not a tool. Throughput stops being bounded by human hours; work is done by morning, waiting at the approval line. |
| **Sealed credentials + approval gate** | This is *why you can let it near the money.* Plaintext never reaches the model; irreversible actions stop for a human. The adoption unlock for finance. |
| **The payment rail (endgame)** | Frontier AI ends at *advice*. Ours ends at *action* — it moves money through your own bank rails. The feature→business turn, and the valuation turn. |

## 4. Deep dive — the MCP Gateway (the most "holy shit" block)

Grounded in `apps/backend/src/agent/mcp-gateway-toolset.ts` + `docs/architecture/mcp-gateway.md`.

**The ceiling everyone else hits.** Naive agents (a ChatGPT custom GPT, a raw tool-using agent) hand
the model every tool's full schema *every turn* — linear cost. 40 tools ≈ 8k tokens before any work.
So "AI connected to your systems" stays a toy past a handful of tools.

**Our move — 3 tools, flat forever.** The model never sees your tools; it sees `mcp_list_tools`
(cheap catalog + param hints), `mcp_describe_tools` (full schema only for the tool it's about to use,
only that turn), `mcp_call` (fire). `discover → describe → dispatch`. **200 wired tools cost the same
context as 6.** There is no ceiling on how much of the company you connect, and it never gets heavier.
*That's the line: we don't connect a few of your tools — we connect your whole company.*

**Scale and safety are the same mechanism (masking).** A tool governance hides isn't *blocked*, it's
**invisible** — asking for it returns the byte-identical error a typo returns (`McpToolNotFoundError`,
fail-closed before anything hits the wire). The agent can't enumerate what it wasn't granted. So the
intern and the CFO use the *same* agent and each sees only their permitted surface → roll out
org-wide on day one, not to one power user in a sandbox.

**The approval gate is a live predicate.** `mcp_call` re-reads live policy on every call and stops
only on irreversible actions; the "irreversible" flag is never shown to the model. The agent does the
95% reversible work autonomously and stops at the 5% that moves money. That's safe delegation.

**One-click connectors + workflows — product, not consultancy.** A connector is curated MCP behind a
one-click install; *"add a tool never needs a deploy."* A workflow = connector + prompt preset +
suggested prompts, a capability you *start* in one click. Under it: audience-bound OAuth (a bank token
can't be replayed to email), encrypted-at-rest creds, and a delegate principle — *a system prompt
can't escalate past what the logged-in user may access.*

**The ownership punchline (proves §0).** All of it — connectors, governance, approval rules, memory —
lives in a layer the **model just visits**. The Router swaps the model freely; the customer's wired-up
operation, governance, and brain are untouched. Their investment is a **model-independent operational
layer every future model inherits.** That's the first building block; everything else plugs into it.

## 4b. Deep dive — the Memory / gravity layer ("the business, not a feature")

Grounded in `apps/backend/src/services/memory/{recall,graph-memory-candidates,extractor,forget}.ts`
+ `docs/architecture`/`docs/initial-idea/memory.md`. This is the answer to all three market-reframe
points (§0): it's how the KB gets built, why the layer is model-independent, and why expansion compounds.

**It builds itself — the seamless KB the raw models don't give you.** After every conversation, off the
hot path, a cheap model distills the durable facts/preferences worth keeping, dedupes against what's
known, and upserts them. **Nobody curates a wiki; the company brain accumulates from the work itself.**
That replaces the stale, never-maintained consulting deliverable every enterprise AI project chokes on.

Four things that make it a real *company brain*, not "ChatGPT remembers your name":

1. **Self-correcting.** A new fact that contradicts an old one **tombstones** it (`superseded_by`),
   excluded from recall at the DB layer and in the ranker. Finance facts change constantly (vendor
   terms, FX rules) — the brain *heals* instead of rotting. Kills the "won't an auto-KB fill with
   junk?" objection.
2. **Decays on purpose.** Recall ranks by **exponential recency decay (30-day half-life)** + relevance.
   Fresh truth outranks year-old stale facts — it weights what's current, like good judgment does.
3. **Associative recall, not just search.** A **graph-memory** layer does a 2-hop walk over memories
   sharing a source conversation / entity / past citation — surfacing related facts recency aged out,
   the way an experienced person remembers *around* a topic. Isolation is structural (discovered ids
   re-enter through the same permission gate; can't leak another user's/team's facts). Rebuildable
   index, 400ms budget — degrades silently, never stalls or breaks a reply.
4. **Auditable.** Every answer that used a memory **cites** the specific memory that grounded it
   (decision trace) → a CFO can ask "why did it say that?" and get the receipt. The trust property
   that lets finance rely on it.

Wrapping all of it: **governed** (per org/space/user, owner controls shared-vs-personal), **no-train**
(never trains a model, never crosses tenants), **exportable/deletable** (a real `forget` path). *The
brain is theirs — they can walk out the front door with it.*

**Model-agnostic punchline.** The brain lives in *our* layer; the model is a rented input the Router
swaps freely. Swap the model next year → **the company keeps its brain.** The Fortune 500 pays
consultants millions to *attempt* this architecture; we ship it turnkey, and it self-builds.

**Why land-and-expand is inevitable.** Every conversation deepens the brain; every new system connected
makes every *other* answer better (finance learns the cash rhythm; add HubSpot and it knows a customer's
deal AND payment history in one breath). Compounding = the gravity = the switching cost. A year in,
leaving means abandoning a self-built, self-correcting brain that knows how the company actually runs.

**The line:** *"The model is rented and replaceable. The brain it builds is yours, and it gets smarter
every time anyone uses it."*

## 5. Why Tesote, not OpenAI — the right to win

> **OpenAI sells the engine. We sell the car — already wired to the roads that exist in Venezuela.**

The gap between "bought ChatGPT seats" and "company runs on AI" is integration + governance + local
rails + accumulated gravity. That's not a model — it's a product and a local operator's job, and no
horizontal giant will build it for a market this size. We own the gap. Five defensible reasons:

1. **Access** — foreign AI is blocked/throttled/priced-for-SF here; we're local, cheap, reachable
   today. They can't be the front door in VE right now.
2. **Integration labor** — someone must wire VE banks + Odoo + local rails and *keep them working*
   through every API change. Two years of Tesote's unglamorous work, already done. OpenAI never will.
3. **Governance & trust** — data stays in-region, no-train, exportable, locally compliant; modeled
   into the schema day one. The thing that lets a CFO say yes.
4. **Accumulated gravity** — every company's brain compounds inside the product, expensive to rebuild
   elsewhere. First-mover here is a permanent lead.
5. **The rail** — we move money; they don't. Turns a thin AI-resale wedge into a fintech business —
   and is the part OpenAI structurally cannot copy in VE.

**The meta-argument (why it's revolutionary, not risky):** we are *not* betting on having the best
model — we rent and swap it through the Router. We're betting the model **stops being the
differentiator**, which is exactly why a horizontal model company is the *wrong shape* to win this.
Value moves to integration, governance, gravity, and rails. (The Harvey/8090 lesson — see
[[winning-vs-horizontal-ai]].) OpenAI winning here would require them to become a Venezuelan fintech
integrator. They won't.

**The honest caveat to hold in the same hand:** our *wedge* (cheap-model access) is also the most
replicable layer. The whole thesis is **convert front-door users into gravity faster than the access
arbitrage closes.** The architecture is built to do exactly that; that conversion rate is the number
the dream rests on.

## 6. The education arc (how we teach customers into it)

1. **Reframe the journey** — "AI-first" isn't seats; it's a model-independent operational layer. We
   build the first building block.
2. **Show customer zero** — Tesote running on Tesote AI is the demo, not a deck.
3. **Name the ownership** — what you build (connectors + brain + governance) is yours and survives
   every model change. De-risks the buy.
4. **Land the partner case** — only a local operator with the bank/Odoo/rail integrations and the
   compliance story can bring it home; that's us.
5. **Point at the rail** — today it advises and acts on your systems; tomorrow it moves your money.

---

*Next moves: (a) keep drafting here; (b) promote a polished cut to the KB for the team; (c) pull the
customer-zero story into the investor narrative. Deeper single-primitive write-ups (memory, payments
seam) on request.*
