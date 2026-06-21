---
title: Tesote AI — Rotating greeting headline
tags: [product, ai, prd, copy, voice]
updated: 2026-05-23
status: filed-as-ticket
audience: Luis (primary), Dan (eng), Majo (product)
author: Luis Pulgar (synthesis with Claude)
linear: https://linear.app/tesote/issue/PRO-163/tesote-ai-rotating-greeting-headline-finance-audience-copy-sweep
tesote_plan_dir:
---

# Tesote AI — Rotating greeting headline

> **One-line purpose.** Replace the static "asistente de tesorería" greeting on `/ai` with a rotating, founder-tone headline that frames Tesote AI as the operating system for the whole finance function — drawn from a curated pool of 10 phrases that randomize on each conversation start.

---

## Tesote-Plan Intake

> Treasury's `/tesote-plan` ingests this block. Six fields. Keep tight.

### Actor & Problem

As a **Tesote AI user (any finance-function role — CFO, controller, AP/AR analyst, contador, analista)**, I need **the greeting on `/ai/new` to read like it was built for me, not just for treasury staff**, because **the current copy ("Soy el asistente de tesorería de Tesote. Te ayudo con facturas en Odoo, conciliaciones, reglas, y trabajo con archivos. ¿Por dónde arrancamos?") narrows the perceived audience to treasury, describes capabilities the affordances below already show, and reads flat — it neither inspires the user nor signals product personality. It also uses Argentine voseo ("Subí un PDF", "empezá rápido con") in a Venezuelan-market product**.

### The Test

This solves **a positioning + voice problem** for **anyone in finance opening Tesote AI** in **IA**. Without it: **the bot continues to read like a narrow treasury tool, the headline duplicates what the capability card + quick-starts already say, and the dialect inconsistency (AR voseo in a VE product) silently erodes trust**.

### V0 — Simplest thing that works

- [ ] Greeting hero on `/ai` (new-conversation state) displays one of 10 curated phrases per page load, selected at random
- [ ] Hero typography unchanged from the locked `/ai` system (Instrument Serif, ~42px, line-height ~1.15, weight 400) — see [[typography-spec]]
- [ ] An always-visible (low-key at rest, primary on hover) ↻ button next to the hero lets the user manually shuffle to another phrase from the pool
- [ ] Capability card subtitle updated: "Ver todo lo que puedo hacer" → **"Lo que puedo hacer por tu equipo de finanzas"** (subline "20 capacidades agrupadas — listas para usar" unchanged)
- [ ] Quick-start chip preface updated: "O empezá rápido con:" → **"O prueba algo rápido:"** (VE)
- [ ] All four quick-start chips rewritten in VE: **Crea una factura nueva en Odoo · Sube un PDF y regístralo · Aplica la tasa BCV a una factura · Crea una regla de categorización**
- [ ] Bot self-description anywhere it appears (empty states, about, hover-tooltip): "asistente de tesorería de Tesote" → **"asistente de finanzas de Tesote"** or **"tu asistente en Tesote"**
- [ ] Hero rotates only on hard page load (or shuffle click) — no auto-rotation while user is reading

**The 10 phrases (final pool):**

1. Sé el mejor en lo que haces. Yo me encargo del resto.
2. El mejor equipo de finanzas de Venezuela empieza por aquí.
3. Trabaja como el mejor CFO que conoces.
4. Vuelve a finanzas el mejor lugar para trabajar en la empresa.
5. El estándar lo pones tú.
6. Cada bolívar en su sitio.
7. ¿En qué te ayudo a brillar hoy?
8. Hoy multiplicas por diez tu impacto.
9. Mueve la aguja del negocio desde finanzas.
10. Piensa en grande. Yo me encargo del detalle.

### Out of Scope (explicit "Not Doing")

- **Weighted rotation by bucket** (maestría / sparring / ambición) — random uniform is fine for v0; weighting defers to v1.1 once we have data on which lines correlate with session quality
- **Time-of-day variants** (morning push vs. end-of-day close energy) — defer
- **A/B testing infrastructure or analytics on which phrase shipped** — defer; if we want this it's its own ticket
- **The dialect sweep across all Tesote surfaces** — this ticket fixes `/ai/new`; the rest of treasury UI still has AR voseo (see Connect, Dashboard) and that's a separate, larger ticket
- **Personalized phrases** (using user name, workspace name, time-since-last-close) — defer to v1.1+
- **Localization for non-VE markets** (DR, US, Panamá) — these markets aren't on `/ai` yet; revisit when they are
- **Capability card content/IA changes beyond the subtitle text** — the card still links to the same "20 capacidades agrupadas" surface

### Technical Requirements

- [ ] Feature-flagged: `ai_rotating_greeting` (so we can flip back to the static greeting if needed during rollout)
- [ ] Spanish copy (VE register — `tú`, never `vos`)
- [ ] No emojis in any UI text or chips — per [[iconography-spec]] + [[feedback-no-emojis]]; existing inline-SVG icons in the capability card and shuffle button stay
- [ ] Phrases live as a typed constant in the React component (`app/javascript/components/ai/Greeting/phrases.ts` or equivalent) — no DB row, no API call, no admin UI. They ship with the code; updating them is a code change
- [ ] Random selection client-side using `Math.random()` — no need for cryptographic randomness; no server roundtrip
- [ ] Shuffle button: always-visible, low-key at rest, primary on hover (per [[feedback-always-visible-affordances]])
- [ ] Existing greeting component refactored, not replaced — preserve any analytics events, focus management, accessibility (`aria-label` on shuffle, hero remains an `h1`)
- [ ] Multi-tenant safe: phrases are static — no workspace-specific content, no cross-workspace leakage risk
- [ ] No audit trail needed (UI-only, no data write)

### Rollout Plan

1. **Internal** — flip `ai_rotating_greeting` on for the Tesote Finance workspace (Mariel). Verify rotation works, no layout regressions, shuffle button reads well, dialect sweep didn't miss anything on `/ai/new`
2. **Beta** — flip for 2–3 paying workspaces. Watch for confused feedback ("why does it change?"). If silent, ship it
3. **GA** — flag flipped for all `/ai` users

Reversion: if any phrase reads wrong in production, the rollback is a one-line array edit, not a feature-flag flip. The flag is for the rotation mechanic, not the phrase list.

---

## Context (why now)

The `/ai` surface has been growing fast — typography locked 2026-05-20 ([[typography-spec]]), no-emoji rule locked ([[iconography-spec]]), capability card + 20-grouped-capabilities surface in place — but the greeting copy hasn't been touched since the surface shipped. Two problems compounded:

1. **Audience framing too narrow.** The bot describes itself as "asistente de tesorería". Real users span the whole finance function — CFO, controller, AP/AR, contador, analista — and "tesorería" undersells the product. (See [[project-tesote-ai-audience]].)
2. **Headline doing the wrong job.** It enumerates capabilities ("facturas en Odoo, conciliaciones, reglas...") that the affordances directly below it (the capability card + 4 quick-start chips) already surface. The hero is the wrong surface for that work. Claude.ai uses the hero for a rotating, possibility-evoking phrase; the affordances below carry the "what can I do" payload. We're adopting that pattern.
3. **Dialect inconsistency.** Current copy mixes AR voseo (`Subí`, `empezá`) in a VE product. The greeting is the right unit of work to fix this on, even if a broader sweep waits.

Luis worked through the phrase pool on 2026-05-22 → 23: drafted 100 candidates across 8 tonal buckets, narrowed to 60, then to a final 10. The 10 sit in three clusters: maestría (5), ambición (3), sparring (1), control (1) — heavy on "be the best at your craft" and "think bigger from finance".

Prototype: [`greeting-copy-prototype.html`](./greeting-copy-prototype.html) (works locally; uses the locked Lunour palette + Instrument Serif / Inter).

---

## Architecture / Design

### Current greeting (treasury, today)

```
┌─────────────────────────────────────────────────────────────┐
│ Nueva conversación                                  listo  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Soy el asistente de tesorería de Tesote. Te ayudo con     │
│  facturas en Odoo, conciliaciones, reglas, y trabajo con   │
│  archivos. ¿Por dónde arrancamos?                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📖 Ver todo lo que puedo hacer                  →  │   │
│  │    20 capacidades agrupadas — listas para usar     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  O empezá rápido con:                                       │
│  [ Crear factura nueva ]  [ Subir un PDF y registrarlo ]   │
│  [ Aplicar tasa BCV ]     [ Crear regla de categorización] │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Target greeting (v0)

```
┌─────────────────────────────────────────────────────────────┐
│ Nueva conversación                                  listo  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [HERO — Instrument Serif, ~42px]                       ↻  │
│  Trabaja como el mejor CFO que conoces.                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [icon] Lo que puedo hacer por tu equipo de         │   │
│  │        finanzas                                  →  │   │
│  │        20 capacidades agrupadas — listas para usar │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  O prueba algo rápido:                                      │
│  [ Crea una factura nueva en Odoo ]                        │
│  [ Sube un PDF y regístralo ]                              │
│  [ Aplica la tasa BCV a una factura ]                      │
│  [ Crea una regla de categorización ]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

`↻` = always-visible shuffle button, low-key at rest, primary on hover. Behaviour: cycles to a random different phrase from the pool of 10.

### Component shape (suggested)

```ts
// app/javascript/components/ai/Greeting/phrases.ts
export const GREETING_PHRASES: readonly string[] = [
  "Sé el mejor en lo que haces. Yo me encargo del resto.",
  "El mejor equipo de finanzas de Venezuela empieza por aquí.",
  "Trabaja como el mejor CFO que conoces.",
  "Vuelve a finanzas el mejor lugar para trabajar en la empresa.",
  "El estándar lo pones tú.",
  "Cada bolívar en su sitio.",
  "¿En qué te ayudo a brillar hoy?",
  "Hoy multiplicas por diez tu impacto.",
  "Mueve la aguja del negocio desde finanzas.",
  "Piensa en grande. Yo me encargo del detalle.",
] as const;

// app/javascript/components/ai/Greeting/Greeting.tsx
const initialIndex = useMemo(
  () => Math.floor(Math.random() * GREETING_PHRASES.length),
  []
);
const [index, setIndex] = useState(initialIndex);
const shuffle = () => {
  if (GREETING_PHRASES.length <= 1) return;
  const next = (index + 1 + Math.floor(Math.random() * (GREETING_PHRASES.length - 1))) % GREETING_PHRASES.length;
  setIndex(next);
};
```

Treasury can structure differently — this is a sketch, not a mandate. What matters: the phrase array is a static typed constant, selection is client-side `Math.random()`, shuffle never repeats the current phrase.

---

## Surfaces affected

- **`/ai` (new-conversation empty state)** — the greeting hero + capability card subtitle + quick-start chip preface + chips themselves
- **`/ai` (any place the bot self-describes)** — empty states, tooltips, about modals if any
- **Feature flag service** — new flag `ai_rotating_greeting`

No data model changes. No new API endpoints. No MCP changes. No system-prompt changes.

---

## Data model implications

None. Phrases are a static constant in the React shell.

---

## AI / automation implications

None at the model layer. The system prompt stays as-is. This is a UI-shell copy change that happens before any LLM call.

---

## Open decisions

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | Rotation frequency: per page load (proposed v0) vs. per conversation vs. per session vs. on-shuffle only | Luis | Resolved 2026-05-23 — per page load + on-shuffle |
| 2 | Should the shuffle button be visible at all? (Luis precedent prefers always-visible, low-key) | Luis | Resolved 2026-05-23 — yes, always-visible |
| 3 | Does the capability card subtitle wording need stakeholder review (Mariel, Majo)? | Luis | Open — Luis to confirm before file |
| 4 | Should the dialect sweep extend to neighboring `/ai` strings (chat input placeholder, file-tree headers) in this same ticket or a follow-up? | Luis / Dan | Open |

---

## Path forward

### V1 wedge

See Intake — V0 is the wedge. The whole ticket is the wedge.

### What sequences after v1

```
v1   (Q2 2026) — 10 phrases, random per-page-load + shuffle, copy sweep on /ai/new
v1.1 (Q2-Q3)  — weighted rotation (3 buckets: maestría / ambición / sparring)
                + time-of-day variants if any feedback signal supports it
v1.2 (Q3+)    — personalization (workspace name, time-since-last-close)
v2   (Q3+)    — extend the dialect sweep + voice work to all of /ai
                (file tree, working pane headers, operation status pills)
```

### Discipline calls

- We are **not** building analytics on which phrase shipped — too small a scope for that infra, and the cost of getting it wrong is one merge to revise the array
- We are **not** opening a CMS / admin UI for phrases. They're in code. Editing them is a code change. The volume (10 lines) doesn't justify infra
- The broader VE dialect sweep across Tesote (Connect, Dashboard, etc.) is its own ticket — naming `/ai/new` as the wedge makes the scope here finite

---

## References

### Internal source docs (this PRD draws from)

- [[greeting-phrases-100]] — the 100-candidate pool
- [[greeting-phrases-selected]] — the 60 marked as keepers
- `greeting-copy-prototype.html` — working prototype with all 60, narrowed at handoff to the final 10
- [[tesote-ai-design]] — the `/ai` surface design dossier (system prompt, panes, security)
- [[typography-spec]] — the typography lock (Instrument Serif hero, Inter body, 15/1.6)
- [[iconography-spec]] — no-emoji rule + inline-SVG conventions
- [[positioning-the-finance-chief]] — positioning anchor (LATAM finance chief, not a copilot)

### External

- Linear ticket: *(to be filed)*
- Treasury plan dir: *(to be created once `/tesote-plan` runs)*
- Prototype HTML: `product/ai/greeting-copy-prototype.html`

### Memory references (load-bearing context)

- [[project-tesote-ai-audience]] — the whole finance function, not just tesorería
- [[feedback-product-ui-spanish-venezuelan]] — VE register in product UI
- [[project-tesote-ai-typography]] — typography lock for `/ai`
- [[feedback-no-emojis]] — no emojis in product UI
- [[feedback-always-visible-affordances]] — affordances always-visible, never hover-only reveal
- [[feedback-tesote-plan-workflow]] — Dan's directive: brain doc matures → `/tesote-plan`

---

## Appendix

### Why these 10 (selection rationale, 2026-05-23)

From the 100-phrase pool, Luis kept 60. From the 60, narrowed to these 10 because they:

- Lean **maestría + ambición** (8 of 10) — the founder-tone center of gravity that emerged from the 60-keep round
- Keep one **sparring** ("¿En qué te ayudo a brillar hoy?") so not every load reads as a manifesto
- Keep one **control** ("Cada bolívar en su sitio") for users who want the bot to feel precise, not just aspirational
- Drop tiempo, velocidad, carrera, reto entirely — they were the lowest-keep buckets in the 60-keep round, and consolidating around maestría + ambición + a sparring + control anchor keeps the rotation feeling intentional rather than scattered

### Phrases considered but not shipped (top 3 honourable mentions)

- *Hagamos de finanzas el área más afilada del negocio.* — sharp but slightly long for the hero
- *Convirtamos cada movimiento en una decisión.* — a strong founder line; cut because we already have "Mueve la aguja" + "Hoy multiplicas por diez" carrying the strategy angle
- *Tu caja, bajo control. ¿Empezamos?* — works, but "Cada bolívar en su sitio" felt sharper

Easy to revisit by editing the array — no ticket overhead to swap one phrase for another.
