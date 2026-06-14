from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
REPORTS_DIR = ROOT_DIR / "data" / "reports"
SQL_DIR = ROOT_DIR / "sql"
DB_PATH = ROOT_DIR / "trade_recon.db"

INTERNAL_TRADES_CSV = DATA_RAW_DIR / "internal_trades.csv"
BROKER_TRADES_CSV = DATA_RAW_DIR / "broker_trades.csv"
INTERNAL_ALLOCATIONS_CSV = DATA_RAW_DIR / "internal_allocations.csv"
BROKER_ALLOCATIONS_CSV = DATA_RAW_DIR / "broker_allocations.csv"
EXPECTED_BREAKS_CSV = DATA_RAW_DIR / "expected_breaks.csv"
