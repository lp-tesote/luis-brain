---
title: Visual Essay HTML Format
tags: [design, storytelling, claude-code]
updated: 2026-06-11
status: draft
---

# Visual Essay HTML Format

A reusable single-file format for turning an essay, strategy doc, or argument into a scroll-driven visual artifact. Reference implementation: [`drafts/the-untrainable/the-untrainable-v1.html`](../drafts/the-untrainable/the-untrainable-v1.html) (built 2026-06-11, approved).

Use it for: investor narratives, strategy memos worth socializing, launch pitches, "why we're doing X" internal persuasion pieces — anything where the argument has *shape* and a wall of prose would bury it.

## Core principle

**Every idea gets its own visual form — never decoration.** Before writing any HTML, decompose the source into beats (the reference has 12) and assign each beat the ONE visual that *is* the idea, not one that sits next to it. If a beat has no natural visual form, it's a typographic beat (big serif statement), not a chart for chart's sake.

## Design tokens

- Background: dark ink `#0c0d11`, raised surfaces `#13151b` / `#1b1e27`, hairlines `rgba(255,255,255,0.09)`
- Text: `#e8e6e1` primary, `#9a978f` dim, `#5e5c56` faint
- **One accent only**: gold `#e8b44f`, reserved strictly for the thesis/payoff concept. Everything commodity/dying gets cool blue-gray (`#3d4f6b`). The color system IS the argument.
- Finale flips to paper `#f3efe7` with ink text — the inversion lands the ending.

## Typography

- Display: **Instrument Serif** (400, italics for emphasis), clamp() sizes, hero up to ~132px
- Body: **Inter** 17px / 1.65
- Data, labels, axes, captions: **JetBrains Mono**, 11–13px, letter-spaced uppercase
- (Same stack as Tesote AI `/ai` typography — deliberate; it already reads as "us".)

## Section grammar

Each section: numbered mono `kicker` ("04 · The map") with hairline rule → serif `h2` with the key phrase in gold italic `<em>` → short body paragraphs (strong sparingly) → the visual. Max-width 680px prose, 920px for wide visuals.

## Visual vocabulary (pick per beat)

- **Logic chain** — vertical connected dots for an argument's steps; last node gold (where the logic leads/breaks)
- **Count-up pair** — two huge serif numbers animating up, one dim one gold (before/after, 13% → 88%)
- **Annotated gap bars** — two horizontal bars at true scale with the gap labeled in mono ("this gap is a person")
- **Typographic law** — full-screen centered serif statement in 2–3 staggered lines, the conclusion line gold italic
- **2×2 matrix** — mono axis labels, three quadrants dimmed, the prize quadrant glowing (radial gold wash + border)
- **Rising tide** — full-width stage where a waterline animates up and strikes through what it swallows; survivors listed above in gold
- **Line-art SVG diagram** — 1.5px strokes, gold for the moving parts, mono labels (the door/lock/deadbolt)
- **Token/object contrast** — dashed-border faded card vs glowing gold card
- **Quote cards** — mono company name, serif claim, dim explanation
- **Statline** — one giant gold figure beside its explanation
- **Paper finale** — numbered serif imperatives between hairlines, then the closing quote in italic serif

## Motion rules

- Top progress bar (2px gold, scroll-linked)
- IntersectionObserver adds `.in`; reveals are translateY(28px) + fade, 0.9s, staggered `.d1–.d4` delays
- Counters: requestAnimationFrame, cubic ease-out, ~1.8s
- Bars/tide: CSS width/height transitions triggered by `.in`
- Always honor `prefers-reduced-motion` (kill transitions, show end state)
- Optional hero texture: a grid of faint mono data that slowly decays (`setInterval` adding a fading class) — ambient thesis-setting

## Process

1. Decompose source into numbered beats; assign each a form from the vocabulary (or invent one — the vocabulary grows)
2. Build as ONE self-contained file, only Google Fonts external; name it `<topic>-v1.html` (versioning workflow: new vN per change)
3. `open` in browser immediately
4. Sharing: copy to `site/index.html`, drag folder onto Netlify Drop → instant `*.netlify.app` link; custom subdomain via DNS later if it sticks
5. Bank a README in the folder on session end

#design #storytelling
