"""Generate simulated internal, broker, and allocation data.

The data intentionally includes common trading-operations reconciliation breaks.
All data is fake and generated for portfolio/demo purposes only.
"""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

import pandas as pd

from config import (
    BROKER_ALLOCATIONS_CSV,
    BROKER_TRADES_CSV,
    DATA_RAW_DIR,
    EXPECTED_BREAKS_CSV,
    INTERNAL_ALLOCATIONS_CSV,
    INTERNAL_TRADES_CSV,
)

SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "TSLA", "JPM", "SPY", "QQQ"]
BROKERS = ["BRKR_A", "BRKR_B", "BRKR_C"]
STRATEGIES = ["STAT_ARB", "MOMENTUM", "MEAN_REVERSION", "ETF_ARB"]
PORTFOLIOS = ["FUND_ALPHA", "FUND_BETA"]
ACCOUNTS = ["PA_MAIN", "PA_LONG_SHORT", "PA_MARKET_NEUTRAL", "PA_EVENT"]


def next_business_day(start_date: datetime, days: int = 2) -> datetime:
    """Return a simple T+N business-day settlement date."""
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current


def money(value: float) -> float:
    return round(value, 4)


def build_base_trades(num_trades: int, seed: int) -> pd.DataFrame:
    random.seed(seed)
    trade_date = datetime(2026, 6, 12)
    rows: List[Dict[str, object]] = []

    for i in range(1, num_trades + 1):
        symbol = random.choice(SYMBOLS)
        side = random.choice(["BUY", "SELL"])
        quantity = random.choice([100, 200, 300, 500, 1000, 1500, 2000])
        price = round(random.uniform(20, 600), 2)
        commission = money(quantity * 0.003)
        fees = money(quantity * price * 0.00002)
        gross_amount = money(quantity * price)
        broker = random.choice(BROKERS)
        account = random.choice(ACCOUNTS)
        execution_id = f"EXEC-{i:06d}"

        rows.append(
            {
                "internal_trade_id": f"INT-{i:06d}",
                "order_id": f"ORD-{(i // 3) + 1:06d}",
                "execution_id": execution_id,
                "trade_date": trade_date.strftime("%Y-%m-%d"),
                "settle_date": next_business_day(trade_date).strftime("%Y-%m-%d"),
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "price": price,
                "gross_amount": gross_amount,
                "commission": commission,
                "fees": fees,
                "currency": "USD",
                "strategy": random.choice(STRATEGIES),
                "portfolio": random.choice(PORTFOLIOS),
                "account_id": account,
                "broker": broker,
                "source_system": "SIM_INTERNAL_OMS",
                "created_at": f"{trade_date.strftime('%Y-%m-%d')}T16:05:00",
            }
        )

    return pd.DataFrame(rows)


def build_broker_from_internal(internal: pd.DataFrame) -> pd.DataFrame:
    broker = internal.copy()
    broker = broker.rename(columns={"internal_trade_id": "broker_trade_id"})
    broker["broker_trade_id"] = [f"BRK-{i:06d}" for i in range(1, len(broker) + 1)]
    broker["broker_execution_id"] = broker["execution_id"].str.replace("EXEC", "BEXEC", regex=False)
    broker["source_system"] = "SIM_BROKER_FILE"
    broker["received_at"] = broker["created_at"].str.replace("16:05:00", "17:00:00", regex=False)
    broker = broker.drop(columns=["order_id", "strategy", "portfolio", "created_at"])
    return broker


def build_allocations(trades: pd.DataFrame, source: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    timestamp_column = "created_at" if source == "internal" else "received_at"
    allocation_prefix = "IALLOC" if source == "internal" else "BALLOC"

    for idx, trade in trades.iterrows():
        # Most trades allocate 100% to the trade account. Some split across two accounts.
        split_trade = idx % 11 == 0
        if split_trade:
            second_account = next(acct for acct in ACCOUNTS if acct != trade["account_id"])
            first_qty = int(trade["quantity"] * 0.6)
            second_qty = int(trade["quantity"] - first_qty)
            allocations = [
                (trade["account_id"], first_qty, round(first_qty / trade["quantity"], 4)),
                (second_account, second_qty, round(second_qty / trade["quantity"], 4)),
            ]
        else:
            allocations = [(trade["account_id"], int(trade["quantity"]), 1.0)]

        for alloc_num, (account_id, alloc_qty, alloc_pct) in enumerate(allocations, start=1):
            rows.append(
                {
                    "allocation_id": f"{allocation_prefix}-{idx + 1:06d}-{alloc_num}",
                    "execution_id": trade["execution_id"],
                    "account_id": account_id,
                    "allocation_quantity": alloc_qty,
                    "allocation_pct": alloc_pct,
                    timestamp_column: trade.get("created_at", trade.get("received_at")),
                }
            )

    return pd.DataFrame(rows)


def inject_breaks(
    internal: pd.DataFrame,
    broker: pd.DataFrame,
    internal_alloc: pd.DataFrame,
    broker_alloc: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Inject deterministic breaks so reports are predictable for testing."""
    expected_breaks: List[Dict[str, str]] = []

    break_plan = {
        "MISSING_BROKER_TRADE": ["EXEC-000005", "EXEC-000010", "EXEC-000015"],
        "MISSING_INTERNAL_BOOKING": ["EXEC-BONLY-000001", "EXEC-BONLY-000002", "EXEC-BONLY-000003"],
        "QUANTITY_MISMATCH": ["EXEC-000020", "EXEC-000021", "EXEC-000022"],
        "PRICE_MISMATCH": ["EXEC-000030", "EXEC-000031", "EXEC-000032"],
        "SIDE_MISMATCH": ["EXEC-000040", "EXEC-000041"],
        "SYMBOL_MISMATCH": ["EXEC-000050", "EXEC-000051"],
        "FEE_MISMATCH": ["EXEC-000060", "EXEC-000061", "EXEC-000062"],
        "SETTLEMENT_DATE_MISMATCH": ["EXEC-000070", "EXEC-000071"],
        "ALLOCATION_ACCOUNT_MISMATCH": ["EXEC-000080", "EXEC-000081"],
        "DUPLICATE_INTERNAL_TRADE": ["EXEC-000090"],
        "DUPLICATE_BROKER_TRADE": ["EXEC-000091"],
    }

    def record(expected_type: str, execution_id: str) -> None:
        expected_breaks.append({"execution_id": execution_id, "expected_break_type": expected_type})

    # 1. Missing broker records
    for execution_id in break_plan["MISSING_BROKER_TRADE"]:
        broker = broker[broker["execution_id"] != execution_id]
        broker_alloc = broker_alloc[broker_alloc["execution_id"] != execution_id]
        record("MISSING_BROKER_TRADE", execution_id)

    # 2. Broker-only records
    template = broker.iloc[0].copy()
    for n, execution_id in enumerate(break_plan["MISSING_INTERNAL_BOOKING"], start=1):
        row = template.copy()
        row["broker_trade_id"] = f"BRK-ONLY-{n:06d}"
        row["broker_execution_id"] = f"BEXEC-ONLY-{n:06d}"
        row["execution_id"] = execution_id
        row["symbol"] = random.choice(SYMBOLS)
        row["quantity"] = random.choice([100, 300, 500])
        row["price"] = round(random.uniform(40, 300), 2)
        row["gross_amount"] = money(row["quantity"] * row["price"])
        broker = pd.concat([broker, pd.DataFrame([row])], ignore_index=True)

        alloc_row = {
            "allocation_id": f"BALLOC-ONLY-{n:06d}",
            "execution_id": execution_id,
            "account_id": row["account_id"],
            "allocation_quantity": int(row["quantity"]),
            "allocation_pct": 1.0,
            "received_at": row["received_at"],
        }
        broker_alloc = pd.concat([broker_alloc, pd.DataFrame([alloc_row])], ignore_index=True)
        record("MISSING_INTERNAL_BOOKING", execution_id)

    # 3. Field-level broker mutations
    for execution_id in break_plan["QUANTITY_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "quantity"] = broker.loc[mask, "quantity"] + 100
        broker.loc[mask, "gross_amount"] = broker.loc[mask, "quantity"] * broker.loc[mask, "price"]
        record("QUANTITY_MISMATCH", execution_id)

    for execution_id in break_plan["PRICE_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "price"] = broker.loc[mask, "price"] + 0.25
        broker.loc[mask, "gross_amount"] = broker.loc[mask, "quantity"] * broker.loc[mask, "price"]
        record("PRICE_MISMATCH", execution_id)

    for execution_id in break_plan["SIDE_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "side"] = broker.loc[mask, "side"].map({"BUY": "SELL", "SELL": "BUY"})
        record("SIDE_MISMATCH", execution_id)

    for execution_id in break_plan["SYMBOL_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "symbol"] = "IBM"
        record("SYMBOL_MISMATCH", execution_id)

    for execution_id in break_plan["FEE_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "fees"] = broker.loc[mask, "fees"] + 4.75
        record("FEE_MISMATCH", execution_id)

    for execution_id in break_plan["SETTLEMENT_DATE_MISMATCH"]:
        mask = broker["execution_id"] == execution_id
        broker.loc[mask, "settle_date"] = (
            pd.to_datetime(broker.loc[mask, "settle_date"]) + pd.Timedelta(days=1)
        ).dt.strftime("%Y-%m-%d")
        record("SETTLEMENT_DATE_MISMATCH", execution_id)

    # 4. Allocation break: change the broker account on one allocation row.
    for execution_id in break_plan["ALLOCATION_ACCOUNT_MISMATCH"]:
        mask = broker_alloc["execution_id"] == execution_id
        original_account = broker_alloc.loc[mask, "account_id"].iloc[0]
        replacement_account = next(acct for acct in ACCOUNTS if acct != original_account)
        first_idx = broker_alloc.loc[mask].index[0]
        broker_alloc.loc[first_idx, "account_id"] = replacement_account
        record("ALLOCATION_ACCOUNT_MISMATCH", execution_id)

    # 5. Duplicate records by execution_id but with distinct primary keys.
    duplicate_internal = internal[internal["execution_id"] == break_plan["DUPLICATE_INTERNAL_TRADE"][0]].copy()
    duplicate_internal["internal_trade_id"] = "INT-DUP-000001"
    internal = pd.concat([internal, duplicate_internal], ignore_index=True)
    record("DUPLICATE_INTERNAL_TRADE", break_plan["DUPLICATE_INTERNAL_TRADE"][0])

    duplicate_broker = broker[broker["execution_id"] == break_plan["DUPLICATE_BROKER_TRADE"][0]].copy()
    duplicate_broker["broker_trade_id"] = "BRK-DUP-000001"
    duplicate_broker["broker_execution_id"] = "BEXEC-DUP-000001"
    broker = pd.concat([broker, duplicate_broker], ignore_index=True)
    record("DUPLICATE_BROKER_TRADE", break_plan["DUPLICATE_BROKER_TRADE"][0])

    numeric_cols = ["price", "gross_amount", "commission", "fees"]
    for col in numeric_cols:
        if col in internal.columns:
            internal[col] = internal[col].astype(float).round(4)
        if col in broker.columns:
            broker[col] = broker[col].astype(float).round(4)

    expected = pd.DataFrame(expected_breaks)
    return internal, broker, internal_alloc, broker_alloc, expected


def main(num_trades: int, seed: int) -> None:
    if num_trades < 100:
        raise ValueError("num_trades must be at least 100 so deterministic break IDs exist.")

    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    internal = build_base_trades(num_trades=num_trades, seed=seed)
    broker = build_broker_from_internal(internal)
    internal_alloc = build_allocations(internal, source="internal")
    broker_alloc = build_allocations(broker, source="broker")

    internal, broker, internal_alloc, broker_alloc, expected = inject_breaks(
        internal, broker, internal_alloc, broker_alloc
    )

    internal.to_csv(INTERNAL_TRADES_CSV, index=False)
    broker.to_csv(BROKER_TRADES_CSV, index=False)
    internal_alloc.to_csv(INTERNAL_ALLOCATIONS_CSV, index=False)
    broker_alloc.to_csv(BROKER_ALLOCATIONS_CSV, index=False)
    expected.to_csv(EXPECTED_BREAKS_CSV, index=False)

    print(f"Generated {len(internal):,} internal trade rows -> {INTERNAL_TRADES_CSV}")
    print(f"Generated {len(broker):,} broker trade rows -> {BROKER_TRADES_CSV}")
    print(f"Generated {len(internal_alloc):,} internal allocation rows -> {INTERNAL_ALLOCATIONS_CSV}")
    print(f"Generated {len(broker_alloc):,} broker allocation rows -> {BROKER_ALLOCATIONS_CSV}")
    print(f"Generated expected break reference -> {EXPECTED_BREAKS_CSV}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate simulated trade reconciliation data.")
    parser.add_argument("--num-trades", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    main(num_trades=args.num_trades, seed=args.seed)
