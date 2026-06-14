DROP VIEW IF EXISTS internal_trade_counts;
DROP VIEW IF EXISTS broker_trade_counts;
DROP VIEW IF EXISTS trade_reconciliation_base;

CREATE VIEW internal_trade_counts AS
SELECT
    execution_id,
    COUNT(*) AS internal_count
FROM internal_trades
GROUP BY execution_id;

CREATE VIEW broker_trade_counts AS
SELECT
    execution_id,
    COUNT(*) AS broker_count
FROM broker_trades
GROUP BY execution_id;

CREATE VIEW trade_reconciliation_base AS
WITH all_execution_ids AS (
    SELECT execution_id FROM internal_trades
    UNION
    SELECT execution_id FROM broker_trades
),
joined AS (
    SELECT
        k.execution_id,
        COALESCE(ic.internal_count, 0) AS internal_count,
        COALESCE(bc.broker_count, 0) AS broker_count,
        i.internal_trade_id,
        b.broker_trade_id,
        i.order_id,
        b.broker_execution_id,
        i.trade_date AS internal_trade_date,
        b.trade_date AS broker_trade_date,
        i.settle_date AS internal_settle_date,
        b.settle_date AS broker_settle_date,
        i.symbol AS internal_symbol,
        b.symbol AS broker_symbol,
        i.side AS internal_side,
        b.side AS broker_side,
        i.quantity AS internal_quantity,
        b.quantity AS broker_quantity,
        i.price AS internal_price,
        b.price AS broker_price,
        i.gross_amount AS internal_gross_amount,
        b.gross_amount AS broker_gross_amount,
        i.commission AS internal_commission,
        b.commission AS broker_commission,
        i.fees AS internal_fees,
        b.fees AS broker_fees,
        ROUND(i.commission + i.fees, 4) AS internal_total_fees,
        ROUND(b.commission + b.fees, 4) AS broker_total_fees,
        i.account_id AS internal_account_id,
        b.account_id AS broker_account_id,
        i.broker AS internal_broker,
        b.broker AS broker_name
    FROM all_execution_ids k
    LEFT JOIN internal_trade_counts ic ON k.execution_id = ic.execution_id
    LEFT JOIN broker_trade_counts bc ON k.execution_id = bc.execution_id
    LEFT JOIN internal_trades i
        ON k.execution_id = i.execution_id
       AND COALESCE(ic.internal_count, 0) = 1
    LEFT JOIN broker_trades b
        ON k.execution_id = b.execution_id
       AND COALESCE(bc.broker_count, 0) = 1
)
SELECT *
FROM joined;
