---
title: Tesote — Asuntos Legales — Abril 2026
tags: [legal, compliance, 10x, payments, licensing, corporate, es]
updated: 2026-04-22
status: draft
---

# Tesote — Asuntos Legales — Abril 2026

Documento maestro para PTCK Legal. Propósito: **enumerar todo el trabajo legal pendiente, pero dejar absolutamente claro qué bloquea los lanzamientos de producto y qué no.** Los lanzamientos de producto son el eje ordenador para el Q2 de 2026 (nuestra apuesta de 10x en ingresos). Cualquier ítem que no condicione un lanzamiento puede avanzar por un carril más lento.

Clasificación por prioridad. Dentro de cada bloque, los ítems están ordenados aproximadamente por urgencia.

- **P0 — Ruta crítica para el lanzamiento de productos.** No podemos hacer un lanzamiento público sin cerrar estos puntos.
- **P1 — Productos de la siguiente ola.** Aún no están en vivo, pero el alcance y la postura legal deben empezar a trabajarse en paralelo para no quedar bloqueados en el segundo semestre.
- **P2 — Corporativo / estratégico.** Estructura societaria, relación laboral, fiscalidad, licenciamiento en Venezuela y uso de marca. Podemos trabajarlos a un ritmo más pausado, salvo que PTCK Legal identifique un ítem que sea bloqueante para un lanzamiento de producto — en ese caso, se eleva a P0 o P1.

---

## P0 — Ruta crítica para el lanzamiento de productos

**Estos ítems condicionan el lanzamiento público de Pagos + Business (red).** Hasta que se cierren, vendemos de forma discreta, cliente por cliente. Eso es aceptable durante 4–8 semanas. Más allá de ese plazo, se convierte en techo para la apuesta de 10x.

### P0.1 — Pagos (Cobros + Envíos) — lanzándose ahora, lanzamiento público en Q2

**Aclaración estructural importante (a profundizar con PTCK Legal):** técnicamente no somos "socios" de BNC en el sentido tradicional. Nuestra interpretación hoy de la estructura es que actuamos como **socios tecnológicos del cliente final**, y es el cliente (no Tesote) quien solicita a BNC la habilitación del acceso API para pagos. Necesitamos que PTCK Legal caracterice formalmente esta relación tripartita (Tesote ↔ cliente ↔ BNC) y confirme que es defendible regulatoriamente. Varios ítems de abajo dependen de esta caracterización.

**Brecha importante que queremos destacar desde ya:** al día de hoy Tesote **no tiene ninguna práctica formal de AML / KYC / KYB**. Necesitamos trabajar este tema a profundidad con PTCK Legal: qué obligaciones son del cliente, cuáles de BNC, y cuáles debemos construir nosotros dada nuestra ubicación en el flujo.

- [ ] **Caracterización legal de la relación tripartita Tesote ↔ cliente ↔ BNC.** Documentar por escrito nuestra postura: somos proveedor tecnológico del cliente, el cliente es titular de la relación con BNC, Tesote no es contraparte de BNC en la transacción. Validar que esta caracterización se sostiene frente a Sudeban, frente a BNC, y frente a terceros.
- [ ] **Revisión del / de los contrato(s) existentes que involucren a BNC.** Incluso si no hay un "contrato de alianza" formal con BNC, debe haber acuerdos de uso de API, términos de servicio de BNC que el cliente acepta, etc. Inventariar qué está firmado hoy, por quién, y qué cubre.
- [ ] **Postura frente a una relación más formal con BNC en el futuro.** Si eventualmente nos conviene firmar una alianza directa con BNC, ¿qué implicaciones regulatorias tendría (positivas y negativas)? ¿Nos convierte en un actor regulado?
- [ ] **Memorando de postura frente a Sudeban.** Opinión escrita de PTCK Legal: ¿Tesote es una entidad regulada, un proveedor tecnológico, o está sin clasificar? Conclusión: o "no se requiere registro por las razones X" o "estamos tramitando Y, con este cronograma". Este memorando es el entregable más importante de esta asesoría.
- [ ] **AML / KYC / KYB — diseño desde cero.** Hoy no implementamos nada. Necesitamos: (a) mapeo regulatorio de obligaciones — qué le toca al cliente, qué a BNC, qué a Tesote dado nuestro rol de proveedor tecnológico; (b) diseño de las prácticas mínimas que Tesote debe implementar (monitoreo transaccional, flags, escalamientos, retención de evidencia); (c) documentación formal de todo lo anterior. Este es uno de los workstreams más pesados de este engagement.
- [ ] **Diagrama de flujo de fondos (one-pager auditable).** Ruta del dinero: cuenta BNC del pagador → rieles del BCV → cuenta BNC del receptor. **Tesote nunca custodia fondos.** Producir el diagrama y que PTCK Legal lo valide. Es la lámina central de cualquier conversación regulatoria.
- [ ] **T&C para el cliente (payee / receptor).** Términos y condiciones específicos de Tesote Pagos para los clientes que utilicen nuestro enlace para cobrar. Debe reflejar la caracterización tripartita de arriba.
- [ ] **Advertencias / disclosures en pantalla OTP para el pagador.** Lo que ve la persona (y más adelante la empresa) al autorizar el débito con OTP. Debe divulgar quién está debitando, de dónde, y a través de qué riel. PTCK Legal debe validar la redacción exacta.
- [ ] **Política de privacidad / cumplimiento con la LOPPCI.** Datos que capturamos de pagadores (teléfono, identificadores de cuenta, intentos de OTP, metadatos de dispositivo/IP) — retención, tratamiento, y acuerdo de procesamiento de datos con BNC.
- [ ] **Pre-clearance de claims de marketing.** Antes de cualquier lanzamiento público, PTCK Legal pre-aprueba las palabras que podemos usar. No podemos autodenominarnos de formas para las que no estamos licenciados. Divulgaciones tipo "Powered by BNC" — ¿obligatorias?, ¿opcionales? ¿Cuál es la redacción que aceptaría Sudeban?
- [ ] **Plantilla para expansión multi-banco.** Contrato genérico (términos de uso + tratamiento de datos + asignación AML) que podamos aplicar con el Banco #2, #3, #4 sin redactar desde cero cada vez. Necesario antes de iniciar conversaciones con otros bancos.
- [ ] **Manejo de fraudes, contracargos y disputas.** Los débitos autenticados por OTP generalmente son finales, pero conviene documentar el manejo de disputas explícitamente. ¿Cuál es nuestra exposición si un pagador alega no-autorización a pesar del OTP?
- [ ] **Política de comunicación ante incidencias / caídas.** Si BNC se cae, 100% de nuestro volumen de Pagos se cae con ellos. ¿Qué estamos obligados a comunicar, a quién, y en qué plazo?

### P0.2 — Tesote Connect (EN VIVO, parte del producto core)

Conectividad bancaria en vivo con ~95% de los bancos venezolanos. Es ya el cimiento sobre el que corren todos los demás productos, incluyendo ahora Pagos.

**Aclaración operativa importante:** Connect funciona porque **nuestros clientes nos entregan sus credenciales bancarias** para que nuestros algoritmos accedan a sus cuentas y extraigan los datos. Esto es central para entender la exposición legal del producto — no hay API bancaria oficial de por medio, hay un otorgamiento de credenciales por parte del cliente.

**Realidad de ciberseguridad que debe reflejarse en los T&C:** en la práctica es **virtualmente imposible garantizar que los datos no puedan ser filtrados**. Los actores y técnicas de penetración avanzan más rápido de lo que cualquier equipo de ciberseguridad puede absorber. Nuestros T&C **NO pueden ofrecer una garantía absoluta de no-fuga**. Sí pueden — y deben — comprometer que aplicamos todas las medidas y mejores prácticas razonables dentro de lo que está en nuestro poder (encriptación, minimización, controles de acceso, auditoría, etc.). PTCK Legal debe ayudarnos a redactar esta cláusula con precisión: comprometer esfuerzo y mejores prácticas, sin comprometer un resultado que es inalcanzable.

- [ ] **Base legal para el uso de credenciales.** El cliente nos entrega credenciales bancarias voluntariamente para que accedamos en su nombre. Confirmar que nuestro T&C captura este consentimiento con el alcance adecuado, y que la figura es defendible frente a cada banco (aunque sus T&C, técnicamente, prohíban compartir credenciales).
- [ ] **Exposición por acceso no-oficial a sistemas bancarios.** Si algún banco considera que el acceso por credenciales viola sus T&C con el titular de la cuenta, ¿qué exposición tiene Tesote? ¿Y el cliente? Necesitamos un análisis honesto de este riesgo.
- [ ] **Cláusula de seguridad de datos en T&C.** Redactar cláusula que: (a) no prometa no-fuga absoluta; (b) comprometa medidas razonables y mejores prácticas de la industria; (c) limite nuestra responsabilidad ante incidentes de seguridad; (d) documente las obligaciones de notificación al cliente en caso de incidente.
- [ ] **Cobertura contractual de Connect en los T&C del cliente.** ¿Nuestro contrato actual con el cliente cubre realmente lo que Connect hace? Acceso por credenciales, almacenamiento de datos extraídos, retención, derecho del cliente a revocar acceso.
- [ ] **LOPPCI / protección de datos** para información a nivel de cuenta bancaria que fluye a través de Tesote.
- [ ] **Redacción de SLA / compromiso de disponibilidad.** Si Pagos corre sobre Connect, nuestros SLAs se vuelven reales. ¿Qué compromisos contractuales podemos asumir? ¿Cuál es nuestra postura de responsabilidad cuando Connect está degradado?
- [ ] **Cualquier exposición regulatoria por la agregación de datos bancarios** (postura adyacente a open banking en Venezuela). ¿Ve PTCK Legal algún camino en el que Sudeban pueda reclasificar esta actividad?

### P0.3 — Tesote Automations (EN VIVO, parte del producto core)

Automatización del lado del ERP, conciliación y registro contable automático (push de asientos). Es el foso defensivo que hace a Pagos defendible.

- [ ] **Postura en el tratamiento de datos.** Leemos y escribimos datos del ERP del cliente. Confirmar que los T&C del cliente cubren el alcance, la retención y las obligaciones de trazabilidad (audit log).
- [ ] **Acuerdos con proveedores de ERP.** Cualquier contrato con proveedores de ERP (Odoo, SAP, Dynamics, etc.) — ¿estamos en cumplimiento con sus T&C de API y programas de partner?
- [ ] **Responsabilidad por precisión / exactitud.** Si una Automation genera un asiento contable erróneo y la contabilidad del cliente queda equivocada, ¿cuál es nuestro tope de responsabilidad? Debe haber cláusulas de limitación de responsabilidad en los T&C — revisar.
- [ ] **Suficiencia de la traza de auditoría.** Para cualquier cliente auditado (fiscal o de otro tipo), nuestro audit log debe ser defendible. ¿Existe un estándar que deberíamos estar cumpliendo?

### P0.4 — Tesote Business (capa de red)

El enlace de pago es la puerta de entrada a la red. Cada contraparte que recibe un enlace es un usuario potencial de la red. Se lanza junto con Pagos (o poco después). La postura legal debe estar lista cuando el producto lo esté.

- [ ] **T&C para pagadores / contrapartes.** Términos ligeros para un pagador que aterriza en nuestro portal tras recibir un enlace. No es un cliente SaaS, pero está usando nuestra superficie — necesitamos un T&C que lo cubra.
- [ ] **Postura en datos de contrapartes** que nunca hemos onboardeado directamente. ¿Qué datos recolectamos de ellos, y con qué base legal?
- [ ] **Derechos de uso de datos de red.** A medida que la red crece, los datos agregados se vuelven valiosos. Nuestros T&C deben reservar los derechos apropiados para usar datos agregados/anonimizados (preservando limpieza en privacidad).

---

## P1 — Productos de la siguiente ola (alcanzar en paralelo, sin bloquear P0)

Aún no se lanzan, pero la postura legal debe empezar a tomar forma antes de que el equipo de producto avance demasiado. Los asesores pueden trabajar estos ítems en paralelo con P0 si hay capacidad; en caso contrario, se encolan detrás de P0.

### P1.1 — Tesote Capital

Capital es un producto para 2027 en el mejor de los casos. No somos prestamistas — somos un marketplace. La postura legal determina si eso es realmente viable en Venezuela.

- [ ] **Pregunta estructural: ¿podemos orquestar el matching de capital sin ser clasificados como prestamistas, banco o intermediario financiero regulado?** Es la pregunta decisiva para el producto. La respuesta define el diseño entero.
- [ ] **Análisis de licenciamiento.** Si la vía "solo orquestación" no resulta viable, ¿qué licencia(s) necesitaríamos para operar Capital? Ver P2.4 para el análisis de licencias VE — Capital es uno de los drivers principales de ese análisis.
- [ ] **Contratos con partners.** Plantilla para socios de capital (factoring, bancos, family offices, DFIs). Necesitamos una plantilla limpia sobre: compartir datos con el partner, modelo de comisiones, nuestra responsabilidad como orquestador, y postura de exclusividad.
- [ ] **Derechos de uso de datos para underwriting.** Uso de datos de Connect + Automations + Business para alimentar el underwriting de Capital — ¿qué consentimiento / redacción de T&C necesitamos tener HOY para no tener que re-contratar después?
- [ ] **Consideraciones transfronterizas.** Capital proveniente desde fuera de Venezuela (DFIs, family offices extranjeros) — exposición en materia cambiaria, remesas, y antielusión.

### P1.2 — Capa de IA

La IA atraviesa todo el stack (interfaz de power-user sobre Connect + Automations + Business + **Pagos**). No es un producto independiente, pero la postura legal es distinta y está posiblemente sub-analizada. Aplica también a Pagos — por ejemplo, sugerencias automáticas de cobranza, priorización de facturas a enviar por enlace, detección de patrones de pago.

- [ ] **Postura sobre datos de entrenamiento.** ¿Usamos datos del cliente para entrenar modelos? En caso afirmativo, ¿los T&C lo cubren? (La respuesta por defecto debería ser "no entrenamos con datos del cliente" — confirmar y reflejarlo en los T&C.)
- [ ] **Contratos con proveedores de modelos de terceros.** Con quien sea que trabajemos (Anthropic, OpenAI, etc.) — acuerdos de flujo de datos, qué se les envía, retención de su lado, y si eso se divulga a nuestros clientes.
- [ ] **Responsabilidad por el output.** La IA sugiere una acción de cobranza / un asiento contable / un mensaje al cliente. Si está equivocado y el cliente confía en él, ¿cuál es nuestra exposición? Redacción de limitación de responsabilidad.
- [ ] **Postura regulatoria sobre IA en servicios financieros.** Nada específico de Venezuela hoy, pero revisar cualquier guía de Sudeban / BCV que pueda afectar decisiones asistidas por IA. Mantenernos adelantados.
- [ ] **Extensión LOPPCI / privacidad.** Procesamiento por IA de datos financieros del cliente — ¿nuestra postura actual de privacidad lo cubre o debemos actualizarla?

---

## P2 — Corporativo / estratégico (importante, pero puede esperar detrás de P0/P1)

**Guía explícita a PTCK Legal: NO dejen que el P2 condicione los lanzamientos de producto.** Son ítems relevantes con dólares reales en juego, pero si se atrasan un trimestre más mientras P0 sale al mercado, no pasa nada. Si acelerar un ítem de P2 *ayuda* a un lanzamiento (p.ej. una licencia que desbloquea Capital), escalarlo — pero sin inventar dependencias artificiales.

### P2.1 — Estructura corporativa: C-corp de Delaware ↔ entidad venezolana

Estado actual: C-corp de Delaware y una entidad legal venezolana que **no están conectadas legalmente de ninguna forma.** Cero relación de propiedad, cero cadena de cesión de propiedad intelectual (IP), cero acuerdo de servicios. Esto está mal y lo ha estado durante un tiempo.

- [ ] **Recomendar la estructura que conecte ambas entidades.** Opciones típicas: (a) que la entidad VE se convierta en subsidiaria 100% propiedad de la C-corp; (b) acuerdo de servicios entre entidades independientes (cost-plus, defensible en precios de transferencia); (c) alguna otra que PTCK Legal recomiende dado el estado del tratado tributario VE/US (o su ausencia).
- [ ] **Titularidad y cesión de IP.** ¿Quién es titular de la IP hoy — la C-corp, la entidad VE, ambas, ninguna? Construir cadena limpia de cesión de IP desde cada contribuyente → la C-corp (o la entidad que deba titularizar la IP en la estructura objetivo).
- [ ] **Registro de ingresos (revenue booking).** ¿Dónde aterrizan los ingresos de Tesote hoy, dónde *deberían* aterrizar en la nueva estructura, y cuál es el plan de transición?
- [ ] **Implicaciones para inversionistas / board.** El cap table vive a nivel de C-corp. Cualquier reestructuración debe ser limpia para rondas futuras — PTCK Legal debe alertar sobre minas terrestres antes de que exploten.
- [ ] **Timing.** ¿Cuál es la reestructuración limpia más rápida?, ¿cuál la completamente optimizada?, ¿cuál es el delta en costo/tiempo? Elegir según el timeline de levantamiento de capital.

### P2.2 — Relación laboral: equipo venezolano clasificado hoy como contratistas

Estado actual: los miembros del equipo VE cobran como **contratistas de la C-corp de Delaware.** Probablemente mal en varios frentes (derecho laboral venezolano, clasificación tributaria estadounidense, obligaciones de beneficios).

- [ ] **Evaluación de riesgo.** Exposición en VE (reclasificación por derecho laboral, beneficios retroactivos) + exposición en US (misclassification de contratistas, problemas de 1099, retenciones).
- [ ] **Estado objetivo.** ¿Los miembros del equipo VE deben ser empleados de la entidad VE (que a su vez recibe pagos desde la C-corp bajo un contrato de servicios — se conecta con P2.1)? ¿O una solución tipo employer-of-record? ¿O mantenerlos como contratistas con contratos más estrictos? Recomendación dPTCK Legal.
- [ ] **Plan de transición.** Si reestructuramos, hacerlo limpio — mitigación de riesgo retroactivo, nuevos contratos, armado de beneficios. La secuencia importa.

### P2.3 — Estrategia fiscal / tributaria

Apalancada en P2.1 + P2.2, pero merece ser ítem de primer nivel.

- [ ] **Postura tributaria general.** ¿Dónde *realmente* se devenga la utilidad de Tesote hoy, dónde *debería* devengarse dada la naturaleza del negocio, y cuál es la estructura limpia para llegar allí? (US ↔ VE, sin tratado, consideraciones cripto/FX.)
- [ ] **IVA / impuestos indirectos en VE.** Nuestros ingresos por SaaS, Pagos, Capital (futuro) — qué es gravable dónde, a qué tasa, y con qué obligaciones de facturación (consideraciones de imprenta fiscal — ver P2.4).
- [ ] **Precios de transferencia.** Si C-corp ↔ entidad VE es la estructura elegida, el acuerdo intercompañía de servicios debe tener economía defendible en precios de transferencia.
- [ ] **Tributación específica de Pagos.** Cuando cobremos un fee transaccional de Pagos, ¿dónde se registra ese fee y cuál es su tratamiento tributario? Conviene confirmarlo explícitamente — los ingresos de Pagos pueden opacar por mucho a los de SaaS.
- [ ] **Eficiencia tributaria para fundraising.** Cualquier reestructuración que hagamos no debe generar fricción para la próxima ronda.

### P2.4 — Estrategia de licenciamiento en Venezuela

Actualmente operamos bajo las licencias de BNC. Funciona mientras Pagos sea discreto y solo sobre BNC. A medida que nos expandamos (Pagos multi-banco, Capital, lanzamiento público), la pregunta de licencia se vuelve seria.

**Presentar todas las opciones viables + su ROI para cada producto en el roadmap.** Entregable dPTCK Legal: una matriz — licencia × qué desbloquea × costo × tiempo × dificultad. Con esa matriz elegimos.

Opciones a analizar (no exhaustivas — PTCK Legal debe añadir cualquiera que falte):

- [ ] **Licencia de PSP** (proveedor de servicios de pago). ¿Qué nos daría? ¿Nos permitiría operar Pagos de forma independiente de las licencias de BNC? ¿Nos permitiría custodiar fondos? Costo / cronograma / relación requerida con Sudeban.
- [ ] **Licencia fintech** (la figura vigente equivalente en Sudeban / SUDEBAN / BCV — confirmar denominación actual). Alcance mayor, umbral más alto. ¿Vale la pena?
- [ ] **Compra de una "imprenta"** (imprenta digital autorizada por el SENIAT para emitir comprobantes fiscales electrónicos). Utilidad: seríamos dueños de la infraestructura de emisión de facturas en lugar de depender de terceros. Relevante para Tesote como producto interno y potencialmente revendible a nuestros clientes.
- [ ] **Casa de bolsa / licencia de corretaje.** Relevante para Capital — ¿desbloquea una intermediación tipo marketplace? Costo/barreras suelen ser altos; evaluar.
- [ ] **Operador cambiario.** Relevante si alguna vez tocamos FX, stablecoins, o rieles en USD. Fuera de alcance para Pagos v1, pero dimensionar antes de planear v2.
- [ ] **Adquisición de entidades ya existentes.** A veces la vía más rápida es comprar una empresa que ya tenga la licencia. PTCK Legal debe señalar cualquier oportunidad activa.
- [ ] **Alternativas sin licencia propia.** Para cada producto, ¿existe una opción de "operar al amparo de otra entidad licenciada" (como nuestra postura actual con BNC)? ¿Cuáles son los trade-offs vs. obtener licencia propia?

### P2.5 — Marca / uso del nombre

La menor urgencia dentro del P2. Vale la pena levantarla porque está en el mismo bucket de "cosas que debemos dejar bien antes de volvernos grandes".

- [ ] **Postura de marca registrada.** "Tesote" + nombres de producto (Connect, Automations, Payments, Business, Capital) — ¿registrados dónde, en qué clases, con qué postura de enforcement? VE + US como mínimo.
- [ ] **Cumplimiento de uso de marca en marketing.** Cuando digamos "Tesote Payments" públicamente, ¿qué disclosures son obligatorios (ver P0.1)? Esto se cruza entre P0.1 y P2.5 — si un disclosure es un bloqueante duro para el lanzamiento, sube a P0.
- [ ] **Squatting de dominios / handles.** No es un tema legal en sentido estricto, pero PTCK Legal suele tener opinión. Registros defensivos.

---

## Lo que necesitamos dPTCK Legal — orden de secuenciación

1. **Primero, confirmar la clasificación de prioridad.** Si PTCK Legal discrepa sobre que algún ítem esté en P0 vs. P1 vs. P2, señalarlo ahora.
2. **Iniciar P0 de inmediato.** En particular el memorando de postura frente a Sudeban (P0.1) y la revisión del contrato con BNC (P0.1) — están en la ruta crítica del rollout de Pagos para Q2.
3. **Dimensionar P1 en paralelo.** Los entregables pueden ir detrás, pero el scope-of-work debe estar definido para no improvisar en el segundo semestre.
4. **P2.4 (matriz de licenciamiento)** es el ítem de P2 con mayor probabilidad de ser *adelantado* a P0/P1 — si una licencia desbloquea materialmente Capital o Pagos multi-banco, queremos saberlo antes de sobre-invertir en workarounds.
5. **P2.1 + P2.2 + P2.3** son un paquete. Se dimensionan juntos, se planifican juntos, se ejecutan juntos. No resolver uno sin los otros.

---

## Preguntas abiertas / a discutir en el kickoff

- ¿Hay algún ítem de los anteriores donde PTCK Legal considere que ya estamos demasiado expuestos y requiera acción *esta semana* independientemente del orden de prioridad?
- ¿Algo en nuestra operación actual que *no* hayamos listado aquí y que PTCK Legal considere un riesgo relevante que deberíamos conocer?
- Modelo de engagement — ¿por horas, retainer mensual, por entregable? Impacta qué tan agresivamente los saturamos de trabajo.
- Relación con asesores externos existentes (lado US, lado VE) — quién queda, quién se reemplaza, quién coordina.

---

## Notas y enlaces

- Plan de ejecución de estrategia de producto (interno) — framing del lado de producto y master checklist legal del que se deriva este documento.
- Viaje Caracas 2026-04-26 — si alguno de estos trabajos requiere reuniones presenciales con asesores en Caracas, se coordina con la planificación del viaje.
- BNC — estado actual del débito empresarial (doc interno) — estado del push para habilitación de débito a cuenta empresarial con BNC.
