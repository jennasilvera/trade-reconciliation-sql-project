from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
REPORTS_DIR = ROOT / "data" / "reports"
OUTPUT_PATH = REPORTS_DIR / "input_manifest.csv"

INPUT_DESCRIPTIONS = {
    "internal_trades.csv": "Simulated internal trade bookings",
    "broker_trades.csv": "Simulated broker-reported trades",
    "internal_allocations.csv": "Simulated internal account-level allocations",
    "broker_allocations.csv": "Simulated broker account-level allocations",
    "expected_breaks.csv": "Reference file describing intentionally injected breaks",
}


def build_manifest() -> pd.DataFrame:
    rows = []

    for filename, description in INPUT_DESCRIPTIONS.items():
        path = RAW_DIR / filename

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
                "input_name": filename,
                "input_path": f"data/raw/{filename}",
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
        print("Missing input files:")
        print(missing[["input_name", "input_path"]].to_string(index=False))
        raise SystemExit(1)

    print("All expected input files found.")


if __name__ == "__main__":
    main()
