# AI

AI as the productized surface — the "superpower layer" on top of the Tesote Agents (the autopilot layer in [[../automations/]]). Anything that's "AI as the product" rather than AI as internal tooling lives here.

## Live docs

- [[launch-master-plan]] — **the all-functions launch operation (the orchestrator above everything else).** Reverse-engineered "be able to upsell 100% of customers in week 1" plan, target **~June 22**. give→watch→bucket→upsell model; owners across sales/marketing/legal/CX/product; the per-tenant usage telemetry **engine** as the linchpin; open decisions for Luis + kickoff agenda. Source: Luis↔Esteban call 2026-06-08. Read this first for launch; the rest are its inputs.
- [[tesote-ai-design]] — **design dossier** for the `/ai` surface as built in treasury (system prompt, op protocol, panes, security boundaries, file map). Snapshot 2026-05-20.
- [[typography-spec]] — **typography redesign** for `/ai`. Drops Inter Tight for Inter + Instrument Serif, caps weights at 500, bumps body to 15/1.6. Companion mockup: `typography-comparison.html`.
- [[iconography-spec]] — **no emojis** rule for `/ai`. All icons inline SVG via Lucide at 1.5px stroke. Audit + replacement table for current symbol-as-icon usage.
- [[winning-vs-horizontal-ai]] — **strategic anchor (the *moat*).** Why Tesote AI beats Claude/ChatGPT + a generic Odoo MCP. Seven patterns to steal from Harvey + Legora, mapped onto the existing 12-jobs taxonomy. Read this before the rollout plan or investor framing.
- [[harvey-legora-teardown]] — companion to the above. Stub: focused look at Harvey + Legora's actual products to validate the seven patterns. Fill in before any narrative locks.
- [[positioning-the-finance-chief]] — **positioning anchor (the *why*).** Tesote AI = the LATAM finance chief, not a copilot. Proactive, opinionated, SENIAT-fluent, never sleeps. Use to set posture.
- [[pitch-today-v2]] — **the operational pitch playbook (the *what to say next week*).** Launch-narrow rebuild (2026-06-05) against the live capability audit: rules-engine reframe ("the AI builds the machine, the engine does the mass work"), three verified pillars, the cut list, dated eng-gate slide, revised 15-min demo.
- [[pitch-today]] — v1 of the playbook (superseded 2026-06-05). Demo mechanics + objection bank still mostly valid; the scope claims are not — read v2 first.
- [[pitch-agents-plus-ai]] — **the deep capability tour (the *catalog*).** Two-layer frame (Agents + AI) + by-function walkthrough + the "install today" test + function-by-function readiness table. Reads better after [[positioning-the-finance-chief]] sets the posture.
- [[launch-day-one-prd-v2]] — **the day-one product definition (all users, all workspaces) — query-anything premise.** Assumes the 100-tx limit dies pre-launch: free-form Q&A becomes Pillar 1, the scope line ("sobre 1.432 movimientos, ene–may…") becomes the trust signature, refusal table shrinks to genuine scope edges, chat-to-report + question-to-rule conversion loops. Security/permissions assumed owned by Dan/Sebastián. Leads the launch-doc family.
- [[launch-day-one-prd]] — v1 of the above (launch-narrow premise: free-form totals refused, everything routed through saved reports + rules). Superseded same-day by the premise change; **stays on file as the fallback plan** if the queries-at-scale gate slips.
- [[launch-contract-2026-06-05]] — **the organizing frame: 7 behaviors the AI must get right at launch** (stays up / large queries with visible logic / hard currency boundaries / kill the 100-tx limit / reports right + format choice / preview-pane before every action / European formatting). Every bug derives from one; leads the eng comms.
- [[launch-readiness-plain-2026-06-05]] — **the decision copy of the bug register.** Same issues in plain language: what the user experiences, why each gates (or doesn't gate) the all-users launch, scoreboard with verdicts for Luis to approve/override. Read this one; eng/agents read the register.
- [[bug-register]] — **consolidated bug & limitation register.** Everything reported 2026-05-12 → 06-03 merged from 7 sources, deduped, **split by surface**: Part 1 = day-one (chat platform + tesote-workspace tools, gates the all-users rollout — ~10 mostly-small items), Part 2 = Odoo connector (wave 2, manual-install only — incl. the whole Bs/USD class). Feeds the eng comms.
- [[capability-audit-2026-06-03]] — **live-verified ground truth.** Every MCP resource probed against prod (2026-06-03): what works, new defects (cash_flow date bug, envelope mismatch), gap-list scorecard (~70% of recon blockers cleared), taxonomy→reality map, surfacing calls. Read this before any customer demo or gallery decision.
- [[tesote-workspace-mcp-feedback]] — gaps in the `tesote-workspace` MCP that block the killer demos. Punch list for what to ship next. Scorecard as of 2026-06-03 lives in [[capability-audit-2026-06-03]].
- [[pricing]] — SKU pricing thinking: $1.5k Workspace / $1.5k Odoo / $2.5k bundle (starter tier), 80% margin target, soft overage for first 6-12 months. Draft — revisit after 30-60d of Mariel usage data.
- [[feature-requests]] — running list of chat-surface UX / capability requests (auto-expand input, OCR, …). Backend tool gaps live in [[tesote-workspace-mcp-feedback]].
- [[use-case-taxonomy]] — **internal taxonomy** of finance workflows by job-to-be-done × execution mode (autopilot / draft-approve / scheduled / on-demand chat). The "what to build next" map. Most of it is Automations work, not chat. Draft 2026-05-22. Companion mockup: `use-case-taxonomy-v0.1.html` (open locally — Lunour + Inter + Instrument Serif, 12 jobs as 4-mode grids).

## Related

- [[../automations/erp-ai/flagship-workflows]] — the 6 flagship agentic workflows with deep choreography
- [[../automations/erp-ai/odoo-mcp]] — the MCP / chat surface strategy
- [[../tesote-2026-command-center-prd]] — the architecture this surface plugs into
