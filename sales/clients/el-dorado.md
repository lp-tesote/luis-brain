---
title: El Dorado
tags: [sales, client, odoo, retail, pago-movil, venezuela]
updated: 2026-04-07
author: Esteban Suárez
---

# El Dorado

| Campo | Detalle |
|---|---|
| **Stage** | `Discovery` |
| **AE** | Esteban Suárez |
| **Owner** | Luis Pulgar |
| **Intro Call** | 2026-03-20 |
| **Discovery Call** | 2026-04-07 |
| **Est. Close** | 2026-05-07 |
| **Qualification** | `Qualified` |
| **Source** | Referral — cliente anterior reconectado por Roberto |

## Contexto

Cadena de retail con 31 sucursales en Venezuela. ERP: Odoo (v17/18/19), implementado por TR. En proceso de migrar POS de Cetux/Setux a Odoo nativo.

**Pain principal:** Conciliación manual de pago móvil — hasta 100 transacciones por tienda por día × 31 sucursales = miles de clics manuales diarios. Todos los pagos móviles llegan por BNC.

**Caso de uso núcleo:** Automatización de conciliación pago móvil + carga automática de extractos bancarios a Odoo.

## Contactos

| Nombre | Rol | Email |
|---|---|---|
| Vanessa Villanueva | Tesorería — Champion | vvillanueva@latam-fs.com |
| Iris (apellido TBC) | Directora — Economic Buyer | Por confirmar |
| Lorena (apellido TBC) | Por confirmar | Por confirmar |

## Scope Flags

- [x] Workflow automation — conciliación pago móvil (Special Request: requiere validación técnica)
- [ ] Inventario de cuentas bancarias (pendiente del cliente)
- [ ] Versión Odoo confirmada

## Documentos

- [Blueprint Operativo v1.0](../../implementation/playbooks/blueprint-operativo-el-dorado.md) — 2026-04-07
- [Propuesta Técnica — Integración Odoo (PM bulk recon + BSLs)](el-dorado/integration-spec-odoo.md) — 2026-05-07 (draft)
- Dossier Interno v1.0 — en cliente folder (Tesote-Sales/clients/El_Dorado/)

## Discovery — Hallazgos Clave

- Demo en vivo: Vanessa mostró el proceso de conciliación pago móvil en Odoo. 31-100 clics manuales por tienda por día.
- BNC: banco exclusivo para pago móvil. API integration (Latin Pagos) — máxima calidad en Tesote.
- Luis confirmó viabilidad técnica preliminar de la automatización en la llamada.
- Módulo de prueba de Odoo disponible para UAT.
- Inventario de cuentas bancarias: pendiente (Esteban enviando formulario).

## Próximos Pasos

1. Esteban → formulario inventario cuentas → Vanessa
2. Luis → propuesta técnica automatización pago móvil
3. Luis → validación con equipo de desarrollo
4. Sesión de revisión de propuesta → agendar
