# Data Dictionary

This document describes the simulated datasets used in the Trade Reconciliation SQL Project.

All data in this project is synthetic and created for portfolio demonstration purposes only.

---

## internal_trades

File: `data/raw/internal_trades.csv`

Represents trades booked internally by a simulated trading or investment system.

| Column | Description |
|---|---|
| trade_id | Internal trade identifier |
| execution_id | Simulated execution identifier used to match broker records |
| trade_date | Date the trade was executed |
| settlement_date | Expected settlement date |
| symbol | Security ticker |
| side | Buy or sell indicator |
| quantity | Number of shares or units |
| price | Execution price |
| gross_amount | Quantity multiplied by price |
| fee | Internal fee amount |
| net_amount | Gross amount adjusted for fees |
| trader | Simulated trader identifier |
| strategy | Simulated strategy name |
| source_system | Internal source system label |

---

## broker_trades

File: `data/raw/broker_trades.csv`

Represents trades reported externally by a simulated broker.

| Column | Description |
|---|---|
| broker_trade_id | Broker-side trade identifier |
| execution_id | Simulated execution identifier used to match internal records |
| trade_date | Date the broker reports the trade execution |
| settlement_date | Broker-reported settlement date |
| symbol | Broker-reported security ticker |
| side | Broker-reported buy or sell indicator |
| quantity | Broker-reported quantity |
| price | Broker-reported execution price |
| gross_amount | Broker-reported gross amount |
| fee | Broker-reported fee amount |
| net_amount | Broker-reported net amount |
| broker | Simulated broker name |
| source_system | Broker source system label |

---

## internal_allocations

File: `data/raw/internal_allocations.csv`

Represents account-level allocations from the internal system.

| Column | Description |
|---|---|
| allocation_id | Internal allocation identifier |
| execution_id | Execution identifier tied to the parent trade |
| account | Internal account code |
| allocated_quantity | Quantity allocated to the account |
| allocation_percent | Percentage of the trade allocated to the account |
| source_system | Internal allocation source label |

---

## broker_allocations

File: `data/raw/broker_allocations.csv`

Represents account-level allocations from the broker side.

| Column | Description |
|---|---|
| broker_allocation_id | Broker allocation identifier |
| execution_id | Execution identifier tied to the parent trade |
| account | Broker-reported account code |
| allocated_quantity | Quantity allocated to the account |
| allocation_percent | Percentage of the trade allocated to the account |
| source_system | Broker allocation source label |

---

## expected_breaks

File: `data/raw/expected_breaks.csv`

Documents the intentionally injected trade breaks used to validate the reconciliation process.

| Column | Description |
|---|---|
| execution_id | Execution identifier associated with the injected break |
| break_type | Type of simulated reconciliation break |
| description | Explanation of the injected discrepancy |

---

## Output Reports

### trade_exceptions

File: `data/reports/trade_exceptions.csv`

Main trade-level exception report.

### duplicate_trade_exceptions

File: `data/reports/duplicate_trade_exceptions.csv`

Detects duplicate execution IDs in internal or broker trade records.

### allocation_exceptions

File: `data/reports/allocation_exceptions.csv`

Detects account-level allocation breaks between internal and broker allocation records.

### reconciliation_summary

File: `data/reports/reconciliation_summary.csv`

Summarizes exception counts by break type.
