---
title: "CAPCA — Deck Claudia Cisneros · 2026-04-30"
tags: [capca, sales, claudia, deck, presentation]
updated: 2026-04-29
author: Luis Pulgar
status: draft
audience: Claudia Cisneros (OCAAT / CAPCA)
language: Spanish (client-facing)
format: |
  7-slide markdown deck — one slide per H1, separated by ---.
  Drop into Google Slides / Keynote / Claude Slides.
companion: |
  Prep dossier (English, internal): claudia-meeting-prep-2026-04-30.md
  Demo HTMLs (live walkthrough — slide 3):
  - product/tesote-pay/prototypes/pro-112/claim-flow-capca-2.html
  - product/tesote-pay/prototypes/pro-112/workspace-capca-2.html
---

# Tesote × CAPCA · Portal Digital B2B
### 30 de abril de 2026

## Agenda

1. **Lo que sabemos** — su visión y la nuestra
2. **Alcance v1** — qué entregamos
3. **Demo en vivo** — el portal funcionando
4. **Rieles de pago** — cobertura bancaria
5. **Alcance v2** — Tesote Procurement
6. **Próximos pasos**

---

# 1 · Lo que sabemos

**Su visión y la nuestra coinciden ~80%.** El documento que Rosa nos compartió valida la dirección que Tesote viene desarrollando los últimos meses.

**El insight que nos cambió la conversación:**

> Lo que ustedes pusieron como **Fase 3** — Pagos y Conciliación — es nuestra **Fase 1**.
> Empezamos donde ustedes querían terminar.

**Lo que tomamos del documento e incorporamos al v1:**
Smart Aging · Pago multi-factura · Conciliación SAP FI · Calculadora BCV · Trazabilidad de terceros · Estado de Cuenta · Plazos de pago · Retenciones SENIAT

**Lo que dejamos para v2:** Solicitudes de pedido · Precios dinámicos · Logística (cita de retiro)

---

# 2 · Alcance v1 — qué entregamos

| Capacidad | Resultado para el cliente |
|---|---|
| **1. Pago multi-factura consolidado** | Selecciona N facturas, paga en un solo débito con un único OTP |
| **2. Smart Aging Dashboard + BCV** | Radiografía financiera inmediata · 0-30 / 31-60 / 60+ días · tasa BCV en vivo |
| **3. Saldo Disponible para Compra** *(CAPCA-only)* | Límite SAP − vencidas − por vencer = saldo · alerta visual si bajo |
| **4. Contraparte 360 + Estado de Cuenta** | Histórico completo · descarga PDF / Excel · plazos otorgados vs. promedios |
| **5. Plazos de pago + Retenciones** | Plazo visible por factura · comprobante con línea de retención + XML SENIAT completo |

**Por debajo de todo:** conciliación automática contra SAP FI sin intervención manual.

---

# 3 · Demo en vivo

→ `claim-flow-capca-2.html`

Recorrido (≈10 min):

1. **Email** — factura llega de CAPCA al cliente
2. **Login** — modelo híbrido (email + OTP, código SAP visible)
3. **Inicio** — Smart Aging, calculadora BCV, Saldo Disponible para Compra
4. **Pago multi-factura** — selección de 3 facturas → débito consolidado → OTP único
5. **Comprobante** — desglose por factura + línea de retención + XML SENIAT
6. **Contrapartes → CAPCA 360** — histórico completo + Estado de Cuenta descargable

Cierre: vista del workspace donde Tesorería y Finanzas monitorean conciliación y excepciones.

---

# 4 · Rieles de pago — cobertura bancaria

**Estamos en conversación activa con BNC, Banesco, Exterior y otros bancos clave.**

**Arquitectura:** *Débito Inmediato* — el cliente autoriza un débito puntual desde su cuenta hacia CAPCA, sin que CAPCA toque credenciales del cliente.

| Tipo de cuenta | Cómo funciona | Estado |
|---|---|---|
| **Persona natural** | OTP del banco emisor en cada pago | Habilitado en todos los bancos relevantes |
| **Persona jurídica** | Domiciliación o OTP empresarial | Validando habilitación B2B banco por banco |

**Hoy en producción:** BNC — persona y empresa.
**En conversación activa:** Banesco, BBVA Provincial, Mercantil, Exterior.

→ Estamos confiados en habilitar la cobertura necesaria para el piloto en plazos cortos.

---

# 5 · Alcance v2 — Tesote Procurement

Su documento incluye un módulo robusto de **ciclo comercial** que va más allá de pagos. Lo capturamos como una **fase posterior**, separada del comercial actual.

| Capacidad v2 | Qué resuelve |
|---|---|
| Solicitudes de pedido (SAP SD) | Cliente solicita azúcar/melaza · Ventas valida y ejecuta |
| Precios dinámicos | Portal consulta SAP en tiempo real, precio personalizado |
| Bloqueo de pedidos por crédito | Si vencidas > 0 → no se permite nueva solicitud |
| Logística "Cita de Retiro" | Timeline tipo DHL · QR + chofer + placa |
| Pagos parciales / abonos | Estado intermedio + clearing parcial en SAP FI |

→ **Engagement comercial separado**, después del milestone de Fase 1. Hoy queremos su lectura sobre prioridades dentro de v2.

---

# 6 · Próximos pasos

1. **Alineación de visión y alcance** para las distintas fases — v1, v2, y la transición entre ambas
2. **Definir fechas y estimados** — milestones de v1 y propuesta de cronograma para v2
3. **Propuesta de "slow roll-out"** — piloto controlado con un grupo reducido de clientes, escalando a medida que validamos cobertura bancaria y comportamiento del flujo
