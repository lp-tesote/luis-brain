---
title: Tesote AI — consolidated bug & limitation register
tags: [product, ai, bugs, qa, launch]
updated: 2026-06-05
status: draft
audience: Luis → basis for the product/eng comms doc; single source of truth for everything reported 2026-05-12 onward (per-item dates in Evidence)
---

# Tesote AI — consolidated bug & limitation register

> **Job of this doc.** Every bug/limitation reported in the last weeks, aggregated from 7 scattered sources, deduped, **split by surface** — because the surfaces have different rollout exposure. Feeds the eng comms doc for the all-users rollout ([[pitch-today-v2]] launch-narrow context).
>
> **Sources merged:** [[../automations/erp-ai/odoo-ai-recon-and-fixes-2026-05]] (05-25 Mariel session + Dan's PR #7154) · daily 2026-05-26 (ENG-4016) · [[feature-requests]] (05-20) · [[tesote-workspace-mcp-feedback]] (05-12) · [[capability-audit-2026-06-03]] · [[qa-pre-created-reports-2026-06-03]] · daily 2026-06-03 (Mariel dogfood, Slack [#feat-ai-workspace post](https://tesote.slack.com/archives/C0B4X86B5R9/p1780514320076159)).

---

## The rollout reality that orders this doc

**At launch, 100% of users are on the Tesote-workspace-only AI.** The Odoo connector requires a manual install — it is not native, and nobody gets it by default. So:

- **Part 1 (chat platform + tesote-workspace tools) = the launch gate.** Every user hits these from day one.
- **Part 2 (Odoo connector) = wave 2.** Only manually-installed workspaces (today: Mariel/dogfood + the AI+Odoo deals). Matters enormously for the deeper sell — but it does not gate the all-users rollout.

**The headline this split reveals:** the scariest bug class — Bs/USD 1:1, rate truncation, silent rate overrides, the whole Avanti/Cenco Zotti family — lives **entirely on the Odoo side**. Day-one users can't hit it. The day-one gate is mostly *small server fixes to the read/report surface* plus two stability bugs. That makes "fix these → successful launch" a genuinely achievable claim.

Class tags carried per item: 🔴 silent wrong answer · 🛑 availability · 🟠 incomplete flow · 🟡 capability gap.

---

# Part 1 — Day-one surface (gates the all-users rollout)

## 1A. Platform / chat surface (every user, every conversation)

| # | Class | Item | Evidence | Status | Ticket |
|---|---|---|---|---|---|
| P1 | 🛑 | **SEV-HIGH: a <100-record report query took the whole app down** — long "thinking," claimed done with no output, then app unreachable on both machines incl. main page. Looks server-side. (Trigger was an Odoo AP query, but the failure is platform — any heavy agent query could do it) | 06-03 Mariel dogfood, conv `…CDDC` era | **Open — UNFILED** | file first |
| P2 | 🛑 | **Token expiry breaks action confirmation** — recoverable on reads, fatal mid-confirmation of an execution. Persists despite #7154-era fixes; verify whether auto-compact-at-60% shipped | 06-03 dogfood, conv `…CDDC` | **Open — UNFILED** | file first |
| P3 | 🔴 | **Mixed Bs+USD in one table column, no currency anchor** — 5,445,475 next to 870 in the same `total` column. #7154's `Intl.NumberFormat` fixed *formatting*, not the missing per-row currency | feature-requests B1, working file `f3e99811` | Open | **PRO-154** |
| P4 | 🟡 | Composer textarea doesn't auto-expand | feature-requests #1 | Open | **PRO-155** |
| P5 | 🟠 | **Conversation leaves things hanging** — tasks/threads started but not closed out mid-conversation | 06-05, conv `b3c6d51f-88ca-45d1-b208-61e386ffe757` | **Open — UNFILED** | file first |

## 1B. Tesote-workspace tools — the "honest reads" cluster 🔴

The silent-wrong-answer class on the day-one surface. These all produce confident, plausible, wrong numbers — the single thing that kills a finance AI's trust at scale.

| # | Item | Evidence | Status | Ticket |
|---|---|---|---|---|
| W1 | **`transaction.search` 100-row hard cap, pagination half-built** — envelope advertises `next_cursor` but input schema has no cursor param. "84% categorizado" computed off 14–22 May only, no caveat | Daily 05-26 live conv; reconfirmed audit 06-03 | **Open.** #7238 added agent-side guardrail — but see W2: the envelope never arrives on the chat path | **ENG-4016** (Medium — per its own description, jumps to High before widening rollout. **We are widening. Re-rank now.**) |
| W2 | **`transaction.search` envelope missing on `manage_resource` path** — bare 100-row array instead of `{items, returned, total, has_more}`. The #7238 guardrail can't fire if `has_more` never arrives. W1+W2 are one fix | Audit 06-03 §3.3 | Open | unfiled |
| W3 | **`report.run` `group_by: "category"` silently ignored** — ungrouped output, no error. Generalize: *unknown params must error, never no-op* | QA 06-03, conv `71ec2c5d` | Open | unfiled |
| W4 | **`cash_flow.statement` silently ignores dates unless `preset: "custom"`** — asked May, got trailing-30d. Wrong numbers, no warning | Audit 06-03 §3.2 | Open | unfiled |
| W5 | **`bank_connection.status` → `last_synced_at: null`** on all VE webscraper connections while data demonstrably flows — AI can't honestly answer "¿están al día mis bancos?" (a guaranteed day-one question) | Audit 06-03 §3.4 | Open | unfiled |

## 1C. Tesote-workspace tools — the reports pillar 🟡

What blocks the "run + narrate reports" leg of the launch pitch.

| # | Item | Evidence | Status | Ticket |
|---|---|---|---|---|
| W6 | **`cash_flow_by_category` report type doesn't exist** — category cash flow structurally impossible today; every path verified blocked. Cheapest fix: mirror `cash_flow_by_counterparty` 1:1 (grouped shape already exists server-side) | QA 06-03, convs `5a192f50`/`f9003145`/`71ec2c5d` | Open — ranked #1 in QA fix spec | unfiled |
| W7 | **Report definitions: zero seeding, zero adoption** — `report_definitions` empty all-time (treasury WORKLOG #7242); agent can only run what `list_definitions` returns. "Pre-created reports" promise is hollow without seeded defaults per workspace | QA 06-03 + WORKLOG | Open — product call | unfiled |
| W8 | **Mixed-currency ergonomics** — `report.run` w/o `account_ids` always errors on multi-currency workspaces; error names the problem, not the next step | QA + audit 06-03 | Open | unfiled |
| W9 | **Period preset trap** — `last_month` rejected; enum undocumented in tool description | QA 06-03 | Open | unfiled |
| W10 | **`cash_flow.statement` real filters undocumented** — `list_resources` advertises `filters: []` | Audit 06-03 §3.1 | Open | unfiled |

## 1D. Workspace — product decisions & enablers

| # | Class | Item | Status |
|---|---|---|---|
| W11 | 🟠 | **`inbox.*` wired but `enabled: false`, zero exercised** — AP-ingestion flagship switched off. Product decision: who flips it, for which workspaces | Open — Luis/product call |
| W12 | 🟡 | **No seeded sandbox workspace** — exercising invoice/inbox/subscription flows means mutating Tesote Finance prod. Blocks QA *and* sales demos for everything above | Open |
| W13 | 🟡 | **internal-ops MCP has no `ai_conversation` resource** — can't pull transcripts to triage; slows the bug-reporting loop itself | Open |

---

# Part 2 — Odoo connector (wave 2: manual-install workspaces only)

Doesn't gate the all-users launch. Gates the AI+Odoo deals (Oriand, the dogfood cohort) and the deeper 2026 sell.

## 2A. The Bs/USD bug class 🔴 — structural fix designed, blocked on Luis

| # | Item | Evidence | Status |
|---|---|---|---|
| O1 | **Silent Odoo rate override at post-time** — user supplied 550, Odoo applied BCV 385.272; AI presented draft as final | Mining #3 (PR #7154) | Gated-actions fix designed (required `rate`+`rate_source` args — "the signature is the forcing function"). **Held on Mariel's collection-flow taxonomy §5 walkthrough — Luis's to unblock, not eng's** |
| O2 | **`currency_id` mis-derivation / Bs-USD 1:1** — Avanti credit note: USD amount in Bs field; "USD 15,000" → `currency_id: VEF` | 05-25 session + mining #4 | Same fix, same blocker |
| O3 | **BCV rate truncation 4→2 decimals** (+ unconfirmed compra/venta confusion) — proposed total ≠ what Odoo posts | 05-25 Cenco Zotti | Open; rate-source verification still pending |
| O4 | **Recon match with no amount sanity floor** — Bs 326,443 BSL matched to Bs 773 invoice on partner alone | Mining #5 | Open (prompt rules may cover; unverified) |
| O5 | **`apply_rate_to_usd_invoice` overwrites `price_unit` instead of `conversion_rate`** — shape_hints itself warns models off it. Fix or retire | Audit 06-03 §3.5 | Open — unfiled |

## 2B. AP flow completion 🟠 — Mariel-validated, currently dead-ends

| # | Item | Evidence | Status |
|---|---|---|---|
| O6 | **`action_create_retention` not mapped** — VE localization custom action absent from connector allowed-list. Comprobante ISLR *reduces the payable*; AP flow is incomplete without it. Biggest AP unblock per Mariel | 06-03 dogfood (Net1/Netuno otherwise clean e2e) | **Open — UNFILED** |
| O7 | **Comprobante delivery must ride Tesote email, not Odoo/Outlook** — ~200/day cap breaks quincenal mass emission. Infra requirement: design in, don't bolt on | 06-03 dogfood | Open — unfiled |
| O8 | **Fecha contable: ask, don't default** — AI defaulted to emission date; correct answer depends on period state | 06-03 dogfood | Open — prompt/flow fix |
| O9 | **Credit-note flow over-decomposed** — "duplicate + mark NC + post" should be one tool call | 05-25 (Mariel) | Open — "simple action" candidate |

## 2C. Connector plumbing 🟡

| # | Item | Evidence | Status |
|---|---|---|---|
| O10 | **BSL ↔ Tesote tx link still string-parsed** — `TESOTE-{uuid}` buried in narration HTML; `tesote_transaction_id` → Invalid field. Last blocker of the e2e recon demo | mcp-feedback #3, reconfirmed audit | Open |
| O11 | **Field-name guessing loops** — 8+ calls cycling `x_studio_…` variants; root of token exhaustion | Mining #1 | Partially addressed (shape_hints now ✅★); P2 shows exhaustion still bites |
| O12 | **`kanban_dashboard` JSON not typed fields** — reconcile counts/balances in a string blob | mcp-feedback #4 | Open |
| O13 | **Dry-run mutations blocked on read-only tokens** — kills prospect-trial demos | mcp-feedback #2 | Unverified (untestable with write-scope token) |

---

## Fixed / verify-then-close ✅

| Item | Fixed by | Verify |
|---|---|---|
| BSL enumeration (was the #1 gap) | generic `erp_console.read` | ✅ verified in audit |
| `stats` / `recent_audits` empty; `fields` selector | — | ✅ verified in audit |
| Conversation IDs in UI + Sentry breadcrumbs | PR #7154 | ✅ paying off (QA used them) |
| Hand-formatted money (8/8 convs) | #7154 `Intl.NumberFormat` | ✅ shipped; per-row currency gap remains (P3) |
| OCR for scanned PDFs (**PRO-156**) | #7286/#7288 — rasterize to vision | ⚠️ verify, then close PRO-156 |
| Confident-totals guardrail (agent side) | #7238 | ⚠️ partial — can't fire on chat path until W2 ships |
| Manual tx creation not whitelisted | #7240 | ✅ per treasury log |

---

## Roll-up for the comms doc

**Day-one gate (Part 1) — what "successful launch" actually requires:**

1. **File + fix the two stability bugs** (P1 outage, P2 token-expiry-mid-confirmation) — both currently unfiled; sev-high
2. **The "honest reads" PR** (W1–W5) — one cluster of small server fixes that kills the silent-wrong-answer class on the day-one surface. Re-rank ENG-4016 to High (its own description says so once we widen — we're widening)
3. **The reports pillar** (W6 `cash_flow_by_category` + W7 seeding + W8–W10 ergonomics) — unblocks the second leg of the launch pitch
4. **Enablers** (W12 sandbox, W13 triage resource) + product calls (W11 inbox — Luis)

That's it. ~10 mostly-small items between today and an honest all-users launch.

**Wave 2 (Part 2) — ordered:** Luis unblocks Mariel taxonomy §5 → gated actions ship (O1–O4) → `action_create_retention` mapping (O6) + Tesote email rail (O7) → plumbing (O10+).

**Luis-blocked, not eng-blocked:** Mariel taxonomy walkthrough (gates the whole 2A class) · inbox enablement decision (W11).

## Cross-links

- [[pitch-today-v2]] — the launch-narrow pitch this register de-risks; its "eng gate" ≈ 1B + W6/W7
- [[capability-audit-2026-06-03]] · [[qa-pre-created-reports-2026-06-03]] · [[../automations/erp-ai/odoo-ai-recon-and-fixes-2026-05]] · [[tesote-workspace-mcp-feedback]] · [[feature-requests]] — merged sources (this register supersedes their punch lists for tracking; they keep the deep repro detail)
