---
title: Web App Redesign 2026 — Implementation Handoff (v4 frozen)
tags: [product, prd, design, web-app, redesign-2026]
updated: 2026-06-11
status: filed-as-ticket
audience: Luis (primary), Dan, Majo
author: Luis Pulgar (synthesis with Claude)
linear: https://linear.app/tesote/issue/PRO-182/web-app-redesign-2026-implement-frozen-v4-design-parity-reskin-all
tesote_plan_dir: [path once /tesote-plan run]
---

# Web App Redesign 2026 — Implementation Handoff

> **One-line purpose.** Ship the frozen v4 redesign — every existing workspace page re-skinned to the locked Tesote design system at **strict UX parity** with today's app.

---

## Tesote-Plan Intake

> **Treasury's `/tesote-plan` ingests this block.**

### Actor & Problem

As **any Tesote workspace user (Mariel as reference)**, I need to **use the existing app with a single coherent visual system** because **today's UI mixes legacy Tailwind/Mercury-era styling with partial `redesign_2026` components, and eng has no complete, signed-off visual contract — each `_index_redesign` variant re-derives design decisions per page**.

### The Test

This solves **inconsistent UI + contract-less redesign work** for **all workspace users and the eng team** in **Workspace/Connect**. Without it: the `redesign_2026` effort keeps shipping page-by-page interpretations, drift multiplies, and the design debt compounds with every new surface.

### V0 — Simplest thing that works

- [ ] Every page below renders per `unified-app-v4.html` (open it; `#hash` deep-links per page) with **zero behavior change** (parity-first — same routes, same capabilities, same flows): Inicio shell* · Saldos (incl. "Por conexiones bancarias" tab) · Movimientos (full filter panel; no standalone search) · Conexiones bancarias (+ detalle, + "Conectar un banco": país → banco → modal credenciales) · Compañías (+ detalle, + unidades de negocio) · Contrapartes (+ detalle, + sugerencias, + nueva) · Historial de reportes · Sincronizaciones programadas (+ detalle, + nueva, + pausar modal) · Mi equipo (+ perfil, + invitar) · Permisos (+ editor de grupo) · Configuración (hub + espacio · webhooks · estado de sync · reglas · categorías · importar · tasas de cambio · claves API)
- [ ] Transaction detail matches v4 `#movimiento-detalle` (Notas + checkbox email, Comentarios, Detalles sidebar, Descargar PDF, "Enviar por Email" modal)
- [ ] Record detail = **full page with back-link** everywhere (no slide-overs)
- [ ] All tokens/rules from `web-app-design-system.md` §§ hold: §1b color roles · §12 pill grammar + semantic mapping · §13 monograms · density/heights per [[archetypes]] (uniform row heights — non-negotiable)
- [ ] Topbar ships **without** entity switcher and without "Mover dinero" (parked decisions)

\* Inicio = shell/chrome parity only; the new dashboard content is a **separate PRD** (`product/dashboard/dashboard-prd.md`).

### Out of Scope (explicit "Not Doing")

- **Inicio dashboard content** (position chart, Δ-decomposition, AI panel) — own PRD/ticket; net-new backend primitives
- **Pagos / Cobros / Contrapartes-payments scope** — PRO-112 track
- **Tesote AI surface** — own track
- Entity filter in topbar; Pagar/Cobrar buttons on Inicio (parked, post-transition)
- Exportación automática + Verificación de datos sub-pages (hub rows link out to current pages)
- Any new feature, field, or flow not in production today (parity-first)

### Technical Requirements

- [ ] Behind existing `redesign_2026` flag / `_index_redesign` variant mechanism; maps onto existing `Ui::*` components (`docs/redesign_2026/HANDOFF.md`)
- [ ] **No schema changes** — pure view/component/CSS layer; controllers and permissions untouched
- [ ] Spanish copy VE `tú` (sweep whole screens); no emojis — inline SVG only
- [ ] Tokens from Lunour ramps only (`design.md`); status pastels never on categories; uniform row heights per density bucket
- [ ] Existing gates respected (Flipper flags, `can_manage_*` — see recon doc per page)

### Rollout Plan

1. **Internal** — Tesote Finance (Mariel) dogfoods on real workspace data, page-by-page flag
2. **Beta** — 3–5 named workspaces; verify no workflow regressions (parity makes this cheap)
3. **GA** — `redesign_2026` flipped for all; legacy views deleted

---

## Context (why now)

Eng already started `redesign_2026` (layout + `Ui::*` nav shipped). The design side is now **complete and frozen** (2026-06-11, Luis sign-off after two review rounds with 33 pinned comments resolved). This ticket turns the frozen contract into an implementation plan.

## The contract (read in this order)

1. **`luis-brain/product/design/unified-app-v4.html`** — the frozen reference app: 33 pages, every flow walkable, `#hash` deep-links. What it shows is the spec.
2. **`luis-brain/product/design/web-app-design-system.md`** — the rules, cite by §. Wins over the prototype on conflicts.
3. **`luis-brain/product/design/treasury-recon-2026-06.md`** — per-page production ground truth (routes, enums, fields, ES labels, gates) the design was built against.
4. `design.md` (tokens) · `archetypes.md` (density) — supporting.

## Open questions for the plan

- Page sequencing (suggestion: Conexiones → Compañías → Contrapartes → Reportes → Sincronizaciones → Equipo/Permisos → Configuración; Saldos/Movimientos retrofits last since they're closest already)
- Whether the Saldos legacy filter migrates to the filter-builder primitive in this pass or stays parity (design-system §10/§18 — flag for Dan's call)
