---
title: "Requerimientos Técnicos — Integración Microsoft Dynamics 365 Business Central [Tesote + Purolomo]"
tags: [purolomo, sales, business-central, dynamics-365, integration, vog]
updated: 2026-04-30
status: final
audience: VOG (implementador BC) + equipo técnico Purolomo
notion: https://www.notion.so/3521ee04eee181d3a60ed6597b480b69
---

> **Notion mirror:** [Implementation › Requerimientos Técnicos — Integración Microsoft Dynamics 365 Business Central [Tesote + Purolomo]](https://www.notion.so/3521ee04eee181d3a60ed6597b480b69) (pushed 2026-04-30). Edit there if changes need to be visible to the team; mirror back here when promoted.

# Requerimientos Técnicos — Integración Microsoft Dynamics 365 Business Central
## Tesote + Purolomo

**Documento preparado por Tesote para el equipo técnico de Purolomo y VOG (implementador Business Central).**
**Fecha:** 30 de abril de 2026 (post reunión técnica del 23 de abril)
**Alcance:** Fase 1 — Entrega a Business Central de extractos bancarios enriquecidos por Tesote (identificación de contraparte por RIF + asignación de empresa).

---

## Resumen de Reunión Técnica — 23 de abril de 2026

**Participantes:**
- Tesote: Luis Pulgar, Esteban Suárez, Roberto
- Purolomo: José Luis González, Daniela Membrilla, D. Chacón, A. Moreno
- VOG: Jesús Hernández, Jesnny H.

**Puntos clave discutidos:**
1. Se confirmó la separación de proyectos: la integración bancaria con Business Central (este documento) es independiente del proyecto de Crédito y Cobranza, aunque ambos avanzan en paralelo.
2. Se definió la frontera de responsabilidades: **Business Central** ejecuta la conciliación bancaria, la aplicación de pagos y el posting contable. **Tesote** entrega los extractos bancarios ya normalizados y enriquecidos con la identificación de la contraparte y la empresa a la que pertenece cada transacción. Tesote no participa en la conciliación ni en el posting.
3. Tesote se comprometió a enviar este documento detallando la arquitectura de comunicación, las APIs requeridas y los flujos de datos para que VOG pueda revisar internamente y preparar dudas para la próxima reunión.
4. Noris Torres (Purolomo) coordinará la próxima reunión una vez VOG haya revisado el documento.
5. José Luis González dará continuidad al desarrollo y prueba del proyecto de Crédito y Cobranza en paralelo a esta integración.

**Acuerdo principal:** Tesote envía este documento; VOG lo revisa internamente; se agenda reunión técnica de seguimiento para alinear sobre dudas y plan de pruebas.

---

## Objetivo

Definir los requerimientos técnicos y la frontera de responsabilidades para construir la integración entre Tesote y Microsoft Dynamics 365 Business Central. Fase 1 cubre la entrega a BC de extractos bancarios enriquecidos por Tesote, donde cada movimiento bancario incluye:

1. **Identificación de la contraparte por RIF** — qué cliente o proveedor está detrás de cada cobro o pago.
2. **Asignación de empresa** — a cuál de las tres companies (Purolomo, Ingredia, Ganadería) pertenece la transacción.

Business Central recibe los extractos ya enriquecidos y ejecuta toda la conciliación, aplicación de pagos y posting contable. Tesote no participa en la conciliación ni en el posting.

---

## Arquitectura de Comunicación — cómo Tesote interactúa con Business Central

La comunicación entre Tesote y Business Central se realiza vía APIs y tiene **dos rutas complementarias** que coexisten:

### Ruta A — APIs estándar de Business Central (OData v4)

Business Central expone un conjunto de APIs estándar bajo el path `api/v2.0` sobre el endpoint del tenant del cliente, con autenticación **OAuth 2.0** vía **Microsoft Entra ID (Azure AD)**. Tesote consume estas APIs en modo lectura para acceder a los maestros de BC (companies, customers, vendors, bank accounts) y poder enriquecer cada movimiento bancario antes de entregarlo.

### Ruta B — Extensión AL nativa de Tesote en Business Central

Tesote desarrolla una aplicación nativa de Business Central publicada en Microsoft AppSource (en proceso de certificación). Esta extensión vive dentro del entorno BC del cliente y provee:

- Pantallas de configuración (Setup) para vincular el tenant de Purolomo con Tesote.
- El endpoint de inyección de extractos bancarios enriquecidos (la API set estándar `api/v2.0` no expone un endpoint de bank statement ingestion).
- Hooks/eventos para detonar reportes desde dentro de BC.

La extensión se comunica con la API de Tesote y con las APIs estándar de BC; no requiere desarrollo custom adicional por parte de VOG más allá de la configuración inicial.

### Flujo de datos

```
                    ┌────────────────────────────────────────┐
                    │   BANCOS (BNC, BBVA Provincial, BDV,   │
                    │   Mercantil, Banesco, etc.)            │
                    └──────────────────┬─────────────────────┘
                                       │ Conexiones Bancarias
                                       ▼
                    ┌────────────────────────────────────────┐
                    │              TESOTE                    │
                    │  - conectividad bancaria               │
                    │  - normalización de extractos          │
                    │  - identificación de contraparte       │
                    │    por RIF                             │
                    │  - asignación de empresa               │
                    │  - separación intercompañía            │
                    └────┬─────────────────────────┬─────────┘
                         │ PULL (lectura)          │ PUSH (escritura)
                         │ maestros                │ extractos
                         │                         │ enriquecidos
                         │   OData v4 / OAuth 2.0  │
                         ▼                         ▼
                    ┌────────────────────────────────────────┐
                    │   BUSINESS CENTRAL (Purolomo,          │
                    │   Ingredia, Ganadería)                 │
                    │   - conciliación bancaria              │
                    │   - aplicación de pagos                │
                    │   - posting contable                   │
                    │   - flujo de caja                      │
                    └────────────────────────────────────────┘
```

**Tesote enriquece antes de entregar.** Para cada movimiento bancario, Tesote consulta los maestros de BC (`customers`, `vendors`) para identificar a la contraparte por RIF y determinar a cuál empresa (Purolomo, Ingredia, Ganadería) pertenece la transacción. La conciliación, la aplicación de pagos y el posting contable ocurren íntegramente dentro de BC sobre los extractos ya enriquecidos.

**Multi-company.** Todas las llamadas incluyen el `companyId` correspondiente. Purolomo, Ingredia y Ganadería operan como companies separadas en el mismo tenant de BC.

---

## APIs Requeridas — Permisos de Lectura y Escritura

| # | API | Ruta | Permiso | Propósito |
|---|---|---|---|---|
| 1 | `companies` | A — estándar | GET | Lista de companies (Purolomo, Ingredia, Ganadería) — base para asignar cada transacción a la empresa correspondiente |
| 2 | `customers` | A — estándar | GET | Maestro de clientes — identificación de contraparte por RIF (Tax Registration No.) en cobros entrantes |
| 3 | `vendors` | A — estándar | GET | Maestro de proveedores — identificación de contraparte por RIF en pagos salientes |
| 4 | `bankAccounts` | A — estándar | GET | Cuentas bancarias en BC — mapeo entre conexiones bancarias en Tesote y bank accounts en BC |
| 5 | Inyección de extractos bancarios enriquecidos | **B — extensión AL** | POST | Endpoint provisto por la extensión nativa de Tesote en BC. Cada línea del extracto incluye RIF identificado, nombre de la contraparte, y referencia al customer/vendor de BC cuando aplica, además del companyId al que pertenece. La API set estándar `api/v2.0` no expone un endpoint de bank statement ingestion; el flujo se canaliza por la extensión, que escribe a la tabla destino acordada con VOG (Bank Acc. Reconciliation Lines o tabla de staging custom). |

**Nota.** Tesote solo necesita lectura sobre las APIs estándar — los maestros se consumen exclusivamente para identificar la contraparte y asignar la empresa. La única escritura ocurre vía la extensión AL de Tesote, que entrega el extracto bancario enriquecido a BC para que BC ejecute la conciliación y el posting.

---

## Qué Necesitamos para Arrancar

| # | Requerimiento | Responsable | Detalle | Estado |
|---|---|---|---|---|
| 1 | Confirmar edición de Business Central | VOG / Purolomo IT | SaaS (cloud) o on-premise; afecta autenticación y disponibilidad de APIs | Pendiente |
| 2 | Tenant sandbox de BC | VOG | URL del tenant sandbox de Purolomo para pruebas | Pendiente |
| 3 | Registro de aplicación Tesote en Azure AD | VOG / Purolomo IT | App registration en el tenant Microsoft de Purolomo, con permisos sobre BC | Pendiente |
| 4 | Credenciales OAuth 2.0 (sandbox) | VOG | Client ID + Client Secret + Tenant ID | Pendiente |
| 5 | Permission Set en BC para la app Tesote | VOG | Permisos GET sobre las APIs listadas arriba | Pendiente |
| 6 | URL base del servicio OData | VOG | Endpoint del entorno (`https://api.businesscentral.dynamics.com/v2.0/{tenantId}/{environment}/api/v2.0/`) | Pendiente |
| 7 | Whitelist de IPs (si aplica) | VOG / Purolomo IT | IPs de egreso de Tesote (Tesote las proporcionará) — solo si BC está detrás de firewall corporativo | Pendiente |
| 8 | Configuración de Bank Accounts en BC | Purolomo Tesorería + VOG | Bank Account Card por cada cuenta bancaria, con mapeo claro a la company correspondiente | Pendiente |
| 9 | Estructura multi-company | VOG | Cómo están separadas Purolomo / Ingredia / Ganadería en BC (companies, intercompany) | Pendiente |
| 10 | Lista de RIFs intercompañía | Purolomo Tesorería | Para que Tesote separe transferencias internas de cobros reales (regla crítica para BNC y otros bancos) | Pendiente |
| 11 | Decisión de tabla destino para inyección | Tesote + VOG | Bank Acc. Reconciliation Lines estándar vs tabla custom de staging de la extensión AL | Pendiente |
| 12 | Selección de cuenta(s) piloto | Purolomo Tesorería | Cuenta(s) bancaria(s) de Ingredia (empresa nueva, sin deuda técnica) para arrancar | Pendiente |

---

## Responsabilidades — Desarrollo e Implementación

| # | Tarea | Responsable | Apoyo | Estado |
|---|---|---|---|---|
| 1 | Habilitar APIs estándar y proveer credenciales OAuth en sandbox | VOG | Purolomo IT | Pendiente |
| 2 | Definir Permission Set BC con accesos requeridos (lectura sobre maestros) | VOG | Tesote (lista de APIs) | Pendiente |
| 3 | Conectar primera cuenta bancaria piloto en Tesote | Tesote | Purolomo Tesorería | Pendiente |
| 4 | Construir conector OData Tesote ↔ BC (lectura de maestros para enriquecimiento) | Tesote | VOG (soporte API) | Pendiente |
| 5 | Decidir tabla destino en BC para extractos enriquecidos | Tesote + VOG | — | Pendiente |
| 6 | Construir inyección de extractos bancarios enriquecidos vía extensión AL | Tesote | VOG | Pendiente |
| 7 | Configurar Bank Accounts en BC con su mapeo a companies | VOG | Purolomo Tesorería | Pendiente |
| 8 | Provisión de lista de RIFs intercompañía y base de clientes inicial | Purolomo Tesorería | — | Pendiente |
| 9 | Validación end-to-end de extractos enriquecidos (calidad de identificación de contraparte y asignación de empresa) con Tesorería de Purolomo | Tesote + Purolomo Tesorería | VOG | Pendiente |
| 10 | Ejecución de la conciliación, aplicación de pagos y posting sobre los extractos enriquecidos | VOG / Purolomo | — | Pendiente |
| 11 | Agregar cuentas restantes de Purolomo y Ganadería | Tesote | Purolomo Tesorería | Pendiente |
| 12 | Pruebas paralelas: sistema actual vs BC sandbox | Tesote + VOG | Purolomo | Pendiente |
| 13 | Migración a producción BC (go-live) | VOG | Tesote + Purolomo | Pendiente |
| 14 | Soporte continuo cuando los bancos cambian formato | Tesote | — | Pendiente |

---

## Patrón de Implementación

El enfoque es iterativo — empezamos a empujar datos reales lo antes posible, sin esperar a que toda la integración esté terminada:

1. **VOG habilita las APIs estándar y entrega credenciales OAuth + Permission Set en el sandbox de BC** — Tesote valida conectividad y lectura de companies, customers, vendors, bank accounts.
2. **Purolomo conecta una cuenta bancaria piloto en Tesote** (recomendado: Ingredia, empresa nueva sin deuda técnica) — Tesote empieza a ingestar transacciones reales y a hacer matching de contraparte por RIF contra los maestros de BC.
3. **Tesote y VOG deciden la tabla destino en BC para los extractos enriquecidos y construyen el flujo de escritura vía la extensión AL** — primera inyección al sandbox de BC.
4. **Validación conjunta con Tesorería de Purolomo** — calidad de identificación de contraparte, asignación de empresa, separación intercompañía; afinamiento contra datos reales.
5. **Expansión a Purolomo y Ganadería**, activación de la regla de RIFs intercompañía, y corte a producción de BC con la integración Tesote ↔ BC ya validada.

---

## Referencia Técnica

APIs Business Central requeridas — todas estándar de la API set `api/v2.0` salvo la inyección de extractos:

- `companies` — companies del tenant
- `customers` / `vendors` — maestros de clientes y proveedores (lectura para enriquecimiento por RIF)
- `bankAccounts` — cuentas bancarias y su mapeo a companies
- Inyección de extractos bancarios enriquecidos — vía extensión AL de Tesote (Ruta B)

**Autenticación:** OAuth 2.0 vía Microsoft Entra ID (app registration en el tenant Microsoft de Purolomo).

**Documentación:**
- BC API v2.0 reference: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/api-reference/v2.0/
- OAuth 2.0 / S2S authentication: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/automation-apis-using-s2s-authentication
- Extensión Tesote para BC (en certificación AppSource): URL pendiente, se compartirá una vez aprobada
- Conector Odoo de Tesote (referencia de patrón de integración nativa): https://tesote.github.io/odoo-master-connector/

---

## Próximos pasos

1. VOG y Purolomo IT revisan internamente este documento.
2. Noris Torres coordina la siguiente reunión técnica para resolver dudas y definir plan de pruebas.
3. Tesote y VOG alinean en la decisión de tabla destino para la inyección de extractos enriquecidos.
4. Una vez confirmadas credenciales OAuth y Permission Set en sandbox, Tesote arranca paso 1 del Patrón de Implementación.

---

**Contacto Tesote:**
- Luis Pulgar — luis@tesote.com
- Esteban Suárez — esteban.suarez@tesote.com
