#!/usr/bin/env bash
set -e

ROOT="/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares"
SOFT="$ROOT/Auditoria - Software - Terminado/Auditoria de PhishGuard Antares/phishguard-antares"
DATA_ROOT="$ROOT/tesis-phishing-dataset/multisource_v3"

echo "Verificando estructura multi-dataset..."
echo

for path in \
  "$DATA_ROOT/01_raw/spaphish" \
  "$DATA_ROOT/01_raw/spearphishmx" \
  "$DATA_ROOT/01_raw/phishtank" \
  "$DATA_ROOT/01_raw/tranco" \
  "$DATA_ROOT/03_processed/textual_global" \
  "$DATA_ROOT/03_processed/url_global" \
  "$SOFT/models/baseline_spaphish_v1" \
  "$SOFT/models/production_multisource_v1" \
  "$SOFT/docs/datasets" \
  "$SOFT/scripts/datasets"
do
  if [ -d "$path" ]; then
    echo "OK     $path"
  else
    echo "FALTA  $path"
  fi
done
