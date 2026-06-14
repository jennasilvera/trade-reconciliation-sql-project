# Daily Reconciliation Runbook

This runbook explains how to operate the Trade Reconciliation SQL Project as a repeatable daily reconciliation workflow.

All data is simulated.

---

## Purpose

The purpose of the daily reconciliation process is to compare internal trade bookings against broker-reported trade and allocation records, identify breaks, and produce exception reports for review.

---

## Daily Workflow

1. Generate simulated internal and broker data.
2. Load raw CSV files into the SQLite database.
3. Run SQL reconciliation logic.
4. Export exception reports.
5. Review exception summary.
6. Investigate high-priority breaks.
7. Regenerate sample report preview.
8. Run tests to confirm expected outputs.

---

## Main Command

Use this command to run the full local validation workflow:

    make check

This command runs:

    make run
    make preview
    pytest

---

## Output Files to Review

| File | Purpose |
|---|---|
| data/reports/trade_exceptions.csv | Main trade-level breaks |
| data/reports/duplicate_trade_exceptions.csv | Duplicate execution ID checks |
| data/reports/allocation_exceptions.csv | Allocation-level breaks |
| data/reports/reconciliation_summary.csv | Summary of exception counts by break type |

---

## First Report to Check

Start with:

    data/reports/reconciliation_summary.csv

This gives a quick count of breaks by exception type.

---

## High-Priority Breaks

Review these first:

| Break Type | Reason |
|---|---|
| MISSING_BROKER_TRADE | Internal trade may not be confirmed externally |
| MISSING_INTERNAL_BOOKING | Broker-reported trade may not have been captured internally |
| SIDE_MISMATCH | Can create incorrect position direction |
| SYMBOL_MISMATCH | Can create incorrect security exposure |

---

## Medium-Priority Breaks

Review these after high-priority breaks:

| Break Type | Reason |
|---|---|
| QUANTITY_MISMATCH | Can affect position, P&L, and settlement |
| PRICE_MISMATCH | Can affect notional, P&L, and reporting |
| SETTLEMENT_DATE_MISMATCH | Can affect settlement workflow |
| ALLOCATION_ACCOUNT_MISMATCH | Can affect account-level booking accuracy |
| DUPLICATE_TRADE | Can indicate duplicate ingestion or booking |

---

## Lower-Priority Breaks

| Break Type | Reason |
|---|---|
| FEE_MISMATCH | Usually affects net amount and cost reporting, but may be less urgent than position-impacting breaks |

---

## Suggested Investigation Order

1. Missing internal or broker records
2. Side and symbol mismatches
3. Quantity and price mismatches
4. Settlement date issues
5. Allocation account breaks
6. Duplicate records
7. Fee differences

---

## Troubleshooting

If reports are missing, run:

    make run

If the sample report preview is stale, run:

    make preview

If tests fail, rerun the full workflow:

    make check

If the SQLite database appears stale, run:

    make clean
    make check

---

## Completion Criteria

A reconciliation run is complete when:

- Raw CSV files exist in data/raw/
- SQLite database is created
- Exception reports exist in data/reports/
- Sample report preview is regenerated
- pytest passes
- High-priority exception types are reviewed

---

## Interview Explanation

A concise way to explain this document:

I added a daily reconciliation runbook to show how the project could be operated as a repeatable control process. It explains how to run the workflow, which reports to review first, how to prioritize breaks, and how to troubleshoot common issues.
