#!/usr/bin/env python3
import sys

import update_portfolio
import generate_summary

def run_production_pipeline():
    print("[pipeline] Starting production pipeline...", file=sys.stderr)

    print("[pipeline] ETL: update_portfolio.main()", file=sys.stderr)
    update_portfolio.main()

    print("[pipeline] Reporting: generate_summary.main()", file=sys.stderr)
    generate_summary.main()

    print("[pipeline] Done.", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()