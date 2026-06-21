---
title: "Blueprint Operativo: CAPCA × Tesote"
tags: [blueprint, capca, implementation, sap]
updated: 2026-04-13
author: Tesote
version: "1.0"
status: draft
---

# Blueprint del Proyecto
**CAPCA × Tesote**
*Versión 1.0 — Abril 2026*

---

| Campo | Detalle |
|---|---|
| **Ejecutivo de cuenta** | Nicolás Rossini |
| **Correo electrónico** | nicolas.rossini@tesote.com |
| **Teléfono** | — |
| **Fecha de llamada introductoria** | Marzo 2026 |
| **Fecha de llamada de discovery** | Marzo 2026 |
| **Fecha estimada de cierre** | Por confirmar |

---

> Este documento constituye la referencia compartida del compromiso entre Central Azucarero Portuguesa C.A. (CAPCA) y Tesote. Recoge el contexto operativo, los puntos de dolor, los casos de uso y el alcance de implementación acordados entre ambas partes. Es un documento vivo — actualizado a lo largo del proceso y validado por ambas partes antes del inicio de la implementación.

---

## 1. Perfil de la Empresa

| Campo | Detalle |
|---|---|
| **Industria / Sector** | Agroindustrial / Sector azucarero |
| **Entidades legales en alcance** | 1 entidad legal (CAPCA); dos sedes operativas: Portuguesa (Acarigua) y Caracas |
| **Países de operación** | Venezuela · Panamá · Estados Unidos · Curazao |
| **Sitio web** | Por confirmar |

**Descripción:** Central Azucarero Portuguesa C.A. (CAPCA) es una empresa venezolana del sector agroindustrial azucarero con sede operativa en Portuguesa (Acarigua) y sede administrativa en Caracas, que gestiona 41 cuentas bancarias en 16 bancos nacionales e internacionales con un volumen de aproximadamente 2.665 transacciones mensuales. CAPCA forma parte del Grupo Cisneros / OCAAT (Organización Cisneros Asesores), con sede corporativa en Caracas. Las decisiones de contratos y gastos significativos requieren aprobación de OCAAT.

---

## 2. Contexto Operativo Actual

CAPCA opera su gestión financiera y bancaria sobre SAP S/4HANA Cloud, un ERP de última generación en la nube. Sin embargo, el proceso de conectividad bancaria es enteramente manual: el equipo de tesorería accede diariamente a los portales de 16 bancos para descargar extractos, los cuales son cargados manualmente a SAP. El tipo de cambio BCV se actualiza también de forma manual en SAP cada día.

La empresa tiene dos dinámicas operativas diferenciadas: Acarigua realiza conciliación bancaria operativa semanal, y Caracas realiza conciliación contable mensual. Esta separación requiere filtrar manualmente información confidencial en Excel antes de distribuirla entre sedes. Adicionalmente, la identificación de pagos de clientes y su asociación a facturas en el módulo FI-AR de SAP se realiza 100% manualmente.

**Ciclo operativo semanal ("situado"):** El flujo de caja sigue un ciclo fijo: el jueves se planifica el presupuesto de caja para la semana siguiente → el lunes OCAAT deposita los fondos en las cuentas de CAPCA → martes y jueves se ejecutan los pagos a cañicultores (agricultores proveedores de caña de azúcar). Yolimar Ortiz coordina la operación de pagos desde Acarigua.

**Evento detonador:** SAP S/4HANA Cloud entró en producción el 9 de marzo de 2026. El socio implementador (Sofos Corp) dejó la extracción bancaria automática y la automatización del tipo de cambio BCV en el backlog post-Go Live por restricciones de tiempo. Esto dejó a CAPCA en producción SAP el día 1 con una operación bancaria 100% manual. Tesote cierra exactamente esa brecha.

---

## 3. Puntos de Dolor y Motivadores Estratégicos

| # | Punto de Dolor | Impacto en el Negocio |
|---|---|---|
| 1 | **Descargas manuales de extractos bancarios** — el equipo accede diariamente a 16 portales bancarios distintos para descargar extractos individualmente | Tiempo operativo perdido a diario; dependencia de personas; riesgo de error o datos incompletos por fallas de portales |
| 2 | **Carga manual de extractos a SAP** — los extractos descargados se cargan manualmente al ERP sin ninguna automatización | Proceso lento, propenso a errores y sin trazabilidad automática en un sistema productivo en la nube |
| 3 | **Actualización manual del tipo de cambio BCV** — la tasa diaria del BCV se actualiza manualmente en SAP todos los días; el BCV publica la tasa después de las 3pm, lo que presiona al equipo de cierre | Riesgo de error con impacto contable directo en el ERP; carga operativa diaria recurrente; ventana estrecha de actualización |
| 4 | **Filtrado manual de información confidencial entre sedes** — la información bancaria debe filtrarse en Excel antes de distribuirse entre Caracas y Acarigua según el rol de cada equipo | Proceso frágil y dependiente de personas; riesgo de exposición de datos sensibles |
| 5 | **Identificación manual de pagos de clientes** — los cobros no se asocian automáticamente a las facturas abiertas en FI-AR de SAP | Ciclo de cobro lento; riesgo de error en liquidación; capacidad del equipo de cobranzas limitada por el proceso manual |
| 6 | **Riesgo de cumplimiento en pagos a terceros** — los pagos a cañicultores y proveedores deben documentarse correctamente; un incidente previo con la Fiscalía evidenció la necesidad de trazabilidad y control de pagos | Exposición regulatoria; riesgo reputacional; necesidad de respaldo documental ante cualquier requerimiento de autoridad |

---

## 4. Aplicación por Área

*Cómo Tesote se integra en la operación de cada equipo dentro de CAPCA. Cada elemento referencia una capacidad del alcance (sección 7.1).*

### Tesorería (Acarigua — Yolimar Ortiz)

- Saldos en tiempo real de todas las cuentas sin acceder a portales bancarios — visibilidad consolidada por banco, moneda y sede
- Disponibilidad bancaria actualizada para planificación del situado semanal
- Sincronizaciones automáticas programadas + a demanda — elimina la descarga manual de extractos de 16 portales
- Automatización de token 2FA para bancos que lo requieran

### Cobranzas (Acarigua — equipo de ventas)

- Identificación automática de pagos de clientes vía matching de RIF y reglas de contraparte
- Marcado de pagos de terceros (sin RIF de cliente) para revisión manual de cumplimiento
- Identificación y registro global de pagos y cobros en SAP — matching FI-AR con facturas abiertas *(Fase 2)*

### Contabilidad / Finanzas (Caracas + Acarigua — Leandro Zapata)

- Envío automático de extractos a SAP S/4HANA Cloud en formato MT940 — sin carga manual
- Automatización del tipo de cambio BCV diario en SAP — sin entrada manual después de las 3pm
- Mapeo de cuentas contables (GL) vinculado al banco de la casa y códigos de transacción SAP

### OCAAT / Corporativo (Caracas)

- Segmentación de confidencialidad — permisos granulares Caracas vs. Acarigua; cada sede ve solo lo que le corresponde; elimina el filtrado manual en Excel
- Visibilidad multi-moneda consolidada (Bs, USD, EUR)
- Roles de usuario y controles de acceso delegados a CAPCA

### Futuro

- Portal de pagos / link de pago para clientes — integrado con SAP para operaciones de tesorería *(Fase 3, en evaluación)*

---

## 5. Infraestructura Bancaria

### 5.1 Cuentas Bancarias en Alcance

*Inventario recibido en abril 2026. CAPCA tiene 41 cuentas en 16 bancos en Venezuela, Panamá, EE.UU. y Curazao. Toda la conectividad bancaria con cobertura Tesote disponible se implementa en la Fase 1. Para JPMorgan y Bank of America ML, la decisión de conectarlos en esta primera fase queda a criterio de OCAAT.*

| Banco | País | Monedas | Cuentas | Conexión Tesote | Prioridad Fase 1 |
|---|---|---|---|---|---|
| BBVA Provincial | Venezuela | Bs, USD | 8 | ✅ Conexión Directa | Alta — ~1.040 tx/mes |
| Banesco Banco Universal | Venezuela | Bs, USD, EUR | 5 | ✅ Conexión Directa | Alta — ~1.250 tx/mes |
| BNC | Venezuela | Bs, USD, EUR | 6 | ✅ Conexión Directa | Alta — ~300 tx/mes |
| Banco de Venezuela | Venezuela | Bs, USD | 3 | ✅ Conexión Directa | Baja — Sin movimientos activos |
| Bancaribe | Venezuela | Bs, USD | 2 | ✅ Conexión Directa | Baja — Mínimo movimiento |
| Banco Plaza | Venezuela | Bs, USD | 2 | ✅ Conexión Directa | Baja — Mínimo movimiento |
| Del Sur | Venezuela | Bs | 2 | ❓ Por confirmar | Baja — Sin/mínimo movimiento |
| Banco del Tesoro | Venezuela | Bs | 1 | ✅ Conexión Directa | Baja — Mínimo movimiento |
| Bancamiga | Venezuela | Bs | 1 | ✅ Conexión Directa | Baja — Mínimo movimiento |
| Banesco Panamá | Panamá | USD | 1 | ✅ Conexión Directa | Media — ~20 mov/mes |
| Banesco USA | EE.UU. | USD | 1 | ❓ Por confirmar | Media — ~20 mov/mes |
| Banesco Cta Ahorro | — | USD | 1 | ✅ Conexión Directa | Media — ~5 mov/mes |
| BNC Curazao | Curazao | USD | 1 | ❌ No disponible | Baja — Sin movimientos activos |
| BNC Puerto Rico | Puerto Rico | USD | 1 | ❌ No disponible | Baja — Sin movimientos activos |
| JPMorgan | EE.UU. | USD, Multidivisa | 5 | ✅ Conexión Directa | Media — ~5 mov/mes c/u |
| Bank of America ML | EE.UU. | USD | 1 | ✅ Conexión Directa | Media — ~5 mov/mes |

> **Cuentas de Alta prioridad (Fase 1):** 11 cuentas en BBVA Provincial, Banesco BU y BNC — concentran aproximadamente 2.590 transacciones mensuales (~97% del volumen total).
>
> **Bancos internacionales:** JPMorgan y Bank of America ML están disponibles en el registro de Tesote. Queda a decisión de OCAAT si conectarlos en esta primera fase. BNC Curazao y BNC Puerto Rico no están disponibles actualmente. Banesco USA y Del Sur están por confirmar.

---

## 6. Sistemas y Integración ERP

| Sistema | Proveedor | Versión | Despliegue | Tipo de Integración | Notas |
|---|---|---|---|---|---|
| **ERP** | SAP | S/4HANA Cloud | `Nube` | `Estándar` — integración nativa vía OData | API_BANKSTATEMENT_SRV · Communication Scenario SAP_COM_0316 · OAuth 2.0 · formato MT940 |

**Partner SAP (implementador):** Sofos Corp (sofoscorp.com) — implementó el SAP S/4HANA Cloud de CAPCA con Go Live el 9 de marzo de 2026. Contactos Sofos en el proyecto: Katiuska Andrade, Blanca Lozada, José Sánchez. Arnaldo Parra es el consultor SAP interno de CAPCA (punto de contacto técnico para la configuración del tenant). Sofos confirmó que el formato soportado para bank statements en el tenant de CAPCA es **MT940**.

**Arquitectura de integración SAP S/4HANA Cloud:**
- Tesote genera los bank statements en **formato MT940** y los envía al tenant productivo de CAPCA mediante `API_BANKSTATEMENT_SRV`.
- La integración requiere que el Communication Scenario `SAP_COM_0316` esté habilitado en el tenant — confirmación pendiente con Arnaldo Parra y Sofos.
- La autenticación entre Tesote y SAP se realiza mediante OAuth 2.0.

**Automatización del tipo de cambio BCV — tres opciones (a definir con equipo TI y partner SAP):**
1. **OData directo** — Tesote escribe la tasa directamente via `API_EXCHANGERATE_SRV`. Opción más simple; requiere permiso de escritura en el tenant.
2. **SAP CPI (Cloud Platform Integration)** — Tesote publica la tasa en un endpoint CPI que la inyecta en SAP. Para entornos con restricciones de escritura directa.
3. **Market Rates Management** — Módulo SAP para gestión centralizada de tasas de mercado. Mayor control desde SAP; requiere configuración adicional en el ERP.

**Mapeo de cuentas contables (GL):** A definir durante el onboarding de implementación. CAPCA deberá proveer el banco de la casa y los códigos de transacción SAP como prerrequisito.

---

## 7. Definición de Alcance

### 7.1 Alcance

*Todo lo que Tesote entregará como parte de este compromiso. Esta es la lista maestra — cada entregable aparece aquí.*

| # | Capacidad | Tipo | Fase | Notas |
|---|---|---|---|---|
| 1 | Conectividad bancaria — BBVA Provincial, Banesco BU, BNC | `Nativo` | 1 | 11 cuentas · ~2.590 tx/mes · núcleo operativo |
| 2 | Conectividad bancaria — Bancaribe, Banco Plaza, Banco del Tesoro, Bancamiga, Banco de Venezuela | `Nativo` | 1 | Conexión Directa disponible |
| 3 | Conectividad bancaria — Banesco Panamá | `Nativo` | 1 | Conexión Directa disponible |
| 4 | Saldos bancarios en tiempo real (actualización ≥1x por día) | `Nativo` | 1 | Disponible desde primera hora sin acceso manual a portales |
| 5 | Movimientos bancarios T+0 y T+1 (actualización ≥1x por día) | `Nativo` | 1 | Sincronización automática programada + sincronizaciones manuales a demanda |
| 6 | Envío automático de extractos a SAP S/4HANA Cloud | `Desarrollo especial` | 1 | Ver 7.2 #1 — Via API_BANKSTATEMENT_SRV + SAP_COM_0316; formato MT940 |
| 7 | Automatización de tipo de cambio BCV diario en SAP | `Desarrollo especial` | 1 | Ver 7.2 #2 — Tres opciones de escritura a definir con equipo TI y partner SAP |
| 8 | Reglas de categorización y contraparte | `Configuración` | 1 | Parametrización de reglas por banco para asociación automática de movimientos |
| 9 | Marcado de pagos de terceros | `Desarrollo especial` | 1 | Ver 7.2 #3 — Motor de reglas + contraparte; crítico para cumplimiento |
| 10 | Roles de usuario, controles de acceso y segmentación de confidencialidad | `Nativo` | 1 | Permisos granulares Caracas vs. Acarigua; administración delegada a CAPCA; elimina filtrado manual en Excel |
| 11 | Soporte multi-moneda — Bs, USD, EUR, Multidivisa | `Nativo` | 1 | Según disponibilidad por banco y cuenta |
| 12 | Mapeo de cuentas contables (GL) | `Configuración` | 1 | Requiere banco de la casa + códigos de transacción SAP como prerrequisito |
| 13 | Automatización de token 2FA | `Nativo` | 1 | Aplicable a bancos con token — a verificar por banco |
| 14 | Sincronizaciones programadas | `Nativo` | 1 | Hasta 3 sincronizaciones automáticas diarias + sincronizaciones manuales a demanda |
| 15 | Identificación de pagos de clientes + matching FI-AR en SAP | `Desarrollo especial` | 2 | Ver 7.2 #4 — Objetivo no negociable de Claudia Cisneros |
| 16 | Portal de pagos / link de pago para clientes | `Desarrollo especial` | 3 | Ver 7.2 #5 — Link BNC en beta |

> **Definiciones de tipo:**
> - **Nativo** — Capacidad estándar de la plataforma. Sin esfuerzo de ingeniería adicional.
> - **Configuración** — Disponible en la plataforma pero requiere configuración específica del cliente (reglas, mapeos, permisos).
> - **Desarrollo especial** — Requiere scoping y desarrollo de ingeniería. Ver 7.2 para detalle.

### 7.2 Funcionalidades Especiales o Integraciones

*Detalle expandido de los elementos marcados como `Desarrollo especial` en 7.1. Cada elemento requiere validación con el equipo de producto e ingeniería antes de comprometerse contractualmente.*

| # | Ref 7.1 | Funcionalidad / Integración | Descripción | Estado | Notas |
|---|---|---|---|---|---|
| 1 | #6 | Envío automático de extractos a SAP S/4HANA Cloud | Tesote genera extractos bancarios en formato MT940 y los envía a SAP vía API_BANKSTATEMENT_SRV + SAP_COM_0316; autenticación OAuth 2.0 | `En evaluación` | Requiere SAP_COM_0316 habilitado en tenant — pendiente confirmación con Arnaldo Parra + Sofos |
| 2 | #7 | Automatización de tipo de cambio BCV diario en SAP | Ingesta automática de la tasa BCV diaria y publicación en SAP; tres vías de escritura en evaluación (OData directo, SAP CPI, Market Rates Management) | `En evaluación` | Vía de escritura a definir con equipo TI y partner SAP (Sofos) |
| 3 | #9 | Marcado de pagos de terceros | Motor de reglas para identificar y marcar pagos desde cuentas de terceros donde el RIF del ordenante no coincide con el maestro de clientes; marca para revisión manual de cumplimiento | `En evaluación` | Crítico para cumplimiento; requiere configuración de reglas de contraparte por banco |
| 4 | #15 | Identificación de pagos de clientes + matching FI-AR en SAP | Identificación automática de pagos de clientes y emparejamiento con facturas abiertas en FI-AR de SAP; liquidación automatizada de cobranzas | `En evaluación` | Naming: "Identificación y registro global de pagos y cobros en SAP". Objetivo no negociable de Claudia Cisneros. |
| 5 | #16 | Portal de pagos / link de pago para clientes | Módulo de iniciación de pagos integrado con SAP para operaciones de tesorería | `En evaluación` | Link de pago BNC en beta; clientes no necesitan ser usuarios de Tesote |

### 7.3 Automatizaciones de Flujo de Trabajo

*Especificación estructurada de los elementos de automatización en 7.1. Requiere scoping de ingeniería antes de comprometerse contractualmente.*

| # | Ref 7.1 | Automatización | Método de Pago | Fuente de Datos | Objeto | Alcance | Frecuencia | Estado |
|---|---|---|---|---|---|---|---|---|
| 1 | #15 | Identificación y liquidación de pagos de clientes | Transferencia / Pago Móvil / Otro | Movimientos bancarios Tesote | FI-AR — Facturas abiertas | CAPCA (Caracas + Acarigua) | Diaria | `Por validar` |

> **Nota de alcance:** La automatización FI-AR requiere scoping con el equipo de producto antes de comprometerse contractualmente. Confirmar viabilidad técnica, nivel de configuración y si aplica carga de maestro de clientes como prerrequisito.

### 7.4 Pendiente de Definición

| # | Elemento | Estado | Responsable |
|---|---|---|---|
| | | | |

---

## 8. Plan de Implementación

### 8.1 Fases

| Fase | Alcance | Responsable (Tesote) | Responsable (Cliente) | Inicio Estimado | Go-Live Estimado |
|---|---|---|---|---|---|
| **Fase 1 — Hub bancario + SAP + BCV** | Conexiones bancarias (todas las cuentas con cobertura Tesote disponible), saldos y movimientos en tiempo real, envío automático de extractos a SAP S/4HANA Cloud (MT940), automatización tasa BCV diaria, segmentación Caracas / Acarigua | Nicolás Rossini | Gheorly Cohil + Arnaldo Parra | Post-firma | ~12 semanas post-arranque |
| **Fase 2 — Identificación y registro global de pagos y cobros en SAP** | Identificación automática de pagos de clientes, emparejamiento con facturas abiertas FI-AR en SAP, liquidación automatizada de cobranzas | Nicolás Rossini | Gheorly Cohil + Leandro Zapata | Post Go-Live Fase 1 | Por definir post-scoping |
| **Fase 3 — Portal de pagos** | Módulo de iniciación de pagos integrado con SAP para operaciones de tesorería | Por definir | Por definir | En evaluación | Por definir |

---

## 9. Puntos Abiertos y Próximos Pasos

| # | Acción | Responsable |
|---|---|---|
| 1 | **Revisión Legal y Administrativa:** Proceso de revisión legal del contrato y la gestión de los pagos correspondientes para formalizar el compromiso. | CAPCA / OCAAT |
| 2 | **Cronograma Detallado de la Fase 1:** Necesitamos definir en conjunto las fechas específicas de inicio y fin para cada uno de los hitos que componen la Fase 1, asegurando que el flujo de carga de extractos y actualización del BCV esté operativo según lo previsto. | Ambas partes |
| 3 | **Alineación Técnica con Partner SAP:** Proponemos coordinar una sesión de alineación técnica con nuestro partner de SAP para validar la arquitectura y los puntos pendientes mencionados en su documento (APIs, comunicación en el tenant y configuración de banco de la casa). | Ambas partes + Sofos |
| 4 | **Definición de Alcance Fases 2 y 3:** Quedamos atentos a la entrega de los tiempos estimados para estas fases, lo cual nos permitirá tener la hoja de ruta completa del proyecto. | CAPCA / OCAAT |

---

## Historial del Documento

| Versión | Fecha | Autor | Resumen de Cambios |
|---|---|---|---|
| 0.1 | Marzo 2026 | Tesote | Borrador inicial — post llamada introductoria |
| 0.2 | Marzo 2026 | Tesote | Actualizado post discovery — casos de uso confirmados, integración SAP S/4HANA Cloud documentada, plan de fases definido |
| 1.0 | Abril 2026 | Tesote | Versión completa — inventario bancario (41 cuentas, 16 bancos), cobertura Tesote mapeada, Sofos Corp como partner SAP documentado, formato MT940 confirmado, OCAAT/Grupo Cisneros añadido, ciclo situado documentado, pendientes técnicos y comerciales actualizados |

---

*Elaborado por Tesote — Nicolás Rossini — Abril 2026*
*Para consultas o ajustes, contactar a nicolas.rossini@tesote.com*
