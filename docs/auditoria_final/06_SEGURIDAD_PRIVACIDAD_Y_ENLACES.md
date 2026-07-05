# 06 — Seguridad, Privacidad y Tratamiento de Enlaces

## Afirmación auditada

> "PhishGuard Antares procesa las entradas de forma local. Las URL se tratan como texto y no son visitadas, abiertas ni consultadas mediante servicios externos."

**Veredicto: CONFIRMADA con evidencia técnica reproducible.**

## Evidencia 1 — Inspección estática del código (03/07/2026)

Búsqueda exhaustiva en `app.py`, `src/` y `tests/` de primitivas de red y ejecución:

```bash
grep -rnE "import requests|urllib\.request|urlopen|http\.client|socket\.|webbrowser|subprocess|os\.system|eval\(|exec\(" app.py src/ tests/
```

Resultado: **cero llamadas de red**. Los únicos hallazgos relacionados y su naturaleza:

| Hallazgo | Ubicación | Naturaleza |
|---|---|---|
| `from urllib.parse import urlparse` | `url_features.py` | Análisis **léxico** de la cadena URL. `urllib.parse` no realiza conexiones (a diferencia de `urllib.request`, ausente). |
| `ast.literal_eval` | `url_features.py` | Evalúa **solo literales** de Python (listas/strings). No ejecuta código arbitrario; es la alternativa segura a `eval`. |
| `joblib.load` | `predictor.py` | Deserialización local de los 3 artefactos propios en `models/` con rutas fijas. Consideración estándar: pickle deserializado solo debe provenir de artefactos de confianza — condición cumplida por diseño (no se cargan archivos del usuario). |

## Evidencia 2 — Prueba dinámica con red bloqueada

`tests/test_core.py::LocalOnlyInferenceTests::test_full_analysis_works_with_network_blocked` parchea `socket.socket.connect`, `socket.create_connection` y `socket.getaddrinfo` para lanzar excepción ante **cualquier** intento de conexión, y ejecuta un análisis híbrido completo (carga de modelo incluida). La prueba **pasa**: la inferencia íntegra funciona sin red. Reproducible con:

```bash
python -m unittest tests.test_core.LocalOnlyInferenceTests -v
```

## Evidencia 3 — Telemetría del framework

Streamlit recolecta estadísticas de uso **por defecto**. Esta auditoría lo detectó en el arranque ("Collecting usage statistics...") y lo desactivó explícitamente en `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = false
```

Verificado post-cambio: el mensaje desaparece del arranque. Con ello, ni el prototipo ni su framework emiten datos.

## Neutralización de enlaces en reportes

`report_builder.neutralize_links` aplica sobre asunto, cuerpo y campo de URL antes de escribir el reporte:

- `https://` → `hxxps://`
- `http://` → `hxxp://`
- `www.` → `www[.]`

Blindado por 2 pruebas (`test_neutralize_links_makes_urls_non_clickable`, `test_report_neutralizes_links_embedded_in_body`) que verifican además la ausencia de `http(s)://` vivos en el reporte final. Simetría defensiva: el extractor también **acepta** entradas ya neutralizadas (`hxxps://`, `dominio[.]tld`) tratándolas como texto, sin "reactivarlas" jamás fuera de la normalización interna de análisis.

## Privacidad de las entradas

- Las entradas viven en memoria (`st.session_state`) durante la sesión del navegador; "Limpiar último resultado" las elimina.
- **No se escribe automáticamente** ningún archivo con datos del usuario: `outputs/` permanece vacío salvo acción manual; el reporte TXT se genera al vuelo y se entrega solo mediante `st.download_button`.
- No hay logging de contenido del usuario, ni cookies propias, ni identificadores.
- El servidor se ejecuta en `127.0.0.1` (loopback) según README y manuales.

## Carácter defensivo

El sistema no contiene ni genera funcionalidades ofensivas: no crea mensajes de phishing, no visita víctimas, no realiza scraping, no evade controles. Su única función es **clasificar de forma orientativa** entradas provistas por el usuario para fines académicos y preventivos.
