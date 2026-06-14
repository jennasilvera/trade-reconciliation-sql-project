from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"


EXPECTED_EXCEPTION_TYPES = {
    "MISSING_BROKER_TRADE",
    "MISSING_INTERNAL_BOOKING",
    "QUANTITY_MISMATCH",
    "PRICE_MISMATCH",
    "SIDE_MISMATCH",
    "SYMBOL_MISMATCH",
    "FEE_MISMATCH",
    "SETTLEMENT_DATE_MISMATCH",
    "ALLOCATION_ACCOUNT_MISSING_AT_BROKER",
    "ALLOCATION_ACCOUNT_MISSING_INTERNALLY",
    "DUPLICATE_INTERNAL_TRADE",
    "DUPLICATE_BROKER_TRADE",
}


def test_reconciliation_summary_contains_expected_exception_types():
    summary_path = REPORTS_DIR / "reconciliation_summary.csv"
    summary = pd.read_csv(summary_path)

    actual_exception_types = set(summary["exception_type"])
    missing_exception_types = EXPECTED_EXCEPTION_TYPES - actual_exception_types

    assert not missing_exception_types, (
        f"Missing expected exception types: {sorted(missing_exception_types)}"
    )


def test_reconciliation_summary_counts_are_positive():
    summary_path = REPORTS_DIR / "reconciliation_summary.csv"
    summary = pd.read_csv(summary_path)

    assert (summary["exception_count"] > 0).all()


def test_exception_report_files_are_not_empty():
    report_files = [
        "trade_exceptions.csv",
        "duplicate_trade_exceptions.csv",
        "allocation_exceptions.csv",
        "reconciliation_summary.csv",
    ]

    for filename in report_files:
        path = REPORTS_DIR / filename
        df = pd.read_csv(path)

        assert not df.empty, f"{filename} should not be empty"
