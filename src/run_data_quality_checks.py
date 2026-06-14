from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
REPORTS_DIR = ROOT / "data" / "reports"

INPUT_FILES = {
    "internal_trades": RAW_DIR / "internal_trades.csv",
    "broker_trades": RAW_DIR / "broker_trades.csv",
    "internal_allocations": RAW_DIR / "internal_allocations.csv",
    "broker_allocations": RAW_DIR / "broker_allocations.csv",
}

REQUIRED_COLUMNS = {
    "internal_trades": [
        "internal_trade_id",
        "order_id",
        "execution_id",
        "trade_date",
        "settle_date",
        "symbol",
        "side",
        "quantity",
        "price",
        "gross_amount",
        "commission",
        "fees",
        "currency",
        "strategy",
        "portfolio",
        "account_id",
        "broker",
        "source_system",
        "created_at",
    ],
    "broker_trades": [
        "broker_trade_id",
        "broker_execution_id",
        "execution_id",
        "trade_date",
        "settle_date",
        "symbol",
        "side",
        "quantity",
        "price",
        "gross_amount",
        "commission",
        "fees",
        "currency",
        "account_id",
        "broker",
        "source_system",
        "received_at",
    ],
    "internal_allocations": [
        "allocation_id",
        "execution_id",
        "account_id",
        "allocation_quantity",
        "allocation_pct",
        "created_at",
    ],
    "broker_allocations": [
        "allocation_id",
        "execution_id",
        "account_id",
        "allocation_quantity",
        "allocation_pct",
        "received_at",
    ],
}


def add_check(results, dataset, check_name, status, details):
    results.append(
        {
            "dataset": dataset,
            "check_name": check_name,
            "status": status,
            "details": details,
        }
    )


def run_checks():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for dataset, path in INPUT_FILES.items():
        if not path.exists():
            add_check(results, dataset, "file_exists", "FAIL", f"Missing file: {path}")
            continue

        add_check(results, dataset, "file_exists", "PASS", f"Found file: {path}")

        df = pd.read_csv(path)

        add_check(
            results,
            dataset,
            "row_count_positive",
            "PASS" if len(df) > 0 else "FAIL",
            f"Row count: {len(df)}",
        )

        missing_columns = [
            col for col in REQUIRED_COLUMNS[dataset] if col not in df.columns
        ]

        add_check(
            results,
            dataset,
            "required_columns_present",
            "PASS" if not missing_columns else "FAIL",
            "All required columns present"
            if not missing_columns
            else "Missing columns: " + ", ".join(missing_columns),
        )

        if "execution_id" in df.columns:
            null_execution_ids = df["execution_id"].isna().sum()
            add_check(
                results,
                dataset,
                "execution_id_not_null",
                "PASS" if null_execution_ids == 0 else "FAIL",
                f"Null execution_id count: {null_execution_ids}",
            )

        if "quantity" in df.columns:
            non_positive_quantity = (df["quantity"] <= 0).sum()
            add_check(
                results,
                dataset,
                "quantity_positive",
                "PASS" if non_positive_quantity == 0 else "FAIL",
                f"Non-positive quantity count: {non_positive_quantity}",
            )

        if "allocation_quantity" in df.columns:
            non_positive_allocation_quantity = (df["allocation_quantity"] <= 0).sum()
            add_check(
                results,
                dataset,
                "allocation_quantity_positive",
                "PASS" if non_positive_allocation_quantity == 0 else "FAIL",
                f"Non-positive allocation quantity count: {non_positive_allocation_quantity}",
            )

        if "allocation_pct" in df.columns:
            invalid_allocation_pct = (
                (df["allocation_pct"] <= 0) | (df["allocation_pct"] > 1)
            ).sum()
            add_check(
                results,
                dataset,
                "allocation_pct_valid",
                "PASS" if invalid_allocation_pct == 0 else "FAIL",
                f"Invalid allocation_pct count: {invalid_allocation_pct}",
            )

        if "price" in df.columns:
            non_positive_price = (df["price"] <= 0).sum()
            add_check(
                results,
                dataset,
                "price_positive",
                "PASS" if non_positive_price == 0 else "FAIL",
                f"Non-positive price count: {non_positive_price}",
            )

        if "commission" in df.columns:
            negative_commission = (df["commission"] < 0).sum()
            add_check(
                results,
                dataset,
                "commission_non_negative",
                "PASS" if negative_commission == 0 else "FAIL",
                f"Negative commission count: {negative_commission}",
            )

        if "fees" in df.columns:
            negative_fees = (df["fees"] < 0).sum()
            add_check(
                results,
                dataset,
                "fees_non_negative",
                "PASS" if negative_fees == 0 else "FAIL",
                f"Negative fees count: {negative_fees}",
            )

        if "side" in df.columns:
            invalid_sides = (~df["side"].isin(["BUY", "SELL"])).sum()
            add_check(
                results,
                dataset,
                "side_values_valid",
                "PASS" if invalid_sides == 0 else "FAIL",
                f"Invalid side count: {invalid_sides}",
            )

    output = pd.DataFrame(results)
    output_path = REPORTS_DIR / "data_quality_checks.csv"
    output.to_csv(output_path, index=False)

    print(f"Wrote {len(output)} checks -> {output_path}")

    failed = output[output["status"] == "FAIL"]
    if not failed.empty:
        print("Data quality failures found:")
        print(failed.to_string(index=False))
        raise SystemExit(1)

    print("All data quality checks passed.")


if __name__ == "__main__":
    run_checks()
