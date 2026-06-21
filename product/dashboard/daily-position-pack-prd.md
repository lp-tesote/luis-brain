---
title: Posición Diaria — Daily Position Pack PRD
tags: [product, prd, dashboard, reports, treasury, fx]
updated: 2026-06-03
status: draft
audience: Luis (primary), Dan, Majo, Mariel
author: Luis Pulgar (synthesis with Claude)
linear: [URL once filed]
tesote_plan_dir: [path once /tesote-plan run]
---

# Posición Diaria — Daily Position Pack

> **One-line purpose.** A daily, delivered-to-you cash position brief — every bank, every currency, every legal entity, USD-consolidated — with yesterday's change *decomposed into flows vs devaluation*, plus exceptions and data freshness. The 5-minute morning ritual that makes Tesote a daily habit.

---

## Tesote-Plan Intake

### Actor & Problem

As a **finance lead at a multi-bank VE company (Mariel as proxy)**, I need to **see my consolidated cash position every morning with yesterday's delta explained (what moved because of flows vs what the bolívar ate) and any data/control exceptions flagged**, because **today "checking position" means logging into 10+ bank portals or eyeballing per-account balances; nobody computes daily FX revaluation (so devaluation losses are invisible until month-end); and stale scraper data silently misstates position with no warning**.

### The Test

This solves **the daily position ritual** for **finance leads** in **Workspace/Dashboard (+ IA as a second surface)**. Without it: position stays a manual multi-portal chore, devaluation cost stays invisible, and Tesote has no daily-habit surface — we remain a tool people *check sometimes* instead of a brief people *receive every morning*.

### V0 — Simplest thing that works

- [ ] Every morning at a fixed hour (default 07:30 America/Caracas), each opted-in workspace member receives the pack (delivery channel per Open Decision #1)
- [ ] Header shows: total position in USD, Δ vs yesterday, decomposed as `flujos ± / devaluación ± / sin explicar ±`
- [ ] Position table: legal entity → bank → account rows with native balance, USD value, Δ, and per-account sync recency
- [ ] Movements section: yesterday's transactions ≥ threshold + first-time counterparties
- [ ] Control section: uncategorized count, stale connections (>24h), per-account unexplained residual (ε ≠ 0) flagged as "movimientos sin capturar"
- [ ] Numbers are exact (integer cents end-to-end); decomposition identity holds to the cent
- [ ] Generated idempotently — re-running for (workspace, date) produces the same artifact

### Out of Scope (explicit "Not Doing")

- Weekly / monthly packs (catalog: [[reports-catalog]] — they sequence after)
- Forecasting / look-ahead (needs recurrence detection — v1.1+)
- Configurable alert rules / minimum-balance thresholds (one fixed large-movement threshold for v0)
- WhatsApp delivery (whatever Open Decision #1 picks, ship ONE channel in v0)
- Per-user layout customization
- Intraday refresh — this is a once-a-day artifact by design

### Technical Requirements

- [ ] Feature-flagged: `daily_position_pack`
- [ ] Permissions: render per-recipient account scope (report engine already enforces viewer scope — the pack must too; two recipients in one workspace may legitimately see different packs)
- [ ] Spanish copy (tú, VE dialect — per [[feedback_product_ui_spanish_venezuelan]])
- [ ] No emojis in product surface — inline SVG icons only ([[feedback_no_emojis]])
- [ ] Idempotent daily job keyed (workspace_id, date)
- [ ] Multi-tenant safe (workspace_id everywhere)
- [ ] Audit trail: each generated pack persisted (it's a financial statement someone may act on — must be retrievable later exactly as sent)
- [ ] Cents-integer math only; never float on money

### Rollout Plan

1. **Internal v0 (this week, zero product code)** — scheduled agent reads MCP every morning, computes the pack, posts to Slack for Luis + Mariel. Validates format, copy, decomposition math, and data quality against real Tesote Finance data
2. **v1 build** — server-side service + scheduled delivery + in-app card, dogfooded on Tesote Finance
3. **Beta** — 2–3 design-partner workspaces with hand-holding
4. **GA** — flag flipped for all

---

## Context (why now)

The [[../ai/capability-audit-2026-06-03]] verified every primitive this pack needs is already shipped: per-account daily balance series (`balance_over_time`), BCV daily rate history (`exchange_rate.history`), transaction search, categories, legal-entity tagging. The [[reports-catalog]] first-principles pass identified the daily pack as build #1 — it's the retention hook (daily habit beats monthly report), and it's mostly *assembly*, not new infrastructure.

The strategic kicker: BCV moved 544.58 → 558.64 in the last 7 days (~2.6%). Every VE company with VES balances is losing USD value daily and almost none of them see the number. We can put it in their inbox every morning.

---

## Architecture / Design

### The decomposition (the finance core — get this exactly right)

For each account, per day *t*, all in integer cents:

```
R_t  = rate (VES per USD) on day t            — exchange_rate.history (BCV), or workspace override
B_t  = native balance at end of day t          — balance_over_time series
F_t  = net signed flows during day t           — Σ amount_cents from transaction.search
V_t  = USD value = B_t / R_t

ε_t  = B_t − B_{t−1} − F_t                     — the unexplained residual

ΔV   = V_t − V_{t−1}
     = F_t / R_t                               ← FLOW EFFECT   (flows valued at today's rate)
     + B_{t−1} × (1/R_t − 1/R_{t−1})           ← FX EFFECT     (revaluation of opening balance)
     + ε_t / R_t                               ← UNEXPLAINED   (data-quality signal)
```

The identity is exact — the three components sum to ΔV to the cent. For USD accounts the FX term is zero and ΔV = F + ε.

**ε is a feature, not noise.** ε ≠ 0 means the scraper captured a balance but missed transactions (or a sync straddled midnight). Surfacing it per-account ("Bs 142.300 en movimientos sin capturar — revisá la conexión") turns the pack into a daily data-integrity check. No competitor does this; most dashboards silently absorb the gap.

**Worked example (real data, BNC VES account, 2026-06-01 → 06-02):**

| | |
|---|---|
| Opening balance | Bs 19.871.741,48 (rate 554,4258 → **$35.842**) |
| Closing balance | Bs 24.871.741,48 (rate 558,6436 → **$44.522**) |
| ΔV | **+$8.680** |
| Flow effect | +Bs 5.000.000,00 / 558,6436 = **+$8.950** |
| FX effect | 19.871.741,48 × (1/558,6436 − 1/554,4258) = **−$271** |

The account *looks* like it gained $8,680 — but flows brought in $8,950 and devaluation quietly ate $271 **in one day, on one account**. That −$271 line, summed across all VES accounts and delivered every morning, is the product.

### Pack layout (email / card — designer pass)

```
┌──────────────────────────────────────────────────────────────┐
│  POSICIÓN DIARIA · Tesote Finance · miércoles 03-jun-2026    │
│                                                              │
│  $521.840                                  BCV 558,6436     │
│  −$3.412 vs ayer                           (+0,76% vs ayer) │
│  flujos −$2.980 · devaluación −$432 · sin explicar $0       │
├──────────────────────────────────────────────────────────────┤
│  POSICIÓN POR CUENTA                                         │
│                                                              │
│  TST Servicios y Consultoría (VE)              $48.210      │
│    BNC ··2916            Bs 25.852.568   $46.277   ↑ hoy    │
│    Bancamiga ··6733      Bs   564.999    $1.011    ↑ hoy    │
│    Banco Exterior ··1849 $650            $650      ⚠ 3 días │
│    …                                                         │
│                                                              │
│  Tesote Technologies Inc (US)                  $445.217     │
│    Mercury Checking      $80.332                  ↑ hoy     │
│    Rho Cash (Checking)   $125.145                 ↑ hoy     │
│    Chase BUS COMPLETE    $10.641                  ↑ hoy     │
│    …                                                         │
│                                                              │
│  Cuentas manuales (sin verificación bancaria)  $35.864      │
├──────────────────────────────────────────────────────────────┤
│  MOVIMIENTOS DE AYER (≥ $1.000 eq.)                          │
│  −$14.264  Million Web · Mercury Checking                    │
│  +Bs 4.446.172  COVENCAUCHO (contraparte nueva) · BNC       │
│  −$1.711  Rho Card Payment                                   │
├──────────────────────────────────────────────────────────────┤
│  CONTROL                                                     │
│  12 transacciones sin categorizar (3 de ayer)                │
│  2 conexiones sin sincronizar >24h: Banco Exterior, Plaza    │
│  ε: Bs 0 — todos los saldos cuadran con los movimientos     │
└──────────────────────────────────────────────────────────────┘
```

Design notes:
- Header number is THE number — total USD position, big. Decomposition line directly under it, muted. Density before pizzazz (same anti-card-abuse doctrine as the AI surface).
- Per-account sync recency lives **in the position table** (not only in Control) — a stale balance changes how you read the number next to it.
- Manual accounts subtotal **separately labeled** — they're self-reported, not bank-verified; mixing them silently into the headline would overstate verified position.
- New-counterparty flag inline in movements — that's the fraud/typo catch.
- Email subject line: `Posición: $521.840 (−$3.412) · mié 03-jun` — the number is in the subject; zero-open-rate days still deliver value.

### v0 dogfood (zero product code, this week)

Scheduled morning agent (cron) → MCP reads (`account.list`, `balance_over_time` per currency-group, `exchange_rate.history`, `transaction.search` for yesterday, `bank_connection.status`, `transaction_rule`/category counts) → computes decomposition → posts formatted pack to Slack for Luis + Mariel.

What v0 validates before any eng spend:
1. Is the decomposition legible to a non-treasury reader (Mariel test)?
2. Does ε fire constantly on webscraper banks (calibrates the threshold before we ship it as an "alert")?
3. Is 07:30 the right hour relative to BCV publication + overnight syncs?
4. The `last_synced_at` bug pain, quantified daily (ammo for the eng fix)

### v1 (product build)

```
Sidekiq cron (per-workspace hour, default 07:30 America/Caracas)
  → PositionPack::Builder (workspace, date)
      - balance snapshots (existing balance_over_time source tables)
      - rate: BCV daily + workspace_exchange_rate override precedence
        (same fallback chain as workspace_exchange_rate.current — one source of truth)
      - decomposition per account → entity/currency rollups
      - exceptions: uncategorized count, stale connections, ε per account
  → persist PackRun (workspace_id, date, payload jsonb, unique index) — idempotent + auditable
  → delivery job per recipient (rendered with THEIR account scope)
  → in-app: Dashboard card "Posición hoy" + archive (/posicion/2026-06-03)
```

---

## Surfaces affected

- **Dashboard (cockpit)** — new card (today's pack) + archive view. This is the first real resident of the dashboard surface; it sets the visual grammar for the weekly/monthly packs that follow ([[reports-catalog]]).
- **Email** (or channel per Open Decision #1) — the delivery leg.
- **Tesote IA** — gallery chip "¿Cómo amanece mi caja?" answers from the same `PositionPack::Builder` output via MCP (new read action `position_pack.show(workspace_id, date)`), so chat and pack never disagree. The AI also becomes the drill-down: pack says "−$432 devaluación" → user asks "¿de qué cuentas?" in chat.

## Data model implications

- `pack_runs` (or similar): workspace_id, pack_type (`daily_position`), date, payload jsonb, generated_at; unique (workspace_id, pack_type, date). Soft-delete only.
- Balance snapshots: already exist (whatever feeds `balance_over_time`). Verify snapshot timing semantics — "end of day" must mean a consistent cutoff per account (America/Caracas midnight?) or ε is polluted by definition drift.
- No Odoo involvement — this is pure Tesote-side ([[project_tesote_vs_odoo_split]]: bank facts are Tesote's half).
- Recipient prefs: per-user opt-in + delivery hour on workspace membership.

## AI / automation implications

- The pack is **Automations work** (scheduled mode, per [[../ai/use-case-taxonomy]] job 5/10) — first concrete instance of "scheduled job with a delivered artifact." Build it as the pattern the Automations surface will later generalize, not a one-off.
- AI chat consumes the same builder output (read-only) — drill-down surface, never a second source of math.
- ε-alerts and stale-connection flags are the seed of the daily control loop (taxonomy job 4 scheduled mode).

## Dependencies / pre-work (from [[../ai/capability-audit-2026-06-03]])

| Dependency | Status | Blocking? |
|---|---|---|
| `balance_over_time` daily series | ✅ verified | no |
| `exchange_rate.history` (BCV daily) | ✅ verified | no |
| `transaction.search` | ✅ verified | no (100-row cap fine for 1-day windows; envelope fix still wanted) |
| `bank_connection.status.last_synced_at` | ❌ null on webscrapers | **yes, for the freshness block** — v0 can ship without it but the Control section is half-blind until fixed |
| Date-filter bug class (`period`/`preset` required) | ❌ open | no (builder passes explicit params) — but fix before AI chat touches these reads |
| EUR→USD rate availability | ❓ unverified | only for the one EUR account — check `exchange_rate.list_currencies` |

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | Delivery channel v1: email / Slack / WhatsApp (v0 dogfood = Slack regardless) | Luis | Open |
| 2 | Large-movement threshold: fixed ($1.000 eq.?) vs adaptive (p95 of trailing 90d per workspace) — propose fixed for v0, adaptive v1.1 | Luis | Open |
| 3 | Manual accounts: separate labeled subtotal (proposed above) vs excluded from headline entirely | Luis | Open |
| 4 | Send time 07:30 VET — verify against BCV publication time + overnight scraper schedule | Luis/Dan | Open |
| 5 | Weekends: send daily incl. sáb/dom (lighter pack) vs lun–vie only | Luis | Open |
| 6 | Rate for non-USD/VES currencies (EUR account): BCV cross rate vs skip-and-flag | Dan | Open |

---

## Path forward

### V1 wedge

See Intake — V0 is the wedge. The dogfood v0 (scheduled agent → Slack) starts **this week** with zero product code and de-risks every design decision above before eng touches it.

### What sequences after v1

```
v0  (now)     — agent-generated pack to Slack, Luis + Mariel dogfood
v1  (next)    — PositionPack::Builder + delivery + dashboard card + AI chip
v1.1          — adaptive thresholds, minimum-balance warnings, weekly pack reuses the builder pattern
v2            — recurrence detection → look-ahead section → forecast bridge (taxonomy job 6)
```

### Discipline calls

- Weekly/monthly packs do NOT start until daily v1 ships and shows retention (open-rate / DAU lift on dogfood + beta).
- No intraday/real-time anything — once a day is the product.
- The Automations surface doesn't block this; this pack becomes its first proof, not its dependency.

---

## References

### Internal source docs

- [[reports-catalog]] — the catalog this is build #1 of
- [[../ai/capability-audit-2026-06-03]] — primitive verification + defect list
- [[../ai/use-case-taxonomy]] — jobs 5 (cash & FX), 10 (report up), 4 (control loop)

### Memory references (load-bearing)

- [[project_tesote_vs_odoo_split]] — bank facts = Tesote-side, no Odoo dependency
- [[feedback_product_ui_spanish_venezuelan]] · [[feedback_no_emojis]] — copy + iconography rules
- [[reference_tesote_legal_entities]] — the two entities the rollup groups by

---

## Appendix — edge cases

- **Rate gap day** (BCV not yet published at send time): use last known rate, flag "tasa del día anterior" in header. Never block the send; never invent a rate.
- **Account opened/closed mid-window**: missing B_{t−1} → treat opening balance 0 with "cuenta nueva" badge; closed accounts drop after 7 days of zero-balance-zero-flow.
- **Same-day rate** (R_t = R_{t−1}, e.g. weekends): FX effect = 0 exactly — show "devaluación $0" not blank, the zero is informative.
- **Midnight-straddling syncs**: ε absorbs them one day and reverses the next; show trailing-3-day ε alongside daily to avoid false alarms.
- **Scope-restricted recipients**: totals must be *their* totals; never render a workspace-wide number to a scoped user (information leak).
