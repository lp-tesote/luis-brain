---
title: Veconinter × Tesote — Blueprint de Trabajo (v1)
tags: [sales, veconinter, blueprint]
updated: 2026-06-18
status: draft
---

# Veconinter × Tesote — Blueprint de Trabajo

**Versión:** v1 · **Fecha:** 2026-06-18 · **Origen:** sesión de discovery posterior a la reunión intro del 2026-06-01

Este documento resume cómo trabajaríamos juntos: qué casos de uso cubrimos, cómo hacemos las integraciones, con qué frecuencia se actualiza la data y en qué fases avanzamos. Es un borrador de trabajo para validar y afinar en la sesión de hoy.

---

## 1. Objetivo

Automatizar la tesorería de Veconinter en Venezuela: eliminar el trabajo manual de entrar banco por banco, descargar el libro banco, armar el flujo de caja en Excel y cargar las plantillas de ingresos al sistema interno (SCI). El objetivo de salida de hoy es dejar acordado este blueprint para pasar a propuesta.

---

## 2. Alcance — Fase 1 (Venezuela)

- **13 cuentas en Venezuela** (prioridad).
- **2 cuentas en USD** asociadas a la entidad VE: **Facebank** y **Mercantil Panamá**.
- Estados Unidos y demás mercados quedan explícitamente para una **Fase 2** (paralela), no se pierden de vista.

> **Por validar hoy:** confirmar el inventario de cuentas (la plantilla que enviamos) para cerrar el alcance exacto de Fase 1.

---

## 3. Casos de uso

### 3.1 Conexión bancaria automatizada — la base

Tesote se conecta una sola vez en el setup y mantiene la conexión persistente. El equipo deja de entrar manualmente a cada portal: las actualizaciones son automáticas / a un clic.

**Cómo lo hacemos hoy y hacia dónde vamos:**

| Banco | Hoy | Hacia dónde vamos |
|---|---|---|
| Banesco | Scraper | **API en tiempo real** (en hoja de ruta) |
| Banco de Venezuela | Scraper | **API en tiempo real** (en hoja de ruta) |
| BNC | **API en tiempo real** (ya disponible, 24/7) | — |
| Banco Exterior | Scraper | **API en tiempo real** (en hoja de ruta) |
| Mercantil | Scraper | Sin API en tiempo real disponible → **seguimos con scraper** |
| Provincial | Scraper | Sin API en tiempo real disponible → **seguimos con scraper** |

**Cómo lo posicionamos hoy:** arrancamos con **scrapers para todos los bancos VE** — funciona desde el día uno y cubre el 100% de la cobertura bancaria que necesitan. En paralelo migramos a **APIs en tiempo real** con **Banesco, Banco de Venezuela, BNC (ya) y Banco Exterior**, que son más estables. **Mercantil y Provincial no ofrecen API en tiempo real**, así que se quedan con el scraper.

> Esto cierra una de las razones por las que se cayó el piloto anterior: ahora hay **cobertura completa de banca venezolana** y la conexión no exige entrar manualmente a cada portal.

### 3.2 Integración con el sistema interno (SCI / Odoo)

Tesote carga automáticamente el **libro banco** al sistema de Veconinter vía **API**, eliminando el descargue + carga manual de plantillas de ingresos — que hoy es donde se va la mayor cantidad de horas del equipo.

- Conexión vía API directa al SCI / Odoo.
- La conciliación operativa↔financiera (match por **número de referencia**) se mantiene; Tesote alimenta la data, el SCI hace el match.

> **Caveat importante a transparentar:** la data que cargamos en tiempo real **no es data "certificada"** — los movimientos pueden cambiar/ajustarse en **T-1** (cierre del día siguiente). Sirve para operar y confirmar ingresos en el momento, pero el dato definitivo se concilia contra el cierre. Hay que dejar claro cómo manejan ustedes esa distinción internamente.

### 3.3 Categorías, contrapartes y reporte intradía

- **Categorización automática** de transacciones y reconocimiento de **contrapartes** (quién paga / a quién se paga), que se va afinando con el uso.
- **Reporte intradía:** dado que el equipo corre el flujo de caja **3 veces al día como mínimo (hasta 6–7)**, el reporte intradía mostraría la **posición bancaria consolidada al momento**, con desglose por tipo de ingreso y tipo de egreso (proveedores, reembolsos, intercompañía, etc.) — reemplazando el Excel que reconstruyen manualmente varias veces al día.

> **Por definir con Bertha:** estructura ideal del reporte (dimensiones: sociedad, moneda, tipo de ingreso/egreso) y la **posición consolidada del grupo en USD**.

### 3.4 Botón de Pagos (cobros) — por validar

Tesote tiene una función de **Botón de Pago** para cobros: permite que los clientes/consignatarios paguen de forma digital y que el ingreso se confirme automáticamente, en lugar de verificar manualmente cada pago entrante.

> **Preguntas a validar hoy:**
> - ¿Es el Botón de Pago una opción para Veconinter, dado su modelo de cobranza?
> - **¿Cómo pagan hoy sus clientes / consignatarios?** (transferencia, depósito, etc.)
> - Si los cobros entran por canales que podemos instrumentar con el Botón, esto ataca directamente su SLA de confirmación de 15–20 min.

### 3.5 Pagos salientes — por validar volumen

Tesorería controla todos los **débitos/pagos**. Tesote puede ejecutar pagos, pero su utilidad depende del volumen.

> **Pregunta a validar hoy:** **¿Cuántos pagos corren al día / a la semana?** Con eso evaluamos si la función de pagos aporta valor real o si la dejamos para una fase posterior.

---

## 4. Frecuencia de actualización (punto técnico clave)

La necesidad de Veconinter es alta: corren flujo de caja **3–7 veces al día** y entran **cada hora** a los bancos de alto movimiento. Hay que alinear expectativas por banco:

- **Scraper (conexión a portal):** disponible las 24 horas, frecuencia alta, pero algo menos estable.
- **API en tiempo real:** más estable, pero algunos bancos imponen **límites de frecuencia** (ej. ciertas APIs limitan a 1–3 actualizaciones/día; BNC es ilimitado 24/7).

> **A acordar hoy:** estrategia por banco (scraper vs. API) para los de alto movimiento — **Banesco, Mercantil, Provincial** especialmente — de modo que la cadencia que necesitan no se vea como una sorpresa más adelante.

---

## 5. Tipo de cambio (FX)

Veconinter consolida en USD a la **tasa a la que efectivamente acceden a dólares** (no BCV/oficial), distinta por mercado y definida manualmente, para **reporting interno**.

> **A confirmar hoy:** Tesote permite **override manual de tasa** por moneda/reporte para la consolidación interna. Definir qué monedas y qué tasas.

---

## 6. Preguntas abiertas para hoy

1. ¿Está completa la **plantilla de inventario de cuentas**? (cierra el alcance de Fase 1)
2. **Formato exacto** que ingiere el SCI hoy (columnas, estructura) — ¿la carga es vía Odoo o sistema aparte?
3. **Cadencia requerida por banco** vs. nuestros límites — ¿algún punto que sea no-negociable?
4. **Estructura ideal del reporte** de flujo de caja (Bertha): dimensiones y consolidado USD.
5. **Override de FX manual:** ¿qué monedas, qué tasas?
6. **Botón de Pago:** ¿aplica? ¿Cómo pagan hoy sus clientes?
7. **Volumen de pagos** diario/semanal.
8. ¿Quién aprueba y cuál es la realidad de presupuesto/tiempos en este ciclo?

---

## 7. Fases (propuesta)

- **Fase 1 — Venezuela:** 13 cuentas VE + Facebank + Mercantil Panamá. Scrapers para todos; migración progresiva a API tiempo real (Banesco, Banco de Venezuela, BNC, Banco Exterior). Integración de carga automática al SCI/Odoo. Reporte intradía + categorías/contrapartes.
- **Fase 1.5 (según validación):** Botón de Pago para cobros y/o ejecución de pagos salientes, según volumen.
- **Fase 2 — Estados Unidos y demás mercados:** stack US (TD Bank y subcuentas, Stripe/Interusa) y mercados adicionales según disponibilidad de API/archivo por banco.
