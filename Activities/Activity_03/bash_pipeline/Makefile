all: process_data

# A rule to fetch the data
fetch_data:
	@echo "--- Fetching data ---"
	bash ./fetch_data.sh

# A rule to process the data, which depends on 'fetch_data'
process_data: fetch_data
	@echo "--- Processing data ---"
	bash ./process_data.sh
	@echo "--- Pipeline complete ---"

clean:
	@echo "--- Cleaning up ---"
	rm -f breeds.json