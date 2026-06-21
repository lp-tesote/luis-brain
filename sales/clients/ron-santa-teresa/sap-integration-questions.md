---
title: Ron Santa Teresa × Tesote — Definición técnica de la integración con SAP
tags: [sales, client, ron-santa-teresa, sap, scoping]
updated: 2026-04-30
status: draft
---

# Ron Santa Teresa × Tesote — Definición técnica de la integración con SAP

Para preparar la propuesta de integración entre Tesote y su SAP (ECC 6.0 EHP 7 sobre HANA), necesitamos confirmar los puntos técnicos listados a continuación.

El alcance que estamos dimensionando es el estándar de Tesote: leer datos maestros desde SAP y entregar el extracto bancario en el formato que su SAP ya consume hoy. No contempla escritura directa de asientos contables vía BAPI/IDoc.

Las preguntas están agrupadas por bloque. Las marcadas con (★) son las que necesitamos resueltas antes de cerrar la propuesta comercial; el resto pueden trabajarse durante el descubrimiento.

## A. Entorno SAP

1. (★) Hospedaje: on-premise, nube privada (AWS/Azure) u hospedado por su partner SAP.
2. (★) Equipo Basis / partner SAP que acompaña el sistema y con quien coordinaríamos el trabajo técnico.
3. Ambiente de pruebas (Sandbox / QAS) disponible para que construyamos y validemos la integración.
4. Personalizaciones en el flujo de extractos bancarios (programas Z, ampliaciones del módulo FI) o se mantiene cercano al estándar.
5. Migración a S/4HANA — ¿está planificada? ¿plazo previsto? Esto nos permite diseñar la integración para que sobreviva a esa transición.

## B. Lectura de datos maestros desde SAP

6. Mecanismo de extracción disponible: OData (servicios activados en SICF), RFC/BAPI, lectura directa sobre HANA (ODBC/JDBC), o exportación CSV programada.
7. Plan de cuentas (GL): ¿qué sociedades (company codes) entran en alcance y qué cuentas son relevantes (caja, compensación, efectivo en tránsito)?
8. Maestro de clientes y proveedores con RIF: ¿accesible por el mismo mecanismo? ¿qué cadencia de actualización es aceptable (tiempo real vs. diaria)?
9. House Bank IDs y Account IDs en SAP: ¿cómo obtenemos la correspondencia entre cada cuenta bancaria real y su identificador interno en SAP?

## C. Entrega del extracto bancario hacia SAP

10. (★) Proceso actual de carga del extracto en SAP: FF.5 manual, FEBAN, programa Z propio, flujo BCM, u otro.
11. (★) Formato que SAP acepta hoy: MT940, BAI2, CAMT.053 o formato propio — y un archivo de muestra que se sepa que se procesa correctamente en su sistema.
12. (★) Electronic Bank Statement (EBS): ¿está configurado? ¿reglas de contabilización y tipos de transacción definidos por house bank?
13. Bank Communication Management (BCM): ¿activo? (Viene incluido en EHP 7. Si está activo, cambia el destino de entrega.)
14. Particularidades del MT940 que su EBS interpreta: campos requeridos en `:86:`, manejo de end-to-end IDs, reglas de parseo del descriptor, códigos de transacción personalizados.
15. Un archivo unificado o un archivo por house bank / company code.
16. Cadencia de entrega que SAP espera: tiempo real, lotes durante el día, fin de día.
17. Convención de nombres de archivo que el job de SAP espera.

## D. Canal de entrega

18. (★) Destino de entrega: SFTP del lado de SAP, directorio en el servidor de aplicación, cola de entrada de BCM, o carga manual.
19. Disparador del lado SAP una vez que el archivo aterriza: job programado, BCM, acción de usuario.

## E. Red y acceso

20. Modelo de acceso entrante: VPN, SAP Cloud Connector, lista blanca de IPs, SFTP público.
21. Autenticación: usuario SAP para RFC/OData, usuario HANA de solo lectura, llaves SFTP — qué se puede aprovisionar y quién lo aprovisiona.

---

**Mínimo para cerrar la propuesta comercial:** A1, A2, C10, C11, C12, D18.

Una vez resueltos estos seis puntos podemos enviar la propuesta. El resto se trabaja en sesiones técnicas conjuntas con su equipo Basis / partner SAP.
