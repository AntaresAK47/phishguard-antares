# Métricas production_multisource_v1 — PhishGuard Antares

Archivo de métricas fuente:

`/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares/Auditoria - Software - Terminado/Auditoria de PhishGuard Antares/phishguard-antares/models/production_multisource_v1/metrics_production_multisource_v1_20260708_190314.json`

## Resultados principales

| Modelo | Accuracy | Precision | Recall | F1-score | ROC-AUC | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| textual_global | 0.8000 | 0.8973 | 0.7500 | 0.8170 | 0.9056 | 311 | 45 | 131 | 393 |
| url_global | 0.9922 | 0.9992 | 0.9852 | 0.9922 | 0.9977 | 12918 | 10 | 191 | 12737 |
| fusion_hibrido_global | 0.8307 | 0.8898 | 0.8168 | 0.8517 | 0.9124 | 303 | 53 | 96 | 428 |

## Interpretación técnica

El modelo híbrido global mejora al modelo textual global en F1-score, recall y reducción de falsos negativos. El modelo URL global obtiene métricas elevadas sobre el conjunto PhishTank-Tranco; sin embargo, debe interpretarse con cautela metodológica, debido a que utiliza un conjunto de prueba distinto y Tranco funciona como fuente legítima/control.

## Advertencia académica

Las métricas del modelo textual e híbrido se calculan sobre el conjunto textual de prueba. Las métricas del modelo URL se calculan sobre el conjunto URL PhishTank-Tranco. Por tanto, no deben compararse de manera simplista como si provinieran del mismo conjunto de evaluación.
