---
title: Arajet — Restart Email Draft (post-breakup pivot)
tags: [sales, arajet, restart, legal]
updated: 2026-05-08
status: draft
---

# Restart email — Arajet

Contexto: el correo de breakup se envió el **2026-04-27** ([breakup-email-2026-04-27.md](breakup-email-2026-04-27.md)). Dos semanas después, Arajet confirmó que quiere seguir adelante con Tesote. Este correo propone retomar el proyecto con alcance y términos económicos revisados, en vez de firmar la terminación mutua.

## Cambios clave vs. contrato original

- **Alcance reducido:** solo bancos en República Dominicana + Citi (vía API proxy de Arajet) + bancos cubiertos por Plaid. Fuera: bancos de otras jurisdicciones originalmente contemplados.
- **Incluye API v2** para integración con Dynamics.
- **Fee de implementación:** USD 4,500 → **USD 6,500** (+USD 2,000 por el trabajo adicional asociado al nuevo alcance).
- **Pago de implementación:** 50% upfront, 50% al cierre.
- **Suscripción:** USD 1,500/mes a partir del **1 de junio de 2026**.
- **Mecanismo legal propuesto:** enmienda al MSA existente (no firmar la terminación, no abrir un contrato nuevo).

## Recipients

- **To:** Nikolay Maltsev (nikolay@arajet.com)
- **Cc:** Scott Clausen (Scott.Clausen@arajet.com), Scarlet Carpio (Scarlet.Carpio@arajet.com), Alexandra Hued (Alexandra.Hued@arajet.com), roberto@tesote.com, daniel@tesote.com
- **Subject:** Propuesta para retomar el proyecto — alcance revisado

## Body

```
Nikolay,

Gracias por la conversación de los últimos días y por confirmar que Arajet quiere seguir adelante con Tesote a pesar de nuestro correo del pasado 27 de abril. Tomamos muy en serio su interés y queremos proponer una forma de retomar el proyecto que sea sostenible para ambas partes.

La propuesta es ajustar el alcance del contrato para enfocarnos exclusivamente en lo que hoy podemos ejecutar con calidad:

Alcance revisado

- Todos los bancos de Arajet en República Dominicana
- Conexión con Citi a través del API proxy de Arajet
- Cualquier banco de la cartera de Arajet cubierto por Plaid (p. ej., Chase, First Horizon, etc.)
- Integración API v2 con Dynamics incluida en el alcance

Quedan fuera del alcance los bancos en otras jurisdicciones contemplados originalmente; podemos retomarlos en una etapa posterior si las condiciones lo permiten.

Términos comerciales

- Fee de implementación: USD 6,500 (los USD 4,500 originales más USD 2,000 por el trabajo adicional asociado al nuevo alcance, principalmente la integración con Dynamics vía API v2)
- Forma de pago de implementación: 50% al firmar la enmienda, 50% al cierre de la implementación
- Suscripción: USD 1,500/mes, comenzando el 1 de junio de 2026

Si están de acuerdo con estos términos, en paralelo a la confirmación, Roberto les enviará una enmienda al MSA que refleje el alcance y los términos económicos revisados, en lugar del acuerdo de terminación que les compartimos previamente.

Quedo atento a sus comentarios. Si ayuda, podemos coordinar una llamada corta esta semana para alinear y avanzar.

Saludos,
Luis

Luis Pulgar
CEO & Co-founder
Cel +1 617 584 9897
Email luis@tesote.com
Web www.tesote.com
```

## TODO antes / después de enviar

- [ ] Confirmar con Roberto que el camino es **enmienda al MSA** (vs. nuevo contrato). El MSA del 25-sep-2025 sigue vivo porque la terminación mutua nunca se firmó.
- [ ] Decidir si Nikolay es el counterpart único o si se mantienen Scott / Scarlet / Alexandra en cc. Hoy quedan en cc por consistencia con el thread del breakup.
- [ ] Coordinar con Mariel: la factura #E310000000001 (que el borrador de terminación anulaba) probablemente debe re-emitirse contra los nuevos USD 6,500 y la nueva fecha de inicio de suscripción (1-jun-2026).
- [ ] Una vez firmada la enmienda, archivar formalmente el borrador de [termination-agreement.md](termination-agreement.md) como "no ejecutado".
- [ ] Confirmar accesos bancarios DR todavía vigentes (Banco Popular, kick-off Citi API del 2026-04-06).
