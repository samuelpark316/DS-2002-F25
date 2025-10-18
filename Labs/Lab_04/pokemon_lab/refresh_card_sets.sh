#!/usr/bin/env bash
set -euo pipefail

echo "Refreshing all card sets in card_set_lookup/ ..."

mkdir -p card_set_lookup

shopt -s nullglob

files=(card_set_lookup/*.json)

if [ ${#files[@]} -eq 0 ]; then
  echo "No JSON files found in card_set_lookup/. Nothing to refresh."
  exit 0
fi

for FILE in "${files[@]}"; do
  SET_ID="$(basename "$FILE" .json)"
  echo "Updating set: ${SET_ID} ..."
  curl -sS "https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250" \
    -o "$FILE"
  echo "Wrote latest data to: $FILE"
done

echo "All card sets have been refreshed."