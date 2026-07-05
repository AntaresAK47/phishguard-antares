# 07 — Pruebas, Validación y Regresión

## Suite automática actual: 14 pruebas (14/14 APROBADAS el 03/07/2026)

| # | Prueba | Clase | Qué protege |
|---|---|---|---|
| 1 | `test_safe_text_accepts_none_and_lists` | UrlFeatureTests | Robustez de entrada (None, listas) |
| 2 | `test_split_raw_links_detects_common_link_types` | UrlFeatureTests | Detección http/mailto/cid |
| 3 | `test_feature_frame_keeps_expected_shape` | UrlFeatureTests | Contrato 1×27 del modelo URL |
| 4 | `test_summary_has_user_facing_keys` | UrlFeatureTests | Resumen legible de señales |
| 5 | `test_neutralize_links_makes_urls_non_clickable` | ReportBuilderTests | Neutralización básica |
| 6 | `test_comparative_report_uses_riesgo_key` | ReportBuilderTests | Formato del comparativo |
| 7 | `test_hybrid_frame_has_text_plus_27_features` | HybridFrameTests | Contrato 1×28 del híbrido |
| 8 | `test_neutralized_urls_are_treated_as_text_links` | HybridFrameTests | Regresión del bug H5 (hxxps + `[.]`) |
| 9 | `test_analyze_signature_is_preserved` | PredictorContractTests | **Firma pública validada de `analyze`** |
| 10 | `test_normalize_model_name_accepts_documented_aliases` | PredictorContractTests | Alias y error controlado |
| 11 | `test_empty_inputs_raise_controlled_value_error` | PredictorContractTests | Entradas vacías → ValueError claro |
| 12 | `test_full_analysis_works_with_network_blocked` | LocalOnlyInferenceTests | **Cero red durante inferencia real** |
| 13 | `test_analysis_is_repeatable` | LocalOnlyInferenceTests | Determinismo del análisis |
| 14 | `test_report_neutralizes_links_embedded_in_body` | ReportNeutralizationTests | Neutralización en cuerpo/asunto |

Nota: las pruebas 12–13 (y 9–11 parcialmente) requieren el entorno con dependencias instaladas y los `.joblib` presentes; son pruebas de integración local deliberadas.

## Comandos de validación (copiables)

```bash
# Desde la raíz del proyecto, con el entorno virtual activo
python -m py_compile app.py src/*.py tests/*.py
python -m unittest discover -s tests -v
python -m pyflakes app.py src/*.py tests/*.py        # opcional: pip install pyflakes
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## Resultados de esta auditoría

| Validación | Resultado |
|---|---|
| `py_compile` (app + src + tests) | APROBADO |
| `unittest` 14 pruebas | APROBADO (OK) |
| `pyflakes` | 0 hallazgos |
| Arranque Streamlit headless | HTTP 200 · 0 errores/tracebacks en consola · sin mensaje de telemetría |
| Smoke funcional (4 casos, red bloqueada por socket) | APROBADO: híbrido 78,76 % (Muy alto), textual legítimo 32,53 % (Precaución), URL con IP 57,54 % (Alto), híbrido con mailto/cid 10,10 % (Bajo) |
| Regresión de vectores de características pre/post-fix | IDÉNTICOS (0 diferencias en 5 entradas de referencia) |
| Entradas vacías por modelo | ValueError controlado en los 3 modos |

## Checklist funcional manual para el tesista

1. Abrir la app (`streamlit run ...`) y verificar carga sin errores en consola.
2. Análisis **textual** con el ejemplo legítimo del expander de la app.
3. Análisis **URL** pegando solo un enlace.
4. Análisis **híbrido** con el ejemplo sospechoso sugerido.
5. Activar **Comparar los tres modelos** y verificar las tres tarjetas + tabla.
6. **Descargar reporte TXT** (simple y comparativo) y abrirlo.
7. Confirmar en el TXT: `hxxps://`, `www[.]`, ausencia de `https://` vivo.
8. Pegar una URL neutralizada `hxxps://dominio[.]com/ruta` y verificar que analiza sin error (regresión H5).
9. **Limpiar último resultado** y **Reabrir ventana de resultado** desde la tarjeta compacta.
10. Colapsar y reabrir el **centro de mando**; verificar que las preferencias persisten.
11. Verificar consola del servidor: cero errores durante toda la sesión.

## Pruebas recomendadas a futuro (no bloqueantes)

- Prueba de humo de la UI con `streamlit.testing.v1.AppTest` (render de `main()` sin navegador).
- Caso de propiedad: fuzzing ligero de `split_raw_links` con cadenas aleatorias (nunca debe lanzar excepción).
- Verificación de hashes de `models/*.joblib` como prueba de integridad en CI.
