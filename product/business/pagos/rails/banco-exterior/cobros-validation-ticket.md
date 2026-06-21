---
title: Validate Banco Exterior INTERCONEX Cobro Débito Inmediato as B2B cobros rail
tags: [payments, banco-exterior, cobros, rails]
updated: 2026-05-03
status: draft
---

# Validate Banco Exterior INTERCONEX Cobro Débito Inmediato as B2B cobros rail

cc daniel for visibility.

## Status

📅 **Drafting — email not yet sent.** Update once sent, then track responses.

## Context

Tesote Pay's MVP is focused on the **cobros leg** — collecting funds from our clients on demand. To do that we need a debit rail that can pull from a client's bank account when authorized.

We're evaluating **Banco Exterior INTERCONEX Cobro Débito Inmediato** as a candidate rail. Banco Exterior shared the full INTERCONEX REST API documentation (Cobro Débito Inmediato v1, dated July 2025), which is technically detailed.

Unlike other vendor specs we've reviewed, the Banco Exterior documentation is unusually explicit about what is **not** supported today. Subproducto `002` (Clave de Pago / OTP) is live, but the error catalog explicitly rejects PJ→PJ combinations (codes `0018`, `0021`–`0024`, `0036`–`0038`). Subproductos `001` (Autorización en Línea) and `003` (Pago Domiciliado / domiciliación) appear in the schema but error `0047` indicates they are not implemented yet.

This ticket captures what we understood, what's still unclear, and the email going to Banco Exterior to close the gaps that block a feasibility decision.

## What we understand from the materials

INTERCONEX Cobro Débito Inmediato is a two-call flow:

1. `POST /api/[env]/v1/debitoInmediato/enviar/oauth2/token` — obtain a 5-minute OAuth2 access token (in addition to the daily JWT and the static API Key)
2. `POST /api/[env]/v1/debitoInmediato/enviar` — execute the debit, requires the payer's OTP and the chosen `subproducto`

Authentication: the merchant (Tesote, jurídico) authenticates via three layered credentials issued by Banco Exterior — HS256 JWT seed (24h validity), static API Key, and OAuth2 client_credentials (5min token) — plus IP whitelisting. The payer authorizes each individual debit by providing a one-time password. Under subproducto `002` ("Clave de Pago"), the OTP is generated and delivered by the **payer's own bank**, not Banco Exterior.

Subproducto enum:

- `001` Autorización en Línea — listed but error `0047` ("subproducto no implementado")
- `002` Clave de Pago — live; restricted to natural-person payers per the endpoint description and the error catalog
- `003` Pago Domiciliado (recurring / standing-mandate) — listed but error `0047`

The schema accepts `pagadorId` with prefixes `V/E/P/J/G/C/R`, so business-account payers (`J`, `G`, etc.) are nominally addressable. But error codes `0021`–`0024` and `0036`–`0038` reject every PJ→PJ combination today, and code `0018` ("CLIENTE JURIDICO NO PUEDE PROCESAR OTP") explicitly says jurídico clients cannot process OTPs. The `bancoCodigo` field accepts any valid Venezuelan bank code, suggesting the rail is not Banco Exterior–only — but this isn't stated.

## Open questions (going to Banco Exterior)

Four questions are blocking a feasibility decision:

1. **Can subproducto `002` work for PJ payers, today or in the near term?** Schema accepts `J/G/C/R`-prefixed `pagadorId`, but errors `0021`–`0024` and `0036`–`0038` reject every PJ→PJ combination, and error `0018` says jurídico clients cannot process OTPs. Is this a Banco Exterior product policy, a BCV/CCE rail-level restriction, or regulatory? Is there a roadmap to enable PJ→PJ in `002`, and on what timeline?

2. **How does single-OTP authorization work on PJ accounts with firmas mancomunadas?** Most Venezuelan PJ accounts require multiple signatures. If/when `002` opens to PJ payers, to which authorized signer does Banco Exterior deliver the OTP, and is one OTP sufficient — or is a different mechanism (multi-OTP, in-app approvals, etc.) required for mancomunadas accounts?

3. **Interbank reach.** Can a Tesote PJ account at Banco Exterior (the recaudador) debit PJ accounts held at **other Venezuelan banks** via Cobro Débito Inmediato? The `bancoCodigo` field accepts any valid bank code, but the documentation doesn't make the interbank vs. intrabank scope explicit.

4. **Subproductos `001` (Autorización en Línea) and `003` (Pago Domiciliado).** Both appear in the schema but return error `0047`. Two parts: (a) what is "Autorización en Línea" (`001`), how does it differ from Clave de Pago, and when does it go live? (b) what is the roadmap and product spec for Pago Domiciliado (`003`)? Since `003` uses a mandate-based authorization (not per-transaction OTP), the `0018` restriction logically should not apply — does that mean `003` will support PJ payers from day one?

---

## Email — English (record copy)

**Subject:** Technical questions — Cobro Débito Inmediato (INTERCONEX) for B2B collections

Hi [contact name],

Thanks for sharing the INTERCONEX documentation, including Cobro Débito Inmediato (v1, July 2025). We've reviewed it in depth and it looks like a strong foundation for the **collections** side of Tesote Pay.

Before we scope the integration on our side, we have four focused questions specifically about using the rail for **B2B cobros** — i.e., debiting our clients' business accounts. Happy to receive written responses or cover these in a short technical call, whichever is easier for your team.

1. **PJ as payer in subproducto `002`.** The schema accepts `pagadorId` with `J/G/C/R` prefixes, but error codes `0021`–`0024` and `0036`–`0038` reject every PJ→PJ combination, and error `0018` ("CLIENTE JURIDICO NO PUEDE PROCESAR OTP") indicates jurídico clients cannot process OTPs today. Is this a Banco Exterior product policy, a BCV/CCE rail-level restriction, or regulatory? Is there a roadmap to enable PJ→PJ in `002`, and on what timeline?

2. **OTP authorization on PJ accounts with firmas mancomunadas.** Most PJ accounts in Venezuela require firmas conjuntas. If/when `002` supports PJ payers, how is the single-OTP authorization compatible with a multi-signer account? To which authorized signer is the OTP delivered, and is one OTP sufficient — or is a different mechanism (multi-OTP, panel approvals, etc.) required for mancomunadas accounts?

3. **Interbank reach.** Can a Tesote business account at Banco Exterior (acting as recaudador) debit PJ accounts held at **other Venezuelan banks** via Cobro Débito Inmediato? The `bancoCodigo` field accepts any valid Venezuelan bank code, but the documentation doesn't make the interbank vs. intrabank scope explicit.

4. **Subproductos `001` (Autorización en Línea) and `003` (Pago Domiciliado).** Both appear in the schema but return error `0047` ("subproducto no implementado"). Two questions: (a) What is Autorización en Línea (`001`), how does it differ from Clave de Pago, and when does it go live? (b) What is the roadmap and product spec for Pago Domiciliado (`003`)? In particular, since `003` uses a mandate-based model rather than per-transaction OTP, can it support PJ payers from day one?

These four answers will tell us whether Banco Exterior can serve as one of our primary B2B collections rails or whether we need to design around specific limits.

Thanks,
Luis Pulgar
CEO, Tesote
[luis@tesote.com](mailto:luis@tesote.com)

---

## Correo — Español (versión a enviar)

**Asunto:** Preguntas técnicas — Cobro Débito Inmediato (INTERCONEX) para cobros B2B

Hola [nombre del contacto],

Gracias por compartir la documentación de INTERCONEX, incluyendo Cobro Débito Inmediato (v1, julio 2025). Ya la revisamos a fondo y nos parece una base sólida para el lado de **cobros** de Tesote Pay.

Antes de cerrar el alcance de la integración por nuestro lado, tenemos cuatro preguntas puntuales sobre el uso del rail específicamente para **cobros B2B** — es decir, debitando las cuentas empresariales de nuestros clientes. Quedamos atentos a respuestas por escrito o, si lo prefieren, agendamos una llamada técnica corta — lo que sea más cómodo para su equipo.

1. **PJ como pagador en subproducto `002`.** El esquema acepta `pagadorId` con prefijos `J/G/C/R`, pero los códigos de error `0021`–`0024` y `0036`–`0038` rechazan toda combinación PJ→PJ, y el código `0018` ("CLIENTE JURIDICO NO PUEDE PROCESAR OTP") indica que los clientes jurídicos no pueden procesar OTPs hoy. ¿Es una restricción a nivel de producto de Banco Exterior, del rail BCV/CCE, o regulatoria? ¿Hay un roadmap para habilitar PJ→PJ en `002`, y en qué horizonte?

2. **Autorización vía OTP en cuentas PJ con firmas mancomunadas.** La mayoría de las cuentas PJ en Venezuela requieren firmas conjuntas. Si/cuando `002` soporte pagadores PJ, ¿cómo se compatibiliza la autorización por OTP único con una cuenta multi-firmante? ¿A cuál firmante autorizado se entrega el OTP, y un solo OTP basta, o se requiere un mecanismo distinto (multi-OTP, aprobaciones en panel, etc.) para cuentas mancomunadas?

3. **Alcance interbancario.** ¿Una cuenta empresarial de Tesote en Banco Exterior (actuando como recaudador) puede debitar cuentas PJ en **otros bancos venezolanos** a través de Cobro Débito Inmediato? El campo `bancoCodigo` acepta cualquier código de banco válido, pero la documentación no hace explícito si el alcance es interbancario o solo intra-Banco Exterior.

4. **Subproductos `001` (Autorización en Línea) y `003` (Pago Domiciliado).** Ambos aparecen en el esquema pero devuelven el código `0047` ("subproducto no implementado"). Dos preguntas: (a) ¿Qué es Autorización en Línea (`001`), en qué se diferencia de Clave de Pago, y cuándo entra en producción? (b) ¿Cuál es el roadmap y la especificación de producto para Pago Domiciliado (`003`)? Particularmente, como `003` usa un modelo de mandato (no OTP por transacción), ¿podrá soportar pagadores PJ desde el día uno?

Estas cuatro respuestas nos permitirán definir si Banco Exterior puede ser uno de nuestros rails principales de cobros B2B o si necesitamos diseñar alrededor de limitaciones específicas.

Gracias,
Luis Pulgar
CEO, Tesote
[luis@tesote.com](mailto:luis@tesote.com)
