# SQL Investigation Examples

This document contains SQL examples for investigating reconciliation breaks in the simulated SQLite database.

To run these manually:

    sqlite3 trade_recon.db

---

## View All Trade Exceptions

    SELECT *
    FROM trade_exceptions
    ORDER BY exception_type, execution_id;

---

## Missing Broker Trades

    SELECT
        i.execution_id,
        i.trade_date,
        i.symbol,
        i.side,
        i.quantity,
        i.price,
        i.settlement_date
    FROM internal_trades i
    LEFT JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE b.execution_id IS NULL;

---

## Missing Internal Bookings

    SELECT
        b.execution_id,
        b.trade_date,
        b.symbol,
        b.side,
        b.quantity,
        b.price,
        b.settlement_date
    FROM broker_trades b
    LEFT JOIN internal_trades i
        ON b.execution_id = i.execution_id
    WHERE i.execution_id IS NULL;

---

## Quantity Mismatches

    SELECT
        i.execution_id,
        i.symbol,
        i.quantity AS internal_quantity,
        b.quantity AS broker_quantity,
        i.quantity - b.quantity AS quantity_difference
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE i.quantity <> b.quantity;

---

## Price Mismatches

    SELECT
        i.execution_id,
        i.symbol,
        i.quantity,
        i.price AS internal_price,
        b.price AS broker_price,
        ROUND(i.price - b.price, 4) AS price_difference,
        ROUND((i.price - b.price) * i.quantity, 2) AS estimated_notional_impact
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE ROUND(i.price, 4) <> ROUND(b.price, 4);

---

## Side Mismatches

    SELECT
        i.execution_id,
        i.symbol,
        i.side AS internal_side,
        b.side AS broker_side,
        i.quantity,
        i.price
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE i.side <> b.side;

---

## Symbol Mismatches

    SELECT
        i.execution_id,
        i.symbol AS internal_symbol,
        b.symbol AS broker_symbol,
        i.side,
        i.quantity,
        i.price
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE i.symbol <> b.symbol;

---

## Fee Mismatches

    SELECT
        i.execution_id,
        i.symbol,
        i.fee AS internal_fee,
        b.fee AS broker_fee,
        ROUND(i.fee - b.fee, 2) AS fee_difference
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE ROUND(i.fee, 2) <> ROUND(b.fee, 2);

---

## Settlement Date Mismatches

    SELECT
        i.execution_id,
        i.trade_date,
        i.symbol,
        i.settlement_date AS internal_settlement_date,
        b.settlement_date AS broker_settlement_date
    FROM internal_trades i
    JOIN broker_trades b
        ON i.execution_id = b.execution_id
    WHERE i.settlement_date <> b.settlement_date;

---

## Duplicate Internal Trades

    SELECT
        execution_id,
        COUNT(*) AS record_count
    FROM internal_trades
    GROUP BY execution_id
    HAVING COUNT(*) > 1;

---

## Duplicate Broker Trades

    SELECT
        execution_id,
        COUNT(*) AS record_count
    FROM broker_trades
    GROUP BY execution_id
    HAVING COUNT(*) > 1;

---

## Allocation Account Breaks

    SELECT
        i.execution_id,
        i.account AS internal_account,
        b.account AS broker_account,
        i.allocated_quantity AS internal_allocated_quantity,
        b.allocated_quantity AS broker_allocated_quantity
    FROM internal_allocations i
    LEFT JOIN broker_allocations b
        ON i.execution_id = b.execution_id
       AND i.account = b.account
    WHERE b.account IS NULL;

---

## Exception Summary

    SELECT
        exception_type,
        COUNT(*) AS exception_count
    FROM trade_exceptions
    GROUP BY exception_type
    ORDER BY exception_count DESC;

---

## Why These Queries Matter

These examples show how SQL can be used to investigate reconciliation breaks without relying only on manual spreadsheet review.

The queries demonstrate missing record detection, duplicate detection, field-level comparison, exception summarization, and operational prioritization.
