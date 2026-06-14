from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"
OUTPUT_PATH = REPORTS_DIR / "report_manifest.csv"

REPORT_DESCRIPTIONS = {
    "trade_exceptions.csv": "Trade-level reconciliation breaks between internal and broker records",
    "duplicate_trade_exceptions.csv": "Duplicate execution ID checks across trade sources",
    "allocation_exceptions.csv": "Account-level allocation reconciliation breaks",
    "reconciliation_summary.csv": "Summary of exception counts by break type",
    "data_quality_checks.csv": "Validation checks for raw input files",
    "exception_lifecycle_report.csv": "Operational exception queue with severity, owner queue, SLA, and status",
}


def build_manifest() -> pd.DataFrame:
    rows = []

    for filename, description in REPORT_DESCRIPTIONS.items():
        path = REPORTS_DIR / filename

        if path.exists():
            df = pd.read_csv(path)
            status = "FOUND"
            row_count = len(df)
            column_count = len(df.columns)
            columns = ", ".join(df.columns)
        else:
            status = "MISSING"
            row_count = 0
            column_count = 0
            columns = ""

        rows.append(
            {
                "report_name": filename,
                "report_path": f"data/reports/{filename}",
                "status": status,
                "row_count": row_count,
                "column_count": column_count,
                "description": description,
                "columns": columns,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    manifest.to_csv(OUTPUT_PATH, index=False)

    print(f"Wrote {len(manifest)} rows -> {OUTPUT_PATH}")

    missing = manifest[manifest["status"] == "MISSING"]
    if not missing.empty:
        print("Missing reports:")
        print(missing[["report_name", "report_path"]].to_string(index=False))
        raise SystemExit(1)

    print("All expected reports found.")


if __name__ == "__main__":
    main()
