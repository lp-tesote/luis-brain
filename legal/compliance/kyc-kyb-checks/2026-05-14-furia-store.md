---
title: Sanctions Screening — FURIA STORE, C.A.
tags: [legal, compliance, kyc, kyb, sanctions, onboarding]
updated: 2026-05-14
status: draft
---

# Sanctions Screening — FURIA STORE, C.A.

**Context:** new customer onboarding.
**Screened on:** 2026-05-14
**Source document:** `~/Downloads/3. ACTA DE FURIA STORE.pdf` (Acta Constitutiva, 2020-11-17, Registro Mercantil Primero del Distrito Capital, Tomo 23-A, No. 62, expediente 220-65144).
**Database:** [OpenSanctions](https://www.opensanctions.org) — aggregates OFAC SDN, OFAC consolidated non-SDN, EU consolidated, UN consolidated, UK HMT, plus PEP datasets.

## Entity

- **FURIA STORE, C.A.**
- Domicilio: Av. Principal El Hatillo, Centro Comercial Ciudad Tepú, piso 3, Oficinas 314 y 315, Municipio El Hatillo, Estado Bolivariano de Miranda
- Objeto social: comercialización, importación, exportación, compra/venta de motocicletas (Sherco, Yamaha, Suzuki, KTM, Honda, Kawasaki, Beta), partes, accesorios y equipos deportivos
- Capital: Bs. 2.000.000.000,00 (50.000 acciones a Bs. 40.000 c/u)
- Expediente: 220-65144
- Duración: 50 años desde inscripción (2020-11-17)

## Persons screened

| Role | Name | Cédula | Result |
|---|---|---|---|
| Presidente | Jose Abigail Vallera Sosa | V-14.884.596 | No match |
| Vicepresidente | Yorwing Anthony Rodriguez Arteaga | V-18.143.206 | No match |
| Director / Accionista | German Enrique Foucault Ray | V-18.184.429 | No match |
| Director / Accionista | Franchesco Antonio Vona Aschettino | V-18.186.268 | No match |
| Director / Accionista | Jean Carlos Rodriguez Arteaga | V-19.398.185 | No match |
| Comisaria | Carmen Patricia Conde Dugarte | V-13.885.065 | No match |
| Abogado redactor | Carlos Rafael Ojeda Cortesia | V-17.117.475 | No match |

Each shareholder holds 10.000 acciones (20% equity); ownership is split equally across the five founders. Junta Directiva acts mancomunadamente (Presidente + Vicepresidente conjunto).

## Result

**Clean — no matches** against OFAC SDN, EU consolidated, UN consolidated, UK HMT, or PEP datasets via OpenSanctions on 2026-05-14.

## Caveats / what this does NOT cover

- **Adverse media** — OpenSanctions does not screen news/press for fraud, ML investigations, or criminal allegations. For higher-risk tiers, run through ComplyAdvantage or Refinitiv World-Check.
- **OFAC 50% rule** — if any of these individuals owns 50%+ of another *sanctioned* entity, FURIA STORE is blocked by extension. Name-only screening does not catch this; would need beneficial-ownership graph.
- **Spelling variants** — "Franchesco" and "Yorwing" are distinctive; no-match is high-confidence. The Rodriguez Arteagas have common surnames but OpenSanctions runs fuzzy matching by default, so a clean result is still meaningful.
- **Point-in-time** — sanctions lists update constantly. Re-screen at material onboarding milestones and at annual review.

## Recommended next steps

- [ ] Re-run on OFAC's official search (https://sanctionssearch.ofac.treas.gov) and screenshot for the file — belt and suspenders.
- [ ] Apply KYB risk-tier scoring per [[kyc-customer-collection-design]] (Matriz de Evaluación de Riesgo).
- [ ] Collect customer-facing docs per the Ficha checklist (RIF, cédulas, registro mercantil, ISLR, refs).
- [ ] Source-of-funds declaration (Modelo-de-Declaración de Origen de Fondos).
- [ ] Beneficial-owner declaration (Formulario Beneficiario Final) — five founders all sit just below the 25% threshold customarily used; confirm with counsel whether each must be disclosed as BO under our policy.

## Related

- [[kyc-customer-collection-design]] — KYC/KYB design framework
- Tesote KYC policy (`Politica-Conoce-Tu-Cliente-Rev02.docx`) — risk tiers
