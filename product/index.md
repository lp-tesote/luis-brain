# Product

Product ideas, explorations, and hunches before they're specs or PRDs.

Mirrors `knowledge-base/product/` selectively. Promote specs when they're ready for eng.

## Product surfaces

Working taxonomy (not yet fully aligned with eng team — placeholder names):

- [[connect/]] — bank connectivity: cuentas, transacciones, conexiones bancarias. Multi-jurisdiction.
- [[dashboard/]] — the cockpit / cross-product workspace experience
- [[automations/]] — ERP integrations + reports
- [[business/]] — pagos, cobros, counterparties
- [[capital/]] — financing / lending / treasury (placeholder)
- [[ai/]] — AI-native surface (placeholder)
- [[taxes/]] — retenciones / SENIAT / tax compliance

## Cross-product

- [[design/]] — design system, workspace decisions, cross-product UX
- [[confirmation-ladder]] — how Tesote scopes cash-confirmation solutions (real-time API / T-1 API / botón; scraping off the menu). The operating model behind every solution-design conversation.

## Working with the data model

When designing/prototyping, give Claude live access to the Rails app so designs respect the existing data model:

```
claude --add-dir ~/Programming/tesote/treasury
```

Or mid-session: `/add-dir ~/Programming/tesote/treasury`. Schema lives at `treasury/db/schema/05_tables/`, models at `treasury/app/models/`, high-level domain tree in `treasury/CLAUDE.md`.
