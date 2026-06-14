DROP TABLE IF EXISTS internal_trades;
DROP TABLE IF EXISTS broker_trades;
DROP TABLE IF EXISTS internal_allocations;
DROP TABLE IF EXISTS broker_allocations;

CREATE TABLE internal_trades (
    internal_trade_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    settle_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price > 0),
    gross_amount REAL NOT NULL,
    commission REAL NOT NULL DEFAULT 0,
    fees REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    strategy TEXT NOT NULL,
    portfolio TEXT NOT NULL,
    account_id TEXT NOT NULL,
    broker TEXT NOT NULL,
    source_system TEXT NOT NULL DEFAULT 'SIM_INTERNAL_OMS',
    created_at TEXT NOT NULL
);

CREATE TABLE broker_trades (
    broker_trade_id TEXT PRIMARY KEY,
    broker_execution_id TEXT NOT NULL,
    execution_id TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    settle_date TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price > 0),
    gross_amount REAL NOT NULL,
    commission REAL NOT NULL DEFAULT 0,
    fees REAL NOT NULL DEFAULT 0,
    currency TEXT NOT NULL DEFAULT 'USD',
    account_id TEXT NOT NULL,
    broker TEXT NOT NULL,
    source_system TEXT NOT NULL DEFAULT 'SIM_BROKER_FILE',
    received_at TEXT NOT NULL
);

CREATE TABLE internal_allocations (
    allocation_id TEXT PRIMARY KEY,
    execution_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    allocation_quantity INTEGER NOT NULL CHECK (allocation_quantity > 0),
    allocation_pct REAL NOT NULL CHECK (allocation_pct > 0 AND allocation_pct <= 1),
    created_at TEXT NOT NULL
);

CREATE TABLE broker_allocations (
    allocation_id TEXT PRIMARY KEY,
    execution_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    allocation_quantity INTEGER NOT NULL CHECK (allocation_quantity > 0),
    allocation_pct REAL NOT NULL CHECK (allocation_pct > 0 AND allocation_pct <= 1),
    received_at TEXT NOT NULL
);

CREATE INDEX idx_internal_execution_id ON internal_trades(execution_id);
CREATE INDEX idx_broker_execution_id ON broker_trades(execution_id);
CREATE INDEX idx_internal_alloc_execution_id ON internal_allocations(execution_id);
CREATE INDEX idx_broker_alloc_execution_id ON broker_allocations(execution_id);
