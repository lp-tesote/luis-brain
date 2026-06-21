# product/design/ — Tesote web-app design system

Home for the **app-wide** design system and the cross-surface review/unification work.
Read this first when resuming design work.

## Files

| File | What it is |
|---|---|
| **`web-app-design-system.md`** | **Source of truth** — page-composition rules for every screen (shell, color roles, typography, cards, multi-currency, charts, filters, pills, bank logos, AI panel, slide-over, hub, flow overlay). Cite by §; this file wins over prototypes. |
| **`unified-app-v4.html`** | **Canonical reference app — post-design-pass.** 33 pages: every record opens a **full detail page** (conexión · compañía · contraparte · sincronización · usuario · movimiento), país-first bank connect + credentials modal, 6 Configuración sub-pages (espacio · webhooks · estado de sync · reglas · categorías · importar), 9 modals, **zero dead CTAs**. Luis's 33 review comments applied. Next sign-off round happens here. |
| `treasury-recon-2026-06.md` | **Production ground truth** — per-page structure extracts from the treasury app (routes, columns, enums, ES labels, forms, gates). Phase-2 input for `/tesote-plan`; re-recon if production moves. |
| `unified-app-v3.html` · `v2` · `v1` | Prior builds (v3 holds Luis's review pins in localStorage). Superseded by v4; kept per versioning convention. |
| `surfaces-review.html` | Earlier review canvas — the three *original* surface prototypes side-by-side in iframes (pre-unification). Superseded by `unified-app-v1` for the unified feel; still handy to see the "before". |
| `design.md` | Lunour **brand tokens** (colors/type/radii hexes). Also feeds `/pdf`, `/proposal`, marketing. |
| `archetypes.md` | Six screen archetypes + density spec (row heights, font scale, table padding). |
| `workspace-design-decisions.md` | PRO-112 migration punch list (historical audit). |

## ★ FROZEN 2026-06-11 — v4 approved by Luis

`unified-app-v4.html` is the **signed-off design contract** for the web-app redesign. No further design edits in place — any post-freeze change is a new vN with a reason. Next: PRO-* ticket → `/tesote-plan` in treasury (+ `redesign-2026-design-system`). Handoff packet = v4 + `web-app-design-system.md` + `treasury-recon-2026-06.md` + `redesign-handoff-prd.md`.

## State (2026-06-09, end of session)

Built `unified-app-v1.html` to make **app-wide** design calls by feeling the real flow. Decisions made this session are **locked into `web-app-design-system.md`**.

### Decided & locked
- **Color system** — black = brand + **every primary button**; **blue = "act or find"** (links, focus, operable controls, modifications-you-made like applied filter chips, key data); **navigation active state = NEUTRAL gray, never blue**; semantic colors = small-dose status only. **Two hard rules: no large semantic fills (banners neutral + icon), no colored edge-strips on containers.** (§1b)
- **Shell** — cream sidebar + white content everywhere (Saldos no longer inverts).
- **Typography** — all tabular numbers = Geist Mono (Saldos included); one size scale.
- **Bank monograms** — always **2-letter** (ME, BN, MC, BS, BM, BB, AC, BE, BV, BT, MB), uniform width. (§13)
- **Pills** — one shape, **4px**, for status *and* category; editability shown by the always-visible caret, not roundness. **(Gut-checked & locked 2026-06-09: shape is constant; the grammar is status = colored pastel + dot, no caret / category = neutral fill, no dot, + caret.)**
- **Category color** — categories never borrow status pastels (no `Software`→orange). Category chips = neutral `pill-draft` fill **+ a colored *category* dot** from a dedicated category-tag palette (own Lunour-ramp hues, stable per category), so categories are color-coded but stay quieter than filled status pills. Palette in [[design]]; rule in §12. Fixed in `unified-app-v1.html`.
- **Removed top summary strips** — Movimientos money-in/out-by-currency + Saldos "Saldos por moneda" cards (lead with data, not a summary slab).
- **Inicio page-head** — workspace logo + name only (no date/tagline/En-vivo/Personalizar) — frozen in `dashboard-v5.html`.

### 2026-06-10 — One-shot redesign of the remaining 8 pages → `unified-app-v2.html`

Scope set by Luis: Conexiones bancarias · Compañías · Contrapartes · Historial de reportes · Sincronizaciones programadas · Mi equipo · Permisos · Configuración. Structure grounded in **treasury production ERB recon** (4 Explore agents: columns, status enums, filters, forms, Spanish labels, permission gates — captured in the session; production nav lives in `treasury/app/views/layouts/application_v2.html.erb`).

- **v2 sidebar IA:** Connect (Saldos · Movimientos · Conexiones · Compañías) / Negocios (Pagos · Cobros stubs · Contrapartes) / Automatizaciones (Reportes · Sincronizaciones) / Espacio de Trabajo (Mi equipo · Permisos · Configuración). Forward-looking names; routes map 1:1 to production.
- **New patterns minted** (locked into design-system §15–§17): slide-over detail panel, settings hub archetype, in-cell progress, avatar stack, copy-with-feedback, danger zone, switch, collapsible archived, warning sub-row. Status semantic mapping locked into §12.
- **Pill grammar update (same session):** categories got their **own dot palette** (design.md → Category-tag palette); shape stays 4px-for-everything, caret = editability.
- **Awaiting:** Luis's browser sign-off + production screenshots to reconcile. Then **Phase 2**: treasury mapping → PRO-* ticket → `/tesote-plan` + `redesign-2026-design-system`.

### 2026-06-11 — v3: the fully-walkable app (final-design-pass artifact)

Luis's call: **finish everything at the HTML level first** — colors, buttons, UX flows all testable by clicking — *then* the technical transition. So v3's bar = zero dead ends.

- **Added:** Nueva conexión wizard (4-paso flow overlay — first archetype-3 impl) · export modal (from Movimientos "Exportar" AND Reportes "Nuevo reporte") · Sugerencias de contrapartes (approve/skip + bulk) · Nueva contraparte + Nueva compañía forms · Unidades de negocio · Tasas de cambio (tabs Actuales/Historial + modal) · Claves API (+ modal) · empty states (proto-toggle on Reportes/Sincronizaciones) · dead-end audit (Saldos banner→Conexiones, hub rows→sub-pages, etc.).
- **Docs:** flow-overlay + flow-modal rules folded into design-system **§17b**; treasury recon banked to `treasury-recon-2026-06.md` (no session-context dependency anymore).
- **Process locked:** v3 gets Luis's final design pass → **freeze** → Phase 2 (PRO-* + `/tesote-plan` + `redesign-2026-design-system`), with the frozen prototype + recon doc as the contract.

### Review workflow (the design pass)

v3 has a built-in **comment layer** (Figma-style pins, prototype-only chrome — amber/dashed): bottom-right **"Comentar"** toggles pin mode (app interactions pause, like Figma) → click anywhere (pages, slide-overs, modals, wizard) → numbered pin + note. **"Lista"** shows all pins and jumps to each. **"Copiar como Markdown"** exports the punch list — paste it into a Claude session and the pins become the change requests. Pins persist in the browser (localStorage), survive reloads, and live outside the design system (never ship). `Esc` exits pin mode.

### 2026-06-11 — v4: Luis's design pass applied (33 pinned comments)

**Governing principle locked (now §0 of the design system): parity-first.** This iteration matches the live app's UX — same pages, flows, capabilities — redesigned skin only, to keep the eng transition low-stress. Structural changes = parked decisions.

Applied in v4: **record details = full pages** (slide-overs retired — §15 reversed, archetypes §2 flipped) · país-first bank connect (flags VE/US/PA/RD) + **credentials modal** (wizard retired) · Movimientos filter panel = full production dimension set + standalone search removed (search lives in filters) · paperplane "enviar confirmación" row action restored · movimiento detail page · Saldos "Por conexiones bancarias" tab built · Conexiones/Contrapartes lose Filtros Guardados + Exportar · Contrapartes uniform 44px rows · Configuración + "Separador de columnas" + 6 sub-pages (espacio · webhooks · estado de sync · reglas · categorías · importar) · topbar slimmed (entity switcher + "Mover dinero" removed).

**2026-06-11 PM — second fix round (Luis's verbal pass):**
- **Root-caused the row-height bug** (visually, via the new screenshot loop): the v3 empty-*state* class `.empty` collided with v1's `.cell-edit.empty` modifier — every "— agregar/— asignar" cell inherited 54px padding + column layout. Renamed to `.empty-state`. v3 ships the bug (frozen, superseded).
- **Movimiento detail rebuilt to production parity** (was invented — recon hadn't covered the tx show view; now it has): descripción as title, monto hero, Detalles sidebar (Referencia/Banco/Cuenta/Moneda/Fecha), Categorías/Contraparte/Contratos/Adjuntos editable, Notas + "incluir en confirmaciones" + Comentarios, Acciones = Descargar PDF + **Enviar por Email modal** (contrapartes multi, CC, asunto, nota). Row paperplane → envelope, opens the same modal. Added to `treasury-recon` knowledge.
- **Saldos "Por conexiones bancarias" = the saldos-v4 design ported** (10-col operations table: Usuario · Entidades · Cuentas · Estado · Último sync · Programación · Modo · 2FA · re-sync), replacing my improvised grouped list. Coexists with the standalone Conexiones page — same name, different job, OK for now (Luis).
- **Usuario detail simplified** toward production's minimal profile.
- **Verification upgraded:** v4 has `#hash` deep links per page; Claude now screenshots pages via headless Chrome and *looks* at them before claiming done.

**Parked decisions (deliberately NOT in this iteration):**
- Entity filter in topbar — removed for now; revisit after transition (Luis, pin #3)
- Pagar / Cobrar buttons on Inicio — decide post-transition (pin #4)
- Exportación automática + Verificación de datos sub-pages — hub rows present, pages not built
- Slide-over panel — deprecated for records; possible future quick-glance uses
- Pins #1, #2, #15, #17, #23 — no text; presumed test clicks. Re-pin in v4 if they were real (export now includes coordinates).

### Open / next thread
1. ~~**Pill shape gut-check**~~ — DONE 2026-06-09. ~~**v3 design pass**~~ — DONE 2026-06-11 → v4.
2. **Saldos filter → filter-builder** — the one structural drift left (§10/§18). NOTE: under parity-first, check what the live Saldos actually ships before migrating — parity may *keep* the current tab/group-by this iteration.
3. **Luis's second pass on v4** — verify the 33 fixes landed right; pin anything new (comment layer carried over, exports now include coordinates). ← **next up**
4. **Freeze + Phase 2** — file PRO-*, run `/tesote-plan` in treasury with `redesign-2026-design-system`; frozen v4 + recon doc = the contract.
3. **AI sparkle mark** — currently blue (accent). Decide if it goes black for a purer black/white identity (offered, not decided).
4. **Saldos big Bs figure** — now Geist Mono per unification; confirm mono reads better than the old Inter Tight display there.
5. Keep tightening the unified feel, then any newly-confirmed rules → fold into `web-app-design-system.md`.

### Related (not in this folder)
- `../dashboard/dashboard-prd.md` — full Inicio PRD (8 boxes specced, decisions resolved; next = file PRO-* + `/tesote-plan`).
- `../dashboard/prototypes/README.md` — Inicio prototype lineage (v5 frozen).
