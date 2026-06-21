---
title: Saldos — Implementation Spec (for AI agent)
audience: AI coding agent (Claude Code or equivalent)
status: promoted
updated: 2026-05-14
version: 1.0
---

> **Promoted to KB** 2026-05-14 → `knowledge-base/product/bank-connectivity/saldos/spec-agent.md`. Edit the KB copy from this point forward.

# Saldos — Agent Implementation Spec

This is the **complete** spec for building the Saldos page. The prototype HTML is the visual contract; this document is the behavior contract. Both must hold.

---

## READ FIRST — required context

Read these files in order **before generating any code**. If any are missing, STOP and ask for the correct path.

1. `luis-brain/product/connect/saldos/design.md` — page-level design rationale, state model, wireframes
2. `luis-brain/product/connect/saldos/prototypes/saldos-v3.html` — **canonical visual reference + sample data**
3. `luis-brain/product/design/archetypes.md` — system-level archetype rules (list/table archetype, density model)
4. `luis-brain/product/design/design.md` — Lunour brand tokens (colors, typography, pills)
5. `luis-brain/product/connect/saldos/spec-eng.md` — strategic context (read for "why")
6. `~/Programming/tesote/treasury/` — data model source-of-truth (Rails models for Account and Connection)

The prototype HTML doubles as a **fixture**: its sample data is realistic (real bank names, realistic amounts, multi-currency, all Estado states demonstrated). Use it to verify your rendering.

---

## SCOPE BOUNDARY — what you touch, what you don't

> **You implement ONLY the Saldos page content area.** Nothing outside it.

The prototype HTML shows the full app shell (sidebar + topbar + main content area) for visual context. **Only the main content area is in scope for this implementation.** Everything else already exists in the `tesote-workspace` codebase and must NOT be modified.

### IN scope — what you build / touch

- The `<SaldosPage />` route component
- All page-internal components: `<AttentionBanner />`, `<CurrencyStrip />`, `<ViewToggle />`, `<FilterBar />`, `<CuentasTable />`, `<ConexionesTable />`, `<EstadoPill />`, `<RowSyncButton />`, `<TwoFaTag />`, `<BankCell />`, etc.
- Page-level data fetching, state management, and effects scoped to this route
- One sidebar nav item activation: ensure `/connect/saldos` highlights the existing "Saldos" sidebar entry (this is a state thing, NOT a sidebar redesign)

### OUT of scope — DO NOT touch

- ❌ `<Sidebar />` component (logo, search, nav sections, user footer) — **already exists, do not modify**
- ❌ `<Topbar />` component (Mover dinero CTA, notification icons, settings icon) — **already exists, do not modify**
- ❌ App shell layout / routing infrastructure — **already exists**
- ❌ Global styles, design tokens at the app level — consume existing tokens, do not redefine
- ❌ Authentication, org switching, permissions — **already exists**
- ❌ Any other page route — Pagos, Cobros, Contrapartes, Inicio, Transacciones, Conexiones bancarias (as a separate route — Conexiones lives as a VIEW within Saldos page, not its own route)

If you find yourself editing a file outside the Saldos page directory or its associated primitives directory, **STOP and ask.** You're likely out of scope.

---

## Page IA and routing

- **Route:** `/connect/saldos`
- **Sidebar location:** under "Tesote Connect" section, between "Inicio" and "Transacciones"
- **Active state:** sidebar item gets `.active` class when route matches `/connect/saldos*`
- **Document title:** "Saldos · Tesote"

---

## Tech stack

Match the existing `tesote-workspace` codebase. **Confirm with eng lead before scaffolding:**
- Framework (presume React + TypeScript)
- Styling solution (CSS modules? Tailwind? Styled-components?)
- State management (presume React Query for server state)
- Test runner (Jest + RTL? Vitest?)

CSS tokens MUST come from the global Lunour design tokens (see `design.md`). Do not hardcode hex values.

---

## Data contracts

### `Account`

```typescript
type Account = {
  id: string;
  compania: string;              // e.g., "TST CYC", "Tesote Tech"
  companiaId: string;            // FK
  banco: string;                 // e.g., "Mercantil", "BBVA Provincial"
  bankLogoKey: BankLogoKey;
  cuentaLast4: string;           // "6733" — UI renders as "••6733"
  saldo: Decimal;                // exact amount, 2 decimal places
  divisa: Divisa;
  estado: AccountEstado;
  lastSyncAt: string | null;     // ISO 8601 datetime; null for manual
  connectionId: string;          // FK to Connection
  isManual: boolean;
};

type AccountEstado = "ok" | "syncing" | "warn" | "manual";

type Divisa = "VES" | "USD" | "EUR" | "PAB" | "DOP";

type BankLogoKey =
  | "mercantil" | "bbva" | "bancamiga" | "activo"
  | "bnc" | "venezuela" | "cash";
```

### `Connection`

```typescript
type Connection = {
  id: string;
  banco: string;
  bankLogoKey: BankLogoKey;
  userMask: string | null;       // e.g., "l...@25"; null for manual
  entidades: string[];           // e.g., ["TST CYC", "Tesote Tech"]
  cuentasCount: number;
  estado: ConnectionEstado;
  estadoReason?: string;         // free-text for "review" or "sync_failed"
  lastSyncAt: string | null;     // ISO 8601
  twoFa: "auto" | "manual" | null;
  isManual: boolean;
};

type ConnectionEstado =
  | "active"
  | "syncing"
  | "credentials_changed"   // user changed bank password
  | "requires_2fa"
  | "bank_down"             // bank API persistently failing
  | "review"                // Tesote support investigating
  | "sync_failed"
  | "manual";
```

### `CurrencyTotal` (client-computed)

```typescript
type CurrencyTotal = {
  divisa: Divisa;
  total: Decimal;
  accountCount: number;
  bcvRate?: number;              // VES only; provided by server with accounts
  bcvDate?: string;              // ISO date for VES rate
  bcvEquivalent?: Decimal;       // VES-only, computed: total / bcvRate
};
```

---

## API surface

**Confirm exact paths and shapes against the treasury repo before implementing.**

| Endpoint | Method | Request | Response | Notes |
|---|---|---|---|---|
| `/api/v1/saldos` | GET | `?compania=&banco=&divisa=&search=` | `{ accounts: Account[], connections: Connection[], bcv: { rate: number, asOf: string }, asOf: string }` | Server returns full org dataset; client-side filtering is fine for ≤500 accounts. Query params are optional (server-side filter passthrough). |
| `/api/v1/connections/:id/sync` | POST | `{}` | `{ syncJobId: string }` | Triggers sync of one connection (all its accounts). |
| `/api/v1/sync-jobs/:id` | GET | — | `{ id: string, connectionId: string, status: "running" \| "complete" \| "failed", errorReason?: string, accountsUpdated?: number }` | Polled every 3s. |

**Rate-limit note:** sync trigger should reject (HTTP 409) if a sync for that connection is already running. Client handles by surfacing the existing in-flight sync rather than starting a new one.

---

## Component breakdown

All components below are **inside the Saldos page boundary** (see scope boundary above). The app shell, sidebar, and topbar are pre-existing and not part of this list.

| Component | New / Reuse | Responsibilities |
|---|---|---|
| `<SaldosPage />` | New | Top-level route component; mounts inside existing app layout. Orchestrates data fetching + view state. |
| `<PageHeader />` | Reuse if exists | Title + meta line |
| `<AttentionBanner />` | New | Yellow banner when one or more connections are in `credentials_changed`/`bank_down`/`sync_failed`/`requires_2fa`/`review` |
| `<CurrencyStrip />` | New | 3-card (or N-card) unified container; recomputes from visible accounts |
| `<ViewToggle />` | Reuse if exists, else new | Segmented control |
| `<FilterBar />` | New (page-specific) | Multi-select dropdowns + search input |
| `<EstadoPill />` | New primitive | Composite badge for Cuentas (3 states + manual) |
| `<ConnectionEstadoPill />` | New primitive | Connection badge (7 states + manual) — same visual, richer vocabulary |
| `<BankCell />` | New primitive | Bank logo bubble + bank name inline |
| `<DataTable />` | Reuse if exists | Generic table primitive |
| `<RowSyncButton />` | New | Per-row sync trigger with disabled state + tooltip |
| `<TwoFaTag />` | New | "Sí" / "Auto" / "—" tag |
| `<Toast />` | Reuse | Sync completion notifications |

Each new primitive should be extracted to the shared design-system package so other pages (Pagos, Cobros, Transacciones) can consume.

---

## State model

### `Account.estado` transitions

```
[ok] ──(server: connection unhealthy)──→ [warn]
[ok] ──(server: sync started)──→ [syncing]
[syncing] ──(sync complete OK)──→ [ok]
[syncing] ──(sync failed / conn went bad)──→ [warn]
[warn] ──(sync started after fix)──→ [syncing]
[manual] = terminal (no transitions)
```

### `Connection.estado` transitions

| From | To | Trigger |
|---|---|---|
| `active` | `syncing` | User clicks sync OR scheduled sync starts |
| `syncing` | `active` | Sync succeeded |
| `syncing` | `sync_failed` | Sync errored |
| `active` | `credentials_changed` | Server detects auth expired |
| `active` | `requires_2fa` | Server requests 2FA approval |
| `active` | `bank_down` | Bank API returns persistent errors |
| `active` | `review` | Tesote support flags |
| `credentials_changed` | `syncing` | User completes re-auth (out of scope v1) |
| `requires_2fa` | `syncing` | User approves 2FA (out of scope v1) |
| `manual` | (terminal) | — |

### Pill class mapping (CSS classes in prototype)

| State | Pill class | Background | Dot color | Label |
|---|---|---|---|---|
| Account `ok` / Connection `active` | `pill-ok` | `#D6E8D5` | `#1A8C5B` | "Sincronizada" / "Activa" |
| `syncing` | `pill-syncing` | `#E4ECF7` | `#1C77F4` | "Sincronizando" |
| Account `warn` / Connection `credentials_changed`, `requires_2fa`, `sync_failed` | `pill-warn` | `#F7EDD0` | `#CC9500` | "Requiere atención" / specific reason |
| Connection `bank_down` | `pill-error` | `#FFE6E6` | `#C41E1E` | "Banco caído" |
| Connection `review` | `pill-review` | `#ECE7DD` | `#857D73` | "En revisión" |
| `manual` | (no pill; render `—`) | — | — | — |

---

## Interactions

### View toggle

1. User clicks `Cuentas` or `Conexiones bancarias`
2. Apply `.active` class to clicked button; remove from sibling
3. Show clicked view pane (`<CuentasView>` or `<ConexionesView>`); hide the other
4. No data refetch — both views render from the same source data
5. Emit telemetry `saldos.view_toggled`

### Filter (Cuentas view)

1. User clicks a filter button (e.g., "Banco ▾")
2. **Close any other open dropdown**
3. Toggle the clicked dropdown's `.open` class
4. User clicks an item → toggle its `.checked` state in local component state
5. On any selection change:
   - Apply ALL active filters AND the current search query to the row list
   - For non-matching rows: hide them (style `display: none` OR omit from rendered list)
   - Recompute `CurrencyTotal` from the visible rows only
   - Update each `<CurrencyStrip />` card in place (amount, count, BCV equivalent)
   - Show `"filtrado"` badge on each currency card when any filter is active
6. User clicks "Limpiar" in dropdown → clear only that filter
7. Click outside any dropdown → close all open dropdowns
8. Filter button gets `.active` class when ≥1 of its values is selected

### Search (Cuentas view)

1. User types in search input → debounced 150ms
2. Apply case-insensitive substring match on combined row text (`compania + banco + cuentaLast4 + saldo + divisa`)
3. Same downstream effects as filter (recompute totals, "filtrado" badge)
4. Clearing the input clears the search filter

### Sync (Conexiones view)

1. User clicks per-row sync button
2. Button enters loading state immediately (disable, swap icon for spinner)
3. POST `/api/v1/connections/:id/sync`
4. Optimistically transition Connection's row Estado to `syncing` (pill color blue)
5. Start polling `/api/v1/sync-jobs/:id` every 3000ms
6. On poll response `{ status: "complete" }`:
   - Transition Connection Estado back to `active` (or stay in current error state if appropriate)
   - **Refetch the affected connection's accounts** from `/api/v1/saldos?connection_id=:id`
   - Show toast: `"<Banco> sincronizada — N cuentas actualizadas"` (auto-dismiss 4s)
   - Stop polling
7. On poll response `{ status: "failed" }`:
   - Transition Connection Estado to `sync_failed`
   - Show error toast: `"Sync de <Banco> falló — <reason>"` (auto-dismiss 8s)
   - Stop polling
8. On poll timeout (60s with no terminal status):
   - Stop polling
   - Show toast: `"Sync de <Banco> está tomando más tiempo del esperado — sigue corriendo en segundo plano"`
   - Leave row in `syncing` state; next page load will reflect final state

Sync button is DISABLED (greyed out, tooltip explains why) when:

| Connection state | Tooltip |
|---|---|
| `syncing` | "Sync en curso" |
| `credentials_changed` | "Re-autentica primero" |
| `requires_2fa` | "Aprueba el 2FA primero" |
| `review` | "Tesote está revisando esta conexión" |
| `manual` | (button not rendered or fully hidden) |
| `bank_down` | (button still enabled — user may retry) |
| `sync_failed` | (button still enabled — user may retry) |

### Banner CTA

1. User clicks "Ver conexiones →"
2. Switch active view to `Conexiones bancarias`
3. (Future v2) Pre-filter Conexiones table to only show problematic connections
4. Emit telemetry `saldos.banner_cta_clicked`

---

## Edge cases — required to handle

1. **Zero accounts, zero connections** → render empty state placeholder (text: "No tienes cuentas conectadas todavía") with a CTA placeholder. Detailed empty state is out of scope for v1; render a minimal version.
2. **All accounts filtered out** → inside the table body area, show "Ningún resultado coincide con los filtros aplicados." Currency cards render with 0 totals, 0 counts.
3. **Single currency only** → render only currencies present (e.g., omit EUR card if no EUR accounts). **Confirm with PM**: alternatively, always show all known currencies.
4. **Connection broken mid-sync** → poll returns failed → connection transitions to `sync_failed` (yellow) + error toast.
5. **Stale account data** (lastSyncAt > 7 days, connection still `active`) → render normally with `pill-ok` "Sincronizada" + `last-sync` text shows "hace N días". Do NOT escalate to `warn` purely based on age.
6. **Manual account with 0 balance** → render normally; show `Bs. 0.00` (or appropriate currency).
7. **Compañía / banco filter dropdown items** → populate only from currently-loaded accounts; do not show options for entities with zero accounts.
8. **Unknown bank logo key** → fall back to a neutral gray bubble with the first letter of `banco`.
9. **Polling continues across view toggle** → if user switches to Cuentas while a Connection's sync is in flight, polling continues. Estado updates appear when user toggles back.
10. **Race condition: sync triggered + filter changed mid-poll** → polling and filter UI are independent; the connection row continues to receive Estado updates regardless of which Account rows are visible.
11. **Initial fetch fails** → render error state: "No pudimos cargar tus saldos. <Reintentar>" button refetches.
12. **Concurrent sync requests on the same connection** → server returns 409. Client should: (a) not start new poll, (b) update Estado to `syncing` if not already, (c) attach polling to the existing job by querying `/api/v1/sync-jobs?connection_id=:id&status=running`.

---

## Acceptance criteria — testable

| # | Given | When | Then |
|---|---|---|---|
| AC-1 | Saldos route, 14 accounts loaded (per prototype data) | Page renders | 14 rows visible in Cuentas table sorted by `saldo` DESC; VES card shows `Bs. 23,662,290.05` (7 cuentas); USD card shows `$411,663.47` (7 cuentas) |
| AC-2 | Cuentas view, no filters | User clicks "Banco ▾" then checks "Mercantil" | Only Mercantil rows visible (3 rows). VES card shows `Bs. 475,056.87` (1 cuenta). USD card shows `$1,840.50` (2 cuentas). "filtrado" badge appears on both cards. Banco filter button has `.active` class. |
| AC-3 | Cuentas, Banco=Mercantil active | User types "6733" in search | Only one row visible (TST CYC ••6733). VES card: `Bs. 475,056.87` (1). USD card: `$0.00` (0). |
| AC-4 | Cuentas, search "6733" + filter Banco=Mercantil active | User clicks "Limpiar" in Banco dropdown | All Mercantil filter values clear. Banco button loses `.active` class. Table re-filters with only the search applied: shows only ••6733 row. |
| AC-5 | Conexiones view, BBVA in `credentials_changed` | View renders | BBVA row's pill shows yellow "Cambio credenciales". Sync button is disabled with tooltip "Re-autentica primero". |
| AC-6 | Conexiones, Mercantil `active` | User clicks Mercantil's sync button | Button enters disabled+spinner state within 100ms. Mercantil row pill transitions to blue "Sincronizando" within 200ms. POST sent to `/api/v1/connections/<id>/sync`. |
| AC-7 | After AC-6, sync polling returns `status: complete, accountsUpdated: 3` | — | Mercantil pill returns to green "Activa". Toast appears: `"Mercantil sincronizada — 3 cuentas actualizadas"`. Toast auto-dismisses after 4s. The 3 Mercantil rows in Cuentas table show updated `lastSyncAt`. |
| AC-8 | Connection sync polling exceeds 60s with no terminal status | Timeout fires | Polling stops. Toast: `"Sync de Mercantil está tomando más tiempo del esperado..."`. Mercantil row remains in `syncing` pill state. |
| AC-9 | User on Saldos | User clicks Conexiones bancarias toggle | Cuentas view hides; Conexiones view shows. View toggle's `.active` class moves. |
| AC-10 | Cuentas with no rows visible (filter excludes all) | View renders | Empty-results message inside table wrap. VES/USD cards show 0. Filter buttons retain `.active` class. |
| AC-11 | Connection has `isManual: true` | Conexiones view renders that row | Estado cell shows `—`. 2FA cell shows `—`. Sync button hidden or fully disabled (no tooltip needed). |

---

## Out of scope (v1) — DO NOT BUILD

**Scope boundary first** (re-emphasized — see top of spec):
- Sidebar, topbar, app shell, global nav — **already exist, do not modify**
- Any other page route — only the Saldos route is in scope

**Feature-level out of scope:**
- Drill-in slide-over panel for Cuenta detail or Conexión detail (separate ticket)
- Empty state full design (render minimal placeholder only)
- Connect-new-bank flow
- Add-manual-account flow
- Edit / disconnect connection flow
- Group-by-banco grouped table (see `saldos-v1.html` for prior exploration; revisit later)
- Sticky table header
- Pagination / virtualization (assume ≤500 rows; revisit at scale)
- Re-auth flow itself (separate Connect-auth ticket)
- Real-time WebSocket/SSE (polling is sufficient)
- Export to CSV
- Column sort beyond default `saldo` DESC
- Mobile / responsive (desktop-only v1)
- Dark mode
- Tooltips on hover for column headers
- Multi-select bulk actions

---

## Performance budgets

- **Initial paint** (route enter to first meaningful render): **< 300ms** for ≤100 accounts
- **Filter / search application** (input change to recomputed totals): **< 50ms** for ≤500 accounts
- **Sync poll interval:** `3000ms`
- **Sync poll timeout:** `60000ms`
- **Search debounce:** `150ms`
- **Toast auto-dismiss:** `4000ms` (success) / `8000ms` (error)
- **Initial data fetch budget:** server responds in ≤500ms for typical org

---

## Telemetry events

Emit to analytics on each event. **Do not log PII** (account numbers, saldos, user names).

| Event | Payload |
|---|---|
| `saldos.viewed` | `{ tab: "cuentas" \| "conexiones", accountCount: number, connectionCount: number, problemCount: number }` |
| `saldos.filter_applied` | `{ field: "compania" \| "banco" \| "estado" \| "divisa", values: string[] }` |
| `saldos.filter_cleared` | `{ field: string }` |
| `saldos.search_performed` | `{ queryLength: number }` |
| `saldos.sync_triggered` | `{ connectionId: string, bankLogoKey: string }` |
| `saldos.sync_completed` | `{ connectionId: string, durationMs: number, success: boolean, accountsUpdated: number, errorReason?: string }` |
| `saldos.banner_cta_clicked` | `{ brokenCount: number }` |
| `saldos.view_toggled` | `{ from: "cuentas" \| "conexiones", to: "cuentas" \| "conexiones" }` |
| `saldos.row_clicked` | `{ rowType: "account" \| "connection", id: string }` (drill-in deferred but track intent) |

---

## Open questions for human resolution

Resolve these with Luis or Dan before writing code:

1. **Framework & styling confirmation** — match existing `tesote-workspace`. What's the actual stack?
2. **Sync API exact path** — what's the real endpoint? Confirm against treasury repo.
3. **Polling vs SSE/WebSocket** — for sync state updates, is 3s polling acceptable load? Or should we go SSE?
4. **EUR card behavior** — show with `€0.00` when zero accounts (current prototype) or hide entirely?
5. **`bcv` data source** — is the BCV rate served alongside `/api/v1/saldos`, or fetched separately?
6. **Row click in v1** — does clicking a row do nothing (current behavior since `⋯` removed) or show a tooltip "Detalles disponibles próximamente"?
7. **Telemetry destination** — Segment? PostHog? GA4?
8. **Feature flag** — should v1 ship behind a flag for staged rollout?

---

## Reference: prototype DOM hooks

The prototype uses these CSS classes as the canonical anatomy. The implementation can rename to component-scoped names, but the same logical regions must exist:

| Region | Prototype class / id |
|---|---|
| Sidebar nav active item | `.sb-item.active` |
| Page header title | `.page-title` |
| Page header meta line | `.page-meta` |
| Page header warning (X necesitan atención) | `.page-meta-warning` |
| Attention banner | `.banner` |
| Banner CTA | `.banner-cta` |
| Currency strip container | `.saldos-strip` |
| Individual currency card | `.saldo-card` (`#card-ves`, `#card-usd`, `#card-eur`) |
| Currency amount integer part | `#ves-amount` etc. |
| Currency amount cents | `#ves-cents` etc. |
| Currency count | `#ves-count` etc. |
| BCV equivalent (VES only) | `#ves-bcv` |
| "filtrado" tag | `#ves-filtered-tag`, `#usd-filtered-tag` |
| View toggle buttons | `.view-toggle-btn[data-view]` |
| View pane | `.view-pane` (`#view-cuentas`, `#view-conexiones`) |
| Filter button | `.filter-btn[data-filter]` |
| Filter dropdown | `.filter-dropdown[data-dropdown]` |
| Filter dropdown item | `.filter-dropdown-item[data-value]` |
| Search input | `#search-cuentas` |
| Table | `.data-table` |
| Estado pill | `.pill.pill-ok` / `pill-syncing` / `pill-warn` / `pill-error` / `pill-review` |
| Pill dot | `.pill-dot` (inside `.pill`) |
| Bank cell | `.bank-cell` |
| Bank logo bubble | `.bank-logo` (variants `.bank-logo-mercantil`, etc.) |
| Per-row sync button | `.row-sync-btn` |
| 2FA tag | `.twofa-tag` (variants `.auto`, `.muted`) |

---

## Done definition

This v1 is "done" when:

- [ ] All 11 acceptance criteria pass
- [ ] Performance budgets met on a typical dev machine
- [ ] Telemetry events fire correctly (verified via analytics dashboard)
- [ ] No console errors in production build
- [ ] All edge cases enumerated handle gracefully (no white screens)
- [ ] Behind feature flag if eng decides

---

*Drafted 2026-05-14 from Luis's session context. See `spec-eng.md` for the strategic / human-facing brief. Update version + changelog at top when changes land.*
