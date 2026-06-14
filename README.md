# Trade Reconciliation SQL Project

A simulated trading operations project that uses **Python, SQL, SQLite, pandas, and CSV reports** to reconcile internal trade bookings against broker trade records.

This project is designed for Trading Operations Associate, Trade Support, Production Support, and SQL/Data Analyst roles at systematic trading firms, hedge funds, banks, and broker-dealers.

> All data is simulated. This project does not claim professional broker, OMS, EMS, FIX, or hedge fund experience.

---

## Project Objective

The goal is to demonstrate a realistic trade reconciliation workflow:

1. Load internal trade bookings and broker trade records.
2. Join trade data across multiple sources using SQL.
3. Detect breaks in quantity, price, side, symbol, fees, settlement date, and allocations.
4. Identify missing and duplicate trade records.
5. Generate repeatable exception reports for operations review.
6. Summarize reconciliation status for daily control reporting.

This mirrors the type of operational control work performed by trading operations and production support teams, where analysts must investigate breaks quickly and produce reliable exception reports without waiting on engineering.

---

## Business Scenario

A systematic trading desk sends orders to market and books fills internally. Brokers send back trade files after execution. Operations must reconcile the internal trade blotter against broker records before downstream settlement and allocation workflows.

This project simulates three source datasets:

| Dataset | Description |
|---|---|
| `internal_trades.csv` | Internal trade bookings from a simulated OMS/trade blotter |
| `broker_trades.csv` | Broker-confirmed executions |
| `internal_allocations.csv` / `broker_allocations.csv` | Account-level allocation details |

The reconciliation flags common breaks:

- Missing broker trade
- Missing internal booking
- Quantity mismatch
- Price mismatch
- Side mismatch
- Symbol mismatch
- Fee mismatch
- Settlement date mismatch
- Allocation account mismatch
- Duplicate trade

---

## Tech Stack

- Python 3.10+
- SQLite
- SQL
- pandas
- CSV files
- pytest

SQLite is used so the project can run locally without database setup. The SQL is intentionally written in a way that can be adapted to PostgreSQL later.

---

## Repository Structure

```text
trade-reconciliation-sql-project/
├── README.md
├── requirements.txt
├── .gitignore
├── Makefile
├── data/
│   ├── raw/
│   │   ├── internal_trades.csv
│   │   ├── broker_trades.csv
│   │   ├── internal_allocations.csv
│   │   ├── broker_allocations.csv
│   │   └── expected_breaks.csv
│   └── reports/
│       ├── trade_exceptions.csv
│       ├── duplicate_trade_exceptions.csv
│       ├── allocation_exceptions.csv
│       └── reconciliation_summary.csv
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
```

---

## Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows PowerShell
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate simulated trade data

```bash
python src/generate_data.py
```

### 4. Load data into SQLite

```bash
python src/load_database.py
```

### 5. Run reconciliation

```bash
python src/run_reconciliation.py
```

### 6. Review exception reports

```bash
ls data/reports
```

Or run everything with:

```bash
make run
```

---

## Output Reports

| Report | Purpose |
|---|---|
| `trade_exceptions.csv` | Trade-level breaks such as missing bookings, price breaks, side breaks, fee breaks, and settlement breaks |
| `duplicate_trade_exceptions.csv` | Duplicate internal or broker execution IDs |
| `allocation_exceptions.csv` | Allocation account and allocation quantity mismatches |
| `reconciliation_summary.csv` | Count of exceptions by break type |

Example output:

```text
exception_type,count
PRICE_MISMATCH,5
QUANTITY_MISMATCH,5
MISSING_BROKER_TRADE,3
MISSING_INTERNAL_BOOKING,3
```

---

## Reconciliation Logic

The project uses SQL to compare internal and broker data on `execution_id`, a simulated shared execution reference.

### Trade-level controls

- Internal trade exists but broker record does not → `MISSING_BROKER_TRADE`
- Broker trade exists but internal record does not → `MISSING_INTERNAL_BOOKING`
- Internal and broker quantities differ → `QUANTITY_MISMATCH`
- Internal and broker prices differ beyond tolerance → `PRICE_MISMATCH`
- Internal and broker sides differ → `SIDE_MISMATCH`
- Internal and broker symbols differ → `SYMBOL_MISMATCH`
- Commission plus fee differs beyond tolerance → `FEE_MISMATCH`
- Settlement dates differ → `SETTLEMENT_DATE_MISMATCH`

### Duplicate controls

The project treats duplicate execution IDs as separate exceptions because duplicates can create false positives in normal joins.

### Allocation controls

The allocation reconciliation compares account-level allocations between internal and broker records. It detects:

- Account exists internally but not at broker
- Account exists at broker but not internally
- Same account exists in both systems but allocation quantity differs

---

## Why This Project Is Relevant

Trading operations teams often need to:

- Monitor systematic trade flow
- Review trade capture and booking accuracy
- Investigate trade breaks across internal and external sources
- Use SQL to pull and reconcile data independently
- Produce exception reports for daily controls
- Escalate only validated issues to engineering, brokers, or trading teams

This project demonstrates those workflows using simulated data and transparent logic.

---

## Interview Explanation

A concise interview explanation:

> I built a simulated trade reconciliation project to practice the type of SQL-based operational control work used in trading operations. The project generates internal trade bookings, broker trade records, and account allocation files. I intentionally inject realistic breaks like missing trades, quantity mismatches, price mismatches, fee breaks, settlement breaks, allocation mismatches, and duplicates. Then I load the data into SQLite and run SQL exception queries to produce CSV reports. The goal was to show that I can reason through trade lifecycle data, join records across sources, isolate breaks, and create repeatable reconciliation controls using SQL and Python.

---

## Resume Bullets

Use only after completing the project:

- Built a simulated trade reconciliation workflow using Python, SQL, SQLite, and pandas to compare internal trade bookings against broker execution records and generate exception reports.
- Designed SQL controls to identify missing trades, duplicate execution IDs, quantity mismatches, price breaks, side discrepancies, symbol discrepancies, fee breaks, settlement date mismatches, and allocation mismatches.
- Created repeatable reconciliation scripts that generate synthetic trade lifecycle data, load CSV files into a relational database, run SQL exception logic, and export operations-ready CSV reports.
- Modeled account-level allocation reconciliation across internal and broker sources to detect allocation account and quantity discrepancies.
- Documented the project in a recruiter-ready GitHub README explaining the business scenario, reconciliation logic, control framework, and interview relevance.

---

## Future Enhancements

Possible extensions:

- Add PostgreSQL support with Docker Compose
- Add Streamlit dashboard for exception review
- Add SLA/severity classification for breaks
- Add intraday monitoring simulation
- Add alerting rules for high-risk breaks
- Add broker-specific file formats
- Add unit tests for each exception type
- Add data quality checks for nulls and invalid symbols

---

## Disclaimer

This project uses simulated data only. It is an educational portfolio project intended to demonstrate SQL, data engineering, reconciliation logic, and trading operations understanding.
