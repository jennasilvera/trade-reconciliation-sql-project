-- Trade-level exceptions. Duplicate execution IDs are excluded here and reported separately.
DROP VIEW IF EXISTS trade_exceptions;
DROP VIEW IF EXISTS duplicate_trade_exceptions;
DROP VIEW IF EXISTS allocation_exceptions;
DROP VIEW IF EXISTS reconciliation_summary;

CREATE VIEW trade_exceptions AS
SELECT
    execution_id,
    'MISSING_BROKER_TRADE' AS exception_type,
    'HIGH' AS severity,
    'Internal trade exists but broker trade is missing' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 0

UNION ALL

SELECT
    execution_id,
    'MISSING_INTERNAL_BOOKING' AS exception_type,
    'HIGH' AS severity,
    'Broker trade exists but internal booking is missing' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 0 AND broker_count = 1

UNION ALL

SELECT
    execution_id,
    'QUANTITY_MISMATCH' AS exception_type,
    'HIGH' AS severity,
    'Internal and broker quantities do not match' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND internal_quantity <> broker_quantity

UNION ALL

SELECT
    execution_id,
    'PRICE_MISMATCH' AS exception_type,
    'MEDIUM' AS severity,
    'Internal and broker prices differ by more than 0.01' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND ABS(internal_price - broker_price) > 0.01

UNION ALL

SELECT
    execution_id,
    'SIDE_MISMATCH' AS exception_type,
    'HIGH' AS severity,
    'Internal and broker trade sides do not match' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND internal_side <> broker_side

UNION ALL

SELECT
    execution_id,
    'SYMBOL_MISMATCH' AS exception_type,
    'HIGH' AS severity,
    'Internal and broker symbols do not match' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND internal_symbol <> broker_symbol

UNION ALL

SELECT
    execution_id,
    'FEE_MISMATCH' AS exception_type,
    'LOW' AS severity,
    'Internal and broker total fees differ by more than 0.01' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND ABS(internal_total_fees - broker_total_fees) > 0.01

UNION ALL

SELECT
    execution_id,
    'SETTLEMENT_DATE_MISMATCH' AS exception_type,
    'MEDIUM' AS severity,
    'Internal and broker settlement dates do not match' AS exception_description,
    internal_trade_id,
    broker_trade_id,
    internal_quantity,
    broker_quantity,
    internal_price,
    broker_price,
    internal_side,
    broker_side,
    internal_symbol,
    broker_symbol,
    internal_settle_date,
    broker_settle_date,
    internal_total_fees,
    broker_total_fees
FROM trade_reconciliation_base
WHERE internal_count = 1 AND broker_count = 1
  AND internal_settle_date <> broker_settle_date;

CREATE VIEW duplicate_trade_exceptions AS
SELECT
    execution_id,
    'DUPLICATE_INTERNAL_TRADE' AS exception_type,
    'HIGH' AS severity,
    COUNT(*) AS duplicate_count,
    GROUP_CONCAT(internal_trade_id) AS duplicate_record_ids
FROM internal_trades
GROUP BY execution_id
HAVING COUNT(*) > 1

UNION ALL

SELECT
    execution_id,
    'DUPLICATE_BROKER_TRADE' AS exception_type,
    'HIGH' AS severity,
    COUNT(*) AS duplicate_count,
    GROUP_CONCAT(broker_trade_id) AS duplicate_record_ids
FROM broker_trades
GROUP BY execution_id
HAVING COUNT(*) > 1;

CREATE VIEW allocation_exceptions AS
SELECT
    i.execution_id,
    'ALLOCATION_ACCOUNT_MISSING_AT_BROKER' AS exception_type,
    'MEDIUM' AS severity,
    i.account_id AS internal_account_id,
    NULL AS broker_account_id,
    i.allocation_quantity AS internal_allocation_quantity,
    NULL AS broker_allocation_quantity
FROM internal_allocations i
LEFT JOIN broker_allocations b
    ON i.execution_id = b.execution_id
   AND i.account_id = b.account_id
WHERE b.account_id IS NULL

UNION ALL

SELECT
    b.execution_id,
    'ALLOCATION_ACCOUNT_MISSING_INTERNALLY' AS exception_type,
    'MEDIUM' AS severity,
    NULL AS internal_account_id,
    b.account_id AS broker_account_id,
    NULL AS internal_allocation_quantity,
    b.allocation_quantity AS broker_allocation_quantity
FROM broker_allocations b
LEFT JOIN internal_allocations i
    ON b.execution_id = i.execution_id
   AND b.account_id = i.account_id
WHERE i.account_id IS NULL

UNION ALL

SELECT
    i.execution_id,
    'ALLOCATION_QUANTITY_MISMATCH' AS exception_type,
    'MEDIUM' AS severity,
    i.account_id AS internal_account_id,
    b.account_id AS broker_account_id,
    i.allocation_quantity AS internal_allocation_quantity,
    b.allocation_quantity AS broker_allocation_quantity
FROM internal_allocations i
JOIN broker_allocations b
    ON i.execution_id = b.execution_id
   AND i.account_id = b.account_id
WHERE i.allocation_quantity <> b.allocation_quantity;

CREATE VIEW reconciliation_summary AS
SELECT exception_type, COUNT(*) AS exception_count
FROM trade_exceptions
GROUP BY exception_type

UNION ALL

SELECT exception_type, COUNT(*) AS exception_count
FROM duplicate_trade_exceptions
GROUP BY exception_type

UNION ALL

SELECT exception_type, COUNT(*) AS exception_count
FROM allocation_exceptions
GROUP BY exception_type;
