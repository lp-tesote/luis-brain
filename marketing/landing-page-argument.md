---
title: Landing Page — Argument & Narrative (Homepage)
tags: [marketing, website, homepage]
updated: 2026-06-06
status: draft
---

# Homepage — the argument

Working doc for the new tesote.com homepage. The story first, the pixels after.
Wireframe v1: [`landing-page/v1-wireframe.html`](landing-page/v1-wireframe.html)

## The thesis of the page

**Villain: la conciliación.** Every Tesote product closes the gap between bank-reality and book-reality at a different point in the money's life. The page never states this abstractly — it repeats it as a refrain (*"se concilia solo"*) until the visitor feels it.

**Structure: el ciclo de vida de la plata.** Ver → Pagar → Cobrar → Contabilizar → Entender. Products appear as chapters of that story, never as a catalog.

**Crescendo: Tesote AI.** The AI beat closes the product story and is *earned* by the stack above it — once banks + pagos + ERP live in one clean layer, intelligence becomes possible. ChatGPT can't reconcile your Banesco account against your ERP; the thing that can is the thing already connected to both.

**What the page is for:** legitimacy + comprehension, not cold conversion. Visitors arrive after hearing about Tesote (colega, banco, pitch). The page answers *"¿esto es real y serio?"* — clarity over cleverness, real UI everywhere, security answered on-page.

## Beliefs the visitor must leave with

1. "Esto fue construido para mi desastre exacto" (VE-specificity is the persuasion engine)
2. "Es real y serio" (UI real, logos reales, respuestas concretas de seguridad)
3. "Reemplaza trabajo, no agrega una herramienta más"
4. "Puedo actuar desde aquí, no solo mirar"
5. "Es para todo mi equipo de finanzas" — CFO a contador. Always "finanzas", never "tesorería"

## Deliberate omissions

- **No product-taxonomy dump** — five products max appear as five *chapters*, one story
- **No Odoo / system-of-record internals**
- **Network thesis stays internal** — the visitor buys "te pagan y se concilia solo"; the network is our consequence, not their pitch
- **No "Claude/OpenAI blocked in VE"** — frame positively: la IA más avanzada, aplicada a tus finanzas, disponible aquí
- **No pricing** — sales-led, single CTA: agenda una demo

---

## Page flow + draft copy (v1 — all copy is draft, Spanish-first VE, `tú`)

### 1. Nav
Logo · Producto · Seguridad · (Blog/Recursos later) · CTA **Agenda una demo**

### 2. Hero — Act I, the day-1 claim
- **H1 (candidate A — wedge, recommended):** "Todos tus bancos. Un solo lugar. En tiempo real."
- H1 candidate B (vision): "El centro de comando de las finanzas de tu empresa."
- H1 candidate C (outcome): "Cierra el día en minutos, no en horas."
- **Sub:** "Y desde ahí: paga, cobra y deja que tus libros se lleven solos. Tesote es el centro de comando de las finanzas de tu empresa."
- Visual: **real product UI** (Cuentas/Transacciones screen), never illustration
- CTA: Agenda una demo

### 2b. Product suite rail (added 2026-06-06, Luis)
Row of 5 cards directly below the hero — the whole suite scannable without scrolling, each card anchor-links to its chapter: **Connect** ("Todos tus bancos, en vivo") · **Pagos** ("Paga por API bancaria") · **Negocios** ("Cobra con un link") · **Contabilidad automática** ("Tu ERP, en piloto automático") · **AI** ("Inteligencia sobre todo"). TOC-as-proof-of-breadth; narrative below stays intact.
⚠️ Wireframe status: CSS in, section markup pending.

### 3. Logos
"Equipos de finanzas que ya operan con Tesote" — recognizable VE logos, borrowed trust.

### 4. Ve todo — Tesote Connect
- **H2:** "Ve todo. Sin entrar a ningún portal."
- Pain-first opener: posición en vivo, todos los bancos (VE · Panamá · RD · EE. UU.), Bs y USD nativo, nadie descarga un estado de cuenta nunca más.
- **The bank grid = the moat wall.** Nobody else can render it. Prominent.
- Depth proof (pick 3): categorización automática (categorías + contrapartes) · permisos granulares (x ve solo y créditos de z cuenta) · insights por transacción (contraparte, similares, comparaciones) · notas en equipo · compartir/descargar
- Refrain: cada transacción llega **categorizada y con su contraparte identificada**.

### 5. Mueve dinero — two doors, one chapter
- **H2:** "Mueve dinero desde el mismo lugar donde lo ves."
- **Door A — Paga (Tesote Pagos):** pagos directo por API bancaria, sin entrar al portal de cada banco. "Conciliado en el momento en que se ejecuta."
- **Door B — Cobra (Tesote Negocios):** "Envía un link de pago con la factura adentro. Te pagan — y no hay nada que conciliar."
- Doors stay visually separate (Luis: two products, two simple entries). If Negocios outgrows the door, it gets its own section later.

### 6. Tus libros se llevan solos — Accounting Automation
- **H2:** "Tus libros se llevan solos."
- ERP integration both directions: sube data bancaria ya enriquecida (categorías, contrapartes, tasas) · baja facturas abiertas, hace el match en Tesote, devuelve partidas conciliadas · crea proveedores, crea y corrige facturas, concilia pagos.
- Strongest visceral promise for the contador/controller — **kept as its own beat** even though internally it merges with AI.

### 7. Tesote AI — Act III, the crescendo
- **H2:** "Todo conectado. Ahora, inteligente."
- "La IA más avanzada, aplicada a las finanzas de tu empresa — con tus bancos, tus pagos y tu ERP ya conectados."
- Show, don't declare: reporte ad-hoc → guárdalo como tuyo → corre flujos a escala.
- **Visually distinct register** (dark section in wireframe) — the page shifts into the future here. As AI grows, the crescendo grows without restructuring the page.

### 8. Seguridad
- **H2:** "Tu data bancaria, tratada como lo que es."
- Concrete answers: cómo se manejan las credenciales · quién ve qué (permisos granulares) · cifrado · qué puede y qué no puede tocar Tesote.
- ⚠️ **Every claim here must be verified with Dan before it ships.** Wireframe uses `[VERIFICAR]` placeholders.

### 9. Testimonial
One strong, named quote — face, cargo, empresa. Beats six anonymous ones.

### 10. CTA band
"¿Cuánto tiempo pierde tu equipo cerrando el día?" → Agenda una demo

### 11. Footer

---

## Open decisions (Luis)

1. **Hero H1**: candidate A/B/C above — recommended A with B woven into the sub
2. **Public names**: ¿"Tesote Negocios" o "Tesote Business"? ¿Nombre en español para Accounting Automation ("Contabilidad automática")? Spanish-first page argues Spanish names
3. **Beat order confirmed?** Connect → Mueve (Paga/Cobra) → Libros → AI. Alternative: AI earlier given the land-grab — current take: trust builds data-first
4. **Security claims** — verify with Dan (read-only vs payment scopes, encryption, infra)
5. Client logos + testimonial — who can we actually use?

## Next steps

1. Luis red-pens this doc + wireframe v1
2. Reference board (tesote.cloud + 4–6 external, annotated) → `landing-page/references/`
3. Fan out 4–6 divergent art-direction variants over the locked copy skeleton
4. Curate → graft → screenshot-critique loop → tokens locked

---

## Prototype state — 2026-06-06/07 session (supersedes parts of the flow above)

Full skeleton built over the real marketing.tesote.com page (not the wireframe). **Live candidate: [`landing-page/v11-homepage.html`](landing-page/v11-homepage.html); version chain + open items in [`landing-page/README.md`](landing-page/README.md).**

Deltas vs. the spec above:

- **§2b rail**: built in v2 style (title + body + mini-UI visual per card), Brex-inspired; sits mid-page after logos, not below hero. v3 tested the doc-literal version (below hero, eyebrow + one-liner) — Luis preferred v2.
- **§5 doors → two full chapters.** Pagos and Negocios each get their own split row; strict Brex left/right alternation across all five chapters. "Mueve dinero desde el mismo lugar donde lo ves" became the Pagos body lead.
- **§8 Seguridad**: placeholders replaced with real claims (Luis, 2026-06-06): AES-256-GCM reposo + TLS tránsito + integridad SHA-256, 2FA, permisos granulares, pentests recurrentes, SOC 2 Type II *en curso* (honest pill), auditoría completa. ⚠️ Dan sign-off still pending. Note: SHA-256 phrased as integridad, not cifrado.
- **§9 Testimonial**: one-strong-quote spec beaten by reality — 3 real named quotes with logos (Ama de Casa, Cines Unidos, Paisa). Clients say "tesorería" verbatim; exempt from the finanzas rule.
- **New decision — "¿Por qué Tesote?" grid (current site) killed.** "More than software" (consulting engagement, expertos, soporte dedicado) woven instead into: testimonios sub ("Ninguno implementó solo…") + CTA band (kicker "Más que un software", consulting-engagement subtitle). No company-proof card grid.
- **§10 CTA**: question live as title.
- **Art direction resolved ahead of step 3 above**: light "Lunour" skin (Saldos/Movimientos product palette) over the site's existing token system; Brex density (1200px canvas, lowered type ceiling). The fan-out step is likely unnecessary now.
- **Still open**: hero H1/sub (§2, candidate A pending), rail→anchor wiring, logo-strip heading (§3), stat-grid claim verification, mobile pass, Rails port.
