---
title: Follow-up Julian (BNC) — Resultados primeros tests débito inmediato PJ-PJ (versión larga, NO enviada)
tags: [bnc, payments, debito-inmediato, domiciliacion, qa, superseded]
created: 2026-05-10
status: superseded
---

> ⚠️ **Versión NO enviada.** Sustituida por la versión WhatsApp en `followup-julian-qa-results-2026-05-10-whatsapp.md`, enviada al equipo técnico de BNC el 2026-05-10. Esta versión larga se conserva como referencia / formato email por si se necesita escalar formalmente.

# Follow-up Julian (BNC) — Resultados primeros tests débito inmediato (PJ → PJ)

**Para:** Julian (BNC — equipo de tecnología)
**De:** Luis Pulgar (Tesote)
**Fecha:** 10 de mayo de 2026
**Referencia:** Reunión del 04 de mayo + matriz de QA acordada

---

## Mensaje

Hola Julian, ¿cómo estás?

Te escribo para darte un primer reporte de los tests que arrancamos esta semana sobre la matriz de QA que acordamos en la reunión del 04 de mayo (riel de débito inmediato BCV, escenario PJ → PJ interbancario, recaudador en Tesote PJ-BNC).

Quería compartirte lo que estamos viendo y aprovechar para hacerles tres preguntas concretas que nos ayudarían a planificar los siguientes lotes de pruebas y la integración del lado de producto.

---

### 1. Resultados del primer batch (PJ → PJ, OTP)

Corrimos el primer set de pruebas contra 12 bancos pagadores, todos con cuenta de persona jurídica. El comportamiento que observamos fue **uniforme en la respuesta del riel pero divergente en la entrega del OTP**:

- **Estatus retornado por el riel:** los 12 requests volvieron con estatus `ACCP` (aceptado).
- **Bancos donde el pagador sí recibió el código OTP:** BNC (intrabank), Bancamiga, Bancrecer.
- **Bancos donde el pagador no recibió código OTP a pesar del `ACCP`:** Banco de Venezuela, Mercantil, BBVA Provincial, Banesco, Banco Plaza, 100% Banco, Banco Activo, Banplus.
- **Settlement confirmado end-to-end:** Bancamiga (PJ → PJ interbancario completó débito y abono en la cuenta recaudadora BNC).

Es decir: en 9 de 12 bancos el riel marca la transacción como aceptada, pero del lado del pagador no llega ningún OTP, por lo que el flujo no puede completarse end-to-end.

Nuestras preguntas sobre esto:

- ¿Tienen visibilidad de cómo debería estar funcionando este riel hoy con los bancos top — específicamente **BdV, Banesco, Mercantil y BBVA Provincial** — para el caso PJ → PJ?
- Sabemos que el riel no está estandarizado igual entre todos los bancos. ¿Hay algo que el banco pagador (lado del cliente que paga) tenga que activar o configurar para que el OTP se dispare correctamente?
- En los casos donde el estatus volvió como `ACCP` pero sin OTP, ¿lo interpretan como un fallo de entrega del lado del banco pagador, una configuración pendiente, o algún otro estado que no estamos leyendo bien?
- **Trazabilidad:** ¿qué herramientas o canales tienen ustedes para rastrear dónde se detuvo el flujo? ¿BNC tiene visibilidad sobre el envío del SMS/OTP hacia el banco del deudor, o esa traza vive solamente del lado del banco receptor?

Cualquier información que puedan compartirnos — aunque sea informal — sobre el estado de habilitación banco por banco nos sirve muchísimo para priorizar el resto de la matriz.

---

### 2. OTP vs. Domiciliación — cómo conmutar el flujo

En la reunión del 04 acordamos que la matriz cubre ambos flujos: **OTP** (débito inmediato por transacción) y **Domiciliación** (mandato recurrente).

Cuando enviamos los requests del primer batch, todos dispararon el flujo de **OTP / débito inmediato**. Lo que no nos quedó claro de la conversación anterior es:

- ¿Cómo se le indica al riel que un request debe procesarse como **domiciliación** en lugar de OTP? ¿Es un flag/parámetro distinto en el payload, un endpoint diferente, o un tipo de mandato que se enrola previamente y luego cada cobro hace referencia a ese mandato?
- En el caso de domiciliación, ¿el primer cobro requiere también una autorización OTP del pagador (creación del mandato), o el mandato se crea por un canal aparte y los débitos posteriores no requieren OTP?
- ¿Hay restricciones por tipo de cuenta del pagador (PN vs PJ) o por banco pagador para el flujo de domiciliación?

Queremos avanzar con un primer test de domiciliación lo antes posible para no quedarnos solo con OTP en la matriz.

---

### 3. Documentación BCV de estatus y comportamiento esperado

Para poder construir bien la capa de producto (manejo de estados, mensajería al pagador, reintentos, conciliación), necesitamos entender los estatus que devuelve el riel y qué significa cada uno.

- ¿Existe documentación oficial del **BCV** sobre el riel de débito inmediato y/o domiciliación (estatus, códigos de error, flujos esperados, requisitos de habilitación por banco)?
- Si la hay, ¿nos podrían compartir el documento o indicarnos cómo accederlo?
- Si no hay documentación pública del BCV, ¿BNC tiene algún documento interno o tabla de equivalencias de estatus que podamos usar como referencia mientras tanto?

Mientras más contexto tengamos sobre el funcionamiento del riel — especialmente la parte que depende del BCV y no de BNC — mejor podemos diseñar el producto y manejar los casos borde sin tener que preguntarles cada vez.

---

### Próximos pasos de nuestro lado

- Continuar el batch PJ-OTP contra los bancos restantes de la matriz.
- Una vez tengamos claridad sobre cómo conmutar a domiciliación, abrir el batch PJ-Domiciliación en paralelo.
- Documentar todo en la matriz de QA que les compartimos para que cuando nos veamos podamos revisarla en frío.

Quedo atento a tus comentarios. Cualquier dato adicional, aunque sea parcial, nos suma.

Gracias, Julian.

Un abrazo,
**Luis Pulgar**
Tesote
luis@tesote.com

---

## Notas internas (no enviar)

### Objetivo del mensaje
- **Formalizar por escrito** los resultados del primer batch para que queden trazables.
- **Forzar diagnóstico** del lado de BNC sobre los bancos donde el estatus volvió `aceptado` sin OTP — ese es el patrón que más nos preocupa porque sugiere un problema silencioso en el riel o en los bancos pagadores.
- **Desbloquear el flujo de domiciliación** — sin esto la matriz queda a la mitad.
- **Pedir documentación BCV** — si existe, nos ahorra ir descubriéndolo a tropezones; si no existe, esa información también es útil (sabemos que vamos a tener que documentarlo nosotros).

### Pendientes antes de enviar
- [ ] Confirmar fechas de los tests si Julian las pide.
- [ ] Decidir si copiamos a alguien más del lado BNC o lo mantenemos 1-a-1 con Julian (e.g., ¿incluir a Dan/Daniel para la pregunta de trazabilidad?).
- [ ] Actualizar la matriz de QA (`juridico-interbank-qa-matrix.md` en KB) con los 12 runs ejecutados (ACCP en todos, OTP recibido en BNC/Bancamiga/Bancrecer, settlement confirmado en Bancamiga) antes de enviar este mensaje.

### Relacionados
- Matriz de QA: `knowledge-base/product/tesote-pay/rails/bnc/juridico-interbank-qa-matrix.md`
- Mensaje anterior a Julian (15-abr-2026): `knowledge-base/.scratch/followup-julian-bnc-2026-04-15.md`
- Tracker de estado: `drafts/bnc-ach-status.md`
- Linear: PAY-4
