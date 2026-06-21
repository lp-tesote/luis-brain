---
title: Retenciones SENIAT IVA + ISLR — Recorrido del Proceso para Revisión de Mariel
tags: [product, seniat, retenciones, venezuela, requiere-revision]
updated: 2026-04-28
author: luis
status: draft
revisor: mariel
---

# Retenciones SENIAT — Recorrido del Proceso (para revisión de Mariel)

**Propósito.** Validar con Mariel el modelo mental de Luis sobre el flujo end-to-end de retenciones SENIAT (IVA + ISLR) antes de actualizar el spec de producto en [[knowledge-base/product/seniat/comprobantes-automation]] e iterar los prototipos HTML de comprobantes.

**Cómo revisar.** Cada afirmación está numerada. Por favor marcar ✅ / ❌ / 🟡 ("requiere matiz") y agregar correcciones inline. Todo lo que se marque se incorpora al spec.

Contexto KB previo a leer:
- [[knowledge-base/product/venezuela/retenciones]] — mecánica completa, tarifas.
- [[knowledge-base/product/seniat/comprobantes-automation]] — feature de producto que esta validación alimenta.

Versión en inglés del mismo doc: [[seniat-retenciones-process-mariel-review]].

---

## Ejemplo numérico (usado en todo el doc)

Precio negociado: **100,000 Bs** (neto, antes de IVA). Es el ejemplo canónico — todos los escenarios de la matriz usan el mismo neto para que sean comparables uno a uno.

| Renglón | Monto (Bs) |
|---------|----------:|
| Neto (base imponible)        | 100,000.00 |
| IVA 16%                      |  16,000.00 |
| **Total factura**            | **116,000.00** |

Cuánto se retiene depende enteramente de **quién es el cliente** y **quién es el proveedor**. Ver matriz abajo.

---

## El flujo en lenguaje simple

Recorrido con el ejemplo. **Tesote como proveedor** cobrando a un cliente venezolano que es Contribuyente Especial (el caso más común para nuestro mercado objetivo).

### Paso 1 — Factura
Tesote emite factura fiscal: 100,000 + 16,000 IVA = **116,000 Bs**.

### Paso 2 — El cliente calcula las retenciones al momento del pago
El cliente (actuando como **agente de retención**) calcula:
- **Ret. IVA** = 75% × 16,000 = **12,000 Bs** (efectivo ~12% del neto).
- **Ret. ISLR** = 2% × 100,000 = **2,000 Bs** (concepto = "servicios", Tesote es PJ domiciliada).
- **Ret. municipal** si el cliente está en un municipio con ordenanza (Chacao, Baruta, etc.) — típicamente <1% sobre neto.

Total retenido en este caso canónico: **14,000 Bs**.

### Paso 3 — El cliente paga a Tesote NETO
El cliente transfiere a Tesote: 116,000 − 14,000 = **102,000 Bs**.

### Paso 4 — El cliente entrega los comprobantes a Tesote
- **Comprobante de Ret. IVA** — generado **dentro del portal SENIAT** una vez el cliente declara la quincena. Formato del número `YYYYMM########`. Debe entregarse a Tesote dentro de los **3 días hábiles** siguientes al cierre de la quincena.
- **Comprobante de Ret. ISLR** — generado por el ERP / sistema contable del cliente (SENIAT no lo emite). Contiene los campos legales (RIF pagador/proveedor, ref. factura, concepto, base, %, retenido, fecha).

### Paso 5 — El cliente declara y entera ante SENIAT
El cliente entra al portal SENIAT en la fecha correspondiente:
- **IVA** — quincenal (período 1 = días 1–15, período 2 = días 16–fin). Fecha específica por dígito terminal del RIF según el **calendario de contribuyentes especiales**. Carga vía archivo TXT batch con todas las retenciones de la quincena.
- **ISLR** — mensual, declarado en los primeros días hábiles del mes siguiente.

### Paso 6 — Pagar el tributo a través de un banco recaudador
El portal SENIAT genera una **planilla de pago** después de la declaración. El cliente paga a través del portal de su banco / banca electrónica seleccionando "pago a SENIAT" contra la planilla. Bancos recaudadores autorizados: BBVA Provincial, Banesco, BdV, BNC, etc.

### Paso 7 — Lado de Tesote: usar los comprobantes como crédito
Tesote **no** sube nada a SENIAT por estas retenciones específicas. Tesote usa los comprobantes recibidos como:
- Crédito fiscal en su propia **declaración mensual de IVA**.
- Rebaja en su **declaración anual de ISLR**.

Si los comprobantes nunca llegan → Tesote no puede reclamar el crédito → la AR de esa factura queda abierta para siempre por los 14,000 Bs.

---

## Matriz de escenarios

Todos los escenarios asumen el mismo precio negociado = **100,000 Bs neto** (total factura = 116,000 Bs si el proveedor cobra IVA). Concepto = "servicios" salvo nota.

| # | Cliente (pagador)                  | Proveedor (Tesote por defecto)              | ¿Cobra IVA?  | Ret. IVA      | Ret. ISLR             | Cash al proveedor | Comprobantes recibidos |
|---|------------------------------------|---------------------------------------------|--------------|---------------|-----------------------|------------------:|------------------------|
| **A** | **Contribuyente Especial (PJ)**    | PJ domiciliada — Especial (Tesote default)  | Sí (16,000)  | 12,000 (75%)  | 2,000 (2%)            |     **102,000**   | IVA + ISLR             |
| **B** | PJ NO especial                     | PJ domiciliada — Especial                   | Sí (16,000)  | **0**         | 2,000 (2%)            |     **114,000**   | Solo ISLR              |
| **C** | Persona natural (consumidor final) | PJ domiciliada — Especial                   | Sí (16,000)  | 0             | 0                     |     **116,000**   | ninguno                |
| **D** | Persona natural designada agente   | PJ domiciliada — Especial                   | Sí (16,000)  | 0 (PN ≠ esp.) | 2,000 (2%) 🟡         |     **114,000**   | Solo ISLR              |
| **E** | Contribuyente Especial             | PJ domiciliada **NO** especial              | Sí (16,000)  | 12,000 (75%)  | 2,000 (2%)            |     **102,000**   | IVA + ISLR             |
| **F** | Contribuyente Especial             | **Persona natural domiciliada** (freelancer, honorarios) 🟡 | Depende del estatus de la PN (formal/ordinario) | Si cobra IVA: 75% del IVA | `(100,000 × 3%) − sustraendo` 🟡 | varía | 1–2                    |
| **G** | Contribuyente Especial             | **NO domiciliada** (proveedor extranjero)   | Trato especial — típicamente ret. 100% IVA | 16,000 (100%) 🟡 | Tarifa más alta, base presunta (~27%–34%) 🟡 | reducido drásticamente | especial               |
| **H** | Contribuyente Especial             | PJ Especial — **pero RIF de Tesote no registrado en SENIAT** (edge) | Sí (16,000)  | **16,000 (100%)** | 2,000 (2%) | **98,000** | IVA + ISLR (con nota de 100% retenido) |

🟡 = requiere confirmación de Mariel. Los casos de proveedor PN y no domiciliado (F, G) involucran fórmulas y tarifas que no he validado contra el Decreto 1808 / valor de UT vigente.

### Notas por escenario

**A — Caso por defecto (Tesote vendiéndole a CAPCA, Mimesa, Fospuca, etc.).** El flujo descrito arriba. Dos comprobantes de regreso, la AR cierra solo cuando ambos se reciben.

**B — Tesote vendiéndole a un cliente más pequeño / no especial.** El cliente es una empresa normal no designada especial → no retiene IVA. La retención de ISLR sí aplica porque el Decreto 1808 obliga a *todas* las personas jurídicas a retener sobre conceptos retenibles. Tesote recibe más cash adelantado pero igual obtiene un comprobante (ISLR).

**C — Tesote vendiendo B2C a una persona natural.** La mayoría de casos retail / consumidor directo. Sin retención. Tesote recibe los 116,000 Bs completos. *(Mariel — confirmar que esto es correcto para individuos ordinarios; las PN designadas como agentes de retención son la excepción del caso D.)*

**D — Persona natural designada como agente de retención.** Caso edge. Algunas PN comerciantes son designadas. Generalmente retienen ISLR pero no IVA (la retención de IVA está restringida a especiales). Necesitamos que Mariel confirme si esto pasa en la práctica con nuestro perfil de cliente.

**E — Cliente especial, proveedor no especial.** La retención de IVA igual aplica porque lo que detona la retención de IVA es la *designación del cliente*, no la del proveedor. ISLR igual que el caso por defecto.

**F — Proveedor es persona natural (freelancer / consultor).** ISLR usa la fórmula `(base × %) − sustraendo`, con base de exención (típicamente 83.3334 UT). La tarifa para honorarios profesionales PN domiciliada es comúnmente 3%. IVA: solo si la PN es contribuyente ordinario. La mayoría de freelancers pequeños son contribuyentes formales (no cobran IVA) — en ese caso no hay IVA que retener. *Mariel — por favor confirmar el cómputo actual del sustraendo y si la tarifa 3% / fórmula sigue vigente bajo el Decreto 1808.*

**G — Proveedor no domiciliado (proveedor extranjero).** Común para SaaS importado, consultoría extranjera. IVA: típicamente 100% retenido. ISLR: base presunta × tarifa más alta. Tratamiento de tratados de doble tributación puede modificar. *Mariel — flagear si esto le aparece a nuestros clientes y cómo se maneja en la práctica.*

**H — Edge: 100% retención de IVA.** Detonado cuando (según KB existente):
- El RIF de Tesote no está registrado / no se encuentra en el portal SENIAT.
- La factura no cumple requisitos formales (numeración mala, RIF faltante, imprenta no autorizada, no se emitió factura electrónica cuando se requería).
- Tesote también es especial pero no cobró / discriminó IVA correctamente.

En nuestro ejemplo, Tesote recibe 98,000 Bs cash (vs. 102,000 en el default). Esto es el modo de falla "higiene de factura" que vale la pena flaguear en el UX del producto.

---

## Afirmaciones para que Mariel confirme

> Por favor marcar cada una como ✅ correcta / ❌ incorrecta / 🟡 requiere matiz.

### A. Quién crea el comprobante

- **A1.** El **cliente (pagador)** crea AMBOS comprobantes (IVA y ISLR). Tesote (proveedor) no crea ninguno.
- **A2.** El número del comprobante de IVA es **asignado por SENIAT** cuando el cliente sube el TXT batch quincenal — no es un número que el cliente escoge.
- **A3.** El comprobante de ISLR se crea enteramente en el ERP / software contable del cliente — SENIAT no asigna número.

### B. Quién sube a SENIAT

- **B1.** Solo el **cliente** (agente de retención) sube/declara las retenciones a SENIAT. Tesote (proveedor) **NO** sube estos comprobantes a SENIAT — Tesote solo los usa como crédito tributario en sus propias declaraciones.
  - 🚨 *El planteamiento original de Luis decía "tanto Tesote como el cliente suben a SENIAT" — según el KB existente esto es incorrecto. Por favor confirmar.*
- **B2.** Cadencia carga IVA = quincenal (cada 15 días), cadencia carga ISLR = mensual.
- **B3.** Las fechas de carga siguen el **calendario de contribuyentes especiales** de SENIAT por dígito terminal del RIF.

### C. La pata de pago bancario

- **C1.** Después de declarar en el portal SENIAT, el cliente recibe una **planilla de pago** con un monto debido y un número de referencia.
- **C2.** El cliente la paga a través del portal de su banco vía "pago a SENIAT" / "tributos nacionales", referenciando la planilla.
- **C3.** Bancos recaudadores actualmente autorizados para SENIAT: BBVA Provincial, Banesco, BdV, BNC. *(Mariel — por favor confirmar/actualizar la lista.)*
- **C4.** El pago debe hacerse en la misma fecha de vencimiento de la declaración (o dentro de una ventana corta — por favor aclarar la regla exacta).

### D. Obligaciones de Tesote como proveedor

- **D1.** Tesote **no** declara comprobantes individuales recibidos. Tesote los usa en agregado al hacer su propia declaración mensual de IVA / anual de ISLR.
- **D2.** Sin el comprobante en mano, Tesote no puede reclamar el crédito → AR queda abierta permanentemente por el monto retenido.
- **D3.** Si un cliente clasifica a Tesote como "honorarios profesionales" (5% ISLR) en vez de "servicios" (2%), Tesote tiene que detectarlo y disputar en AR.

### E. Casos edge a confirmar

- **E1.** **Retención 100% IVA** se detona cuando el RIF de Tesote no está registrado/no se encuentra en SENIAT, o cuando la factura no cumple requisitos formales. ¿Sigue activo en 2026?
- **E2.** **Anulaciones / correcciones** — ¿cuál es el flujo exacto si el cliente cargó un comprobante mal (monto, concepto)?
- **E3.** **Pago en divisas** — cuando un cliente paga a Tesote en USD, las retenciones se calculan en Bs ¿a qué tasa de cambio (BCV del día? día del pago? día de la factura?)?
- **E4.** **Proveedor persona natural (Escenario F)** — confirmar la fórmula de ISLR vigente, sustraendo, y base de exención. Confirmar tratamiento de IVA cuando la PN es contribuyente formal vs. ordinario.
- **E5.** **Proveedor no domiciliado (Escenario G)** — confirmar si retención 100% IVA es estándar, y confirmar tarifa ISLR / base presunta bajo reglas vigentes. ¿Excepciones por tratado?

---

## Dos ángulos del mismo flujo

El feature de producto [[knowledge-base/product/seniat/comprobantes-automation]] vive en el **lado del pagador** — automatiza lo que los clientes de Tesote hacen hoy (Pasos 2–6 arriba) cuando le pagan a sus proveedores vía Tesote Pay. La validación cubre ambos:

1. **Tesote como proveedor** (Pasos 1, 4-recibiendo, 7) — relevante para nuestra propia AR reconciliation.
2. **Clientes de Tesote como pagadores** (Pasos 2, 3, 4-emitiendo, 5, 6) — lo que automatizamos en producto.

El feature primariamente vive en el lado #2.

---
