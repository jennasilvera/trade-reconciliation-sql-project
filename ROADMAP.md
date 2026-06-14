# Roadmap

This roadmap lists possible future enhancements for the Trade Reconciliation SQL Project.

The current version is portfolio-ready and uses simulated data only.

---

## Current Version

The current version includes:

- Simulated trade and allocation data
- SQLite database workflow
- SQL reconciliation logic
- Trade, duplicate, allocation, lifecycle, manifest, and data quality reports
- pytest validation
- GitHub Actions CI
- Documentation, runbooks, ERD, architecture diagrams, and assumptions

---

## Future Enhancements

| Enhancement | Priority | Description |
|---|---|---|
| PostgreSQL migration | Medium | Move from SQLite to PostgreSQL for a more production-like database |
| Docker Compose | Medium | Add reproducible local infrastructure for PostgreSQL |
| Streamlit dashboard | Medium | Build a simple dashboard for reviewing exception reports |
| Exception aging | Medium | Track how long exceptions have remained open |
| SLA breach detection | Medium | Flag exceptions that exceed SLA thresholds |
| Historical reconciliation runs | Medium | Store multiple reconciliation run dates |
| Ticket-style assignment | Low | Add assigned owner, comments, and resolution workflow |
| Multi-asset simulation | Low | Add futures, FX, options, or fixed income examples |
| Order/fill lifecycle | Low | Add order, route, fill, cancel, and correction events |
| FIX-style message simulation | Low | Simulate simplified FIX-like execution messages |

---

## Design Principles for Future Work

Future improvements should preserve the current project goals:

- Use simulated data only
- Avoid claiming professional trading systems experience
- Keep the project easy to run locally
- Prioritize SQL, reconciliation logic, and operational clarity
- Maintain clear documentation and tests
