# Normalización y particiones V3 — PhishGuard Antares

## Archivos normalizados

### Dataset textual global

Archivo local utilizado:

`/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares/tesis-phishing-dataset/multisource_v3/03_processed/textual_global/textual_global_normalizado_20260708_182613.csv`

Columnas principales normalizadas:

- `record_id`
- `source_dataset`
- `source_hash`
- `label_binary`
- `label_name`
- `subject`
- `body`
- `urls`
- `date`
- `url_count`
- `attachments_count`
- `hops_count`

### Dataset URL global

Archivo local utilizado:

`/home/sansi_gnomo_magico/Escritorio/Tesis N°1 - Antares/tesis-phishing-dataset/multisource_v3/03_processed/url_global/url_global_balanceado_20260708_182613.csv`

Columnas principales normalizadas:

- `record_id`
- `source_dataset`
- `source_id`
- `label_binary`
- `label_name`
- `url`
- `domain`
- `rank`
- `target`
- `date`

## Criterios de etiquetado

| Valor | Interpretación |
|---|---|
| `1` | Phishing / spear-phishing |
| `0` | Legítimo / legítimo-control |

## Particiones generadas

### Textual

| Partición | Total | Etiquetas | Fuentes |
|---|---:|---|---|
| Entrenamiento | 3521 | `{'phishing': 2098, 'legitimo': 1423}` | `{'spearphishmx': 2405, 'spaphish': 1116}` |
| Prueba | 880 | `{'phishing': 524, 'legitimo': 356}` | `{'spearphishmx': 601, 'spaphish': 279}` |

### URL

| Partición | Total | Etiquetas | Fuentes |
|---|---:|---|---|
| Entrenamiento | 103428 | `{'phishing': 51714, 'legitimo_control': 51714}` | `{'phishtank': 51714, 'tranco': 51714}` |
| Prueba | 25856 | `{'legitimo_control': 12928, 'phishing': 12928}` | `{'tranco': 12928, 'phishtank': 12928}` |

## Semilla

Las particiones fueron generadas con semilla reproducible:

`42`

## Nota de seguridad

Las URLs se neutralizaron como `hxxp`, `hxxps` o con `[.]` cuando correspondía, para evitar apertura accidental.
