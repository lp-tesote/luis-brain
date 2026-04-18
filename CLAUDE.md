# CLAUDE.md — Luis's Brain

This is Luis Pulgar's **personal knowledge base** — not a team resource.

## Who is Luis

- CEO of Tesote (B2B SaaS / fintech, LATAM — Venezuela-focused, expanding)
- Email: luis@tesote.com
- 2026 goal: **10x revenue**
- Relies on Claude to move faster across strategy, sales, product, marketing, CX, legal, finance, ops

## What this repo is

Luis's private brain. It holds:

- Raw, unfiltered thinking before ideas are ready for the team
- Drafts, half-formed takes, decisions-in-progress
- Notes on people (team, investors, clients) that aren't for public consumption
- Daily session logs, learnings, scratch work

**It is NOT a company resource.** The shared team KB lives separately at `~/Programming/tesote/knowledge-base/` (pushes to `github.com/tesote/knowledge-base`).

## Relationship to the shared KB

Content flows **one-way, selectively**: `luis-brain/` → `knowledge-base/`.

- Draft and think here freely — no audience concerns, no formatting pressure
- When a doc matures and is ready for the team, **copy** the file into the matching folder in `knowledge-base/`, commit, push
- Function folders here (`sales/`, `product/`, `finance/`, etc.) intentionally mirror the KB's structure so promotion is zero-friction
- Never symlink or auto-sync — the manual copy is a feature (forces "is this ready to share?" decisions)

## Structure

```
── how I think (process / time) ──
daily/                 — daily notes, session logs, what I'm chewing on today
decisions/             — decisions I've made + why (before they're team-wide)
people/                — raw notes on team, investors, clients, advisors
drafts/                — half-formed ideas, not ready for a function folder yet
learnings/             — skills I'm building (Claude Code, fundraising, engineering, etc.)
.scratch/              — ephemeral, disposable, auto-generated

── what I think about (functions — mirror the KB) ──
strategy/              — 10x thesis, OKRs, bets, competitive positioning
sales/                 — pipeline thinking, client-specific raw notes, playbook drafts
product/               — ideas and explorations before they're specs
marketing/             — positioning, narrative experiments, channel tests
customer-experience/   — CX observations, onboarding patterns, support signals
legal/                 — contracts, compliance thinking, risk
finance/               — runway, pricing, unit economics, fundraising
ops/                   — team, hiring, process, cycles
```

## Conventions

- Markdown with Foam-style `[[wiki-links]]` to connect docs
- `kebab-case.md` file naming
- Every folder has an `index.md` describing what's in it
- Tags inline: `#strategy`, `#sales`, `#10x`
- Absolute dates always (e.g., `2026-04-18`), never relative ("last week")
- Frontmatter when useful:

```yaml
---
title: Doc Title
tags: [strategy, 10x]
updated: 2026-04-18
status: draft | ready-for-kb | promoted
---
```

- `status: promoted` means a version of this doc has been copied to the shared KB — stop editing here and edit there.

## Writing guidelines (different from the KB)

The shared KB demands polish because the team reads it. The brain does not:

- Write fast, write raw — messy thinking is fine, that's the point
- First-person is fine ("I think...", "my gut says...")
- Opinions, hunches, half-baked takes all welcome
- Don't self-censor for audience — there is no audience except future-Luis and Claude
- When something's worth keeping in polished form, **promote it to the KB** rather than cleaning it up in place

## For Claude specifically

When working in this repo:

- Frame responses for Luis as CEO — strategic, decision-oriented, time-constrained
- Default to terse; Luis can ask for depth
- Connect cross-functional implications (a pricing idea touches finance + sales + product)
- When Luis is drafting something that could become a team doc, flag it: "this looks ready to promote to the KB"
- Scratch/session logs go in `.scratch/` or `daily/`, not in function folders
- This is *thinking* space, not *reference* space — be okay with ambiguity
