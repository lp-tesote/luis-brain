# Banco Exterior — INTERCONEX API Spec

(extracted from vendor PDFs on 2026-05-03; source files in `/tmp/banco-exterior-docs/`)

Banco Exterior C.A. Banco Universal — RIF J-00002950-4. The internal codename for the platform is "Proyecto Zeus." Production environment value is `zeus` for older endpoints (pago móvil, cobros, validar-pago-recibido, anulaciones, listar-movimientos) and `pro` for newer ones (transferencias inmediatas, débito inmediato, listados-bancos, consultas v4, OTP, límites). All endpoints share the same base host `https://wsi.bancoexterior.com` and an `[env]` placeholder in the path.

## 0. Source documents

| PDF (file in `/tmp/banco-exterior-docs/`) | Version | Doc date / last update | Purpose |
|---|---|---|---|
| `Condiciones de Seguridad de la Información (Cliente) v1.1.pdf` | 1.1 | 2021-01-04 | Auth/security model: JWT (HS256) + API Key + OAuth2 + IP whitelist + RSA key exchange |
| `Documento Tecnico - INTERCONEX API REST -listados-bancos v3.pdf` | v3 | 2024-03-12 | List banks (pago móvil and CCE) |
| `Documento Técnico - INTERCONEX API REST - consultar-cuentas v3.pdf` | v3 | 2023-05-11 | Query own accounts + validate third-party FX account |
| `Documento Tecnico - INTERCONEX API REST - listar-movimientos v3.pdf` | v3 | 2025-01-29 | List account movements (pago móvil / FX storage / interbank transfers) |
| `Documento Técnico -  INTERCONEX API REST - transferencias-inmediatas v1.pdf` | v1 | 2024-02-28 | Send instant interbank transfer (debit own account → credit any-bank account) |
| `Documento Técnico -  INTERCONEX API REST - limites-transferencias-inmediatas v1.pdf` | v1 | 2023-03-12 | Query daily/monthly transfer limits & available |
| `Documento Técnico - INTERCONEX API REST - Consultas Transferencias Inmediatas v4.pdf` | v4 | 2025-07-01 | Query status of instant transfers (debit & credit, sent & received) |
| `Documento Técnico - INTERCONEX API REST - consultas-pagos-enviados v1.pdf` | v1 | 2022-05-22 | Query sent pago-móvil payments |
| `Documento Técnico - INTERCONEX API REST - realizar-pago-movil v2.pdf` | v2 | 2020-12-16 | Send pago móvil (with OAuth2 + RSA-signed authorization JWT) |
| `Documento Técnico - INTERCONEX API REST - consultas-limites-pago-movil v1.pdf` | v1 | 2020-10-22 | Query pago-móvil limits per phone (P2C/C2P) |
| `Documento Técnico - INTERCONEX API REST - cobros v1.pdf` | v1 | 2020-10-22 | Pago-móvil collection (debit payer via OTP) |
| `Documento Técnico - INTERCONEX API REST - Cobro Débito Inmediato v1.pdf` | v1 | 2025-07-15 | **Immediate debit (CCE rail) — STRATEGIC for Tesote** |
| `Documento Técnico - INTERCONEX API REST - Solicitud OTP v2.pdf` | v2 | 2025-08-28 | Issue OTP / Clave de Pago for Débito Inmediato (and other CCE ops) |
| `Documento Técnico - INTERCONEX API REST - validar-pago-recibido v2.pdf` | v2 | 2021-10-31 | Validate inbound pago móvil received |
| `Documento Técnico - INTERCONEX API REST - anulaciones-cobros v1.pdf` | v1 | 2020-10-22 | Reverse a cobro (collection) |

The platform is branded **INTERCONEX**, exposed as a **REST API for clientes jurídicos (legal entities / business clients)**. Internal codename is **Zeus**.

---

## 1. Security & authentication conventions

The model is **layered defense**: every call carries 4 separate auth artifacts; transactional calls add a 5th (OAuth2) and pago-móvil specifically adds a 6th (RSA per-tx signature). This is non-trivial.

### 1.1 Required for every endpoint

1. **`Authorization: Bearer <JWT>`** — JWT signed with **HMAC-SHA256 (HS256)**, `typ: "JWT"`, max validity **24 hours**. Bank issues `iss` (issuer ID) and `secretkey` to the affiliated company. Payload: `{ "exp": <unix-timestamp>, "iss": "<assigned-id>" }`. Signature: `HMAC-SHA256(secretkey, base64url(header) + "." + base64url(payload))`. Stateless.
2. **`X-API-Key: <api_key>`** — opaque value issued by the bank.
3. **IP whitelist** — caller must originate from a fixed public IP previously registered with the bank. Mandatory.
4. **HTTPS** on `https://wsi.bancoexterior.com`.

### 1.2 Additional layer for transactional endpoints (PUSH and PULL)

5. **`X-Authorization-OAuth2: <token>`** — a short-lived OAuth2 access token (300 sec / 5 min). Obtained from a dedicated `<base-path>/oauth2/token` endpoint (one per microservice — the OAuth2 path is namespaced under each transactional endpoint). Body: `{ "grant_type": "client_credentials", "client_id": "<id>", "client_secret": "<secret>" }`. Bank issues the `client_id` / `client_secret` confidentially.

### 1.3 Additional layer specifically for `realizar-pago-movil`

6. **`datosAutorizados`** field in the request body — a separate **JWT signed with RSA-SHA512 (RS512)** using a **2048-bit RSA private key the client generates and keeps**. The corresponding public key is delivered to the bank ahead of time (process described in section 1.5). Payload includes `telefonoEmisor`, `cuentaEmisor`, `idBeneficiario`, `telefonoBeneficiario`, `moneda`, `monto`, `exp`. **`exp` must be ≤ 3 minutes from issuance.** This is the bank's substitute for an end-user OTP when the payer is a legal entity (no human at the keyboard to type an OTP).

### 1.4 Three "tokens" delivered by the bank per affiliated client (per "Condiciones de Seguridad" §8)

Per the Condiciones doc, the bank's Information Security division creates **three security artifacts per affiliated client**, delivered via password-protected 7zip/RAR archive over email plus phone-call password:

- API KEY
- JWT (`iss` + `JWT_secret` / `JWT_key`) — for the HS256 daily token
- OAuth2.0 (`client_id` + `client_secret`) — for the per-tx access token

### 1.5 Public-key exchange process (Condiciones §6–7)

For RSA-signed transactional flows (pago móvil, and future flows):

- Client generates a 2048- or 4096-bit RSA key pair, **SHA-512**, X.509, PEM/Base64.
- Example: `openssl req -x509 -nodes -sha512 -days 365 -newkey rsa:2048 -keyout prueba.pem`
- Public key is saved as `.txt`, compressed with 7zip/RAR, encrypted with **AES Crypt** (≥ 16-char password).
- Sent by email to **seguridadlogica@bancoexterior.com** AND **arquitecturay.Soporte@bancoexterior.com**.
- Password is communicated by phone to the bank's authorized personnel.
- Key expiration is at the client's discretion; must be rotated immediately on incident.
- Legal basis: SUDEBAN Resolución 119-10 (No-Repudio).

### 1.6 Environments

| Environment | `[env]` value (newer endpoints) | `[env]` value (older endpoints) |
|---|---|---|
| Development | `des` (Cobro Débito Inmediato, Consultas v4) | n/a |
| Sandbox / QA | `qa` | `qa` |
| Production | `pro` | `zeus` |

**Inconsistency**: Some endpoints (consultas-pagos-enviados, realizar-pago-móvil v2, listar-movimientos v3, anulaciones-cobros, validar-pago-recibido v2, cobros, consultas-limites-pago-movil) use `zeus` for production. Others (transferencias-inmediatas v1, listados-bancos v3, consultas-transferencias-inmediatas v4, Cobro Débito Inmediato v1, Solicitud OTP v2, limites-transferencias-inmediatas v1) use `pro`. Open question for the bank.

### 1.7 Standard auth error responses (consistent across all endpoints)

| HTTP | JSON body | Meaning |
|---|---|---|
| 401 | `{"message": "Connection reset"}` | IP not whitelisted (gateway-level rejection) |
| 401 | `{"message": "Unauthorized"}` | `Authorization` header missing or malformed |
| 401 | `{"message": "Bad token; invalid JSON"}` | JWT is malformed |
| 401 | `{"message": "Invalid signature"}` | JWT signed with wrong secretkey |
| 401 | `{"exp": "token expired"}` | JWT past expiry |
| 401 | `{"exp": "exceeds maximum allowed expiration"}` | JWT exp too far in the future (>24h) |
| 401 | `{"message": "No credentials found for given 'iss'"}` | Unknown `iss` |
| 401 | `{"message": "Invalid authentication credentials"}` | `X-API-Key` invalid |
| 401 | `{"message": "No API key found in request"}` | `X-API-Key` header missing |
| 401 | `Rejected by policy. (from client)` (XML/SOAP envelope) | IP rejected at edge |
| 403 | `{"message": "Your IP address is not allowed"}` | IP not whitelisted (gateway 403) |
| 200* | `{"error_description": "Invalid client authentication", "error": "invalid_client"}` | OAuth2: bad `client_id` / `client_secret`. **Note: returns HTTP 200 even though semantically a failure — gotcha.** |
| 401 | `{"error_description": "The access token is missing", "error": "invalid_request"}` | `X-Authorization-OAuth2` missing |
| 401 | `{"error_description": "The access token is invalid or has expired", "error": "invalid_token"}` | OAuth2 token bad or > 5 min old |
| 429 | `{"message": "API rate limit exceeded"}` | Hourly rate limit hit (where applicable — e.g. listar-movimientos, limites-transferencias-inmediatas: 100 req/hour) |

### 1.8 Common idCanal / idConsumidor pattern

Most endpoints accept a request-body `idCanal` field with two values:
- `01` = the affiliated company is calling directly
- `02` = an authorized integrator is calling on behalf of an affiliated company. Then `idConsumidor` (integrator's RIF) is required.

This permits the bank to host both direct integrations (Tesote → Banco Exterior) and aggregator/reseller integrations (e.g. Tesote acting as integrator for sub-clients).

---

## 2. Reference endpoints

### 2.1 listados-bancos

- **Method/path**: `POST https://wsi.bancoexterior.com/api/[env]/v3/listadosBancos`
- **Purpose**: list banks active in pago móvil (SW7B) ecosystem and/or in the CCE (Cámara de Compensación Electrónica) for interbank transfers.
- **Auth**: JWT + API Key + IP whitelist (no OAuth2 — read-only).
- **Headers**: `Content-Type: application/json`, `Authorization: Bearer <JWT>`, `X-API-Key`.

**Request body**:

| Field | Type | Required | Description |
|---|---|---|---|
| `idCliente` | String(30) | Yes | Client RIF (e.g. `J123456789`) |
| `idUsuario` | String(20) | No | Originating user in client system |
| `idTerminal` | String(20) | No | Originating terminal |
| `idCanal` | String(2) | Yes | `01` direct / `02` integrator |
| `ipOrigen` | String(20) | No | |
| `idConsumidor` | String(20) | Conditional | Required if `idCanal=02` |
| `tipoOperacion` | String(1) | No | `P` pagos (default), `C` cobros — only used for pago móvil list |
| `tipoListado` | Integer | No | `0` pago móvil banks (default), `1` CCE / interbank-transfer banks |
| `tipoPersonaBeneficiario` | String(1) | Conditional | `N`/`J` — required when `tipoListado=0` |

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "OPERACION EXITOSA" },
  "datos": {
    "totalBancos": 23,
    "bancos": [
      { "codigo": 0114, "nombre": "BANCARIBE" },
      ...
    ]
  },
  "comision": { "moneda": "VES", "monto": 0.00 }
}
```

**Error codes**: `0000` OK, `2000` no record, `0007` invalid idCliente, `0009` invalid idCanal, `0035` invalid tipoPersonaBeneficiario, `0048` consumer not authorized for this client, `9999` system error.

### 2.2 consultar-cuentas

- **Method/path**: `POST /api/[env]/v3/consultasCuentas`
- **Purpose**: list active accounts of the affiliated company with current balances.
- **Auth**: JWT + API Key + IP whitelist.

**Request body**: `idCliente` (Yes), `idCanal` (Yes), `idUsuario`, `idTerminal`, `idConsumidor`, `consultaAlmacenamiento` (Boolean, default false — flag for storage account inclusion).

**Response** (per account):

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "datos": {
    "total_cuentas": 3,
    "cuentas": [
      {
        "numero": "01150000000000000000",
        "tipo": "CTE",                  // AHO or CTE
        "moneda": "VES",
        "saldo": 1234567.89,
        "signo": "+"
      }
    ]
  },
  "comision": { "moneda": "VES", "monto": 0.00 }
}
```

**Sub-endpoint `validacionesCuentasTerceros`**: `POST /api/[env]/v3/consultar-cuentas/validacionesCuentasTerceros` — validates a third party's foreign-currency (USD) Banco Exterior account by `documentoIdentidad`. Response: `numero`, `nombreCliente`, `condicionCuenta` (1 = accepts deposits, 2 = does not).

**Error codes**: `0000` OK, otherwise generic `ESTIMADO USUARIO, ERROR EN SISTEMA...` message — error catalog less detailed in this doc.

### 2.3 listar-movimientos

- **Method/path**: `POST /api/[env]/v3/listadosMovimientos`
- **Purpose**: paginated list of account transactions across three flavors.
- **Auth**: JWT + API Key + IP whitelist.
- **Rate limit**: 100 req/hour (data refreshes hourly anyway).

**`tipoListado` controls flavor**:
- `0` (default) — **Pago móvil debit + credit**, paged 500 records/page, ordered ascending by hour. Caller iterates `posicionInicial`. Window: today + 3 prior days; refresh every 30 min.
- `1` — **FX storage transfers** (almacenamiento → cuenta exterior divisas, e.g. for remittance payouts).
- `2` — **Interbank instant transfers** (sent + received), 150 records/page, today + 3 prior days. Adds two extra response fields: `status` of operation and `nombre del banco contraparte`.

**Important quirk**: `idCliente` should be sent as 9 digits with left-zero padding (`V008000000`, `J012000000`).

**Request body**: `idCliente`, `idCanal`, `idUsuario`, `idTerminal`, `fecha` (DD/MM/AAAA, **required**), `cuenta` (20-digit, required), `posicionInicial` (Int, required, default 0), `tipoListado` (Boolean — doc says Boolean but values are 0/2; transcription quirk).

**Response per record** (selected fields):

```
tipo_documento_empresa, numero_documento_empresa, cuenta_empresa,
fecha_operacion, hora_operacion (HH:MM:SS),
naturaleza_transaccion (D/C),
referencia (12), canal, codigo_moneda, monto,
tipo_documento_contraparte, numero_documento_contraparte (12),
telefono_contraparte (12), codigo_banco_contraparte (4),
fecha_contable, hora_contable,
concepto, descripcion
```

**Error codes**: `0000` OK, `2105` cuenta no permitida para consulta, `2000` no record, `0004` fecha not sent, `0005` fecha format wrong, `0023/0024/0025` cuenta validation, `0026/0027` posicionInicial validation.

---

## 3. PUSH — outbound payments

### 3.1 transferencias-inmediatas (send)

- **Auth dance**: client must call **`POST /api/[env]/v1/transferenciasInmediatas/enviar/oauth2/token`** first to mint an OAuth2 access token (5-min lifetime), then call the send endpoint with `X-Authorization-OAuth2`.
- **Method/path**: `POST /api/[env]/v1/transferenciasInmediatas/enviar`
- **Purpose**: instant interbank transfer (CCE rail) — debit from one of the company's accounts, credit any other bank's account.

**Request body** (nested):

```json
{
  "datosPeticion": {
    "idCliente": "J123456789",
    "idSesion": "20260503143015AB",      // 16-char yyyyMMddHHmmSSss
    "idCanal": 1,                          // Integer here (vs String in other endpoints — gotcha)
    "idUsuario": "user01",
    "idTerminal": "term01",
    "idConsumidor": "..."                  // when idCanal=2
  },
  "transferenciaInmediata": {
    "ctaPagadora": "01150000000000000000",   // 20-digit, required
    "ctaReceptora": "01340000000000000000",  // 20-digit, optional
    "codigobancoReceptor": "0134",            // 4-digit, required
    "telefonoReceptor": "04141234567",        // optional, 11-char
    "idReceptor": "V12345678",                // 10-char alphanumeric e.g. "V000000000"
    "monto": 1234.56,                          // Double
    "moneda": "VES",
    "nombreBeneficiario": "Juan Perez",        // up to 50
    "concepto": "..."                          // up to 70
  }
}
```

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "datosTransferenciainmediata": {
    "referencia": "REF12345",   // 15-char
    "fecha": "...",              // 20-char
    "estatus": "..."             // sync OR async — see open question
  }
}
```

**Error codes** (selected — full list ~40 entries):

| Code | HTTP | Meaning |
|---|---|---|
| 0000 | 200 | OK |
| 0001 | 422 | Invalid account format |
| 0002 | 422 | Invalid beneficiary doc |
| 0006 | 422 | Invalid receiving bank code |
| 0011 / 0022 | 422 | Invalid amount format |
| 0013 | 422 | Exceeds max per-tx amount |
| 0020 | 422 | Invalid credit account |
| 0021 | 422 | Invalid debit account |
| 0023 | 422 | Invalid phone |
| 0024 | 422 | Invalid identification format |
| 0025 | 422 | Pagadora == Receptora |
| 0026 | 422 | Exceeds **daily** OR **monthly** limit (same code reused, per doc) |
| 0051 | 422 | Insufficient balance |
| 0424 | 422 | Account closed/blocked/inactive |
| 7777 | 422 | Reversed without response |
| CC02 | 422 | Already reversed |
| CC04 | 422 | Foreign-currency account, not allowed |
| CC05 | 422 | Already applied |
| CC07 | 422 | Issuer ID's client mismatches account's client |
| CC08 | 422 | Beneficiary ID does not exist |
| CC09 | 422 | Invalid beneficiary info |
| 9999 | 500 | Contact support |

**Note**: Important — `idCanal` here is **Integer** type (`1`/`2`) per the doc, while in other endpoints it's String `"01"/"02"`. Suspect inconsistency; confirm with bank.

### 3.2 transferencias-inmediatas — limits

- **Method/path**: `POST /api/[env]/v1/limitesTransferenciasInmediatas`
- **Auth**: JWT + API Key + IP whitelist (read-only, no OAuth2).
- **Rate limit**: 100 req/hour.

**Request body**: `idCliente` (Yes), `idCanal` (Yes).

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "datos": {
    "registro": {
      "limiteTransaccion": 100000.00,
      "limiteDiario": 500000.00,
      "limiteMensual": 5000000.00,
      "acumuladoDiario": 12345.67,
      "acumuladoMensual": 234567.89,
      "disponibleDiario": 487654.33,
      "disponibleMensual": 4765432.11
    }
  }
}
```

**Error codes**: `0000`, `2000` no record, `0007/0009` invalid idCliente/idCanal, `0048` consumer not authorized, `9999` system.

### 3.3 transferencias-inmediatas — status query (Consultas v4)

- **Method/path**: `POST /api/[env]/v4/transaccionesInmediatas/consultas`
- **Purpose**: query status of instant transfers (both debit AND credit, sent AND received) by date + counterparty document; optionally filter by account, contraparte bank, reference, amount.
- **Auth**: JWT + API Key + IP whitelist.

**Request body** (nested under `datosPeticion`):

```
idCliente (e.g. "V10000000", required)
idCanal (Integer, required)
fecha ("YYYY-MM-DD", required)        ← note: ISO format here, vs DD/MM/AAAA elsewhere
documentoContraparte (required)
referencia (optional)
cuenta (optional)
telefonoContraparte (optional)
tipoConsulta ("C" credit / "D" debit, default "C")
otroBanco (Boolean, default true — false = mismo banco intra-Exterior)
bancoContraparte (optional)
monto (optional)
posicionInicial (optional)
```

**Response per operation**: `status`, `fechaOperacion`, `horaOperacion`, `fechaContable`, `moneda`, `monto`, `signoOpr` (+/-), `referencia`, `documentoContraparte`, `telefonoContraparte`, `telefono`, `cuenta` (origin), `cuentaContraparte` (destination), `bancoContraparte`, `concepto`, `descripcion` (e.g. `5723 - CREDITO INMEDIATO ENVIADO` / `5724 - CREDITO INMEDIATO RECIBIDO`), `codMotRechazo`, `motivoRechazo`.

**Error codes**: 0000 OK, 2000 no record, plus 422 validation errors `0001`–`0037` (account/doc/amount/currency/channel formats), `0048` consumer not authorized, `0050` no almacenamiento service, `0051` query only allowed for natural persons (regarding the FX-storage variant), `0301`–`0316` various blank-field errors, `9999` system.

### 3.4 consultas-pagos-enviados

- **Method/path**: `POST /api/[env]/v1/consultas-pagos-enviados`
- **Purpose**: query pago-móvil payments sent by the affiliated company to third parties, paginated 10 records/page, ordered ascending by time.
- **Auth**: JWT + API Key + IP whitelist.

**Request body**: `idCliente`, `idCanal`, `idUsuario`, `idTerminal`, `idConsumidor`, `fecha` (DD/MM/AAAA, required), `telefonoReceptor` (12-char `58XXXXXXXXXX`, required), `idReceptor` (optional), `moneda`, `monto`, `referencia`, `bancoReceptor`, `posicionInicial` (required, default 0).

**Response per record**: `fechaTransaccion`, `horaTransaccion`, `moneda`, `monto`, `signoMonto` (+/-), `referencia`, `bancoReceptor`, `motivoPago`. Plus `total_registros`.

**Error codes**: 0000 OK, 0025 no movements, 0001–0011 validation errors, 0024 client not registered, 0030–0034 nat./céd./tel./fecha/ref. errors, 0047 idCanal missing, 0048 consumer not authorized, 0049 consumer not registered, 1039 client not affiliated to INTERCONEX, 9999 system.

### 3.5 realizar-pago-movil

This is the **most complex auth flow** in the entire API, because it requires the per-tx RSA-signed authorization JWT (since pago móvil is normally OTP-confirmed by a human, but a legal entity has no human at the keyboard).

**Sequence**:

1. `POST /api/[env]/v2/realizar-pago-movil/oauth2/token` → get OAuth2 token (5 min).
2. **Build a separate RSA-SHA512 JWT** containing `telefonoEmisor`, `cuentaEmisor`, `idBeneficiario`, `telefonoBeneficiario`, `moneda`, `monto`, `exp` (≤ 3 min from now). Sign with the company's RSA-2048 private key. The bank verifies with the public key the company shipped beforehand.
3. `POST /api/[env]/v2/realizar-pago-movil` with `Authorization: Bearer <JWT>`, `X-API-Key`, `X-Authorization-OAuth2: <oauth2-token>`, and the RSA-signed JWT inside the body field `datosAutorizados`.

**Request body** (the main call):

```
ip (consumer IP, 20)                    Yes
idCliente (RIF, 30)                      Yes
idCanal ("01"/"02", String(2))           Yes
idUsuario (20)                           No
idTerminal (20)                          No
idOperacion (15) — client's unique tx id  Yes
fechaOperacion ("dd/MM/yyyy HH:mm:ss.SSS") Yes
codigoBanco (4) — beneficiary bank        Yes
nombreBanco (String)                      Yes
concepto (35)                             Yes
datosAutorizados (the RSA JWT, String)    Yes
envioEmailEmisor (Boolean)                Yes
envioEmailBeneficiario (Boolean)          Yes  (only effective if destino is Banco Exterior)
idConsumidor (20)                         when idCanal=02
ipOrigen (20)                             when idCanal=02
```

Example RSA-JWT payload (natural person):

```json
{
  "telefonoEmisor": "58XXXXXXXXXX",
  "cuentaEmisor": "01150000000000000000",
  "idBeneficiario": "V123456789",
  "telefonoBeneficiario": "58XXXXXXXXXX",
  "moneda": "VES",
  "monto": 700.00,
  "exp": 1602946200
}
```

**Response**: `referencia` (12), `comision`.

**Error codes**: 50+ codes, highlights: 0000 OK, 0017 emisor account not affiliated to service, 0033 phone not enabled to pay, 0034 exceeds daily count, 0035 exceeds daily amount, 0036 exceeds per-tx amount, 0037 exceeds monthly count, 0038 exceeds monthly amount, 0040 receptor phone not registered in pago móvil, 0042 idOperacion already used (idempotency!), 0043 invalid signature on `datosAutorizados`, 0044 idBeneficiario == idPagador, 0046 client inactive in pago móvil, 0047 receptor refuses payments, 2026 fund not available, 2052 transaction rejected, 2062 cédula doesn't match beneficiary record, 9998 conciliate manually (response missed — **don't retry**), 9999 system error.

### 3.6 pago-movil — limits

- **Method/path**: `POST /api/[env]/v1/consultas-limites-pago-movil`
- **Purpose**: query pago-móvil limits (per phone, P2C/C2P, separated by natural-vs-legal beneficiary).
- **Auth**: JWT + API Key + IP whitelist (read-only, no OAuth2).

**Request body**: `idCliente`, `idCanal`, `telefonoCliente` (12-char `58XXXXXXXXXX`, required), `idUsuario`, `idTerminal`, `idConsumidor`, `ipOrigen`.

**Response.datos.Limites**:

```
nroCuenta, tipoCuenta, moneda,
cantPagosNaturalesDiaDisp, montoPagosNaturalesDiaDisp,
cantPagosNaturalesDia, montoPagosNaturalesDia,
cantPagosNaturalesMesDisp, montoPagosNaturalesMesDisp,
cantPagosNaturalesMes, montoPagosNaturalesMes,
cantPagosJuridicosDiaDisp, montoPagosJuridicosDiaDisp,
cantPagosJuridicosDia, montoPagosJuridicosDia,
cantPagosJuridicosMesDisp, montoPagosJuridicosMesDisp,
cantPagosJuridicosMes, montoPagosJuridicosMes
```

So the bank tracks separate count + amount caps for **payments TO natural** vs **TO legal** persons, daily and monthly.

**Error codes**: 0000 OK, 0002/0003 phone format, 0032 phone not affiliated, 0034 invalid tx, 0023 user not registered, 0047 idCanal blank, 0048 consumer not authorized.

---

## 4. PULL — inbound collections / debits

### 4.1 cobros (general collections — pago-móvil rail)

- **Method/path**: `POST /api/[env]/v1/cobros`
- **Purpose**: the affiliated company **collects from** its customer using **pago móvil** rail. Customer pre-supplies an OTP (called `otp`/clave dinámica) to the company; company submits with the request.
- **Auth dance**: get OAuth2 first via `POST /api/[env]/v1/cobros/oauth2/token`, then call the main endpoint with `X-Authorization-OAuth2`.

**Request body**:

```
idUsuario (20), idTerminal (20), idCanal (2, req), idConsumidor (20),
idCliente (30, req) — receiving company RIF
ipOrigen (20)
telfReceptor (12, "58...", req) — company's phone in pago móvil
ctaReceptor (20, req) — company's account
idPagador (30, req) — payer's national ID/RIF
telfPagador (12, "58...", req)
moneda (3, req, "VES")
concepto (35, req)
monto (String "0.00", req)
codBanco (4, req) — payer's bank
otp (8, req) — OTP authorized by payer
envioEMailPagador (Boolean, optional, default false)
envioEMailReceptor (Boolean, optional, default false)
```

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "datos": { "referencia": "REF12345678", "serialTransaccion": "12345678901" }
}
```

**Error codes**: 0000 OK, 0014 invalid temporal key, 0017 invalid bank, 0030 service unavailable, 0050 cédulas pagador/receptor must differ, 0051 insufficient funds, 0055 invalid clave, E040 reverse not processable, E046 clave already used, E048 wrong clave, E050 clave expired, 9998 conciliate manually, 9999 system.

### 4.2 Cobro Débito Inmediato — **STRATEGIC** ⭐

This is the endpoint Tesote should evaluate hardest. It's the **immediate-debit / pull** equivalent to an ACH-style debit — but using the Venezuelan CCE rail and an OTP that the *payer* authorizes ahead of time.

- **Method/path**: `POST /api/[env]/v1/debitoInmediato/enviar`
- **OAuth2 path**: `POST /api/[env]/v1/debitoInmediato/enviar/oauth2/token`
- **Purpose** (verbatim from doc): "Permite realizar solicitudes de cobro a **persona naturales** a través de Débito Inmediato, utilizando la categoría de 'Clave de Pago' (OTP)."
- **Auth**: full stack — JWT + API Key + IP whitelist + OAuth2.

**CRITICAL constraint** (from error codes 0021–0024, 0036–0038, and 0018):

| From → To | Allowed? |
|---|---|
| Natural (V/E/P) → Natural | ✅ |
| Natural (V/E/P) → Jurídico (J/G/C) | ❌ — error 0021 |
| Natural (R) → Jurídico (G/C) | ❌ — error 0022 |
| Jurídico (J/C) → Jurídico (G/C) | ❌ — error 0023 |
| Jurídico (G) → Jurídico (G) | ❌ — error 0024 |
| Jurídico (J) → Jurídico (J) | ❌ — error 0036 |
| Jurídico (G) → Jurídico (J) | ❌ — error 0037 |
| Jurídico (J) → Jurídico (G) | ❌ — error 0038 |

**And error 0018 says: "CLIENTE JURIDICO NO PUEDE PROCESAR OTP"** — this is the smoking gun. Read literally, this endpoint **debits a natural-person payer**, even though the cobrador (Tesote) is jurídico. It does NOT support pulling from another business account.

**Request body** (nested):

```json
{
  "datosPeticion": {
    "idCliente": "J123456789",
    "idSesion": "...",
    "idCanal": 1,
    "idUsuario": "...",
    "idTerminal": 0,
    "ipCliente": "...",
    "idConsumidor": "N/A",
    "ipConsumidor": "..."
  },
  "debitoInmediato": {
    "cobrador": {
      "nombre": "Tesote SA",
      "cuenta": "01150000000000000000",  // 20-digit Banco Exterior account, required
      "telefono": "04141234567"          // 11-digit, optional
    },
    "pagador": {
      "pagadorId": "V10000000",          // required
      "nombre": "Juan Perez",            // 45-char, optional
      "cuenta": "01340000000000000000",  // 20-digit, optional — must provide cuenta OR telefono
      "telefono": "04241234567",         // 11-digit, optional
      "bancoCodigo": "0134"              // 4-digit, REQUIRED
    },
    "otp": "12345678",                    // 8-digit, REQUIRED — Clave de Pago authorized by payer
    "monto": 3000.45,                     // Double
    "concepto": "...",                    // 40-char, optional
    "notificar": false,                   // Boolean, optional
    "subproducto": "002"                  // String(3), default "002"
  }
}
```

**`subproducto` values**:
- `001` — Autorización en Línea (real-time per-tx authorization, e.g. the payer approves on the spot)
- `002` — **Clave de Pago (default — OTP per-transaction)**
- `003` — Pago Domiciliado (pre-authorized recurring)

Important: error 0047 says "SUBPRODUCTO NO IMPLEMENTADO" returns HTTP 200 — only `002` is currently confirmed live.

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "debitoInmediato": {
    "monto": 3000.45,
    "estatus": "EN PROCESO",      // OR "APROBADA" — async semantics
    "referencia": "REF12345",     // 8-char
    "fechaOperacion": "16/04/2025",
    "horaOperacion": "15:37:33",
    "concepto": "...",
    "cobrador": { ... },
    "pagador": { ... }
  }
}
```

**Error codes** (~80 entries; selection):

| Code | HTTP | Meaning |
|---|---|---|
| 0007 | 400 | Datos petición missing |
| 0008 | 400 | Cobrador data invalid |
| 0009 | 400 | Pagador data invalid |
| 0010 | 400 | idCliente invalid |
| 0017 | 400 | Invalid amount |
| 0018 | 400 | OTP invalid |
| 0021–0024, 0036–0038 | 400 | Forbidden person-type combinations (see table above) |
| 0031 | 400 | Bank code + cuenta mismatch |
| 0033 | 400 | Pagador cuenta invalid |
| 0034 | 400 | Pagador bank code invalid |
| 0039 | 422 | Cliente no existe |
| 0040 | 422 | Consumer not authorized |
| 0046 | 400 | Subproducto invalid |
| 0047 | 200 | **Subproducto not implemented** (returns 200 OK with this code — must check `resultado.codigo`) |
| 0001–0009 | 200 | Sub-errors from CCE/SIMF backend (cliente no existe, no registrado en pago móvil, cuenta inválida, etc.) |
| 0018 | 200 | **CLIENTE JURIDICO NO PUEDE PROCESAR OTP** — confirms biz-account debit unsupported |
| 0051 | 200 | Insufficient funds |
| 0424 | 200 | Operation not permitted |
| V001 | 200 | OTP already used |
| V002 | 200 | Generate a new OTP |
| V003 | 200 | OTP wrong |
| V004 | 200 | Client blocked |
| V005 | 200 | OTP expired |
| 5000–5028, 1000–1010 | 200 | CCE/SIMF protocol-level field validation errors (numTransac, instrumentoLocal, channel, idMensaje, regId/refPuntoAPunto, bancoDebito/Credito, concepto, etc.) |
| 9999 | 200 | Invalid op code |

**Async-vs-sync**: response `estatus` can be `"EN PROCESO"` or `"APROBADA"` — strongly suggests **the call returns provisional status; final state must be polled** (likely via the Consultas v4 endpoint with `tipoConsulta=D` and `otroBanco=true`).

### 4.3 Solicitud OTP

- **Method/path**: `POST /api/[env]/V2/otp/claves-pagos/creaciones` (note: doc shows path with double-slash `//V2/` — may be typo; verify with bank)
- **Purpose**: generate a Clave de Pago / OTP. If the operation is intra–Banco Exterior, the bank delivers the OTP itself via SMS/Email. If interbank, the bank sends an OTP-issuance request to the receiving (payer's) bank, which is then responsible for delivering it to its customer.
- **Auth**: JWT + API Key + IP whitelist.

**Request body** is **CCE-shaped** (mirrors the SUDEBAN CCE message format):

```
datosPeticion: {
  canal ("01"/"02"),
  canalCore ("15" for Débito Inmediato),
  idUsuario (15), idTerminal (50), idConsumidor, ip, codUsuario,
  idSesion ("YYYYMMddHHmmss"), idCliente (RIF, 30)
},
encabezado: {
  List<datos>: [
    {
      bancoDebito (4-digit CCE bank code),    // payer's bank
      bancoCredito (4-digit CCE bank code),   // collector's bank (Banco Exterior = 0115)
      datosOperacion: {
        instrumentoLocal: "050"  // 050 = DEBITO INMEDIATO
      },
      monto: { montoOperacion: <BigDecimal>, moneda: "VES" },
      cuentaDebito: {
        tipoInstrumento: "CELE"|"CNTA"|"ALIS",  // phone | account | alias
        instrumento: "<value>"                   // 11-digit phone OR 20-digit account
      },
      deudor: {
        nombreEsquema: "SCID"|"SRIF"|"SPAS",   // CÉDULA | RIF | PASAPORTE
        idCliente: "V123456" / "J012000000" / "P..."
      },
      acreedor: { nombreEsquema, idCliente },   // same scheme
      cuentaCredito: { tipoInstrumento, instrumento }
    }
  ]
}
```

Note: List structure suggests **multiple OTPs can be requested in a single call** (or it's there to mirror CCE batch shape).

**Response**: `resultado.codigo` (`0000` OK / `0001` failure) + descripcion. **No OTP value is returned in the response** — the OTP is delivered out-of-band (SMS/email) by the payer's bank.

**Error codes**: `0000` OK, `0001` failed, plus 1001–1036 field-level validation, 2001–2018 MQ/llave-única errors, 2002 client doesn't have llave única, 2003 llave única suspended, 2004 OTP already used, 2005 OTP exists but not yet usable (wait N seconds), 2007 user blocked, 2009/2010 client doesn't have llave única registered, 3002 phone not registered for user, 3003 user unaffiliated, 3005 SMS disabled for channel, 6000 DB error.

### 4.4 validar-pago-recibido

- **Method/path**: `POST /api/[env]/v2/validar-pago-recibido`
- **Purpose**: validate a pago-móvil payment was actually received (currently only validates pago-móvil channel — interbank-transfer validation must use Consultas v4).
- **Auth**: JWT + API Key + IP whitelist.

**Request body**: `id_cliente`, `id_canal`, `id_usuario`, `id_terminal`, `id_consumidor`, `fecha` (DD/MM/AAAA, req), `telefono_emisor` (12-char `58XXXXXXXXXX`, req), `moneda`, `monto`, `referencia`. Note: **field-naming convention here is snake_case** (`id_cliente` vs `idCliente` elsewhere — gotcha).

**Response per record**: `fecha`, `hora`, `cuenta` (receptora), `referencia`, `id_emisor` (may be missing if pago móvil was from another bank), `codigo_banco_emisor`, `canal`, `moneda`, `signo`, `monto`, `motivo`. Plus `total_registros` (max 10 returned per call).

**Error codes**: 0000 OK, 2000 no record, 0001–0010 phone/fecha/moneda/cédula validation, 9999 system.

### 4.5 anulaciones-cobros

- **Method/path**: `POST /api/[env]/v1/anulaciones-cobros`
- **Purpose**: reverse a previously executed cobro (collection from natural person via pago móvil).
- **Auth**: JWT + API Key + IP whitelist (no OAuth2 — interesting; reversal is "within window" so doesn't seem to re-require OAuth2).

**Request body**: same shape as `cobros` (idCliente, telfReceptor, ctaReceptor, idPagador, telfPagador, moneda, monto, codBanco) PLUS `serialOperacion` (11-char — the serialTransaccion returned by the original cobro response). All required.

**Response**:

```json
{
  "resultado": { "codigo": "0000", "descripcion": "..." },
  "datos": { "AnulacionRealizada": true },
  "comision": { "moneda": "VES", "monto": 0.00 }
}
```

**Error codes**: 0000 OK, E040 movement not found, 0030–0035/0047/0048/0049 validation errors, 0032 cuenta inválida, 1039 client not affiliated to INTERCONEX.

---

## 5. Cross-cutting observations

### 5.1 OTP flow

- Pago-móvil cobros (§4.1) and Débito Inmediato (§4.2) both consume an **OTP/clave dinámica that the payer obtains separately** — either from the payer's bank's app (intra-bank) or via SMS/email triggered by §4.3 Solicitud OTP (interbank).
- OTP is **8 digits**.
- OTP semantics: single-use, time-bounded, per-tx. Codes V001 (USADA), V003 (ERRADA), V005 (EXPIRO), 0014 (invalid temporal key), E046 (used), E047 (not available), E048 (wrong), E050 (expired) all confirm this.
- OTP issuance for Débito Inmediato cross-bank flows the bank to the **payer's bank**, which sends the OTP to its customer. So Tesote's customer (paying natural person) gets the SMS from their own bank, not from Banco Exterior.
- **Validity window** is not stated explicitly in any doc — the only timing hint is OTP code 2005 saying "wait N seconds before requesting a new one." Open question.

### 5.2 Biz-account debit support — **THE big gotcha**

- **Cobro Débito Inmediato is restricted to natural-person payers.** Error codes 0018 ("CLIENTE JURIDICO NO PUEDE PROCESAR OTP") and 0021–0024/0036–0038 (forbidden person-type combos) are unambiguous. There is no documented path in any of these 15 PDFs for Tesote (jurídico) to debit another business's account at any bank via INTERCONEX.
- Subproducto `003` = "Pago Domiciliado" (pre-authorized recurring direct debit) hints at an alternate biz-OK path, but error 0047 says "SUBPRODUCTO NO IMPLEMENTADO" — so the docs ship `001` and `003` as enums but only `002` (Clave de Pago) is live.
- Multi-signatory / approval semantics: **not mentioned** in any of the docs.

### 5.3 Settlement / clearing timing

- Pago móvil: **instant** (real-time, SW7B network). Limits + counts query (§3.6) confirms daily and monthly buckets.
- Interbank instant transfers: **instant** (CCE rail). Limits query (§3.2) confirms per-tx, daily, monthly buckets.
- Débito Inmediato: response `estatus` can be `"EN PROCESO"` — **suggests asynchronous** at least in some path. Final state must be polled via Consultas v4.
- Listar-movimientos (§2.3) refreshes data **every 30 minutes** for pago móvil; transfers in tipoListado=2 same window. Open question whether final settlement completes intra-day or T+1.
- "Cutoffs" / business-hours / holiday handling: **not mentioned** anywhere — Débito Inmediato response shape includes `fechaOperacion` "(día hábil o no hábil)" parenthetical, suggesting the service runs 24/7 but actual settlement may differ.

### 5.4 Currency support

- **VES is the dominant moneda** across all transactional endpoints.
- USD is supported only via `validacionesCuentasTerceros` (§2.2) for foreign-currency Banco Exterior accounts and `tipoListado=1` of listar-movimientos (FX-storage transfers).
- Transferencias-inmediatas, pago móvil, cobros, débito inmediato all assume VES (ISO 4217 3-char field, but the only documented value is `VES`).

### 5.5 Idempotency

- **Pago móvil** (§3.5) — has `idOperacion` field; bank rejects with code `0042` if reused. **This is a true idempotency key**.
- **Transferencias inmediatas** (§3.1) — has `idSesion` (16-char yyyyMMddHHmmSSss) — appears to function as request ID but doesn't say re-submit returns the same response. Unclear whether retry-safe.
- **Cobros / Débito Inmediato** — no documented idempotency key. Code `9998` says "ocurrió un error al recibir respuesta — **no intente de nuevo**, realice conciliación de forma manual" — implies the bank cannot guarantee dedup; client must reconcile via the consultas endpoints.
- **Solicitud OTP** — no idempotency key.

### 5.6 Webhooks / callbacks

- **None.** No outbound webhooks documented anywhere. Confirmation is exclusively via:
  - Synchronous response (when available)
  - Email notifications (`envioEMailPagador`, `envioEMailReceptor`, `notificar`, `envioEmailEmisor`, `envioEmailBeneficiario` flags)
  - Polling: Consultas Transferencias Inmediatas v4, listar-movimientos, validar-pago-recibido, consultas-pagos-enviados

### 5.7 Rate limits

- listar-movimientos: 100 req/hour
- limites-transferencias-inmediatas: 100 req/hour
- Other endpoints: not documented — assume reasonable limits but ask.

### 5.8 Other gotchas

- **Field-name inconsistency**: snake_case in `validar-pago-recibido` (`id_cliente`) vs camelCase elsewhere (`idCliente`). Mixed `idCanal` types (Integer in transferencias-inmediatas, String elsewhere).
- **Date format inconsistency**: `DD/MM/AAAA` in older endpoints; `YYYY-MM-DD` in Consultas v4. Plus pago móvil uses `dd/MM/yyyy HH:mm:ss.SSS`.
- **Production env value inconsistency**: `zeus` vs `pro`.
- **HTTP 200 with error in body**: OAuth2 invalid_client returns 200; Débito Inmediato `0047` (subproducto not implemented) returns 200. **Always check `resultado.codigo`**, never trust HTTP status alone.
- **Three separate auth secrets to manage**: `iss`+`secretkey` (HS256 JWT), `X-API-Key`, OAuth2 `client_id`+`client_secret`. Plus an RSA key pair for pago móvil. All delivered out-of-band via AES-Crypt-encrypted email + phone-call password. Onboarding is high-touch.
- **idCliente padding**: should be 9 digits left-padded with zeros (`V008000000`), at least for listar-movimientos. Suspect this applies elsewhere too.
- **Daily JWT rotation**: HS256 JWT must be regenerated daily (24h max). Must be automated.
- **OAuth2 token = 5 minutes**. Must mint fresh per transaction batch.
- **`fechaOperacion` in pago móvil includes milliseconds** — easy to format wrong.

---

## 6. Open questions for Banco Exterior

1. **Biz-account debit**: Is there ANY documented path for Tesote (jurídico) to debit another business's account (jurídico-to-jurídico) via INTERCONEX? The Débito Inmediato error catalog explicitly forbids it. Is `subproducto=003` Pago Domiciliado the answer, and what's its onboarding path? When will it be implemented?
2. **Multi-signatory / approval flow**: For Tesote's own outbound transferencias-inmediatas — is there any built-in multi-approver flow, or does the API assume single-approver and Tesote builds approval upstream of the API call?
3. **`zeus` vs `pro` for production**: Which environment value applies to which endpoint, and is `zeus` being deprecated?
4. **OTP validity window**: How long is a Clave de Pago / OTP valid (in seconds/minutes)? Solicitud OTP doc references "wait N seconds for new" but doesn't state the active-validity duration.
5. **Settlement timing for Débito Inmediato**: When response `estatus = "EN PROCESO"`, what's the typical and worst-case time-to-final-state? Is there a guaranteed intra-day cutoff or could a Friday-evening debit settle Monday?
6. **Subproducto availability**: `subproducto` 001 (Autorización en Línea) and 003 (Pago Domiciliado) — when go-live? Both could unblock B2B.
7. **Idempotency for cobros / débito inmediato**: How does Tesote dedup retries safely? Code 9998 says "do not retry, reconcile manually" — what's the bank's recommended reconciliation API call sequence?
8. **Rate limits beyond the documented two**: Any per-endpoint or per-client tx-rate limits not documented?
9. **Webhooks**: Any roadmap for push-notifications instead of polling?
10. **idCanal type inconsistency** (Integer vs String) in transferencias-inmediatas — is that doc-error or actual API behavior?
11. **USD support**: Beyond the FX-storage and validation flows, can transferencias-inmediatas or débito inmediato move USD?
12. **Pago móvil RSA key vs OAuth2 — why both?** Is it possible to call realizar-pago-móvil with only OAuth2 (i.e., no `datosAutorizados`), or is the per-tx RSA JWT mandatory for every legal-entity call forever?
13. **Onboarding SLA**: The doc describes AES-Crypt + email + phone-password + manual key exchange. What's the typical days-to-go-live once Tesote signs INTERCONEX contract?
14. **Sandbox availability**: Is `qa` (or `des`) available immediately on signing, or does it gate behind production-key issuance?
15. **CCE participating-bank coverage**: The Débito Inmediato doc references CCE-published bank codes. Which Venezuelan banks are CURRENTLY active for inbound débito inmediato? (vs in-network of Banco Exterior alone)
