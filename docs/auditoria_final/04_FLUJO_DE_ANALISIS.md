# 04 — Flujo de Análisis Paso a Paso

Recorrido exacto cuando el usuario presiona **Analizar**:

1. **Captura de entradas** (`render_input_area`): asunto, cuerpo y URL/enlaces como texto plano. Nada se guarda en disco.
2. **Validación** (`validate_inputs`):
   - Modo textual/híbrido sin texto → error claro y `st.stop()`.
   - Modo URL sin URL ni texto con enlaces → error claro y `st.stop()`.
3. **Animación local** (`run_loading_animation`): anillo 0→100 % (~4,9 s) con etapas descriptivas. Es retroalimentación visual del procesamiento local; **no** representa conexión externa (así se rotula en pantalla: "Procesamiento local · Sin abrir enlaces · Sin APIs externas").
4. **Construcción de insumos** (`predictor`):
   - `build_text_input`: `"{asunto}\n{cuerpo}".strip()`.
   - `build_url_input`: usa siempre `urls_raw`; añade asunto/cuerpo **solo** si contienen señales reales de enlace (`LINK_SIGNAL_PATTERN`), evitando que texto normal se cuente como enlaces.
5. **Carga del modelo** (`load_model`): lee `models/<modelo>.joblib` desde ruta fija local, con caché `lru_cache(3)`.
6. **Extracción de señales** (solo modos URL/híbrido, `url_features`):
   - `split_raw_links`: 4 estrategias en cascada (lista literal → regex de esquemas incl. `hxxp(s)` y token `[.]` → dominios sueltos/neutralizados → separadores simples).
   - `classify_links`: web / mailto / cid / otros; los correos con `@` no se confunden con dominios.
   - `web_features`: 19 métricas léxicas (longitudes, dígitos, símbolos, subdominios, IP en host, HTTPS, acortadores, palabras sospechosas ES/EN) + 8 contadores de tipos = **27 columnas exactas** del entrenamiento.
   - Cualquier URL malformada degrada a análisis léxico sin host (guardia añadida en esta auditoría); jamás aborta el análisis.
7. **Inferencia:**
   - Textual: `model.predict(Series[text])` + `predict_proba`.
   - URL: `model.predict(DataFrame 1×27)`.
   - Híbrido: `model.predict(DataFrame 1×28)` con columna `text` + 27 características.
   - `positive_probability` localiza la clase positiva (1 = phishing) vía `model.classes_`; si el modelo no expone `predict_proba`, retorna `None` y la UI muestra "No disponible".
8. **Resultado estandarizado** (`build_result`): clase, probabilidad formateada, nivel de 7 grados (`risk_profile`), mensaje, texto/enlaces usados, DataFrame de features y resumen legible.
9. **Persistencia de sesión** (`store_single_result`/`store_comparative_result`): el resultado queda en `st.session_state` para reabrir la ventana sin re-analizar; "Limpiar último resultado" lo elimina.
10. **Ventana de resultado** (`maybe_open_result_dialog` → `st.dialog` o degradación en página): tarjeta de dictamen con color por nivel, medidor 0–100 %, nota de calidad de contexto, píldoras de señales, análisis avanzado (tablas) y **botón de descarga del reporte TXT**.

## Modo comparativo

`run_comparative_analysis` valida como híbrido, ejecuta los tres modelos tolerando fallos por modelo (los errores se listan en tabla sin abortar los demás), toma el híbrido como lectura principal y genera reporte comparativo con las filas de los tres.

## Reporte TXT

`build_report_text` arma: encabezado con fecha local, modelo, clase, probabilidad, nivel; mensaje de riesgo; señales URL; comparación (si aplica); **entrada neutralizada** (asunto, URL y cuerpo pasan por `neutralize_links`); y advertencia metodológica final. El archivo se entrega vía `st.download_button` — descarga bajo acción explícita del usuario; nada se escribe en `outputs/` automáticamente.
