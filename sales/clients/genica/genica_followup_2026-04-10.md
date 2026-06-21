---
title: "Follow-up Email — Génica × Tesote (Post-Discovery)"
tags: [sales, genica, email, follow-up]
updated: 2026-04-10
---

**Asunto:** Próximos pasos — Génica × Tesote

---

Hola José, Anaura, Leodardo,

Gracias por la sesión de hoy. Fue una conversación muy rica — salimos con una imagen clara del proceso actual, de lo que necesitan y de cómo Tesote encaja exactamente en la pieza que falta: automatizar la extracción de extractos bancarios y su integración con SAP.

**Puntos clave de la conversación:**

- **El caso de uso es preciso:** El 95% del proceso ya está automatizado en SAP. Tesote cierra el eslabón que falta: la descarga diaria de extractos desde los portales bancarios y su envío automático a SAP en formato JSON vía API — sin intervención manual.
- **Alertas de códigos bancarios:** Acordamos que Tesote notificará en tiempo real cuando un movimiento contenga un código bancario no registrado en SAP, permitiendo al equipo de IT crear el código rápidamente y evitar fallos en la carga. Leodardo, nos comprometemos a compartir los tiempos de respuesta de nuestro equipo técnico para incidencias de este tipo en los próximos días.
- **Infraestructura de seguridad:** Anaura, entendemos que crearán un usuario bancario de sólo lectura para las conexiones de Tesote — esto es exactamente lo que recomendamos. La gestión y administración de usuarios en Tesote queda completamente en manos del equipo de Génica.
- **Timeline estimado:** 4–5 semanas para tener a los usuarios financieros operativos; 5–7 semanas para la integración SAP completa, en paralelo. Total estimado: ~8 semanas desde el arranque.
- **Próxima reunión de propuesta:** Antes de presentar la propuesta formal, nos gustaría confirmar quién del equipo de dirección debería estar en esa conversación para que podamos presentarles el caso de negocio completo.

**Próximos pasos:**

- **José Boscán** — Enviar inventario completo de cuentas bancarias (banco, tipo de cuenta, entidad legal, número de cuenta) lo antes posible. Esto es el insumo principal para dimensionar la propuesta comercial.
- **Anaura Prieto** — Validar y enviar el promedio de transacciones mensuales por banco para el dimensionamiento técnico.
- **Equipo Tecnología Génica (Leodardo / Juan)** — Revisar la documentación técnica de API y seguridad que les enviamos adjunta. Nos avisan cualquier duda o requerimiento adicional.
- **Esteban Suárez (Tesote)** — Confirmar internamente los tiempos de respuesta para gestión de alertas de códigos bancarios nuevos y compartirles la información esta semana.
- **Esteban Suárez (Tesote)** — Preparar propuesta comercial una vez recibido el inventario de cuentas y el volumen de transacciones.

Adjunto el Blueprint Operativo que resume todo lo que conversamos: el contexto, los casos de uso, la arquitectura de integración propuesta y el plan de implementación. Queda abierto para cualquier ajuste o comentario de su parte antes de avanzar con la propuesta formal.

Saludos,

Esteban Suárez
Tesote
esteban.suarez@tesote.com
