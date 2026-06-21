---
title: Movimientos — v1.1 Retrofit PRD (against production transactions page)
tags: [product, prd, connect, movimientos, ws-1, redesign]
updated: 2026-05-19
status: ready-for-tesote-plan
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: https://linear.app/tesote/issue/PRO-152/movimientos-v11-retrofit-on-production-transactions-page
tesote_plan_dir: [TBD]
---

# Movimientos — v1.1 Retrofit PRD

> **One-line purpose.** Surgically retrofit the production `transactions` page (live in `treasury/app/controllers/transactions_controller.rb` + `Transactions::IndexDataService` + 2 view partials + the `TesoteTransactions::SearchFiltersComponent` + `TesoteTransactions::FilterPresetsComponent` + the `Ui::DataTableComponent` redesign partial) into the new Movimientos design — visual contract from [[prototypes/movimientos-v6]], naming (Transacciones → Movimientos), 4 killed columns, Banco+Cuenta merge, paperplane (Compartir) trailing action, Geist Mono numerics, 36px density, stacked totals cards above the filter bar, default Fecha 30 días — **without touching the Ransack query, the session-persistence mechanism, the `SearchFiltersComponent` (4-section collapsible) form, the server-backed `transaction_filter_presets`, the cash-flow chart, the bulk-edit infrastructure, the `transaction_show_page` flag, the existing turbo frame names, or any data-model bones**. Mercury-style filter builder + side-panel drill-in defer to v2 / v1.2.

> **Visual + behavior contract.** [[prototypes/movimientos-v7-retrofit]] — open in browser. Every visual decision in this PRD is anchored to that file. Where the prototype and this doc disagree, the prototype wins. [[prototypes/movimientos-v6]] remains the design-exploration superset (includes the deferred Mercury filter builder + slide-over drill-in previews); v7-retrofit is the v1.1-scoped subset locked for shipping after Mercury-density iteration on 2026-05-19.

---

## Tesote-Plan Intake

> Treasury's `/tesote-plan` ingests this block. Tight. Match format exactly.

### Actor & Problem

As a **Tesote workspace admin (Mariel — internal dogfood; named prospects in live demos)**, I need to **open Connect → Movimientos and have it look + feel like the rest of the new Tesote — not the partially-redesigned in-flight state it currently ships in** because **the production `transactions` page is mid-migration (a `_transactions_table_redesign.html.erb` partial already uses `Ui::DataTableComponent` + `text-redesign-*` tokens + the freshly-shipped Estado pill, gated by `redesign_2026?`), but four load-bearing v6 brain decisions are still missing from production: (1) page is titled "Transacciones" not "Movimientos", (2) totals are rendered as table-footer "Resumen de página" rows instead of stacked currency cards above the filter bar, (3) the production column set has 11 columns (Fecha · Referencia · Banco · Cuenta · Descripción · Nota · Monto · Estado · Categoría · Contraparte · Acciones) when the v6 contract is 7 (Fecha · Banco/Cuenta merged · Descripción · Contraparte · Monto · Categoría · Compartir), (4) the row-trailing action is an ellipsis-menu to a show page / edit modal, when v6 specifies a `paperplane (Compartir)` always-visible icon that opens a share dialog — and the Saldos retrofit shipping in parallel makes this drift acutely visible**.

### The Test

This solves **visual + naming + column-set + totals-placement + trailing-action drift** for **Mariel + named-prospect demos** in **Connect**. Without it: **the second surface in a Tesote demo (Movimientos is reached by Cuenta row-click from the polished new Saldos) shows a half-migrated 11-column page with table-footer totals next to the polished new Saldos surface, undermining the "Saldos = where I stand · Movimientos = what moved" couplet the Connect demo opens with**.

### V0 — Simplest thing that works

- [ ] **Naming**: page title, document title, sidebar nav label all change `Transacciones` → `Movimientos`. The i18n key `nav.transactions` resolves to `Movimientos` (es.yml). `content_for(:title, "#{@workspace.name} - Movimientos")` in `app/views/transactions/index.html.erb`. `Ui::PageHeaderComponent` title arg → `Movimientos`. Empty-state copy `No hay transacciones disponibles para mostrar.` → `No hay movimientos disponibles para mostrar.`. Component test_id `transactions-page-header` / `redesign-transactions-table-card` retained (internal IDs, not user-facing).
- [ ] **Compact stacked totals strip rebuilt** above the filter bar to the [[prototypes/movimientos-v7-retrofit]] spec: 2-card grid (VES + USD; EUR / additional currencies appear as users add cuentas in those currencies; cards render in canonical order VES → USD → EUR via JS), Lunour border + `border-radius: 8px` (was 12px — smaller for the compact treatment), card padding `12px 16px` (was `18px 22px`), three stacked rows per card (Ingresos / Egresos / Neto with solid divider above Neto + dashed divider between Ingresos/Egresos), label-left 80px column + amount-right tabular-nums, **Geist Mono 13px / 500-weight** for Ingresos/Egresos and **14px / 600-weight** for Neto (was 18px / 20px before density iteration on 2026-05-19 — Luis flagged the original treatment as too space-heavy; tested Mercury-style horizontal port and reverted to stacked-but-smaller). Currency label 10.5px uppercase tracking. **Pulled out of the table footer**; the `tfoot` "Resumen de página" rows in `_transactions_table.html.erb` go away. Render inside a new `turbo_frame_tag :transactions_totals` so it recomputes on filter changes. `filtrado` tag appears beside the currency code when filters beyond the default Fecha are active.
- [ ] **Columns killed (4) per [[prototypes/movimientos-v6]] + design doc lock #4 / #5 / #23 / v1.1 add-on**: drop `Referencia`, `Nota`, `Estado` (the freshly-shipped status pill — deferred per v5 design lock #5 until rail data has real pending states), and `Acciones` from the `columns` array in `_transactions_table_redesign.html.erb` (lines 38–50) and their corresponding `with_cell` blocks. **Reasoning**: Referencia → moved to drill-in (v1.2). Nota → replaced by note-icon inside Descripción cell (sparse SVG when `transaction.note&.content.present?`, full text in cell `title=""` tooltip + future drill-in). Estado → re-evaluate when rail pending states materialize. Acciones → replaced by paperplane Compartir column.
- [ ] **Banco + Cuenta merged into one `Banco/Cuenta` cell**: drop the `:bank` and `:account` columns; introduce a new `:bank_account` column rendering `<bank short name> · <cuenta nickname> ··<last-4>` inside one `<td>` — **text only, no bank-logo glyph** (tested 2026-05-19 with logo + without; the logo added visual noise without disambiguation value since the bank short-name already labels the row). Last-4: monospace `text-redesign-text-3`. **The merged cell becomes the row's primary "where it happened" anchor**; replaces the two prior cells.
- [ ] **Paperplane (Compartir) trailing column added** — new `:share` column at the end of the `columns` array. Header label: `Compartir`. Column width **90px** (was 50px; widened so the header reads in full at 11px uppercase tracking instead of truncating). Cell renders an inline SVG paperplane icon (no emoji per [[feedback_no_emojis]]), centered, always-visible (not hover-only), low-key at rest (gray stroke on transparent), primary on hover (blue fill + `--primary-light` bg + primary border). Click opens a `Movimientos::ShareModalComponent` stub modal — title `Compartir movimiento`, primary CTA `Compartir`, body lists destinations (counterparty on file / teammate / free-form email/WhatsApp) but **destinations + channels + actual send are deferred to v1.2** (modal renders, captures intent, no-ops on Compartir click with a "Compartido (simulado)" toast).
- [ ] **Inline-edit on Contraparte + Categoría preserved + always-visible ▼ caret** — production already uses `TransactionCategories::AssignedCategoriesComponent` + `Counterparties::AssignedCounterpartiesComponent`; confirm both expose click-to-edit dropdown affordance and that the dropdown menus consume Lunour tokens (not Mercury pastels). **Add an always-visible chevron-down ▼ caret** to the right of each editable cell value (12×12 SVG, `text-redesign-text-3` at 65% opacity at rest, full color on cell hover) — makes the dropdown affordance discoverable without requiring hover-state reveal. Em-dash `—` placeholder when null. **Contraparte cell renders text-only** (no avatar chip — tested 2026-05-19, visual noise without proportional payoff; counterparty-as-identity surfaces elsewhere). Tooltip on dash: "click para asignar".
- [ ] **Density — 40px row height locked** across the redesign table (was default ~44px in production; 36px tested in v6 and felt cramped — bumped after Mercury-density iteration 2026-05-19). One-line rows, no two-line treatments, no wrap on any cell. `table-layout: fixed` + per-column widths via the `columns` array passed to `Ui::DataTableComponent` (Fecha 80px · Banco/Cuenta 220px · Descripción flex · Contraparte 220px · Monto 160px · Categoría 150px · Compartir **90px**). **Content max-width 1440px** (was 1320px) for horizontal breathing room on the column widths. Cell horizontal padding 14px (was 12px). **Descripción truncation pattern locked**: `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` + native `title=""` carrying the full text. Row height never breaks.
- [ ] **Default Fecha filter — 30 días** (was `last_week` / 7 días). Single change to `query_filters` method in `transactions_controller.rb` lines 100–132: replace `else` fallback `filters[:transaction_date_gteq] = 7.days.ago` with `filters[:transaction_date_gteq] = 30.days.ago`, and `date_filter_type` radio defaults shift to a new option `30d` (label `Últimos 30 días`) — and the previous `last_week` (`Últimos 7 días`) radio remains available, just not the default.
- [ ] **Geist Mono via Google Fonts** wired into `application_v2.html.erb` (or self-hosted — Dan's call). Applied to: totals card amounts (Ingresos / Egresos / Neto), Monto column, Banco/Cuenta last-4 display.
- [ ] **Estado pill family verified** (still applies to Saldos and other tables that keep an Estado column — the killed column here was the row-level Estado, not the global pill family). All Lunour pill backgrounds (`pill-paid #D6E8D5`, `pill-new #E4ECF7`, `pill-pending #F7EDD0`, `pill-overdue #F8D8C0`, `pill-draft #ECE7DD`) consumed via `Ui::PillComponent` variants per the redesign skill — confirm no Mercury-pastel drift on this surface's Categoría chip rendering.
- [ ] **Design tokens migrated** across every touched file: `text-tesote-blue-*` → Lunour `text-redesign-primary` family; `text-tesote-red-*` → `text-redesign-status-red`; `bg-tesote-tan` → `var(--bg-main)` (white) for content area, `var(--bg-sidebar) #F7F5F0` for sidebar; `border-tesote-gray-200` → `border-redesign-border`; `shadow-md` on table wrapper → `1px solid var(--border)` (borders > shadows); confirm `rounded-redesign` (8px) and `rounded-redesign-sm` (4px) match Lunour `--radius` / `--radius-sm`. The production `redesign-*` tokens **must resolve to Lunour values** in Tailwind config; if not, align as part of this PRD's scope.
- [ ] **Default sort preserved**: `s_date asc, created_at asc, id asc` is fine as the underlying Ransack sort, but visible UI default = `Fecha desc` (most recent first). Confirm sort direction matches v6 prototype on page-load.
- [ ] **Filter chip row** below the filter form (the existing `Shared::FilterChipsComponent`): visual token swap to Lunour. Behavior preserved.

### Out of Scope (explicit "Not Doing")

- **Mercury-style filter builder** (single `[+ Filtrar]` button + popover + dimension picker + 11 dimensions per design doc Round-3 locks #18–22) — **deferred to v2 as the canonical filter primitive workstream** ([[project_filter_system_primitive]]). v1.1 keeps the production 4-section collapsible `SearchFiltersComponent` form verbatim with visual token swap only. **Reasoning**: filter-primitive consolidation across Movimientos + Saldos + Pagos + Cobros + Contrapartes is its own multi-surface workstream; building it inside a Movimientos retrofit PRD speculates the API and forces every consumer to re-litigate dimensions.
- **Side-panel slide-over drill-in (Surface A)** — deferred to **v1.2**. The v6 prototype shows what it should be (mirrors the Cobros invoice-click panel pattern); building `Movimientos::DrillInPanelComponent` + its turbo frame + the field grid + the "Compartidos" section + the future "Reconciliación" section is real new work. Row click in v1.1 continues to route to the existing show page (gated by `Flipper.enabled?(:transaction_show_page, workspace)`) OR the edit modal — exactly as production today.
- **Full individual movimiento page (Surface B)** — already exists in production at `/tesote_account/:tesote_account_id/tesote_transactions/:id` via `TesoteTransactionsController#show` (gated by `transaction_show_page` flag). **Not redesigned in this pass.** When the slide-over lands in v1.2, Surface B becomes "Ver página completa →" from the panel; Surface B's own visual retrofit is a separate ticket.
- **Compartir destinations + channels + actual send** — paperplane opens a modal stub only. Picking destinations, formatting the row details, choosing channel (counterparty on file / teammate inside Tesote / free-form email / WhatsApp), wiring the send infrastructure — all deferred. v1.1 ships icon + stub modal + "Compartido (simulado)" toast.
- **Server-backed saved-views beyond what already exists** — the production `transaction_filter_presets` table + `TesoteTransactions::FilterPresetsComponent` (personal + shared + default-flag, save modal, delete modal) is **more evolved than the v6 brain spec's localStorage saved views**. v1.1 keeps production's preset system as-is, visual token swap only. The v6 prototype's localStorage saved-views are abandoned in favor of production's better implementation. (This means design doc Round-3 lock #22 "Saved views — named filter combinations, persisted to `localStorage` for v4 (server-backed in production)" is **already realized in production**.)
- **Bulk-edit infrastructure** — the existing `Shared::BulkEdit::SelectComponent` + bulk-categorize / bulk-counterparty modals continue to render in the legacy table partial. **Not on the redesign partial today** (gated by `redesign_2026?`); whether bulk select lands in the redesign table is a separate ticket. v1.1 does not add bulk-edit to the redesign partial.
- **Cash-flow chart (`TesoteTransactions::CashFlowSectionComponent`)** — keeps its visual + behavior verbatim, separate turbo frame `:transactions_chart`. Visual token audit only (Lunour palette). Not redesigned in this pass beyond token swap.
- **Export modal (`TesoteTransactions::ExportModalComponent`)** — keeps verbatim, visual token swap only.
- **Edit modal (`tesote_transactions/_edit_tesote_transaction_modal.html.erb`)** — keeps verbatim, visual token swap only. Reached when `transaction_show_page` flag is off.
- **Per-account drilled view** (`TesoteTransactionsController#index`) — separate controller, scoped to a single `tesote_account_id`, with its own `insights` + `related_transactions` + `comments`. **Not redesigned in this pass.** Reached from Saldos Cuenta row click; that target URL change (`tesote_account_tesote_transactions_path(account.id)`) is what the Saldos PRD anchored against. This PRD touches the multi-account `TransactionsController#index` only.
- **Route / controller rename** — `transactions_path` and `TransactionsController` keep their names. **Visible title rename only.** Avoids touching every spec path + every internal `tesote_transactions` reference + every `transactions_path` call site across the codebase.
- **Optional `movimientos_path` alias** in `config/routes.rb` is the only routing addition under consideration; recommendation is to ship it for clean URL (`/connect/movimientos`); old `/transactions` URL keeps working.
- **PDF export (`TransactionsController#show`)** — unchanged. PDF template is a separate concern from the index page.
- **KYC onboarding** + **Saldos** + **Pagos** + **Cobros** new surfaces — all separate scopes.
- **Empty state full hero design** — keep production's existing minimal "Sin movimientos" empty state, visually retrofitted only.
- **Sticky header, virtualization, CSV export beyond the existing export modal, multi-select bulk actions in the redesign partial, mobile, dark mode** — deferred.

### Technical Requirements

- [ ] Spanish copy on every user-facing string. `nav.transactions` i18n value becomes `Movimientos` (es.yml). Empty-state, modal headers, toast copy all in Spanish.
- [ ] **Geist Mono** loaded via Google Fonts `<link>` (or self-host if Dan prefers) with weights `500;600;700`. Wired in `application_v2.html.erb` head. (Same loading strategy as Saldos retrofit — share the work.)
- [ ] **Inter Tight + Aspekta** continue per [[../../design/design]] — full migration to those is its own workstream.
- [ ] `tabular-nums` on totals card amounts and Monto cell (implicit in Geist Mono; explicit `font-variant-numeric: tabular-nums` on any non-mono numeric).
- [ ] All visual tokens consumed from Lunour palette via Tailwind theme extension or CSS vars. **Zero hardcoded `slate-*`, Tailwind default `gray-*`, `tesote-blue-*`, `tesote-red-*`, `tesote-tan`, `tesote-gray-*`, or `#000` text** in any touched file. The `text-redesign-*` token family must resolve to Lunour values in `tailwind.config.js`.
- [ ] **Multi-tenant**: `workspace_id` scoping preserved via `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)` in `permitted_tesote_accounts`. No changes to data scoping.
- [ ] **Feature flags**: existing `redesign_2026` flipper continues to gate the redesign partial vs legacy. Existing `transaction_show_page` flipper continues to gate row-trailing-action target (show page vs edit modal — though the Acciones column itself goes away, the underlying flag stays). **No new flag.**
- [ ] **Turbo Streams**: existing `index.turbo_stream.erb` + `turbo_frame_tag :transactions_filters` + `turbo_frame_tag :transactions_chart` + `turbo_frame_tag :transactions_table` all preserved verbatim. **New**: `turbo_frame_tag :transactions_totals` for the stacked totals strip (recomputes on filter changes). The `Transactions::IndexDataService` already computes `currency_totals` single-pass; the frame just renders the new card markup with that data.
- [ ] **Ransack filter mechanism**: every dimension currently in the `SearchFiltersComponent` — `tesote_account_id_in`, `tesote_account_tesote_legal_entity_id_in`, `tesote_account_bank_name_in`, `counterparty_id_in`, `transaction_categories_id_in`, `transaction_categories_id_not_in`, `amount_currency_eq`, `transaction_type` (session-only), `amount_filter_type` (session-only), `amount_cents_eq_money`, `amount_cents_gteq_money`, `amount_cents_lteq_money`, `transaction_date_gteq`, `transaction_date_lteq`, `description_cont`, `note_content_cont`, `external_service_id` (combined eq/cont via scope) — preserved verbatim. Only visual tokens change inside the component template.
- [ ] **Session persistence**: `session[:transaction_filters]` + 24h expiry logic preserved (`transactions_controller.rb` lines 140–248).
- [ ] **Filter presets**: `transaction_filter_presets` table + `FilterPresetsComponent` (personal + shared + default + save modal + delete modal) preserved verbatim. Visual token swap only.
- [ ] **No emojis** — production already uses `heroicon` helper; **the existing `&crarr;` arrow on the "Aplicar Filtros" button is the one emoji-codepoint in this surface — replace with an inline SVG arrow** per [[feedback_no_emojis]]. New paperplane Compartir icon is an inline SVG, not a `✈` codepoint.
- [ ] **Locked pill family** — `Ui::PillComponent` consumed by Categoría rendering uses Lunour `pill-*` tokens, not Mercury pastels (`#e4e8f7`, `#fdefce`, `#fddcc5`, `#d8e9de`, `#eef1f4` — drift to kill). The killed Estado column's variants (mint/amber/salmon/gray/lavender) stay defined on `Ui::PillComponent` for other surfaces.
- [ ] **Performance**: initial paint <300ms for ≤200 movimientos (production per_page = 200, max 500), filter recompute <50ms client-side after Turbo Stream lands, totals recompute <50ms (already single-pass in `IndexDataService`). N+1 prevention preserved via `Current.cache` in `populate_request_cache`.

### Rollout Plan

1. **Internal** — Tesote Finance workspace (Mariel dogfoods on real data). Luis + Mariel walk through `/connect/movimientos` end-to-end: every filter combination, every active filter chip, the totals strip recompute, inline-edit on Contraparte + Categoría, the paperplane stub modal, the merged Banco/Cuenta cell with last-4 disambiguation, the note-icon-in-Descripción when notes are present, the 30-day default + filter persistence across page reloads.
2. **Beta** — first 2–3 friendly prospect demos. Movimientos is the second surface in the demo flow (Saldos → click Cuenta row → Movimientos filtered to that account).
3. **GA** — existing `redesign_2026` flipper flipped on for all workspaces. No new flag needed.

---

## Context (why now)

The original Movimientos `design.md` (locked through v6 brain prototype 2026-05-17) was drafted assuming the production page was Mercury-style-builder-ready and that the visual + filter-builder + drill-in could all land together. **Reading `treasury/app/controllers/transactions_controller.rb` and its 7-file dependency graph (controller + service + 2 view partials + 2 components + page header) changed the framing entirely** — Movimientos is already live as `transactions`, partway redesigned (a `_transactions_table_redesign.html.erb` partial already uses `Ui::DataTableComponent` + the `text-redesign-*` token family + a freshly-shipped Estado pill column per ENG-3820), gated by `redesign_2026?`, with a working Ransack filter system, working 24h-session-persisted filters, working server-backed `transaction_filter_presets` (personal + shared + default), working currency totals single-pass in `IndexDataService`, and working nested turbo frames for filters / chart / table.

The retrofit is therefore not "build Movimientos". It's: **rename, swap the visual surface, lift the totals strip out of the footer into stacked cards above the filter bar, merge Banco+Cuenta into one cell, kill 4 columns, add the paperplane stub, drop default Fecha from 7d to 30d, and don't touch anything else**.

The interactive prototype [[prototypes/movimientos-v6]] (2026-05-16 → 2026-05-17) locked every visual + behavior decision by direct manipulation across v1–v6: column anatomy, Banco/Cuenta merge, description truncation pattern, em-dash placeholders, paperplane always-visible affordance, stacked totals strip handling 10-digit Bs without wrapping, the (deferred) Mercury filter builder mockup, the (deferred) drill-in slide-over. **That file is the visual contract this PRD ships.** The filter builder + drill-in survive in the prototype as v2 / v1.2 previews; v1.1 is the surgical wedge.

This pattern mirrors [[../saldos/saldos-prd]] — Saldos retrofit was also surgical, also kept the production filter mechanism, also deferred the slide-over drill-in, also did the visual + naming + density flip. The two PRDs ship together to make Connect's first two surfaces coherent in the internal demo.

---

## Current production state (read 2026-05-19 from `~/Programming/tesote/treasury`)

| Surface | Production file(s) | What's there |
|---|---|---|
| Controller | `app/controllers/transactions_controller.rb` (248 LOC) | `match :transactions, via: %w[get post]` route, 24h `session[:transaction_filters]` persistence, `determine_active_filters` priority logic (params > session > defaults), `default_query_sorts = ['s_date asc', 'created_at asc', 'id asc']`, `permitted_tesote_accounts` scoping, turbo_stream + html response, `query_filters` builds Ransack + handles date_filter_type (`today` / `last_week` / `last_month` / `month` / `custom`), default = last 7 days |
| Data service | `app/services/transactions/index_data_service.rb` (173 LOC) | Loads paginated `tesote_transactions` (per_page 50/100/200/500, default 200), pre-computes `currency_totals` in a single pass (grouped by `amount_currency`, inflow/outflow/net), populates `Current.cache` with `:recently_updated_categories_by_transaction_id` + `:recently_updated_counterparties_by_transaction_id` (kills the per-row `.any?` N+1), loads `transaction_categories` + `tesote_legal_entities` + `counterparties` + `bank_names` |
| Layout view | `app/views/transactions/index.html.erb` (71 LOC) | Page header (gated `redesign_2026?` → `Ui::PageHeaderComponent` else `Shared::PageHeaderComponent`) with title `Transacciones`, `Shared::ControlledFrameLoaderComponent` wrapper, **3 turbo frames** (`:transactions_filters` + `:transactions_chart` + `:transactions_table`), `bg-tesote-tan` outer (legacy) / Lunour bg (redesign) |
| Filter component | `app/components/tesote_transactions/search_filters_component.{rb,html.erb,_controller.js}` | **4-section collapsible inline form** (not a popover builder): "Compañías, Cuentas y Bancos" (3-col grid of MultiSelect: Cuentas / Compañías / Bancos) · "Contrapartes y Categorías" (Counterparties + Cats-with + Cats-without) · "Monto y Financiero" (Divisa / Tipo radio / amount exact-or-range) · "Detalles de Transacción" (Date radio 5-buttons + custom date pickers + Descripción text + Notas text + Referencia segmented control). Form: `search_form_for query`, ID `tesote_transactions_filters_form`, submits POST to `transactions_path`. Buttons: `Restablecer Filtros` + `Aplicar Filtros` (with `&crarr;` emoji). Below: `Shared::FilterChipsComponent` for removable applied-filter chips |
| Filter presets | `app/components/tesote_transactions/filter_presets_component.{rb,html.erb}` + `app/models/transaction_filter_preset.rb` | **Server-backed** named filter combinations. Dropdown trigger `Filtros Guardados` with bookmark icon + count badge. Menu: "Guardar filtro actual…" + `Mis Filtros` section (personal, with star = default + trash on hover) + `Compartidos` section. Save modal + delete confirmation modal. Inline "Guardar esta búsqueda" CTA when filters are active. Per-user, per-workspace; shared-with-team flag; default flag (auto-applies on visit). **Already more evolved than the v6 brain spec's localStorage saved-views.** |
| Legacy table | `app/views/transactions/_transactions_table.html.erb` (388 LOC) | Top-level `if redesign_2026?` → renders `_transactions_table_redesign`, else legacy markup. Legacy: **11 columns** (Checkbox bulk-select sticky left · Fecha · Referencia · Banco · Cuenta · Descripción · Nota · Monto · Categoría · Contraparte · Actions sticky right). `bg-white` + `shadow-md` table. `bg-gray-50` header. Footer `tfoot` "Resumen de página" rows (3 per currency: Ingresos ↑ green · Egresos ↓ red · Neto). Pagination: "Mostrar 50 · 100 · 200 · 500 por página". Bulk-edit modals for categories + counterparties. |
| Redesign table | `app/views/transactions/_transactions_table_redesign.html.erb` (226 LOC) | Uses `Ui::DataTableComponent` declaratively. `columns` array: 11 entries (`date`, `reference`, `bank`, `account`, `description`, `note`, `amount`, `status`, `category`, `counterparty`, `actions`). `status_pill_variants` + `status_pill_labels` dicts (mint=Conciliado / amber=Pendiente / salmon=Fallido / gray=Borrador / lavender=Nuevo/Por procesar/Externo). Cells use `text-redesign-*`, `rounded-redesign-*`, `bg-redesign-surface-soft`. **No paperplane.** **No Banco/Cuenta merge.** **No stacked totals strip — totals still render inside the same pagination footer.** **Estado pill column ALREADY SHIPPED** (ENG-3820). |
| Cash-flow chart | `app/components/tesote_transactions/cash_flow_section_component.{rb,html.erb}` | Turbo frame loader (lazy-loads chart). `text-tesote-blue-700` button. Not redesigned. |
| Comments / insights | `app/components/tesote_transactions/{comments_section,comment_item,note,related_transactions,export_modal}_component.{rb,html.erb}` | Render on the per-account `TesoteTransactionsController#show` page only — not on the multi-account `TransactionsController#index` we're retrofitting. Out of scope. |
| Query builder | `app/queries/queries/index_transactions.rb` | Wraps Ransack with permission scoping; memoizes query object |
| Sidebar nav | `app/views/layouts/application_v2.html.erb` (or its partial) | i18n key `nav.transactions` → label = `Transacciones`. Path: `transactions_path`. Icon: `currency-dollar` heroicon. |
| Feature flags | Flipper | `redesign_2026` (workspace-scoped — gates page header + table partial choice + token family); `transaction_show_page` (workspace-scoped — gates row-trailing action target: show page vs edit modal) |

**Already aligned with new design — keep as-is**: heroicons everywhere (no emojis except the `&crarr;` arrow on Aplicar Filtros — fix in v1.1), `Ui::DataTableComponent` declarative columns architecture, `text-redesign-*` token family, Estado pill via `Ui::PillComponent` with Lunour variants, Ransack + 24h session persistence, server-backed filter presets (better than v6's localStorage saved-views), inline-edit components for Contraparte + Categoría, single-pass currency totals in `IndexDataService`, request-scoped `Current.cache` N+1 fixes, 3 nested turbo frames, workspace-scoping via `authorized_scope`, Spanish copy throughout.

**Drift to fix**: visible page title + sidebar nav label still `Transacciones`, 11 columns where v6 wants 7, Banco + Cuenta separate when v6 merges, no paperplane Compartir column, totals at table footer when v6 wants stacked cards above filter bar, default Fecha = 7d when v6 wants 30d, `&crarr;` emoji codepoint on Aplicar Filtros button, `bg-tesote-tan` outer surface, `text-tesote-blue-*` + `text-tesote-red-*` legacy tokens scattered in components not yet swapped to `text-redesign-*`, Geist Mono not loaded (numeric Monto column + totals card amounts both want it).

---

## What changes (per-file change table)

| Production file | Change in v1.1 |
|---|---|
| `app/views/transactions/index.html.erb` | `content_for(:title, "...Transacciones")` → `"...Movimientos"`. `Ui::PageHeaderComponent` title arg → `"Movimientos"`. `Shared::PageHeaderComponent` title arg (legacy path) → `"Movimientos"`. **Insert new `turbo_frame_tag :transactions_totals` between page header and the existing `:transactions_filters` frame**, rendering a new `Transactions::TotalsStripComponent` (or equivalent partial) that consumes `@currency_totals` and renders the 2-card stacked layout per [[prototypes/movimientos-v6]]. `bg-tesote-tan` → Lunour `--bg-main` (white content area). `border-tesote-gray-200` → `border-redesign-border`. `redesign_2026?` ternaries collapse to just the redesign branch once Lunour tokens are universal (or keep dual-rendering if Dan prefers gradual rollout). |
| `app/controllers/transactions_controller.rb` | Single change to `query_filters` method (lines 100–132): replace `else` fallback `filters[:transaction_date_gteq] = 7.days.ago` with `30.days.ago`. Default `date_filter_type` (when none provided) shifts to `30d` (or rename existing `last_week` semantics — Dan's call at implementation time). Pass `@currency_totals` to the new totals frame (already loaded into `@currency_totals` in `index` action; just render the new frame inside the view). Everything else preserved (session persistence, flag gates, default sorts, Ransack handling, etc.). |
| `app/services/transactions/index_data_service.rb` | **No data-shape change.** Currency-totals computation already single-pass and already returns the shape the new totals strip needs (`{currency => {inflow:, outflow:, net_change:}}`). Add a `filters_beyond_fecha_active?` boolean to the service output (computed by inspecting active filter keys; used by totals strip to decide whether to render the `filtrado` tag). |
| `app/views/transactions/_transactions_table.html.erb` | **`tfoot` "Resumen de página" rows (lines ~279–318) get deleted** — totals move to the new strip above the filter bar. Pagination control rows (still inside `tfoot` or moved to a separate `<div>`) preserved. `bg-tesote-tan` / `bg-white` / `shadow-md` / `border-tesote-gray-200` / `text-tesote-blue-*` / `text-tesote-red-*` token swaps. Legacy partial only renders when `redesign_2026?` is false — eventually deletable once redesign is universal. |
| `app/views/transactions/_transactions_table_redesign.html.erb` | **Columns array updated** (lines 38–50): delete `{key: :reference}`, `{key: :note}`, `{key: :status}`, `{key: :actions}`. Replace `{key: :bank}` + `{key: :account}` with single `{key: :bank_account, label: 'Banco/Cuenta'}`. Add `{key: :share, label: 'Compartir'}` at end. Delete the corresponding `with_cell(:reference)`, `with_cell(:note)`, `with_cell(:status)`, `with_cell(:actions)` blocks. Delete `status_pill_variants` and `status_pill_labels` dicts (their definitions become dead code on this surface). Add new `with_cell(:bank_account)` block rendering bank-logo + bank short name + cuenta nickname + monospace last-4. Add `with_cell(:share)` block rendering inline SVG paperplane + `data-action="click->mov-share#open"` (Stimulus controller stub) with appropriate hover state. Modify `with_cell(:description)` to inject a small note SVG icon when `transaction.note&.content.present?` and to apply `title="<full description>"` for the truncation tooltip. Empty-state message: `'No hay transacciones disponibles para mostrar.'` → `'No hay movimientos disponibles para mostrar.'`. `html_options` test_id: keep as `redesign-transactions-table-card` (internal). |
| `app/components/ui/data_table_component.{rb,html.erb}` | **Confirm `table-layout: fixed` + per-column `width` support** at the component level (or add it). The `columns:` array entries may need a new optional `width:` key (`{key: :date, label: 'Fecha', width: '80px'}`). If not present, add. Apply v6 widths: Fecha 80px / Banco/Cuenta 220px / Descripción flex (no width) / Contraparte 220px / Monto 160px / Categoría 150px / Compartir 50px. Row height: 36px tight density. Truncation on Descripción (and other) cells: `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`. |
| `app/components/tesote_transactions/search_filters_component/search_filters_component.html.erb` | **Visual token swap only.** All `bg-gray-50` → Lunour `--bg-soft` / `var(--bg-main)`. All `border-gray-200` / `border-gray-300` → `border-redesign-border`. All `ring-tesote-blue-500` → `ring-redesign-primary`. The `&crarr;` arrow on "Aplicar Filtros" → inline SVG arrow per [[feedback_no_emojis]]. Multi-select dropdown rendering: confirm Lunour family. **No behavior change. No structural change. 4-section collapsible form intact.** |
| `app/components/tesote_transactions/filter_presets_component/filter_presets_component.html.erb` | Visual token swap. `bg-tesote-blue-100 text-tesote-blue-700` (badge) → `bg-redesign-primary-soft text-redesign-primary`. `text-tesote-blue-600` (enabled button + link) → `text-redesign-primary`. `bg-red-600 hover:bg-red-700` (delete button) → `bg-redesign-status-red hover:bg-redesign-status-red-hover` (or whichever Lunour red mapping exists). All other gray-* tokens audited and mapped. **No behavior change.** |
| `app/components/tesote_transactions/cash_flow_section_component.{rb,html.erb}` | `text-tesote-blue-700` button → `text-redesign-primary`. Chart color tokens audited. **No structural change.** |
| `app/components/tesote_transactions/export_modal_component.{rb,html.erb}` | Token swap. No behavior change. |
| **NEW** `app/components/transactions/totals_strip_component.{rb,html.erb}` | New component for the stacked totals strip above the filter bar. Consumes `currency_totals` hash + `filters_beyond_fecha_active?` boolean. Renders 2-card grid (VES + USD; additional currencies append as cards on the right). Card anatomy: currency header (`VES`/`USD`) + optional `filtrado` tag + count subscript (`12 movimientos`); 3 rows (Ingresos green / Egresos neutral / Neto with solid divider above + slightly larger amount); Geist Mono numerics; right-aligned, tabular-nums, nowrap. Renders inside `turbo_frame_tag :transactions_totals` so it recomputes on filter changes. |
| **NEW** `app/components/movimientos/share_modal_component.{rb,html.erb}` | New stub component. Modal opens on paperplane click. Title: `Compartir movimiento`. Body: list of destinations (counterparty on file, teammate inside Tesote, free-form email, WhatsApp) — **all disabled / labelled "Próximamente"** in v1.1. Primary CTA: `Compartir` (no-op + dispatches "Compartido (simulado)" toast). Cancel: `Cancelar`. Modal architecture mirrors `FilterPresetsComponent`'s save-modal (fixed inset-0 z-50, hidden until triggered, Stimulus-controlled). |
| **NEW** `app/javascript/controllers/mov_share_controller.js` | Stimulus controller for paperplane click → opens the share modal. Captures `data-mov-share-transaction-id-value`. Stub `submit` action no-ops + dispatches toast. |
| **NEW** `app/javascript/controllers/clamp_with_title_controller.js` (optional) | Stimulus controller that sets `title="<full text>"` on any element whose text content overflows. Or — simpler — `title="<%= transaction.description %>"` rendered directly in the cell template, no Stimulus needed. **Recommendation: skip the Stimulus controller; render `title` attribute server-side.** |
| `config/locales/es.yml` | `nav.transactions` → `Movimientos`. Any other `transactions` i18n keys on this page audited (empty state copy, etc.) and updated. |
| `config/locales/en.yml` | `nav.transactions` → `Transactions` (kept English-side for now; the page itself is Spanish-only). |
| `config/routes.rb` | **Optional** alias: `get '/connect/movimientos', to: 'transactions#index', as: :movimientos`. Original `transactions_path` preserved. Recommendation: ship the alias for clean URL; old URL keeps working. Sidebar nav points to `movimientos_path` if alias ships, else continues pointing to `transactions_path`. |
| `app/views/layouts/application_v2.html.erb` (or sidebar partial) | Nav item label = `t('nav.transactions')` → resolves to `Movimientos` post-i18n change. Icon `currency-dollar` retained. Active-state matches `/connect/movimientos` if alias is added; if route name stays `transactions_path`, active-state stays at that route. |
| `application_v2.html.erb` (or wherever fonts load) | **Coordinated with Saldos retrofit** — Geist Mono Google Fonts `<link>` once, not twice. Weights `500 / 600 / 700`. If Saldos retrofit ships first and adds Geist Mono, this PRD has zero additional font work. |
| Tailwind config (`config/tailwind.config.js`) | Confirm `text-redesign-primary` resolves to Lunour `#1661E2`; `text-redesign-status-red` to Lunour `#C41E1E`; `text-redesign-status-green` to Lunour `#1A8C5B` / `#0F6E45`; `border-redesign-border` to Lunour `#E8E3DA`; `bg-redesign-surface-soft` to Lunour `#FCFBF7`. If any drift, align as part of this PRD's scope (it's the design-system gate). Add `'mono': ['Geist Mono', 'SF Mono', 'Menlo', 'monospace']` to `fontFamily` if not already (Saldos retrofit may do this — coordinate). |

---

## What does NOT change

Spell these out explicitly so `/tesote-plan` doesn't speculate work:

- **Routes**: `transactions_path` keeps its name. `TransactionsController` keeps its class name. (Optional `movimientos_path` alias is the only routing addition.)
- **Filter mechanism**: `SearchFiltersComponent` 4-section collapsible form preserved verbatim. **Not** migrating to the Mercury-style filter builder. All 17 Ransack dimensions enumerated in Technical Requirements stay exactly as they are. The `Shared::FilterChipsComponent` below the form stays.
- **Filter presets**: `transaction_filter_presets` table + `FilterPresetsComponent` + save / delete modals + personal-vs-shared split + default flag. **Server-backed; better than v6's localStorage saved views.** Preserved verbatim, visual token swap only.
- **Turbo Streams**: `index.turbo_stream.erb`, `:transactions_filters`, `:transactions_chart`, `:transactions_table` — all preserved verbatim. **New** `:transactions_totals` frame is additive.
- **Pagination**: per_page 50/100/200/500 (default 200), POST-based will-paginate renderer, "Mostrar X por página" copy. Unchanged.
- **Bulk-edit**: existing legacy-partial bulk-categorize + bulk-counterparty modals stay on the legacy partial. **Not added to the redesign partial in v1.1.**
- **Cash-flow chart**: `CashFlowSectionComponent` rendered inside `:transactions_chart` turbo frame. Visual token swap only.
- **Export modal**: `ExportModalComponent` reachable from filters area. Visual token swap only.
- **Edit modal**: `_edit_tesote_transaction_modal.html.erb` (reached via the killed Actions column today, gated by `!transaction_show_page`). When the Actions column goes away, **row-click target** = whatever the existing show page handles when `transaction_show_page` is enabled (which is the default). If `transaction_show_page` is off, row click falls back to edit modal (preserved). The row-click affordance moves from the trailing Actions column to the row itself (`data-action="click->row-navigate#go"`).
- **Show page** (`tesote_account/:account_id/tesote_transactions/:id`): unchanged. Reached from row click (when flag on) or from the future slide-over's "Ver página completa →" (v1.2).
- **Per-account drilled view** (`TesoteTransactionsController#index` at `tesote_account/:tesote_account_id/tesote_transactions`): unchanged. That's the target of the Saldos Cuenta row click. **Separate retrofit ticket if needed.**
- **PDF export** (`TransactionsController#show`): unchanged.
- **Data scoping**: `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)`. Unchanged.
- **Default sort**: `s_date asc, created_at asc, id asc` underlying. Visible UI default `Fecha desc` already correct.
- **N+1 prevention**: `Current.cache` request-scoped memoization in `IndexDataService#populate_request_cache`. Unchanged.
- **Inline-edit affordances**: `TransactionCategories::AssignedCategoriesComponent` + `Counterparties::AssignedCounterpartiesComponent` click-to-edit dropdowns. Preserved. Token audit only.
- **Empty-state pattern**: heroicon + Spanish copy. Visual retrofit only, plus copy `transacciones` → `movimientos`.
- **Sortable columns**: Fecha + Monto (the only two with `sort_link` in production). Unchanged.

---

## Architecture / Design

**Visual contract**: [[prototypes/movimientos-v6]] — single self-contained HTML, ~1640 LOC, fully interactive. Stacked totals strip, the (deferred) Mercury-style filter builder, the row table with all 6 surviving columns at locked widths + Banco/Cuenta merge + paperplane Compartir trailing action + em-dash placeholders for null Contraparte/Categoría, the description truncation pattern, the (deferred) slide-over drill-in panel preview. Anchor every visual decision against this file.

**Totals strip — locked layout** (v4 design doc lock #17 → v6 prototype):

```
┌─ VES · 12 movimientos · filtrado ────────────┐  ┌─ USD · 5 movimientos · filtrado ────────────┐
│                                                │  │                                               │
│  Ingresos     +Bs. 3.700.000.000,00            │  │  Ingresos     +$ 13.700,00                    │
│  Egresos      -Bs. 375.035,16                  │  │  Egresos      -$ 6.700,00                     │
│  ─────────                                      │  │  ─────────                                     │
│  Neto         +Bs. 3.324.964.964,84            │  │  Neto         +$ 7.000,00                      │
└────────────────────────────────────────────────┘  └───────────────────────────────────────────────┘
   ↑ 90px label column · right-aligned amount       ↑ Geist Mono 18px Ingresos/Egresos · 20px Neto
   ↑ Stacked, never wraps regardless of digit count ↑ Tabular nums · whitespace nowrap
```

- 2-card grid (`grid-template-columns: repeat(2, 1fr)`); EUR / additional currencies append as new cards on the right.
- Solid divider above Neto row; dashed divider between Ingresos/Egresos.
- Ingresos green (`var(--green-text) #0F6E45`); Egresos neutral (`var(--text) #12110F`); Neto green if ≥ 0 else neutral.
- `filtrado` tag (blue pill, `--primary-light` bg, `--primary` text) appears beside the currency code only when filters beyond the default Fecha are active.
- **No FX conversion** — each currency totals independently (matches Saldos decision).

**Column anatomy — locked** (post 2026-05-19 Mercury-density iteration):

| Column | Width | Header | Cell content |
|---|---|---|---|
| Fecha | 80px | `Fecha` | `DD/MM` for current year, `DD/MM/YYYY` for prior year. Tabular nums. Sortable. |
| Banco/Cuenta | 220px | `Banco/Cuenta` | **Text only**: `<bank short> · <cuenta nickname> ··<last-4>`. Last-4 monospace `text-redesign-text-3`. **No bank-logo glyph** — visual noise without disambiguation payoff. |
| Descripción | flex (~456px @ 1440px content) | `Descripción` | Bank-raw + ref tail, truncated `nowrap + ellipsis + title=""` tooltip. Small note SVG icon inside the cell when `transaction.note&.content.present?`. |
| Contraparte | 220px | `Contraparte` | **Text only** + always-visible ▼ caret. Resolved counterparty name, em-dash `—` if null. Inline-edit on click. **No avatar chip**. Caret at 65% opacity rest, 100% on cell hover. Tooltip on dash: "click para asignar". |
| Monto | 160px | `Monto` (right-aligned) | Currency prefix + signed amount + currency badge. **Cents-deemphasis pattern**: integer at 13.5px / 600-weight, decimals at 11px / 60% opacity — Mercury's subordinated-decimal treatment (`+$214.06` reads big-integer-dot-tiny-cents). Green for credits, neutral for debits, red only for reversed/failed. Geist Mono. Sortable. |
| Categoría | 150px | `Categoría` | `Ui::PillComponent` chip with Lunour pill family + always-visible ▼ caret. Em-dash `—` if null. Inline-edit on click. |
| Compartir | 90px | `Compartir` | Inline SVG paperplane. Always-visible; low-key at rest (gray stroke); primary on hover (blue fill + `--primary-light` bg). Click opens stub share modal. Column widened from 50px to 90px so the header label reads in full at 11px uppercase tracking. |

**Density**: **40px row height** (was 36px in v6; bumped after Mercury-density iteration). 14px horizontal cell padding (was 12px). One-line rows. No wrap. No two-line clamp. **Content max-width 1440px** (was 1320px). `table-layout: fixed` is non-negotiable.

**Estado pill family** (still consumed by other surfaces; the Estado column is killed on this surface only):

| State (still in `Ui::PillComponent`) | Lunour pill | Label |
|---|---|---|
| `completed` | `:mint #D6E8D5` | `Conciliado` |
| `pending` | `:amber #F7EDD0` | `Pendiente` |
| `failed` | `:salmon #F8D8C0` | `Fallido` |
| `draft` | `:gray #ECE7DD` | `Borrador` |
| `created` / `ready_to_be_processed` / `created_in_external_service` | `:lavender #E4ECF7` | `Nuevo` / `Por procesar` / `Externo` |

---

## Surfaces affected

- `/transactions` (route name preserved; visible title + sidebar label rename to Movimientos) — the page itself
- Optional new alias `/connect/movimientos` → same controller action
- Sidebar nav active item — i18n `nav.transactions` value flips to `Movimientos`
- App shell font stack — Geist Mono added (coordinated with Saldos retrofit)
- Tailwind theme — `text-redesign-*` family audited against Lunour
- `Ui::DataTableComponent` — `columns:` array gains optional `width:` key + `table-layout: fixed` enforcement (if not already present)

**Not touched**: any other Connect route (Saldos has its own retrofit PRD, KYC onboarding deferred), `TesoteTransactionsController` (per-account drilled view, separate ticket if needed), authentication, organization switching, permission stack, the cash-flow chart's data path, the export modal's data path, bulk-edit infrastructure.

---

## Data model implications

**Zero schema changes.** Movimientos retrofit is read-only over existing `TesoteTransaction`, `TesoteAccount`, `Counterparty`, `TransactionCategory`, `TransactionFilterPreset`, `Note`, `ExternalServiceTransaction`. All loads exist in production today.

Per [[project_tesote_vs_odoo_split]]: Movimientos is purely Tesote-side observation (system-of-action surface, not Odoo regulatory record). No Odoo touchpoints. Cross-ref [[reference_finance_db_schema]] for canonical schema path.

**Workspace-tenant safety**: `permitted_tesote_accounts` uses `authorized_scope(workspace.active_tesote_accounts, with: ::TesoteAccountPolicy)` — already enforces `workspace_id` boundary. Unchanged.

The new `Transactions::TotalsStripComponent` consumes data already loaded by `IndexDataService`. The new `Movimientos::ShareModalComponent` stub captures intent only; no persistence in v1.1. The new `mov-share` Stimulus controller has no server interaction.

---

## AI / automation implications

None in v1.1. Movimientos is a scan + reconcile + categorize surface; no AI features in scope.

Future AI affordances naturally live in:
- **The slide-over drill-in** (v1.2): "describe this movimiento", "find similar", "draft a Compartir message".
- **The Compartir modal** (v1.2): auto-format row details for the chosen channel, suggest a recipient based on counterparty on file.
- **Categoría / Contraparte inline-edit** (later): suggest categorization based on description + amount + similar past rows (already partially shipped via `transaction_rules` — not in scope of this PRD).

Flagged for AI roadmap; not this PRD.

---

## Open decisions (resolved)

| # | Decision | Resolution |
|---|---|---|
| 1 | Filter system: v3 4-section collapsible vs Mercury-style builder | **Keep production's 4-section collapsible.** Migration to builder is a separate v2 workstream as the canonical filter primitive. |
| 2 | Saved views: localStorage (v4 brain spec) vs server-backed (production) | **Server-backed (production wins).** `transaction_filter_presets` table + personal/shared/default already shipped. localStorage saved-views from the v4 brain spec are abandoned. |
| 3 | Estado pill column | **Kill from row.** Re-evaluate when rail data has real pending states. Pill family stays defined on `Ui::PillComponent` for other surfaces. |
| 4 | Referencia column | **Kill from row.** Move to drill-in (v1.2). |
| 5 | Nota column | **Kill from row.** Replace with note-icon-in-Descripción when present. |
| 6 | Actions column | **Kill from row.** Replace with paperplane Compartir column. Row click handles drill-in target (show page when `transaction_show_page` flag on, edit modal when off). |
| 7 | Banco + Cuenta columns | **Merge into single Banco/Cuenta cell** with bank logo + name + cuenta nickname + monospace last-4. |
| 8 | Paperplane (Compartir) | **Stub in v1.1**: icon + modal + "Compartido (simulado)" toast. Destinations + channels + actual send deferred to v1.2. |
| 9 | Side-panel drill-in (Surface A) | **Defer to v1.2.** Prototype is the contract; build deferred. Row click in v1.1 continues to route to existing show page or edit modal per `transaction_show_page` flag. |
| 10 | Full-page drill-in (Surface B) | **Already exists in production** as `tesote_account_tesote_transaction_path`. Not redesigned in this pass. |
| 11 | Totals strip placement | **Above filter bar, stacked cards.** Lifted out of `tfoot`. New `turbo_frame_tag :transactions_totals`. |
| 12 | Default Fecha filter | `last_week` (7d) → **`30d` (Últimos 30 días)**. |
| 13 | Density | **40px rows + 14px horizontal cell padding + 1440px content max-width.** Browse/scan archetype. Tested 36px (v6) on 2026-05-19 with 200-row dataset — felt cramped; bumped to 40px and widened content. `table-layout: fixed` non-negotiable. |
| 14 | Inline-edit on Contraparte + Categoría + always-visible ▼ caret | **Preserved + caret added.** Production components already support inline-edit; add always-visible chevron-down (12×12 SVG, 65% opacity rest, 100% on hover) so the dropdown affordance is discoverable without hover-reveal. |
| 25 | Bank-logo glyph in Banco/Cuenta cell | **Killed.** Tested with + without on 2026-05-19; logo added visual noise without disambiguation value since bank short-name already labels the row. Text-only cell. |
| 26 | Counterparty avatar chip in Contraparte cell | **Killed.** Same reasoning as bank-logo; counterparty-as-identity surfaces elsewhere (drill-in panel in v1.2, counterparties page). Text-only cell. |
| 27 | Monto cents-deemphasis | **Adopted.** Integer 13.5px / 600-weight + decimals 11px / 60% opacity (Mercury's subordinated-cents pattern). Big amounts read at-a-glance; precision stays available. |
| 28 | Totals strip card scale | **Compact.** Card padding `12px 16px` (was `18px 22px`), Ingresos/Egresos amount 13px (was 18px), Neto amount 14px (was 20px), border-radius 8px (was 12px). Same 2-card stacked-rows shape; smaller. Roughly halves vertical space. |
| 29 | Compartir column width | **90px** (was 50px). Header `Compartir` now reads in full at 11px uppercase tracking. |
| 30 | Content max-width | **1440px** (was 1320px). Outer content padding 36px (was 32px). Horizontal slack for Banco/Cuenta + Contraparte + Descripción column widths. |
| 15 | Description truncation | **`nowrap + ellipsis + title="" tooltip`.** Row height never breaks. |
| 16 | Em-dash placeholder for null Contraparte + Categoría | **`—` not "Sin contraparte" / "Sin categoría".** Tooltip clarifies "click para asignar". |
| 17 | Route + controller class rename | **No.** Visible title only. `transactions_path` + `TransactionsController` keep names. Optional `movimientos_path` alias for clean URL. |
| 18 | Feature flag | **Keep existing `redesign_2026` flipper.** No new flag. |
| 19 | Font loading | **Geist Mono via Google Fonts `<link>`** (or self-host — Dan's call at implementation time). Coordinated with Saldos retrofit so the font loads once. |
| 20 | Sidebar nav label | i18n `nav.transactions` value flips to **`Movimientos`** (es.yml). Path stays `transactions_path` unless alias ships. |
| 21 | `&crarr;` emoji on Aplicar Filtros button | **Replace with inline SVG arrow** per [[feedback_no_emojis]]. |
| 22 | Currency totals — FX conversion across currencies | **None.** Each currency totals independently (matches Saldos decision). |
| 23 | `Ui::DataTableComponent` per-column widths + `table-layout: fixed` | **Required.** If not currently supported by the component, this PRD's scope adds it. |
| 24 | Bulk-edit on redesign partial | **Not in v1.1.** Stays on legacy partial only. |

---

## Path forward

### V1.1 wedge — this PRD

See Intake. Surgical naming + 4 column kills + 1 column merge + 1 new column + 1 totals-strip move + 1 default change + 1 density flip + token migration + paperplane stub. No filter-builder, no slide-over drill-in, no data-model changes.

### What sequences after v1.1

```
v1.1 (this PRD, ~1 week)   — naming + columns + Banco/Cuenta merge + paperplane stub + totals strip lift +
                              default 30d + Geist Mono + 36px density + token migration
v1.2 (~next sprint)        — Movimientos::DrillInPanelComponent slide-over (mirrors Cobros invoice panel) +
                              paperplane Compartir destinations + channels + actual send wiring +
                              keyboard nav (j/k) between movimientos in the panel
v1.3 (post-Connect-sweep)  — Bulk-select on redesign partial + bulk-categorize + bulk-counterparty modals
                              ported to redesign tokens + multi-select toolbar
v2   (later)               — Mercury-style filter builder as canonical filter primitive
                              (consumed by Movimientos + Saldos + Pagos + Cobros + Contrapartes)
v2.1 (later)               — AI affordances in drill-in panel + Compartir auto-formatting
v3   (later)               — Reconciliación / certification surface where row-level
                              certification signals (currently loaded but not rendered) finally live
```

### Discipline calls

- **Don't ship the Mercury filter builder in v1.1.** It's v2 — the canonical filter primitive workstream. Resist scope creep.
- **Don't ship the slide-over in v1.1.** It's v1.2. Resist scope creep.
- **Don't extract the filter primitive doc in this PRD.** Three consumers (Saldos retrofit, Movimientos retrofit, future v2 builder) is the right threshold; doing extraction inside this PRD speculates the API.
- **Don't rename routes / controllers.** Internal infra rename has zero user-visible value. Visible title is the user-facing fix.
- **Don't migrate filter presets to localStorage.** Production's server-backed pattern is strictly better than v6 brain's localStorage saved views; the brain spec is updated by this PRD's resolution.

---

## References

### Internal source docs (this PRD draws from)

- [[prototypes/movimientos-v6]] — **canonical visual + behavior contract**
- [[design]] — Movimientos full page design (v6-anchored, every lock #1–#26)
- [[../saldos/saldos-prd]] — sibling retrofit PRD (mirror structure)
- [[../redesigns-week-2026-05-18]] — workstream umbrella (this PRD is one of two children)
- [[../../design/archetypes]] — table-padding tokens (Browse density)
- [[../../design/design]] — Lunour brand tokens
- [[../../_prd-template]] — schema this PRD follows

### External

- **Production codebase**: `~/Programming/tesote/treasury/app/controllers/transactions_controller.rb` + `app/services/transactions/index_data_service.rb` + `app/views/transactions/{index.html.erb,_transactions_table.html.erb,_transactions_table_redesign.html.erb,index.turbo_stream.erb}` + `app/components/tesote_transactions/{search_filters_component,filter_presets_component,cash_flow_section_component,export_modal_component}` + `app/components/ui/data_table_component` — every per-file change in this PRD anchors here.
- **Treasury skill**: `~/Programming/tesote/treasury/.claude/skills/redesign-2026-design-system/SKILL.md` — `/tesote-plan` will pull this in automatically; it's the design-system gate.
- Linear ticket: [TBD]
- Treasury plan dir: [TBD]

### Memory references (load-bearing context)

- [[project_filter_system_primitive]] — context for the decision to keep production's pattern (filter-builder migration is v2 workstream)
- [[project_tesote_command_center]] — Movimientos sits inside Connect, the inbound observation half
- [[project_tesote_vs_odoo_split]] — Movimientos is Tesote-side observation; no Odoo touchpoints
- [[feedback_no_emojis]] — production already uses heroicons; kill the `&crarr;` arrow; new paperplane is inline SVG
- [[reference_finance_db_schema]] — canonical schema for the read-only data Movimientos consumes
- [[feedback_tesote_plan_workflow]] — this PRD → Linear PRO ticket → `/tesote-plan` in treasury

---

## Before I run `/tesote-plan` — checklist

All 24 decisions above are **resolved**. Four implementation-time confirmations remain — flag for `/tesote-plan` to resolve with Dan during planning:

1. **`Ui::DataTableComponent` per-column widths** — does the component accept a `width:` key in the `columns:` array entries? If not, add support (small additive change). Same applies to `table-layout: fixed` at the table level — if not already enforced, add.
2. **Tailwind token audit** — confirm `text-redesign-primary` / `text-redesign-status-red` / `text-redesign-status-green` / `border-redesign-border` / `bg-redesign-surface-soft` resolve to Lunour values in `config/tailwind.config.js`. If not, align as part of this PRD's scope.
3. **Geist Mono loading strategy** — Google Fonts `<link>` (fastest to ship) vs. self-host via `app/assets/fonts/`. Dan's call at implementation time; coordinated with Saldos retrofit so the font loads once.
4. **`movimientos_path` alias** — ship the clean-URL alias in `routes.rb`, or skip? Recommendation: ship it; old URL keeps working; sidebar nav points to the alias for cleaner browser history.

After Luis confirms this PRD reads correctly, the next concrete moves are:

```
# 1. File the Linear PRO ticket — paste this PRD's Tesote-Plan Intake block verbatim as the description
#    Title: "Movimientos — v1.1 retrofit on production transactions page"
#    Then update movimientos-prd.md frontmatter: linear: <ticket URL>, status stays ready-for-tesote-plan

# 2. cd to treasury and run /tesote-plan:
cd ~/Programming/tesote/treasury
/tesote-plan <Linear-ticket-URL>

# 3. Plan lands at treasury/.debugging/plans/movimientos-v1-1-retrofit/
#    Hand to Dan, or run /implement directly
```

---

*Drafted 2026-05-19 after reading production `transactions` controller + service + 2 view partials + 5 components + `Ui::DataTableComponent` and locking visual + behavior decisions via [[prototypes/movimientos-v6]]. The prototype is the contract; this PRD is the bridge to treasury. Sibling to [[../saldos/saldos-prd]] — same retrofit discipline, same /tesote-plan pattern, ships together as the Connect redesign sweep ([[../redesigns-week-2026-05-18]]).*
