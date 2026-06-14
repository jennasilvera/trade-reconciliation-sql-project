"""Load generated CSV data into a local SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from config import (
    BROKER_ALLOCATIONS_CSV,
    BROKER_TRADES_CSV,
    DB_PATH,
    INTERNAL_ALLOCATIONS_CSV,
    INTERNAL_TRADES_CSV,
    SQL_DIR,
)

TABLE_LOADS = {
    "internal_trades": INTERNAL_TRADES_CSV,
    "broker_trades": BROKER_TRADES_CSV,
    "internal_allocations": INTERNAL_ALLOCATIONS_CSV,
    "broker_allocations": BROKER_ALLOCATIONS_CSV,
}


def execute_sql_file(connection: sqlite3.Connection, sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    connection.executescript(sql)


def validate_input_files() -> None:
    missing = [str(path) for path in TABLE_LOADS.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing CSV files. Run `python src/generate_data.py` first. Missing: "
            + ", ".join(missing)
        )


def main() -> None:
    validate_input_files()

    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as connection:
        execute_sql_file(connection, SQL_DIR / "01_create_tables.sql")

        for table_name, csv_path in TABLE_LOADS.items():
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, connection, if_exists="append", index=False)
            print(f"Loaded {len(df):,} rows into {table_name}")

        connection.commit()

    print(f"SQLite database created at {DB_PATH}")


if __name__ == "__main__":
    main()
