#!/usr/bin/env python3
import os, sys, json, glob
import pandas as pd

def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    all_lookup_df = []
    json_files = sorted(glob.glob(os.path.join(lookup_dir, "*.json")))
    if not json_files:
        return pd.DataFrame(columns=[
            "card_id","card_name","card_number","set_id","set_name","card_market_value"
        ])
    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cards = data.get("data", [])
        if not cards:
            continue
        df = pd.json_normalize(cards)
        holo = df.get("tcgplayer.prices.holofoil.market", pd.Series([None]*len(df)))
        normal = df.get("tcgplayer.prices.normal.market", pd.Series([None]*len(df)))
        df["card_market_value"] = holo.fillna(normal).fillna(0.0)
        rename_map = {
            "id": "card_id",
            "name": "card_name",
            "number": "card_number",
            "set.id": "set_id",
            "set.name": "set_name",
        }
        df = df.rename(columns=rename_map)
        required_cols = [
            "card_id", "card_name", "card_number", "set_id", "set_name", "card_market_value"
        ]
        for c in required_cols:
            if c not in df.columns:
                df[c] = pd.NA
        df = df[required_cols].copy()
        df["card_number"] = df["card_number"].astype(str)
        df["card_market_value"] = pd.to_numeric(df["card_market_value"], errors="coerce").fillna(0.0)
        all_lookup_df.append(df)
    if not all_lookup_df:
        return pd.DataFrame(columns=[
            "card_id","card_name","card_number","set_id","set_name","card_market_value"
        ])
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False).drop_duplicates(
        subset=["card_id"], keep="first"
    ).reset_index(drop=True)
    return lookup_df

def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    inventory_data = []
    csv_files = sorted(glob.glob(os.path.join(inventory_dir, "*.csv")))
    for path in csv_files:
        try:
            df = pd.read_csv(path)
            inventory_data.append(df)
        except Exception as e:
            print(f"Warning: could not read {path}: {e}", file=sys.stderr)
    if not inventory_data:
        return pd.DataFrame(columns=[
            "card_name","set_id","card_number","binder_name","page_number","slot_number","card_id"
        ])
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    for col in ["set_id", "card_number"]:
        if col not in inventory_df.columns:
            inventory_df[col] = ""
    inventory_df["set_id"] = inventory_df["set_id"].astype(str).str.strip()
    inventory_df["card_number"] = inventory_df["card_number"].astype(str).str.strip()
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]
    return inventory_df

def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)
    final_cols = [
        "index","binder_name","page_number","slot_number","card_id",
        "card_name","set_id","set_name","card_number","card_market_value"
    ]
    if inventory_df.empty:
        print("ERROR: Inventory is empty. Writing empty portfolio CSV.", file=sys.stderr)
        empty = pd.DataFrame(columns=final_cols)
        empty.to_csv(output_file, index=False)
        print(f"Wrote empty portfolio: {output_file}")
        return
    merge_cols_from_lookup = ["card_id","card_name","set_id","set_name","card_number","card_market_value"]
    lookup_trimmed = lookup_df[merge_cols_from_lookup].copy() if not lookup_df.empty else pd.DataFrame(columns=merge_cols_from_lookup)
    merged = pd.merge(inventory_df, lookup_trimmed, on="card_id", how="left", suffixes=("_inv", ""))
    if "card_market_value" not in merged.columns:
        merged["card_market_value"] = 0.0
    merged["card_market_value"] = pd.to_numeric(merged["card_market_value"], errors="coerce").fillna(0.0)
    if "set_name" not in merged.columns:
        merged["set_name"] = "NOT_FOUND"
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")
    if "card_name" in merged.columns and "card_name_inv" in merged.columns:
        merged["card_name"] = merged["card_name"].fillna(merged["card_name_inv"])
    for c in ["binder_name","page_number","slot_number"]:
        if c not in merged.columns:
            merged[c] = ""
    merged["index"] = (
        merged["binder_name"].astype(str) + "-" +
        merged["page_number"].astype(str) + "-" +
        merged["slot_number"].astype(str)
    )
    for c in final_cols:
        if c not in merged.columns:
            merged[c] = pd.NA
    out = merged[final_cols].copy()
    out.to_csv(output_file, index=False)
    print(f"Portfolio updated: {output_file}")

def main():
    update_portfolio("./card_inventory/", "./card_set_lookup/", "card_portfolio.csv")

def test():
    update_portfolio("./card_inventory_test/", "./card_set_lookup_test/", "test_card_portfolio.csv")

if __name__ == "__main__":
    print("update_portfolio.py starting in Test Mode (using *_test/ dirs)...", file=sys.stderr)
    test()