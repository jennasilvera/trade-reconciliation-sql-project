# Trade Reconciliation SQL Project Walkthrough

## 1. Business Problem

Trading operations teams need to confirm that internal trade records match broker-reported executions and allocation files. If the internal system and broker records disagree, the break must be identified, investigated, and resolved before downstream processes such as settlement, P&L, risk, and reporting are affected.

This project simulates that workflow using Python, SQL, SQLite, pandas, and CSV-based exception reports.

## 2. Data Sources

The project uses simulated data only.

### Internal Trade Bookings

`data/raw/internal_trades.csv`

Represents trades booked internally by a simulated investment or trading system.

### Broker Trade Records

`data/raw/broker_trades.csv`

Represents trades reported by a simulated broker or execution venue.

### Internal Allocations

`data/raw/internal_allocations.csv`

Represents account-level allocations from the internal side.

### Broker Allocations

`data/raw/broker_allocations.csv`

Represents account-level allocations from the broker side.

## 3. Reconciliation Workflow

The workflow follows this sequence:

1. Generate simulated trade and allocation data.
2. Load CSV files into a SQLite database.
3. Join internal and broker records by execution ID.
4. Detect missing, mismatched, duplicate, and allocation-level breaks.
5. Export CSV exception reports.
6. Summarize exceptions by break type.

## 4. Break Types Detected

The reconciliation identifies:

- Missing broker trade
- Missing internal booking
- Quantity mismatch
- Price mismatch
- Side mismatch
- Symbol mismatch
- Fee mismatch
- Settlement date mismatch
- Allocation account mismatch
- Duplicate internal trade
- Duplicate broker trade

## 5. SQL Logic

The SQL logic is organized into three files:

- `sql/01_create_tables.sql`
- `sql/02_reconciliation_views.sql`
- `sql/03_exception_queries.sql`

The main reconciliation process uses SQL joins, `CASE` logic, grouping, and exception classification to identify differences between internal and broker records.

## 6. Output Reports

The project creates the following reports:

- `data/reports/trade_exceptions.csv`
- `data/reports/duplicate_trade_exceptions.csv`
- `data/reports/allocation_exceptions.csv`
- `data/reports/reconciliation_summary.csv`

These reports simulate the type of output a trading operations analyst might review during daily trade reconciliation.

## 7. How This Maps to Trading Operations

This project demonstrates practical skills relevant to trading operations and production support:

- Pulling and joining data across multiple sources
- Investigating trade breaks
- Reconciling internal and external records
- Detecting booking and broker discrepancies
- Creating repeatable operational controls
- Producing clear exception reports
- Using SQL to investigate issues without waiting on engineering support

## 8. Limitations

This is a simulated portfolio project. It does not use real broker, OMS, EMS, FIX, fund, client, or proprietary trading data.

The purpose is to demonstrate understanding of reconciliation workflows, SQL investigation techniques, and operational control design using realistic simulated data.

## 9. Future Enhancements

Potential improvements include:

- PostgreSQL version
- Docker Compose setup
- Streamlit dashboard
- Scheduled reconciliation job
- More asset classes such as futures, FX, and options
- More complex trade lifecycle events
- SLA tracking for unresolved exceptions
- Exception aging report
