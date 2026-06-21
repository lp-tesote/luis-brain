---
title: Workspace Prototype Design Decisions — Punch List vs Lunour
tags: [design, brand, product, pro-112, reconciliation]
updated: 2026-05-03
status: ready-for-engineering-review
audience: Luis, Dan
---

# Workspace Design Decisions — what to change to match Lunour

> Companion to [[design]] (the Lunour brand system). Audits the visual decisions baked into the PRO-112 prototypes (`workspace-shell.html`, `claim-flow.html`) and flags **what diverges from Lunour and needs to be changed**.
>
> Premise: **Lunour is Tesote's brand.** Mercury was inspiration for layout density and a few interaction patterns, not a source of brand tokens. Anywhere the prototypes pulled Mercury (or Tailwind) hexes, fonts, radii, or pill styles, we treat that as drift to correct — not as a Tesote design decision.
>
> Where Lunour is silent (e.g., a product-UI font scale), we extend Lunour with **Tesote-original** decisions, not by importing Mercury's choices.
>
> **Sources audited:** `product/tesote-pay/prototypes/pro-112/workspace-shell.html` (May 1) and `claim-flow.html` (May 1, canonical visual source per packet README).

---

## TL;DR

The prototypes are essentially built on the **Tailwind palette + Mercury-app pastel pills + plain Inter**. Almost every brand-relevant token diverges from Lunour:

- **Colors** are Tailwind, not Lunour. Migrate every hex.
- **Status pills** are Mercury's pastels. Replace with Tesote-original pastels (locked — see §2 below; tokens added to `design.md`).
- **Typography** is Inter, not Inter Tight + Aspekta. Migrate or get Lunour's blessing for an in-product exception.
- **Radii** are systematically larger than Lunour's. Migrate to 4/8/12.
- **Shadows** use a 3-tier system; Lunour says borders over shadows. Restyle.

This is a **prototype-side fix list**. `design.md` mostly stays as-is; we add a small "Product UI extension" section for things Lunour doesn't yet specify (a 11–24px font scale, status-pill family, button/pill width conventions). That extension is Tesote's own — not Mercury's.

---

## Punch list — what to change in the prototypes

| # | Area | Prototype today | Lunour spec | Action |
|---|---|---|---|---|
| 1 | Brand blue | `#2563eb` (Tailwind) | `blue-700 #1661E2` | Replace |
| 2 | Primary text | `#0f172a` (Tailwind slate) | `gray-1000 #12110F` | Replace |
| 3 | App background | `#ffffff` + cool grays (`#f6f6f8`, `#f9fafb`, `#fafafb`) | white + cream `gray-50 #F7F5F0` | Replace cool grays with cream surfaces |
| 4 | Borders | `#e8e9ee` | `gray-200 #E8E3DA` (warm) | Replace |
| 5 | Success | `#059669` (Tailwind emerald) | `green-600 #1A8C5B` | Replace |
| 6 | Error | `#dc2626` (Tailwind red) | `red-600 #C41E1E` | Replace |
| 7 | Warning text | `#b45309` (Tailwind amber) | `yellow-600 #CC9500` | Replace |
| 8 | Status pills (5 colors) | Mercury pastels lifted directly: lavender `#e4e8f7`, amber `#fdefce`, salmon `#fddcc5`, mint `#d8e9de`, cool-gray `#eef1f4` | Now defined in `design.md` → Product UI extension | **Locked.** Replace with Tesote pill family: `pill-new #E4ECF7` · `pill-pending #F7EDD0` · `pill-overdue #F8D8C0` · `pill-paid #D6E8D5` · `pill-draft #ECE7DD`. See §2. |
| 9 | Heading font | Inter | Inter Tight | Migrate (or formalize an in-product exception via Lunour) |
| 10 | Body font | Inter | Aspekta | Same as #9 |
| 11 | Pill radius | 5px | 4px (tags/inputs) | Replace with 4px |
| 12 | Card radius | 10px / 14px | 8px / 12px | Replace |
| 13 | Color count | ~60 distinct hex per file | Confined ramps, "don't introduce new hues" | Audit and consolidate after migration |
| 14 | Shadows | 3-tier (`--shadow`, `--shadow-md`, `--shadow-lg`) on cards/panels/dropdowns | "Use sparingly. Prefer 1px border in gray-200 over drop shadow." | Restyle: replace shadows with borders for elevation |
| 15 | Inline color leaks | Many `style="color: #xxx"` bypassing CSS vars | — | Cleanup pass after var migration |

Items 1–7 are mechanical CSS find-and-replace. Items 11–12 are nearly mechanical. Items 8, 9–10, and 14 are real design work.

---

## Per-area detail

### 1. Colors — wholesale migrate to Lunour

The prototype's `--primary`, `--text`, `--green`, `--red`, `--yellow-bg`, `--border` are all Tailwind defaults. None match Lunour. None are Tesote-original choices — they're whatever was easiest to type when the HTML was scaffolded. Replace.

Side effect worth naming: swapping `#0f172a` (cool blue-black) → `#12110F` (warm near-black) and the cool grays → Lunour's warm cream (`gray-50 #F7F5F0`) shifts the prototype from a Mercury-temperature feel to a Lunour-temperature feel. That's the point. The proposal templates already have this temperature; the workspace UI should match.

### 2. Status pills — Tesote-original pastels (LOCKED)

**Decision: option B.** Five Tesote-original pastels, derived from Lunour ramps with custom desaturation. Tokens now live in `design.md` under "Product UI extension → Status pill family."

| Token | Hex | Hue | Replaces (Mercury) |
| -------------- | --------- | ------------ | ----------------------- |
| `pill-new`     | `#E4ECF7` | Blue         | lavender `#e4e8f7`      |
| `pill-pending` | `#F7EDD0` | Yellow       | amber `#fdefce`         |
| `pill-overdue` | `#F8D8C0` | Orange       | salmon `#fddcc5`        |
| `pill-paid`    | `#D6E8D5` | Green        | mint `#d8e9de`          |
| `pill-draft`   | `#ECE7DD` | Gray (warm)  | cool-gray `#eef1f4`     |

**Why option B over Lunour ramps direct:**
- Lunour `100` ramp shades (`blue-100`, `yellow-100`, `orange-100`, `green-100`, `gray-100`) are brighter and more saturated — designed for charts, CTAs, and banners. Pills should recede, not shout.
- Mercury's hexes had a cool blue-grey cast across the family that doesn't match Lunour's warm `gray-50` cream surfaces. Tesote pills shift the entire family **warm**.
- All five sit at similar perceived lightness (~92 L*) and similar low chroma so they read as a cohesive family, not five independent colors.

**Derivation rule** (for adding a sixth status later): start from the Lunour ramp `100` for the right hue family, push lightness up ~5%, drop chroma ~20%. Add the new token to `design.md`. Do not invent a new hue family.

### 3. Typography — Inter Tight + Aspekta, or sanctioned exception

Lunour mandates Inter Tight (display) + Aspekta (body). Prototypes use Inter only. Two valid paths:

- **Migrate.** Adopt Inter Tight + Aspekta in the prototypes. Re-tune layout because metrics shift slightly. Higher fidelity to brand, real engineering cost.
- **Formalize an in-product exception.** Update `design.md` to say in-product UI uses Inter at 11–14px sizes where Inter Tight readability degrades; marketing artifacts (proposals, PDF, web pages) keep Inter Tight + Aspekta. Lower cost, but requires brand@lunour.com sign-off — it's their call whether the brand allows that split.

Either way, the current state ("Inter because that's what got typed") isn't a Tesote design decision. Pick a path and document it.

### 4. Radii — migrate to 4 / 8 / 12

Lunour: 4 (tags/inputs), 8 (cards), 12 (larger surfaces). Prototype: 5 / 10 / 14 — systematically softer. Mechanical replace. Pills go 5px → 4px. Cards 10px → 8px. Modals/large surfaces 14px → 12px.

### 5. Shadows — replace with borders

Lunour: *"Use sparingly. Prefer a 1px border in gray-200 over a drop shadow."*

Prototype: shadows on every card, panel, dropdown, modal — three tiers (`--shadow`, `--shadow-md`, `--shadow-lg`).

This is a **real visual change**, not a token swap. Cards and panels become flatter and more contained. It's also more on-brand for Lunour's stated principle of "bold, distinctive, sharp." Restyle.

### 6. Color sprawl — clean up after migration

Each prototype file uses ~60 distinct hex values. After migrating CSS variables, most will collapse. The remaining stragglers are inline `style="color: #xxx"` — sweep them into vars.

---

## Where Lunour is silent — Tesote-original extensions needed

Lunour doesn't currently specify these. The prototypes filled the gap with Mercury choices; we should replace those with **Tesote-original** decisions and add them to `design.md`.

| Gap in Lunour | What the prototype does today | What we need |
|---|---|---|
| Product-UI font-size scale (11–24px range) | 18 ad-hoc sizes including half-pixels (10.5, 11.5, 12.5, 13.5) | A clean Tesote scale: `11 / 12 / 13 / 14 / 16 / 18 / 22` (or similar). Lose the half-pixels. |
| Status-pill color family | Mercury's five pastels | Five Tesote pill colors (see §2) |
| Pill + small-button uniform width convention | 96px min-width, 11px font, 3px padding | Tesote convention — fine, just document it |
| Button radius | 6 / 7px | A Tesote button-radius decision (probably 6px or align with 4/8) |
| Iconography weight / line stroke | Inconsistent across HTMLs | Tesote icon spec |

These go into a new "Product UI extension" section in `design.md` once decided. Not into Mercury's leftover tokens.

---

## Decisions

### Locked

- **2026-05-03 — Pill color approach:** option B. Five Tesote-original pastels added to `design.md` under "Product UI extension → Status pill family." See §2 above.

### Still open

1. **Typography path:** (A) full migration to Inter Tight + Aspekta in product UI, OR (B) get Lunour to formalize an Inter-as-product-UI exception. *Either is defensible — (B) is cheaper but requires `brand@lunour.com` sign-off.*
2. **Sequencing:** do this migration **before** Dan starts the engineering build, **during** the build (designer in parallel), or **after v1 ships** as a follow-up sweep. *Affects timeline and how much rework is on the table.*

Everything else on the punch list is mechanical or has a clear Lunour answer.

---

## What goes back into `design.md` (in the KB)

After decisions:

- **No Mercury tokens.** None of these go into `design.md`.
- **New "Product UI extension" section** with: Tesote font scale, button/pill width conventions, button radius, Tesote pill color family (option B) or pointer to Lunour ramp tokens used (option A).
- **Update typography section** with whatever the (A)/(B) typography decision is.
- **Reduce "Known drift"** list as items get reconciled.

## What goes back into the prototypes

Once `design.md` is updated:

- CSS variable swap: `--primary` → `#1661E2`, `--text` → `#12110F`, `--border` → `#E8E3DA`, `--green` → `#1A8C5B`, `--red` → `#C41E1E`, etc.
- Pill hexes replaced (per option A or B).
- Font swap (per typography path).
- Radii migrated 4/5/8/10/12/14 → 4/8/12.
- Shadows replaced with `1px solid gray-200` borders for elevation.
- Inline `style=` color cleanup.
- Half-pixel font-sizes removed; sizes snapped to Tesote scale.

Estimated effort: **half a day** for color + radius migration alone. Add **half a day** for font swap (if migrating). Add **a full day** for shadow → border restyle and visual QA. Total: 1–2 dev-days for the mechanical work, plus design review.

---

*Last updated 2026-05-03 — initial punch list. Update when any open question is decided or as items get reconciled in the prototypes.*
