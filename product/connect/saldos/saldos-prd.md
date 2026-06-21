---
title: Saldos — v1.1 Retrofit PRD (against production sync_dashboard)
tags: [product, prd, connect, saldos, ws-1, redesign]
updated: 2026-05-19
status: ready-for-tesote-plan
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: https://linear.app/tesote/issue/PRO-145/saldos-v11-retrofit-on-production-sync-dashboard
tesote_plan_dir: [TBD]
---

# Saldos — v1.1 Retrofit PRD

> **One-line purpose.** Surgically retrofit the production `sync_dashboard` page (live in `treasury/app/controllers/sync_dashboard_controller.rb` + 7 ViewComponents + 1 service + 5 view partials) into the new Saldos design — visual tokens, naming, the killed-Validación column, the dollarized sort, the renamed Sync column, and the Geist Mono numeric treatment — **without touching the Ransack filter system, the Turbo Stream wiring, the group_by mechanism, the per-connection sync flow, the feature flags, or any data-model bones**. Drill-in drawer + Programación/Modo column removal defer to v1.2.

> **Visual + behavior contract.** [[prototypes/saldos-v4-functional]] — open in browser. Every visual decision in this PRD is anchored to that file. Where the prototype and this doc disagree, the prototype wins.

---

## Tesote-Plan Intake

> Treasury's `/tesote-plan` ingests this block. Tight. Match format exactly.

### Actor & Problem

As a **Tesote workspace admin (Mariel — internal dogfood; named prospects in live demos)**, I need to **open Connect → Saldos and have it look + feel like the rest of the new Tesote — not the in-flight Lunour-meets-Tailwind-slate state it currently ships in** because **the production `sync_dashboard` page predates the locked design system (Lunour tokens, Geist Mono numerics, the 3-state Estado pill family, the killed-cert-on-Saldos decision), surfaces a Validación column that dilutes trust on a page where the data is 99% reliable anyway, and embeds visual drift (Tailwind slate-*, `shadow-sm`, mixed radii) that breaks the demo frame**.

### The Test

This solves **visual + naming + trust-signal drift** for **Mariel + named-prospect demos** in **Connect**. Without it: **the first surface in a Tesote demo (Saldos is the default Connect landing) shows a half-migrated page next to the polished Movimientos v5 redesign, undermining the "operational trust dashboard" frame the page exists to project**.

### V0 — Simplest thing that works

- [ ] **Naming**: page title, document title, sidebar nav label, attention-banner subtitle copy all change `Panel de Sincronización` → `Saldos`. Subtitle warning copy `N con problemas` → `N requieren atención` (with `requiere`/`requieren` singular handling). Tab label `Por conexiones bancarias` → `Conexiones Bancarias`.
- [ ] **Currency strip rebuilt** to the [[prototypes/saldos-v4-functional]] spec: 3-up grid, fixed **92px** card height with `align-items: start` on the grid, Lunour border + `border-radius: 10px`, **Geist Mono 23px / 700 / `letter-spacing: -0.04em`** for the integer + cents unified (no size/color split), single-line BCV sub on the VES card only formatted exactly `$1,738,909.97 (Tasa BCV 510 Bs/$)` (BCV rate floored to integer for display; full precision for math). 9-digit integer max — no auto-step needed at the new size.
- [ ] **Validación column removed** from the Cuentas table (visual only — `ReconciliationStat` + `ReconciliationAccountSummary` still loaded by `IndexDataService` for future Transacciones page; just stop rendering the column).
- [ ] **Sync column** on Conexiones Bancarias gets a `Sync` header label (was empty `<th>`) and widens from cut-off to 8% of table width.
- [ ] **Default sort** = `Saldo desc, dollarized via BCV` — implemented client-side via Ruby `sort_by` on the already-loaded accounts array inside `IndexDataService` (the data already gets `to_a`'d, so this is free).
- [ ] **Default group_by** changes from `entity` → `none` (flat list) in `resolve_group_by` fallback. Group-by control still offers all four modes; user choice persists in session as today.
- [ ] **Cuenta row click** navigates to filtered Movimientos: `/connect/movimientos?query[tesote_account_id_in][]=<account.id>` (target URL pattern: confirm Movimientos controller accepts `tesote_account_id_in`; if Movimientos new redesign isn't ready, fall back to existing `v2_tesote_accounts_path` filtered URL).
- [ ] **Design tokens migrated** across every touched file: `slate-*` → Lunour `gray-1000 / 600 / 200 / 50`; `tesote-blue-*` verified against Lunour `blue-700` family; `shadow-sm` → `1px solid gray-200` (borders > shadows); `rounded-xl/lg/full` audited against 4/8/10/12; `bg-tesote-tan` outer surface confirmed = `#F7F5F0` (Lunour `gray-50`).
- [ ] **Geist Mono via Google Fonts** wired into the app shell (or self-hosted — Dan's call). Applied to: currency card amounts, currency sub-equiv USD number, accounts table `Saldo` column, connections table `Cuentas` count, account-number display (`··6733`).
- [ ] **Estado pill family** verified — the 3 account states (`Sincronizada` / `Sincronizando` / `Requiere atención`) and 7 connection states (`Activa` / `Sincronizando` / `Cambio credenciales` / `Requiere 2FA` / `Banco caído` / `En revisión` / `Sync falló`) use the locked Lunour pill backgrounds (`pill-paid #D6E8D5`, `pill-new #E4ECF7`, `pill-pending #F7EDD0`, `pill-overdue #F8D8C0`, `pill-draft #ECE7DD`) with `gray-1000` text and the correct dot colors per the redesign skill.

### Out of Scope (explicit "Not Doing")

- **Connection drill-in slide-over drawer** — deferred to **v1.2**. The prototype shows what it should be; building `ConnectionDrawerComponent` + its turbo frame + the `Re-autenticar` / `Desconectar` flows is real new work and would balloon v1.1.
- **Removal of `Programación` + `Modo de Sync` columns** from Conexiones Bancarias — also deferred to v1.2. Killing them now strands the data (no drawer to surface it in). v1.1 keeps both columns visible with the visual retrofit applied.
- **Migration to the Movimientos v5 `+ Filtrar` builder filter primitive** — explicit decision: keep production's 5-fixed-pill Ransack-driven pattern (Cuentas / Compañías / Bancos / Tipo de Cuenta / Divisa). Filter-primitive consolidation is a separate workstream.
- **Cuenta drill-in drawer** — Cuenta row click navigates to Movimientos instead. No drawer for accounts.
- **Re-auth flow, add-bank flow, edit-connection flow, add-manual-account flow** — separate Connect-auth tickets.
- **Empty state full hero design** (the bank-availability strip + illustration from [[design#1-empty-state]]) — keep production's minimal empty state, visually retrofitted only.
- **Route / controller rename** — `sync_dashboard_path` and `SyncDashboardController` keep their names. **Visible title rename only.** Avoids touching every spec path + every internal reference.
- **`SyncAccountability::BannerComponent`** — separate component with its own flipper flag; not redesigned in this pass beyond Lunour token swap.
- **Movimientos**, **KYC onboarding**, **Transacciones** new surface — all separate scopes.
- **Sticky header, virtualization, CSV export, multi-select bulk actions, mobile, dark mode, column sort beyond Saldo + Banco + Compañía + Divisa + Último sync** — deferred.

### Technical Requirements

- [ ] Spanish copy on every user-facing string.
- [ ] **Geist Mono** loaded via Google Fonts `<link>` (or self-host if Dan prefers) with weights `500;600;700`. Wired in `application_v2.html.erb` head.
- [ ] **Inter Tight + Aspekta** continue per [[../../design/design]] — full migration to those is its own workstream.
- [ ] `tabular-nums` (implicit in mono fonts; explicit `font-variant-numeric: tabular-nums` on any non-mono numeric).
- [ ] All visual tokens consumed from Lunour palette via Tailwind theme extension or CSS vars. **Zero hardcoded `slate-*`, `gray-*` (Tailwind defaults), or `#000` text** in any touched file.
- [ ] **Multi-tenant**: `workspace_id` scoping preserved via `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)` in the controller. No changes to data scoping.
- [ ] **Feature flag**: existing `sync_operations_dashboard` flipper continues to gate the page. No new flag.
- [ ] **Turbo Streams**: existing `index.turbo_stream.erb` + `turbo_frame_tag :sync_dashboard_filters` + `turbo_frame_tag :sync_dashboard_accounts_table` + `turbo_frame_tag 'sync_accountability_banner'` + currency-summaries div `id="sync_dashboard_currency_summaries"` all preserved verbatim.
- [ ] **Ransack filter mechanism**: 5-pill `FilterBarComponent` + `FilterPillComponent` + `Shared::MultiSelectComponent` preserved verbatim. Only visual tokens change inside the component templates.
- [ ] **Session persistence**: `session[:sync_dashboard_filters]` + `session[:sync_dashboard_group_by]` + 24h expiry logic preserved.
- [ ] **No emojis** — production already uses `heroicon` helper; audit any new SVGs introduced for the retrofit ensure they're inline SVGs, not emoji codepoints.
- [ ] **Locked pill family** — confirm `Ui::Pill` (if used) or pill CSS in this surface uses Lunour `pill-*` tokens, not Mercury pastels (`#e4e8f7`, `#fdefce`, `#fddcc5`, `#d8e9de`, `#eef1f4` — drift to kill).
- [ ] Performance: initial paint <300ms for ≤500 accounts, filter recompute <50ms, currency summary recompute on Turbo Stream <50ms.

### Rollout Plan

1. **Internal** — Tesote Finance workspace (Mariel dogfoods on real data). Luis + Mariel walk through `/connect/saldos` end-to-end: every Estado, every group-by mode, every filter combination, the sync interaction, both empty states, the 9-digit Bs case on the BNC connection.
2. **Beta** — first 2–3 friendly prospect demos. Saldos is the demo's opening surface (Connect's default landing).
3. **GA** — existing `sync_operations_dashboard` flipper flipped on for all workspaces. No new flag needed.

---

## Context (why now)

The original `saldos-prd.md` was drafted (2026-05-18) before reading production code. It assumed `saldos-v3.html` was the baseline and that the redesign was greenfield against a stale prototype. **Reading `treasury/app/controllers/sync_dashboard_controller.rb` and its 2,100 LOC of view + component code changed the framing entirely** — Saldos is already live as `sync_dashboard`, gated by the `sync_operations_dashboard` flipper, with a working Ransack filter system, working Turbo Stream wiring, working session-persisted group_by, working per-connection sync triggers, and `ReconciliationStat`/`ReconciliationAccountSummary` already loaded server-side.

The retrofit is therefore not "build Saldos". It's: **swap the visual surface, kill one column, label one column, change one default, add one cross-currency sort comparator, rename one user-facing string set, and don't touch anything else**.

The interactive prototype [[prototypes/saldos-v4-functional]] (2026-05-18 → 2026-05-19) locked every visual + behavior decision by direct manipulation: tab toggle, multi-select filter dropdowns + chips + reset, group-by with dollarized saldo desc sort, sync state transitions with toasts, BCV display format, currency card sizing (fixed 92px), Geist Mono numerics. **That file is the visual contract this PRD ships.**

---

## Current production state (read 2026-05-18 from `~/Programming/tesote/treasury`)

| Surface | Production file(s) | What's there |
|---|---|---|
| Controller | `app/controllers/sync_dashboard_controller.rb` (183 LOC) | Flipper gate, Ransack `determine_active_filters` with 24h session persistence, `resolve_group_by` (entity / bank / currency / none — default `entity`), `permitted_tesote_accounts` scoping, exchange-rate loading, turbo_stream + html response |
| Data service | `app/services/sync_dashboard/index_data_service.rb` (205 LOC) | Loads + groups accounts, builds currency summaries, computes active-sync connection IDs, loads `ReconciliationStat` + `ReconciliationAccountSummary`, builds filter dropdown data |
| Layout view | `app/views/sync_dashboard/index.html.erb` (156 LOC) | Page header, `SyncAccountability::BannerComponent` (flag-gated), currency summary cards (text-xl, mixed slate-*), tab toggle (Stimulus `tab-toggle`), filter bar mount, both tab partials, webscraper modal turbo frame |
| Filter bar | `app/components/sync_dashboard/filter_bar_component.{rb,html.erb}` (98 + 174 LOC) | 5 fixed pills (accounts / entities / banks / account_types / currencies) wrapping `Shared::MultiSelectComponent`, search_form_for ransack, auto-submit 300ms debounce, active-chip secondary row, count badge |
| Accounts table | `app/views/sync_dashboard/_accounts_table.html.erb` (116 LOC) | **9 columns** (Compañía / Banco / Cuenta / Saldo / Divisa / Estado / Último sync / **Validación** / action), sortable via `sort_link`, group_by-aware, group header rows, `AccountRowComponent` renders each row |
| Connections tab | `app/views/sync_dashboard/_connections_tab.html.erb` (40 LOC) | **10 columns** (Conexión / Usuario / Entidades / Cuentas / Estado / Último sync / **Programación** / **Modo de Sync** / 2FA / sync-button), `ConnectionRowComponent` renders each, table footer with count |
| Empty states | Inline in both tab views | Minimal — gray-100 circle + heroicon + Spanish copy + filter-aware sub-copy |
| Visual palette | Throughout | **Tailwind `slate-50/100/200/400/500/700/900`** + **`tesote-blue-*`** + **`bg-tesote-tan`** outer, **`shadow-sm`** on every card / button / chip, mixed `rounded-xl / rounded-lg / rounded-full` |
| Feature flags | Flipper | `sync_operations_dashboard` (page gate — off ⇒ redirect to `v2_tesote_accounts_path`); `sync_accountability_actions` (banner gate) |

**Already aligned with new design — keep as-is**: Heroicons everywhere (no emojis), ViewComponent architecture, Turbo Streams, Ransack + session persistence, per-connection sync API, workspace-scoping, Estado as a single column.

**Drift to fix**: every color token, `shadow-sm` usage, currency-card sizing, `Panel de Sincronización` title, `Validación` column rendering, `Sync` column missing label, default `group_by` of `entity`, sort-by-raw-`balance_cents` (cross-currency broken), font stack lacks Geist Mono.

---

## What changes (per-file change table)

| Production file | Change in v1.1 |
|---|---|
| `app/views/sync_dashboard/index.html.erb` | `content_for(:title, "...Panel de Sincronización")` → `"...Saldos"`. `PageHeaderComponent` title arg → `"Saldos"`. Currency summary cards: replace inline Tailwind block (lines 35–82) with Lunour-token-based markup matching [[prototypes/saldos-v4-functional]] currency strip (fixed 92px, Geist Mono, single-line BCV sub for VES). Tab labels: keep `Cuentas` left, rename `Por conexiones bancarias` → `Conexiones Bancarias`. All `slate-*` / `tesote-tan` / `shadow-sm` replaced per token migration. |
| `app/components/sync_dashboard/filter_bar_component.html.erb` | **Visual token swap only.** All `tesote-blue-*` confirmed = Lunour `blue-700` family; all `tesote-gray-*` → Lunour `gray-*`; `border-tesote-blue-300` → `var(--blue-200)`; `shadow-sm` → border-only; chip row `bg-tesote-blue-50/30` retained but verified against Lunour blue-50. **No behavior change.** |
| `app/components/sync_dashboard/filter_pill_component.html.erb` | Visual token swap. `ACTIVE_CLASSES` / `INACTIVE_CLASSES` in `.rb` audited — keep blue-50 / gray-200 family. No behavior change. |
| `app/components/sync_dashboard/account_row_component.{rb,html.erb}` | **Drop Validación cell** from the row template (the `<td>` rendering reconciliation stat). Add row-level click: `data-action="click->row-navigate#go" data-row-navigate-href-value="/connect/movimientos?query[tesote_account_id_in][]=<%= account.id %>"` (or equivalent Rails link wrapping). Saldo cell: add `font-family: 'Geist Mono'` via CSS class. Account number display (`··6733`): same. Pill rendering: confirm Lunour pill family. |
| `app/views/sync_dashboard/_accounts_table.html.erb` | **Drop `<th>Validación</th>`** and corresponding `<td>` (lines ~54–59 + wherever Validación cell renders). Update colgroup widths. Group-header colspan: 9 → 8. Sort link on Saldo column remains; sort default + dollarization happen in the service (see below). |
| `app/components/sync_dashboard/connection_row_component.{rb,html.erb}` | **Visual retrofit only in v1.1.** Programación + Modo de Sync columns stay (deferred to v1.2). Sync button: confirm disabled-state logic + tooltips ("Re-autentica primero" on `credentials_changed`, "Sync en curso" on `syncing`). 2FA tag: Lunour tokens. Acct-num: Geist Mono. **No row-click behavior** (drawer is v1.2). |
| `app/views/sync_dashboard/_connections_tab.html.erb` | **Last column `<th class="px-4 py-3 w-12 text-right"></th>` → `<th>Sync</th>`** with widened col width. All token swaps. Footer count copy: confirm Spanish + Lunour text color. |
| `app/services/sync_dashboard/index_data_service.rb` | Add `balance_in_usd_cents(account)` helper: `VES` → `account.balance_cents / @bcv_rate`, `EUR` → `account.balance_cents * 1.08` (or load proper EUR→USD `ExchangeRate`), `USD` → `account.balance_cents`. In `load_filtered_accounts`, after Ransack `.to_a`, apply `.sort_by { -balance_in_usd_cents(_1) }` when active sort is `balance_cents desc`. **Only affects in-memory sort; Ransack query unchanged.** |
| `app/controllers/sync_dashboard_controller.rb` | Single one-line change: `resolve_group_by`'s default fallback `'entity'` → `'none'`. Everything else preserved (session persistence, flag gates, exchange rate load, etc.). |
| Sidebar nav (wherever it's defined — `Ui::SideNavComponent` or partial) | Nav item label `Panel de Sincronización` → `Saldos`. Confirm active-state matches `/connect/saldos` if route alias is added; if route name stays `sync_dashboard_path`, active-state stays at that route. |
| `config/routes.rb` | **Optional** alias: `get '/connect/saldos', to: 'sync_dashboard#index', as: :saldos`. Original `sync_dashboard_path` preserved. Recommendation: ship the alias for clean URL; old URL keeps working. |
| `application_v2.html.erb` (or wherever fonts load) | Add Geist Mono Google Fonts `<link>` (or self-host). Weights `500 / 600 / 700`. |
| Tailwind config (`config/tailwind.config.js`) | Confirm `tesote-blue-700` = `#1661E2` (Lunour brand blue). If currently a different shade, align. Confirm `tesote-tan` = `#F7F5F0` (Lunour `gray-50`). Add `'mono': ['Geist Mono', 'SF Mono', 'Menlo', 'monospace']` to `fontFamily` if not already. |
| `SyncAccountability::BannerComponent` | **Out of scope** for behavior; visual token audit only (Lunour palette). |

---

## What does NOT change

Spell these out explicitly so `/tesote-plan` doesn't speculate work:

- **Routes**: `sync_dashboard_path` keeps its name. `SyncDashboardController` keeps its class name. (Optional `saldos_path` alias is the only routing addition.)
- **Ransack filter mechanism**: 5 fixed pills, `Shared::MultiSelectComponent`, 24h `session[:sync_dashboard_filters]`, auto-submit 300ms debounce, chip secondary row, count badge, `Limpiar` reset button. **Not** migrating to the Movimientos v5 `+ Filtrar` builder.
- **Group-by mechanism**: `VALID_GROUP_BY = %w[entity bank currency none]` stays. Session persistence stays. UI control unchanged. Only the **default fallback** changes from `entity` → `none`.
- **Turbo Streams**: every `turbo_frame_tag`, the `index.turbo_stream.erb` response, the `ControlledFrameLoaderComponent` wrapper, the `sync_accountability_banner` frame, the currency-summaries div ID — all preserved verbatim.
- **Sync interactions**: per-connection POST to whatever endpoint `ConnectionRowComponent` triggers, polling cadence, disabled-state logic, completion handling, error toasts. Unchanged.
- **Feature flags**: `sync_operations_dashboard` (page) + `sync_accountability_actions` (banner) continue gating. No new flag.
- **Data scoping**: `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)`. Unchanged.
- **`IndexDataService` data loads**: `ReconciliationStat` + `ReconciliationAccountSummary` still loaded (consumed later by Transacciones page); only the rendering stops on Saldos.
- **Sort columns sortable in headers**: Compañía, Banco, Saldo, Divisa, Último sync — same set. (Estado, Cuenta, 2FA, Programación, Modo de Sync not sortable.) Default flips to `Saldo desc dollarized`.
- **Empty-state pattern**: heroicon-in-circle + Spanish copy + filter-aware sub-copy. Visual retrofit only.

---

## Architecture / Design

**Visual contract**: [[prototypes/saldos-v4-functional]] — single self-contained HTML, ~2400 LOC, fully interactive. Tab toggle, multi-select filter dropdowns with searchable + checklist variants, removable chips, reset, group-by with 4 modes, dollarized saldo desc sort, sync animation with state transitions + toast, drawer drill-in for connections (preview of v1.2), Geist Mono numerics, fixed-height currency cards. Anchor every visual decision against this file.

**Currency strip — locked layout**:

```
┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐
│ VES              7 cuentas  │ │ USD              8 cuentas  │ │ EUR              1 cuenta   │
│ Bs. 888.217.824,37          │ │ $419,073.69                 │ │ —                           │
│ $1,738,909.97  (Tasa BCV…)  │ │                             │ │                             │
└─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘
   ↑ fixed 92px height          ↑ same height (whitespace below) ↑ same height
   ↑ Geist Mono 23px integer + cents unified (same color/size/weight)
```

**Estado pill — locked vocabulary** (already in production, just confirming token alignment):

| State | Where | Pill | Label |
|---|---|---|---|
| `ok` | Account `estado` / Connection `active` | `pill-paid #D6E8D5` + green dot | `Sincronizada` / `Activa` |
| `syncing` | Both | `pill-new #E4ECF7` + blue dot | `Sincronizando` |
| `warn` | Account `estado` | `pill-pending #F7EDD0` + yellow dot | `Requiere atención` |
| `credentials_changed` | Connection | `pill-pending` | `Cambio credenciales` |
| `requires_2fa` | Connection | `pill-pending` | `Requiere 2FA` |
| `sync_failed` | Connection | `pill-overdue #F8D8C0` + orange dot | `Sync falló` |
| `bank_down` | Connection | `pill-overdue` | `Banco caído` |
| `review` | Connection | `pill-draft #ECE7DD` + gray dot | `En revisión` |
| `manual` | Both | `pill-draft` | `Manual` |

---

## Surfaces affected

- `/sync_dashboard` (route name preserved) — the page itself, content area only
- Sidebar nav active item — `Panel de Sincronización` label → `Saldos`
- App shell font stack — Geist Mono added (currently not loaded)
- Tailwind theme — `tesote-blue-*` / `tesote-tan` audited against Lunour

**Not touched**: any other Connect route (Movimientos, KYC onboarding), `SyncAccountability::BannerComponent` (separate flag-gated module), webscraper sync modal turbo frame, authentication, organization switching, permission stack.

---

## Data model implications

**Zero schema changes.** Saldos is read-only over existing `TesoteAccount`, `ExternalServiceBankConnection`, `ExchangeRate`, `ReconciliationStat`, `ReconciliationAccountSummary`, `BankSyncSession`. All loads exist in production today.

Per [[project_tesote_vs_odoo_split]]: Saldos is purely Tesote-side observation, not Odoo-side regulatory record. No Odoo touchpoints. Cross-ref [[reference_finance_db_schema]] for canonical schema path (`tesote_notebook/Finance/schema.rb`).

**Workspace-tenant safety**: `permitted_tesote_accounts` uses `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)` — already enforces `workspace_id` boundary. Unchanged.

---

## AI / automation implications

None in v1.1. Saldos is a read + diagnostic surface; no AI features in scope.

Future AI affordances naturally live in the **connection drill-in drawer** (v1.2): "explain why this connection is unhealthy", "summarize this account's recent activity". Flagged for AI roadmap; not this PRD.

---

## Open decisions (resolved)

| # | Decision | Resolution |
|---|---|---|
| 1 | Filter system: v3 dropdowns vs Movimientos v5 builder | **Keep production's 5-fixed-pill Ransack pattern**. Migration to builder is a separate workstream. |
| 2 | Currency total digit handling | **9-digit integer max, Geist Mono 23px, no auto-step**. Validated against `Bs. 888.217.824,37` worst case. |
| 3 | Validación column on Cuentas | **Kill from render**. Data still loaded server-side for Transacciones page. |
| 4 | Programación + Modo de Sync columns on Conexiones | **Keep in v1.1**. Remove in v1.2 when the drawer lands (data would be stranded otherwise). |
| 5 | Connection drill-in drawer | **Defer to v1.2.** Prototype is the contract; build deferred. |
| 6 | Cuenta drill-in drawer | **Killed entirely.** Cuenta row click → navigate to Movimientos filtered. |
| 7 | Default group_by | `entity` → **`none`** (flat list with dollarized saldo desc sort dominant) |
| 8 | Default sort | `balance_cents desc` (raw) → **`balance_cents desc, dollarized via BCV`** (client-side `sort_by` in service) |
| 9 | Sort dollarization implementation | **Client-side** in `IndexDataService` after `to_a`. Server-side SQL CASE WHEN deferred (not worth schema/index complexity). |
| 10 | Route + controller class rename | **No.** Visible title only. `sync_dashboard_path` + `SyncDashboardController` keep names. Optional `saldos_path` alias for clean URL. |
| 11 | Feature flag | **Keep existing `sync_operations_dashboard` flipper.** No new flag. |
| 12 | Font loading | **Geist Mono via Google Fonts `<link>`** (or self-host — Dan's call at implementation time). |
| 13 | Sync column label | **`Sync`** (was empty `<th>`), widened. |
| 14 | Tab label | `Por conexiones bancarias` → **`Conexiones Bancarias`** |
| 15 | Subtitle warning copy | `N con problemas` → **`N requieren atención`** with singular handling |
| 16 | Cuenta row click target URL | `/connect/movimientos?query[tesote_account_id_in][]=<id>` — **confirm Movimientos controller accepts this Ransack key at implementation time**; fall back to `v2_tesote_accounts_path` filtered if Movimientos new isn't ready. |

---

## Path forward

### V1.1 wedge — this PRD

See Intake. Surgical visual + naming + 2 column changes + 1 default change + 1 sort comparator + 1 row-click rewire. No drawer, no filter-system migration, no data model changes.

### What sequences after v1.1

```
v1.1 (this PRD, ~1 week)   — visual retrofit + naming + Validación kill + Sync label + dollarized default sort + Cuenta→Movimientos row click + token migration
v1.2 (~next sprint)        — ConnectionDrawerComponent + Programación/Modo column removal + cuentas-vinculadas mini-rows in drawer that also navigate to Movimientos + Re-autenticar/Desconectar flows wired
v1.3 (post-Connect-sweep)  — full empty-state hero (illustration + bank-availability strip) + onboarding for zero-bank workspace
v2   (later)               — filter-primitive consolidation across Saldos + Pagos + Cobros + Contrapartes (decide builder vs fixed-pill at that point with multiple consumers)
v2.1 (later)               — AI affordances in connection drawer (explain unhealthy connection, summarize account activity)
v3   (later)               — Transacciones surface (where the Validación / certification data finally lives)
```

### Discipline calls

- **Don't touch Movimientos.** v1.1 only depends on Movimientos accepting one Ransack filter param at the target URL; if that's not ready, fall back to v2_tesote_accounts_path. No Movimientos changes in this PRD.
- **Don't extract the filter primitive doc.** Two consumers (production sync_dashboard + Movimientos v5) is the threshold to extract; doing it pre-v1.1 speculates. Doing it post-v1.1 is mechanical refactor.
- **Don't ship the connection drawer in v1.1.** It's the v1.2 wedge. Resist scope creep.
- **Don't rename routes / controllers.** Internal infra rename has zero user-visible value here. Visible title is the user-facing fix.

---

## References

### Internal source docs (this PRD draws from)

- [[prototypes/saldos-v4-functional]] — **canonical visual + behavior contract**
- [[design]] — Saldos full page design (v3-anchored, still valid for state model + drill-in spec)
- [[spec-eng]] — engineering brief, locked decisions
- [[spec-agent]] — full implementation spec (data contracts, state machine)
- [[../movimientos/design]] — filter-primitive canonical spec (not adopted here but useful context)
- [[../redesigns-week-2026-05-18]] — week PRD (Movimientos drill-in lives there; Saldos slice lives here)
- [[../../design/archetypes]] — table-padding tokens per density
- [[../../design/design]] — Lunour brand tokens
- [[../../_prd-template]] — schema this PRD follows

### External

- **Production codebase**: `~/Programming/tesote/treasury/app/controllers/sync_dashboard_controller.rb` + `app/services/sync_dashboard/index_data_service.rb` + `app/views/sync_dashboard/*` + `app/components/sync_dashboard/*` (8 ViewComponents) — every per-file change in this PRD anchors here.
- **Treasury skill**: `~/Programming/tesote/treasury/.claude/skills/redesign-2026-design-system/SKILL.md` — `/tesote-plan` will pull this in automatically; it's the design-system gate.
- Linear ticket: [TBD]
- Treasury plan dir: [TBD]

### Memory references (load-bearing context)

- [[project_filter_system_primitive]] — context for the decision to keep production's pattern (not adopt Movimientos v5)
- [[project_tesote_command_center]] — Saldos sits inside Connect, the inbound observation half
- [[project_tesote_vs_odoo_split]] — Saldos is Tesote-side observation; no Odoo touchpoints
- [[feedback_no_emojis]] — production already uses heroicons (compliant); audit any new SVG
- [[reference_finance_db_schema]] — canonical schema for the read-only data Saldos consumes
- [[feedback_tesote_plan_workflow]] — this PRD → Linear PRO ticket → `/tesote-plan` in treasury

---

## Before I run `/tesote-plan` — checklist

All 16 decisions above are **resolved**. Three implementation-time confirmations remain — flag for `/tesote-plan` to resolve with Dan during planning:

1. **Movimientos filter param** — does the Movimientos controller (production or new redesign branch) accept `?query[tesote_account_id_in][]=<id>` as a Ransack filter? If not yet, use `v2_tesote_accounts_path` filtered URL as the fallback target for Cuenta row click.
2. **Tailwind token audit** — confirm `tesote-blue-700` in `config/tailwind.config.js` is `#1661E2` (Lunour) and not a Tailwind default. If not, align as part of this PRD's scope (it's the design-system gate).
3. **Geist Mono loading strategy** — Google Fonts `<link>` (fastest to ship) vs. self-host via `app/assets/fonts/` (more control, no third-party dep). Dan's call at implementation time.

After Luis confirms this PRD reads correctly, the next concrete moves are:

```
# 1. File the Linear PRO ticket — paste this PRD's Tesote-Plan Intake block verbatim as the description
#    Title: "Saldos — v1.1 retrofit on production sync_dashboard"
#    Then update saldos-prd.md frontmatter: linear: <ticket URL>, status stays ready-for-tesote-plan

# 2. cd to treasury and run /tesote-plan:
cd ~/Programming/tesote/treasury
/tesote-plan <Linear-ticket-URL>

# 3. Plan lands at treasury/.debugging/plans/saldos-v1-1-retrofit/
#    Hand to Dan, or run /implement directly
```

---

*Drafted 2026-05-18; restructured 2026-05-19 after reading production `sync_dashboard` and locking visual + behavior decisions via [[prototypes/saldos-v4-functional]]. The prototype is the contract; this PRD is the bridge to treasury.*
