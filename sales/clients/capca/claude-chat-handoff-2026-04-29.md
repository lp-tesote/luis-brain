# CAPCA Claudia Meeting — Claude Chat Handoff

> **Purpose of this doc:** Self-contained context dump so Luis can continue the work in claude.ai (which doesn't have access to his local files). Paste this entire doc into a fresh chat to bring the new conversation up to speed.
>
> **Last updated:** 2026-04-29 (afternoon, day before meeting)

---

## Who I am, what I'm doing

I'm **Luis Pulgar**, CEO of **Tesote** — a Venezuelan B2B SaaS / fintech company. 2026 goal: 10x revenue. We work in payments, treasury, ERP integrations for LATAM mid-market.

Tomorrow (**2026-04-30**) I have a meeting with **Claudia Cisneros** — the OCAAT decision-maker for **CAPCA** (Central Azucarero Portuguesa C.A., one of the largest sugar producers in Venezuela, part of Grupo Cisneros). CAPCA just went live with **SAP S/4HANA Cloud on 2026-03-09** and we're their treasury / banking automation partner.

The contract for the broader project is signed (Fase 1 = bank hub + SAP MT940 + BCV automation, currently in implementation). Tomorrow's meeting is about **the customer portal piece** — a payer-facing portal that lets CAPCA's customers self-manage invoices, pay them, see their account.

---

## What just happened (context for the meeting)

On **2026-04-24** I had a call with **Rosa Toro** (a consultant working with CAPCA, from DigiSalud) where she shared CAPCA's vision for this customer portal. She sent a written doc afterwards (`Propuesta Integral Portal de Clientes.docx`) that lays out their full vision.

The vision overlaps ~80% with what Tesote has been building independently for the last few months (a product internally called **Tesote Negocios**). The key strategic insight:

> **Lo que ustedes pusieron como Fase 3 — Pagos y Conciliación — es nuestra Fase 1. Empezamos donde ustedes querían terminar.**

We've already built the prototypes (`claim-flow-capca-2.html` + `workspace-capca-2.html`) that demo the portal. Tomorrow's meeting will use those prototypes as a live demo. The deck is scaffolding around the demo, not the substance.

---

## Rosa's vision document (source material)

> Title: *"Propuesta Integral: Portal Digital B2B CAPCA"*
> Tagline: *"La extensión financiera y comercial de SAP S/4HANA en manos del cliente"*
> Sent by Rosa Toro (rosa.toro@digisalud.org) on 2026-04-24

### 1. Visión General

The Portal Digital B2B CAPCA is a transactional self-service platform with **"Home Banking" aesthetic**. Empower the customer to manage their debt and orders, optimize traceability, financial transparency, and reduce CAPCA's administrative burden. Lets Finance Director see Treasury + Sales operations in one place.

- **Apertura Estratégica** — digital channel as native extension of SAP S/4HANA Cloud
- **Concepto "Banco"** — autonomous management of history, debts, payments
- **Eficiencia de Doble Vía** — 24/7 customer savings + ops liberation for Sales/Finance
- **Integración como Requisito** — bidirectional sync, logic + pricing live in SAP

### 2. Dashboard Financiero "Smart Aging"

- Login con código de cliente SAP + contraseña
- Calculadora BCV widget (uses Tesote's Phase 1 BCV automation)
- Fiori-style cards: volumen de compras, facturas pendientes, deuda actual, facturación histórica
- Aging analysis: 0–30 / 31–60 / 60+ días
- Línea de tiempo de deuda
- Saldo Disponible para Compra: `Límite SAP − (Vencidas + Por Vencer) = Saldo`
  - If insufficient → blocks new requests
- Estado de Cuenta download (PDF / Excel)

### 3. Pagos y Conciliación — Autogestión

- Multi-invoice select for consolidated pay
- Exact Bs. calc using BCV at moment of payment
- Bank/reference/proof upload
- **Conciliación automática SAP FI clearing** (the big goal)
- **Trazabilidad de terceros** (RIF mismatch flag for compliance / Fiscalía)
- **Retenciones** (acknowledged Luis's input)

### 4. Ciclo Comercial — Solicitudes y Precios

- Solicitud de pedido (NOT direct purchase) — SAP SD integration
- Precios dinámicos — real-time SAP query, personalized by client profile
- Saldo validation against FI-AR before allowing new request
- Forma de pago (Contado / Crédito) info to Sales

### 5. Logística — Timeline "Cita de Retiro"

DHL-style for retiro in Acarigua:
1. Solicitud Recibida → "Enviada para revisión"
2. Pedido Procesado → "Orden de Venta generada"
3. Cita Asignada → "Fecha de retiro: DD/MM HH:MM"
4. Autorización de carga → "Listo para carga — QR" (chofer + placa)
5. Despacho → "Retiro completado"

### 6. Fundamentos Técnicos / Seguridad / Legal

- SAP as source of truth — APIs OData (`API_BILLINGDOCUMENT`, `API_EXCHANGERATE`)
- Open architecture question: web independiente vs. middleware SAP CPI?
- Tenant/data isolation question
- AWS encrypted storage (US, Panamá, Curazao standards)
- CEDCA arbitraje (Caracas)
- Mandatory T&C on first login
- Responsive (mobile)

### 7. Roadmap (Rosa)

- **Fase 1:** Login + BCV + Fiori dashboard + Estado de Cuenta
- **Fase 2:** Solicitudes + precios dinámicos + timeline logística
- **Fase 3:** Pagos + Conciliación SAP FI clearing

### 8. Claves para Aprobación de Claudia

- Cronograma por fases (early wins, mitigate risk)
- ROI analysis (horas-hombre cobranzas + ventas)
- **SAP siempre manda** — no data duplication

---

## Strategic framing (decisions baked in)

### How Rosa's vision maps to Tesote's spec

| Bucket | Items |
|---|---|
| **Already in v1** | Dashboard with pendientes/deuda/histórico · timeline · multi-bank pay · trazabilidad terceros · retenciones (line in comprobante) · multi-invoice select · estado de cuenta download · BCV calc · aging buckets |
| **Promote to v1 for CAPCA** | Saldo Disponible para Compra (CAPCA-only, display-only no blocking) · SENIAT XML completo |
| **Defer to v2** | Solicitudes de pedido · Precios dinámicos · Bloqueo por crédito · Logística (cita de retiro) · Pagos parciales / abonos |

### The phasing flip — the load-bearing strategic argument

Rosa's roadmap puts Pagos + Conciliación as **Fase 3**. Tesote's natural fit is **Fase 1**. Frame to Claudia: "Empezamos donde ustedes querían terminar." Highest-ROI piece first, lowest-risk path to value.

### Tactical posture (locked)

- **Portal IS the protagonist.** CAPCA mental model: SAP does everything; portal is the customer-facing extension of SAP.
- **Do not push the workspace dashboard.** It exists, but for CAPCA's day-to-day operators, SAP is the workspace. Tesote workspace = monitoring/exceptions only.
- **Auth model = hybrid.** Email + OTP for auth; SAP customer code shown as identifier in dashboard. Don't build passwords (payers aren't Tesote customers).
- **v2 = "Tesote Procurement"**, separate engagement, post-Fase 1 milestone. Capture, don't commit commercial.
- **Tone = warmth + conviction.** Open with 60 sec of rapport before slides. It's a relationship moment as much as a pitch.

### Decisions Claudia owns at the meeting

1. **Auth model** — recommend hybrid (email+OTP, SAP code visible)
2. **Pilot scope** — 5–10 clients, 4–6 weeks, BNC-paying first
3. **v2 Procurement** — in/out of current commercial scope (recommend: separate engagement)

---

## The deck — current state

7-slide deck, Spanish, client-facing. Currently rendered as HTML using Tesote design system (Inter font, brand blue #1661E2, white surfaces, pure black text, Tesote SVG logo). Luis is rebuilding this in **Canva** for tomorrow's meeting.

### Slide 1 — Cover + Agenda

**Cover content:**
- Pill: "Propuesta · Portal Digital B2B"
- H1: "Portal Digital B2B para **CAPCA**" (CAPCA in brand blue)
- Subtitle: "Visión, alcance v1 y roadmap. Conversación con Claudia Cisneros para alinear próximas fases."
- Meta: Cliente (CAPCA · OCAAT) · Para (Claudia Cisneros) · Equipo Tesote (Luis Pulgar · Nicolás Rossini) · Fecha (30 de abril de 2026)

**Agenda (right side):**
1. Lo que sabemos — Su visión y la nuestra
2. Alcance v1 — Qué entregamos
3. Demo en vivo — El portal funcionando
4. Rieles de pago — Cobertura bancaria
5. Alcance v2 — Tesote Procurement
6. Próximos pasos

> *La parte central de la conversación será una demo en vivo del portal funcionando.*

### Slide 2 — Lo que sabemos *(BEING REWRITTEN — see "in-progress" section below)*

**Current content (about to be replaced):**
- H2: "Su visión y la nuestra coinciden ~80%"
- Subtitle: "El documento que Rosa nos compartió valida la dirección que Tesote viene desarrollando los últimos meses."
- Big insight callout: *"Lo que ustedes pusieron como Fase 3 — Pagos y Conciliación — es nuestra Fase 1. Empezamos donde ustedes querían terminar."*
- Two columns:
  - Lo que tomamos al v1: [tags] Smart Aging · Pago multi-factura · Conciliación SAP FI · Calculadora BCV · Trazabilidad de terceros · Estado de Cuenta · Plazos de pago · Retenciones SENIAT
  - Lo que dejamos para v2: Solicitudes de pedido · Precios dinámicos · Logística (cita de retiro) · Pagos parciales

### Slide 3 — Alcance v1

**H2:** "Cinco capacidades en producción para v1"
**Subtitle:** "Por debajo de todo: conciliación automática contra SAP FI sin intervención manual."

| # | Capacidad | Resultado para el cliente |
|---|---|---|
| 01 | Pago multi-factura consolidado | Selecciona N facturas y paga en un solo débito con un único OTP del banco. |
| 02 | Smart Aging + Calculadora BCV | Radiografía financiera inmediata · 0–30 / 31–60 / 60+ días · tasa BCV en vivo. |
| 03 | Saldo Disponible para Compra **[CAPCA-only]** | Límite SAP − vencidas − por vencer = saldo · alerta visual cuando esté bajo. |
| 04 | Contraparte 360 + Estado de Cuenta | Histórico completo · descarga PDF / Excel · plazos otorgados vs. promedios reales. |
| 05 | Plazos de pago + Retenciones SENIAT | Plazo visible por factura · comprobante con línea de retención + XML SENIAT completo. |

### Slide 4 — Demo en vivo

**H2:** "El portal funcionando"
**Subtitle:** "Recorrido de extremo a extremo, ≈10 minutos. Cierre breve en el workspace donde Tesorería y Finanzas monitorean conciliación y excepciones."

**Demo script (live walkthrough of `claim-flow-capca-2.html`):**

1. **Email** — factura llega de CAPCA al cliente. Notificación automática con link directo al portal.
2. **Login** — modelo híbrido. Email + OTP, código SAP visible en cada pantalla.
3. **Inicio** — Smart Aging + BCV + Saldo Disponible. Radiografía financiera completa al primer vistazo.
4. **Pago multi-factura** — selección de 3 facturas → débito consolidado → OTP único.
5. **Comprobante** — con retención + XML SENIAT. Desglose por factura · línea de retención · descarga directa.
6. **Contrapartes → CAPCA 360 → Estado de Cuenta** — Histórico completo, descarga PDF/Excel, plazos otorgados vs. promedios.

### Slide 5 — Rieles de pago

**H2:** "Conversaciones activas con **BNC, Banesco y Exterior**"
**Subtitle:** "Estamos confiados en habilitar la cobertura necesaria para el piloto en plazos cortos."

**Architecture banner (dark/black):**
> **Arquitectura — *Débito Inmediato*** — el cliente autoriza un débito puntual desde su cuenta hacia CAPCA, sin que CAPCA toque las credenciales del cliente.

**Coverage table:**

| Tipo de cuenta | Cómo funciona | Estado |
|---|---|---|
| **Persona natural** | OTP del banco emisor en cada pago | ● Habilitado en todos los bancos relevantes |
| **Persona jurídica** | Domiciliación o OTP empresarial | ● Validando habilitación B2B banco por banco |

**Two columns:**
- **Hoy en producción:** BNC · persona y empresa
- **En conversación activa:** Banesco · BBVA Provincial · Mercantil · Exterior

### Slide 6 — Alcance v2 (Tesote Procurement)

**H2:** "Tesote **Procurement** — el ciclo comercial completo"
**Subtitle:** "Su documento incluye un módulo robusto que va más allá de pagos. Lo capturamos como una fase posterior, separada del comercial actual."

| Capacidad v2 | Qué resuelve |
|---|---|
| Solicitudes de pedido (SAP SD) | Cliente solicita azúcar / melaza · Ventas valida y ejecuta en SAP. |
| Precios dinámicos | Portal consulta SAP en tiempo real · precio personalizado por perfil. |
| Bloqueo de pedidos por crédito | Si vencidas > 0 → no se permite nueva solicitud. Extiende el Saldo Disponible de v1. |
| Logística "Cita de Retiro" | Timeline tipo DHL · QR + chofer + placa · estatus visible al cliente. |
| Pagos parciales / abonos | Estado intermedio de factura + clearing parcial en SAP FI. |

**Phase callout:**
> **Engagement comercial separado**, posterior al milestone de Fase 1. Hoy queremos su lectura sobre prioridades dentro de v2 — qué pesa más para ustedes.

### Slide 7 — Próximos pasos

**H2:** "Cómo avanzamos juntos"
**Subtitle:** "Tres conversaciones que necesitamos cerrar para entrar en ejecución."

**Timeline (vertical, dot+line markers):**

1. **Alineación de visión y alcance para las distintas fases**
   v1, v2 y la transición entre ambas. Confirmar que las prioridades quedan capturadas correctamente y que no hay piezas faltantes desde la perspectiva de CAPCA.

2. **Definir fechas y estimados**
   Milestones de v1 — fecha de arranque del piloto, criterios de salida — y propuesta de cronograma para v2.

3. **Propuesta de "slow roll-out"**
   Piloto controlado con un grupo reducido de clientes, escalando a medida que validamos cobertura bancaria y comportamiento del flujo en producción.

---

## In-progress: Slide 2 ("Lo que sabemos") rewrite

Luis is reframing slide 2 to be less transactional and more partnership-grade. New direction:

**4 bullets (in order):**

1. **Compartimos la misma visión del alcance y los objetivos.**
2. **Queremos sentar un precedente de cómo se relacionan cliente y proveedor en Venezuela.**
3. **Tesote tiene la experiencia, capacidad y know-how para construir software de talla mundial.**
   *(alternative: "software generacional" — bolder but riskier in C-level Spanish)*
4. **CAPCA es una empresa líder de su sector que está transformando su operación con tecnología.**

**Structure:** shared belief → shared ambition → our credibility → CAPCA's character. Pairs nicely as 2×2 in Canva (top row = partnership, bottom row = each party).

**What gets relocated:** the "Fase 3 → Fase 1" insight. **Don't lose it** — move it to slide 3 (Alcance v1) as the opening callout. It's the line that explains *why* we're delivering what we're delivering.

**Slide title:** keep "Lo que sabemos" (modest title, bullets do the work). Alternative: "Por qué estamos aquí" or "Compartimos una visión".

---

## Tesote design system (for Canva styling)

From `tesote.lunour.design` — same system used in the Coca-Cola Core Plus proposal.

### Colors

| Token | Hex | Use |
|---|---|---|
| `--color-text-primary` | `#000000` | Headlines, main text |
| `--color-text-secondary` | `#4b5563` | Body text |
| `--color-text-tertiary` | `#9ca3af` | Meta, labels |
| `--color-surface-primary` | `#ffffff` | Main background |
| `--color-surface-secondary` | `#f9fafb` | Card / section backgrounds |
| `--color-surface-tertiary` | `#f3f4f6` | Pills, inputs |
| `--color-border` | `#e5e7eb` | Dividers |
| `--color-brand` | `#1661E2` | Tesote blue — accents, highlights |
| `--color-brand-light` | `#eef4ff` | Brand-light backgrounds |
| `--color-brand-dark` | `#104ab5` | Hover states |

### Typography

- **Font:** Inter (Google Fonts) — weights 300/400/500/600/700/800
- **H1:** clamp(40px, 6vw, 64px) · weight 800 · letter-spacing -0.04em · line-height 1.05
- **H2:** 24–38px · weight 700 · letter-spacing -0.025em · line-height 1.15
- **H3:** 22px · weight 700 · letter-spacing -0.02em
- **Subtitle:** 17–20px · weight 400 · color text-secondary · max-width 880px
- **Body:** 14–15px · color text-secondary · line-height 1.5

### Spacing (4pt grid)
4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64

### Radii
- `sm`: 6px
- `md`: 12px
- `lg`: 24px
- `full`: 9999px

### Components

- **Pill:** uppercase, 12px, weight 600, letter-spacing 0.04em, rounded-full, surface-tertiary bg
- **Pill primary:** black bg, white text
- **Tag:** 11–12px, weight 500, rounded-full, surface-tertiary bg
- **Tag brand-light:** brand-light bg, brand color, weight 600
- **Stat box:** white bg, border, shadow-sm, padding 16px, radius-md
- **Hero card:** surface-secondary bg, padding 32px, radius-lg, border
- **Timeline:** dot (12px, black, rounded) + line (1px, border color)
- **Architecture banner:** black bg, white text, brand-blue accent

### Visual conventions

- Use brand blue **sparingly** — for accent words inside headlines (`<span class="highlight">CAPCA</span>`), brand-light tags, button accents, status pills. Not for big areas.
- Section headers as `01 — Title` format (number in brand blue, em-dash, then plain title)
- Tables: uppercase th in tertiary text color, left-aligned, surface-secondary bg
- Numbered lists: number in brand blue, weight 700

---

## Open threads (pick up here)

1. **Slide 2 rewrite** — finalize bullet wording, decide "talla mundial" vs. "generacional", produce final Canva layout (2×2 vs. vertical)
2. **Where does the "Fase 3 → Fase 1" insight live now?** Recommend: slide 3 callout
3. **Pilot scope** — Luis didn't fully decide whether to put a number (5/10/20) on the slides or leave it for the conversation. Currently absent from deck.
4. **What % of CAPCA's customers pay from BNC vs. other banks** — useful data point for the meeting; not on slides but worth being ready to ask.
5. **Auth model** — currently shown as "decided" (hybrid). If Luis wants Claudia to confirm live, surface as a question.
6. **Closing line / explicit ask** — current deck ends on "tres conversaciones que necesitamos cerrar." Could add a clearer "what we need from CAPCA in the next 14 days" if Luis wants stronger close.

---

## File locations (in Luis's brain repo, for reference)

```
~/Programming/tesote/luis-brain/
├── sales/clients/capca/
│   ├── rosa-vision-doc-2026-04-24.md         ← Rosa's full doc transcribed
│   ├── claudia-meeting-prep-2026-04-30.md    ← Internal prep dossier (English)
│   ├── claudia-meeting-deck-2026-04-30.md    ← Markdown deck source
│   ├── claudia-meeting-deck-2026-04-30.html  ← Rendered HTML deck (Tesote design system)
│   └── claude-chat-handoff-2026-04-29.md     ← THIS FILE
├── sales/clients/capca.md                    ← Master CAPCA client record
├── customer-experience/playbooks/
│   └── blueprint-operativo-capca.md          ← Master CAPCA blueprint (project Fases 1/2/3)
├── product/tesote-pay/
│   ├── plans/counterparty-portal-prd.md      ← Tesote Negocios v1 PRD
│   └── prototypes/pro-112/
│       ├── claim-flow-capca-2.html           ← Latest payer-side prototype (CAPCA-tailored)
│       ├── claim-flow.html                   ← Canonical (cross-client)
│       ├── workspace-capca-2.html            ← Latest workspace-side prototype
│       └── README.md                         ← Engineering handoff packet
└── drafts/
    └── prompt-capca-htmls-iteration.md       ← Prompt template for HTML iterations
```

Fireflies of the Rosa call: <https://app.fireflies.ai/view/01KPTRCQGMVGZQNSZ70WW391AC>
