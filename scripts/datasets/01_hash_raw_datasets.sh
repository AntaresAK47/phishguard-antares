#!/usr/bin/env bash
set -e

FECHA="$(date +%Y%m%d_%H%M%S)"
ROOT="/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares"
DATA_ROOT="$ROOT/tesis-phishing-dataset/multisource_v3"
OUT="$DATA_ROOT/06_hashes/SHA256_RAW_DATASETS_$FECHA.txt"

mkdir -p "$DATA_ROOT/06_hashes"

echo "Generando hashes SHA-256 de datasets crudos..."
find "$DATA_ROOT/01_raw" -type f \
  \( -name "*.csv" -o -name "*.xlsx" -o -name "*.zip" -o -name "*.7z" -o -name "*.json" -o -name "*.txt" \) \
  -print0 | sort -z | xargs -0 --no-run-if-empty sha256sum | tee "$OUT"

echo
echo "Hash generado en:"
echo "$OUT"
