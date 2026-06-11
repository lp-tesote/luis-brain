---
name: team-calls
description: Build Luis's weekly team-call digest — pull the week's meetings from Roam (Luis's internal calls) + Fireflies (org-wide, all team calls) and write a scannable rollup to luis-brain/daily/team-calls-week-of-YYYY-MM-DD.md. Use when Luis says "team calls digest", "what did the team talk about this week", "weekly call rollup", or when the Friday EOW routine fires.
argument-hint: optional explicit window, e.g. "2026-06-08..2026-06-12" (defaults to current Mon–Fri)
---

Build a weekly digest of every call the team had, from two sources, into one scannable file in luis-brain.

## Step 1 — Resolve the window

- Default window: the current week, **Monday 00:00 → Friday 23:59** in `America/Caracas` (the business tz; Roam timestamps come back `-04:00`).
- **Compute `<MONDAY>`/`<FRIDAY>` with a shell command — do NOT hand-calculate the weekday (mental date math is error-prone and has produced off-by-one Mondays).** Run via Bash, set `TZ=America/Caracas`:
  ```sh
  export TZ=America/Caracas
  DOW=$(date +%u)                                   # 1=Mon .. 7=Sun
  MONDAY=$(date -d "-$((DOW-1)) days" +%F 2>/dev/null) \
    || MONDAY=$(date -v-$((DOW-1))d +%F)            # GNU first, BSD/macOS fallback
  FRIDAY=$(date -d "$MONDAY +4 days" +%F 2>/dev/null) \
    || FRIDAY=$(date -j -v+4d -f %F "$MONDAY" +%F)
  echo "MONDAY=$MONDAY ($(date -d "$MONDAY" +%A 2>/dev/null || date -j -f %F "$MONDAY" +%A)) FRIDAY=$FRIDAY"
  ```
  **Assert the echo prints `Monday`** before continuing. If it doesn't, stop and fix — a wrong Monday silently drops a day of calls.
- If `$ARGUMENTS` gives an explicit range (`YYYY-MM-DD..YYYY-MM-DD`), use that instead; the file's `week-of` date is the range start.
- Target file: `~/Programming/tesote/luis-brain/daily/team-calls-week-of-<MONDAY>.md` (absolute path).

## Step 2 — Pull Roam (Luis's internal calls)

Use Roam's **`meeting_list`** tool (tool id is `mcp__claude_ai_roam__meeting_list` in a local session, `mcp__roam__meeting_list` in a cloud routine — match whichever prefix is present) with:
- `after` = `<MONDAY>T00:00:00-04:00`, `before` = `<FRIDAY>T23:59:59-04:00`
- `expand` = `"summary,actionItems"`
- `limit` = 25, then page with `nextCursor` until meetings fall before the window.

This token is **personal** — it returns only meetings Luis attended. Capture per meeting: `id`, `title`, `start`, `participantCount`, `summary`, and `actionItems` (note any with `assignedToMe: true` or `suggestedForMe: true`).

## Step 3 — Pull Fireflies (org-wide, all team calls)

Luis is a Fireflies **admin**, so an unfiltered query returns every team member's calls.

Use Fireflies' **`get_transcripts`** tool (tool id is `mcp__claude_ai_Fireflies__fireflies_get_transcripts` locally, `mcp__Fireflies__fireflies_get_transcripts` in a cloud routine — match whichever prefix is present) with:
- `fromDate` = `<MONDAY>`, `toDate` = `<FRIDAY>`
- `format` = `"toon"`, `limit` = 50
- **Do NOT set `mine` or `participants`** — we want the whole org.
- Page with `skip` if 50 are returned.

**Volume warning:** this response is heavy (inline `short_summary` + `action_items` per call). If the tool result overflows and gets saved to a file, read that file in chunks / use `jq`; do not re-request. Capture per call: `title`, `dateString`, `duration`, `organizer_email`, `summary.short_summary`, `summary.action_items`, `meeting_link`.

## Step 4 — Merge + dedupe

- A call may appear in both sources (rare — only if Fireflies joined a Roam call). Dedupe by matching title + start time within ~5 min; prefer the Roam record (richer action-item assignment).
- Group calls by **workstream/theme** (e.g. Product/AI launch, Banking migration, Finance/fundraising, Sales pipeline, Legal, CX/ops). Infer theme from title + summary. Within a theme, order by date.

## Step 5 — Write the digest

Frontmatter:

```yaml
---
title: Team calls — week of <MONDAY>
tags: [team-calls, weekly-digest, fireflies, roam]
updated: <TODAY>
window: <MONDAY> .. <FRIDAY>
---
```

Then, in this order:

1. **`## Needs Luis's attention`** — action items assigned to or suggested for Luis (Roam `assignedToMe`/`suggestedForMe`; Fireflies `action_items` naming Luis). One line each: `- [ ] <item> — from "<call title>" (<date>)`. If none, say so.
2. **`## By workstream`** — one `###` per theme. Under each, one block per call:
   ```
   - **<title>** — <date>, <participants/organizer>, <duration if known>
     <2–4 line tight summary — decisions + notable action items, not a transcript replay>
   ```
3. **`## Coverage`** — a short honest note: "Roam = Luis's calls only (no org token). Fireflies = org-wide (admin). Gap: purely-internal Roam syncs between teammates Luis wasn't in are not captured." Plus counts: N Roam calls, M Fireflies calls, K deduped.

## Step 6 — Style

- Terse, decision-oriented, scannable — brain voice, not KB polish (see CLAUDE.md).
- Spanish-source calls: summarize in English (internal-docs-in-English convention) unless the call was client-facing.
- Absolute dates always. `[[wiki-links]]` only for luis-brain docs; plain text for names/IDs.
- This is reference-flavored but lives in `daily/`; keep it skimmable in under a minute.

## Step 7 — Confirm

Tell Luis: file path written, # calls by source, and the count of items in "Needs Luis's attention".
