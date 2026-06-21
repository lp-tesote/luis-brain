---
title: Tesote AI — Typography Spec
tags: [product, ai, design, typography]
updated: 2026-05-20
status: locked — variant 2 (Inter + Instrument Serif) chosen by Luis on 2026-05-20
companion: [[typography-comparison.html]]
---

# Tesote AI — Typography Spec

A redesign of the type system for the `/ai` surface. Replaces the current Inter Tight + heavy-weight hierarchy with a quieter, more editorial system that lets artifacts (the right-pane working files) carry the visual weight instead of the chat chrome.

Companion HTML mockup: [`typography-comparison.html`](typography-comparison.html) — open in a browser to see the current state vs. proposed side-by-side.

---

## The problem in one paragraph

The current system uses **Inter Tight** at 14px / 1.5 line-height with weights ranging up to 700 on the chat-pane title. Inter Tight is a *headline cut* — narrower letters, tighter tracking — designed for chrome and badges, not body text. Combined with 600/700-weight headers and conservative leading, the AI surface reads "control panel" instead of "thoughtful collaborator." Compared to Mercury (Söhne, max 500 weight), Claude Desktop (serif + sans pairing, generous leading), and ChatGPT (Söhne at 16/1.7), the Tesote AI surface fights for attention with the working files it produces. We want the chat to recede so the artifact reads as the deliverable.

---

## The system

### Sans — UI, chat, body
**Inter** (variable, default width — NOT Inter Tight). Free, open-source, already loaded by Tesote. Variable font with `wght` axis (100–900) and `opsz` axis for optical sizing at display sizes.

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

--font-sans: 'Inter', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif;
```

Migration cost: change one line in `styles.css:10` — drop `+Tight` from the URL and the family name.

**Alternative if you want more character**: **Geist** (Vercel). Slightly more modernist, more geometric `g`, sharper terminals. Pulls the brand toward "AI-native" companies (Vercel, Linear, Cursor) rather than "fintech" (Mercury, Stripe, Brex). Both are right answers — Inter is the safer one; Geist signals more.

### Serif — hero copy only
**Instrument Serif** (Google Fonts). Used **only** in the empty-state hero ("¿Qué querés ver hoy?"), capability browser title, and major moments of voice. Never in body text, never in tool labels, never in the file tree.

```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap');

--font-serif: 'Instrument Serif', ui-serif, Georgia, serif;
```

This is the Anthropic move (Copernicus serif for assistant messages). Even one moment of serif breaks the all-sans monotony and signals craft. Use sparingly — one or two surfaces, not everywhere.

### Mono — machine identifiers only
**JetBrains Mono** stays. Already loaded. Used for: file names (`revenue-by-category.json`), file IDs (`f_rev_by_cat`), tool names (`counterparty.create`), code blocks in chat. Never for tool *labels* (humanized "Crear contraparte" goes in sans).

---

## Scale

| Token | Size | Where | Rationale |
|---|---|---|---|
| `--text-xs` | 11px | Badge pills, eyebrow labels, status chips | Compressed metadata |
| `--text-sm` | 12px | File-tree rows, secondary labels, timestamps | Quiet structural text |
| `--text-base` | **15px** | Chat messages, composer, file viewer body | **Up from 14px** — reading scale |
| `--text-md` | 17px | Section headers, file viewer titles | Subtle step up |
| `--text-lg` | 22px | Conversation title (pane H1) | Mid-emphasis heading |
| `--text-xl` | 32px | Empty-state hero ("¿Qué querés ver hoy?") | The serif moment |
| `--text-mono-sm` | 12px | File names in tree, tool names in pills | Mono runs ~1pt smaller than sans for visual balance |
| `--text-mono-base` | 13px | Code blocks in chat | One step down from body sans |

Base size goes from **14px → 15px**. That extra 1px (≈7%) is the single highest-leverage change. It moves the chat from "compact UI" to "reading surface" without any other intervention.

## Weights

| Weight | Allowed in | Forbidden in |
|---|---|---|
| 400 (Regular) | Body, chat, file rows — everything by default | — |
| 500 (Medium) | Pane titles, section headers, active states, badges, hero | — |
| 600 (Semibold) | Brand mark only ("Tesote AI" in sidenav) | Chat headers, tool labels, file rows |
| 700 (Bold) | **Forbidden in chat surface.** Reserved for inline emphasis (`**bold**` in user/AI markdown) only. | Pane titles, headers, labels |

**Cap chat hierarchy at 500.** Let size + color carry hierarchy instead of weight. Mercury's whole feel comes from this principle.

## Line-height

| Context | Line-height | Rationale |
|---|---|---|
| Chat messages | **1.6** | Up from 1.5. Reading rhythm, not scanning rhythm. |
| Pane titles, headers | 1.25 | Compact for display sizes |
| File-tree rows, table rows | 1.4 | Dense structural lists |
| Code blocks, mono content | 1.55 | Mono needs room |

## Letter-spacing

Minimal use. Inter is well-tracked out of the box. Two exceptions:
- **Uppercase eyebrows** (e.g. "CONVERSACIONES" in sidenav): `letter-spacing: 0.06em` — uppercase always needs +tracking
- **Display hero serif**: `letter-spacing: -0.01em` — slight tighten for Instrument Serif at 32px+

Never apply letter-spacing to body sans.

## Color hierarchy (companion to weight)

Since we're capping weight, color does more lifting. The existing tokens are correct — just used more deliberately.

```css
--text-primary:   var(--gray-1000);  /* default chat text */
--text-secondary: var(--gray-600);   /* labels, timestamps, secondary metadata */
--text-muted:     var(--gray-400);   /* placeholder text, decorative ids */
```

Pattern: primary text at 400-weight feels heavier than secondary text at 500-weight. Use color hierarchy first, then bump weight only when color alone can't disambiguate.

---

## Migration plan

Priority-ordered. Each step ships independently — no big-bang.

### Step 1 — Swap the face (single-line change, biggest impact)
- Drop `Inter+Tight:wght@400;500;600;700` from the `@import` in `styles.css:10`
- Replace with `Inter:wght@400;500;600` + `Instrument+Serif`
- Update `--lunour-font-sans` to `'Inter'` (remove `Tight`)
- Add `--lunour-font-serif: 'Instrument Serif', ui-serif, Georgia, serif;`

### Step 2 — Bump body
- `body { font-size: 15px; line-height: 1.6; }`
- Audit hardcoded `font-size: 14px` declarations in `styles.css` — most should become `inherit` or move up one step

### Step 3 — Cap weights
- Find/replace `font-weight: 700` → `font-weight: 500` in chat-pane surfaces
- Find/replace `font-weight: 600` → `font-weight: 500` everywhere EXCEPT the sidenav brand mark
- Pane title: keep at 22px but drop to weight 500

### Step 4 — Add the serif moment
- Empty-state hero gets `font-family: var(--lunour-font-serif); font-size: 32px; font-weight: 400; letter-spacing: -0.01em;`
- Capability browser title: same treatment
- One moment of serif. Don't sprinkle.

### Step 5 — Audit mono usage
- Tool pill *labels* (the humanized "Crear contraparte") → sans
- Tool *names* (`counterparty.create`) → keep mono
- File names in tree → mono
- File names in chat-bubble pills → mono
- Anywhere mono is decorative rather than identifying → sans

### Step 6 — Dark theme review
- The Lunour gold accent (`#c3a05e`) plays well with Inter; no changes needed
- Verify Instrument Serif renders cleanly at 32px on dark — it has thin strokes that can disappear; may need to step down to 30px or add `font-weight: 400` (default is already 400, but explicit beats inherited)

---

## What this is NOT

- Not a brand-system overhaul. Tesote Classic stays on its current type. This is `/ai` only.
- Not a token-name rewrite. `--lunour-*` tokens stay; just their values change.
- Not a redesign of the visual layout. Same panes, same colors, same components — just calmer type.
- Not a recommendation to license Söhne. Inter gets us 90% there for $0. Revisit Söhne if/when the AI surface graduates into a separately-branded product (which the [[project_tesote_command_center]] arc may eventually require).

---

## Decisions (locked 2026-05-20)

1. **Sans: Inter** (default width, NOT Tight). Zero migration friction, already loaded, matches the Mercury/Stripe cohort. Revisit Geist if/when Tesote AI gets its own brand identity separate from Tesote Classic.
2. **Serif: Instrument Serif** for the hero moment. Modernist, Anthropic-adjacent, lets the content speak. Free on Google Fonts.
3. **Mono: JetBrains Mono** stays as-is. Already loaded.
4. **PR shape: one PR**, behind the existing `:tesote_ai_demo` flag. Whole change is ~50 lines of CSS.

## Next step — bridge to treasury

This is product-UI work; eng has to implement. Per [[../../CLAUDE.md|brain CLAUDE.md]], the move is `/tesote-plan` in the treasury repo — pair it with `redesign-2026-design-system` skill in the same session so design-system drift gets caught before code is written.

Suggested Linear ticket scope: "Tesote AI typography pass — Inter + Instrument Serif + weight cap." File the PRO-* ticket, then in treasury:

```
cd ~/Programming/tesote/treasury
/tesote-plan <linear-url>
```

The plan lands at `.debugging/plans/[name]/`. Hand to Dan or run `/implement` directly.

---

## Companion mockup

[`typography-comparison.html`](typography-comparison.html) — open locally in a browser. Shows the same chat-pane content rendered three ways:

1. **Current** — Inter Tight, 14px/1.5, weights to 700
2. **Proposed (Inter + serif)** — what we'd actually ship
3. **Alternative (Geist + serif)** — the more modernist option

Squint test: scroll between them. Current stays sharp and active. Proposed blurs into something quiet and editorial. That's the move.
