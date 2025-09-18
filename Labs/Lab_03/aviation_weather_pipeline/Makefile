.PHONY: all fetch analyze clean

analyze: fetch
	@echo "[analyze] Starting analysis into weather_report.csv..."
	@./analyze_data.sh
	@echo "[analyze] Done. Pipeline completed successfully. Output -> weather_report.csv"

fetch:
	@echo "[fetch] Fetching METAR JSON into raw_metars/..."
	@./fetch_metars.sh
	@echo "[fetch] Finished fetching. Files are in raw_metars/"

clean:
	@echo "[clean] Removing generated files..."
	@rm -rf raw_metars weather_report.csv
	@echo "[clean] Workspace reset."

all: analyze