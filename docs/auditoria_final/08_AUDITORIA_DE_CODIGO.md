# 08 — Auditoría de Código: Hallazgos y Decisiones

Metodología: inspección manual línea a línea de `app.py` y `src/`, análisis estático (`pyflakes`), grep exhaustivo de primitivas de red/ejecución, ejecución de la suite, smoke funcional con red bloqueada, arranque headless de Streamlit y prueba de regresión de vectores.

## Hallazgos corregidos

| ID | Hallazgo | Archivo | Severidad | Evidencia | Decisión y validación |
|---|---|---|---|---|---|
| H1 | Import muerto: `URL_FEATURES` importado y no usado | `src/predictor.py` | Baja | `pyflakes` | **CORREGIDO** (import retirado). Post-fix: pyflakes 0 hallazgos; 14/14 tests. |
| H2 | Dependencia no utilizada: `matplotlib` declarada pero jamás importada | `requirements.txt` | Baja | grep sin coincidencias; suite y app ejecutadas con éxito en entorno **sin** matplotlib | **CORREGIDO** (retirada de requirements). El lock de Ubuntu se conserva intacto como evidencia histórica del entorno validado. |
| H3 | `.gitignore` defectuoso: patrón `**pycache**/` mutilado (artefacto de Markdown sobre `__pycache__/`), finales CRLF, y **no ignoraba `.venv_ubuntu/`** (el venv que el propio README indica crear) ni `.pytest_cache/` | `.gitignore` | Media (para control de versiones) | Inspección; riesgo real de subir un entorno virtual completo a GitHub | **CORREGIDO** (reescrito; ver doc 09). Sin efecto en ejecución. |
| H4 | Telemetría del framework activa: Streamlit recolecta estadísticas de uso por defecto, contradiciendo el espíritu "sin servicios externos" | `.streamlit/config.toml` | Media (privacidad) | Mensaje "Collecting usage statistics" en arranque | **CORREGIDO** (`gatherUsageStats = false`). Verificado: mensaje ausente post-cambio; arranque HTTP 200. |
| H5 | **Bug funcional:** URL neutralizada con esquema (`hxxps://dominio[.]tld/ruta`) provocaba `ValueError: Invalid IPv6 URL` no controlado. Causa raíz: el regex de extracción excluía `]`, truncando en `secure-login[.`; `urlparse` interpretaba el corchete residual como IPv6. La docstring prometía soporte de dominios neutralizados. En la app, el usuario veía "No se pudo realizar el análisis: Invalid IPv6 URL". | `src/url_features.py` | **Media** | Reproducción determinista; descubierto por prueba nueva | **CORREGIDO** en dos capas: (a) regex acepta el token literal `[.]` dentro del enlace; (b) guardia `try/except ValueError` en `web_features` degrada URL malformadas a análisis léxico sin host, sin abortar. **Regresión: vectores idénticos** en las 5 entradas de referencia pre/post-fix. Prueba de regresión permanente añadida (#8). |
| H6 | `outputs/logs/` y `outputs/reports/` vacíos: git no versiona carpetas vacías → la estructura documentada se perdería en GitHub | `outputs/` | Baja | Convención de git | **CORREGIDO** (`.gitkeep` en ambas). |

## Hallazgos con decisión CONSERVAR (justificada)

| ID | Hallazgo | Archivo | Severidad | Decisión |
|---|---|---|---|---|
| H7 | Símbolos definidos y no invocados por la app: `load_all_models`, `compact_result` (predictor); `risk_color` (risk_rules); `merge_url_inputs` (url_features); `validate_model_files`, `OUTPUTS_DIR/REPORTS_DIR/LOGS_DIR`, `RISK_THRESHOLDS`, `LABEL_NAMES`, `NEGATIVE_LABEL` (config) | varios | Baja | **CONSERVAR.** Constituyen una pequeña API de diagnóstico/terminal y constantes de reserva documentadas (algunas usadas por la propia suite, p. ej. `load_all_models`). Eliminarlas no aporta beneficio funcional, reduce utilidades de depuración defendibles ante tribunal y contradice el principio de cambios mínimos. Nota de coherencia: la escala vigente de riesgo es la de `risk_rules.risk_profile` (7 niveles); `RISK_THRESHOLDS` queda como reserva histórica. |
| H8 | Recursos gráficos no referenciados por el código: `logo pro.png`, `logo.jpeg`, `logo1.png`, `logo2.png`, `logoanterior.png` (~7,8 MB en total); `assets/screenshots/` vacía | `assets/` | Baja | **CONSERVAR + RECOMENDACIÓN.** Regla del proyecto: no eliminar archivos sin autorización. Son material histórico de diseño. *Recomendación opcional* del auditor: si se desea aligerar el repositorio público, moverlos a `docs/backups_limpieza_final/` o eliminarlos en un commit dedicado y reversible. La app solo requiere `assets/logo.png` (con degradación elegante a monograma "PG" si faltara). |
| H9 | Escala de riesgo con 7 niveles definida dos veces conceptualmente (colores del `risk_profile` vs. minipaleta ilustrativa del centro de mando en `app.py`) | `app.py`/`risk_rules.py` | Muy baja | **CONSERVAR.** La minipaleta del centro de mando es ilustrativa (5 muestras de gradiente), no un mapa 1:1 de niveles; ambos usan la misma familia cromática. Unificarlas no aporta valor y tocaría UI validada. |

## Aspectos evaluados sin hallazgos

- **Inyección HTML/XSS:** todo dato dinámico interpolado en bloques `unsafe_allow_html` pasa por `html.escape` (verificado en tarjetas, minicards, loader, notas y previsualización).
- **Manejo de errores:** excepciones de análisis capturadas y comunicadas con `st.error` legible; entradas vacías validadas antes de inferir; modo comparativo tolera fallos por modelo sin abortar.
- **Rutas:** todas derivadas de `Path(__file__)` — sin rutas absolutas de máquina.
- **CSS:** organizado con variables `:root`, secciones comentadas, 5 breakpoints y `prefers-reduced-motion`; los selectores repetidos son overrides responsivos legítimos.
- **Consistencia código ↔ documentación:** README, manual técnico y manual de usuario describen la v2.0 real; la firma documentada de `analyze` coincide con el código (ahora blindada por test).

## Dictamen de código

**APTO.** Código claro, modular, con separación UI/lógica, docstrings pertinentes, type hints en el núcleo y superficie de ataque mínima. Los seis hallazgos corregidos elevan higiene, privacidad y robustez sin alterar ningún comportamiento validado.
