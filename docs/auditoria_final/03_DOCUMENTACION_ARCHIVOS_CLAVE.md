# 03 — Documentación de Archivos Clave

Estado auditado al 03/07/2026. Formato por archivo: propósito, funciones principales, dependencias internas, entradas/salidas, riesgos, estado y recomendaciones.

---

## `app.py` (996 líneas)
- **Propósito:** interfaz Streamlit completa: encabezado, centro de mando plegable, formularios, animación de análisis 0–100 %, ventana modal de resultado, comparación de modelos, persistencia de sesión y descarga de reportes.
- **Funciones principales:** `main`, `render_command_center`, `render_command_rail`, `render_workspace`, `render_input_area`, `validate_inputs`, `run_loading_animation`, `run_single_analysis`, `run_comparative_analysis`, `render_result_card`, `render_comparative_content`, `open_dialog`, `store_*`/`clear_persisted_result`, `build_context_quality`.
- **Dependencias internas:** `src.config`, `src.predictor.analyze`, `src.report_builder.build_report_text`, `src.risk_rules.risk_profile`, `src.ui_theme.APP_CSS`.
- **Entradas:** asunto (text_input), cuerpo (text_area), URL/enlaces (text_area), selección de modelo, opciones de comparación/avanzado.
- **Salidas:** dictamen visual, señales, tablas técnicas, reporte TXT descargable.
- **Riesgos:** usa `unsafe_allow_html=True` para el tema premium; **mitigado** porque todo dato dinámico del usuario pasa por `html.escape` antes de interpolarse (verificado en `render_result_card`, `render_model_mini_card`, `render_persisted_result`, animación y notas de contexto).
- **Estado:** APROBADO. **Recomendaciones:** ninguna bloqueante.

## `src/config.py` (54 líneas)
- **Propósito:** configuración central (rutas con `pathlib`, nombres de modelos, textos, umbrales).
- **Entradas/Salidas:** constantes; `validate_model_files()` retorna dict de existencia de modelos.
- **Riesgos:** `RISK_THRESHOLDS` y `LABEL_NAMES` no son consumidos por la app (la escala vigente vive en `risk_rules.risk_profile`); riesgo de divergencia documental BAJO.
- **Estado:** APROBADO. **Recomendación:** tratar `RISK_THRESHOLDS`/`LABEL_NAMES`/`validate_model_files` como API de reserva/diagnóstico (decisión: CONSERVAR, ver doc 08).

## `src/predictor.py` (294 líneas)
- **Propósito:** carga cacheada de modelos y orquestación de los tres modos de análisis.
- **Funciones principales:** `normalize_model_name` (alias: texto/textual, url/urls, hibrido/híbrido/hybrid), `load_model` (`@lru_cache(3)`), `load_all_models`, `build_text_input`, `build_url_input`, `positive_probability`, `build_result`, `predict_textual|url|hybrid`, **`analyze` (contrato público)**, `compact_result`.
- **Contrato preservado:** `analyze(model_name: str, subject: str = '', body: str = '', urls_raw: str = '') -> dict` — verificado por prueba automática de firma.
- **Entradas:** strings del usuario. **Salidas:** dict estandarizado (clase, probabilidad, nivel, mensajes, features, resumen).
- **Riesgos:** `joblib.load` deserializa pickle: solo debe cargar artefactos propios de `models/` (así ocurre; rutas fijas desde `config.MODEL_PATHS`). Riesgo residual BAJO y documentado en doc 06.
- **Estado:** APROBADO (se retiró un import muerto; ver doc 09).

## `src/url_features.py` (505 líneas)
- **Propósito:** detección/clasificación de enlaces y cálculo de las 27 características léxicas; construcción de DataFrames para modelos URL e híbrido. **Nunca visita enlaces.**
- **Funciones principales:** `safe_text`, `merge_url_inputs`, `normalize_url_for_parsing`, `split_raw_links` (4 estrategias en cascada), `classify_links`, `is_ip_address`, `count_subdomains`, `contains_shortener`, `web_features`, `extract_all_features`, `build_feature_frame` (1×27), `build_hybrid_frame` (1×28, columna `text` primero), `summarize_features`.
- **Riesgos:** entrada adversaria por definición. Hallazgo H5 (URL neutralizada con esquema provocaba `ValueError: Invalid IPv6 URL`) **corregido** con regresión de vectores idéntica; guardia defensiva añadida en `web_features`. `ast.literal_eval` solo evalúa literales (seguro; no ejecuta código).
- **Estado:** APROBADO tras corrección.

## `src/risk_rules.py` (179 líneas)
- **Propósito:** capa de presentación del riesgo: escala didáctica de 7 niveles con color, icono, titular y mensaje; wrappers de compatibilidad `risk_level`, `risk_message`, `risk_color`.
- **Riesgos:** ninguno funcional; la escala se declara explícitamente como no-calibración formal.
- **Estado:** APROBADO.

## `src/report_builder.py` (100 líneas)
- **Propósito:** construir el reporte TXT descargable con dictamen, señales, comparación opcional, entrada neutralizada y advertencias.
- **Funciones:** `neutralize_links` (`https→hxxps`, `http→hxxp`, `www.→www[.]`), `build_report_text`.
- **Riesgos:** ninguno; no escribe a disco, no persiste entradas.
- **Estado:** APROBADO (blindado con 2 pruebas adicionales de neutralización).

## `src/ui_theme.py` (1542 líneas)
- **Propósito:** CSS consolidado del tema "centro de comando" oscuro (variables `:root`, paleta carmesí/fucsia/morado, botones, formularios, hero, centro de mando, riel plegado, loader circular, tarjetas de dictamen, medidor, píldoras, modal, 5 breakpoints responsivos y `prefers-reduced-motion`).
- **Riesgos:** selectores repetidos corresponden a overrides responsivos legítimos dentro de `@media` (verificado), no a duplicación desordenada. Depende de `data-testid` de Streamlit: una actualización mayor del framework puede requerir ajustes cosméticos (riesgo BAJO, propio de todo theming en Streamlit; fijado por el lock file).
- **Estado:** APROBADO SIN CAMBIOS (versión dorada validada visualmente el 24/06/2026).

## `tests/test_core.py` (14 pruebas)
- **Propósito:** regresión del núcleo. Originales (6): safe_text, detección de enlaces, forma 1×27, resumen, neutralización, clave "Riesgo" en comparativo. Añadidas (8): forma híbrida 1×28, URL neutralizadas como texto, **firma de `analyze` preservada**, alias de modelos, entradas vacías controladas, **inferencia completa con red bloqueada a nivel socket**, repetibilidad determinista, neutralización de enlaces embebidos en cuerpo.
- **Estado:** APROBADO (14/14). Requiere dependencias instaladas y `models/` presente para las pruebas de inferencia.

## `README.md`
- **Propósito:** presentación, características, requisitos, instalación (Ubuntu y Windows), ejecución, evidencias, limitaciones y seguridad.
- **Estado:** APROBADO (se añadió sección de instalación y ejecución en Windows; requisito corregido a "Python 3.10 o superior, validado en 3.14" — el código usa sintaxis `X | None` de 3.10+).

## `requirements.txt`
- **Propósito:** dependencias mínimas reales de ejecución: `streamlit`, `pandas`, `numpy`, `scikit-learn`, `joblib`.
- **Estado:** APROBADO (se retiró `matplotlib`, no importada por ningún módulo; demostrado ejecutando toda la suite y la app en un entorno sin matplotlib). Las versiones exactas validadas permanecen en `requirements-ubuntu-lock.txt` como evidencia histórica.
