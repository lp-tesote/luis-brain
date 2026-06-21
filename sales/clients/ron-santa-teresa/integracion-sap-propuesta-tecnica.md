---
title: Integración Tesote × SAP — propuesta técnica para la sesión conjunta
tags: [sales, client, ron-santa-teresa, sap, scoping, client-facing]
updated: 2026-05-06
status: draft
---

# Integración Tesote × SAP — propuesta técnica

**Documento base para la sesión técnica conjunta** entre Ron Santa Teresa, Abside, Integratec y Tesote. Recoge nuestro entendimiento de las respuestas que nos enviaron y propone una forma de fasear el proyecto. La intención es alinear alcance antes de cerrar la propuesta comercial.

---

## 1. Lo que entendimos de su respuesta

| Tema | Lo que confirmaron |
|---|---|
| Partner SAP | **Abside** acompaña la implementación; **Integratec** mantiene el contrato de soporte Basis. |
| Hospedaje | SAP en GCP, hospedado directamente por SAP. |
| Carga actual del extracto | Vía transacción **FF.67**, ejecutada por un Bot desarrollado en **SAP BTP**. |
| Disparador del Bot | El Bot se activa al recibir un correo con el archivo adjunto. |
| Lectura de datos maestros | Disponible vía SAP BTP — OData, RFC/BAPI o lectura HANA. Preferencia explícita: **no crear desarrollos Z**. |
| Conectividad | Abierta a **VPN** o **SAP Cloud Connector**, según nuestra recomendación. |

**Formato del extracto.** El archivo de muestra (`MERCANTIL BS CARST 7215902.xlsx`) tiene siete columnas: `Op.`, `Fe.valor`, `Importe`, `Asignacion`, `Texto position`, y `Saldo final` solo en la primera fila. Tesote puede entregar exactamente ese mismo layout desde cualquier banco que cubrimos, sin requerir cambios en SAP ni en el Bot.

---

## 2. Propuesta: fasear el proyecto en tres etapas

Sugerimos separar el alcance en tres fases progresivas. Las dos primeras pueden ir muy seguidas; la tercera abre una conversación de mediano plazo con su equipo Basis y con Abside.

| | **Fase 1 — Canal de entrega** | **Fase 1.5 — Entrega enriquecida** | **Fase 2 — Integración directa** |
|---|---|---|---|
| Qué hace Tesote | Envía correo con el extracto en Excel a la bandeja del Bot | Igual, pero el Excel incluye enriquecimiento Tesote: categoría, contraparte, RIF, sugerencia de cuenta GL | Postea movimientos directamente en FI; FF.67 se retira |
| Cambio en SAP | Ninguno. El Bot se mantiene tal cual. | El Bot puede aprovechar las columnas adicionales (o ignorarlas, según prefieran) | EBS configurado, consumidores BAPI/OData construidos, Bot reemplazado |
| Lectura desde SAP | No requerida | **Sí** — datos maestros: plan de cuentas, clientes/proveedores con RIF, House Bank IDs | Sí, igual que 1.5 + confirmación de posteo |
| Escritura en SAP | No (la escribe el Bot vía FF.67) | No (sigue vía Bot) | **Sí** — posteos directos a FI |
| Red | Solo SMTP | SAP Cloud Connector para OData de lectura | SCC para lectura y escritura |
| Esfuerzo de su lado | Configurar regla de correo y validar formato | Confirmar alcances OData y aprovisionar SCC | Configurar EBS, definir reglas de posteo, retirar Bot |

La lógica detrás de la propuesta:

- **Fase 1** los pone en producción rápido, **sin tocar el Bot** y sin riesgo operativo. Es esencialmente reemplazar el paso de descarga manual del usuario por un envío automatizado de Tesote.
- **Fase 1.5** es donde la integración empieza a aportar valor visible: las filas que llegan al Bot (y por tanto a SAP) ya vienen **categorizadas, con contraparte resuelta y RIF asociado**, en lugar de requerir clasificación posterior dentro de SAP.
- **Fase 2** es la evolución natural una vez consolidadas las dos primeras: saltarse el FF.67 y postear directamente en FI.

---

## 3. Recomendaciones técnicas (sujetas a su validación)

| Tema | Recomendación |
|---|---|
| Canal de entrega del extracto (Fase 1) | Tesote → SMTP → bandeja del Bot, Excel adjunto con el mismo esquema actual. Cero cambios al Bot. |
| Lectura de datos maestros (Fase 1.5+) | Servicios **OData expuestos vía SAP BTP**. RFC/BAPI como respaldo cuando no exista equivalente OData. Evitar lectura directa sobre HANA por consideraciones de seguridad y mantenimiento. |
| Conectividad (Fase 1.5+) | **SAP Cloud Connector**. Es el patrón estándar para SAP hospedado y permite exponer servicios BTP de forma controlada. |
| Desarrollos Z | No requeridos en ninguna fase. Respetamos su preferencia. |

---

## 4. Pendientes a confirmar

Para cerrar la propuesta comercial y dimensionar correctamente Fase 1.5 y Fase 2, necesitamos confirmar los siguientes puntos:

- **Edición exacta de SAP.** ¿ECC 6.0 EHP 7 sobre HANA, o ya migraron a **S/4HANA Cloud Private Edition (RISE)**? Su mención de "hospedado directamente por SAP" sugiere RISE, pero queremos confirmar para diseñar la integración alineada con la edición correcta.
- **EBS (Electronic Bank Statement).** ¿Está configurado en su sistema, aunque hoy no lo estén usando? Esto define la transición hacia Fase 2.
- **Casas bancarias y sociedades en alcance.** Número de House Banks y company codes que entrarían en el proyecto.
- **Cadencia esperada de entrega.** ¿Una entrega diaria al cierre, varias intradía, o tiempo real?
- **Convención de nombres.** Del archivo y del asunto del correo que el Bot espera para activarse correctamente.
- **Alcance de datos maestros.** Qué sociedades, qué maestro de proveedores y clientes con RIF, y qué cuentas GL son relevantes para la conciliación.
- **Responsabilidad BTP.** ¿Quién aprovisionaría los servicios OData en BTP y el túnel SAP Cloud Connector — Abside o Integratec?

---

## 5. Próximos pasos sugeridos

1. **Sesión técnica conjunta** de 30 a 45 minutos entre Tesote, Abside e Integratec, utilizando este documento como guion.
2. Salir de la sesión con: alcance de **Fase 1** cerrado, alcance de **Fase 1.5** dimensionado, y **dueños técnicos asignados** de cada lado para los entregables iniciales.
3. **Tesote envía propuesta comercial** dentro de la semana siguiente a la sesión.

---

*Cualquier ajuste sobre el alcance, fases o supuestos técnicos lo recogemos en la sesión y lo reflejamos en la propuesta comercial final.*
