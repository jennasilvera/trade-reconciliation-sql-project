# Trade Reconciliation SQL Project

[![Trade Reconciliation CI](https://github.com/jennasilvera/trade-reconciliation-sql-project/actions/workflows/ci.yml/badge.svg)](https://github.com/jennasilvera/trade-reconciliation-sql-project/actions/workflows/ci.yml)

A simulated SQL-based trade reconciliation workflow designed to demonstrate trading operations, production support, and data investigation skills for systematic trading, hedge fund, and capital markets operations roles.

This project uses **Python, SQL, SQLite, pandas, and CSV reports** to simulate how a trading operations analyst might reconcile internal trade bookings against broker-reported trades and allocation records.

> This is a portfolio project using simulated data only. It does not use real broker, OMS, EMS, FIX, fund, client, or proprietary trading data.

---

## Project Highlights

- Simulates internal trade bookings, broker trade records, and account-level allocation files
- Detects trade-level, duplicate, allocation, settlement, fee, and lifecycle exceptions
- Uses SQL views and queries to reconcile internal records against broker records
- Generates CSV exception reports, data quality reports, manifests, and lifecycle/SLA reports
- Includes pytest validation and GitHub Actions CI
- Documents the workflow with runbooks, architecture diagrams, ERD, controls matrix, and assumptions

---

## Quick Start

Run the full project workflow locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make check
```

The `make check` command regenerates simulated data, loads the SQLite database, runs reconciliation logic, builds reports, validates data quality, generates manifests, updates documentation previews, and runs the test suite.

---

## Project Objective

The goal of this project is to demonstrate the ability to:

- Pull, join, and reconcile trade data across multiple sources
- Investigate trade breaks using SQL
- Detect missing trades, booking discrepancies, and broker mismatches
- Review order, fill, trade, and allocation-level records
- Generate operational exception reports
- Build repeatable reconciliation controls
- Present a realistic trading operations workflow in a recruiter-friendly GitHub project

---

## Business Context

Trading operations teams are responsible for ensuring that internally booked trades match external broker or counterparty records. When records do not match, the discrepancy is called a **trade break**.

Trade breaks can affect:

- Settlement
- P&L reporting
- Risk reporting
- Portfolio accounting
- Client reporting
- Downstream operational workflows

This project simulates a daily reconciliation process where internal trade records are compared against broker trade records to identify exceptions.

---

## Tech Stack

- Python
- SQL
- SQLite
- pandas
- CSV
- pytest
- Git/GitHub

---

## Repository Structure

```text
trade-reconciliation-sql-project/
├── README.md
├── Makefile
├── requirements.txt
├── LICENSE
├── CHANGELOG.md
├── ROADMAP.md
├── .github/workflows/ci.yml
├── data/
│   ├── raw/
│   └── reports/
├── docs/
│   ├── README.md
│   ├── project_walkthrough.md
│   ├── architecture.md
│   ├── schema_erd.md
│   ├── data_dictionary.md
│   ├── sample_report_preview.md
│   ├── sql_investigation_examples.md
│   ├── break_investigation_runbook.md
│   ├── daily_reconciliation_runbook.md
│   ├── reconciliation_controls_matrix.md
│   ├── exception_lifecycle_sla_guide.md
│   ├── reconciliation_tolerance_policy.md
│   ├── postgresql_migration.md
│   ├── assumptions_and_limitations.md
│   └── project_quality_checklist.md
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_reconciliation_views.sql
│   ├── 03_exception_queries.sql
│   └── 04_investigation_queries.sql
├── src/
│   ├── generate_data.py
│   ├── load_database.py
│   ├── run_reconciliation.py
│   ├── run_data_quality_checks.py
│   ├── build_exception_lifecycle_report.py
│   ├── build_input_manifest.py
│   ├── build_report_manifest.py
│   └── export_report_preview.py
└── tests/
    ├── test_reconciliation_outputs.py
    ├── test_expected_break_types.py
    ├── test_data_quality_checks.py
    ├── test_exception_lifecycle_report.py
    ├── test_input_manifest.py
    ├── test_report_manifest.py
    ├── test_sql_investigation_queries.py
    └── test_documentation_links.py
```

---

---

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for future enhancement ideas.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes and project history.

## License

This project is released under the MIT License.

See [LICENSE](LICENSE) for details.

