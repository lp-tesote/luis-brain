# Reverón — Pitch Deck (scrollytelling)

Storytelling deck of the Reverón pitch, built in the [visual-essay HTML format](../../../learnings/visual-essay-html-format.md) with **Tesote colors** (blue `#1661e2` on light, dark finale inversion — same palette as the [odoo-connector-story light version](../../automations/accounting-automation/odoo-connector-story/odoo-connector-story-es-light-v1.html)).

## Files

- `reveron-pitch-deck-es-v3.html` — **current** (Spanish). Interactive: live demos you click during the pitch.
- `reveron-pitch-deck-es-v2.html` — pitch-mode static (minimal text, icons). Good fallback if a screen can't run JS.
- `reveron-pitch-deck-es-v1.html` — first cut (more prose). Kept for the diff.

Single self-contained file; only Google Fonts external.

### v2 → v3 — the interactions (drive these live)

| Beat | Interaction |
|---|---|
| Hero | mouse-reactive grid — moving the cursor "paints light" onto the flat banking data |
| 04 · Pregúntale | **live ask** — click a question chip → Reverón scans → answers line-by-line with trazabilidad + a "calculado en 0,7 s" stamp (3 preset questions) |
| 05 · Acciones masivas | **propose → approve → cascade** — click "propone una regla" (rows highlight) → "Aprobar" (checks cascade, badges flip to *categorizado*, status resolves). Nothing executes until you approve. |
| 06 · Aprende | **teach it live** — type a fact, hit Enseñar → it appears as a new remembered chip + "✓ lo recordará para siempre" |
| 07 · Es tuyo | **swap the model** — click "Cambiar el motor" → model name cycles underneath while "tu conocimiento: intacto" stays put |
| 08 · Roadmap | click each timeline stop to expand its detail |

All interactions degrade gracefully under `prefers-reduced-motion` (end states shown, no animation). Verified live-triggered via headless Chrome on 2026-06-21.

### v1 → v2

Same 12 beats. v2 strips explanatory paragraphs, trims copy, enlarges headlines, adds SVG icons. Goal: a deck you talk over, not read off.

## Source

Built from [`../reveron-pitch.md`](../reveron-pitch.md) (Luis's ChatGPT draft + the four thread additions: control on acciones masivas, memory/aprende, ownership/model-agnostic, no-train). The deck folds those additions in as first-class beats (06 aprende, 07 es tuyo, 05 control gate, 04 no-train note).

## Beats (one visual per idea)

| # | Beat | Visual form |
|---|---|---|
| Hero | Reverón | giant serif name + faint banking-data grid that lights up blue (info coming alive) |
| 01 | Dos años escuchándolos | request chips + twist line (isolated features won't scale) |
| 02 | Una nueva capa · 2D→3D | flat-vs-alive token contrast |
| 03 | Tres formas | three cards (recurrente / complejo / masivo) w/ examples |
| 04 | No es un chatbot · trazabilidad | answer-card mock (BCV devaluation query) + no-train note |
| 05 | Acciones masivas + control | chain + approval gate (propone → tú apruebas → ejecuta) |
| 06 | Aprende | memory chips that light up blue (what it already knows about you) |
| 07 | Es tuyo | two-layer ownership stack (your knowledge / swappable model) |
| Law | El equipo de Tesote | typographic centered statement (change management) |
| 08 | Roadmap | timeline (hoy bancaria → ERPs → Gmail/Outlook) |
| 09 | ROI tangible | numbered outcomes list |
| Finale | Primer gran paso | dark inversion + 3 imperatives + closing quote |

## Mock-data discipline

Per [marketing mock-data rules]: USD protagonist, no real bank names, Tesote-derivative entities (Comercial Andina), Bs/USD reconcile at BCV 567 (rate never printed). Footer marks "datos de muestra ilustrativos."

## Conventions / next

- Versioning: new `…-vN.html` per load-bearing change (don't edit v1 in place once shown).
- Verified visually via headless Chrome (all 12 beats) on 2026-06-21.
- An **English version** of the prose exists at [`../reveron-pitch-en.md`](../reveron-pitch-en.md); an EN deck would be `reveron-pitch-deck-en-v1.html` if needed.
- Sharing: copy to `site/index.html` → Netlify Drop for a link (per format spec).

## Open

```
open product/ai/reveron-pitch-deck/reveron-pitch-deck-es-v1.html
```
