---
title: Tesote Design System
tags: [design, brand, reference]
updated: 2026-05-03
---

# Design System

Tesote's brand tokens, distilled from the Lunour brand book. This file is the source of truth for skills that generate branded artifacts (`/pdf`, `/proposal`, prototypes). When in doubt, defer to Lunour.

- **Canonical brand book:** https://tesote.lunour.design/
- **Studio contact:** brand@lunour.com

## Principles

- Bold, distinctive, consistent. Tesote uses a confined primary palette with generous white/cream space, sharp type, and high contrast.
- Default color ratio across applications: **50% primary / 20% secondary / 20% tertiary / 10% accent.** Don't let accents dominate.
- If something's not covered here, the brand book is the fallback. Don't invent tokens — if we need one, add it here first.

## Colors

### Primary palette (use these for 90% of surfaces)

| Token          | Hex       | RGB            | Use                                      |
| -------------- | --------- | -------------- | ---------------------------------------- |
| `white`        | `#FFFFFF` | 255, 255, 255  | Default background, logo on dark         |
| `gray-1000`    | `#12110F` | 18, 17, 15     | Primary text, dark surfaces (not `#000`) |
| `gray-50`      | `#F7F5F0` | 247, 245, 240  | Cream background, subtle surfaces        |
| `blue-700`     | `#1661E2` | 22, 97, 226    | Brand blue — CTAs, links, accents        |

### Secondary palette (use sparingly — data viz, status, subtle accents)

Full 25→1000 ramps. `500` is the perceptual mid; `700` is the default "strong" for each family.

**Red** (error, destructive)
`25 #FFF5F5` · `50 #FFE6E6` · `100 #FFD1D1` · `200 #FFAAAA` · `300 #FF7D7D` · `400 #FF4F4F` · `500 #E53030` · `600 #C41E1E` · `700 #A31515` · `800 #7E1010` · `900 #5A0C0C` · `1000 #2E0707`

**Orange** (warning, highlight)
`25 #FFF8F2` · `50 #FFECDE` · `100 #FFD9B8` · `200 #FFBD85` · `300 #FF9A4F` · `400 #FF7A1F` · `500 #E65C00` · `600 #CC4D00` · `700 #A83E00` · `800 #853000` · `900 #5E2200` · `1000 #2E1200`

**Yellow** (caution, highlight)
`25 #FFFBEA` · `50 #FFF6CC` · `100 #FFE999` · `200 #FFDD66` · `300 #FFD233` · `400 #FFC400` · `500 #E6AB00` · `600 #CC9500` · `700 #A37400` · `800 #805A00` · `900 #5E4000` · `1000 #2E2000`

**Green** (success, confirmation)
`25 #F3FCF8` · `50 #E6FAF1` · `100 #C9F1E0` · `200 #9DE4C6` · `300 #6FD6AA` · `400 #40C98E` · `500 #24AD72` · `600 #1A8C5B` · `700 #156F49` · `800 #10543A` · `900 #0B3928` · `1000 #0C1E18`

**Blue** (informational, links — `700` is the primary brand blue)
`25 #F5FBFF` · `50 #EEF8FF` · `100 #D9EEFF` · `200 #BCE2FF` · `300 #8ED1FF` · `400 #59B6FF` · `500 #3396FE` · `600 #1C77F4` · `700 #1661E2` · `800 #184EB5` · `900 #123F8A` · `1000 #152B56`

**Purple** (experimental, niche accents)
`25 #FBF7FE` · `50 #F6ECFD` · `100 #EAD3FB` · `200 #D3A9F7` · `300 #C994F7` · `400 #B87AF2` · `500 #9C4CEC` · `600 #7E29C8` · `700 #641FA3` · `800 #4D187D` · `900 #39125C` · `1000 #260C3E`

**Gray** (neutrals, borders, muted text)
`25 #FCFBF7` · `50 #F7F5F0` · `100 #F2EEE6` · `200 #E8E3DA` · `300 #D6D0C7` · `400 #C7C0B5` · `500 #A8A096` · `600 #857D73` · `700 #635D55` · `800 #47423B` · `900 #302C25` · `1000 #12110F`

### Semantic shortcuts

Use these names in skill output so intent is clear:

| Semantic        | Token         | Hex       |
| --------------- | ------------- | --------- |
| `text-primary`  | `gray-1000`   | `#12110F` |
| `text-muted`    | `gray-600`    | `#857D73` |
| `background`    | `white`       | `#FFFFFF` |
| `surface-cream`| `gray-50`     | `#F7F5F0` |
| `border`        | `gray-200`    | `#E8E3DA` |
| `brand`         | `blue-700`    | `#1661E2` |
| `brand-soft`    | `blue-50`     | `#EEF8FF` |
| `success`       | `green-600`   | `#1A8C5B` |
| `warning`       | `yellow-600`  | `#CC9500` |
| `error`         | `red-600`     | `#C41E1E` |

### Don'ts

- Don't use pure `#000000` for text — use `gray-1000` (`#12110F`).
- Don't introduce new hues. Extend only by picking from the ramps above.
- Don't pair low-contrast combos (e.g., `gray-400` text on white). Verify contrast per WCAG AA (4.5:1 for body).

## Typography

### Font families

| Role              | Font          | Use                                                      |
| ----------------- | ------------- | -------------------------------------------------------- |
| **Primary**       | Inter Tight   | Headings, display, digital UI. Crisp, modern, versatile. |
| **Supporting**    | Aspekta       | Body copy, captions, long-form text. Highly legible.     |

Fallback stack: `'Inter Tight', 'Aspekta', -apple-system, BlinkMacSystemFont, sans-serif`.

Font files: served from Lunour (see brand book "Download" links). For web embeds, mirror into `templates/assets/fonts/` when needed.

### Hierarchy

| Style                | Font & weight           | Leading | Tracking | Case     |
| -------------------- | ----------------------- | ------- | -------- | -------- |
| Headline             | Inter Tight SemiBold    | 110%    | -3%      | Sentence |
| Subhead              | Inter Tight SemiBold    | 125%    | -3%      | Sentence |
| Body Copy            | Aspekta 400             | 125%    | 0        | Sentence |
| Body Copy Bold       | Aspekta 600             | 125%    | 0        | Sentence |
| Body Copy Light      | Aspekta 200             | 125%    | 0        | Sentence |
| Headline Bold        | Inter Tight Bold        | 110%    | -3%      | Sentence |

**Leading formulas** (use when a specific pt isn't listed):
- Headlines: `size × 1.1`
- Subheads / body: `size × 1.25`

**Example sizes used in our artifacts:**
- Proposal hero headline: 80/88pt
- Section heading (H2): 30/36pt
- Body: 15–16/20pt

## Logo

Files live in `templates/assets/`:
- `logo.svg` — symbol only (the "T" mark)
- `text.svg` — full wordmark (symbol + "tesote")
- `logo-60.png`, `text-200.png` — raster exports

Additional SVG variants on Lunour (black / white / two-color):
- `tesote-logo-black.svg`, `tesote-logo-white.svg`
- `tesote-logo-two-color-black-1.svg`, `tesote-logo-two-color-white.svg`

### Usage

- **Default:** full logo (wordmark). Use the standalone symbol only when space is tight or context already establishes the brand (avatars, favicons, app icons).
- **Colors:** black or white only. No other fills.
- **Minimum size:** 20px digital, ¼ inch print.
- **Clearspace:** at least the height of the symbol on all sides. Nothing inside that margin.
- **Favicon / avatar:** black logomark on off-white (`gray-50`) for avatars; black logomark on transparent for favicons.

### Don'ts

Don't stretch, distort, outline, shadow, rotate, skew, recolor, or place patterns inside the logo.

## Layout + shapes

Lunour doesn't publish a spacing/radius scale yet. Current practice in our artifacts:

- **Spacing:** 4px base unit. Prefer the scale `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64`.
- **Border radius:** `4px` (inputs, tags), `8px` (cards), `12px` (larger surfaces). Avoid fully rounded unless for pill badges.
- **Shadows:** use sparingly. For elevation, prefer a `1px` border in `gray-200` over a drop shadow.

If Lunour later publishes these, replace this section.

## Product UI extension

These tokens extend Lunour for in-product UI (workspace app, counterparty portal, internal surfaces). Marketing artifacts (proposals, PDFs, web pages) continue to use the primary palette and typography above without these extensions.

Lunour is silent on most of these conventions today. The choices below are **Tesote-original** — derived from Lunour ramps and principles, not lifted from any third-party app.

### Status pill family

Five pastel tokens for status indicators in lists, tables, and cards. Designed so pills **recede rather than shout** — all five at similar perceived lightness, all warm-toned to match `gray-50` cream surfaces. Derived from Lunour ramps with custom desaturation (~5% lighter, ~20% lower chroma than the corresponding `100` shade).

| Token          | Hex       | Hue family   | Use                                                |
| -------------- | --------- | ------------ | -------------------------------------------------- |
| `pill-new`     | `#E4ECF7` | Blue         | New / sent / informational                         |
| `pill-pending` | `#F7EDD0` | Yellow       | Pending / awaiting action / approved-not-yet-paid  |
| `pill-overdue` | `#F8D8C0` | Orange       | Overdue / late                                     |
| `pill-paid`    | `#D6E8D5` | Green        | Paid / success / completed                         |
| `pill-draft`   | `#ECE7DD` | Gray (warm)  | Draft / inactive / neutral                         |

**Rules:**
- Pair pill backgrounds with `gray-1000` (`#12110F`) text. No borders. Filled background only.
- Do not substitute Lunour ramp shades (e.g., `green-100`, `yellow-50`) — those are brighter and intended for charts, CTAs, and banners. Pills get this dedicated family.
- If a sixth status arises, derive it the same way: pick the appropriate Lunour ramp `100`, apply the same desaturation curve, and add it here. Do not invent a new hue family.

### Category-tag palette (2026-06-09)

A **separate** family from the status pills, for taxonomy labels (transaction categories, "tipo" labels) — *not* state. Categories must never borrow a status pastel (a `Software` category is not in an "error" state; a `Cobros` category is not "new"). Treatment: a **neutral `pill-draft` (`#ECE7DD`) chip + a colored category dot** — the hue lives in the 6px dot, so categories stay quieter than the filled status pills (correct hierarchy: status is acted on, category is ambient). Editable categories add the always-visible caret.

Dots use the **`600`/strong shade** of a Lunour ramp. Stable per category (a category is always the same hue). Default-stable assignment:

| Hue (token) | Dot hex | Ramp | Example categories |
| ----------- | ------- | ---- | ------------------- |
| `cat-green`  | `#1A8C5B` | green-600  | Cobros, Reembolsos (ingresos) |
| `cat-blue`   | `#1661E2` | blue-700   | Nómina, Contraparte |
| `cat-purple` | `#7E29C8` | purple-600 | Software |
| `cat-orange` | `#CC4D00` | orange-600 | Infraestructura |
| `cat-yellow` | `#CC9500` | yellow-600 | Servicios, Tipo |
| `cat-red`    | `#C41E1E` | red-600    | Impuestos |
| `cat-gray`   | `#857D73` | gray-600   | Bancarios, otros / unmapped |

**Rules:** dot-only color (chip fill stays neutral `pill-draft`, no border); pick the hue from a ramp `600` and don't invent new hues; an unmapped category falls back to `cat-gray`. More categories than hues is fine — reuse a hue across related categories (the label disambiguates). Reference impl: `product/design/unified-app-v1.html`.

### Locked decisions (2026-05-14)

- **Product-UI font scale:** `11 / 12 / 13 / 14 / 16 / 18 / 22 / 28`. Half-pixels removed. Default body / table cell / input = 13px. Page title = 26px. See [[archetypes]] for which size goes where per archetype.
- **Product-UI typography path:** **full migration to Inter Tight + Aspekta.** No in-product Inter-only exception. Updates required: PRO-112 prototypes, `templates/pdf-style.css`, `proposal-template.html`.
- **Density target:** Mercury / Linear high-density. Standard list row = **44px**. Compact 36px (single-line, no avatar) · Comfortable 56px (high-context with metadata).

### Open extensions (still TBD)

Things the prototypes currently improvise that Tesote should still formalize:

- **Pill + small-button uniform width.** Prototypes use 96px min-width, 11px font, 3px 8/10px padding. Document if kept.
- **Button radius.** Prototypes use 6/7px. Decide and align with the 4/8/12 scale (likely 4px for sm buttons, 8px for md).
- **Iconography.** Stroke weight, line style, sizing — currently inconsistent across prototypes.

See [[archetypes]] for the six screen archetypes and density spec, and [[workspace-design-decisions]] for the full audit and the punch list for migrating the PRO-112 prototypes to this system.

## Where this gets applied

Skills that produce branded output — update them here when tokens change:

| Artifact                             | File                                                   | Notes                                |
| ------------------------------------ | ------------------------------------------------------ | ------------------------------------ |
| Branded PDF (for `/pdf`)             | `templates/pdf-style.css`                              | Global stylesheet                    |
| Commercial proposal (for `/proposal`)| `.claude/skills/proposal/proposal-template.html`       | Uses CSS custom props — easy to sync |
| Logo assets                          | `templates/assets/logo*.{svg,png}`, `text*.{svg,png}`  | —                                    |

### Known drift from Lunour (as of 2026-04-24)

Flagging so we can sync when we next touch these files — not a blocker:

- `templates/pdf-style.css` uses `Inter` (not `Inter Tight`), `#4361ee` (not `#1661E2`), `#1a1a2e` (not `#12110F`), `#f8f9fa` (not `#F7F5F0`).
- `proposal-template.html` text uses pure `#000000` — Lunour spec is `gray-1000` (`#12110F`).
