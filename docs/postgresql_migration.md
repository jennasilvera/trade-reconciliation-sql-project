# PostgreSQL Migration Notes

This project currently uses SQLite because it is simple to run locally and easy for reviewers to reproduce.

In a production-style trading operations environment, a relational database such as PostgreSQL would be more realistic for storing trade, broker, allocation, and exception data.

This document explains how the project could be migrated from SQLite to PostgreSQL.

---

## Why SQLite Was Used First

SQLite was chosen for the initial version because:

- It requires no database server
- It is easy to run locally
- It keeps the portfolio project simple for reviewers
- It allows the SQL reconciliation logic to be demonstrated quickly
- It avoids unnecessary infrastructure complexity for a student-level project

---

## Why PostgreSQL Would Be More Production-Like

PostgreSQL would be a better long-term option because it supports:

- Stronger data typing
- Multiple users
- Better indexing
- Larger datasets
- More realistic production deployment
- Database roles and permissions
- Better support for scheduled reconciliation jobs
- More advanced SQL features
- Integration with dashboards and orchestration tools

---

## Tables to Migrate

The current SQLite tables would migrate directly into PostgreSQL:

- `internal_trades`
- `broker_trades`
- `internal_allocations`
- `broker_allocations`

The generated reports could also become database tables:

- `trade_exceptions`
- `duplicate_trade_exceptions`
- `allocation_exceptions`
- `reconciliation_summary`

---

## SQLite to PostgreSQL Type Mapping

| SQLite Type | PostgreSQL Type | Usage |
|---|---|---|
| TEXT | VARCHAR or TEXT | IDs, symbols, accounts, source systems |
| INTEGER | INTEGER or BIGINT | Quantities and counts |
| REAL | NUMERIC or DOUBLE PRECISION | Prices, fees, notional values |
| DATE stored as TEXT | DATE | Trade dates and settlement dates |

For financial data, PostgreSQL `NUMERIC` is preferred over floating point types when exact decimal precision matters.

---

## Example PostgreSQL Table Design

```sql
CREATE TABLE internal_trades (
    trade_id TEXT PRIMARY KEY,
    execution_id TEXT NOT NULL,
    trade_date DATE NOT NULL,
    settlement_date DATE NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(18, 6) NOT NULL,
    gross_amount NUMERIC(18, 2) NOT NULL,
    fee NUMERIC(18, 2) NOT NULL,
    net_amount NUMERIC(18, 2) NOT NULL,
    trader TEXT,
    strategy TEXT,
    source_system TEXT
);

CREATE INDEX idx_internal_trades_execution_id
ON internal_trades (execution_id);
