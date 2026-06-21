---
title: Tier Numbering Convention — Position for Eng Convo
tags: [ops, conventions, eng]
updated: 2026-05-16
status: draft
---

# Tier Numbering Convention

**My position for when I raise this with eng:** Tier 1 should be the **top** tier (strategic / anchor accounts), not the bottom. Eng currently has it inverted.

## Context

Eng team recently decided Tesote would use inverted tier numbering — Tier 1 = bottom (long-tail / smallest), higher numbers = more strategic. I have personal friction with this every time I look at it. Asked Claude for an independent take regardless of my or eng's opinion.

## Why Tier 1 should be top

1. **External gravity.** Every CS playbook, Gartner report, sales book, peer-company doc, and exec hire uses Tier 1 = strategic. Inverting creates a permanent translation tax on every new hire, board deck, investor convo, and benchmark we read. We'd be the only company in the room speaking backwards.

2. **Linguistic load.** "Tier 1" naturally connotes primary / first / most important — Tier 1 city, Tier 1 capital, Tier 1 university, Tier 1 investor, Tier 1 VC. The brain doesn't fight that mapping. It fights the inverted one — I'm proof of that.

3. **Where eng's instinct came from.** Tier 1 = bottom is the **support-tiering** convention (Tier 1 = front-line, Tier 2/3 = escalation specialists). Real and valid pattern — but it applies to *workflow escalation*, not *strategic ranking of entities*. Eng probably imported it from muscle memory without noticing the domain switch. For customer tiering specifically, the support analogy doesn't hold.

4. **CEO friction is signal.** If I have to do mental gymnastics every time I look at it, every exec hire, board member, and future CS lead will too. The convention should minimize cognitive load on the highest-leverage readers, not the implementer.

## The compromise that would also work

If eng has a real code/DB reason for ascending = more strategic (e.g., a numeric weight where higher = more important sorts naturally), keep that **in code**. Call the column `tier_weight` or `strategic_score`, not `tier`. The **human-facing label** — dashboards, CS plays, exec reports, sales conversations — should be Tier 1 = top. Don't leak an internal sort order into the business vocabulary.

## What to do

- Raise with eng (Dan / whoever owns the call) before the convention calcifies further
- The longer it sits in production code/docs, the more expensive the flip
- Frame as: "I want to confirm we're aligned on business-facing language even if the underlying data model stays as-is"

## Open questions for the convo

- How widely has the inverted convention already been used? (DB schemas, dashboards, internal docs, customer-facing surfaces?)
- Is there a specific reason eng went inverted, or was it muscle-memory from support tiering?
- If we flip, what's the migration cost?
