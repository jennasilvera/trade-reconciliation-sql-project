help:
	@echo "Trade Reconciliation SQL Project"
	@echo ""
	@echo "Available commands:"
	@echo "  make run      Generate data, load database, and run reconciliation"
	@echo "  make quality  Run data quality checks"
	@echo "  make preview  Generate Markdown preview of output reports"
	@echo "  make test     Run pytest suite"
	@echo "  make check    Run full workflow, preview, quality checks, and tests"
	@echo "  make clean    Remove generated database and report files"

.PHONY: run generate load reconcile test clean

generate:
	python src/generate_data.py

load:
	python src/load_database.py

reconcile:
	python src/run_reconciliation.py

run: generate load reconcile

test:
	pytest -q

clean:
	rm -f trade_recon.db
	rm -f data/raw/*.csv
	rm -f data/reports/*.csv

preview:
	python src/export_report_preview.py

check:
	make run
	make quality
	make preview
	pytest

quality:
	python src/run_data_quality_checks.py

