from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "data" / "reports"


def run_command(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT_DIR, check=True)


def test_reconciliation_reports_include_expected_exception_types() -> None:
    run_command([sys.executable, "src/generate_data.py"])
    run_command([sys.executable, "src/load_database.py"])
    run_command([sys.executable, "src/run_reconciliation.py"])

    summary = pd.read_csv(REPORTS_DIR / "reconciliation_summary.csv")
    exception_types = set(summary["exception_type"])

    expected_types = {
        "MISSING_BROKER_TRADE",
        "MISSING_INTERNAL_BOOKING",
        "QUANTITY_MISMATCH",
        "PRICE_MISMATCH",
        "SIDE_MISMATCH",
        "SYMBOL_MISMATCH",
        "FEE_MISMATCH",
        "SETTLEMENT_DATE_MISMATCH",
        "DUPLICATE_INTERNAL_TRADE",
        "DUPLICATE_BROKER_TRADE",
        "ALLOCATION_ACCOUNT_MISSING_AT_BROKER",
        "ALLOCATION_ACCOUNT_MISSING_INTERNALLY",
    }

    assert expected_types.issubset(exception_types)


def test_trade_exception_report_has_required_columns() -> None:
    run_command([sys.executable, "src/generate_data.py"])
    run_command([sys.executable, "src/load_database.py"])
    run_command([sys.executable, "src/run_reconciliation.py"])

    trade_exceptions = pd.read_csv(REPORTS_DIR / "trade_exceptions.csv")
    required_columns = {
        "execution_id",
        "exception_type",
        "severity",
        "exception_description",
        "internal_trade_id",
        "broker_trade_id",
    }

    assert required_columns.issubset(set(trade_exceptions.columns))
