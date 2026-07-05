# 09 — Reporte de Cambios (Auditoría 03/07/2026)

**Principio aplicado:** cambios mínimos, justificados, respaldados y validados. Firma pública, modelos, métricas, UI validada y enfoque local: **intactos**.

## Respaldos previos (creados antes de cualquier edición)

Carpeta `docs/backups_limpieza_final/`, sufijo `_pre_auditoria_20260703`:
`gitignore`, `requirements`, `README`, `config_toml`, `predictor`, `test_core`, `url_features`.

## Archivos modificados

| Archivo | Cambio exacto | Motivo | Validación |
|---|---|---|---|
| `src/predictor.py` | Eliminada 1 línea: `URL_FEATURES,` del bloque de import | H1: import muerto (pyflakes) | pyflakes limpio; 14/14 tests; smoke OK |
| `src/url_features.py` | (a) Regex del caso 2 de `split_raw_links`: de `[^\s,\];|]+` a `(?:\[\.\]|[^\s,;|\[\]])+` con comentario; (b) `web_features`: `urlparse` envuelto en `try/except ValueError` con degradación a `host=""`/esquema léxico; (c) `uses_https` calculado desde la variable `scheme` protegida | H5: bug "Invalid IPv6 URL" con URL neutralizadas con esquema | **Regresión de vectores: idénticos** (5 entradas de referencia); bug irreproducible; tests #8 y 14/14 OK |
| `requirements.txt` | Retirada `matplotlib`; añadido salto de línea final | H2: dependencia no importada por ningún módulo | Suite completa + arranque de app ejecutados en entorno sin matplotlib: OK |
| `.gitignore` | Reescrito: `__pycache__/` correcto, LF, añade `.venv_ubuntu/`, `venv/`, `.pytest_cache/`, editores, `.env`, `*.7z/*.zip`; preserva estructura de `outputs/` vía negaciones `!.gitkeep` | H3: patrón mutilado y venv del README no ignorado | Inspección; `git status` limpio tras init |
| `.streamlit/config.toml` | Añadida sección `[browser]` con `gatherUsageStats = false` | H4: telemetría del framework activa por defecto | Arranque HTTP 200; mensaje de telemetría ausente; 0 errores |
| `tests/test_core.py` | **Ampliación aditiva** (las 6 pruebas originales quedan intactas): +8 pruebas en 4 clases nuevas (contrato de firma, alias, entradas vacías, forma híbrida 1×28, URL neutralizadas, inferencia con red bloqueada, repetibilidad, neutralización en cuerpo) | Blindar contrato, seguridad y el fix H5 | 14/14 APROBADAS |
| `README.md` | Aditivo: sección **Instalación** (venv + pip, Ubuntu y Windows), sección **Ejecución en Windows**, referencia a `docs/auditoria_final/`; requisito corregido de "Python 3.14 o superior" a "Python 3.10 o superior (validado en Python 3.14)" — el código emplea sintaxis `X | None` disponible desde 3.10 | Reproducibilidad para terceros (tribunal/GitHub) sin alterar el contenido validado | Lectura; coherente con manuales y lock |

## Archivos creados

- `outputs/logs/.gitkeep`, `outputs/reports/.gitkeep` (H6).
- `docs/auditoria_final/00…11_*.md` (esta documentación) y `12_GUIA_SUBIDA_GITHUB.md`.
- Respaldos fechados listados arriba.

## Archivos NO tocados (garantía)

- `models/*.joblib` — integridad verificable por hash:

```text
382eeffb77ce5cc240bc1af3ffca41a9932dea6ea7890855345efb89146723c0  models/modelo_textual.joblib
44230184c22f7b996954071197b3d8f16a5f4a961161fce63f0f95a07be3b421  models/modelo_url.joblib
7b3eca59da22174ac3ead1fb452dde7545bfb1cc31f1974d8266497a904e294a  models/modelo_hibrido.joblib
```

- `app.py`, `src/ui_theme.py`, `src/risk_rules.py`, `src/report_builder.py`, `src/config.py`, `src/__init__.py`.
- `requirements-ubuntu-lock.txt`, manuales, checklist, evidencias históricas, capturas, assets y logo.

## Decisión sobre la mejora visual solicitada

La interfaz v2.0 ("versión dorada") ya implementa íntegramente la estética requerida: centro de comando plegable, paleta carmesí/fucsia/morado con variables CSS, animación 0–100 %, ventana modal de resultado, píldoras de señales, medidor, responsive en 5 breakpoints y `prefers-reduced-motion`. Fue **validada visualmente el 24/06/2026** con capturas en `docs/evidencias_ubuntu/capturas/`. Conforme a las reglas "no sacrificar estabilidad por estética" y "mejorar solo si no rompe nada", y dado que esta auditoría se ejecuta sin verificación visual de navegador, el dictamen profesional es **APROBADA SIN CAMBIOS**: cualquier retoque a ciegas del CSS introduciría riesgo sin evidencia de beneficio.

## Cómo revertir (rollback)

Cada archivo modificado tiene su copia exacta en `docs/backups_limpieza_final/*_pre_auditoria_20260703.*`; basta restaurarla sobre la ruta original. Los cambios además quedan aislables commit a commit si se sigue la guía de GitHub (doc 12).
