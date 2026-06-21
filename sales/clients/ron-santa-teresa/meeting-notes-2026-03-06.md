---
title: Ron Santa Teresa — meeting notes 2026-03-06
tags: [sales, client, ron-santa-teresa, meeting]
updated: 2026-05-06
status: draft
---

# Ron Santa Teresa — meeting notes 2026-03-06

**Source:** Fireflies transcript `Tesote-Ron-Santa-Teresa-89476182-bfa9.md`.
**In the room:**
- Tesote: Esteban Suárez (AE), Luis Pulgar.
- RST: Fadi (Javier "Padi" Salama, CFO/Director), Ingrelis (tesorería lead), Carmen (tesorería), Evelyn Icar (tesorería), José Ángel Flores (gerente de sistemas).

What follows is what was important **to them**, organized by persona, with the proposal hooks pulled out at the end.

---

## Fadi (CFO/Director) — strategic frame

His pain is CEO-level pain, not finance-team pain.

- **Under-invested in finance on purpose.** "Tenemos una falencia y carencia de inversión muy grande en la parte financiera, se le ha dado prioridad al tema de CAPEX, capacidad productiva, expansión mundial con Bacardí/Diageo." Now coming back to fix it.
- **What he wants:** "Quiero control, visibilidad para poder tomar decisiones mejor y más rápido. Total, sin perder el tema compliance — usualmente cuando uno gana agilidad pierde control y yo no quiero que esto pase."
- **The "moment" framing.** He sees this as "poner la casa en orden" right before macro normalization — encaje bajando, crédito abaratándose, "ya no hay brecha". Timing-driven, not feature-driven.
- **Multi-entity / multi-country / multi-currency mess is bigger than treasury.** "Tengo el equipo totalmente saturado, la estructura cada vez más grande a nivel de compañías fuera de Venezuela." Named **Panamá and Portugal** as the international footprint.
- **Three sets of books**: nominal, constante, financiera (en USD). Manual.
- **🚩 Hard concern: information security.** "La empresa es pública, nada de eso puede contaminar mi sistema ni sacar mi información." Came back at the end via José Ángel asking about certificados/seguridad. Have the security/certs deck ready by next meeting.
- **Future-scope tease.** "Para una próxima sería bueno hablar de toda la maraña de compañías." That's a v3+ signal at CEO level — multi-entity consolidation.

---

## Tesorería (Ingrelis / Carmen / Evelyn) — operational pain

This is where the v1 ROI lives.

- **Existing bot is half-manual.** "Aunque instalamos un bot, esto representa aproximadamente **dos o tres horas** de la persona tener que descargar los archivos." → Concrete ROI line for the proposal: 2–3 hours/day per person handed back.
- **#1 ask, repeated three times: registro contable en SAP.** "El tema del registro es como que nuestro mayor valor en cuanto al proyecto." Even after dashboards, FX tracking, etc., she came back: "Eso sí tendría que ir sí o sí desde el principio." → **Phase 1 must include SAP loading from day one.** Don't sell the dashboard as Phase 1 alone.
- **Provincial is the priority bank.** "El que más nos interesaría es Provincial" — and they know it's API-less. They'll watch how we handle BBVA Provincial. Líneas de crédito + tabla de amortización en USD also matter here.
- **Banco del Tesoro = data nightmare.** "El Banco del Tesoro es un desastre total." Carmen has to request PDFs at month-end because the platform extract doesn't reconcile. → **Capa de integridad de datos** answers this directly. Highlight as a named scenario in the proposal, not just a generic feature.
- **Conciliation breaks across days.** "El banco obvia una línea, te hace un cambio de saldo… cuando registras el día siguiente tu saldo inicial no es el mismo saldo final de SAP." → Tesote's webhook update mechanism fixes this; make it explicit.
- **They wish they could register intra-day.** Cobranza is blocked until next day. Today they can't because of bad bank data. → Position Tesote intraday + categories + counterparty as the unlock for cobranza-on-T0 (without contaminating SAP).
- **Crédito y Cobranza is a real second user.** Ingrelis described needing to label inbound payments (e.g., "Licores Mundiales") so cobranza can pre-apply. → Tesote contraparte + permisos model fits; sell as a second-team unlock.

---

## José Ángel (Sistemas / SAP) — technical

Internal champion on the SAP side. Pragmatic, not gatekeeping.

- **Endorsed our v1 architecture explicitly.** "Si queremos algo más expedito, pudiera ser algo similar pero con un solo archivo… que descargan toda la información consolidada en un solo archivo y envían ese archivo al bot." Then: "**Hacer la interfaz con la plataforma — ya eso sí amerita hacer. Quizás.**" → He himself sees direct integration as v2. Validates our phasing.
- **Volunteered for the cleaner path.** When asked who adapts to whom: "Yo creo que la primera opción [Tesote produce el formato] sería la ideal, porque tú eres el dueño de los datos y las estructuras." → He's offering us format flexibility.
- **Confirmed SaaS is the expected model.** "Esta solución es un SaaS, ¿no? Ustedes son los dueños de la plataforma, no tengo yo que poner la nube de mi parte." Almost asking permission to be relieved of cloud ops.
- **End-of-meeting ask: certificados + seguridad.** Send him the security/certs documentation. He's the one who'll review it.

---

## Commercial signals

- **Fadi defined the next step explicitly**: sign NDA → we send inventory questionnaire → they fill out → second meeting to present commercial proposal. Follow that path.
- **The previous Tesote proposal didn't include SAP.** Ingrelis confirmed it. This proposal is positioned as the upgrade with SAP — that's the wedge.
- **Pricing model already understood.** Annual fee + implementation, flexible payment cadence. No friction on commercial structure.
- **Fadi is warm.** "Yo estoy todo oído, yo estoy muy entusiasmado con esto, soy fanático." Engaged on macro framing himself. He's sold on the idea; now he wants to see fit + scope + price.

---

## What this changes for the proposal / Abside session

1. **Phase 1 ≠ "just dashboards".** Their #1 ask is the SAP registro. Phase 1 must include the email-to-Bot pipeline producing the consolidated Excel. The rest of v1 (dashboards, multi-bank visibility) comes for free.
2. **Lead with Provincial.** Highest-value bank for them and the hardest technical case. If we credibly handle Provincial + Banco del Tesoro, the rest is easy.
3. **Make security/certs an early deliverable.** Fadi flagged it; José Ángel asked specifically. Don't wait for them to chase.
4. **Bake the macro framing into the cover narrative.** Fadi sold himself on "this is the moment — credit's coming back, we need control." Mirror that language back to him in the exec summary.
5. **Tease v3 (la maraña de compañías) without scoping it.** He gave us the hook himself. One sentence: "this also positions you for X."
6. **Categorización + contraparte is now a confirmed v1.5 hook**, not future-cleanup. Both Ingrelis (cobranza pre-aplicación) and Esteban's RIF→Licores Mundiales example landed. Lean in.

---

## Reconsideration of the SAP integration scope (important)

Their explicit preference (José Ángel + Fadi aligned in the room): the **first rollout is just an automated email-to-Bot file delivery** — no direct SAP integration, no master-data reads, no API/SCC/OData.

That has a real consequence: in pure v1 we **do not pass through Tesote's enrichment** (categories, counterparty, RIF, GL hint). The Bot keeps typing raw rows into FF.67 exactly as today.

This is what the v1 / v1.5 / v2 framing in `integracion-sap-propuesta-tecnica.md` is built to address. The next conversation needs to be honest about:

- **What v1 actually delivers**: 2–3 hours/day saved, single consolidated file, no human downloads. Real but limited.
- **What v1 leaves on the table**: every Tesote-side enrichment stays trapped on our side. SAP keeps needing humans to clean up categorization, counterparty, GL mapping.
- **Why v1.5 is the value step**: enriched payload reaching SAP via the same channel. Minimal additional client effort.
- **Why v2 is worth scoping now**: direct posting, EBS, retire FF.67. Bigger change but the destination.

We should sell v1 → v1.5 → v2 as a sequence, with a soft commitment to start v1 immediately and scope v1.5 in parallel.
