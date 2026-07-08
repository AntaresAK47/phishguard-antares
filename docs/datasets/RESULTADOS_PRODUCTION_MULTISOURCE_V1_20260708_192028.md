# Resultados production_multisource_v1 — PhishGuard Antares

## Modelos generados

- modelo_textual_global.joblib
- modelo_url_global.joblib
- modelo_fusion_hibrido_global.joblib

## Métricas principales

### textual_global

- Accuracy: 0.8000
- Precision: 0.8973
- Recall: 0.7500
- F1: 0.8170
- ROC-AUC: 0.9056
- TN: 311 | FP: 45 | FN: 131 | TP: 393

### url_global

- Accuracy: 0.9922
- Precision: 0.9992
- Recall: 0.9852
- F1: 0.9922
- ROC-AUC: 0.9977
- TN: 12918 | FP: 10 | FN: 191 | TP: 12737

### fusion_hibrido_global

- Accuracy: 0.8307
- Precision: 0.8898
- Recall: 0.8168
- F1: 0.8517
- ROC-AUC: 0.9124
- TN: 303 | FP: 53 | FN: 96 | TP: 428

## Dictamen técnico

El modelo híbrido global mejora al modelo textual global en F1, recall y reducción de falsos negativos. El modelo URL global presenta métricas elevadas sobre PhishTank-Tranco, pero debe interpretarse con cautela metodológica porque utiliza fuentes distintas y Tranco opera como control legítimo.

## Carpeta de modelos

/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares/Auditoria - Software - Terminado/Auditoria de PhishGuard Antares/phishguard-antares/models/production_multisource_v1
