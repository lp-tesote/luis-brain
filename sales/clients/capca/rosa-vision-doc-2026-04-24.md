---
title: "CAPCA — Portal Digital B2B (Rosa Toro / DigiSalud — visión)"
tags: [capca, portal, sales, source-material]
updated: 2026-04-24
author: Rosa Toro (DigiSalud)
source: Email a luis@tesote.com — Asunto "Propuesta Integral: portal Digital B2B CAPCA"
attachment: "Propuesta Integral Portal de Clientes.docx"
status: source-material
---

# Propuesta Integral: Portal Digital B2B CAPCA

> Transcripción del DOCX que Rosa envió 2026-04-24 tras la llamada Tesote // Rosa Toro. Fuente externa — no editar contenido, solo anotar en bloques `> [LP]:`.

> **Tagline de Rosa:** *"La extensión financiera y comercial de SAP S/4HANA en manos del cliente"*

---

## 1. Visión General

El Portal Digital B2B CAPCA trasciende la función de una web informativa para convertirse en una **plataforma transaccional de autoservicio con estética de "Home Banking"**. Empoderar al cliente en la gestión de su deuda y pedidos, optimizando trazabilidad, transparencia financiera y reduciendo carga administrativa de CAPCA.

Permite a la Dirección de Finanzas visualizar de forma consolidada la operatividad de Tesorería y Ventas en un solo punto de control.

- **Apertura Estratégica:** canal digital como extensión nativa de SAP S/4HANA Cloud
- **Concepto "Banco":** gestión autónoma de historial, deudas y pagos
- **Eficiencia de Doble Vía:** ahorro 24/7 cliente + liberación operativa Ventas/Finanzas
- **Integración como Requisito:** sincronización bidireccional; lógica y precios en SAP, reflejados en tiempo real

## 2. Dashboard Financiero "Smart Aging"

- Login con **código de cliente SAP + contraseña**
- **Calculadora BCV** (widget — usa la tasa diaria que Tesote inyecta en SAP en Fase 1)
- **Dashboard tipo Fiori** — tarjetas: volumen de compras, facturas pendientes, deuda actual, facturación histórica
- **Análisis de Antigüedad (Aging):** 0–30, 31–60, 60+ días
- **Línea de Tiempo de Deuda:** cronológico, más antigua → más reciente
- **Saldo Disponible para Compra:**
  `Límite de Crédito SAP − (Vencidas + Por Vencer) = Saldo para nuevos pedidos`
  Si insuficiente → portal **bloquea** ingreso de nuevas solicitudes
- **Estado de Cuenta:** descarga en PDF / Excel

## 3. Pagos y Conciliación — Autogestión

- **Selección Múltiple:** facturas marcables para pago consolidado
- **Cálculo Exacto en Bs** según tasa BCV del momento
- **Notificación de Pago Dinámica:** soportes, bancos, números de referencia
- **Conciliación Automática (gran objetivo):** clearing en SAP FI sin intervención manual
- **Trazabilidad de Terceros:** campo obligatorio para pagos con RIF distinto al cliente (Fiscalía)
- **Retenciones de Impuesto** *(reconocida como aporte de Luis Pulgar / Tesote)*

## 4. Ciclo Comercial — Solicitudes y Precios

- **Solicitud de Pedido (NO compra directa):** registro de requerimientos (azúcar/melaza), integración SAP SD; cliente solicita reserva, Ventas valida crédito y ejecuta
- **Precios Dinámicos:** consulta SAP en tiempo real, precio personalizado por perfil
- **Validación de Saldo Pendiente:** consulta FI-AR antes de permitir solicitud
- **Forma de pago:** Contado / Crédito (informa a Ventas)

## 5. Logística — Timeline "Cita de Retiro"

Estilo DHL para retiro en Acarigua:

| Etapa | Estado en Portal | Acción Interna (SAP / Ventas) |
|---|---|---|
| 01. Solicitud Recibida | "Enviada para revisión" | Entra a flujo de aprobación Ventas |
| 02. Pedido Procesado | "Orden de Venta generada" | Validación pago/crédito + orden SAP |
| 03. Cita Asignada | "Fecha de retiro: DD/MM HH:MM" | Slot en cronograma despacho Acarigua |
| 04. Autorización de carga | "Listo para carga — QR" | Autorización con chofer + placa |
| 05. Despacho | "Retiro completado" | Cierre salida SAP + factura final |

## 6. Fundamentos Técnicos / Seguridad / Legal

- **SAP como Fuente de Verdad:** APIs OData estándar (`API_BILLINGDOCUMENT`, `API_EXCHANGERATE`)
- **Arquitectura abierta:** ¿web independiente vía APIs vs. middleware SAP CPI? — *pregunta abierta*
- **Aislamiento de datos por cliente** — *pregunta abierta*
- **Almacenamiento cifrado en AWS** (estándares EE.UU., Panamá, Curazao)
- **Blindaje Legal:** arbitraje CEDCA en Caracas
- **Términos de confidencialidad/seguridad** obligatorios en primer ingreso
- **Responsive** (móvil)

## 7. Roadmap (Rosa)

- **Fase 1:** Login + Calculadora BCV + Dashboard Fiori + Estados de Cuenta
- **Fase 2:** Solicitudes de pedido + precios dinámicos + timeline logística
- **Fase 3:** Pagos + Conciliación automática (SAP FI clearing)

## 8. Claves para Aprobación de Claudia

- Cronograma por fases (éxitos tempranos, mitigar riesgo)
- Análisis de ROI (horas-hombre cobranzas + ventas)
- **Integridad de Datos: SAP siempre manda** — sin duplicidad

---

## Cross-ref

- Mapping vs. Tesote spec: `claudia-meeting-prep-2026-04-30.md`
- Master blueprint: `customer-experience/playbooks/blueprint-operativo-capca.md`
- Counterparty PRD: `product/tesote-pay/plans/counterparty-portal-prd.md`
- HTMLs en re-do paralelo: `product/tesote-pay/prototypes/pro-112/{claim-flow-capca,workspace-capca}.html`
- Fireflies — Rosa Toro 2026-04-24: <https://app.fireflies.ai/view/01KPTRCQGMVGZQNSZ70WW391AC>
