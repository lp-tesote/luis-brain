---
title: Tesote Web App — Design System (page rules)
tags: [design, product, web-app, design-system]
updated: 2026-06-11
status: ready-for-kb — v4 frozen 2026-06-11 (Luis sign-off); this doc + unified-app-v4.html = the eng contract
audience: Luis, Dan, Majo
---

# Tesote Web App — Design System

> **One source of truth for rules that apply to *every page* of the Tesote web app.** Hoisted from the three locked surfaces — Saldos v4, Movimientos v7, Dashboard v4 — so the next page doesn't re-derive them.
>
> This is **page-composition rules**, not brand tokens. It sits *on top of* the existing design files:
>
> | File | Owns |
> |---|---|
> | [[design]] | Brand tokens — colors, type families, radii, pill hexes. Also feeds `/pdf`, `/proposal`, marketing. |
> | [[archetypes]] | Six screen archetypes + density spec (row heights, font scale, table padding). |
> | [[workspace-design-decisions]] | PRO-112 migration punch list (historical audit). |
> | **this file** | How a Tesote app page is *composed* — shell, cards, currency, charts, filters, AI panel, affordances. |
>
> **Rule of precedence:** tokens → `design.md`. Density/archetype → `archetypes.md`. Everything about how a page hangs together → here. Where a prototype diverges from this file, **this file wins** — see [§18 Known drift](#18-known-drift-to-reconcile).
>
> **Reference implementations** (open these, don't reinvent):
> - **`product/design/unified-app-v4.html`** — the canonical unified app, **fully walkable + post-design-pass**: 33 pages (record details are full pages), país-first bank connect, 9 modals, reachable empty states, zero dead CTAs. This is the **design sign-off artifact** — the eng-handoff contract once frozen. **Start here.**
> - `unified-app-v3.html` (Luis's review pins live here) · `v2` · `v1` — prior builds, superseded; kept per versioning convention.
> - `product/design/treasury-recon-2026-06.md` — production ground truth the prototypes were designed against (routes, enums, fields, gates).
> - `product/dashboard/prototypes/dashboard-v5.html` — frozen Inicio (most detailed single surface)
> - `product/connect/saldos/prototypes/saldos-v4-retrofit.html` · `product/connect/movimientos/prototypes/movimientos-v7-retrofit.html` — original surface prototypes (pre-unification)

---

## 0. Hard constraints (non-negotiable, apply everywhere)

These override anything below. If a design choice fights one of these, the constraint wins.

- **Parity-first (this iteration — Luis, 2026-06-11).** The redesign keeps **UX parity with the live web app**: same pages, same flows, same capabilities — redesigned skin, not re-architected behavior. Anything that adds/changes UX structure (new buttons, removed flows, slide-overs vs pages) is a *parked decision*, not part of this iteration. Rationale: don't add stress to the eng transition.
- **VE Spanish, `tú`.** Product UI copy is Venezuelan Spanish, second person `tú` — never `vos` (AR). Sweep entire screens for dialect consistency, not just the line you touched. Per [[feedback_product_ui_spanish_venezuelan]].
- **No emojis. Inline SVG only.** Every glyph in a user-facing surface — sidebars, filters, indicators, empty states, buttons, modal headers, AI feed icons — is an inline SVG. Per [[feedback_no_emojis]].
- **Lunour tokens only. No Tailwind, no Mercury hexes.** Every color comes from the [[design]] ramps. Mercury was layout/density inspiration, never a token source.
- **Borders, not shadows, for elevation.** A 1px `gray-200` border. Shadows only for true overlays (modals, dropdowns).
- **Radii: 4 / 8 / 12.** Tags/inputs/pills → 4. Cards → 8. Large surfaces/modals → 12. No 5/6/7/10/14 in product UI.
- **Always-visible affordances.** Row-action and inline-edit affordances render always-visible (low-key at rest, primary on hover). Never hover-only reveal. Per [[feedback_always_visible_affordances]].

---

## 1. Typography roles

Four families, four jobs. (Token definitions live in [[design]]; this is the *role assignment* for the app.)

| Role | Family | Where it's used |
|---|---|---|
| **Display** | Inter Tight | Page titles, headings, card "big numbers" that aren't tabular, brand wordmark, bank/avatar bubbles. `letter-spacing: -.01em`. |
| **Body / UI** | Aspekta (fallback Inter) | Default body, table cells, labels, buttons, form inputs. 13–14px. |
| **Numbers / tabular** | **Geist Mono** | Every number that lines up in a column or wants tabular alignment: amounts, balances, dates, percentages, account last-4, chart axis labels. `font-variant-numeric: tabular-nums`. |
| **Tesote AI voice** | Instrument Serif | *Only* the Tesote AI panel's lead/voice line (Claude-style). Never used for chrome, labels, or data. See [§16](#16-tesote-ai-panel). |

**Number-font rule (locked, supersedes Saldos v4):** all tabular figures render in **Geist Mono**, not Inter Tight. Movimientos v7 and Dashboard v4 are correct; Saldos v4's KPI amounts in Inter Tight are [drift](#18-known-drift-to-reconcile).

Font scale is `11 / 12 / 13 / 14 / 16 / 18 / 22 / 28` — no half-pixels. Per-size assignment in [[archetypes]]. Default body / cell / input = 13px. Full-page title = 26px.

---

## 1b. Color roles (locked 2026-06-09)

The accent color is a **budget** — spend it to direct the eye. If everything interactive is blue, nothing is. So each color has one job:

| Role | Color | Where |
|---|---|---|
| **Brand + foundation** | black `gray-1000` / white / cream `gray-50` | ~90% of every screen: surfaces, text, structure |
| **Primary action** | **black** (`gray-1000`, hover `gray-900 #302C25`) | **every** primary button — "Mover dinero", "Aplicar Filtros", "Ver conexiones", AI send. *Never blue.* |
| **Interactive accent** | **blue `blue-700 #1661E2`** | links, focus/keyboard ring, operable controls, a **modification you made** (applied filter chips), changed-from-default signals (active-filter count), key data points / chart line, new/unread |
| **Status (semantic)** | green / yellow / orange / red | **small doses only** — dots, icons, pills, number text |

**The teachable line: blue = "act or find"; neutral = "you are here / structure".**

- **Navigation active state is NEUTRAL, never blue.** "You are here" is ambient, persistent location — felt, not shouted (a loud blue pill competes with content all day). Active nav = subtle gray fill + black text + 500 weight. Same for selected tabs, table-row selection.
- **Applied filter chips + active-filter count = blue** (they're modifications you made / changed-from-default). **Ambient counts** (e.g. "Filtros Guardados · 3") = neutral gray.
- **Status pastels are for status only.** A category/taxonomy label never borrows a status color (no `Software`→orange, no `Cobros`→blue) — category chips are neutral. See [§12](#12-pill-family--status-vs-category-locked-2026-06-09).
- **Two hard rules (never again):**
  1. **No large semantic fills.** Warning/success/etc. never fill a banner or big surface. An attention banner = neutral surface + a black icon (or a small semantic dot), never a yellow slab. Per Lunour's 50/20/20/10 ratio — accents don't dominate.
  2. **No colored edge-strips on containers** (no 3px left bars in a semantic color).

Reference impl: `product/design/unified-app-v1.html`.

---

## 2. The app shell

The frame is identical on every page. Build it once as a layout, never per-page.

```
┌──────────┬───────────────────────────────────────┐
│ sidebar  │ topbar (entity switcher · spacer · CTA)│
│ (cream,  ├───────────────────────────────────────┤
│  224px)  │ content (white, centered, max-width)   │
│          │   page-head                            │
│ Connect  │   …cards / tables…                     │
│ Business │                                        │
│          │                                        │
│ user ▾   │                                        │
└──────────┴───────────────────────────────────────┘
```

- **Grid:** `224px 1fr`, `min-height: 100vh`.
- **Sidebar:** background `gray-50` cream (`--bg-sidebar #F7F5F0`), `border-right: 1px gray-200`. Holds: brand lockup (`T` logomark + "Tesote" + `PRO` chip) → search (`⌘K`) → sectioned nav → user block pinned to bottom (`margin-top: auto`).
  - **Nav sections** carry uppercase 11px labels: **Connect** (Saldos · Movimientos · Conexiones) and **Business** (Pagos · Cobros · Contrapartes). Item = 13px, icon + label, optional right-aligned count pill. Active = `--active` fill + 500 weight; hover = `--hover` fill.
- **Main:** white background (`--bg-main`). The cream/white split is **sidebar cream, content white** — this is the locked convention (Saldos v4's white sidebar is [drift](#18-known-drift-to-reconcile)).
- **Topbar:** 52px, `border-bottom: 1px gray-200`. Left = **entity/workspace switcher** ("Todas las entidades · 2 ▾"). Right = primary page CTA (e.g. "Mover dinero") + notification/help icons.
- **Content:** `max-width` ~1280–1440px, centered (`margin: 0 auto`), padding ~`26–32px 36px 60px`. Dashboards run narrower (1280), dense tables wider (1440).

---

## 3. Workspace identity in the page head

Locked Dashboard v4 decision — applies to any page with a page-head greeting.

- **Workspace = the protagonist of the header.** Logo slot (uploadable workspace mark) + workspace **name** ("Tesote Ventas"), optional `● En vivo` status. *Not* a personal "Hola, Mariel" greeting.
- **Personal identity lives in the sidebar** user block (avatar + name + role).
- **The AI greets by name** in its panel ("Buena semana, Mariel…") — that's where the personal touch goes, not the page head.
- The logo is a real uploadable mark per workspace; render a generated monogram as fallback.

---

## 4. Card & section primitives

One card primitive. One section-divider primitive. Reused everywhere.

- **Card:** white, `border: 1px gray-200`, `border-radius: 12px`, padding ~`18px 20px`, `display: flex; flex-direction: column`. No shadow.
- **Card head:** title is **uppercase 11px `gray-600`, letter-spacing .06em**. Optional **range sub-label** directly beneath in 11px `gray-500` (this is where the time window goes — see [§9](#9-explicit-time-window-labeling)). Right side = a `card-link` ("Ver Movimientos ↗") or a `⋯` menu.
- **In-card section divider:** uppercase 11px label with a `1px border-top` hairline in `border-2` (`#F2EEE6`). Use `.sec.flush` (no top border) for the first section so it doesn't double-rule against the card head.
- **Grid:** cards live in a `display: grid; gap: 16px`. Common layouts: `grid-hero` (≈1.6fr / 1fr — main box + AI panel), `grid-3` (KPIs), `grid-2` (1.25fr / 1fr), `grid-1` (full-width list).

**Chrome discipline** (Dashboard v4 ruling — applies everywhere):
- Kill labels that repeat what columns already say (no "Desglose" header above self-labeled columns).
- Keep only **load-bearing** dividers. The chart→band hairline stays; redundant rules between tight rows go.
- Tighten gaps so a box and its neighbor (e.g. position box + AI panel) **read end-to-end on load**, not as two stacked islands.

---

## 5. Multi-currency display

The most-repeated rule in the app. Get this identical on every surface.

- **USD is the consolidated protagonist.** Top-line "posición total" and any cross-currency rollup is shown in **USD** (`$`).
- **VES is shown Bs-first.** Wherever a bolívar balance appears, the **Bs amount is the primary (larger) number**, with the dollarized **`≈ $X` directly beneath** in muted Geist Mono. Never lead a VES balance with its dollar equivalent.
- **The BCV rate is the conversion basis but recedes.** Show it as quiet meta (`Tasa BCV: 1 USD = … · dd/mm/aaaa`) under a currency card; never as a headline figure.
- **Devaluación always lives on the VES side.** FX-loss decomposition attaches to bolívar balances/flows, never to USD.
- **Long Bs amounts auto-step down.** 10-digit bolívar figures overflow a card — step the font down (28px → 22px, cents 18px → 15px) when the integer portion exceeds ~13 chars. `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`.
- **Empty/zero:** render `—` in muted weight, not `$0,00`.

Per [[feedback_marketing_mock_data_rules]] for mock data: USD protagonist, numbers reconcile at the displayed BCV rate, rate itself never the hero.

---

## 6. Numbers & amounts

- **Geist Mono, `tabular-nums`**, right-aligned in table columns.
- **Integer/decimal split sizing:** the integer part is the heavier/larger size; the decimals (`,89`) ride smaller and lighter (`opacity ~.6`). Same pattern for cents on big hero figures.
- **Sign + direction color:** credits/inflows use `green-text` (`#0F6E45`); debits/outflows stay ink (`gray-1000`). Lead credits with `+`, debits with `−` (the real minus glyph, not a hyphen).
- **Currency tag:** an optional small uppercase `VES`/`USD`/`EUR` chip after the amount (10px, `bg-soft`, 3px radius) — use in mixed-currency tables (Movimientos) where the column carries multiple currencies.
- **Locale formatting:** VES uses `de-DE` grouping (`23.851.234.567,89`); USD/EUR use `en-US` (`411.253,69` → `$411,253.69` style only if you flip locale — match the prototype: Bs uses dot-thousands/comma-decimal, `$` mirrors it). Keep it consistent per currency.

---

## 7. Charts + decomposition-band reconciliation

When a box shows a trend chart *and* a flow breakdown, **they must reconcile to the same arithmetic.** This is a correctness rule, not a style one.

- **Position chart:** large gradient **area** chart over the window (30 d). The **beginning balance is marked on the curve** — a start dot + its value label, with **no "hace 30 d" caption**. Current point is a dotted/filled end marker.
- **Decomposition band** sits directly under the chart, separated by the one kept hairline. Order is fixed: **Entró · Salió · Variación neta · Devaluación.** "Variación neta" gets visual emphasis.
- **The reconciliation must hold and be checkable:**
  `begin + entró − salió … = variación neta`, and `begin + neta − devaluación = today`, and `today − begin = the "+$X · 30 d" delta chip.`
  In the reference: `490.550 + 33.190 − 1.900 = 521.840 = +31.290 · 30 d`. If your mock numbers don't close, the box is wrong.
- **Devaluación is the bridge term** between flow-neutral variation and actual ending balance — it's why "money in − money out" ≠ "balance change" in a bolívar economy. Always present it; never fold it silently into "salió".

> **Backend reality:** Δ-decomposition (flujos vs devaluación vs ε), cash-flow-by-category (direct method), and recurrence detection are **not shipped primitives** — the prototypes mock them. Any PRD that uses these must flag them as net-new eng. See [[../dashboard/prototypes/README]] and the daily-position-pack PRD.

---

## 8. Explicit time-window labeling

Every time-bound box **states its own window**, visibly. No globally-assumed period.

- Window goes in the **card range sub-label** under the title: "Esta semana · 02–08 jun 2026", "Últimos 30 días · 234 movimientos", "Este mes · método directo".
- **Different boxes can run different windows on the same page** — and must, when the data demands it (position chart = 30 d, entró/salió KPI = the *week* with explicit dates, cash-flow = the *month*). This is intentional, not a bug.
- **Guard against window bleed:** don't let a weekly KPI accidentally show the 30-day band's exact numbers. Each window is its own computed subset. (This was a real bug caught in Dashboard v4.)
- Decide the multi-window data story (30 d / week / month) **deliberately at PRD time** — don't let it fall out of whatever query was easy.

---

## 9. List vs grid conventions

- **Saldos por cuenta = a list**, not a grid of cards. Accounts are a ranked, bar-backed list (logo + name + meta · share-of-total bar · value + %). One row per account, full-width card.
- **Cards in a grid** are for *distinct metrics* (KPIs, the position hero, the AI panel) — things you compare side-by-side, not scan top-to-bottom.
- **Rule of thumb:** homogeneous, rankable, "more of the same" → **list**. Heterogeneous, "different things I glance across" → **grid of cards**.
- Within a list, a **share-of-total mini-bar** (6–8px track, `bg-soft` ground, brand/`ves-bar` fill) is the standard way to show relative weight.

---

## 10. Filter-builder primitive

**Movimientos is the reference implementation** ([[project_filter_system_primitive]]). Every table that filters uses this shape — not bespoke per-page filter bars.

- **Trigger row:** a `Filtros` toggle button with a **count badge** of active filters, alongside `Filtros Guardados` (saved presets, also count-badged), `Exportar`, and a right-aligned full-text **search** field.
- **Collapsible panel** (`.filter-panel`, hidden until toggled): sectioned filter builder — Movimientos groups into **Compañías/Cuentas/Bancos · Contrapartes/Categorías · Monto y Financiero · Detalles de Transacción**. Each section is a labeled grid of multi-selects, selects, segmented controls, radio groups. Panel footer = `Restablecer` + `Aplicar Filtros`.
- **Applied-chips row** below the bar: one chip per active filter (`Dimensión · valor ✕`), each removable; a `Limpiar` clear-all. Removing the last chip hides the count badge.
- **"Filtrado" tag** propagates to summary/totals cards when a non-default filter is active, so the user knows a number is a filtered subset.
- The **legacy 5-fixed-pill bar in Saldos v4 is drift** — it predates this primitive and should migrate. See [§18](#18-known-drift-to-reconcile).

---

## 11. Table & row affordances

- **Density per task, not per page** (browse 36 / manage 44 / review-and-decide 52). Padding tokens per density are in [[archetypes]]. Don't drift table-to-table.
- **Header:** uppercase 11px `gray-600` on `bg-soft`, `border-bottom: 1px gray-200`. Sortable columns get a dotted-underline sort link with a ↓/↑ indicator. Numeric headers right-align.
- **Cells:** 13px, `vertical-align: middle`, `border-bottom: 1px border-2`. Last row drops its border. Row hover = `bg-soft` fill. Whole row is clickable when it drills in (`cursor: pointer`).
- **Always-visible affordances** (per [[feedback_always_visible_affordances]] — restating because it's load-bearing):
  - **Inline-edit cells** (Contraparte, Categoría) render as a low-key clickable affordance *at rest* — visible caret, subtle padding box — that lifts to a `hover` background + primary caret on hover. Empty values show `—` in muted text but are still obviously clickable. **Never** reveal the edit control only on hover.
  - **Row actions** (share/paperplane, sync) are visible buttons at rest, primary on hover. Disabled state = reduced opacity + `not-allowed`, not hidden.
- **Group headers** (grouped tables): a tinted `bg-soft` row spanning all columns — group name + count meta + right-floated subtotals in Geist Mono.
- **Pagination / footer:** per-page selector + range info + prev/next, on `bg-soft` with a top border.
- **Empty state:** centered icon bubble + 14px title + 12px sub. Inline SVG icon, never emoji.

---

## 12. Pill family — status vs. category (locked 2026-06-09)

**One pill primitive, one shape: 4px filled tag.** Shape is *not* a signal — it never encodes editability or state. The locked grammar uses **color + dot + caret** to separate the two kinds of pill, while shape stays constant:

| Pill | Treatment | Means |
|---|---|---|
| **Status** | **colored pastel fill** + leading colored **dot**, no caret | a state the system assigned — read-only (synced, requiere atención, manual…) |
| **Category** | **neutral `pill-draft` fill + a colored *category* dot** (own palette, not status pastels), + always-visible **caret** when editable | a taxonomy label — the hue is in the dot, so categories stay quieter than status (Cobros, Software, Nómina…) |

- **Why shape isn't the signal (the gut-check, settled):** the always-visible **caret** already carries "you can edit this" ([§11](#11-table--row-affordances), [[feedback_always_visible_affordances]]). Making *shape* a second editability signal is redundant and breaks on a real counterexample — the **same** category token renders editable in Movimientos but read-only on Inicio's "Nuevo en tus cuentas". A "rounded = editable" rule would force the same token into two shapes by screen, fragmenting the primitive. So: caret = editable, shape = constant 4px. A 999px capsule also violates the radius scale ([§0](#0-hard-constraints-non-negotiable-apply-everywhere)).

**The five locked Tesote pastels** (from [[design]] → Product UI extension; don't substitute Lunour `100` ramp shades) — these are **status colors, reserved for state**:

| Token | Hex | Use |
|---|---|---|
| `pill-paid` | `#D6E8D5` | Paid · success · completed · synced |
| `pill-new` | `#E4ECF7` | New · sent · informational · syncing |
| `pill-pending` | `#F7EDD0` | Pending · awaiting action · needs attention |
| `pill-overdue` | `#F8D8C0` | Overdue · late · error |
| `pill-draft` | `#ECE7DD` | Draft · manual · inactive · **neutral (also the category-chip fill)** |

- **Status shape:** filled background, **`gray-1000` text, no border, 4px radius**, leading 6px **dot** in the family's strong color (paid→`green-600`, new→`blue`, pending→`yellow-600`, overdue/error→`orange-700`, draft→`gray-600`).
- **Category chip:** same 4px filled shape, **neutral `pill-draft` fill (no border) + a colored *category* dot**. Categories are taxonomy, not status — **never** borrow a status pastel to color a category (a `Software` category is not in an "error" state, a `Cobros` category is not "new"). Categories have their **own dot palette** ([[design]] → Category-tag palette: `cat-green`/`cat-blue`/`cat-purple`/`cat-orange`/`cat-yellow`/`cat-red`/`cat-gray`), pulled from the Lunour ramp `600` shades, **stable per category**, falling back to `cat-gray` when unmapped. The hue lives in the **dot only** — the chip fill stays neutral — so categories read *quieter* than the filled status pills (right hierarchy: status is acted on, category is ambient). Fixed in `unified-app-v1.html` (was status-color drift). More categories than hues is fine — reuse a hue across related categories; the label disambiguates.
- **Radius is 4px**, not pill-rounded, for both. Movimientos v7's 999px status pills are [drift](#18-known-drift-to-reconcile). (Count *badges* and filter *chips* may be fully rounded — those aren't pills.)
- Sixth status? Derive it the same way (Lunour ramp `100`, +5% lightness, −20% chroma) and add it to `design.md` first. Don't invent a hue.
- **Semantic mapping across surfaces (locked 2026-06-10 in v2).** Map every page's states into the five families — don't invent per-page pills: **paid** = Activa · Completado · Activo · Sincronizada · Verificado/Al día; **new** = Pendiente (setup) · Procesando · Sincronizando · En revisión · Requerido (política); **pending** = Requiere atención · Pendiente (invitación/acción del usuario); **overdue** = Fallida/Fallido · error; **draft** = Pausada · Borrador · En cola · Manual · Deshabilitada. Rule of thumb: *pending* es "te toca a ti", *new* es "el sistema está en ello".

---

## 13. Bank logos & avatar bubbles

- **Bank logo bubble:** a rounded-square (4px radius) monogram, white **Inter Tight** 700 letters on the bank's brand color, ~18–24px depending on density. **Always a 2-letter monogram (locked 2026-06-09)** — never 1 letter, never 3+ — so every bubble is the same width and the VE "B" banks disambiguate. Canonical map: Mercantil `MC #006B3F` · BBVA `BB #004481` · BNC `BN #C8102E` · Banesco `BS #0067A6` · Bancamiga `BM #00A0DF` · Activo `AC #2D2A26` · Mercury `ME #2D2A26` · Banco de Venezuela `BV #16A085` · Banco Exterior `BE #6C5CE7` · Bicentenario `BT #C0392B` · Mi Banco `MB #2C3E50` · manual = `gray-500`. (Production swaps these for real brand logos.)
- **Counterparty avatar:** circular monogram, **deterministic** color from initials (hash → one of 8 palette slots) so the same counterparty is always the same color. Empty/unassigned = dashed `border` ring.
- **Entity bubble:** neutral (white bg, `gray-200` border, `gray-600` text) — entities aren't brand-colored.

---

## 14. Tesote AI panel

Lives in the **hero's right column** (~1fr beside the main box). Locked Dashboard v4 structure.

- **Name is "Tesote AI"** — English "AI", not "IA". "La IA" is marketing/colloquial only. **No "Copiloto" badge.** Per [[feedback_tesote_ai_naming]].
- **Header:** small brand-blue AI mark + "Tesote AI". That's it — no tagline chip.
- **Voice line:** one catchy **Instrument Serif** lead (~24px, italic emphasis allowed), Claude-style, greets the user by name and states the headline insight ("Buena semana, Mariel — tu posición sigue en *máximos*.").
- **Week-to-date report:** an uppercase section label ("Tu semana hasta hoy") over an **insight-led feed** — 3–4 items, each a small inline-SVG icon (up/fx/new/warn, color-coded) + a one-sentence finding with the key number bolded. Insights, not a transaction dump.
- **Prompt buttons:** an uppercase "Pregúntale…" label + **exactly 3** suggested-question buttons (icon + question), tuned to the page's data.
- **Input:** pinned to the bottom of the panel via a flex spacer, so the panel can stretch to the hero's height with the input always at the floor. Placeholder "Pregúntale a Tesote AI…" + send button.
- **Audience framing:** the whole finance function (CFO/controller/AP-AR/contador) — frame copy as "finanzas", not "tesorería". Per [[project_tesote_ai_audience]]. Typography per [[project_tesote_ai_typography]].

---

## 15. Record detail pages (REVERSED 2026-06-11 — full page, not slide-over)

**Luis's design-pass ruling, governed by the parity-first principle:** *this first iteration keeps UX parity with the live web app — redesign the skin, not the architecture — to not add stress to the transition.* The live app opens a **whole page** per record; the redesign does the same.

- **Clicking a record row** (conexión, compañía, contraparte, sincronización, miembro del equipo, movimiento, settings sub-section) navigates to a **full detail page** with a `back-link` to its parent list. Sub-pages highlight the parent nav item.
- **Detail-page anatomy:** back-link → page-head with identity mark (bank logo / avatar at 38px) + 22px title + meta row (status pill + dot-separated facts) + one primary CTA right → content as **cards in `grid-2`/`grid-1`** using `dl-row` field rows (12px muted key / 13px value; `cell-edit` caret where editable) → **danger zone** as the last card ("Avanzado": neutral `bg-soft` rows, red-*text* bordered buttons, never red fills).
- **Movimiento detail** leads with the amount as hero (`detail-hero`, Geist Mono 32px, green when credit) instead of a name.
- Mini-lists inside detail cards (cuentas, métodos de pago, contratos, grupos) use the `method-card` row: icon + title/meta + optional switch/pill/chevron.
- **The 460px slide-over is deprecated for record details.** The CSS/pattern remains documented for possible quick-glance secondary uses, but no current surface uses it. (Was: "locked 2026-06-10" — reversed by the v3 design pass; supersedes [[archetypes]] §2's slide-over default.)
- Reference impls in `unified-app-v4.html`: `page-conexion-detalle` · `page-contraparte-detalle` · `page-sincronizacion-detalle` · `page-usuario-detalle` · `page-movimiento-detalle` · `page-compania-detalle`.

## 16. Settings hub (new archetype, locked 2026-06-10)

Configuración is a **hub**, not a form: grouped cards of rows that link out to sub-surfaces. Reference: `unified-app-v2.html` → Configuración.

- **Two-column grid of cards** (`hub-grid`), each card = one domain (Usuario · Seguridad · Descarga de reportes · Espacio · Transacciones · API e integraciones · Equipo y permisos) with the standard uppercase card title.
- **Hub row anatomy:** label (13px/500) + optional one-line explainer (11.5px muted) · right side = current **value** (muted) and/or **status pill** + chevron. Hover = `bg-soft` + blue chevron (act-or-find blue, §1b).
- **Inline toggles** (switch) only for true one-bit settings; anything with options links out.
- A hub row never holds a form. Editing happens in the linked sub-surface (or a modal for single fields).

## 17. Small shared patterns (minted in v2)

| Pattern | Anatomy | Where |
|---|---|---|
| **In-cell progress** | 5px blue-fill track + `64% · 1.498/2.340` Geist Mono caption. Completed → green check + result count; failed → red ✕ + reason. Blue = activity, per §1b. | Reportes |
| **Avatar stack** | Overlapping 24px circles (2px white ring), `+N` overflow bubble in mono, `N miembros` caption. Deterministic per-person colors (§13). | Permisos |
| **Copy-with-feedback** | Always-visible ghost button (clipboard icon + "Copiar enlace") → swaps to "¡Copiado!" for 2 s, disabled during. Never hover-revealed. | Mi equipo invitaciones |
| **Danger zone** | Neutral `bg-soft` bordered row: title + consequence sentence + red-*text* bordered button. No red fills, no edge strips. | All detail panels, group editor |
| **Switch** | 32×18, blue when on (operable control = blue, §1b), gray-200 off. | Hub, panel account toggles |
| **Collapsible archived** | Ghost toggle row "X archivadas (N)" + rotating caret → dense table with `Restaurar` row action. Archived content never mixes into the live table. | Conexiones, Compañías |
| **Warning sub-row** | 11px yellow icon+text line *under* the primary cell text (small-dose semantic). Never a banner inside a table. | Conexiones (scheduler desactivado) |

## 17b. Flow overlay + flow modals (updated 2026-06-11 post-design-pass)

- **Nueva conexión = parity with the live app (v4):** a **sub-page** ("Conectar un banco") with **país first — flag chips** (Venezuela · Estados Unidos · Panamá · Rep. Dominicana, per [[project_connect_multi_jurisdiction]]) → the country's **bank grid** → clicking a bank opens the **credentials modal** (compañía + usuario + clave + apodo, with the "cifrada en reposo / solo lectura" reassurance line) → lands on the connection's detail page. Flags are simplified inline SVGs (no emoji). Reference: `page-conexiones-nueva` + `modal-credenciales` in `unified-app-v4.html`.
- **Full-screen flow overlay** (the v3 wizard) is **retired for Nueva conexión** but remains the documented archetype-3 shell for future genuinely multi-step flows (pagos, onboarding): 56px topbar, centered step dots (black done-state, never blue), 520px column, sticky footer with per-step primary renaming. Reference impl preserved in `unified-app-v3.html`.
- **Bank picker:** 3-col grid of bordered options (monogram + name); selected/hover affordance per §1b. Always includes "Cuenta manual" as the last option.
- **Export modal** (the report-generation pattern): summary box of the **applied filters** + row count, editable report name (sensible default), format note ("XLSX… disponible en Historial de reportes"). Reports are *generated from the data surface* (Movimientos/Saldos "Exportar"), and "Nuevo reporte" in Historial opens the same modal — never a bespoke builder.
- **Creation modals vs. sub-pages:** single-object quick creates (tasa, clave API, unidad) = **modal**; anything with sections or consequences (invitar usuario, nueva contraparte/compañía, group editor, wizard) = **sub-page or flow overlay** with a back-link. Back-links highlight the parent nav item.
- **Prototype-only chrome:** the dashed `proto-link` ("prototipo: ver estado vacío") marks controls that exist only to demo states. Anything styled that way **never ships**.

## 18. Known drift to reconcile

Where the locked surfaces disagree. The **rule above is canonical**; these are the surfaces that need to catch up.

| # | Drift | Where | Canonical rule |
|---|---|---|---|
| 1 | Number font = Inter Tight | Saldos v4 KPI amounts | **Geist Mono** for all tabular figures ([§1](#1-typography-roles)) |
| 2 | Sidebar = white, main = cream | Saldos v4 | **Sidebar cream, content white** ([§2](#2-the-app-shell)) |
| 3 | Status pills = 999px rounded | Movimientos v7 | **4px radius** status pills ([§12](#12-status-pill-family)) |
| 4 | Legacy 5-fixed-pill filter bar | Saldos v4 | **Movimientos filter-builder** primitive ([§10](#10-filter-builder-primitive)) |
| 5 | Row height 40px (between buckets) | Movimientos v7 | Snap to density buckets 36/44/52 ([[archetypes]]) |

None block shipping the dashboard; they're the cleanup list when each surface is next touched (or when this becomes the eng spec).

---

## Terminal move

This file is the **brain seed** for the app design system. Three exits:
- **(a) keep drafting here** as more surfaces land and reveal new shared rules.
- **(b) promote to the KB** once stable (it's a genuine team reference — Majo + Dan + any designer need it). Likely a `product/design/` doc in `knowledge-base/`.
- **(c) feed `/tesote-plan` in treasury** alongside `redesign-2026-design-system` when the dashboard PRD ships — this file is the cross-page contract the implementation plan should honor.

Right now: **(a)**. Revisit after the dashboard PRD locks.
