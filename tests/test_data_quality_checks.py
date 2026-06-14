from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"


def test_data_quality_report_exists():
    path = REPORTS_DIR / "data_quality_checks.csv"

    assert path.exists(), "data_quality_checks.csv should exist after make quality or make check"


def test_all_data_quality_checks_pass():
    path = REPORTS_DIR / "data_quality_checks.csv"
    checks = pd.read_csv(path)

    assert not checks.empty, "data_quality_checks.csv should not be empty"

    failed_checks = checks[checks["status"] != "PASS"]

    assert failed_checks.empty, (
        "Expected all data quality checks to pass, but found failures:\n"
        + failed_checks.to_string(index=False)
    )


def test_data_quality_report_has_expected_columns():
    path = REPORTS_DIR / "data_quality_checks.csv"
    checks = pd.read_csv(path)

    expected_columns = {
        "dataset",
        "check_name",
        "status",
        "details",
    }

    assert expected_columns.issubset(set(checks.columns))
