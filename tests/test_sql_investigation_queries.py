from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "trade_recon.db"
SQL_PATH = ROOT / "sql" / "04_investigation_queries.sql"


def test_investigation_sql_file_exists():
    assert SQL_PATH.exists(), "sql/04_investigation_queries.sql should exist"


def test_investigation_sql_executes_against_database():
    assert DB_PATH.exists(), "trade_recon.db should exist after make run or make check"

    sql = SQL_PATH.read_text()

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql)
