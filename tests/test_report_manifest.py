from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"


EXPECTED_REPORTS = {
    "trade_exceptions.csv",
    "duplicate_trade_exceptions.csv",
    "allocation_exceptions.csv",
    "reconciliation_summary.csv",
    "data_quality_checks.csv",
    "exception_lifecycle_report.csv",
}


def test_report_manifest_exists():
    path = REPORTS_DIR / "report_manifest.csv"

    assert path.exists(), "report_manifest.csv should exist after make manifest or make check"


def test_report_manifest_has_expected_reports():
    path = REPORTS_DIR / "report_manifest.csv"
    manifest = pd.read_csv(path)

    actual_reports = set(manifest["report_name"])

    assert EXPECTED_REPORTS.issubset(actual_reports)


def test_report_manifest_reports_are_found():
    path = REPORTS_DIR / "report_manifest.csv"
    manifest = pd.read_csv(path)

    assert set(manifest["status"]) == {"FOUND"}


def test_report_manifest_row_counts_are_positive():
    path = REPORTS_DIR / "report_manifest.csv"
    manifest = pd.read_csv(path)

    assert (manifest["row_count"] > 0).all()
