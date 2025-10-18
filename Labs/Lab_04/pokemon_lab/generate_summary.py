#!/usr/bin/env python3
import os, sys
import pandas as pd

def generate_summary(portfolio_file: str) -> None:
    if not os.path.exists(portfolio_file):
        print(f"ERROR: Portfolio file not found: {portfolio_file}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("Portfolio is empty. Nothing to summarize.")
        return
    
    if "card_market_value" not in df.columns:
        print("ERROR: Missing 'card_market_value' column in portfolio.", file=sys.stderr)
        sys.exit(1)

    df["card_market_value"] = pd.to_numeric(df["card_market_value"], errors="coerce").fillna(0.0)

    total_portfolio_value = df["card_market_value"].sum()

    max_idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[max_idx]

    print("\n=== Pokémon Portfolio Summary ===")
    print(f"Total Portfolio Market Value: ${total_portfolio_value:,.2f}")
    print("Most Valuable Card:")
    print(f"  Name: {most_valuable_card.get('card_name', 'UNKNOWN')}")
    print(f"  ID:   {most_valuable_card.get('card_id', 'UNKNOWN')}")
    print(f"  Value: ${float(most_valuable_card.get('card_market_value', 0.0)):,.2f}")
    print("=================================\n")


def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")


if __name__ == "__main__":
    test()