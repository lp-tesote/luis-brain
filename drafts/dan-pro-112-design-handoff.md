---
title: Draft message to Dan — PRO-112 design handoff (Lunour reconciliation)
tags: [drafts, dan, pro-112, design]
updated: 2026-05-03
status: draft
---

# Draft — Linear comment on PRO-112

> Paste target: Linear PRO-112. Tone: peer/collaborative. Length kept short on purpose.
> Companion files Dan needs read access to before this lands:
> - `knowledge-base/design.md` (will be updated with the same Product UI extension once we promote from `luis-brain`)
> - `luis-brain/product/design/workspace-design-decisions.md` (the punch list — currently brain-only; promote once Dan signs off on the approach)

---

Hey Dan — picking up your design-spec question.

**TL;DR.** We have a brand source of truth (`design.md`, distilled from Lunour's brand book) and a fresh punch list of where the PRO-112 prototypes diverge from it. Both are linked below. The prototypes you've been reviewing are visually close to Mercury, but **Mercury was layout/density inspiration, not a brand source** — almost every brand-relevant token (colors, fonts, radii, pills, shadows) is Tailwind/Mercury default rather than a Tesote design decision. This is the audit + plan to fix that.

## What I did

- Audited `workspace-shell.html` and `claim-flow.html` (the two canonical PRO-112 prototypes) against `design.md`
- Catalogued every divergence — colors, typography, radii, status pills, shadows, color sprawl
- Wrote a 15-row punch list with prototype-current → Lunour-spec → recommended action for each

## How I approached it

Premise: **Lunour is Tesote's brand**, full stop. Where the prototypes pulled tokens from elsewhere (Tailwind defaults, Mercury pastels, ad-hoc `style=` hexes), that's drift to correct, not a Tesote choice to preserve. Where Lunour is genuinely silent (e.g., a product-UI font scale), we extend Lunour with **Tesote-original** decisions — not by importing Mercury's choices.

Most rows on the punch list are mechanical CSS find-and-replace. A few are real design work:
- **Status pills** had no Lunour analogue worth substituting → designed five Tesote-original pastels derived from Lunour ramps. Now locked, tokens added to `design.md`.
- **Shadows** are the biggest visual change — Lunour says "borders > shadows" and the prototype is shadow-heavy. This is a restyle, not a swap.
- **Typography** — prototypes use Inter; Lunour mandates Inter Tight + Aspekta. Two valid paths, undecided (see "open" below).

## What I'm giving you

1. **`design.md`** — the brand source of truth. Now includes a new "Product UI extension" section that documents the locked status-pill family. Other product-UI extensions (font scale, button radii, typography path) are flagged TBD inside the same section.
2. **`workspace-design-decisions.md`** — the punch list. 15-row table at the top, per-area detail below, decisions log at the bottom. Read in that order.

## What I locked

- **Pill color family.** Five Tesote-original pastels: `pill-new #E4ECF7` · `pill-pending #F7EDD0` · `pill-overdue #F8D8C0` · `pill-paid #D6E8D5` · `pill-draft #ECE7DD`. Replacing the Mercury pastels currently in the prototypes. Hexes designed to be cohesive (similar perceived lightness, all warm-toned to match `gray-50` cream surfaces, all derived from Lunour ramps with consistent desaturation).

## What I still need from you

Two open questions where engineering judgement matters:

1. **Typography path.** Full migration to Inter Tight + Aspekta in product UI, OR keep Inter and we'll formalize an in-product exception with Lunour? Real cost difference (additional font load + layout re-tune for the migration). Want your read on what's worth it for the build.
2. **Sequencing.** Do we apply this migration **before** you start the engineering build (cleanest, ~1–2 dev-days mechanical + ½–1 day for shadow restyle), **during** the build (a designer paralleling you), or **after v1 ships** (sweep follow-up)? My instinct is "before" because the diff touches almost every component; would rather not have you build twice. But you have better visibility on the sprint.

Drop thoughts in this thread or grab time — happy to walk through either doc.

— Luis
