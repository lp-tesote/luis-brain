---
title: Treasury Production Recon — 8 Redesigned Pages
tags: [design, product, web-app, treasury, recon]
updated: 2026-06-11
status: reference
audience: Luis, Dan, Claude (future sessions)
---

# Treasury production recon — structure extracts for the v2/v3 redesign

> Extracted 2026-06-10 from the treasury Rails app (`~/Programming/tesote/treasury`) by 4 read-only agents. This is the **ground truth** the unified-app v2/v3 prototypes were designed against, and the **Phase-2 input** for `/tesote-plan`. If production changes, re-recon before trusting this.
>
> Production nav source: `app/views/layouts/application_v2.html.erb` — eng already ships `redesign_2026` infra (`Ui::SideNavComponent`, `Ui::TopNavComponent`, `_index_redesign` view variants, `docs/redesign_2026/HANDOFF.md`).

## Production nav (sectioned, with gates)

| Section | Item | Route | Gate |
|---|---|---|---|
| — | Dashboard | `root_path` | always |
| — | Tesote AI | `ai_path` | Flipper `tesote_ai_demo` |
| Tesote Connect | Cuentas | `v2_tesote_accounts_path` | always |
| Tesote Connect | Transacciones | `transactions_path` | always |
| Tesote Connect | Conexiones bancarias | `external_service_bank_connections_path` | always |
| Tesote Connect | Entidades legales | `tesote_legal_entities_path` | always |
| Tesote Negocios | Pagos | `payments_path` | Flipper `payments_v1` |
| Tesote Negocios | Contrapartes | `counterparties_path` | `payments_v1` OR `contract_management` |
| Tesote Negocios | Contratos | `contracts_path` | Flipper `contract_management` |
| Tesote Automatizaciones | Reportes | `reporting_reports_path` | always |
| Tesote Automatizaciones | Workflows | `workspace_workflows_path` | Flipper `workflows_enabled` |
| Tesote Automatizaciones | Sincronizaciones programadas | `scheduled_syncs_path` | Flipper `scheduled_syncs_ui` |
| Espacio de Trabajo | Mi equipo | `workspace_users_path` | `can_manage_members?` |
| Espacio de Trabajo | Grupos | `groups_path` | `can_manage_members?` && `use_group_permissions?` |
| Espacio de Trabajo | Configuración | `settings_path` | always |

---

## 1 · Conexiones bancarias

- **Controller:** `ExternalServiceBankConnectionsController` — index (has `_index_redesign` variant), show, update, `link_token` (JSON), `archived_connections` (lazy AJAX partial).
- **Index:** title "Conexiones bancarias" + "N conexiones" count. CTA = `BankConnections::NewBankConnectionButtonComponent` (disabled at plan limit via `enforce_active_bank_connection_limit?`).
- **Status enum:** `draft / active / pending / failing` → ES: Borrador / Activa / Pendiente / **Requiere atención**.
- **Filters (collapsible panel + chips via `Shared::FilterChipsComponent`):** Banco (multi), Estado (multi, excl. draft), Compañía (multi, conditional).
- **Table:** Banco + entidad legal (sub-text) · Estatus (`Shared::StatusBadgeComponent` + inactive-scheduler warning icon) · Cuentas (count) · Creado (`%d-%m-%Y`). Whole row clickable → show.
- **Archived:** collapsible bottom section, lazy-loaded, restore action.
- **Show page sections:** Conexión · Nombre del banco · **Apodo** (editable; "Ej: Conexión vía José") · Estatus · **Cuentas Tesote asociadas** (table w/ active checkboxes + "Actualizar estados activos" bulk; inactive = hidden + unsynced) · **Reconectar** (Plaid relink, orange pulse) · **Cambiar credenciales** (per connector type: API / Plaid / webscraper) · Eliminar respuestas de seguridad (webscraper) · Agregar pregunta de seguridad (webscraper) · **Sincronización programada** (embedded scheduler table: horario humano + cron, estado, última sync; amber warning if inactive schedulers) · **Archivar** (red, confirm) · Coordenadas de seguridad (webscraper image upload) · 2FA setup component.
- **Permissions:** visibility scoped by `TesoteAccountPolicy`; management actions need `can_manage_bank_connections?`.

## 2 · Sincronizaciones programadas

- **Controller:** `ScheduledSyncsController` — index/new/create/show/update/pause/resume/submit_for_approval. Gates: Flipper `scheduled_syncs_ui` + `workspace.scheduled_syncs_enabled?` (+ `can_create_scheduled_sync?` free-tier limit → info banner "Sincronización Programada Gratuita Incluida").
- **Scheduler status enum:** `draft / pending_approval / active / paused / disabled / failed`.
- **Filters:** Banco, Estado, Tipo (`full` Completa / `transactions` Solo transacciones / `balances` Solo saldos).
- **Table:** Banco (+n cuentas) · Estado · Tipo ("Saldo y transacciones" / "Saldo sin transacciones" + green "Más rápido" pill / "Solo transacciones") · Frecuencia (`user_friendly_schedule`; draft = "Pendiente por revisión") · Última / Próxima sync · pause/play actions (`can_be_paused?`/`can_be_resumed?`).
- **Pause modal:** required `reason` textarea → Pausar / Cancelar. Pause metadata (reason, timestamp, by-user) shown on show page.
- **Show:** header CTA varies (Pausar / Reanudar / "Reparar Conexión Requerida" disabled). Alerts: connection-failing (red), paused (yellow w/ reason). 2×2 grid: Información de conexión · Información de programación · Acciones de sincronización · Historial (última/próxima, exitosas/fallidas counts). Footer link → `bank_sync_sessions_path` filtered.
- **New form:** Conexión bancaria (single-select w/ readiness icons) · Zona horaria (default América/Santo_Domingo) · **Rango 2 h** (start time + auto-computed end, readonly) · Días de la semana (checkboxes, default Lun–Vie) · Acciones de sync (checkboxes) · Notas administrativas (internal) · info box "el equipo de soporte optimizará el horario exacto… después de aprobar".
- **Empty state:** clock icon · "No hay sincronizaciones programadas" · "Configura sincronizaciones automáticas para mantener tus datos actualizados".

## 3 · Compañías (entidades legales)

- **Controller:** `TesoteLegalEntitiesController` + nested `LegalEntitySetupFormsController`; `ExternalServiceLegalEntitiesController` is admin-ish read-only (not a design surface).
- **Index:** title "Compañías" + count. CTAs: **Unidades de Negocio** (`business_units_path`) · **Organizar cuentas** (`tesote_accounts_path`) · **Nueva entidad**.
- **Table:** Nombre (+tax_id sub) · Fecha de creación · Unidad de negocio (or "Sin unidad") · Cuentas (or "Sin cuentas"). Row → show.
- **Fields:** `legal_name`, `nickname`, `tax_id` (encrypted; RIF "J317507339" / "V12345678"), `business_unit_id`, `discarded_at` (soft delete), `entity_type` enum (partnership / LLP / LLC / c_corporation / person).
- **Archived:** collapsible + restore (`undiscard: true`).
- **Show:** DL (nombre, RIF, unidad, cuentas count, creado, actualizado) + "Opciones avanzadas" collapsible w/ red warning — **archivable only with zero accounts**.
- **Create:** just legal_name + business_unit. **Edit:** + tax_id.
- **Setup wizard (US entities):** sidebar steps Company Info (entity_type, EIN, incorporation date, address…) → Owner Info (person, TIN/SSN/passport, identity file drag-drop) → All Owners.
- **Permissions:** primary user sees all; secondary only entities linked to permissioned accounts.

## 4 · Contrapartes

- **Controller:** `CounterpartiesController` — index/new/create/edit/update/show/destroy/restore/**wipe**/search/inline_create.
- **Index:** count subtitle. CTAs: **Nueva Contraparte** + **Sugerencias** (✨ + pending-count badge; Flipper `suggested_counterparties`).
- **Filters:** nombre (text) · estado (Activas/Archivadas/Todas) · correo (text) · ID externo (text). Chips row.
- **Table (sortable):** Nombre (+ "Archivada" red pill if discarded, "Auto" blue pill if `source != 'manual'`) · Correo · ID Externo · Fecha de creación. Discarded rows = opacity-60.
- **Source enum:** `manual / auto_seniat / auto_rule / erp_import`.
- **Show:** DL (nombre, correo, ID externo, transacciones count, creado, actualizado) + **Métodos de pago** (Flipper `payments_v1`: cards w/ bank + currency badge + masked account + label + tipo + "Débitos permitidos" + "Verificado") + **Contratos** (Flipper `contract_management`: cards w/ título, ref, status, total pagado) + Avanzado: **Limpiar** (remove from ALL transactions) / **Restaurar** / **Archivar**.
- **Form:** Nombre (req; "ej. Proveedor ABC, Cliente XYZ") · Correo (opt) · Identificador Externo (opt; "ej. CP-001, RIF, NIT").
- **Sugerencias sub-page:** suggested_name, normalized_identifier, identifier_type, transaction_count, accounts_seen, first/last_seen; status `pending/approved/skipped`; **bulk_approve / bulk_skip**.

## 5 · Historial de reportes

- **Controller:** `Reporting::ReportsController#index`; generation via STI sub-controllers (POST): `Reporting::TesoteTransactions::Report`, `Reporting::TesoteAccounts::Report`, `Reporting::ReconciliationDailySummary::Report` (Flipper `reconciliation_health_dashboard`).
- **Status enum:** `pending / processing / completed / failed` → pendiente / procesando / completado / fallido.
- **Table (10/page):** Nombre (+ rango dd/mm/yyyy) · Fecha de creación · Estado · **Progreso** (bar + % + progress/total_records; ✓ Completo; ✗ Error) · Acciones (download via `rails_blob_path` / cancel / failure_reason).
- **Generation = export modal in source pages** (`TesoteTransactions::ExportModalComponent` from Movimientos "Exportar"): resumen de filtros aplicados + count + **Nombre del reporte** (autogenerated default, max 200) + nota "se generará en formato Excel (.xlsx) y estará disponible en la sección de reportes". Progress via Turbo Streams + email on completion.
- **Empty:** "No hay reportes disponibles."

## 5b · Transacción — detail view (recon'd 2026-06-11; the original sweep missed it)

- **Full page** (not modal): `/tesote_accounts/{account_id}/tesote_transactions/{id}`, `data-turbo:false`; back-link preserves list state (page, search, range).
- **Header:** descripción as title · subtitle = fecha ("DD de MONTH, YYYY") + cuenta · **monto grande color-coded** (green credit / red debit).
- **Sidebar "Detalles":** Referencia (external service id) · Banco · Cuenta (+entidad legal) · Moneda · Fecha de transacción. Then editable sections (pencil → modal, Turbo Stream): **Categorías · Contraparte · Contratos · Documentos Adjuntos** (flag `transaction_attachments`).
- **Main column:** Insights (async) · **Notas** (textarea inline + checkbox "incluir en confirmaciones por correo") · **Comentarios** (internal collab).
- **"Acciones" card:** **Descargar PDF** (+ checkbox incluir nota interna; direct `/transactions/{id}.pdf`) · **"Enviar por Email"** (envelope icon) → modal: Contrapartes multi-select (solo con correo) · CC a mi correo · CC adicionales (máx 10) · Asunto personalizado (255) · Nota para el correo (2000) · incluir nota interna · incluir adjuntos. Queues `SendReceiptEmailsJob`.

## 6b · Usuario — profile page (recon'd 2026-06-11)

- **Minimal**: nombre + correo + "Usuario Principal" badge (if primary) + Editar (`manage_members`) + delete section w/ confirm. No transactions/history.

## 6 · Mi equipo

- **Controller:** `WorkspaceUsersController` — index/new/create/destroy/autocomplete.
- **Index:** "Miembros activos del equipo". CTA Nuevo usuario (`can_manage_members?`).
- **Table:** Usuario (nombre completo) · Correo · Estado: **Pendiente** (yellow; Devise `invited_to_sign_up?`) + **"Copiar enlace"** button (copies `accept_user_invitation_url` w/ raw token; "¡Copiado!" 2 s feedback) / **Activo** (green).
- **Invite form:** Correo (req) · Nombre (req) · Apellido (req) · **Grupos (opcional)** — radio per group; "sin grupo no podrá ver ninguna cuenta"; if none exist → link to create. Sends email from `ENV['EMAIL_ADDRESS']`.

## 7 · Permisos (grupos)

- **Controller:** `GroupsController` — index/new/create/edit/update; gate `require_group_permissions!`.
- **Index table:** Nombre · Miembros (avatar stack: first 3 + "+N"; count) · Creado. Row → edit.
- **Editor sections:** Nombre · **Usuarios** (checkbox grid w/ avatar+nombre+email) · **Permisos del espacio** (if `workspace.advanced_permissions?`; only grantable-by-current-user shown — anti-escalation) · **Cuentas y permisos** (per-account cards; per-account restrictions `view_debit / view_credit / view_balance` if Flipper `transactions_restrictions`; quick-selects: Marcar todos / Débitos / Créditos / Saldos) · footer: Cancelar / **Archivar** (confirm) / Guardar.
- **Workspace permission catalog:** `manage_workspace_settings` (Administrar configuración) · `manage_members` · `manage_bank_connections` · `manage_all_accounts` (visibilidad de cuentas) · `manage_security` · + payments-module: `view_payments` · `send_and_request_payments` · `approve_payments` · `manage_payment_methods`.
- **Model:** Group ↔ workspace_users via group_memberships; `Permission` polymorphic (owner: Group|ApiKey; resource: Workspace|TesoteAccount; `restrictions` JSONB).

## 8 · Configuración

- **Hub model:** single page (`SettingsController#index`), all sections stacked, links out to sub-routes. No sub-nav.
- **Sections (+ gates):**
  1. **Información del usuario** — nombre/apellido/correo/mis grupos/nombre del equipo (edit → `edit_workspace_path`, `can_manage_settings?`).
  2. **Seguridad** — 2FA personal (Habilitado/Deshabilitado badge → two_factor_settings) · **Política 2FA del espacio** (Requerido/Opcional; adoption stats w/ % progress bar green≥80/yellow≥50/red<50; deadline `require_2fa_on`; exemption workers-only; edit → workspace_configuration).
  3. **2FA para conexiones bancarias** — SMS forwarder devices (Flipper `sms_forwarder`); device count badge; QR pairing.
  4. **Descarga de reportes** — formato de fecha · separador de columnas · marca decimal · tipo de archivo (CSV/XLS) · separar crédito/débito (per-user `ReportDownloadSettings`).
  5. **Espacio** — workspace config (`number_of_classification_levels`, `show_full_account_number_on_reports`, separators, `display_balances_in_api`) · **Tasas de cambio** (Flipper `workspace_exchange_rates`): tabs **Actuales/Historial**; columns par · tasa workspace · tasa sistema · diferencia; add/edit/delete modals; "tus tasas tienen prioridad sobre las del sistema"; filters par + rango (7/30/90 d), 20/page.
  6. **Estado de sincronizaciones** — `bank_sync_sessions_path` (read-only).
  7. **Escaneo de integraciones** (Flipper `integration_scanning`).
  8. **API** (Flipper `generating_api_keys`) — keys list: nickname · creada · token enmascarado · scopes · delete; create modal (`nickname`, `bearer_kind`, all_accounts vs `permitted_account_ids[]`, account/workspace restrictions); empty state "Comienza con la API de Tesote" + 3-step guide; sidebar API/webhook status.
  9. **Webhooks** (Flipper `webhook_events`) — table: estado (toggle) · URL · eventos · última entrega · acciones; form: url (HTTPS req) + description + subscribed_events[] + active; empty = onboarding 3 pasos.
  10. **Verificación de datos** (Flipper `reconciliation_health_dashboard`).
  11. **Transacciones** — Workflows o Reglas (Flipper `workflows_transition`) · Categorías · Contrapartes · **Unidades de negocio** (table: nombre · compañías count · edit) · Importar transacciones.
  12. **Exportación automática** (Flipper `workspace_data_export`) — endpoint_url + bearer_token + hora; manual sync + history.
  13. **Administrar equipos** — `new_workspace_path` (`can_manage_settings?`).

---

*Banked 2026-06-11 so design threads don't depend on session context. Companion to [[web-app-design-system]] (the rules) and `unified-app-v2/v3.html` (the prototypes).*
