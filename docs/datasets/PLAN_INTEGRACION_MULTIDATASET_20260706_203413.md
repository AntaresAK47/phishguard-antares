# Plan de integración multi-dataset — PhishGuard Antares

## Fecha
20260706_203413

## Decisión técnica

La versión actual auditada queda congelada como PhishGuard Antares v2.0 baseline.  
La nueva fase construirá PhishGuard Antares v3.0 multi-dataset.

## Arquitectura objetivo

models/
├── baseline_spaphish_v1/
├── experiments_by_source/
│   ├── spaphish_only/
│   ├── spearphishmx_only/
│   └── phishtank_tranco_url/
└── production_multisource_v1/

## Modelos objetivo

1. modelo_textual_global.joblib
2. modelo_url_global.joblib
3. modelo_fusion_hibrido_global.joblib

## Criterio académico

No se reemplazarán los modelos existentes sin conservar baseline, métricas, model cards, hashes y documentación.
