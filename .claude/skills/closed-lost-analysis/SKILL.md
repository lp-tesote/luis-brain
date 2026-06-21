---
name: closed-lost-analysis
description: Run a forensic closed-lost deal analysis — HubSpot recon → Luis picks deals → per-deal evidence packs (HubSpot engagements + Fireflies + email) → pattern synthesis → share to #sales/Notion. Use when Luis asks to analyze lost deals, do a loss post-mortem, or "run the closed-lost analysis" (he wants this recurring). First run: 2026-06-05 (sales/closed-lost-analysis-2026-06.md).
---

# Closed-Lost Analysis

Forensic post-mortem of closed-lost deals. Core principle: **evidence over CRM labels** — `lost_reason` says "Timing/Budget", the transcripts say what actually happened. Read `sales/closed-lost-analysis-2026-06.md` for the reference output and the standing findings (repricing, absent decision-makers, one-shot proposals, headcount/ENIAC) — new runs should check whether those patterns persist or moved.

## Phase 0 — Recon (HubSpot)

1. Pipeline = "Sales Pipeline [NEW]" (`156377365`). Key stage IDs: Proposal Sent `263081761`, Negotiation `263081764`, Closed Lost `263081766`.
2. Query closed-lost deals that reached proposal+: `search_crm_objects` on `deals`, two OR filterGroups (dealstage EQ closed-lost AND pipeline AND `HAS_PROPERTY hs_v2_date_entered_263081761` / `..._263081764`), sort `closedate` DESC.
3. Properties: `dealname, amount, deal_currency_code, closedate, lost_reason, detailed_loss_reason, hubspot_owner_id, hs_v2_date_entered_*, num_associated_contacts`.
4. Beware: **close dates are cleanup dates, not death dates** (bulk-close sweeps happen). Evidence windows run createdate → closedate + buffer.
5. Show Luis the candidate table (deal, $, date, stated reason, detail) and **let him pick the set** — don't auto-select. Recommend weighting by $ value + failure-mode coverage over "literal last N".

## Phase 1 — Evidence packs (per deal, batched in parallel)

Permissions: read-only tools for HubSpot/Gmail/Fireflies are already allowlisted in `.claude/settings.local.json` — this phase runs prompt-free. If subagents hit API 529s, run inline instead (worked fine on run 1).

Per deal, in batch across all deals:
1. **Contacts**: `search_crm_objects` contacts `associatedWith` the deal → names/emails (join keys). Some deals have 0 contacts — fall back to company-name search.
2. **Notes**: objectType `notes` associatedWith deal (Fireflies sometimes syncs meeting summaries here).
3. **Fireflies**: `fireflies_search` with `keyword:"<company>" scope:all from:<created> to:<closed+buffer>`. Summaries first; pull full transcript (`fireflies_get_transcript`) only for decisive meetings (final calls, proposal calls, competitor mentions).
4. **Emails**: `search_crm_objects` objectType `emails` associatedWith deal — this captures the reps' threads (Luis's Gmail won't have them). Proposal emails contain the actual economics.
5. **Calls**: same pattern — historically empty (WhatsApp is unlogged; flag this gap per deal).

## Phase 2 — Per-deal rubric

Same questions for every deal so patterns are comparable:
- Timeline of touches (dated, who initiated, source IDs)
- Where momentum actually died (last meaningful prospect touch vs official close)
- Stated vs **inferred** loss reason, with verbatim quotes + citations
- Champion: real or polite contact? single/multi-threaded? did the decision-maker ever meet us?
- Objections + how handled; competitor/status-quo mentions (ask: vs headcount? vs ENIAC/other?)
- Our execution: latency, proposal→decision gap, proposal versions sent (v2 ever?)
- Coverage rating (solid/partial/speculative) — **state evidence gaps explicitly**, esp. WhatsApp-dark endgames
- Max 3 could-have-dones, grounded in evidence

## Phase 3 — Synthesis + output

- One doc: `sales/closed-lost-analysis-YYYY-MM.md` — scoreboard table, 3–5 cross-deal findings (not 15), immediate actions, coverage caveats, then per-deal post-mortems appended. Frontmatter per brain conventions, `status: draft`.
- Frame findings as **process patterns, never rep performance** — this gets shared with the team.
- Flag re-engagement candidates with dates ("revisit in June" = calendar item).
- Compare against prior runs' findings — that's the whole point of recurring.

## Phase 4 — Share (only on Luis's explicit ask)

- Slack: #sales = `C05HT92FRMK`. Luis drafts/approves the message; show draft before sending. Slack tools can't upload files.
- Notion: create page under **"Sales (Closed Lost)"** (`3251ee04-eee1-808b-96b1-d967ee74d6ff`), post link in the Slack thread.
- PDF if asked: md → HTML (marked.js CDN) → Chrome headless `--print-to-pdf` (no pandoc on this machine).
- Update memory `project_closed_lost_analysis_*` + MEMORY.md index with run pointer + new competitor names.

## Known traps (from run 1)

- Fireflies recordings sometimes capture **internal Tesote talk after the client leaves** — check long transcripts before citing/sharing.
- Loss-reason fields are populated but soft ("Timing" ≈ price/value failure ~80% of the time).
- The decisive last 2–6 weeks of most deals lives in WhatsApp = invisible; say so rather than over-concluding.
