from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"


EXPECTED_INPUTS = {
    "internal_trades.csv",
    "broker_trades.csv",
    "internal_allocations.csv",
    "broker_allocations.csv",
    "expected_breaks.csv",
}


def test_input_manifest_exists():
    path = REPORTS_DIR / "input_manifest.csv"

    assert path.exists(), "input_manifest.csv should exist after make input_manifest or make check"


def test_input_manifest_has_expected_inputs():
    path = REPORTS_DIR / "input_manifest.csv"
    manifest = pd.read_csv(path)

    actual_inputs = set(manifest["input_name"])

    assert EXPECTED_INPUTS.issubset(actual_inputs)


def test_input_manifest_files_are_found():
    path = REPORTS_DIR / "input_manifest.csv"
    manifest = pd.read_csv(path)

    assert set(manifest["status"]) == {"FOUND"}


def test_input_manifest_row_counts_are_positive():
    path = REPORTS_DIR / "input_manifest.csv"
    manifest = pd.read_csv(path)

    assert (manifest["row_count"] > 0).all()
