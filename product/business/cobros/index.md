# Cobros

Inbound collections. The mirror of pagos — money flowing toward the Tesote customer.

The outbound half of the command center loop ([[../counterparties/system-of-record]]) runs through here: Tesote routes the invoice → customer pays in the counterparty portal → Tesote reconciles → writeback to Odoo.

- [[outbound-invoice-routing]] — **Outbound invoice routing + payment portal**. The full outbound loop one-pager (routing engine + reconciliation + FX-aware invoicing).
- [[cobros-spec]] — current spec (chase/dunning workflow).
- [[banesco-rails-readiness]] — Banesco rails readiness notes.
- [[2026-05-10-session-banesco-kickoff]] — Banesco kickoff session log.
