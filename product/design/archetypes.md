---
title: Tesote Product UI — Screen Archetypes
tags: [design, product, archetypes]
updated: 2026-05-14
status: draft
audience: Luis, Dan
---

# Archetypes — Tesote Product UI

> Sits between [[design]] (brand tokens — colors, type, status pills) and page-by-page screens. Defines the **six screen archetypes** Tesote ships, the **density target** that constrains them, and the **shared primitives** we'll formalize next.
>
> **Canonical visual reference:** `product/business/pagos/prototypes/pro-112/workspace-shell284.html` — the most-iterated prototype. Anatomy below is extracted from it (and `claim-flow.html` for the form archetype). Where the prototype diverges from this spec, the spec wins — see [[workspace-design-decisions]] for the migration punch list.

---

## TL;DR

| | |
|---|---|
| Density model | **Task-driven, not archetype-driven.** Density follows user intent (browse / manage / review-and-decide). |
| Row heights | **36 browse · 44 manage · 52 review-and-decide** |
| Typography | Inter Tight (display) + Aspekta (body) — full migration |
| Font scale | `11 / 12 / 13 / 14 / 16 / 18 / 22 / 28` |
| Archetypes | List · Detail · Form/flow · Dashboard · Empty · Onboarding · **Hub** (added 2026-06-10 — settings-style grouped link-out cards; spec in [[web-app-design-system]] §16, reference `unified-app-v2.html` → Configuración) |

The doc is **opinionated by default** — every archetype below picks a layout and density. If you disagree with a number, change the number and propagate.

---

## House rules (apply everywhere)

- **No emojis in product UI.** Per [[feedback_no_emojis]] (2026-05-17). Every glyph in user-facing surfaces is an inline SVG. Sidebars, filters, indicators, empty states, buttons, modal headers — all SVG, never emoji. Brain notes and team-internal channels are exempt; this rule is about *what ships to users*.
- **Table-padding tokens** are defined per density bucket — see [[#table-cell-padding-per-density]]. Don't drift across pages.

## Locked foundation

These decisions are upstream of every archetype. Don't relitigate per-page.

- **Typography migration: full Inter Tight + Aspekta.** Decision 2026-05-14. Update `templates/pdf-style.css`, `proposal-template.html`, and the PRO-112 prototypes. Inter is out.
- **Density: Mercury/Linear high-density.** Decision 2026-05-14. Operators live in lists all day; rows are tight, padding is restrained, screens are dense.
- **Color tokens:** Lunour palette per [[design]]. No Tailwind hexes.
- **Status pills:** locked five-pastel Tesote-original family — `pill-new / pending / overdue / paid / draft`. Don't substitute.
- **Shadows out, borders in:** elevation is a 1px `gray-200` border, not a drop shadow.
- **Radii: 4 / 8 / 12.** Tags/inputs/pills → 4. Cards → 8. Large surfaces / modals → 12. No 5/6/7/10/14 in product UI.

---

## Density spec

The numbers that make every archetype feel like the same product.

### Font scale (drop half-pixels)

| Size | Use |
|---|---|
| `11px` | Pills, table headers, micro-meta, tag badges |
| `12px` | Filter labels, dropdown items, secondary captions |
| `13px` | **Default body / table cell / button / form input** |
| `14px` | Sidebar nav, card titles, slightly emphasized body |
| `16px` | Section subhead inside cards/panels |
| `18px` | Card "big number" secondary (e.g., cents on amounts) |
| `22px` | KPI card values, panel titles |
| `28px` | Page hero / dashboard "saldo" amounts |

Page titles (`H1`-equivalent) sit between 22 and 28 depending on context. Default to **26px** for full-page titles to match the prototype.

### Row heights — task-driven, not archetype-driven

Density is a property of the **user's task on the screen**, not of the archetype. Mercury splits this cleanly (sparse Payments queue, dense Transactions ledger); Stripe sits in the middle because their users mix tasks; Linear varies per view. Tesote does it deliberately: three densities, picked by intent.

| Task | Row height | Why | Tesote examples |
|---|---|---|---|
| **Browse / scan** (find one among many) | **36px** | Signal-to-noise; you're hunting. Tight rows fit more on screen. | Transacciones, GL, Bank account ledger, Conciliación queue, Audit log |
| **Manage** (curate a small set) | **44px** | Default. Balanced. 28px avatar + 2-line cell. | Contrapartes, Bank accounts, Reglas, Categorías, Team / users |
| **Review & decide** (act on each row) | **52px** | Each row is a decision; whitespace says "this matters." | **Pagos, Cobros**, Disputas, Approvals, KYC review, New invoices |

**Inferred rule:** if the user's job on this screen is to *do something to each row*, go roomy. If their job is to *find the one row that matters*, go dense. If their job is to *keep the set tidy*, stay standard.

### Table cell padding (per density)

Calibrated against the first two real tables we shipped (Saldos at Manage density, Movimientos at Browse density). Use these numbers verbatim — drift across tables is a smell.

| Density | Row height | `th` vertical | `th` horizontal | `td` vertical | `td` horizontal |
|---|---|---|---|---|---|
| **Browse / scan** | 36px | 10px | 14px | 7px | 14px |
| **Manage** | 44px | 12px | 16px | 11px | 16px |
| **Review & decide** | 52px | 14px | 18px | 15px | 18px |

Rules that hold across all three densities:

1. **`th` and `td` horizontal padding must match exactly** within a single table — otherwise column edges shift visually as you scroll, which feels broken. Vary horizontal *between* densities, never *within* a table.
2. **`th` vertical padding can be slightly tighter** than `td` at the same density, since header text is small-caps and visually lighter. Browse and Manage break this rule (10>7 and 12>11) because at very tight row heights the header earns the extra air; Review density goes the other way (14<15) because body cells carry more content.
3. **Numeric (right-aligned) columns get the same edge padding as left-aligned** — symmetric horizontal padding makes the table feel balanced even with mixed alignments.
4. **Per-column horizontal overrides are allowed** for tightening visually-paired columns (e.g., Fecha → Banco/Cuenta on Movimientos drops to 6px on the inner edges), but the override must apply to BOTH `th` and `td` of those columns so alignment holds.

Use `table-layout: fixed` + explicit per-column widths via `<colgroup>` on every table. Without it, columns auto-size to longest content and row heights drift — the killer of browse-density readability. See [[../connect/movimientos/design#Description truncation pattern]] for the rationale carried forward to every long-text column.

> **Heads-up on supporting chrome:** review-and-decide screens benefit from less header chrome too — Mercury's Payments has no KPI strip, just a clean title + tabs. Tesote's Pagos screen *does* show a 4-card KPI strip (Total / Vencido / Próximo / Pagadas), which is genuinely useful. Don't blindly strip it. But: if a future review-and-decide screen has no useful summary numbers, drop the KPI strip rather than padding it with throwaway stats.

### Spacing rhythm

Use the scale: `4 · 8 · 12 · 16 · 22 · 32 · 48`. (22 instead of 20/24 — it's the dominant card-padding number in the prototype and we're keeping it.)

### Avatar sizes

`20 / 24 / 28 / 32 / 40`. List rows: 28px. Detail panel header: 40px. Sidebar user: 26px.

---

## The six archetypes

Each one has: **purpose**, **wireframe**, **anatomy**, **Tesote examples**, **variants**.

---

### 1 · List / Table

**Purpose:** Browse, filter, and act on a collection of records. The dominant Tesote archetype — probably 60% of screens.

**Wireframe:**

```
┌──────────┬─────────────────────────────────────────────────────┐
│          │  ┌─ topbar (52px) ──────────────────────────────┐   │
│ Sidebar  │  │                       [primary CTA] [⋯ ⋯ ⋯] │   │
│ (224px)  │  └──────────────────────────────────────────────┘   │
│          │                                                      │
│          │   Page Title              [secondary] [Primary CTA]  │
│          │   subtitle                                           │
│          │                                                      │
│          │   ┌─ KPI strip (4-col unified container) ─────┐     │
│          │   │ 22px # │ 22px # │ 22px # │ 22px #         │     │
│          │   │ label  │ label  │ label  │ label          │     │
│          │   └────────┴────────┴────────┴────────────────┘     │
│          │                                                      │
│          │   [Tab] [Tab] [Tab] [Tab] [Tab]                      │
│          │   [Filter ▾] [Group ▾]               [🔍 search   ]  │
│          │                                                      │
│          │   ─────────────────────────────────────────────      │
│          │   COL 1     │ COL 2  │ COL 3  │ COL 4  │ STATUS │ ⋯ │
│          │   ─────────────────────────────────────────────      │
│          │   ◯ name    │ data   │ data   │ data   │ [pill] │ ▸ │
│          │   ◯ name    │ data   │ data   │ data   │ [pill] │ ▸ │
│          │   ◯ name    │ data   │ data   │ data   │ [pill] │ ▸ │
│          │   …                                                  │
└──────────┴──────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Sidebar (224px):** logo + section nav + favorites + user footer. Persistent.
- **Topbar (52px):** primary mover-money CTA (right), icon controls (messages, notifications, settings). No breadcrumbs in v1.
- **Page header:** `26px` title (Inter Tight SemiBold, -0.02em), `13px` subtitle in `text-muted`. Right side: secondary actions + primary page-level CTA.
- **KPI strip (4 cards):** single bordered container with vertical dividers (not 4 separate cards). 22px values, 12px labels, 11px sub-line for context. Distinctive Tesote pattern — keep it.
- **Tabs:** segmented horizontal control with count badges. Live above filter row.
- **Filter row:** `[Filter ▾]` + `[Group ▾]` dropdowns left, search right. 13px font, 7px radius.
- **Table:** 5–8 columns. 11.5px uppercase header in `text-muted`. **Row height varies by task** — 36 browse / 44 manage / 52 review-and-decide (see Density spec above). No zebra striping, hover-reveal only. No sticky header in v1.
- **Row anatomy (left to right):** identity cell (avatar + name + sub) → data cells → status pill → action button. Action column always rightmost, center-aligned, fixed 96px button.

**Tesote examples:** Pagos, Cobros, Contrapartes, Bancos, Transacciones, Conciliaciones, Categorías, Reglas.

**Variants:**

- **No-KPI list:** drop the KPI strip when the data isn't summable (e.g., bank list).
- **Grouped list:** rows clustered by header (e.g., transactions by date). Group header is sticky.
- **Selectable list:** add checkbox column at the very left; surfaces a sticky action bar at the bottom when ≥1 selected.

**Notes:** Pagination UX is the biggest gap. Default: load 50, "Show more" button at bottom. Server-side filter does the heavy work.

---

### 2 · Detail / Record

**Purpose:** Inspect and edit a single record without losing context of the list it came from.

**Decision REVERSED 2026-06-11 (Luis's v3 design pass): full-page detail with back-link, not slide-over.** Parity-first ruling — the live web app opens a whole page per record, and this iteration matches it to keep the eng transition low-stress. Spec + reference impls: [[web-app-design-system]] §15 / `unified-app-v4.html`. The slide-over anatomy below is preserved as documentation for possible future quick-glance uses, but no current surface ships it.

~~**Decision: slide-over panel, not full-page navigation.**~~ (original 2026-05-14 take — superseded)

**Wireframe:**

```
┌──────────┬───────────────────────────────────────┬──────────────┐
│          │   (list page, dimmed, still visible)  │ ✕            │
│ Sidebar  │                                       │              │
│          │                                       │  Record Name │
│          │                                       │  meta · meta │
│          │                                       │              │
│          │                                       │  ─────────── │
│          │                                       │  Section     │
│          │                                       │   field: val │
│          │                                       │   field: val │
│          │                                       │  ─────────── │
│          │                                       │  Section     │
│          │                                       │   ...        │
│          │                                       │              │
│          │                                       │  ─────────── │
│          │                                       │  [Secondary] │
│          │                                       │  [Primary  ] │
└──────────┴───────────────────────────────────────┴──────────────┘
                                                   ↑ 460px panel
```

**Anatomy:**

- **Slide-over panel:** 460px wide, fixed right, full viewport height, slide+fade in. Backdrop dims list but doesn't blur.
- **Panel header (sticky top):** close button (30×30, top-right), record title (22px Inter Tight SemiBold), metadata row (13px `text-muted`, dot-separated).
- **Panel body (scrollable):** stacked sections. Each section: 11px uppercase label → field rows. Field row anatomy: 12px label on left (40% width), 13px value on right. Inline-edit on click.
- **Panel footer (sticky bottom):** right-aligned actions. Primary CTA (filled), secondary (ghost). 56px height, 1px top border, white bg.

**Tesote examples:** counterparty detail, invoice detail, transaction detail, bank account detail, claim detail.

**Variants:**

- **Read-only panel:** drop the footer, no inline edit. Use for "history" views.
- **Full-page detail:** reserved for records too complex for 460px (e.g., a multi-section client dashboard). Avoid unless slide-over genuinely doesn't fit — full-page costs context.
- **Side-by-side panel:** two stacked records (compare counterparties, side-by-side claims). Defer to v2.

---

### 3 · Form / Flow-step

**Purpose:** Create or modify a record through a structured multi-step flow. Distinct from detail/record because the user is *building* something, not browsing it.

**Wireframe:**

```
┌─ topbar (56px) ───────────────────────────────────────────────────┐
│  T  Pagar factura                                              ✕  │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│                      ●━━━━━●━━━━━○━━━━━○                          │
│                    Datos  Banco  Revisar Listo                    │
│                                                                   │
│                   ┌─ Content (max-w 520px) ─┐                     │
│                   │                          │                     │
│                   │  Step Title (22px)       │                     │
│                   │  Step subtitle (13.5px)  │                     │
│                   │                          │                     │
│                   │  ┌─ SECTION LABEL ────┐  │                     │
│                   │  │ field              │  │                     │
│                   │  │ field              │  │                     │
│                   │  └────────────────────┘  │                     │
│                   │                          │                     │
│                   │  ┌─ SECTION LABEL ────┐  │                     │
│                   │  │ field              │  │                     │
│                   │  └────────────────────┘  │                     │
│                   │                          │                     │
│                   └──────────────────────────┘                     │
│                                                                   │
├───────────────────────────────────────────────────────────────────┤
│  ┌─ Sticky footer (56px) ───────────────────┐                     │
│  │                         [Atrás] [Continuar →]                  │
│  └────────────────────────────────────────────────────────────────┘
└───────────────────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Full-screen overlay** (z-index above app shell). 56px topbar, scrollable body, 56px sticky footer.
- **Topbar:** Tesote mark + flow title (left), close button (right). No sidebar — the flow is a focused task.
- **Step indicator:** horizontal dots (22px circles), connected by 1.5px lines. Inactive/active/done states. Step label 12px under each dot. Centered, 28px below topbar.
- **Step title:** 22px Inter Tight SemiBold + 13.5px subtitle in `text-muted`. Left-aligned within the 520px column.
- **Content column:** **max-width 520px, single-column.** Multi-column forms are visually noisy and slow to scan — break into stacked sections instead.
- **Sections:** white card, 1px `gray-200` border, 12px radius, 18px padding. 11px uppercase section label → fields stack inside.
- **Field anatomy:** 12px label → 13px input. Inputs: 9px / 12px padding, 1px border, 4px radius, focus ring in `blue-700` 12% alpha.
- **Footer:** sticky bottom, right-aligned actions. Primary `[Continuar →]` always on the far right. `[Atrás]` ghost button when applicable.

**Tesote examples:** pay an invoice (claim-flow), onboard a bank, add counterparty, create a recurring rule, submit a dispute, request capital.

**Variants:**

- **Single-step form:** drop the step indicator, keep the rest. Used for quick creates (add note, edit category).
- **Embedded form (no overlay):** if the form is part of a settings page, render inline at 520px max-width. Skip the topbar/footer chrome.
- **Long-form:** if a flow has >5 steps, consider breaking into 2 connected flows. >7 steps is a smell.

---

### 4 · Dashboard

**Purpose:** First impression on load. Status-at-a-glance + jump-off points to deeper work. The opposite of List — it's *summary*, not *enumeration*.

**Wireframe:**

```
┌──────────┬─────────────────────────────────────────────────────┐
│          │  Hola Luis, buenos días                              │
│ Sidebar  │  martes 14 de mayo · resumen del día                 │
│          │                                                      │
│          │  [Pagar] [Cobrar] [Transferir] [Subir factura] […]   │
│          │                                                      │
│          │  ┌──────────────────────────┬───────────────────┐    │
│          │  │ SALDO TOTAL              │ CUENTAS           │    │
│          │  │                          │                   │    │
│          │  │  Bs. 1.245.890,50        │ ◯ Mercantil 800k  │    │
│          │  │  ╱╲  ╱╲     ╱╲           │ ◯ BNC      320k   │    │
│          │  │ ╱  ╲╱  ╲╱╲╱  ╲╱╲         │ ◯ Banesco  85k    │    │
│          │  │  spark chart             │ ◯ BBVA      40k   │    │
│          │  └──────────────────────────┴───────────────────┘    │
│          │                                                      │
│          │  ┌──────────────────────────┬───────────────────┐    │
│          │  │ ACTIVIDAD RECIENTE       │ NEGOCIOS          │    │
│          │  │                          │ PENDIENTES        │    │
│          │  │ • $X paid to Vendor A    │                   │    │
│          │  │ • $Y received from B     │ ⚠ 3 vencidas      │    │
│          │  │ • Reconcile completed    │ ⏱ 8 por vencer    │    │
│          │  │ …                        │ ✓ 12 aprobadas    │    │
│          │  └──────────────────────────┴───────────────────┘    │
└──────────┴─────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Greeting (page header replacement):** 26px "Hola [Name], [time-of-day]" + 13px date/context line. No CTA on the right — the quick-action row is the CTA.
- **Quick-action row:** 4–6 pill buttons in `qaction-row` style. Primary (filled blue) for top action; rest are secondary. Wrap to next line on narrow viewports.
- **Card grid:** 2×2 (or 2×N) grid of dashboard cards. Each card: white bg, 1px `gray-200` border, 12px radius, 22px padding, 14px card title in `text-muted` uppercase 11px label above.
- **Big-number card:** 28px value (Inter Tight Bold, tabular-nums) + small spark chart (96px tall, full-width inside card).
- **List-within-card:** for "Cuentas" / "Actividad" — mini list, 4–6 rows max, no headers, smaller row height (32px), `[Ver todo →]` link at bottom of card.

**Tesote examples:** Inicio (workspace home), Cobros dashboard, Capital dashboard.

**Variants:**

- **Tier-conditional:** show different cards depending on which Tesote modules the workspace has enabled (CP user vs full workspace). The prototype handles this with `.hide-cp` / `.hide-workspace` class toggles — keep that pattern.
- **Empty dashboard:** if there's no data yet, replace cards with onboarding archetype (see #6).

---

### 5 · Empty state

**Purpose:** Tell the user *why* they're seeing nothing and what to do next. Lives **inside** a list/detail/dashboard — it's not a standalone destination.

**Wireframe:**

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   (page header & filters still visible)          │
│                                                  │
│   ┌─ Empty container (centered) ─────────────┐   │
│   │                                          │   │
│   │              ┌──────────┐                │   │
│   │              │   icon   │                │   │
│   │              └──────────┘                │   │
│   │                                          │   │
│   │           Title (22px)                   │   │
│   │           Body (13px, text-muted)        │   │
│   │           max-width 360px                │   │
│   │                                          │   │
│   │           [Primary CTA →]                │   │
│   │                                          │   │
│   └──────────────────────────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Anatomy:**

- **Container:** centered in the would-be data region. 80px top padding minimum. White bg, no card border (the page already provides container chrome).
- **Icon:** 48px square, `gray-50` background, 12px radius, simple line icon (1.5 stroke). Not colorful — empty states should feel quiet.
- **Title:** 22px Inter Tight SemiBold. One sentence, action-oriented ("No tienes facturas por pagar" — not "Empty").
- **Body:** 13px in `text-muted`. Max-width 360px to force one-line readability. Explain *why* it's empty and what fills it.
- **CTA:** one primary action max. Optional secondary ghost link below.

**Variants:**

- **No-data empty** ("you have 0 records"): action = create the first.
- **Filtered-to-zero empty** ("your filter returned 0"): action = clear filter. Icon is more neutral.
- **Locked / not-yet-enabled** (e.g., `screen-conectar-erp`): action = enable / contact / upgrade. Title is more "this is coming" than "do this now."
- **Error state**: red icon background, retry CTA. Treat as a sibling pattern.

**Notes:** Don't reuse onboarding visuals here. Onboarding teaches a new user; empty state addresses an existing user with a temporary gap.

---

### 6 · Onboarding

**Purpose:** First-run experience that orients a new user/workspace to Tesote. Distinct from form/flow — it teaches *the product*, not a record action.

> No prototype exists yet. This is the only archetype defined forward, not extracted. Treat the spec as provisional until we ship a real one.

**Wireframe:**

```
┌───────────────────────────────────────────────────────────────┐
│  T  Bienvenido a Tesote                              [salir]  │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   ●━━●━━○━━○━━○                                               │
│   Step 1 of 5                                                 │
│                                                               │
│              ┌─ Content (max-w 640px) ────────┐               │
│              │                                 │               │
│              │   Big title (28px)              │               │
│              │   Supporting copy (16px)        │               │
│              │   max-width 480px               │               │
│              │                                 │               │
│              │   [    Inline illustration    ] │               │
│              │   [    or interactive demo    ] │               │
│              │                                 │               │
│              │   ── optional: small form ──    │               │
│              │   field                         │               │
│              │   field                         │               │
│              │                                 │               │
│              └─────────────────────────────────┘               │
│                                                               │
├───────────────────────────────────────────────────────────────┤
│                          [Saltar]  [Continuar →]              │
└───────────────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Full-screen overlay**, like form/flow, but **wider content column (640px)** to make room for illustration/explanation. Forms are 520px; onboarding is bigger to let the design breathe.
- **Step indicator:** identical to form/flow, but with copy "Step N of M" for clarity.
- **Title size:** 28px (vs 22px in form) — onboarding is meant to feel ceremonial, not transactional.
- **Body copy:** 16px (not 13px) — easier reading for new users, less scanning.
- **Visual:** every step should have an image, illustration, or interactive demo. Text-only onboarding fails.
- **Form fields if any:** stacked, max 3 per step. Heavy data collection belongs in form/flow, not here.
- **Footer:** `[Saltar]` link on left (ghost) + `[Continuar →]` on right. Saltar exits to dashboard with onboarding flagged-incomplete; returns user later via a banner.

**Tesote examples:** new workspace setup, first bank connection, first counterparty import, Tesote IA introduction.

**Variants:**

- **Inline tour:** non-overlay version that walks the user through a real screen using tooltips/spotlights. Defer — overlay-first is simpler.
- **Module activation onboarding:** when a workspace enables Capital or IA for the first time. Same template, scoped to that module.

---

## Shared primitives (preview — next doc)

Every archetype above is composed of the same ~10 primitives. Naming them here so the next doc has scope:

1. **Page header** (title + sub + right-aligned actions)
2. **Row** (identity cell + data cells + status + action)
3. **Cell** (typography rules per data type: amount, date, name, status)
4. **Status pill** ✅ already locked in [[design]]
5. **Button** (primary / secondary / ghost / destructive · sm / md)
6. **KPI card strip** (unified 4-col container)
7. **Filter system** (pill row + `+ Filtrar` builder + dimension popovers + saved views) — Mercury-style. **Shared across every Tesote table.** Canonical reference impl: [[../connect/movimientos/prototypes/movimientos-v5]]. Full spec at [[../connect/movimientos/design#filter-system-full-spec]]. The shell (filter row layout, pill anatomy, two-step popover engine, saved-views dropdown + persistence, general search input) is reused; the dimensions and per-dim inputs are per-page. New tables declare their dim set, reuse the shell. See [[project_filter_system_primitive]].
8. **Tab control** (segmented, with count badges)
9. **Side panel** (header + scrollable body + sticky footer)
10. **Form field** (label + input + helper text + error)
11. **Section block** (uppercase label + body, for forms and detail panels)
12. **Empty container** (icon + title + body + CTA)

Each gets a small spec doc: anatomy, variants, tokens, when-to-use. Probably 1–2 pages each. Next doc.

---

## Open questions

1. **Sticky table header?** Worth it for long lists but adds engineering cost. My default: ship without, add later. Override?
2. **Pagination UX.** "Show more" button vs page numbers vs infinite scroll. My default: "Show more" — cheapest, most consistent with operator-software conventions.
3. **Multi-select bulk actions in lists.** Spec'd as a variant above, but not in the prototype. Worth scoping for v1?
4. **Dashboard customization.** Can users rearrange cards? Default: no (keeps the spec tight). Add only if power users ask.
5. **Dark mode.** Out of scope for v1. Confirm.

## Next steps

1. **Sign-off on this doc.** Mark archetypes locked or push back on density / layout choices.
2. **Draft the primitives doc** (`product/design/primitives.md`) — spec each of the 12 above. Probably 1 week of design work.
3. **Apply primitives back to PRO-112 prototypes** — the punch list in [[workspace-design-decisions]] becomes concrete once primitives exist.
4. **Pick one non-prototyped archetype to validate the system** — I'd nominate the dashboard (`screen-inicio`) since it's the most composed of primitives and the hardest to get right.

---

*Drafted 2026-05-14 from canonical reference `workspace-shell284.html` + `claim-flow.html`. Update as decisions land.*
