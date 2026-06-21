# Reverón — brand landing (reveron.ai)

Brand home for **Reverón, por Tesote AI** — the named AI agent (lab model: agent = Reverón, maker/lab = "Tesote AI", company stays Tesote). reveron.ai domain owned.

## Design direction (current — 2026-06-14)

- **Sell the transformation, at two altitudes.** Audience = AI-naïve LATAM finance teams who've never used AI. The page must *expand imagination* (40k-ft dream) AND *ground it in precise impact* (real prompts + real before/after) so it can't be dismissed as hype. Vision + proof, both. No fluff — every aspirational claim is paid off by a concrete exchange.
- **Palette: platinum on carbon** — Mercedes-AMG F1 register. Deep carbon field, brushed-platinum metallic wordmark (silver sheen gradient), cool platinum text.
- **Type:** Instrument Serif (display, chosen in Canva), Inter (body), JetBrains Mono (technical labels / the prompt lines — adds data/precision texture). Accent kept: **Reverón**.
- **Story = Tesote's arc, not the painter.** Years connecting banks / ordering data → "ready for something bigger" → Reverón is the leap. Painter reduced to one whisper line in the footer.
- **Voice:** VE Spanish, *tú*, CFO-altitude. No emoji.

## Decision (2026-06-14)

**`landing-v4.html` is the locked landing for today — final.** Centered, one-screen, platinum field + black Instrument Serif wordmark, copy-only (no product image). Do not reopen the layout; the split (v5) and wordmark+small-app galleries were explored and rejected. Any further work resumes from v4.

## Files

- `landing-v4.html` — **LOCKED / current.** Centered one-screen hero, platinum/black, copy-only.
- `landing-v5.html` — split (copy left / app right) experiment. Rejected. v4's platinum/black aesthetic converted to an **asymmetric split: copy left, full-app image right**, Reverón dialed a bit smaller. One screen, no scroll (app hidden < 980px). App = split-theme 3-pane (convos · chat · approval). Copy uses the **improved** line, not v4's: tagline *"Deja de operar tus finanzas. Dirígelas."* + sub *"Reverón concilia, categoriza y arma tus reportes. Tú solo apruebas."* (pairs with the approve-image). Luis rejected all wordmark+small-app gallery layouts as "hideous" — this clean split is what he liked.
- `landing-v4.html` — centered, copy-only, no image. The look Luis approved; v5 is its split evolution. (2026-06-14). Per Luis: **giant "Reverón" dominates, the full-app image is small/supporting.** Platinum field, black letters, single-screen each (no scroll). Vary by app placement (below / corners / bottom-bleed / behind-as-ghost / floating / strip / right-slice / overlap / asymmetric) and wordmark treatment (solid / outline-stroke / wide-tracking / ghost-watermark / extra-large). Constant copy + app (split theme, approval right-pane). Awaiting Luis's pick.
- `hero-app-options.html` — 20 iterations where the full app was the *large* hero. Superseded by the wordmark-led direction; kept. (2026-06-14). Per Luis: the hero image = the **whole product app** — conversations nav (left) · chat interactions (center) · proposals-waiting-for-approval (right). All built from one JS-rendered app template; vary by frame (bleed / browser / laptop / float / tilt / tilt2), theme (split = dark sidebar + light panels, like the live app · dark · light · mono/platinum), right-pane content (actions / report / categorías / pagos / conciliación / gráfico / digest), and copy placement (overlay / above / left / none / bottom-bar). Constant copy. Awaiting Luis's pick → build into the full single-screen landing.
- `hero-options.html` — earlier 20 iterations where the UI was a *card* (single approval table), not the full app. Superseded by hero-app-options but kept. (2026-06-14). All show the **proposed-work → approve** product UI (the agentic, human-in-the-loop concept Luis flagged in the live-app screenshot — Reverón does the labor, you approve). Constant copy across all so the comparison is UI-treatment only. Each option is itself one-screen/no-scroll; the gallery stacks them. Variants span framing (floating / tilted 3D / chat→table / before-after / full-app / macro / stack / browser / data-horizon / approve-in-action), content (acciones / categorización / pagos / conciliación / reporte / digest), and treatment (glass / editorial / wireframe / copy-dominant / right-edge bleed). Awaiting Luis's pick(s) → then build the chosen into the full single-screen landing.
- `landing-v4.html` — one-screen platinum/black, copy-only (no product UI yet). One screen, no scroll (`overflow:hidden`, fits down to ~720px height). **Inverted palette: platinum/brushed-metal field, black letters** (wordmark has a subtle white letterpress emboss). "por Tesote AI" sized up. Ruthlessly cut to: wordmark · endorsement · tagline (*"Inteligencia artificial, dentro de tus finanzas."*) · one proof line (*"Pregunta, construye reportes, automatiza. Lo que tomaba días, ahora toma una frase."*) · CTA. Dream + proof in a single glance.
- `landing-v3.html` — dark carbon, 4-section scroll (hero → shift → proof exchanges → leap). Superseded by the one-screen direction; mine it for the longer-form copy + the 4 example exchanges if we ever build a deeper page. Four sections, descending altitude: **40k ft** (hero promise + "the shift" provocation — AI changed the world, your finance dept hasn't touched it, that ends *hoy*) → **on the ground** (4 prompt→outcome→impact exchanges, e.g. "media mañana en Excel → una frase") → **the leap** (Tesote's arc + aspirational close) → footer whisper. Hero tagline: *"Inteligencia artificial, dentro de tus finanzas."*
- `landing-v2.html` — platinum/carbon, brand-teaser altitude. Too cool/vague for an AI-naïve buyer — superseded, kept for the diff.
- `landing-v1.html` — warm dawn-light + painter manifesto. Superseded, kept for the diff.

## Evolution

- v1: warm dawn light on canvas-white (the painter's light) + heavy artist story.
- v2: → platinum on carbon; story pivots to Tesote's arc; value prop = power/depth/3D.
- v3: → sells the AI transformation explicitly; adds concrete prompt→outcome→impact proof.

## Verify

Headless-Chrome screenshot + LOOK before claiming done (per workflow). v3 hero, "shift", lead, and exchange block verified rendering 2026-06-14.

## Open decisions / next

- **`by` vs `por` Tesote AI** — page uses *por* (native on a Spanish page); Luis wrote "by". His call.
- CTA target — `Solicitar acceso` is a placeholder anchor; wire to waitlist/form for launch (~late June).
- The 4 example exchanges are credible-but-illustrative — confirm each maps to a real shipped/launch-scope capability before going live.
- Pending: persona/voice bible (keystone — feeds site voice + product system prompt), wordmark/lockup asset, tagline final.
