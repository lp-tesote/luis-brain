# Connect

The original Tesote product. Bank connectivity across multiple jurisdictions (VE, Panamá, RD, EEUU, Caribe).

## Surface

- **Saldos** — account balances. (Old UI label: *Cuentas*.)
- **Transacciones** — transaction sync. (Old UI label: *Movimientos*.)
- **Conexiones bancarias** — credentials, 2FA, sync engine, reliability

## Folders

- [[saldos/]] — Saldos (the accounts page)
- [[kyc-onboarding/]] — KYC + onboarding flows (collection spec, Connect prototype)

## Notes

- Multi-jurisdiction by design — don't assume VE-only when working in this folder.
- Engineering workstreams (sync, recon, self-healing, etc.) live in the shared KB at `knowledge-base/product/bank-connectivity/`. Brain folder is for product-side thinking only.
