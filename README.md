# Trade Reconciliation SQL Project

A simulated SQL-based trade reconciliation workflow designed to demonstrate trading operations, production support, and data investigation skills for systematic trading, hedge fund, and capital markets operations roles.

This project uses **Python, SQL, SQLite, pandas, and CSV reports** to simulate how a trading operations analyst might reconcile internal trade bookings against broker-reported trades and allocation records.

> This is a portfolio project using simulated data only. It does not use real broker, OMS, EMS, FIX, fund, client, or proprietary trading data.

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
├── data/
│   ├── raw/
│   └── reports/
├── docs/
│   └── project_walkthrough.md
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_reconciliation_views.sql
│   └── 03_exception_queries.sql
├── src/
│   ├── config.py
│   ├── generate_data.py
│   ├── load_database.py
│   └── run_reconciliation.py
└── tests/
    └── test_reconciliation_outputs.py
