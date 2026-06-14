"""Run SQL reconciliation and export exception reports."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from config import DB_PATH, REPORTS_DIR, SQL_DIR

REPORT_QUERIES = {
    "trade_exceptions.csv": "SELECT * FROM trade_exceptions ORDER BY exception_type, execution_id",
    "duplicate_trade_exceptions.csv": "SELECT * FROM duplicate_trade_exceptions ORDER BY exception_type, execution_id",
    "allocation_exceptions.csv": "SELECT * FROM allocation_exceptions ORDER BY exception_type, execution_id",
    "reconciliation_summary.csv": "SELECT * FROM reconciliation_summary ORDER BY exception_count DESC, exception_type",
}


def execute_sql_file(connection: sqlite3.Connection, sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    connection.executescript(sql)


def export_report(connection: sqlite3.Connection, filename: str, query: str) -> pd.DataFrame:
    df = pd.read_sql_query(query, connection)
    output_path = REPORTS_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df):,} rows -> {output_path}")
    return df


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run `python src/load_database.py` first.")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        execute_sql_file(connection, SQL_DIR / "02_reconciliation_views.sql")
        execute_sql_file(connection, SQL_DIR / "03_exception_queries.sql")

        reports = {
            filename: export_report(connection, filename, query)
            for filename, query in REPORT_QUERIES.items()
        }

    print("\nReconciliation complete.")
    print("Summary:")
    print(reports["reconciliation_summary.csv"].to_string(index=False))


if __name__ == "__main__":
    main()
