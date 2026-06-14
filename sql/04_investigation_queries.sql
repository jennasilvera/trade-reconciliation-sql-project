-- Trade Reconciliation SQL Project
-- Ad Hoc Investigation Queries
--
-- These queries can be used to investigate reconciliation breaks
-- after the SQLite database has been created with:
--
--     make run
--
-- To run manually:
--
--     sqlite3 trade_recon.db
--     .read sql/04_investigation_queries.sql


-- 1. View all trade exceptions
SELECT *
FROM trade_exceptions
ORDER BY exception_type, execution_id;


-- 2. Missing broker trades
SELECT
    i.execution_id,
    i.trade_date,
    i.symbol,
    i.side,
    i.quantity,
    i.price,
    i.settle_date
FROM internal_trades i
LEFT JOIN broker_trades b
    ON i.execution_id = b.execution_id
WHERE b.execution_id IS NULL;


-- 3. Missing internal bookings
SELECT
    b.execution_id,
    b.trade_date,
    b.symbol,
    b.side,
    b.quantity,
    b.price,
    b.settle_date
FROM broker_trades b
LEFT JOIN internal_trades i
    ON b.execution_id = i.execution_id
WHERE i.execution_id IS NULL;


-- 4. Quantity mismatches
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


-- 5. Price mismatches
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


-- 6. Side mismatches
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


-- 7. Symbol mismatches
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


-- 8. Fee mismatches
SELECT
    i.execution_id,
    i.symbol,
    i.fees AS internal_fees,
    b.fees AS broker_fees,
    ROUND(i.fees - b.fees, 2) AS fee_difference
FROM internal_trades i
JOIN broker_trades b
    ON i.execution_id = b.execution_id
WHERE ROUND(i.fees, 2) <> ROUND(b.fees, 2);


-- 9. Settlement date mismatches
SELECT
    i.execution_id,
    i.trade_date,
    i.symbol,
    i.settle_date AS internal_settle_date,
    b.settle_date AS broker_settle_date
FROM internal_trades i
JOIN broker_trades b
    ON i.execution_id = b.execution_id
WHERE i.settle_date <> b.settle_date;


-- 10. Duplicate internal trades
SELECT
    execution_id,
    COUNT(*) AS record_count
FROM internal_trades
GROUP BY execution_id
HAVING COUNT(*) > 1;


-- 11. Duplicate broker trades
SELECT
    execution_id,
    COUNT(*) AS record_count
FROM broker_trades
GROUP BY execution_id
HAVING COUNT(*) > 1;


-- 12. Allocation account breaks
SELECT
    i.execution_id,
    i.account_id AS internal_account,
    b.account_id AS broker_account,
    i.allocation_quantity AS internal_allocated_quantity,
    b.allocation_quantity AS broker_allocated_quantity
FROM internal_allocations i
LEFT JOIN broker_allocations b
    ON i.execution_id = b.execution_id
   AND i.account_id = b.account_id
WHERE b.account_id IS NULL;


-- 13. Exception summary
SELECT
    exception_type,
    COUNT(*) AS exception_count
FROM trade_exceptions
GROUP BY exception_type
ORDER BY exception_count DESC;
