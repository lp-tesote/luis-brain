# Blueprint del Proyecto
**El Dorado × Tesote**
*Versión 1.0 — 2026-04-07*

---

| Campo | Detalle |
|---|---|
| **Ejecutivo de cuenta** | Esteban Suárez |
| **Correo electrónico** | esteban.suarez@tesote.com |
| **Teléfono** | — |
| **Fecha de llamada introductoria** | 2026-03-20 |
| **Fecha de llamada de descubrimiento** | 2026-04-07 |
| **Fecha estimada de cierre** | 2026-05-07 |

---

> Este documento constituye la referencia compartida del compromiso entre El Dorado y Tesote. Recoge el contexto operativo, los puntos de dolor, los casos de uso y el alcance de implementación acordados entre ambas partes. Es un documento vivo — actualizado a lo largo del proceso y validado por ambas partes antes del inicio de la implementación.

---

## 1. Perfil de la Empresa

| Campo | Detalle |
|---|---|
| **Industria / Sector** | Retail / Cadena de tiendas |
| **Facturación anual (est.)** | Por confirmar |
| **Entidades legales en alcance** | Por confirmar — operación bajo dominio latam-fs.com |
| **Países de operación** | Venezuela |
| **Sitio web** | Por confirmar |

**Descripción:** El Dorado es una cadena de retail con 31 sucursales en Venezuela, con operaciones de punto de venta de alto volumen transaccional en múltiples bancos, actualmente en proceso de consolidación de sus sistemas de gestión dentro de Odoo.

---

## 2. Contexto Operativo Actual

El Dorado opera con 31 sucursales activas, cada una con sus propias cuentas bancarias en múltiples instituciones. Todos los pagos móviles recibidos en tienda llegan exclusivamente a través del BNC (Banco Nacional de Crédito). La conciliación bancaria se realiza manualmente: el equipo de tesorería descarga los extractos de cada banco, los sube a Odoo, y valida transacción por transacción cada pago móvil del extracto contra el registro de ventas de la tienda. El volumen por tienda puede alcanzar entre 50 y 100 movimientos de pago móvil por día, lo que se multiplica por las 31 sucursales. La empresa está en proceso de migrar su sistema de punto de venta de Cetux/Setux al módulo POS nativo de Odoo, implementado por TR con localización venezolana. El ERP es Odoo (versión 17, 18 o 19 — estándar).

---

## 3. Puntos de Dolor y Motivadores Estratégicos

| # | Punto de Dolor | Impacto en el Negocio |
|---|---|---|
| 1 | **Conciliación manual de pago móvil — transacción por transacción** | Hasta 3.100 clics diarios (31 sucursales × hasta 100 pago móviles/día). "Es clic y paridad. Literal clic y paridad." — Vanessa Villanueva | 
| 2 | **Descarga y carga manual de extractos bancarios** | El equipo entra cada mañana a 7+ bancos, descarga extractos y los sube manualmente a Odoo. Tiempo operativo diario no cuantificado pero recurrente. |
| 3 | **Detección de discrepancias en Excel externo** | El cuadre de lo facturado en Odoo vs. lo recibido en banco se hace en una hoja de cálculo paralela. Proceso frágil, dependiente de un solo operador, propenso a error. |
| 4 | **Odoo no permite selección masiva de pago móviles** | El módulo de conciliación de Odoo no tiene funcionalidad nativa de selección múltiple + validación en lote para extractos bancarios. El workaround es clic individual. |

**Evento detonador:** El Dorado está migrando de Cetux/Setux al módulo POS de Odoo. Una vez completada la migración, toda la conciliación de métodos de pago deberá ocurrir dentro de Odoo. Esto convierte la automatización de la conciliación de pago móvil en una necesidad urgente para que el equipo de tesorería no quede atrapado en un proceso insostenible a escala.

---

## 4. Casos de Uso

| # | Caso de Uso | Descripción | Prioridad |
|---|---|---|---|
| 1 | **Automatización de conciliación — Pago Móvil** | Agrupar todos los movimientos de pago móvil del extracto BNC por sucursal y fecha, conciliarlos automáticamente contra el método de pago registrado en el cierre de caja de Odoo. Diferencias (sobrante/faltante) se asientan automáticamente. | `Alta` |
| 2 | **Carga automática de extractos bancarios** | Eliminar la descarga y carga manual de extractos. Tesote sincroniza todos los bancos conectados y alimenta Odoo automáticamente, con los movimientos del día anterior validados cada mañana. | `Alta` |
| 3 | **Automatización de conciliación — Puntos de Venta** | Conciliar los lotes de POS (referencias correlativas) contra los registros de venta en Odoo. Incluye Bancaribe con condición especial por liquidación diferida (24–48h). | `Media` |
| 4 | **Visibilidad bancaria centralizada en tiempo real** | Consultar saldos y movimientos del día en curso de todos los bancos desde un solo dashboard, sin entrar a cada portal bancario individualmente. | `Media` |

---

## 5. Infraestructura Bancaria

### 5.1 Cuentas Bancarias en Alcance

*Inventario pendiente — Vanessa Villanueva y Esteban Suárez enviando en paralelo.*

| Banco | País | Tipo de Cuenta | Entidad Legal | Últimos 4 dígitos | Nivel de Volumen |
|---|---|---|---|---|---|
| BNC (Banco Nacional de Crédito) | Venezuela | Corriente (por sucursal) | Por confirmar | Por confirmar | `Alto` — recibe TODOS los pago móviles de las 31 sucursales |
| Bancamiga (Banca Amiga) | Venezuela | Por confirmar | Por confirmar | Por confirmar | `Medio` |
| Bancaribe | Venezuela | Por confirmar | Por confirmar | Por confirmar | `Medio` — liquida POS con 24–48h de retraso |
| Banco de Venezuela (BdV) | Venezuela | Por confirmar | Por confirmar | Por confirmar | `Bajo` |
| Otros (estimado 3–4 bancos adicionales) | Venezuela | Por confirmar | Por confirmar | Por confirmar | Por confirmar |

> **Nota:** El Dorado opera una "cuenta consolidadora" por entidad que agrega los saldos de todas las sucursales al cierre del día. El inventario completo (nombres, tipos, cantidades y volúmenes) está pendiente de recepción.

### 5.2 Cobertura Tesote por Institución

| Banco | Estado en Registro Tesote | Tipo de Integración | Notas |
|---|---|---|---|
| BNC | `En registro activo` | API (Latin Pagos) — máxima calidad | Banco principal para pago móvil |
| Bancamiga | `En registro activo` | Webscraper | Token automatizado |
| Bancaribe | `En registro activo` | Webscraper | Configurar condición especial por liquidación T+2 |
| BdV | `En registro activo` | Webscraper | Token automatizado |
| Otros | `Por confirmar contra inventario` | Por confirmar | Confirmar tras recibir inventario |

---

## 6. Sistemas y Integración ERP

| Sistema | Proveedor | Versión | Despliegue | Tipo de Integración | Notas |
|---|---|---|---|---|---|
| **ERP** | Odoo | 17 / 18 / 19 (por confirmar) | Por confirmar | `Estándar` — integración nativa Tesote × Odoo | Implementado por TR con localización venezolana |
| **POS** | Odoo POS (módulo nativo) | Mismo | Por confirmar | Incluido en integración Odoo | En proceso de migración desde Cetux/Setux |

**Mapeo de cuentas contables (GL):** A definir durante el onboarding de implementación. El equipo contable de El Dorado deberá proveer el plan de cuentas como prerequisito. Incluye configuración de asientos de ajuste para sobrantes/faltantes de pago móvil.

**Ambiente de pruebas:** El Dorado dispone de un módulo administrativo de Odoo dedicado a pruebas (no afecta producción). Disponible para validación de la automatización antes del go-live.

---

## 7. Definición de Alcance

### 7.1 En Alcance

| # | Capacidad | Notas |
|---|---|---|
| 1 | Conectividad bancaria — BNC, Bancamiga, Bancaribe, BdV | Todos en registro activo. Otros bancos del inventario a confirmar. |
| 2 | Ingesta automatizada de extractos bancarios | Elimina descarga y carga manual. Movimientos del día anterior validados cada mañana en Odoo. |
| 3 | Datos intraday (T+0) | Disponibles en dashboard Tesote en tiempo real. Sincronización a Odoo ocurre post-cierre bancario (T+1). |
| 4 | Datos T+1 (día anterior confirmado) | Todos los movimientos validados disponibles en Odoo cada mañana. |
| 5 | Normalización de transacciones por banco | Incluye identificación de pago móvil, POS, comisiones, referencias numéricas. |
| 6 | Reglas de categorización y contraparte | Configuración de reglas específicas para pago móvil BNC, pago móvil manual, lotes POS. |
| 7 | Integración ERP — Odoo (v17/18/19, estándar) | Nativa. Carga extractos bancarios y asientos contables en Odoo automáticamente. |
| 8 | Mapeo de cuentas contables (GL) | Configuración de plan de cuentas de El Dorado para asientos de ajuste de pago móvil. |
| 9 | Soporte multi-sucursal — 31 entidades | Una instancia Tesote para todas las sucursales. |
| 10 | Token automatizado (todos los bancos) | Incluye BNC API, Bancamiga, Bancaribe, BdV — sin intervención manual. |
| 11 | Roles de usuario y controles de acceso | Por definir según modelo organizacional de El Dorado. |

### 7.2 Fuera de Alcance

| # | Elemento | Motivo |
|---|---|---|
| 1 | Iniciación de pagos (payment initiation) | No fue mencionado. Requiere evaluación independiente si surge en el futuro. |
| 2 | Integración con Cetux/Setux | El Dorado está migrando fuera de este sistema. No aplica. |
| 3 | Automatización avanzada de FX | No aplica para la operación actual descrita. |

### 7.3 Pendiente de Definición

| # | Elemento | Estado | Responsable |
|---|---|---|---|
| 1 | Inventario completo de cuentas bancarias (banco, tipo, cantidad, volúmenes) | `Pendiente — Cliente` | Vanessa Villanueva / Esteban Suárez |
| 2 | Versión específica de Odoo (17, 18 o 19) y tipo de despliegue (nube/on-premise) | `Pendiente — Cliente` | El Dorado / TR |
| 3 | Número de entidades legales en alcance | `Pendiente — Cliente` | El Dorado |
| 4 | Bancos adicionales del inventario — verificación en registro activo Tesote | `Pendiente — Tesote` | Esteban Suárez |
| 5 | Propuesta técnica detallada de automatización pago móvil | `Pendiente — Tesote` | Luis Pulgar + equipo de desarrollo |
| 6 | Validación de propuesta técnica con equipo de desarrollo | `Pendiente — Tesote` | Luis Pulgar |
| 7 | Definición de fases (Fase 1 solo pago móvil vs. pago móvil + POS simultáneo) | `En revisión` | Ambas partes |

### 7.4 Automatizaciones de Flujo de Trabajo

*Workflows automatizados a incluir en el alcance de este compromiso.*

| # | Automatización | Método de Pago | Fuente de Datos | Objeto en Odoo | Alcance (entidades / sucursales) | Frecuencia | Estado |
|---|---|---|---|---|---|---|---|
| 1 | Conciliación automática — Pago Móvil | Pago Móvil BNC + Pago Móvil Manual | Estado de cuenta BNC (por sucursal) | Método de pago Pago Móvil en cierre de caja (CxC abiertas) | 31 sucursales | Diaria (post cierre T+1) | `Por validar` |
| 2 | Conciliación automática — Puntos de Venta | POS / Punto BNC | Estado de cuenta (BNC / Bancaribe por lotes) | Método de pago Punto de Venta en cierre de caja | ~10 sucursales con Punto BNC (resto por confirmar) | Diaria (post liquidación; Bancaribe: condición T+2) | `Por validar` |

> **Nota de alcance:** Ambas automatizaciones requieren validación técnica con el equipo de desarrollo de Tesote antes de comprometerse contractualmente. Luis Pulgar confirmó viabilidad preliminar en la reunión de descubrimiento del 2026-04-07. La propuesta técnica detallada está en preparación.

---

## 8. Plan de Implementación

### 8.1 Fases

| Fase | Alcance | Inicio Estimado | Go-Live Estimado |
|---|---|---|---|
| **Fase 1** | Conectividad bancaria (BNC + otros bancos confirmados) · Carga automática de extractos a Odoo · Automatización de conciliación pago móvil (31 sucursales) | Por definir post-propuesta técnica | Por definir |
| **Fase 2** | Automatización de conciliación POS · GL mapping completo · Visibilidad consolidada multi-sucursal | Post go-live Fase 1 | Por definir |

### 8.2 Hitos Clave

| Hito | Responsable | Fecha Estimada |
|---|---|---|
| Inventario de cuentas bancarias recibido | El Dorado | Por confirmar |
| Propuesta técnica de automatización enviada | Tesote (Luis Pulgar) | Por confirmar |
| Validación técnica con equipo de desarrollo | Tesote | Por confirmar |
| Blueprint validado por ambas partes | Ambas partes | Por confirmar |
| Kickoff de implementación | Ambas partes | Por confirmar |
| Pruebas en ambiente de Odoo (módulo administrativo) | Ambas partes | Por confirmar |
| Go-live Fase 1 | Tesote | Por confirmar |

### 8.3 Prerequisitos del Cliente

- [ ] Inventario completo de cuentas bancarias (banco, tipo de cuenta, entidad legal, volumen estimado de transacciones)
- [ ] Versión específica de Odoo confirmada (17, 18 o 19) y tipo de despliegue
- [ ] Plan de cuentas contables para mapeo GL (incluyendo cuentas de ajuste para sobrantes/faltantes)
- [ ] Acceso al módulo administrativo de Odoo para pruebas
- [ ] Credenciales bancarias / autorización de acceso
- [ ] Confirmación de entidades legales en alcance
- [ ] Designación de contacto técnico con TR (proveedor implementador de Odoo)

---

## 9. Puntos Abiertos y Próximos Pasos

| # | Acción | Responsable | Fecha Límite |
|---|---|---|---|
| 1 | Enviar formulario de inventario de cuentas bancarias | Esteban Suárez (Tesote) | Inmediato |
| 2 | Completar inventario de cuentas bancarias | Vanessa Villanueva (El Dorado) | Por confirmar |
| 3 | Elaborar propuesta técnica: automatización pago móvil + carga extractos | Luis Pulgar (Tesote) | Por confirmar |
| 4 | Validar propuesta técnica con equipo de desarrollo Tesote | Luis Pulgar (Tesote) | Por confirmar |
| 5 | Confirmar versión Odoo y despliegue con TR | El Dorado | Por confirmar |
| 6 | Agendar sesión de revisión de propuesta técnica | Esteban Suárez (Tesote) | Por confirmar |

---

## Historial del Documento

| Versión | Fecha | Autor | Resumen de Cambios |
|---|---|---|---|
| 0.1 | 2026-03-20 | Tesote | Borrador inicial — post llamada introductoria ("Tesote 2.0 // El Dorado") |
| 0.2 | 2026-04-07 | Tesote | Actualizado post llamada de descubrimiento — demo en vivo, casos de uso confirmados, sección 7.4 agregada |
| 1.0 | 2026-04-07 | Tesote | Versión 1.0 — pendiente validación conjunta |

---

*Elaborado por Tesote — Esteban Suárez — 2026-04-07*
*Para consultas o ajustes, contactar a esteban.suarez@tesote.com*
