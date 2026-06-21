---
title: Integración Tesote × SAP — propuesta técnica fasada para La Sante
tags: [sales, client, la-sante, sap, scoping, client-facing]
updated: 2026-06-09
status: draft
---

# Integración Tesote × SAP — La Sante

**Propuesta técnica fasada.** Tesote entrega los movimientos bancarios consolidados de todas las cuentas de La Sante directamente en SAP, en formato estándar de extracto bancario electrónico. El alcance se fasea alrededor de la migración planificada a SAP S/4HANA de octubre 2026: arrancamos sin tocar SAP sobre el sistema actual (MT940) y evolucionamos a integración automática con el estándar moderno (CAMT.053 / ISO 20022) sobre el sistema nuevo.

---

## 1. Punto de partida

| Tema | Estado actual |
|---|---|
| ERP actual | **SAP R/3 EHP7 for SAP ERP 6.0** (ECC 6.0 EHP7), on-premise |
| Migración planificada | **SAP S/4HANA — octubre 2026** |
| Dirección del flujo | **Solo escritura** (push). Tesote entrega movimientos a SAP; no leemos ni conciliamos dentro de SAP. |
| Formato de entrega | **MT940** sobre ECC 6.0 (Fase 1) · **CAMT.053 / ISO 20022 XML** sobre S/4HANA (Fase 2) |
| Mecanismo de carga (hoy) | Transacción **FF.5** (importación de extracto bancario electrónico) — manual, ejecutada por el equipo de La Sante |

**Por qué cambiamos de formato al migrar.** Sobre ECC 6.0, MT940 es el formato nativo, simple y de cero configuración para FF.5 — perfecto para arrancar ya. Sobre S/4HANA aprovechamos la migración para pasar al estándar moderno **CAMT.053 (ISO 20022 XML)**, que SAP soporta nativamente y que transporta datos estructurados mucho más ricos (contraparte, referencias, información de remesa) que el campo de texto libre `:86:` de MT940. El pipeline de datos subyacente es el mismo: no rehacemos la captura ni la lógica de Tesote, solo cambia la serialización del archivo de salida — MT940 hoy, CAMT.053 después.

**Un solo archivo para todas las cuentas — en ambos formatos.** Tanto MT940 (multi-extracto, cada cuenta delimitada por su etiqueta `:25:`) como CAMT.053 (múltiples bloques `<Stmt>` por archivo) permiten consolidar todas las cuentas y bancos en **un único archivo**. La Sante carga un solo archivo, no uno por banco. Requisito previo (lado SAP, una sola vez): que cada cuenta exista como cuenta de banco de la casa (*house bank account*) en SAP y que estén configuradas las reglas de posteo / mapeo de códigos de transacción.

---

## 2. Las fases (alineadas a la migración de octubre)

| | **Fase 1 — Archivo MT940 (ECC 6.0, ahora)** | **Fase 2 — Push automático (S/4HANA, post-octubre)** |
|---|---|---|
| Qué hace Tesote | Genera un **MT940** consolidado de todas las cuentas y lo entrega (correo / SFTP) | Genera un **CAMT.053 (ISO 20022)** consolidado y lo envía automáticamente al tenant productivo de S/4HANA |
| Carga en SAP | **Manual** — el equipo de La Sante importa vía FF.5 | **Automática** — vía `API_BANKSTATEMENT_SRV` |
| Cambio / desarrollo en SAP | **Ninguno** | Habilitar Communication Scenario `SAP_COM_0316` + OAuth 2.0 |
| Conectividad | Solo entrega de archivo (correo / SFTP) | API sobre el tenant S/4HANA |
| Licenciamiento SAP | **Sin exposición** — carga mediada por humano, no es acceso indirecto | A validar según contrato S/4HANA |
| Esfuerzo Tesote | Bajo — reuso del generador MT940 existente | Bajo — mismo archivo, cambia el transporte |
| Esfuerzo La Sante | Configurar house banks + reglas FF.5 (una vez); ejecutar carga | Habilitar escenario de comunicación + OAuth con su partner SAP |

**Lógica de la secuencia.** La Sante migra a S/4HANA en octubre. No tiene sentido construir plomería profunda (RFC/BAPI/IDoc) sobre ECC 6.0 que se desecha en cuatro meses. La Fase 1 los pone en producción **ya**, sin tocar SAP y sin riesgo de licenciamiento, sobre el sistema que están a punto de dejar. La Fase 2 aprovecha que S/4HANA expone una API limpia y el estándar moderno ISO 20022 — la migración no rompe la integración, la habilita y la mejora.

---

## 3. Recomendaciones técnicas (sujetas a validación)

| Tema | Recomendación |
|---|---|
| Formato | **MT940** en Fase 1 (ECC, nativo, cero configuración). **CAMT.053 / ISO 20022 XML** en Fase 2 (S/4HANA, estándar moderno, datos estructurados ricos). |
| Carga Fase 1 | Transacción **FF.5** (importación EBS), ejecutada por La Sante. Cero desarrollos. |
| Entrega Fase 1 | Tesote → correo o SFTP → bandeja de La Sante, un archivo consolidado. |
| Integración Fase 2 | `API_BANKSTATEMENT_SRV` + `SAP_COM_0316` + OAuth 2.0 sobre S/4HANA. |
| Enriquecimiento de datos | En Fase 1 (MT940) estructuramos el campo de detalle `:86:` con contraparte / referencia. En Fase 2 (CAMT.053) ese enriquecimiento es **nativo**: campos estructurados para contraparte, referencias y remesa → mejor auto-posteo y conciliación que con MT940. |

---

## 4. Pendientes a confirmar

- **Cuentas y bancos en alcance** — inventario de cuentas a consolidar en el MT940.
- **House banks en SAP** — confirmar que cada cuenta está dada de alta como cuenta de banco de la casa en ECC (prerrequisito de la carga FF.5).
- **Reglas de posteo / mapeo de códigos de transacción** — configuración EBS existente en ECC; quién la mantiene del lado SAP.
- **Cadencia de entrega** — ¿una entrega diaria al cierre, varias intradía?
- **Fecha firme de migración a S/4HANA** — para fijar el corte Fase 1 → Fase 2.
- **Partner SAP de La Sante** — quién acompaña la migración y habilitaría `SAP_COM_0316` + OAuth en Fase 2.
- **Convención de nombres** del archivo / asunto del correo, si la carga se dispara por bandeja.

---

## 5. Nota comercial (interna)

- Vender como **entregable gestionado recurrente**, no como build único. Tesote genera el archivo cada período; el costo marginal por archivo es casi cero, el valor para el cliente es continuo. Precio recurrente.
- **Fase 1 = deal sustancial con esfuerzo bajo:** reusamos el generador MT940 ya existente (CAPCA / Ron Santa Teresa), cero desarrollo SAP, carga manual del cliente. Se cierra rápido.
- **Fase 2 = upsell natural post-octubre:** sobre S/4HANA la integración automática es fácil (API nativa, ISO 20022). El pipeline de datos de Fase 1 se reutiliza; solo cambia el formato de salida (MT940 → CAMT.053).
- **No es one-off:** otros clientes tienen setups SAP similares → este patrón (archivo consolidado, manual ahora / API después; MT940 en ECC, CAMT.053 en S/4HANA) es producto reutilizable para la cohorte SAP, no trabajo a medida.

---

*Borrador inicial — 2026-06-09. Modelado sobre la propuesta SAP de Ron Santa Teresa y el blueprint CAPCA. Cualquier ajuste de alcance/fases se refleja en la propuesta comercial final.*
