---
title: Movimientos — Page Design
tags: [design, product, connect, movimientos]
updated: 2026-05-19
status: design-exploration (v1.1 contract = prototypes/movimientos-v7-retrofit)
audience: Luis, Dan (when ready), Vero (when ready)
---

> **v1.1 shipping contract = [[prototypes/movimientos-v7-retrofit]]** (locked 2026-05-19 after Mercury-density iteration). This design doc is the broader exploration: v6 prototype includes the deferred Mercury filter builder + slide-over drill-in previews. The PRD that ships is [[movimientos-prd]].
>
> **Key v1.1 deltas from this design doc** (folded into the PRD):
> - Density 40px rows (was 36px tight)
> - No bank-logo glyph in Banco/Cuenta cell
> - No counterparty avatar chip in Contraparte cell
> - Always-visible ▼ inline-edit caret on Contraparte + Categoría
> - Cents-deemphasis on Monto (Mercury subordinated-cents)
> - Compartir column 90px (was 50px)
> - Totals strip compact-scale (card padding + font sizes ~halved vs v6)
> - Content max-width 1440px (was 1320px)

# Movimientos — Page Design

> The transactions ledger for Tesote Connect. Where users scan, reconcile, categorize, and find the line items that explain the saldos.
>
> Sits under **Connect** in the sidebar, beside [[../saldos/index|Saldos]]. Replaces the current "Transacciones" UI.
>
> Builds on [[../../design/archetypes]] (list/table archetype, **browse/scan** density), [[../../design/design]] (Lunour brand tokens), and the canonical visual reference `product/business/pagos/prototypes/pro-112/workspace-shell284-v2-lunour.html`. Follows the same playbook as [[../saldos/design|Saldos design]].

---

## What this page is

The ledger of every transaction that has hit any of the user's connected accounts. Users come here to:

1. **Scan recent activity** — "what happened in my accounts today / this week?" Probably 50% of time on page.
2. **Find a specific transaction** — by counterparty, amount, date, reference. Triggered by an external question ("did the BNC payment from Acme land?").
3. **Categorize / reconcile** — inline-tag transactions with categoría and contraparte so downstream reports work. Some inline, some bulk.
4. **Trust the data** — believe that what's shown is complete and clean. *This is the load-bearing one — see below.*

**Pairs with Saldos:** *Saldos = where I stand. Movimientos = what moved.* Saldos answers "how much?"; Movimientos answers "why."

---

## Naming

**Locked: "Movimientos"** (per [[index]] and confirmed 2026-05-16).

- Page title + sidebar nav label = **Movimientos**
- Objects on the page = **Movimientos** (each row is a movimiento)
- Singular = "un movimiento" (e.g., drill-in panel title)

**Why not "Transacciones":**

- "Movimientos" is the native VE/LATAM bank-app vocabulary — every extracto bancario says "movimientos." "Transacciones" reads as imported ERP/SaaS language.
- Job over object — same logic that picked Saldos over Cuentas. Names what the user is reading for.
- Pairs as a couplet with Saldos (state + action, both in user vocabulary).
- One known tension: when Tesote becomes system-of-record, this page may surface non-bank-pulled rows (manual journal entries, internal transfers). "Movimientos" survives that scaling — "movimientos contables" is the Spanish accounting term for journal entries too.

---

## Critical clarification: data certification lives HERE (but not in the row, for now)

> **The certification value prop lands on this page** (Saldos shed it on 2026-05-14 — saldos are 99% reliable; transactions are where completeness is a real concern). But in v1, it does **not** get its own column or inline indicator. Decision 2026-05-16: **killed from the row for now.**

What "certified" *would* eventually mean for a movimiento:

- Row was successfully pulled from the bank (not lost in a sync gap)
- Tesote can match it to a counterparty
- It hasn't been flagged as a possible duplicate
- No gap detected in the surrounding date range for that account

**Where it might surface later:** a filter pill ("Mostrar solo no certificadas"), a dedicated reconciliación view, or — if the row-level signal becomes load-bearing — re-added as a column. Out of scope for v1 prototypes. The design needs to stay open to it landing back here without a major rewrite.

---

## Columns (locked)

```
Fecha · Banco/Cuenta · Descripción · Contraparte · Monto · Categoría
```

| Column | What it shows | Notes |
|---|---|---|
| **Fecha** | `DD/MM` (current year). `DD/MM/YYYY` if prior year. | Default sort: desc. Tightest column (80px). Numeric format is denser at 36px than the `14 May` label form. Right-padding tightened to bring Banco/Cuenta closer (v2 feedback). |
| **Banco/Cuenta** | Bank logo + short bank name + account label + monospace last-4, e.g. `🟦 BNC · Ops VES ··5421` | Merged single cell. In Tesote's mental model, the cuenta tells you the banco. **Last-4 of account number is part of the cell** (v2 feedback) — disambiguates when same bank has multiple accounts of the same flavor. Rendered in monospace at gray-3 for scan-without-noise. |
| **Descripción** | Bank-raw description + ref tail, truncated. `Pago Móvil · 12345…` | Anchor column; flexes to remaining width. Raw because in VE this is where rail/method info naturally lives (Pago Móvil, Transferencia, Débito, etc.). **Truncation: `table-layout: fixed` + `text-overflow: ellipsis` + native `title=""` tooltip + full text in drill-in.** Row height never breaks. See "Description truncation pattern" below. |
| **Contraparte** | Resolved counterparty (name) or em-dash `—` placeholder if unresolved | **Inline-editable in v1** (click → dropdown). When null, render an em-dash `—` (not "Sin contraparte" — v2 feedback). Tooltip on the dash clarifies "click para asignar". |
| **Monto** | Currency prefix + signed amount, color-coded. `+1,200.00 USD`, `-8,500.00 VES` | Right-aligned. Green for credits, neutral gray-1000 for debits, red only for reversed/failed. Currency prefix matches Saldos. |
| **Categoría** | Pill chip — `Servicios`, `Compras`, `Cobros` etc. Em-dash `—` if uncategorized. | **Inline-editable in v1** (click → dropdown). Mercury-style. Em-dash placeholder when null (matches Contraparte treatment). |
| **(trailing)** | Paperplane ✈ — **always visible**, low-key at rest, primary on hover | Send/share this movimiento. Always-visible (not hover-only) so the affordance is discoverable. Hover state: bg = primary-light, color = primary. |

## Description truncation pattern (load-bearing)

> **Rule: row height never breaks. Descriptions never wrap.** Bank descriptions in VE are often long ("Pago Móvil — pago parcial contrato mantenimiento oficinas 2026-05") and the page must stay scannable at 36px.

The pattern, lifted from Mercury / Linear / Stripe / Airtable / Brex / Ramp:

1. **`table-layout: fixed`** on the `<table>` + explicit per-column widths via `<colgroup>`. Without this, columns auto-size to the longest content and row heights drift. With it, every column locks at its declared width and the layout is deterministic. **This is the single most important CSS rule on the page.**
2. **`white-space: nowrap; overflow: hidden; text-overflow: ellipsis`** on the Descripción cell. One line, hard ellipsis.
3. **Native `title=""` attribute** on the cell carrying the full text — free hover tooltip from the browser. v1 ok. (v3 polish: custom branded tooltip with delay.)
4. **Drill-in panel** (row click) shows the full text in a comfortable reading layout.

**Why not a fade-out gradient** instead of ellipsis: prettier but ambiguous — user can't tell if there are 5 more characters or 50. For a reconciliation surface, the unambiguous `…` is the safer call. Save fade-out for non-load-bearing areas.

**Why not a two-line clamp** (`-webkit-line-clamp: 2`): explicitly rejected. Two-line treatments at 36px don't fit, and the variable row heights from "some rows wrap, some don't" destroy the scan.

**Column width plan** (1320px content max, ~1256px usable):

| Column | Width | Treatment |
|---|---|---|
| Fecha | 80px | Fixed |
| Banco/Cuenta | 220px | Fixed — accommodates `LOGO · Bank · cuenta-label ··1234` |
| Descripción | flexes (fills remaining ~376px) | `nowrap + ellipsis + tooltip` |
| Contraparte | 170px | Fixed — `cp-text` inner span ellipses if long |
| Monto | 160px | Fixed — right-aligned, tabular nums |
| Categoría | 150px | Fixed — pill ellipses if long |
| Acción (✈) | 50px | Fixed |

When viewport narrows, Descripción shrinks first (it's the only flexible column); all other columns hold their widths.

---

**Row trailing action: paperplane (✈) — "send this movimiento."**

**Always-visible** action on the right edge of each row (after Categoría). Low-key at rest (gray-4 stroke on transparent bg), primary on hover (blue fill + primary-light bg + primary-blue border). On click, opens a share dialog: pick a destination (counterparty on file, teammate, free-form email/WhatsApp), Tesote auto-formats the row details. **Send-out, not attach-in** — flips Mercury's AP attach-invoice pattern into Tesote's "share / forward this with someone" pattern. Aligns with Tesote-as-system-of-action.

> **Why always-visible** (not hover-only): hover-reveal made the affordance undiscoverable in v1 — a CTA we want adoption on can't hide. The visual weight is kept low enough that it doesn't compete with cell content; only on hover does it pop.

Use cases the paperplane unlocks:
- "Here's the wire we just received from you" — confirmation to a payer counterparty
- "We just paid your invoice — here's the proof" — confirmation to a payee counterparty
- "Look at this movimiento" — share with a teammate inside Tesote
- Future: trigger a request to categorize / tag from the recipient

For v1 prototype: render the icon (hover-reveal), wire a no-op modal stub. Full destinations / formatting / channels are deferred.

**Not in default columns** (drill-in only):

- Referencia bancaria (filter/search target, not a scan target)
- Nota interna (sparse — shown as icon in Descripción cell when present)
- Estado de tx pending/reversed inline pill (**deferred** — re-evaluate when we have rail data with real pending states)
- Adjuntos / file attachments (**not on this page** — paperplane is the row CTA, in the opposite direction)
- Raw bank metadata, sync timestamp, transaction hash, etc.

---

## Density

**36px tight rows.** This is a **browse/scan** archetype — the densest of the three buckets in [[../../design/archetypes]]. Mercury's Transactions ledger sits here too.

Justification:
- High row count (potentially thousands per month across 10+ accounts)
- One-line-per-row mental model — user is scanning, not deciding-per-row
- Density does the work that grouping does on Saldos — pack the rows so a single screen shows ~25–30 movimientos at a glance
- Inline-editable cells (Contraparte, Categoría) still work at 36px — that's Mercury's exact pattern

One-line rows are non-negotiable at 36px. No two-line treatments anywhere in the table.

---

## Multi-currency totals strip

Same behavior as Saldos v3 — a totals strip that recalculates **live** as filters and search change. **Stacked layout (v4 update)** so 10-digit Bs and 9-digit USD amounts always fit without wrapping:

```
┌─ VES · 12 movimientos ──────────────────┐  ┌─ USD · 5 movimientos ──────────────────┐
│                                          │  │                                          │
│  Ingresos     +Bs. 3.700.000.000,00     │  │  Ingresos     +$ 13.700,00              │
│  Egresos      -Bs. 375.035,16            │  │  Egresos      -$ 6.700,00                │
│  ─────────                                │  │  ─────────                                │
│  Neto         +Bs. 3.324.964.964,84      │  │  Neto         +$ 7.000,00                 │
└──────────────────────────────────────────┘  └──────────────────────────────────────────┘
```

Anatomy:
- Each currency gets its own card. **Two cards visible by default** (VES + USD); EUR / additional currencies cards appear as users add cuentas in those currencies.
- Three rows per card: Ingresos · Egresos · Neto (Neto separated by a solid divider, slightly larger amount font).
- Label-left (90px column) + amount-right (tabular nums, right-aligned, nowrap). At 18px for Ingresos/Egresos and 20px for Neto.
- Color: Ingresos green, Egresos neutral (gray-1000), Neto green if ≥ 0 else neutral.
- Splits by currency (**no FX conversion** — same decision as Saldos).
- `filtrado` tag appears beside the currency code when filters beyond the default Fecha are active.

**Why stacked, not horizontal:** in production, VES amounts can reach 10 digits before decimals (Bs. 9.999.999.999,99 ≈ 20 chars at tabular-nums). Side-by-side Ingresos/Egresos/Neto at 22px would either wrap or overflow. Stacking with right-aligned amounts in nowrap cells guarantees the layout never breaks regardless of digit count.

---

## Filter system (full spec)

**Pattern: Mercury-style filter builder.** A single `[+ Filtrar]` button that opens a popover, lets the user pick a dimension, configure it, and apply it as a removable pill. Multiple filters stack as pills. A saved-views dropdown ("Vistas guardadas") persists named combinations of filters.

### Filter row anatomy

```
[Fecha · Últimos 30 días ×]  [Banco · BNC y 1 más ×]  [+ Agregar filtro]  [💾 Vistas (3)]  [Limpiar todo]                    [🔎 Buscar en todo …]
```

Left to right:
- **Active filter pills** — one per active dimension, ordered by [FILTER_ORDER](#filter-order), each with a click-to-edit body and an `×` to remove
- **`+ Filtrar` / `+ Agregar filtro` button** — dashed border at rest, solid + primary-blue when open
- **`💾 Vistas (n)` button** — appears once ≥1 filter is active; opens the saved-views dropdown
- **"Limpiar todo"** — appears once ≥2 filters are active
- **Search box** — pinned right, full-text search across description / ref / counterparty / note / bank / cuenta / entity name

### Dimensions (11)

Order: `fecha · bancos · entidades · cuentas · cps · cats · ccys · monto · desc · nota · ref` <a name="filter-order"></a>

| # | Dim | Pill format | Input UI |
|---|---|---|---|
| 1 | **Fecha** | `Fecha · Últimos 30 días` or `Fecha · 01/05 → 14/05` | Two-pane popover (wide, 540px): **left** = preset radios (Hoy / Esta semana / Este mes / Este trimestre / Este año / Semana pasada / Mes pasado / Últimos 30 días / Últimos 90 días / Trimestre pasado / Todo el tiempo); **right** = two-month calendar grid (range selection: click start, click end, in-between fills) + `Desde` / `Hasta` text inputs for typed dates (`dd/mm/aaaa`). Clicking a preset sets both `from` and `to`; clicking a calendar cell or typing in a date input clears the preset. |
| 2 | **Bancos** | `Banco · BNC` (single) or `Banco · 3 bancos` | Searchable checklist of all banks present in the data |
| 3 | **Entidades** | `Entidad · TST` or `Entidad · 2 entidades` | Searchable checklist of Tesote-customer legal entities (TST · VDT · TTI) with jurisdiction sub-label |
| 4 | **Cuentas** | `Cuenta · BNC ··5421` or `Cuenta · 4 cuentas` | Searchable checklist of unique `(bank, cuenta, last4)` tuples, rendered with bank logo + name + label + monospace last-4 |
| 5 | **Contrapartes** | `Contraparte · Acme C.A.` or `Contraparte · 5 contrapartes` | Searchable checklist of all counterparties on file |
| 6 | **Categorías** | `Categoría · Cobros` or `Categoría · 3 categorías` | Checklist with colored pill chips (no search — set is small enough) |
| 7 | **Moneda** | `Moneda · USD` or `Moneda · USD + VES` | Checklist of currencies present in the data |
| 8 | **Monto** | `Monto · Crédito · ≥ Bs. 1.000` or `Monto · = 5.000` | Composite popover with two sub-sections: **Tipo** (Cualquiera / Crédito / Débito radio) and **Cantidad** (Cualquier monto / Monto exacto / Rango — radio; conditional reveal of one numeric input for exact, two for rango). Tipo and Cantidad combine multiplicatively. |
| 9 | **Descripción** | `Descripción · contiene "wire"` | Single text input, case-insensitive substring match on `desc` |
| 10 | **Nota** | `Nota · contiene "urgente"` | Single text input, case-insensitive substring match on internal `note` field |
| 11 | **Referencia** | `Referencia · contiene 88421` or `Referencia · exacta WIR-88421` | Segmented control (Contiene / Exacta) + text input. `contains` does case-insensitive substring; `exact` does case-insensitive whole-string match. |

### Popover anatomy (universal)

```
┌─ Filter popover ───────────────────────┐
│ ← Dimension name                       │  ← back arrow (when on a specific dim)
├────────────────────────────────────────┤
│ [body — varies per dim]                │
├────────────────────────────────────────┤
│ [Quitar filtro]    [Cancelar] [Aplicar]│  ← Quitar shown only when filter active
└────────────────────────────────────────┘
```

- **Step 1 (no `dim` set):** popover shows the list of *inactive* dimensions to pick. Active dimensions are not listed (edit them by clicking their pill).
- **Step 2 (dim picked OR pill clicked):** popover replaces its body with the dimension-specific input + footer with `Quitar filtro` (only if currently active) / `Cancelar` / `Aplicar`.
- **Back arrow** returns to Step 1 (dim list).
- **Apply** commits the working draft to `filterState`; **Cancel** discards.

### Saved views

A named, persisted combination of filters. Use cases: "Cobros pendientes USD", "Egresos Banesco este mes", "Wires entrantes Q2", "TST únicamente".

- **Persistence:** `localStorage` key `tesote.mov.savedViews.v1` (per-browser, per-user). In production this lives on the server, scoped to the user — but the data shape is the same.
- **Data shape:** `{ name: string, state: FilterState }` — store the full filter state object snapshot
- **Anatomy of the views dropdown:**
  ```
  ┌─ Vistas guardadas ──────────────────────┐
  │ Cobros pendientes USD                ×  │
  │ ↳ Últimos 30 días · 1 categoría · USD   │
  │                                          │
  │ Egresos Banesco este mes             ×  │
  │ ↳ Este mes · 1 banco · Débito           │
  │ ─────────────────────────────────────── │
  │ [Guardar vista actual…    ] [Guardar]   │
  └──────────────────────────────────────────┘
  ```
- **Click a view** → applies the full filter state (overrides current state)
- **`×` on a view** → deletes after confirm (or with undo toast — TBD)
- **"Guardar vista actual…"** input + button → captures current state with the typed name; saves and re-renders the dropdown
- **No edit-in-place yet** — to update a saved view, apply it, modify, save under same name (or a new one)

### Edge cases & rules

- **Default Fecha = Últimos 30 días** on page load. Removable, but the page-meta will switch to "Todo el tiempo" and the backend should hint that this is heavier.
- **Date range with no end:** valid — interpreted as "from X onward" (or "up to Y" if only `to` is set).
- **Multiple selections inside one dimension** are OR'd (`bancos: ['bnc', 'banesco']` = BNC OR Banesco). Across dimensions, filters AND.
- **Null-handling for Contraparte / Categoría filters:** if a row has `cp: null` and the filter requires specific cps, the row is excluded. Add a "Sin contraparte" / "Sin categoría" virtual option as a future enhancement (out of v4).
- **Currencies filter doesn't sum across currencies** — same rule as Saldos: no FX conversion. The totals strip splits VES / USD independently.
- **General-search vs per-dimension Descripción / Nota / Ref:** the right-side search box is a *general* across-all-fields fuzzy match; the per-dimension filters are precise and scoped. Both can coexist (intersected).
- **Totals strip recalc:** every filter change triggers a full recompute of Ingresos / Egresos / Neto for both VES and USD cards.
- **`filtrado` tag on totals strip** appears only when filters beyond the default Fecha are active.

### What's deferred for v5+

- Virtual "Sin contraparte" / "Sin categoría" options in the checklist
- Saved view edit-in-place / rename
- Sharing saved views with teammates
- Server-backed saved views (current v4 is localStorage-only)
- Keyboard-driven filter builder (⌘F, ⌘shift+F, etc.)
- Filter URL hash so a state can be shared via copy-paste link

---

## Sort model (open)

- **Default:** Fecha desc.
- **Other sortable columns:** Monto (asc/desc), Contraparte (alpha), Categoría (alpha).
- Click column header to sort, click again to flip.
- Multi-column sort: out of scope for v1.

---

## Sync philosophy

Same as Saldos: **read-only here.** Movimientos appear as soon as the underlying connection syncs (and the sync is triggered from Conexiones, not from here). Inline `↻ refrescar` link at top-right hints at refreshability but the actual sync action lives on Conexiones. No sync-all button.

---

## States to design

1. **Empty** ✅ — no movimientos / filters returned zero (covered in v3+; small icon + title + sub copy)
2. **Loaded — primary view** ✅ — default state, locked through v5
3. **Loading** — initial fetch / pagination scroll · *deferred*
4. **Drill-in** — see [[#drill-in-deferred-todo]] below · *deferred*
5. **Inline edit** ✅ — Contraparte and Categoría cells become dropdowns on click (locked v1+)
6. **Bulk select** — left-side checkboxes, bulk-categorize action surfaces in a toolbar · *deferred*

Wireframes + anatomy emerge in iteration. v1-v5 ship without drill-in / loading / bulk-select — those are the next phase of work.

## Drill-in (deferred TODO) <a name="drill-in-deferred-todo"></a>

When the user clicks a row, two complementary surfaces could open. Both are deferred from the v1-v5 scope — captured here so the spec doesn't get re-litigated when this becomes the active work:

### Surface A — Quick-view side panel (slide-over)

Mirrors the **Cobros invoice-click pattern**. Slide-over from the right; list stays visible underneath; doesn't take the user out of context. Default surface for the row-click action.

Anatomy (preliminary — refine when this becomes active work):

- **Header:** bank logo + cuenta + ··last4 + close (×). Title = the movimiento's resolved counterparty (or fallback to bank-raw description if no counterparty).
- **Hero amount block:** large currency + signed amount + date + estado pill (if applicable).
- **Field grid:** Fecha · Cuenta · Contraparte · Categoría · Tipo · Moneda · Monto · Referencia · Entidad — all readable, some editable inline.
- **Descripción (raw bank text):** full, unwrapped, in monospace tone. This is where the bank's untouched description lives — the row's truncated version was the preview.
- **Nota interna:** if present; editable.
- **Sección "Compartir":** prior shares of this movimiento (date · destinatario · canal). Inline "Compartir de nuevo" CTA.
- **Sección "Reconciliación" / cert (future):** when cert lands, this is where the certification breakdown shows — what's matched, what's missing, the gap detection trail.
- **Footer actions:** Compartir · Ver página completa → · ⋯ (more).

When to use Surface A: row click default. Cobros' invoice-detail panel is the visual reference.

### Surface B — Full individual movimiento page

A dedicated URL/route for a single movimiento. Same content as Surface A but laid out as a full page (room for the long tail: edit history, related movimientos, full audit log, raw API payloads, sync timestamps, attachments, send history).

When to use Surface B:

- Linked-to from Surface A's "Ver página completa →"
- Linked-to from external surfaces (Cobros showing "this invoice paid by [movimiento]", Tesote IA referencing a specific movimiento, email confirmations linking back)
- Bookmark / share use cases — a URL someone can copy-paste

Anatomy (preliminary):

- Top bar with breadcrumb: `Connect / Movimientos / Movimiento de [contraparte] del [fecha]`
- Hero block: same as Surface A but full-width
- Tabs across the middle: **Detalle · Reconciliación · Compartidos · Auditoría · API**
- Each tab is a section of the long tail

### Open questions for when this becomes active

- **Default surface = A or B?** My lean: A (slide-over) for row clicks; B reachable from the panel + from external links. Mercury / Linear / Stripe all default to slide-over for "view detail" with full-page reserved for "permalink".
- **Should the slide-over support keyboard navigation between movimientos** (j/k or arrow keys)? Worth it — Mercury and Linear both do this and it's surprisingly load-bearing for scan-heavy workflows.
- **Do edits in Surface A reflect immediately in the underlying row?** Yes — same data, no draft mode.
- **Can the user open Surface A and B simultaneously?** Probably not — Surface B replaces the list view; A is layered over it.
- **Mobile:** Surface A becomes a bottom sheet. Surface B is its own route, full screen.

Reference: pattern-match the Cobros invoice-click panel that Luis flagged 2026-05-17 — copy its anatomy / sizing / motion / transition once we get there, then adapt fields to the movimiento data shape.

---

## ASCII sketch (v0)

```
┌──────────┬─────────────────────────────────────────────────────────────────────────────┐
│ sidebar  │  Movimientos                                                       [↻ refrescar] │
│          │  234 movimientos · USD +13,700 / -2,400 · VES +12,500,000 / -85,000,000           │
│ Connect  ├─────────────────────────────────────────────────────────────────────────────┤
│  ▸ Saldos│  [Banco/Cuenta ▾] [Categoría ▾] [Contraparte ▾] [Fecha ▾] [Monto ▾] [🔎 Buscar ] │
│  ▸ Movi…│├──────────┬────────────────────┬───────────────────────┬───────────────┬────────────┬────────────┤
│  ▸ Conex│ │ Fecha    │ Banco/Cuenta       │ Descripción           │ Contraparte   │ Monto      │ Categoría  │
│         │ ├──────────┼────────────────────┼───────────────────────┼───────────────┼────────────┼────────────┤
│ Business│ │ 14 May   │ 🟦 BNC · Ops VES   │ Pago Móvil ref 12345…│ Juan Pérez    │ -8,500.00  │ Servicios  │
│         │ │ 14 May   │ 🟧 BANE · USD AR   │ Transf BANESCO       │ Acme C.A.     │ +1,200.00  │ Cobros     │
│ Capital │ │ 14 May   │ 🟦 BNC · Ops VES   │ Débito ACH inicial   │ Distribuidora │ -55,810.16 │ Compras    │
│         │ │ 13 May   │ 🟪 EXT · USD       │ Wire incoming        │ —             │ +12,500.00 │ —          │
│ AI      │ │ 13 May   │ 🟦 BNC · VES Ops   │ Comisión SWIFT       │ BNC           │ -25.00     │ Bancarios  │
│         │ │ 13 May   │ 🟧 BANE · VES Ops  │ Pago Móvil ref 88421 │ María García  │ -1,500.00  │ Servicios  │
│         │ │ 13 May   │ 🟦 BNC · Ops VES   │ Transferencia        │ Polar         │ -180,000.00│ Compras    │
│         │ │ 12 May   │ 🟪 EXT · USD       │ Wire outgoing        │ Stripe Inc.   │ -3,400.00  │ Software   │
│         │ │ 12 May   │ 🟦 BNC · Ops VES   │ Cobro recibido       │ Cliente XYZ   │ +850,000.00│ Cobros     │
│         │ │ …        │ …                  │ …                    │ …             │ …          │ …          │
│         │ └──────────┴────────────────────┴───────────────────────┴───────────────┴────────────┴────────────┘
└──────────┴─────────────────────────────────────────────────────────────────────────────┘
```

Notes on the sketch:
- 36px rows, one-line each
- Monto right-aligned, currency in same cell, color encodes direction (not shown in ASCII)
- Totals strip lives **above** the toolbar (same as Saldos v3) — recalculates with filters
- Banco/Cuenta is a single cell: small logo block + bank short-name + account label
- "—" for unresolved Contraparte / Categoría (signals "needs work" without coloring it as a problem yet)
- Certification placement **not yet drawn** — pending decision

---

## Decisions locked 2026-05-16

1. **Cert placement** → killed from the row for v1. Re-evaluate later as filter pill or dedicated reconciliación view.
2. **Inline-edit on Contraparte + Categoría** → **v1.** Current UI already supports it; keep parity.
3. **Date format** → `DD/MM` for current year, `DD/MM/YYYY` if prior year.
4. **Adjuntos column** → killed. Replaced by **paperplane (✈) row action** — send/share-out the movimiento, opposite direction from Mercury's attach-in. CTA toward counterparty / teammate.
5. **Estado de tx pending pill** → deferred. Re-evaluate once we have a rail surfacing real pending states.

### v2 round-1 locks

6. **Fecha → Banco/Cuenta padding tightened** — Fecha cell right-padding reduced, Banco/Cuenta cell left-padding reduced. The two columns visually pair as a "when + where" combo.
7. **Banco/Cuenta cell anatomy includes last-4** — `LOGO · Bank · cuenta-label ··1234`. Last-4 in monospace gray-3 to disambiguate same-bank same-flavor accounts.
8. **Description truncation pattern locked** — `table-layout: fixed` + per-column widths + `text-overflow: ellipsis` + native title tooltip + full text in drill-in. Row height never breaks. **No wrap, no fade-out, no two-line clamp.**
9. **Em-dash placeholder for null Contraparte and Categoría** — `—` not "Sin contraparte" / "Sin categoría". Tooltip on the dash clarifies "click para asignar".
10. **Paperplane always-visible** — low-key at rest, primary on hover. Not hover-only, so the affordance is discoverable.

### v3 round-2 locks

11. **Contraparte column widened 170 → 220px** — feels right for the typical counterparty name length and balances visual weight against Categoría + Compartir. Descripción flexes down accordingly.
12. **Trailing action column gets a header label: `Compartir`** — matches the verb action (send/share-out). Title-case Spanish, with accent. Header reads ENVÍA in the small-caps treatment.
13. **Mercury-style filter system** — replaces the v1/v2 fixed filter buttons:
   - `[+ Filtrar]` button (dashed border at rest) opens a popover
   - Popover step 1: pick a filter *dimension* from the list (Fecha · Banco/Cuenta · Categoría · Contraparte · Monto · Tipo)
   - Popover step 2: dimension-specific input (preset radio for Fecha/Tipo, multi-select checklist for Banco/Cat/CP, min/max numerics for Monto), with `← back` arrow + `Cancelar` / `Aplicar` actions
   - Applied filters render left-to-right as removable pills: `[Fecha · Últimos 30 días ×] [Banco/Cuenta · 2 bancos ×] [+ Agregar filtro]`
   - Clicking the pill body re-opens the popover scoped to that dimension (edit existing filter)
   - **All filtering is live**: table rows, totals strip (with `filtrado` tag), and page meta count all recalc on every change
   - "Limpiar todo" appears when ≥2 filters are active
14. **Default Fecha filter = "Últimos 30 días"** — pre-applied on page load. Removable. Pinned by convention: when removed, page-meta switches to "Todo el tiempo" but the search is much heavier on the backend, so we should always seed a date filter.
15. **Page meta strip simplified**:
   - `Últimos 30 días · 17 movimientos · Última actualización: hace 8h`
   - Drops the previous "14 cuentas conectadas" (count belongs on Conexiones, not here)
   - Drops the `Refrescar` link (sync action lives on Conexiones — per the read-only sync philosophy)
   - All three labels are dynamic — the count and date scope reflect active filter state
16. **Table-padding tokens promoted to [[../../design/archetypes#Table cell padding (per density)]]** — same numbers all Tesote tables must use, calibrated against Saldos (Manage) and Movimientos (Browse).

### v4 round-3 locks

17. **Totals strip = stacked layout** — fits 10-digit Bs / 9-digit USD without wrapping. See [[#multi-currency-totals-strip]] for anatomy. Replaces the v3 horizontal layout that broke on real-scale VES amounts.
18. **Full 11-dimension filter system** — see [[#filter-system-full-spec]] for the complete spec. Dimensions: Fecha · Bancos · Entidades · Cuentas · Contrapartes · Categorías · Moneda · Monto · Descripción · Nota · Referencia.
19. **Calendar date picker** — two-month grid with range selection + preset list + typed `Desde`/`Hasta` inputs. Lives in the Fecha popover (540px wide variant).
20. **Combined Monto filter** — Tipo (Cualquiera/Crédito/Débito) + Cantidad (Cualquier monto/Exacto/Rango) composed multiplicatively.
21. **Referencia with mode toggle** — Segmented control: Contiene / Exacta. Both case-insensitive.
22. **Saved views** — named filter combinations, persisted to `localStorage` for v4 (server-backed in production). See [[#saved-views]] for shape + interactions.
23. **Notes data field surfaced as a column-adjacent icon** — sparse note icon (small doc SVG) appears in the Descripción cell when a row has an internal note; full note shown in the cell tooltip + drill-in. The Nota *filter* is independent of the icon (filter searches the note text content).

### v5 round-4 locks

24. **Compartir** replaces **Envía** as the trailing-action column header — neutral verb, broader fit. Modal title + primary CTA updated to "Compartir movimiento" / "Compartir".
25. **No emojis anywhere in product UI** — replaced every emoji with inline SVG icons. Per [[feedback_no_emojis]]. Applies to sidebar nav, topbar controls, filter dimension icons, search, note indicator, empty state, vistas/bookmark glyph, send-modal icon. **All Tesote product surfaces from here forward.** Brain notes / drafts / scratch are exempt.
26. **Filter system promoted to shared design-system primitive** — see [[../../design/archetypes#shared-primitives-preview-next-doc]] and [[project_filter_system_primitive]]. Mechanism is reusable (filter row + popover engine + saved views); dimensions are per-page. Movimientos v5 is the canonical reference implementation. Saldos, Pagos, Cobros, Contrapartes adopt the same shell when they need filters.

## Still open

- **Drill-in (Surface A side panel + Surface B full page)** — see [[#drill-in-deferred-todo]]. The next phase of work on this page. Pattern-match Cobros invoice-click panel for Surface A.
- **Default date window** — locked at Últimos 30 días for now; revisit if backend load is an issue.
- **Compartir destinations + channels** — out of scope for v1-v5 prototype (icon + stub modal only); spec out when we know the share-flow.
- **Bulk select** — deferred.
- **Loading state** — deferred. Spec when pagination becomes active.

---

## Cross-links

- [[../saldos/design|Saldos design]] — sibling page; same archetype, same density bucket logic, opposite density choice (44px vs our 36px)
- [[../../design/archetypes|Archetypes]] — browse/scan density justification
- [[../../design/design|Design system]] — Lunour tokens + Inter Tight + Aspekta typography
- `product/business/pagos/prototypes/pro-112/workspace-shell284-v2-lunour.html` — canonical visual shell
- [[../../../daily/2026-05-14|2026-05-14 daily]] — Saldos session that ended with the certification-lives-on-transacciones clarification
