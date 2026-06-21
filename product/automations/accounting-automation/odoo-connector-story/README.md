# Odoo Connector Story — visual essay

Scroll-driven visual essay on how the Tesote ↔ Odoo connector works. Built 2026-06-12 in the approved visual-essay format ([`learnings/visual-essay-html-format.md`](../../../../learnings/visual-essay-html-format.md), reference impl: `drafts/the-untrainable/`).

- **Current version**: `odoo-connector-story-v1.html` (English) — new vN per change, never edit in place
- **Spanish twin**: `odoo-connector-story-es-v1.html` — same beats/design/tokens, copy in Venezuelan Spanish; keep the two in lockstep when versioning
- **Simplified / client-facing (ES)**: `carga-bancaria-odoo-es-v1.html` — bank-data-upload story only, no extraction/architecture detail; 7 beats: data arrives → Tesote verifies (clean + categorize + counterparty, before/after cards) → T-1 law → overnight upload → lands mapped to its Odoo bank account ready to reconcile → one-time configuration → finale. No internal markers (third-party-clean).
- **Light-mode variants**: `odoo-connector-story-es-light-v1.html` and `carga-bancaria-odoo-es-light-v1.html` — same copy as their dark siblings, inverted palette: white `#fafbfd` bg, ink `#0d1117` text, blue accent `#1661e2` (`#4d8dff` on the dark finale). The ending inversion flips the other way: dark ink finale instead of paper. Law section sits on light gray `#f1f4f9`. Keep light/dark pairs in lockstep when versioning.
- **Source material**: [`../odoo-prd.md`](../odoo-prd.md) (cockpit PRD — phasing, categories-vs-CoA, Ramp model, mapping layer, T-1 push)
- **Palette deviation from the format spec**: Tesote colors instead of gold — near-black ink `#07090d`, white text, accent blue `#4d8dff` on dark / `#1661e2` deep (from the web-app design system). Finale flips to white paper instead of cream.

## Beats

1. Hero — "Two systems, one truth" (hero grid: bank movements getting posted/turning blue)
2. Where it starts — banking data live in Tesote (ledger visual)
3. The pull — reading the full Odoo accounting graph (object chips → rendered state)
4. Two languages — categories vs chart of accounts (token contrast cards)
5. Categorize independently — Tesote never waits for Odoo (logic chain)
6. The mapping layer — translation is the integration (mapping table, versioned)
7. T-1 law (typographic beat) + the push (timeline + T−1 statline)
8. What lands in Odoo — posted statement-line mock with translations annotated
9. Three architectures, two fail — thin UI / parallel sync / mapping layer (prize card)
10. Where this goes — pipe → cockpit
11. Finale (white) — "Odoo runs the books. Tesote runs the team."

## Verifying with headless Chrome

Scroll reveals + vh sizing break naive full-page screenshots. Working recipe: make a throwaway copy that appends a `<style>` forcing `.rv{opacity:1}`, `scroll-behavior:auto`, and px section padding, then screenshot tall (`--window-size=1440,11000`); for specific sections, `display:none` the others. sips cropping is unreliable — don't bother.

Sections have ids `#s01`–`#s09` (+ `#hero`, `#law`, `#finale`) for deep links.

## Sharing

Copy to `site/index.html`, drag folder onto Netlify Drop (same flow as the-untrainable).
