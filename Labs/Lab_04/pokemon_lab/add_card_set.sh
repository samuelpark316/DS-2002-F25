#!/usr/bin/env bash
set -euo pipefail

read -rp "Enter TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
  echo "Error: Set ID cannot be empty." >&2
  exit 1
fi

mkdir -p card_set_lookup

echo "Fetching card data for set: ${SET_ID} ..."
curl -sS "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250" \
  -o "card_set_lookup/${SET_ID}.json"

if [ -s "card_set_lookup/${SET_ID}.json" ]; then
  echo "Saved: card_set_lookup/${SET_ID}.json"
else
  echo "Warning: Download finished but file is empty. Check the set id or API status." >&2
fi