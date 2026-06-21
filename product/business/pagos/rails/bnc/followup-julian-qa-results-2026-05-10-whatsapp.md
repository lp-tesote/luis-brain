---
title: Follow-up BNC tech team — QA débito inmediato — WhatsApp (enviado)
tags: [bnc, payments, debito-inmediato, qa, whatsapp, sent]
created: 2026-05-10
sent: 2026-05-10
status: sent
---

# Follow-up BNC tech team — WhatsApp (enviado 2026-05-10)

✅ **Enviado el 2026-05-10 por WhatsApp al equipo técnico de BNC.** Contenido final abajo. Pequeños ajustes de tono respecto al borrador previo: orden de bullets en resultados (OTP primero), OTP marcado con 🆗 en vez de ✅, cierre acortado y sin firma.

---

## Mensaje (final, tal como se envió)

Hola equipo, ¿cómo están?

La semana pasada hicimos las primeras pruebas de débito inmediato interbancario para jurídico<->jurídico, aquí les enviamos el reporte inicial, siguiendo la matriz que acordamos en nuestra reunión.

Probamos contra 12 bancos pagadores con cuenta jurídica:
🆗 OTP recibido en 3: BNC (intrabank), Bancamiga y Bancrecer.
✅ ACCP en los 12 — el riel acepta la transacción en todos los casos.
❌ ACCP sin OTP en 9: BdV, Mercantil, BBVA Provincial, Banesco, Banco Plaza, 100% Banco, Banco Activo, Banplus.

Algunas preguntas que nos ayudarían a avanzar:

1. Bancos top (BdV, Banesco, Mercantil, Provincial): ¿tienen info de cómo debería estar funcionando hoy el riel con ellos en PJ → PJ? ¿Hay algo que el banco del pagador tenga que activar de su lado para que dispare el OTP? El patrón ACCP-sin-OTP nos hace pensar que es config del lado pagador, pero queremos confirmar.
2. Trazabilidad: ¿qué herramientas tienen ustedes para rastrear dónde se detuvo el flujo cuando el ACCP no llega a OTP? ¿BNC ve el envío del SMS/OTP hacia el banco del deudor, o esa traza vive solo del lado del banco receptor?
3. Domiciliación: en este batch todos los requests dispararon OTP / débito inmediato. ¿Cómo se le indica al riel que un request debe procesarse como domiciliación en lugar de OTP? ¿Es un parámetro en el payload, otro endpoint, o un mandato que se enrola previamente? Queremos abrir el batch de domiciliación lo antes posible.
4. Documentación BCV: ¿existe documento oficial del BCV sobre estatus, códigos y comportamiento esperado del riel (débito inmediato y/o domiciliación)? Si lo hay, ¿nos lo pueden compartir? Si no, ¿BNC tiene un doc interno o tabla de equivalencias que podamos usar como referencia mientras tanto?

Cualquier dato, aunque sea parcial o informal, nos suma muchísimo para seguir avanzando!

Muchas gracias, quedamos atentos.

---

## Notas internas

### Deltas vs. el borrador previo
- Saludo abierto al equipo (no solo a Julian) — fue al canal/grupo de tech.
- Resultados: OTP primero, luego ACCP en los 12, luego ACCP-sin-OTP. Lectura: lo positivo arriba.
- Eliminado el bullet de "settlement end-to-end confirmado: Bancamiga" — implícito en que Bancamiga recibió OTP. (Vale tenerlo a mano si Julian pregunta.)
- Cierre más corto, sin firma — formato grupo/WhatsApp.

### Próximos pasos
- Esperar respuesta del equipo. Las cuatro preguntas son las que mueven la aguja.
- Si tardan >48h en responder, ping a Julian directo.
- Comenzar a identificar accounts para el batch de domiciliación apenas tengamos respuesta a #3.

### Relacionados
- Versión email/larga (no enviada): `followup-julian-qa-results-2026-05-10.md`
- Matriz de QA: `juridico-interbank-qa-matrix.md` (brain) / `knowledge-base/product/tesote-pay/rails/bnc/juridico-interbank-qa-matrix.md` (KB, branch `kb/bnc-qa-matrix`)
- Mensaje anterior a Julian (15-abr): `knowledge-base/.scratch/followup-julian-bnc-2026-04-15.md`
- Linear: PAY-4 — comment con este reporte añadido el 2026-05-10
