# Banesco — Q&A on B2B cobros (2026-05-03 → 2026-05-04)

Email exchange with Grecia (Banesco) on the four open questions about Cargo en Cuenta for B2B collections. Questions sent 2026-05-03; responses received 2026-05-04. Luis followed up the same day with a strategic reframe and call request — Grecia offered slots for **Wed 2026-05-06**.

## Status

📞 **Call scheduled (pending slot confirmation): Wed 2026-05-06, 9:00 AM or 11:00 AM** (Grecia offered both, Luis to pick).

**Call agenda — set by Luis's follow-up email:** strategic, not technical. The point is to learn how Banesco is thinking about the **interbank PJ→PJ debit space** (priorities, timing, alternatives) so Tesote can decide whether Banesco is the consolidation partner for the cobros leg or whether Tesote needs to design around them.

## 1. PJ as payer

**Q.** The schema accepts `customerIdType: "J"`. Does the rail work in production today with PJ payers? Are there clients operating that flow currently?

**A.** ✅ Yes (both). The flow is live in production and clients are operating it today.

## 2. OTP authorization on PJ accounts with firmas mancomunadas

**Q.** How is single-OTP authorization compatible with multi-signer accounts? To which authorized signer is the OTP delivered, and is one OTP sufficient — or is a different mechanism required?

**A.** The API requests the OTP (Clave Dinámica) and validates against the **devices the client has registered** with Banesco. **One OTP is sufficient** to authorize the debit on mancomunadas accounts.

## 3. Interbank reach

**Q.** Can a Tesote PJ account at Banesco (recaudadora) debit PJ accounts held at other Venezuelan banks via Cargo en Cuenta or any equivalent apificada product? If not, what's the recommended path?

**A.** ❌ No. Banesco currently has **no API service that allows debit to other banks**. The recommended path is **Débito Inmediato**, which is currently under analysis by TI BBU. Expected availability: **Q3 2026** (not committed).

## 4. Other debit rails

**Q.** Beyond Cargo en Cuenta, does Banesco offer other apificada debit capabilities — in particular domiciliación or any standing-authorization / recurring-debit mechanism that doesn't require a customer OTP per transaction?

**A.** 🆕 New product launched in production the **week of 2026-04-27**: **"Pagos por notificaciones push" / "Solicitar Pago Móvil"** — sends bulk payment requests via API to paying clients. Banesco provided the technical docs and a product presentation.

> Note: this is a payment-request flow (push notification → client approves), not a true debit pull or domiciliación. No per-transaction OTP, but the client still has to act. Worth a separate evaluation as a complementary collection UX.

---

## Bottom line (Luis's read)

- OTP juridico→juridico **intrabank**: yes, live and working.
- OTP juridico→juridico **interbank**: no, Q3 via Débito Inmediato.

---

## Original email — Grecia (2026-05-04, in Spanish, for the record)

> Luis, sobre los puntos que mencionaste, te comento las respuestas en color azul:
>
> **PJ como pagador.**
> El esquema acepta `customerIdType: "J"`. ¿El riel funciona hoy en producción con pagadores PJ? **Si.** ¿Hay clientes operando ese flujo actualmente? **Si.**
>
> **Autorización vía OTP en cuentas PJ con firmas conjuntas.**
> ¿Cómo se compatibiliza la autorización por OTP único con una cuenta de múltiples firmantes? ¿A cuál firmante autorizado se entrega el OTP? **Parte de la lógica del api es que solicita la OTP (Clave Dinámica) y realiza la validación según los dispositivos que tenga registrado el cliente.**
> ¿Un solo OTP basta para autorizar el débito, o se requiere un mecanismo distinto para cuentas mancomunadas? **Si.**
>
> **Alcance interbancario.** Por lo que entendemos de la documentación, Cargo en Cuenta opera solo Banesco→Banesco. **Si.**
> ¿Una cuenta empresarial en Banesco (actuando como recaudadora) puede debitar cuentas PJ en otros bancos a través de este riel, o de algún producto apificado equivalente? **No, actualmente no contamos con un servicio vía API que permita el débito a otros Bancos.**
> Si no es vía Cargo en Cuenta, ¿cuál sería el camino recomendado? **Vía Débito Inmediato. Actualmente esta API se encuentra en análisis por parte de TI BBU, esperamos tenerla para el T3.**
>
> **Otros rieles de débito.**
> Más allá de Cargo en Cuenta, ¿Banesco ofrece otras capacidades apificadas de débito que debiéramos conocer — en particular domiciliación o algún mecanismo de autorización permanente / débito recurrente que no requiera OTP del cliente por cada transacción? **La semana pasada salió a producción el servicio Pagos por notificaciones push (Solicitar Pago Móvil), el cual permite enviar solicitudes de pago masivo vía API a los clientes pagadores. Adjunto el documento técnico y la presentación del servicio.**

---

## Follow-up — Luis's reply (2026-05-04, requesting a call)

> Hola Grecia,
>
> Gracias por las respuestas y por la documentación, nos dejan muy claro lo que está disponible hoy y lo que viene pronto.
>
> Quisiera proponerte una llamada para profundizar en el siguiente paso. Puedo por WhatsApp al +1 (617) 584-9897 o por Google Meet, lo que prefieras. Tienes disponibilidad hoy o mañana?
>
> En el centro de nuestro modelo está el objetivo de que los clientes de Tesote canalicen toda su recaudación a través de Banesco. Para que eso funcione a escala, es crítico poder debitar fondos desde cuentas PJ en otros bancos —vía domiciliación o vía OTP— y consolidarlos en la cuenta Banesco del cliente recaudador.
>
> Lo que vimos en sus respuestas sugiere que ese caso aún no tiene un riel apificado disponible (Cargo en Cuenta opera intra-Banesco, Débito Inmediato está en análisis con horizonte T3, y no hay API de domiciliación / autorización permanente). Queremos entender mejor cómo Banesco está pensando ese espacio: prioridades, tiempos, posibles alternativas. Con eso podemos decidir con claridad si el modelo encaja con su hoja de ruta o si debemos abordar el problema de otra forma.

**Strategic frame to remember on the call:**

- The pitch is consolidation: clients route 100% of their collections to a Banesco account.
- That only works if Banesco can debit clients' PJ accounts at **other banks** (via OTP or domiciliación) and consolidate at Banesco.
- Today none of Banesco's apificadas cover that case. Cargo en Cuenta = intra-Banesco only. Débito Inmediato = Q3 horizon (in TI BBU analysis). Domiciliación = not apificada.
- Decision the call should inform: is Banesco the consolidator, or do we design around them?

## Grecia's response — call slots offered (2026-05-04)

> Buen día, un gusto saludarles
> Luis contamos con disponibilidad para el miércoles 06/05 a las 9:00 am u 11:00 am
> Quedamos atentos a tus comentarios

**Action:** Luis to pick 9:00 AM or 11:00 AM on Wed 2026-05-06 and send the meeting link (WhatsApp or Google Meet).
