# Integración de modelos production_multisource_v1

Fecha: 20260708_201451

## Cambio realizado

Se configuró PhishGuard Antares para usar por defecto los modelos globales entrenados con múltiples datasets:

- SpaPhish
- SpearPhishMX
- PhishTank
- Tranco

## Preservación de línea base

Los modelos anteriores no fueron eliminados. Permanecen preservados como baseline en:

models/baseline_spaphish_v1/

## Modelos activos

- Modelo textual global
- Modelo URL global
- Modelo híbrido global

## Seguridad

La aplicación continúa procesando URLs como texto. No visita enlaces ni consulta servicios externos.
