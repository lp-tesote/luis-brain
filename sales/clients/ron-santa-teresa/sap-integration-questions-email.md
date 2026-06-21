---
title: Email — Definición técnica integración SAP (versión condensada)
tags: [sales, client, ron-santa-teresa, sap, scoping, email]
updated: 2026-05-04
status: draft
---

# Email — Definición técnica integración SAP

Versión condensada (5 preguntas) para primer contacto. La versión completa de 21 preguntas está en `sap-integration-questions.md` / `.docx` — usar esa para la sesión técnica con el partner SAP, una vez aprobada la propuesta.

---

**Asunto:** Definición técnica — Integración Tesote × SAP

Hola [nombre],

Para preparar la propuesta de integración con su SAP (ECC 6.0 EHP 7 sobre HANA), nos basta con que nos confirmen estos cinco puntos. El alcance que estamos dimensionando: Tesote lee datos maestros desde SAP y entrega el extracto bancario en el formato que su sistema ya consume hoy.

**1. Partner SAP / equipo Basis.** ¿Quién acompaña su SAP y con quién coordinaríamos el trabajo técnico? ¿El sistema es on-premise, en nube privada, u hospedado por su partner?

**2. Carga del extracto hoy.** ¿Cómo cargan los extractos bancarios actualmente (FF.5 manual, programa Z propio, BCM, otro)? Idealmente con un archivo de muestra del formato que SAP procesa sin problemas hoy (MT940, BAI2, CAMT.053 o propio).

**3. Datos maestros.** ¿Qué mecanismo tienen disponible para que Tesote lea su plan de cuentas y maestro de clientes/proveedores con RIF (OData, RFC/BAPI, lectura sobre HANA, exportación CSV programada)?

**4. Canal de entrega.** ¿Dónde dejaríamos el archivo del extracto generado por Tesote (SFTP del lado SAP, directorio en servidor de aplicación, cola BCM, carga manual)?

**5. Acceso de red.** ¿Qué modelo de conectividad utilizan para integraciones entrantes (VPN, SAP Cloud Connector, lista blanca de IPs)?

Con estas cinco respuestas podemos cerrar la propuesta. El resto del detalle (reglas EBS por house bank, cadencia de entrega, convenciones de nombres, etc.) lo trabajamos en sesión técnica conjunta una vez aprobada.

Si les resulta más cómodo, coordinamos 30 minutos con su partner SAP y las respondemos en conjunto. También podemos ir por escrito.

Saludos,
Luis
