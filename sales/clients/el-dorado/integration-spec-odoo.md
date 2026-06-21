---
title: "Propuesta Técnica — Integración Odoo [Tesote + El Dorado]"
tags: [el-dorado, sales, odoo, integration, pago-movil, bsl, reconciliation]
updated: 2026-05-07
status: draft
audience: El Dorado (Vanessa Villanueva, Iris) + TR (implementador Odoo) + equipo de desarrollo Tesote
---

# Propuesta Técnica — Integración Odoo
## Tesote + El Dorado

**Documento preparado por Tesote para el equipo de tesorería de El Dorado, TR (implementador Odoo) y el equipo de desarrollo Tesote.**
**Fecha:** 7 de mayo de 2026 (post reunión de descubrimiento del 7 de abril)
**Alcance:** Fase 1 — Carga automática de extractos bancarios a Odoo vía Bank Statement Lines (BSLs) y conciliación masiva de Pago Móvil de las 31 sucursales.

---

## Resumen Ejecutivo

El proceso actual de conciliación de Pago Móvil en Odoo es manual — clic por clic, línea por línea — y se ejecuta sobre 31 sucursales con volúmenes diarios de hasta 100 movimientos por tienda. La causa raíz no es Odoo en sí, sino la falta de una herramienta complementaria que (a) cargue los extractos bancarios automáticamente como Bank Statement Lines (BSLs) y (b) ejecute la conciliación contra los métodos de pago de Odoo en lote, no transacción por transacción.

Esta propuesta cubre ambos frentes:

1. **Ingesta automatizada de extractos bancarios** — Tesote conecta los bancos en alcance (BNC como prioritario) y entrega cada movimiento a Odoo como un `account.bank.statement.line` clasificado por método de pago, sucursal y cuenta destino.
2. **Conciliación masiva de Pago Móvil** — Tesote agrupa todos los Pago Móviles de un mismo día/sucursal en el extracto BNC y los concilia contra las dos partidas que Odoo registra al cierre de caja (`pago móvil BNC` + `pago móvil manual`), calcula la diferencia, y postea automáticamente el asiento de ajuste a la cuenta de ganancia o pérdida configurada.

**Resultado para El Dorado:** se eliminan los miles de clics diarios de conciliación, los extractos se cargan solos cada mañana, y el proceso queda en modo revisión por excepción — el equipo de tesorería solo interviene cuando hay una pérdida material que requiere análisis manual.

---

## 1. Arquitectura de Comunicación — cómo Tesote interactúa con Odoo

La comunicación entre Tesote y Odoo se realiza vía la **API externa de Odoo** (XML-RPC / JSON-RPC sobre HTTPS) sobre el endpoint del cliente, autenticada con un usuario de servicio dedicado a Tesote dentro de Odoo, con un Permission Set acotado a los modelos en alcance. Tesote escribe directamente sobre los modelos contables de Odoo (`account.bank.statement`, `account.bank.statement.line`, `account.move`, `account.payment`) y consume los maestros (`res.company`, `account.journal`, `account.account`, `pos.config`) en modo lectura para enriquecer cada movimiento antes de cargarlo.

### Flujo de datos

```
                    ┌────────────────────────────────────────┐
                    │   BANCOS (BNC, Bancamiga, Bancaribe,   │
                    │   BdV, otros)                          │
                    └──────────────────┬─────────────────────┘
                                       │ Conexiones bancarias
                                       │ (BNC: API Latin Pagos;
                                       │  resto: webscraper)
                                       ▼
                    ┌────────────────────────────────────────┐
                    │              TESOTE                    │
                    │  - conectividad bancaria               │
                    │  - normalización de extractos          │
                    │  - clasificación por método de pago    │
                    │    (PM BNC, PM manual, POS BNC, etc.)  │
                    │  - mapeo a sucursal vía cuenta destino │
                    │  - agrupación PM por día/sucursal      │
                    │  - cálculo de diferencias              │
                    └────┬─────────────────────────┬─────────┘
                         │ PULL (lectura)          │ PUSH (escritura)
                         │ maestros Odoo           │ BSLs + conciliación
                         │                         │ + asiento de ajuste
                         │   XML-RPC / JSON-RPC    │
                         ▼                         ▼
                    ┌────────────────────────────────────────┐
                    │             ODOO (El Dorado)           │
                    │  - bank statements + BSLs              │
                    │  - reconciliation                      │
                    │  - posting contable                    │
                    │  - cierre de caja POS                  │
                    └────────────────────────────────────────┘
```

**Tesote ejecuta tanto la ingesta como la conciliación.** A diferencia de un patrón donde Odoo concilia internamente, en este caso Tesote ejecuta la lógica de matching contra las partidas registradas en Odoo y escribe el resultado conciliado directamente sobre los modelos de Odoo. El equipo de tesorería ve el resultado ya cuadrado dentro de Odoo, no un proceso de validación manual.

**Multi-sucursal.** Cada una de las 31 sucursales tiene sus propias cuentas bancarias por institución. Tesote mantiene el mapeo entre cada cuenta del extracto y la sucursal en Odoo, de forma que cada BSL se inyecta sobre el `account.journal` correcto.

---

## 2. Caso de Uso 1 — Carga Automática de Extractos vía BSLs

### Comportamiento esperado

Cada mañana, sin intervención manual, todos los extractos del día anterior están cargados en Odoo como `account.bank.statement` con sus correspondientes BSLs, listos para conciliación. El equipo deja de descargar archivos de los portales y de subirlos a Odoo.

### Lógica de ingesta

| # | Paso | Sistema | Detalle |
|---|---|---|---|
| 1 | Sincronización de extractos | Tesote | Tesote sincroniza los movimientos del día anterior de cada cuenta bancaria conectada (BNC vía API, resto vía webscraper). |
| 2 | Normalización | Tesote | Cada movimiento se normaliza al modelo canónico de Tesote: fecha, monto, signo, contraparte, referencia, metadata bancaria. |
| 3 | Clasificación por método de pago | Tesote | Cada línea se clasifica como `pago_movil_bnc`, `pago_movil_manual`, `pos_bnc`, `pos_bancaribe`, `comision`, `transferencia`, etc., según patrones específicos por banco (referencia, descripción, código de operación). |
| 4 | Mapeo a sucursal y journal Odoo | Tesote | Cada cuenta bancaria está mapeada a un `account.journal` en Odoo, que a su vez está asociada a la sucursal correspondiente. |
| 5 | Creación del statement en Odoo | Tesote | Tesote crea un `account.bank.statement` por cuenta y por día, con los movimientos del día como `account.bank.statement.line`. |
| 6 | Idempotencia | Tesote | Cada BSL se tagea con un identificador único derivado del banco (referencia + monto + timestamp) para evitar duplicados en re-ingestas. |

### Modelos Odoo escritos por Tesote

| Modelo | Operación | Notas |
|---|---|---|
| `account.bank.statement` | `create` | Un statement por journal por día, con `name = "BNC-Varal-2026-04-30"` (o convención equivalente). |
| `account.bank.statement.line` | `create` | Una línea por movimiento bancario, con metadata enriquecida en `narration` o campos custom acordados con TR. |

### Configuración requerida (one-time)

- Mapeo `cuenta bancaria ↔ account.journal` para las 31 sucursales × bancos en alcance.
- Convención de nombres de statement (`{banco}-{sucursal}-{fecha}`) para trazabilidad.
- Decisión: ¿custom fields en `account.bank.statement.line` para almacenar `metodo_pago_clasificado` y `sucursal_id`, o usar `narration`? — A acordar con TR.

---

## 3. Caso de Uso 2 — Conciliación Masiva de Pago Móvil

### Problema actual

En Odoo, al cierre de caja diario, cada sucursal registra dos partidas de Pago Móvil: `pago móvil BNC` (cuando el POS captura el pago automáticamente vía Bluetooth con el datáfono) y `pago móvil manual` (fallback cuando hay problemas de señal y el cajero ingresa el pago a mano). Estas dos partidas están **englobadas** — un solo monto agregado por método y por día.

En el extracto BNC, en cambio, cada Pago Móvil es una línea independiente. Para una sucursal con 50 PM en un día, el flujo manual exige 50 clics de validación uno-a-uno. Multiplicado por 31 sucursales, son miles de clics diarios.

### Solución

Tesote ejecuta la conciliación en lote. Para cada cuenta bancaria × día, Tesote:

1. **Identifica los BSLs** correspondientes a Pago Móvil (clasificación `pago_movil_bnc` realizada en la ingesta).
2. **Calcula la sumatoria** de todos los BSLs del día.
3. **Encuentra las partidas Odoo a conciliar** — los `account.payment` registrados en el cierre de caja con métodos `Pago Móvil BNC` y `Pago Móvil Manual` para esa sucursal y fecha.
4. **Calcula la diferencia** entre la sumatoria del extracto y la sumatoria de los pagos Odoo.
5. **Concilia y postea el ajuste** en una sola operación.

### Lógica de matching y diferencia

```
sumatoria_extracto_PM     = Σ BSLs clasificados como pago_movil_bnc (día N, sucursal S)
sumatoria_facturado_PM    = pago_móvil_BNC_payment + pago_móvil_manual_payment (día N, sucursal S)

diferencia = sumatoria_extracto_PM − sumatoria_facturado_PM

if diferencia == 0:
    conciliar BSLs ↔ payments, sin ajuste
elif diferencia > 0  (sobrante):
    conciliar BSLs ↔ payments + asiento al account.account "Otros Ingresos / Sobrantes PM"
elif diferencia < 0  (faltante):
    conciliar BSLs ↔ payments + asiento al account.account "Otros Egresos / Faltantes PM"
```

> El equipo de El Dorado mantendrá el control sobre el umbral de revisión manual — por ejemplo, si la diferencia (en valor absoluto) supera un monto X, el asiento de ajuste se crea en estado borrador y queda pendiente de revisión por tesorería antes de ser posteado.

### Modelos Odoo escritos por Tesote

| Modelo | Operación | Notas |
|---|---|---|
| `account.bank.statement.line` | `update` (reconciliation) | Vinculación BSL ↔ `account.payment` mediante el flujo de reconciliation interno. |
| `account.move` | `create` | Asiento de ajuste para sobrantes/faltantes, con líneas a la cuenta GL configurada. |

### Configuración contable requerida (one-time)

- Cuenta GL para **Sobrantes de Pago Móvil** (tipo: ingreso).
- Cuenta GL para **Faltantes de Pago Móvil** (tipo: gasto).
- Umbral de monto para revisión manual (configurable).
- Política sobre asiento en borrador vs posteado automáticamente.

---

## 4. Caso de Uso 3 (Fase 2) — Conciliación POS

### Diferencias respecto a Pago Móvil

- **Identificación:** los lotes POS tienen referencias correlativas (números secuenciales 1, 2, 3, ...) y un identificador consistente por banco — el matching es más directo que el de Pago Móvil.
- **Liquidación diferida:** los movimientos de Punto BNC y, sobre todo, de Bancaribe, **liquidan en el banco 24 a 48 horas después** de la fecha de la venta en Odoo. La conciliación debe correlacionar la fecha de venta (Odoo) con la fecha de liquidación (extracto), no con la fecha del extracto.
- **Cobertura:** aproximadamente 10 de las 31 sucursales tienen Punto BNC; el resto, por confirmar.

### Lógica de matching

Misma estrategia que Pago Móvil — agrupación por sucursal × fecha de venta + diferencia + asiento de ajuste — pero con:

1. **Ventana temporal de ±3 días** entre fecha de venta Odoo y fecha de liquidación bancaria.
2. **Matching por referencia correlativa** cuando esté disponible en el extracto, como confirmación adicional al agrupado por monto y fecha.

> Esta fase se trabaja en paralelo a Fase 1 en diseño, pero su go-live es posterior — primero estabilizamos Pago Móvil, luego POS.

---

## 5. Ambiente de Pruebas

El Dorado dispone de un módulo administrativo de Odoo dedicado a pruebas (no afecta producción) que la auditoría interna utiliza para experimentación. Vanessa Villanueva confirmó disponibilidad de este módulo en la reunión del 7 de abril.

**Plan de validación:**

1. Tesote conecta una cuenta bancaria piloto (recomendado: una sucursal con volumen medio, no la más grande, para iterar más rápido) al ambiente de pruebas.
2. Ingesta de extractos del último mes — validación de clasificación por método de pago contra el Excel actual de Vanessa.
3. Ejecución de conciliación masiva PM en seco — comparación de los asientos resultantes contra los que Vanessa habría generado manualmente.
4. Iteración hasta paridad ≥ 99.5% sobre el mes piloto.
5. Expansión progresiva al resto de sucursales sobre el mismo ambiente, antes de cualquier corte a producción.

---

## 6. Qué Necesitamos para Arrancar

| # | Requerimiento | Responsable | Detalle | Estado |
|---|---|---|---|---|
| 1 | Versión de Odoo confirmada | TR / El Dorado | 17, 18 o 19 — afecta API y compatibilidad de la integración nativa de Tesote | Pendiente |
| 2 | Tipo de despliegue | TR / El Dorado | Odoo SaaS, Odoo.sh u on-premise — afecta autenticación y conectividad | Pendiente |
| 3 | Acceso al módulo administrativo de pruebas | El Dorado | URL del ambiente, usuario de servicio para Tesote, Permission Set acotado | Pendiente |
| 4 | Inventario de cuentas bancarias | El Dorado | Banco, sucursal, número de cuenta, journal Odoo asociado, volumen estimado | En curso (Esteban enviando formulario) |
| 5 | Plan de cuentas — cuentas de ajuste | El Dorado (Tesorería) | Cuenta GL para Sobrantes PM y Faltantes PM (+ análogas para POS en Fase 2) | Pendiente |
| 6 | Convención de naming para statements | TR + Tesote | Decisión sobre formato `{banco}-{sucursal}-{fecha}` u otro | Pendiente |
| 7 | Custom fields en BSL vs uso de `narration` | TR + Tesote | Decisión sobre cómo persistir metadata enriquecida (método de pago, sucursal, ID Tesote) | Pendiente |
| 8 | Umbral y política de revisión manual de ajustes | El Dorado (Tesorería) | Monto mínimo para auto-postear vs dejar en borrador | Pendiente |
| 9 | Mapeo cuenta bancaria ↔ journal Odoo | El Dorado + TR | Una vez recibido el inventario, mapear cada cuenta a su journal | Pendiente |
| 10 | Whitelist de IPs (si aplica) | El Dorado IT | Solo si el Odoo está detrás de firewall corporativo — Tesote proporcionará IPs de egreso | Pendiente |

---

## 7. Responsabilidades — Desarrollo e Implementación

| # | Tarea | Responsable | Apoyo | Estado |
|---|---|---|---|---|
| 1 | Habilitar usuario de servicio Tesote en ambiente de pruebas + Permission Set | TR | El Dorado IT | Pendiente |
| 2 | Conectar BNC piloto en Tesote | Tesote | El Dorado Tesorería | Pendiente |
| 3 | Construir mapeo cuenta ↔ journal y reglas de clasificación de método de pago | Tesote | El Dorado Tesorería + TR | Pendiente |
| 4 | Implementar ingesta de BSLs vía API Odoo | Tesote | TR (decisión sobre custom fields) | Pendiente |
| 5 | Implementar lógica de conciliación masiva PM + asiento de ajuste | Tesote | El Dorado Tesorería (validación de cuentas GL) | Pendiente |
| 6 | Validación end-to-end sobre mes piloto contra Excel actual de Vanessa | Tesote + El Dorado Tesorería | TR | Pendiente |
| 7 | Configuración de cuentas GL de ajuste y umbrales | El Dorado Tesorería + TR | — | Pendiente |
| 8 | Expansión a las 31 sucursales | Tesote | El Dorado Tesorería | Pendiente |
| 9 | Pruebas paralelas — proceso actual vs automatizado | Tesote + El Dorado | TR | Pendiente |
| 10 | Go-live Fase 1 (PM) | Tesote | TR + El Dorado | Pendiente |
| 11 | Diseño y ejecución de Fase 2 (POS, incluyendo Bancaribe T+2) | Tesote | El Dorado + TR | Pendiente |
| 12 | Soporte continuo cuando los bancos cambian formato | Tesote | — | Pendiente |

---

## 8. Patrón de Implementación

El enfoque es iterativo — empezamos a empujar datos reales lo antes posible, sin esperar a que toda la integración esté terminada:

1. **TR habilita el usuario de servicio Tesote en el ambiente de pruebas con Permission Set acotado** — Tesote valida conectividad, lectura de maestros y escritura sobre statements.
2. **Tesote conecta una sucursal piloto en BNC** y arranca ingesta de BSLs sobre el ambiente de pruebas — validación de clasificación por método de pago contra el Excel actual de Vanessa.
3. **Tesote implementa la conciliación masiva PM** y la valida contra el último mes en seco — paridad ≥ 99.5% sobre el mes piloto antes de avanzar.
4. **Configuración contable de cuentas de ajuste y umbrales** con tesorería de El Dorado.
5. **Expansión progresiva al resto de sucursales** sobre el ambiente de pruebas, hasta cubrir las 31.
6. **Go-live Fase 1** — corte a producción con paralelo controlado durante las primeras dos semanas.
7. **Diseño Fase 2** (POS + Bancaribe T+2) en paralelo a la estabilización de Fase 1.

---

## 9. Referencia Técnica

**APIs de Odoo en uso:**

- `account.bank.statement` — `create`, `read`, `write`
- `account.bank.statement.line` — `create`, `read`, `write` (incluyendo flujo de reconciliation)
- `account.move` / `account.move.line` — `create` (asientos de ajuste)
- `account.payment` — `read` (matching contra partidas de cierre de caja)
- `res.company`, `account.journal`, `account.account` — `read` (maestros para enriquecimiento y mapeo)
- `pos.config`, `pos.session` — `read` (correlación con cierre de caja POS, Fase 2)

**Autenticación:** XML-RPC / JSON-RPC con usuario de servicio dedicado, Permission Set acotado a los modelos listados.

**Documentación:**
- Odoo External API: https://www.odoo.com/documentation/19.0/developer/reference/external_api.html
- Odoo Accounting — Bank Reconciliation: https://www.odoo.com/documentation/19.0/applications/finance/accounting/bank/reconciliation.html

---

## 10. Próximos Pasos

1. El Dorado / TR confirman versión de Odoo, tipo de despliegue y acceso al ambiente de pruebas con usuario de servicio Tesote.
2. El Dorado completa el inventario de cuentas bancarias (formulario enviado por Esteban).
3. Tesote y TR alinean en la decisión de custom fields vs `narration` para metadata en BSLs.
4. El Dorado Tesorería confirma cuentas GL de ajuste y umbrales de revisión manual.
5. Tesote arranca el paso 1 del Patrón de Implementación.

---

**Contacto Tesote:**
- Luis Pulgar — luis@tesote.com
- Esteban Suárez — esteban.suarez@tesote.com

---

## Historial del Documento

| Versión | Fecha | Autor | Resumen de Cambios |
|---|---|---|---|
| 0.1 | 2026-05-07 | Tesote (Luis Pulgar) | Borrador inicial post reunión de descubrimiento del 7 de abril |
