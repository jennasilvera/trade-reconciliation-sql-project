from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "data" / "reports"
OUTPUT_PATH = REPORTS_DIR / "exception_lifecycle_report.csv"

INPUT_REPORTS = [
    ("trade_exceptions", REPORTS_DIR / "trade_exceptions.csv"),
    ("duplicate_trade_exceptions", REPORTS_DIR / "duplicate_trade_exceptions.csv"),
    ("allocation_exceptions", REPORTS_DIR / "allocation_exceptions.csv"),
]

SEVERITY_MAP = {
    "MISSING_BROKER_TRADE": "HIGH",
    "MISSING_INTERNAL_BOOKING": "HIGH",
    "SIDE_MISMATCH": "HIGH",
    "SYMBOL_MISMATCH": "HIGH",
    "QUANTITY_MISMATCH": "MEDIUM",
    "PRICE_MISMATCH": "MEDIUM",
    "SETTLEMENT_DATE_MISMATCH": "MEDIUM",
    "ALLOCATION_ACCOUNT_MISSING_AT_BROKER": "MEDIUM",
    "ALLOCATION_ACCOUNT_MISSING_INTERNALLY": "MEDIUM",
    "DUPLICATE_INTERNAL_TRADE": "MEDIUM",
    "DUPLICATE_BROKER_TRADE": "MEDIUM",
    "FEE_MISMATCH": "LOW",
}

OWNER_QUEUE_MAP = {
    "MISSING_BROKER_TRADE": "Broker Operations",
    "MISSING_INTERNAL_BOOKING": "Trade Support",
    "SIDE_MISMATCH": "Trade Support",
    "SYMBOL_MISMATCH": "Security Master / Trade Support",
    "QUANTITY_MISMATCH": "Trade Support",
    "PRICE_MISMATCH": "Trade Support",
    "SETTLEMENT_DATE_MISMATCH": "Settlements",
    "ALLOCATION_ACCOUNT_MISSING_AT_BROKER": "Allocations",
    "ALLOCATION_ACCOUNT_MISSING_INTERNALLY": "Allocations",
    "DUPLICATE_INTERNAL_TRADE": "Data Operations",
    "DUPLICATE_BROKER_TRADE": "Broker Operations",
    "FEE_MISMATCH": "Fees / Commissions",
}

SLA_HOURS_MAP = {
    "HIGH": 4,
    "MEDIUM": 24,
    "LOW": 48,
}


def normalize_report(report_name: str, path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)

    if df.empty:
        return pd.DataFrame()

    if "exception_type" not in df.columns:
        return pd.DataFrame()

    output = pd.DataFrame()
    output["source_report"] = report_name
    output["execution_id"] = df["execution_id"] if "execution_id" in df.columns else ""
    output["exception_type"] = df["exception_type"]

    output["severity"] = output["exception_type"].map(SEVERITY_MAP).fillna("REVIEW")
    output["owner_queue"] = output["exception_type"].map(OWNER_QUEUE_MAP).fillna("Operations Review")
    output["sla_hours"] = output["severity"].map(SLA_HOURS_MAP).fillna(24).astype(int)

    output["status"] = "OPEN"
    output["age_days"] = 0
    output["generated_at_utc"] = "2026-01-15 17:00:00"
    output["resolution_notes"] = ""

    return output


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    frames = [
        normalize_report(report_name, path)
        for report_name, path in INPUT_REPORTS
    ]

    frames = [frame for frame in frames if not frame.empty]

    if frames:
        lifecycle = pd.concat(frames, ignore_index=True)
        lifecycle.insert(
            0,
            "exception_id",
            [f"EXC-{idx:05d}" for idx in range(1, len(lifecycle) + 1)],
        )
    else:
        lifecycle = pd.DataFrame(
            columns=[
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
            ]
        )

    lifecycle.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(lifecycle)} rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
