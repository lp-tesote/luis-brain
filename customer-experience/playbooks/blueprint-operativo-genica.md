---
title: "Blueprint del Proyecto — Alimentos Génica × Tesote"
tags: [blueprint, genica, sap, venezuela]
updated: 2026-04-15
notion_page_id: 3431ee04-eee1-8150-bf97-ebf1b91b57a5
notion_last_synced: "2026-04-15T20:00:00Z"
---

# Blueprint del Proyecto
**Alimentos Génica × Tesote**
*Versión 1.0 — 2026-04-15*

---

| Campo | Detalle |
|---|---|
| **Ejecutivo de cuenta** | Esteban Suárez |
| **Correo electrónico** | esteban.suarez@tesote.com |
| **Teléfono** | — |
| **Fecha de llamada introductoria** | 2026-03-27 |
| **Fecha de llamada de discovery** | 2026-04-10 |
| **Fecha estimada de cierre** | 2026-05-10 |

---

> Este documento constituye la referencia compartida del compromiso entre Alimentos Génica y Tesote. Recoge el contexto operativo, los puntos de dolor, los casos de uso y el alcance de implementación acordados entre ambas partes. Es un documento vivo — actualizado a lo largo del proceso y validado por ambas partes antes del inicio de la implementación.

---

## 1. Perfil de la Empresa

| Campo | Detalle |
|---|---|
| **Industria / Sector** | Manufactura de Alimentos |
| **Entidades legales en alcance** | Por confirmar — múltiples entidades mencionadas (incluye cuentas custodio) |
| **Países de operación** | Venezuela + cuentas internacionales (Panamá, EE.UU., otros) |
| **Sitio web** | genica.com.ve |

**Descripción:** Alimentos Génica es una empresa venezolana del sector de manufactura de alimentos con operaciones financieras complejas que incluyen múltiples entidades, entre 25 y 30 cuentas bancarias nacionales (sin contar cuentas custodio y electrónicas), y cuentas internacionales, gestionando aproximadamente 5.000 transacciones mensuales.

---

## 2. Contexto Operativo Actual

Alimentos Génica opera con entre 25 y 30 cuentas bancarias nacionales, más cuentas custodio, electrónicas y en el exterior (Panamá, EE.UU.). El equipo de finanzas gestiona actualmente la descarga manual diaria de extractos bancarios desde múltiples portales, los cuales son cargados posteriormente a SAP para conciliación. Anaura Prieto confirmó que el 95% de las cargas en SAP ya están automatizadas internamente, pero la extracción inicial de datos desde los bancos continúa siendo un proceso manual que consume al menos una hora diaria y está expuesto a errores por caídas de portales y cambios en códigos bancarios. José Boscán señaló que este proceso manual existe desde 2018, cuando comenzaron a gestionar pagos y cobros en su forma actual.

---

## 3. Puntos de Dolor y Motivadores Estratégicos

| # | Punto de Dolor | Impacto en el Negocio |
|---|---|---|
| 1 | **Descarga manual diaria de extractos bancarios** — una persona dedica mínimo 1 hora al día a acceder a múltiples portales bancarios y descargar extractos | Tiempo operativo perdido, dependencia de una persona, riesgo de error humano en el proceso de carga a SAP |
| 2 | **Códigos bancarios nuevos no registrados en SAP** — cuando un banco introduce un código nuevo, la carga automática a SAP falla hasta que el equipo IT actualiza el código en el sistema | Interrupciones en el proceso de carga, necesidad de resolución manual urgente, exposición a cierres del día incompletos |
| 3 | **Caídas y errores en portales bancarios** — los extractos descargados pueden contener datos incompletos o incorrectos (RIF truncados, referencias erróneas) por inconsistencias en los portales | Errores en la conciliación, retrabajos, cargas incorrectas en SAP que deben corregirse manualmente |

**Evento detonador:** Aunque no se identificó un evento de transformación inmediato como una migración de ERP, el equipo de Génica lleva desde 2018 con este proceso manual y reconoce que la automatización es la evolución natural. La urgencia está impulsada por la escala actual del volumen de transacciones (~5.000 mensuales) y la voluntad del equipo de finanzas de liberar capacidad operativa para tareas de mayor valor.

---

## 4. Aplicación por Área

*Cómo Tesote se integra en la operación de cada equipo dentro de Génica. Cada elemento referencia una capacidad del alcance (sección 7.1).*

### Tesorería (Anaura Prieto)

- Saldos consolidados en tiempo real de todas las cuentas sin acceder a portales bancarios — elimina la revisión manual de saldos banco por banco a las 10am *(7.1 #3)*
- Sincronizaciones automáticas programadas (mañana, tarde, cierre) + a demanda — elimina la descarga manual de 1+ hora/día *(7.1 #4, #12)*
- Automatización de token 2FA para bancos que lo requieran *(7.1 #13)*
- Carga manual vía plantilla Excel para cajas principales y cuentas custodio sin integración bancaria *(7.1 #14)*

### Cobranza (Mileidy Hernández)

- Vista segmentada: el equipo de cobranza ve únicamente créditos (ingresos) — sin acceso a saldos ni débitos *(7.1 #11)*
- Identificación de pagos de clientes vía RIF y reglas de contraparte por banco *(7.1 #8)*
- Visibilidad directa de datos bancarios en Tesote como alternativa a esperar la carga en SAP

### Finanzas / Contabilidad (Dayana Faneitte, Alexandra Rodríguez, analistas)

- Envío automático de extractos a SAP en formato JSON — sin descarga ni carga manual *(7.1 #5)*
- Módulo de reconciliación valida integridad de datos antes del envío a SAP — alertas de discrepancias, errores y códigos no registrados *(7.1 #6, #7)*
- Movimientos categorizados (comisiones, pagos, cobros, transferencias) para reportes de flujo de caja *(7.1 #15)*
- Reglas por banco para resolver problemas de calidad de datos (RIF truncados, referencias erróneas, código 595 Provincial) *(7.1 #8)*

### Tecnología / IT (Leodardo Chacín, Juan García)

- Alertas en tiempo real cuando un banco introduce un código nuevo no registrado en SAP — habilita el proceso interno de registro (15–60 min) sin esperar descubrimiento manual *(7.1 #7)*
- Documentación de API para integración SAP — Tesote envía JSON, el equipo IT conecta a SAP *(7.1 #5)*
- Dos opciones de gestión de códigos: (1) registrar nuevo código en SAP, o (2) Tesote remapea vía motor de reglas *(7.1 #8)*

---

## 5. Infraestructura Bancaria

### 5.1 Cuentas Bancarias en Alcance

> **Inventario pendiente.** José Boscán se comprometió a enviar el listado completo de cuentas bancarias (empresas, bancos, tipos y número de cuentas). La información a continuación es el resumen confirmado en la llamada de discovery.

| Banco | País | Tipo de Cuenta | Entidad Legal | Nivel de Volumen | Notas |
|---|---|---|---|---|---|
| Por confirmar (múltiples) | Venezuela | Corriente / Ahorro | Por confirmar | `Alto` | 25–30 cuentas principales confirmadas; excluye cuentas custodio y electrónicas que multiplican el total real |
| Por confirmar | Panamá | Por confirmar | Por confirmar | Por confirmar | Cuentas internacionales mencionadas — detalle pendiente del inventario |
| Por confirmar | EE.UU. | Por confirmar | Por confirmar | Por confirmar | Cuentas internacionales mencionadas — detalle pendiente del inventario |

> **Nota de cobertura:** Una vez recibido el inventario, cada banco será verificado contra el registro activo de integraciones de Tesote. Los bancos venezolanos principales (BNC, Banesco, Mercantil, BBVA Provincial, Banco de Venezuela, Bancaribe, Bancamiga, y otros) están en el registro activo. Para bancos internacionales en Panamá (Banesco Panamá, Mercantil Panamá, Global Bank, Banistmo) y EE.UU. (Amerant), Tesote tiene cobertura confirmada. Cualquier banco fuera del registro será escalado al equipo de producto antes de comprometerse.

---

## 6. Sistemas y Integración ERP

| Sistema | Proveedor | Versión | Despliegue | Tipo de Integración | Notas |
|---|---|---|---|---|---|
| **ERP** | SAP | Por confirmar | Por confirmar (On-Premise típico) | `Estándar` | Integración nativa Tesote → SAP vía API; Tesote envía movimientos en formato JSON; conciliación final homologada en SAP |

**Mapeo de cuentas contables (GL):** A definir durante el onboarding de implementación. Génica deberá proveer el plan de cuentas SAP como prerrequisito.

> **Nota técnica:** El equipo de tecnología de Génica (liderado por Leodardo Chacín y Juan García) debe revisar la documentación de API y seguridad enviada por Tesote para validar el proceso de integración y definir los tiempos de respuesta para el registro de nuevos códigos bancarios en SAP.

---

## 7. Definición de Alcance

### 7.1 En Alcance

*Todo lo que Tesote entregará como parte de este compromiso. Esta es la lista maestra — cada entregable aparece aquí.*

| # | Capacidad | Tipo | Fase | Notas |
|---|---|---|---|---|
| 1 | Conectividad bancaria — bancos nacionales según inventario | `Nativo` | 1 | 25–30 cuentas nacionales confirmadas; cobertura a validar banco por banco contra registro activo post-inventario |
| 2 | Conectividad bancaria — bancos internacionales (Panamá, EE.UU.) | `Nativo` | 1 | A validar contra registro post-inventario |
| 3 | Saldos bancarios en tiempo real (actualización ≥1x por día) | `Nativo` | 1 | Disponible a primera hora sin acceso manual a portales |
| 4 | Movimientos bancarios T+0 y T+1 (actualización ≥1x por día) | `Nativo` | 1 | Sincronización automática programada + sincronizaciones manuales a demanda |
| 5 | Integración SAP vía API — envío de extractos en formato JSON | `Nativo` | 2 | Estándar nativo — envío a día muerto (T+1) recomendado para SAP |
| 6 | Validación automática de extractos y alertas de errores | `Nativo` | 1 | Módulo de reconciliación que alerta sobre discrepancias, datos corruptos y movimientos con códigos no registrados |
| 7 | Alertas de nuevos códigos bancarios no registrados en SAP | `Nativo` | 1 | Notificación en tiempo real al equipo para habilitar creación rápida en SAP |
| 8 | Reglas de categorización y contraparte | `Configuración` | 1 | Parametrización de reglas por banco para resolver datos incompletos (RIF truncados, referencias erróneas, código 595) |
| 9 | Mapeo de cuentas contables (GL) | `Configuración` | 2 | Requiere plan de cuentas de Génica como prerrequisito |
| 10 | Soporte multi-entidad | `Nativo` | 1 | A dimensionar según inventario de cuentas |
| 11 | Roles de usuario y controles de acceso | `Nativo` | 1 | Administración de usuarios delegada a Génica; accesos segmentados por área (tesorería, cobranza, finanzas, IT) |
| 12 | Sincronizaciones programadas | `Nativo` | 1 | Hasta 3 sincronizaciones automáticas diarias + sincronizaciones manuales |
| 13 | Automatización de token 2FA | `Nativo` | 1 | Aplicable a bancos con token — verificar por banco en el inventario |
| 14 | Carga manual de cuentas sin integración bancaria directa | `Configuración` | 1 | Plantilla Excel para cuentas custodio, electrónicas y cajas principales sin conexión directa |
| 15 | Clasificación de movimientos para flujo de caja | `Configuración` | 1 | Categorización automática: comisiones, pagos, cobros, transferencias |

> **Definiciones de tipo:**
> - **Nativo** — Capacidad estándar de la plataforma. Sin esfuerzo de ingeniería adicional.
> - **Configuración** — Disponible en la plataforma pero requiere configuración específica del cliente (reglas, mapeos, permisos).
> - **Desarrollo especial** — Requiere scoping y desarrollo de ingeniería. Ver 7.2 para detalle.

### 7.2 Funcionalidades Especiales o Integraciones

No se identificaron elementos de `Desarrollo especial`. La integración SAP es estándar (JSON vía API). Todos los elementos del alcance son Nativos o de Configuración.

### 7.3 Pendiente de Definición

| # | Elemento | Estado | Responsable |
|---|---|---|---|
| 1 | Inventario completo de cuentas bancarias (banco, tipo, entidad, número de cuenta) | `Pendiente — Cliente` | José Boscán |
| 2 | Volumen promedio de transacciones mensuales por banco | `Pendiente — Cliente` | Anaura Prieto |
| 3 | Revisión de documentación técnica API y seguridad para integración SAP | `Pendiente — Cliente` | Equipo Tecnología Génica (Leodardo Chacín / Juan García) |
| 4 | Versión exacta de SAP y tipo de despliegue | `Pendiente — Cliente` | Equipo Tecnología Génica |
| 5 | Listado y detalle de bancos internacionales (Panamá, EE.UU., otros) | `Pendiente — Cliente` | José Boscán / Anaura Prieto |
| 6 | Número exacto de entidades legales en alcance | `Pendiente — Cliente` | José Boscán |
| 7 | Tiempos de respuesta internos de Tesote para gestionar alertas de nuevos códigos bancarios | `En revisión` | Esteban Suárez (Tesote) |
| 8 | Metodología de mapeo código bancario → cuenta contable: entender cómo Génica mapea actualmente los códigos de operación bancaria a cuentas GL en SAP — si los códigos son estrictamente necesarios o si el mapeo por descripción (RIF, contraparte, tipo de transacción) podría reemplazar o complementar el mapeo por código. Solicitar ejemplos de reglas de mapeo actuales y casos de fallo. | `Pendiente — Tesote` | Esteban Suárez (Tesote) |

### 7.4 Fuera de Alcance

| # | Elemento | Notas |
|---|---|---|
| 1 | Conciliación final en SAP | Responsabilidad del equipo de finanzas de Génica en SAP. Tesote realiza pre-conciliación y envía datos validados. |
| 2 | Creación de nuevos códigos bancarios en SAP | Responsabilidad del equipo tecnológico de Génica. Tesote alerta; el cliente actúa. |
| 3 | Gestión de pagos o transferencias | Tesote es plataforma de visualización y conciliación — no maneja fondos ni ejecuta pagos. |

---

## 8. Plan de Implementación

### 8.1 Fases

| Fase | Alcance | Inicio Estimado | Go-Live Estimado |
|---|---|---|---|
| **Fase 1 — Finanzas y Operaciones** | Configuración de cuentas bancarias, conectividad bancaria, tablero de saldos, reportes de disponibilidad, roles de usuario, reglas de categorización | Post-firma (estimado Mayo 2026) | ~4–5 semanas desde inicio |
| **Fase 2 — Integración SAP** | Conexión API Tesote → SAP, envío automático de extractos en JSON, validación de carga, parametrización de alertas de códigos bancarios | Paralela a Fase 1 | ~5–7 semanas desde inicio (~8 semanas totales) |

### 8.2 Prerrequisitos del Cliente

| Prerrequisito | Responsable | Fecha Límite |
|---|---|---|
| Inventario completo de cuentas bancarias | José Boscán | Lo antes posible |
| Validación de volumen de transacciones | Anaura Prieto | Lo antes posible |
| Revisión y aprobación de documentación técnica API | Equipo Tecnología Génica | A definir post-recepción |
| Plan de cuentas SAP (GL) para mapeo | Equipo Tecnología Génica | Antes del inicio de Fase 2 |
| Designación de usuario Master Tesote en Génica | José Boscán / Anaura Prieto | Antes del inicio de Fase 1 |
| Creación de usuarios bancarios de consulta para Tesote | Anaura Prieto | Antes del inicio de Fase 1 |

---

## 9. Puntos Abiertos y Próximos Pasos

| # | Acción | Responsable | Fecha Límite |
|---|---|---|---|
| 1 | Enviar inventario completo de cuentas bancarias (bancos, entidades, tipos, número de cuentas, volumen) | José Boscán (Génica) | Lo antes posible |
| 2 | Validar y enviar volumen promedio de transacciones mensuales | Anaura Prieto (Génica) | Lo antes posible |
| 3 | Revisar documentación técnica de API y seguridad enviada por Tesote; definir proceso y tiempos para integración SAP | Equipo Tecnología Génica | A definir post-recepción |
| 4 | Definir tiempos de respuesta internos para gestión de alertas de nuevos códigos bancarios | Esteban Suárez (Tesote) → consultar equipo técnico | Próximos días |
| 5 | Enviar correo con próximos pasos + documentación técnica de API y seguridad para equipo IT de Génica | Esteban Suárez (Tesote) | Hoy, 2026-04-10 |
| 6 | Preparar propuesta comercial con pricing basado en inventario de cuentas y volumen de transacciones | Esteban Suárez (Tesote) | Post-recepción de inventario |

---

## Historial del Documento

| Versión | Fecha | Autor | Resumen de Cambios |
|---|---|---|---|
| 0.1 | 2026-03-27 | Tesote | Borrador inicial — post llamada introductoria |
| 0.2 | 2026-04-10 | Tesote | Actualizado post llamada de discovery — casos de uso confirmados, contexto SAP detallado, plan de implementación definido |
| 1.0 | 2026-04-15 | Tesote | Versión completa post-discovery — alcance con columna de Tipo, aplicación por área, pendiente validación de inventario de cuentas |

---

*Elaborado por Tesote — Esteban Suárez — 2026-04-15*
*Para consultas o ajustes, contactar a esteban.suarez@tesote.com*
