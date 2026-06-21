---
title: Tesote AI — launch readiness, in plain words
tags: [product, ai, bugs, launch, decision]
updated: 2026-06-05
status: draft
audience: Luis — the decision copy. Each issue explained as what the user experiences, why it's critical pre-launch, and what the fix is. Approve/override the verdicts here; the technical version for eng/agents is the register.
---

# Tesote AI — what has to work before every user gets it

> **Companion to [[bug-register]]** — same issues, different layout. That doc is for eng and agents (tool names, repro paths). This one is for the call *you* have to make: which of these gate the launch, and why. IDs (P1, W1…) map back to the register so nothing gets lost in translation.

---

## The thesis in five lines

1. We're rolling Tesote AI out to **every Tesote user**, and 100% of them land on the workspace-only AI (Odoo requires manual install).
2. The product is **trust**. A finance AI that gives one confident wrong number is worse than no AI — the user never asks again, and tells their team why.
3. Almost every issue below is a version of the same failure: **the AI answers wrong without knowing it's wrong** — not because the model is bad, but because our tools feed it partial data without telling it.
4. The fixes are mostly **small server-side changes**. This is not a "delay the launch by a quarter" list.
5. The scary bugs you've seen with Mariel (Bs/USD, rates) are **all on the Odoo side** — day-one users can't hit them. They're wave 2.

---

## The scoreboard — approve or override each verdict

| # | The issue, in one line | My verdict | Your call |
|---|---|---|---|
| P1 | One question can take the whole app down | **BLOCKER** | ☐ |
| P2 | The AI dies in the middle of confirming an action | **BLOCKER** | ☐ |
| W1+W2 | The AI only ever sees the last 100 movements — and doesn't know it | **BLOCKER** | ☐ |
| W3 | Ask for a report grouped by category → get it ungrouped, no warning | **BLOCKER** | ☐ |
| W4 | Ask for May → silently get "last 30 days" instead | **BLOCKER** | ☐ |
| W7 | "Pre-created reports" — the library is empty for every customer | **BLOCKER** (product task, not eng) | ☐ |
| W5 | "¿Están al día mis bancos?" — unanswerable | Strongly recommended | ☐ |
| W6 | Cash flow by category is impossible, on any path | Strongly recommended | ☐ |
| P3 | Tables mix Bs and USD in one column with no way to tell them apart | Strongly recommended | ☐ |
| W8 | Report requests fail outright on multi-currency workspaces | Strongly recommended | ☐ |
| W12 | No safe test workspace — QA and demos touch real books | Strongly recommended | ☐ |
| W9+W10 | The AI has to guess undocumented "magic words" to use the report tools | Recommended | ☐ |
| W13 | We can't pull AI conversations to triage bugs (slows all of the above) | Recommended (internal) | ☐ |
| P4 | Chat input box doesn't grow with long text | Defer — not launch-critical | ☐ |
| W11 | The AP email inbox is built but switched off | **Your decision**, not a bug | ☐ |

Six blockers. Everything else is judgment.

---

## The blockers, one by one

### P1 — One question took Tesote down. The whole app. *(BLOCKER)*

**What happened:** Mariel asked for a small report (<100 records). The AI "thought" for a long time, claimed it finished but showed nothing — and then **Tesote stopped loading entirely, on both machines, including the main page.** This looks server-side: the query consumed something that didn't recover.

**Why this gates launch:** today this hit one dogfood user. After rollout, any of hundreds of users can type a heavy question at any time. If one chat prompt can take the platform down, the AI isn't a feature risk — it's a platform risk. This is the only issue on the list that can hurt users who never even open the AI.

**The fix, plainly:** eng needs to find what that query consumed and put guardrails around it (timeouts, resource limits) so the worst case is "the AI apologizes," never "Tesote is down."

**Status: not yet filed as a ticket.** That's the first action out of this doc.

---

### P2 — The AI dies mid-action. *(BLOCKER)*

**What happened:** conversations still run out of steam (token/context exhaustion). When it happens during a *read*, the AI recovers — annoying but survivable. When it happens **while the user is confirming an execution** (Mariel's case: an adjustment, ready to go, conversation ends), the flow is dead and the user doesn't know if anything happened.

**Why this gates launch:** the entire trust model we pitch is "the AI drafts, you approve, it executes." If the approve step itself can die, the trust model has a hole at its most sensitive point. A user who hits this once will never let the AI touch anything that matters again.

**The fix, plainly:** conversations must never expire while an action is pending confirmation — either the pending action survives the conversation, or the conversation gets compacted before it can die. (Dan had "auto-compact at 60%" on his list — verify whether it shipped; this bug says it didn't, or didn't cover this.)

**Status: not yet filed.**

---

### W1+W2 — The AI only sees the last 100 movements. And it doesn't know. *(BLOCKER)*

**What happened (real conversation, mine):** I asked *"¿qué porcentaje de transacciones están categorizadas en 2026?"* The AI answered **"84% categorizado"** — computed from the last 100 transactions only, which covered May 14–22. Eight days of data, presented as the year. No caveat. When I pushed (*"how do you know you're getting all the movements?"*), it admitted it has no way to ask for more.

**Why this gates launch:** this is the **single most common question type a finance user will ask** — "how much did I spend," "what % is X," "compare this month to last." Any workspace with >100 movements per period (most of them) gets confidently wrong answers on day one. A customer already caught one of these in prod and asked *"¿de dónde estás sacando eso?"* — that question is the sound of trust dying.

**The fix, plainly:** two halves, one fix. (a) Let the AI ask for the next page of results — the plumbing is literally half-built, the response side already supports it. (b) Make sure the "there's more data" signal actually reaches the AI in chat — right now it doesn't, so even the safety rule Dan added ("never total a truncated list") can't trigger.

**Status:** half of it is filed (ENG-4016, Medium) with a note in the ticket itself saying *raise to High when we widen the rollout*. We're widening. **Re-rank it now** — that's a one-line message to Dan citing his own ticket.

---

### W3 — Ask for a grouped report, silently get an ungrouped one. *(BLOCKER)*

**What happened:** the AI asked the report tool to group cash flow by category. The tool **doesn't support that option — but instead of saying so, it ignored it** and returned the ungrouped report. No error. The AI had no way to know the result wasn't what it asked for.

**Why this gates launch:** same family as W1 — wrong numbers without warning — but nastier, because the AI did everything right. You cannot prompt-engineer your way out of a tool that lies by omission. Rule for eng: **a tool that gets an option it doesn't understand must say "I don't understand," never answer as if it did.** Cheap to fix, kills a whole class of future bugs.

---

### W4 — Ask for May, get "the last 30 days" instead. *(BLOCKER)*

**What happened:** asked the cash-flow tool for May 1–31. Unless you also pass one specific extra setting, **it ignores your dates** and returns a default trailing-30-day window (May 5–June 3 that day). Numbers come back plausible and wrong.

**Why this gates launch:** finance lives on calendar periods — "mayo," "el trimestre," "YTD." Every period question routed through this tool silently returns a shifted window. Same trust-killer family; arguably the most likely to be discovered by a real CFO comparing against their own spreadsheet.

**The fix, plainly:** if dates are provided, honor them. One server-side default change.

---

### W7 — We say "pre-created reports." The library is empty. *(BLOCKER — but it's a product task, not an eng bug)*

**What happened:** the AI can only run reports that exist as saved definitions in the workspace. Across **all customers, all time, zero saved definitions exist** (the one in our own workspace was created mid-test, by me). The feature shipped; nobody ever sees it.

**Why this gates launch:** the launch pitch's reports leg is *"the AI runs your reports and explains them."* If a new user's library is empty, the AI has literally nothing to run — the pillar is hollow on first contact, which is exactly when adoption is decided.

**The fix, plainly:** decide the 3–5 default reports every workspace ships with (e.g., monthly cash flow Bs + USD, balances by bank) and seed them. Eng builds the seeding; **someone has to pick the reports — that's us.**

---

## Strongly recommended — would ship before launch if the calendar allows

**W5 — "¿Están al día mis bancos?" is unanswerable.** The sync-freshness field comes back empty for every VE bank connection even when data is flowing. This is a guaranteed first-session question, and "I can't tell" (or worse, "not synced since—") about *their bank data* reads as broken product. Fix: populate the field for scraper connections.

**W6 — Cash flow by category doesn't exist, on any path.** I verified every route the AI could take; all blocked. This is the most natural report request in finance ("¿en qué se me va la plata?"). The cheap fix: the server already has a "cash flow by counterparty" report — build the identical twin for categories. One warning: ~70% of typical volume is uncategorized today, so the report must show the "sin categorizar" bucket loudly, not hide it (ties into the rules/setup pitch — the AI fixes the very gap the report exposes).

**P3 — Tables mix Bs and USD in one column.** A working-file table showed 5,445,475 (clearly Bs) directly above 870 (clearly USD) in the same "total" column, nothing distinguishing them. In a dual-currency country this makes the table meaningless. Fix: every money column carries its currency, or split per-currency tables. (Already filed: PRO-154.)

**W8 — Multi-currency workspaces break naive report requests.** Asking for a report without hand-picking same-currency accounts errors out — and almost every VE workspace is multi-currency. Seeded definitions (W7) mostly route around it; still worth fixing the error to *tell the AI what to do next* instead of just failing.

**W12 — No sandbox.** Today, testing or demoing invoice/inbox flows means mutating our real books. Blocks safe QA of everything above *and* blocks sales demos. Fix: one seeded demo workspace.

---

## Recommended / defer

- **W9+W10 — undocumented magic words.** The report tools reject natural inputs ("last_month") and hide their real options from the AI's view of them. Each one causes a failed first attempt the user watches. Small documentation/aliasing fixes.
- **W13 — we can't pull AI conversations for triage** (internal tooling). Made this QA slower than it should be; will matter more post-launch when volume grows.
- **P4 — chat box doesn't grow with long text.** Real annoyance, not launch-gating. Already filed (PRO-155).

---

## Your decisions (not bugs)

1. **W11 — the AP inbox is built and switched off.** Email-a-bill-in, AI drafts it — wired end to end, `enabled: false`, never exercised. Flipping it on is a product decision (which workspaces, what support load). Not launch-gating, but it's the highest-leverage switch sitting idle.
2. **The Mariel walkthrough (wave 2, but yours).** The entire Odoo Bs/USD bug class has a designed fix (Dan's gated actions) that has been **waiting since 05-25 on a 30-minute sitting with Mariel** (collection-flow taxonomy §5). Doesn't gate this launch — but it's the longest-pole item for the AI+Odoo deals, and it's blocked on your calendar, not eng's.

---

## What wave 2 (Odoo) looks like, in one paragraph

Everything Mariel hit — USD amounts landing in Bs fields, BCV rate truncated, Odoo silently swapping the rate at post-time, the missing comprobante de retención step, email sending capped by Outlook — lives on the Odoo connector, which **no day-one user has**. The structural fix for the money bugs is designed and blocked on the walkthrough above; the AP-flow completion (retention action + Tesote-owned email) is the next biggest piece. Full detail: [[bug-register]] Part 2.

---

## If you approve the verdicts as-is, the eng ask becomes

1. File P1 + P2 today (sev-high, currently unfiled)
2. Re-rank ENG-4016 to High; bundle W1–W5 as one "honest reads" work-cluster
3. Build `cash_flow_by_category` (W6) + the seeding mechanism (W7) — we owe the default report list
4. P3, W8, W12 as the second batch
5. Wave 2 starts when Mariel's walkthrough happens (yours to schedule)
