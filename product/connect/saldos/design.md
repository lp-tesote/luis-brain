---
title: Saldos — Page Design
tags: [design, product, connect, saldos]
updated: 2026-05-14
status: promoted
audience: Luis, Dan, Vero (when ready)
---

> **Promoted to KB** 2026-05-14 → `knowledge-base/product/bank-connectivity/saldos/design.md`. Edit the KB copy from this point forward.

# Saldos — Page Design

> The operational trust dashboard for Tesote. Where Tesote's value prop earns or loses trust every single day.
>
> Sits under **Connect** in the sidebar. Replaces the current "Cuentas" / "Panel de Sincronización" UI.
>
> Builds on [[../../design/archetypes]] (list/table archetype, review-and-decide density), [[../../design/design]] (Lunour brand tokens), and the canonical visual reference `product/business/pagos/prototypes/pro-112/workspace-shell284-v2-lunour.html`.

---

## What this page is

Tesote sits on top of many third-party banks. Banks are flaky. Syncs fail. Connections expire. Multi-currency adds another layer. **This page is where users go to:**

1. **"How much cash do I have, right now?"** — treasury read (probably 60% of daily time on page)
2. **"Is this number current / can I trust it?"** — sync recency check
3. **"What's broken if it's not?"** — connection diagnostics
4. **"Force a refresh"** — manual sync trigger

If users don't trust the saldos here, they can't trust anything downstream — cashflow forecast, Pagos decisions, Cobros reconciliation. So the design stakes are unusually high. **It's not a list page; it's the foundation everything else stands on.**

## Naming

**Locked: "Saldos"** (per [[index]] and confirmed 2026-05-14).

- Page title + sidebar nav label = **Saldos** (the outcome — cash position)
- Objects on the page = **Cuentas** (each row is a Cuenta)
- Secondary view = **Conexiones bancarias** (the plumbing underneath)
- Sync action = **Sincronizar saldos** (the verb is sync, the noun is saldos)

Why not the current "Panel de Sincronización": sells the mechanism, not the outcome. Sync is internal plumbing; users come here for the number, not for the panel.

---

## Critical clarification: saldos vs transacciones data trust

> **Saldos are 99% reliable as pulled from banks.** The "data certification" concept — Tesote guaranteeing data is fully verified and complete — **applies to transactions, not saldos.**

This is load-bearing. The current UI shows a "Validación" column on the Saldos page with "Verificado (real-time)" / "Sin verificación" badges per account. **That column is misplaced** — it belongs on the Transacciones page, where transaction completeness is a real concern. Surfacing certification on Saldos creates a trust signal for a problem that doesn't exist (saldos accuracy) and dilutes the signal on the page where it matters (transacciones).

**On Saldos, the trust question is simpler:**

- Is the connection still working?
- When was this number last fetched?
- That's it.

This collapses the per-row status from three signals (connection-health + sync-recency + certification) to **two** (connection-health + sync-recency) — and those two are tightly coupled, so they compose into a single composite badge cleanly. See below.

**Where certification belongs:** the Transacciones page (a separate Connect surface). When we design that page, "Datos certificados" becomes a per-account or per-period badge there — and the value prop lands in the right context.

---

## The Estado badge (per row) — 3 states only

One column. One badge. Three traffic-light states. The recency timeline lives in a **separate** "Último sync" column so it doesn't get conflated with state.

| Badge | When | Meaning to user |
|---|---|---|
| 🟢 **Conexión OK** | Connection healthy (regardless of last sync time) | Plumbing works. Read the "Último sync" column to judge recency yourself. |
| 🔵 **Sincronizando** | Sync in flight right now | Number you see is stale by minutes; new one coming |
| 🟡 **Necesita atención** | Needs re-auth, sync failed, 2FA required, stale beyond threshold | Click in to see what's wrong and fix it |

**Manual accounts** (user-entered, no API connection): no Estado badge — render as `—`. They're outside the connection-state model.

**Why 3 instead of 5:**
- "Atrasado" doesn't need its own badge — if the connection is fine but the last sync was 3 days ago, the badge stays green and the "Último sync" column tells you "hace 3 días." User self-judges whether to refresh.
- "Rota" and "Atrasado past threshold" both demand the same action (user looks into it). Collapsing into "Necesita atención" reduces cognitive load. Drill-in shows the specifics.

**Visual treatment:** dot + short label inside the pill (`🟢 Conexión OK`). Reuse the locked pill family from `archetypes.md`:
- Green = `pill-paid` background `#D6E8D5` + dot `#1A8C5B`
- Blue = `pill-new` background `#E4ECF7` + dot `#1C77F4`
- Yellow = `pill-pending` background `#F7EDD0` + dot `#CC9500`

**The "Último sync" column stays as data, not state.** Reads as "hace 8h", "hace 1 semana", "hace 2 minutos." It's information the user needs but doesn't need to be encoded as a colored signal.

**On Conexiones view**, the badge keeps the same 3-state model — same green/blue/yellow, same meanings — just scoped to the connection (since that's the unit). The label can be tuned for context (e.g., "Activa" instead of "Conexión OK" since it's already at connection level).

---

## Density

**Saldos page = "review and decide" + "browse" mixed.** Users do both jobs here. Default to **44px standard rows** (manage-a-set density from [[../../design/archetypes]]). Rationale:

- 10×30+ connections-to-accounts → 300+ rows. 52px review-density would force too much scroll.
- The page is multi-job (treasury read + diagnostic + action) → standard density matches the breadth.
- Grouping (sin agrupar / por banco / por divisa / por entidad) does the work that roomy rows would otherwise do — it lets users zoom into a subset before density matters.

When designing the Transacciones page later (browse-heavy), drop to **36px dense**.

---

## States to design

1. **Empty** — first-time user, 0 banks connected
2. **Loaded — Cuentas view** (primary)
3. **Loaded — Conexiones view** (secondary, via toggle)
4. **Syncing** — page-level + row-level indicators while a sync is in flight
5. **Connection broken** — top-of-page banner + affected rows marked
6. **Detail drill-in** — slide-over panel for one Cuenta (and a separate one for one Conexión)

Wireframes + anatomy for each below.

---

## 1 · Empty state

First-time user. No banks connected. **This is the unlock for the entire product** — every Tesote feature downstream depends on at least one connected bank. Don't waste it on a generic icon + button.

```
┌──────────┬──────────────────────────────────────────────────────────────┐
│          │  Saldos                                                       │
│ Sidebar  │  Conecta tus bancos para empezar                              │
│          │                                                               │
│          │                                                               │
│          │              ┌─ Hero block (centered, max 480px) ─┐           │
│          │              │                                     │           │
│          │              │       ┌──────────────────┐         │           │
│          │              │       │   illustration    │         │           │
│          │              │       │   stack of banks  │         │           │
│          │              │       └──────────────────┘         │           │
│          │              │                                     │           │
│          │              │   Tu centro de saldos               │           │
│          │              │                                     │           │
│          │              │   Conecta cuentas de Mercantil,    │           │
│          │              │   BNC, Banesco, BBVA y +10 bancos  │           │
│          │              │   más. Tesote sincroniza tu efectivo│           │
│          │              │   en una sola vista.                │           │
│          │              │                                     │           │
│          │              │   [Conectar primer banco →]         │           │
│          │              │   o crear cuenta manual             │           │
│          │              │                                     │           │
│          │              └─────────────────────────────────────┘           │
│          │                                                               │
│          │   ─────────────────────────────────────────────────           │
│          │   Bancos disponibles para conectar:                           │
│          │   [Mercantil] [BNC] [Banesco] [BBVA] [Mi Banco] [Activo] +9   │
│          │                                                               │
└──────────┴──────────────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Hero block:** centered, max-w 480px. Illustration (stack-of-banks visual, not an empty-folder cliché). Title (22px Inter Tight). Pitch copy (13px body, 2 lines max). Two CTAs: primary "Conectar primer banco →" + ghost link "crear cuenta manual" for cash drawers / petty cash use cases.
- **Bank availability strip below:** small logos of the banks Tesote supports, with a "+9 más" or similar overflow. Builds trust — "yes, my bank is here."
- **No top KPI strip** (nothing to summarize). No filter row (nothing to filter). Page is dominated by the hero.

**Edge case — partial empty:** user has 1+ manual accounts but no API-connected banks. Show the manual accounts in a tiny "Cuentas manuales" section above the hero, with a banner gently pushing toward a real connection: "Conecta tu banco para sincronizar automáticamente."

---

## 2 · Loaded — Cuentas view (primary)

The default state. What users see 80% of the time.

```
┌──────────┬─────────────────────────────────────────────────────────────────┐
│          │  Saldos                                  [Sincronizar todo (10) ]│
│ Sidebar  │  10 conexiones · 32 cuentas · Última actualización general: 8h  │
│          │                                                                  │
│          │  ┌─ SALDOS POR MONEDA ─────────────────────────────────────────┐│
│          │  │ VES                  │ USD                  │ EUR           ││
│          │  │ Bs. 23.85M  (7 ctas) │ $411,253.69 (15)     │ €N (1)        ││
│          │  │ ≈ $46,692 al BCV     │                      │               ││
│          │  │ Tasa BCV: 510.79 ↗   │                      │               ││
│          │  └─────────────────────────────────────────────────────────────┘│
│          │                                                                  │
│          │  ── 🟡 BBVA: Conexión requiere re-autenticación (afecta 2 ctas) ── │
│          │                                          [Re-conectar ahora →]   │
│          │                                                                  │
│          │  [ Cuentas ] [ Conexiones bancarias ]    [Agrupar: ▾ Banco]      │
│          │                                                                  │
│          │  [Compañías ▾] [Bancos ▾] [Tipo ▾] [Divisa ▾]   [🔍 buscar  ]   │
│          │                                                                  │
│          │  ┌─ Mercantil ────────────────────────────────────────────── ──┐│
│          │  │ COMPAÑÍA │ CUENTA       │ SALDO ▼     │ DIV │ ESTADO       │ ÚLT SYNC ││
│          │  ├─────────┼──────────────┼─────────────┼─────┼──────────────┼──────────┤│
│          │  │ TST CYC │ ••6733       │ Bs 475,056  │ VES │ 🟢 Conexión OK│ hace 8h  ││
│          │  │ TST CYC │ ••3755       │ $95.62      │ USD │ 🟢 Conexión OK│ hace 8h  ││
│          │  └─────────────────────────────────────────────────────────────┘│
│          │                                                                  │
│          │  ┌─ Banco Activo ─ 🟡 Conexión necesita atención ────────── ──┐│
│          │  │ TST CYC │ ••6280       │ Bs 31,030   │ VES │ 🟡 Atención  │ hace 1 sem││
│          │  │ TST CYC │ ••3543       │ $0.00       │ USD │ 🟡 Atención  │ hace 1 sem││
│          │  └─────────────────────────────────────────────────────────────┘│
│          │                                                                  │
│          │  ┌─ Bancamiga ───────────────────────────────────────────── ──┐│
│          │  │  ...                                                        ││
│          │  └─────────────────────────────────────────────────────────────┘│
│          │                                                                  │
└──────────┴─────────────────────────────────────────────────────────────────┘
```

**Anatomy:**

- **Page header:** title + meta line (`10 conexiones · 32 cuentas · Última actualización general: hace Xh`) + primary CTA on the right: **"Sincronizar todo (N)"** — the N makes the side-effect explicit (the original ambiguity-killer).
- **Saldos por moneda strip:** unified 3-card container (per [[../../design/archetypes]] KPI strip pattern). Each currency: total + account count + BCV conversion if applicable. **Lead with this — biggest thing on the page after the title.** This is the answer to "how much cash do I have?"
- **Connection-broken banner** (only if applicable): full-width red banner directly above the toggle. Reads "BBVA: Conexión requiere re-autenticación (afecta 2 cuentas)" + CTA "Re-conectar ahora →". This appears at page-level, not per row, because connection brokenness affects many rows at once. Loud, hard to miss.
- **View toggle** + **grouping dropdown:** segmented `[Cuentas] [Conexiones bancarias]` (Cuentas as primary, weight-wise) + on the right, `Agrupar: ▾ Banco` (collapses the 4-button row from current design into 1 dropdown with 4 options: ninguno / banco / compañía / divisa).
- **Filter row:** dropdown filters + search. Same as current pattern in workspace-shell284-v2-lunour.html.
- **Grouped table:** rows clustered under group headers. Group header is sticky-on-scroll, shows the group label ("Mercantil") + optional summary ("3 cuentas · Bs 750K") + group-level state if any rows are broken/syncing. Rows inside are 44px standard.
- **Columns (7):** Compañía · Cuenta (••last4) · Saldo · Divisa · **Estado** (composite badge) · Último sync · ⋯ (drill-in trigger). No per-row sync button — sync is per-connection (see "Sync interactions" below).
- **No per-row sync icon** (current UI lies — API can't sync one account; clicking it triggers the whole connection). Replace with `⋯` overflow menu offering "Ver detalles", "Ver conexión", "Sincronizar conexión (3 ctas)".

**Multi-currency handling:** Saldos card strip is the cross-currency summary. The table itself shows native currency per row. No global "convert all to USD" toggle in v1 — the strip's BCV conversion handles the most common case.

**Hover row:** light bg + cursor pointer. Click row → slide-over detail (see state 6).

---

## 3 · Loaded — Conexiones view (secondary)

Same page chrome (KPI strip, toggle, filters). Different table.

```
│          │  [ Cuentas ] [ Conexiones bancarias ]    [Sincronizar todas →] │
│          │                                                                  │
│          │  [Compañías ▾] [Estado ▾] [Modo ▾]               [🔍 buscar  ]  │
│          │                                                                  │
│          │  CONEXIÓN          │ USUARIO   │ ENTIDADES │ CTAS │ ESTADO     │ ÚLT SYNC│ MODO │ ⋯ │
│          │  ────────────────────────────────────────────────────────────── │
│          │  Mercantil          │ A...e25  │ Tesote T. │ 3    │ 🟢 Activa   │ hace 8h │ API   │ ⋯ │
│          │  BBVA               │ A...e7   │ TST CYC   │ 2    │ 🟡 Atención │ hace 10h│ API   │ ⋯ │
│          │  Bancamiga          │ A...e25  │ TST CYC   │ 3    │ 🟢 Activa   │ hace 8h │ API   │ ⋯ │
│          │  Caja Chica Tesote  │ —        │ Tesote T. │ 1    │ —           │ —       │ Manual│ ⋯ │
│          │  ...                                                              │
```

**Anatomy:**

- **Columns (~8 — tighter than today's 10):** Conexión (with sub-text for nickname) · Usuario (masked) · Entidades · Cuentas (count) · Estado · Último sync · Modo (API / Manual) · ⋯
- **Dropped from current design** (moved into drill-in detail panel): Programación (auto-sync schedule), 2FA. Reasoning: these are configuration, not status. Don't compete for column real estate.
- **Estado here is connection-level, same 3-state model:**
  - 🟢 Activa — connection healthy, syncing on schedule
  - 🔵 Sincronizando — sync in flight
  - 🟡 Atención — needs re-auth, 2FA, or has failed (specifics shown in the row's drill-in)
  - For manual connections (cash drawers), Estado renders as `—`
- **Page-level CTA changes** to "Sincronizar todas →" — bulk sync at connection level.
- **Click row → slide-over detail** for that connection (see state 6).
- **No grouping** by default in Conexiones view — only 10–15 rows, doesn't need it.

---

## 4 · Syncing state

While a sync is in flight (one connection or many), the page shows it loud.

```
│          │  Saldos                          [ ⟳ Sincronizando 4 conexiones ]│
│          │  10 conexiones · 32 cuentas · ⟳ Sincronización en curso          │
```

**Anatomy:**

- **Top-right CTA flips** from "Sincronizar todo" → spinner + count: "⟳ Sincronizando 4 conexiones". Clickable to expand details ("BBVA · Mercantil · BNC · Bancamiga").
- **Meta line under title** changes: "Última actualización general" → "Sincronización en curso" with a spinner icon.
- **Row-level:** affected rows show 🟡 Sincronizando badge in Estado column.
- **Saldos por moneda cards:** the value visible is the pre-sync value, with a small spinner icon next to the currency code indicating "this number is updating." On completion, value animates to new total (subtle slide / fade — not flashy).
- **Toast on completion** (bottom-right, 4s auto-dismiss): "4 conexiones sincronizadas · 12 cuentas actualizadas". Click toast → highlights the rows that changed.

**Why so much surface for sync:** because right now this page is where users go specifically when they're anxious about whether the data is current. Strong sync-state visibility = strong trust signal.

---

## 5 · Connection broken state

When one or more connections are in a non-healthy state (re-auth needed, failed, etc.), surface it loudly at page-level — not just as a row-level dot.

```
│          │  Saldos                                  [Sincronizar todo (8)] │
│          │  10 conexiones · 32 cuentas · 2 con problemas                   │
│          │                                                                  │
│          │  ╔══════════════════════════════════════════════════════════╗  │
│          │  ║ 🟡  2 conexiones necesitan atención                       ║  │
│          │  ║                                                            ║  │
│          │  ║ • BBVA — Necesita re-autenticación (afecta 2 cuentas)     ║  │
│          │  ║ • Banco Activo — Sync falló hace 1 semana (4 ctas)        ║  │
│          │  ║                                                            ║  │
│          │  ║                                  [Ver conexiones →]       ║  │
│          │  ╚══════════════════════════════════════════════════════════╝  │
│          │                                                                  │
│          │  [Saldos por moneda — same as state 2]                          │
│          │  ...
```

**Anatomy:**

- **Banner placement:** between meta line and Saldos por moneda strip. Demands attention without burying the cash position.
- **One banner aggregates all broken connections** — list inside (max 3 shown, "+N más" overflow if many).
- **Each item:** connection name + brief reason + impact ("afecta N cuentas").
- **CTA on banner:** "Ver conexiones →" jumps to Conexiones view filtered to broken-only.
- **Saldos still show.** Don't hide the cash position because of broken connections — the user still needs the number; just flag clearly that part of it is stale.
- **Affected rows in Cuentas view** show 🔴 Rota badge — same composite Estado column doing its job.

---

## 6 · Detail drill-in (slide-over panel)

Click any row → slide-over from right (460px wide, per [[../../design/archetypes]] detail archetype). Different content per view:

### For a Cuenta:

```
                                                      ┌──────────────────┐
                                                      │ ✕                │
                                                      │                  │
                                                      │  Mercantil ••6733│
                                                      │  TST CYC · VES   │
                                                      │                  │
                                                      │  Saldo            │
                                                      │  Bs. 475,056.87   │
                                                      │  ≈ $929.84 al BCV │
                                                      │                  │
                                                      │  ─ Estado         │
                                                      │  🟢 Conexión OK  │
                                                      │  Último sync:    │
                                                      │  hace 8h          │
                                                      │  Cert. transac.: │
                                                      │   ─→ ver Transacc│
                                                      │                  │
                                                      │  ─ Conexión      │
                                                      │  Vinculada a:    │
                                                      │  Mercantil API   │
                                                      │  3 cuentas total │
                                                      │  [Ver conexión →]│
                                                      │                  │
                                                      │  ─ Historial sync│
                                                      │  hoy 08:14 ✓     │
                                                      │  ayer 21:30 ✓    │
                                                      │  ayer 14:02 ✓    │
                                                      │  ...             │
                                                      │                  │
                                                      │  ─ Notas         │
                                                      │  (inline edit)   │
                                                      │                  │
                                                      ├──────────────────┤
                                                      │ [Sincronizar     │
                                                      │  conexión (3)]   │
                                                      └──────────────────┘
```

**Anatomy:**

- **Header:** banco + ••last4, sub-line: compañía · divisa
- **Saldo block:** big number + BCV conversion if applicable
- **Estado de sync section:** the composite Estado badge expanded — current state + last sync time. **Mentions transaction certification with a "Ver Transacciones" link** (we don't show cert here; we point to where it lives).
- **Conexión block:** which Conexión owns this Cuenta. "Vinculada a: Mercantil API · 3 cuentas total." Link to that Conexión's detail.
- **Historial de sync:** scrollable list of recent syncs, success/failure marks.
- **Notas:** free-text inline-edit field. Operator-personal — "this account is used for X."
- **Footer CTA:** "Sincronizar conexión (3 cuentas)" — explicit about what it triggers.

### For a Conexión:

Same panel structure but content tuned for connection: credentials masked, 2FA state, scheduled-sync config (Programación + Modo, moved from main table), connection-level sync history, affected accounts list with mini-rows, re-auth CTA if broken, disconnect CTA in a danger zone at the bottom.

---

## Sync interactions

Spelling out because this is where the page can go wrong.

| Trigger | What happens | UI feedback |
|---|---|---|
| Top-page "Sincronizar todo (10)" | Triggers sync on every active connection | CTA flips to spinner + count. All connection rows in Conexiones go 🔵 Sincronizando. Cuentas rows show 🔵 too. Toast on completion. |
| Conexión row sync button | Triggers sync on that one connection (its N accounts) | That row + its child accounts go 🔵. Toast on completion. |
| Cuenta row "Sincronizar conexión (3)" (in ⋯ menu or drill-in footer) | Same as above — triggers parent connection's full sync. **Label makes it explicit.** | Same |
| Re-auth on a broken connection | Opens auth flow (form/flow-step archetype, separate page) | On return, banner clears, row state updates to Sincronizando, then Al día |

**Confirmation modal:** only if triggering "Sincronizar todo" with ≥5 connections, show a quick "Sincronizar 10 conexiones (32 cuentas)? Esto puede tomar varios minutos." with confirm + cancel. Below 5, no confirm — direct trigger.

---

## Why grouping is the volume answer

10 connections × 30+ accounts = 300+ rows. That's the volume Luis flagged. Options considered:

- **Pagination** (load 50 at a time) — bad: users want totals at top, which require all rows loaded anyway.
- **Virtualization** (render only visible rows) — fine for performance but doesn't help cognition. 300 rows feel like 300 rows.
- **Grouping** ✅ — collapse to ~10 group headers (one per banco) with expand-to-see-accounts. Default-expanded for ≤3 accounts; default-collapsed for >3. User sees "10 bancos at a glance" and zooms into the one that matters.

The current design already has this (`Por banco`, `Por entidad`, etc.) — just promote it to be a dropdown rather than 4 toggle buttons, and default to **Banco** grouping (the most common mental model).

---

## What I deliberately did NOT include in v1

- **Cross-currency global total** ("Total in USD across everything"). Multi-currency reality is too varied; BCV per-card is enough.
- **Charts / sparklines per account.** Pretty but not load-bearing for "how much do I have right now." Save for the dashboard, not Saldos.
- **Per-account history beyond drill-in.** The drill-in has it; main table doesn't.
- **Manual account creation flow.** It's a CTA in the empty state and in the ⋯ menu; the flow itself is separate (form/flow archetype).
- **Account aliases / nicknames** as a first-class column. Lives in drill-in.

---

## Open questions

1. **Banner placement when multiple problems exist.** Above Saldos por moneda (current proposal) vs below it. Above means the user sees the problem before the number; below means they see cash first, problems second. I lean above.
2. **Default grouping for Cuentas view.** Por banco (my recommendation) vs Sin agrupar (today's default vibe). For 300 rows, grouping should be default.
3. **What state goes in the Saldos por moneda card during a partial-failure?** If BBVA's connection broke, the USD total includes their 2 cached accounts which may be wrong. Show the total normally and let the row-level 🔴 dots tell the story? Or asterisk the total with a footnote? I lean asterisk + tooltip: "Incluye Bs. 31K de conexiones con problemas — ver banner."
4. **Re-auth UX surface.** Inline modal in Saldos page vs full-page form-flow? Banks vary — some need OTP input, some need redirect. Probably modal for OTP, page for redirect. Defer to Connect engineering for the auth-flow design.

---

## Next steps

1. Sign-off on this page design (or push back on specific states).
2. Apply the composite Estado badge to the v2 prototype `workspace-shell284-v2-lunour.html` (or build a dedicated Saldos prototype HTML). I'd recommend a dedicated HTML — Saldos has enough surface that hosting it inside the existing pagos-prototype gets crowded.
3. Iterate on the prototype until each state passes the taste test.
4. Extract reusable primitives (KPI strip, composite-Estado badge, grouped table, connection-broken banner, slide-over detail) for `primitives.md`.

---

## Decisions log

- **2026-05-14** — Estado collapsed from 5 states → **3 states** (Luis). Green = connection good · Blue = syncing · Yellow = needs attention. Sync recency stays in a separate "Último sync" column as data, not encoded into state. Manual accounts render Estado as `—` (outside the 3-state model). Rationale: 5 states forced the user to interpret shades; recency is already in its own column.
- **2026-05-14** — Doc initialized. Naming locked (Saldos), certification scope clarified (transacciones only, not saldos), volume context captured (10 conexiones × 30+ cuentas), API constraint locked (per-connection sync only).

---

*Drafted 2026-05-14 from Luis's domain context (10×30+ scale, multi-currency default, per-connection sync API only, certification is for transactions not saldos). Update as decisions land.*
