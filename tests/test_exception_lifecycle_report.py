from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"


def test_exception_lifecycle_report_exists():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"

    assert path.exists(), "exception_lifecycle_report.csv should exist after make lifecycle or make check"


def test_exception_lifecycle_report_is_not_empty():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"
    df = pd.read_csv(path)

    assert not df.empty, "exception_lifecycle_report.csv should not be empty"


def test_exception_lifecycle_report_has_expected_columns():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"
    df = pd.read_csv(path)

    expected_columns = {
        "exception_id",
        "source_report",
        "execution_id",
        "exception_type",
        "severity",
        "owner_queue",
        "sla_hours",
        "status",
        "age_days",
        "generated_at_utc",
        "resolution_notes",
    }

    assert expected_columns.issubset(set(df.columns))


def test_exception_lifecycle_status_defaults_to_open():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"
    df = pd.read_csv(path)

    assert set(df["status"]) == {"OPEN"}


def test_exception_lifecycle_has_valid_severity_values():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"
    df = pd.read_csv(path)

    valid_severities = {"HIGH", "MEDIUM", "LOW", "REVIEW"}

    assert set(df["severity"]).issubset(valid_severities)


def test_high_severity_breaks_have_short_sla():
    path = REPORTS_DIR / "exception_lifecycle_report.csv"
    df = pd.read_csv(path)

    high_severity = df[df["severity"] == "HIGH"]

    assert not high_severity.empty
    assert (high_severity["sla_hours"] == 4).all()
