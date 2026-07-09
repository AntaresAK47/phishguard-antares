# Cierre técnico — PhishGuard Antares V3.0 Multidataset

## Estado del software

PhishGuard Antares quedó actualizado a la versión:

`3.0-multidataset`

## Repositorio

- Remoto: `https://github.com/AntaresAK47/phishguard-antares.git`
- Rama: `main`
- Commit actual: `358280b`
- Tags en commit actual: `v3.0-multidataset-20260708`

## Modelos activos

Los modelos activos se encuentran en:

`models/production_multisource_v1/`

Archivos principales:

- `modelo_textual_global.joblib`
- `modelo_url_global.joblib`
- `modelo_fusion_hibrido_global.joblib`
- `metrics_production_multisource_v1_20260708_190314.json`
- `model_card.md`
- `thresholds.json`

## Línea base preservada

Los modelos anteriores fueron preservados en:

`models/baseline_spaphish_v1/`

Esto permite trazabilidad entre la versión V2.0 basada en SpaPhish y la versión V3.0 multi-dataset.

## Pruebas

La versión V3.0 fue validada localmente con pruebas unitarias:

- Resultado: **14/14 pruebas OK**
- Inferencia textual: funcional.
- Inferencia URL: funcional.
- Inferencia híbrida: funcional.
- Reporte local TXT: funcional.

## Seguridad

El prototipo mantiene el principio defensivo:

- No visita URLs.
- No abre enlaces.
- No consulta APIs externas.
- Procesa URLs únicamente como texto.
- Genera reportes neutralizados.

## Dictamen

PhishGuard Antares V3.0 Multidataset queda técnicamente apto como versión principal del software académico para la tesis, sujeto a la actualización correspondiente del libro de tesis.
