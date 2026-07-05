# 10 — Guía para Profesores de Auditoría Informática

Documento de apoyo para evaluar PhishGuard Antares en 30–45 minutos.

## 1. Qué es y qué no es

- **Es:** un prototipo académico local (Python + Streamlit) que clasifica de forma orientativa mensajes/URL con tres modelos de ML entrenados en la tesis, con trazabilidad, pruebas y reportes con enlaces neutralizados.
- **No es:** una herramienta profesional de ciberseguridad, un verificador de reputación en línea, ni un sistema con capacidades ofensivas.

## 2. Puesta en marcha (Ubuntu o Windows)

```bash
# 1) Entorno
python3 -m venv .venv && source .venv/bin/activate      # Windows: python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# 2) Validaciones automáticas
python -m py_compile app.py src/*.py tests/*.py
python -m unittest discover -s tests -v                  # Esperado: 14/14 OK

# 3) Aplicación
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## 3. Qué revisar y dónde (mapa de evidencias)

| Aspecto a auditar | Dónde verificarlo |
|---|---|
| Arquitectura y flujo | `docs/auditoria_final/02` y `04`; código en `src/` |
| Localidad / cero red | `docs/auditoria_final/06`; ejecutar `python -m unittest tests.test_core.LocalOnlyInferenceTests -v`; grep del doc 06 |
| Neutralización de enlaces | Descargar un reporte desde la app y buscar `hxxps://`/`www[.]`; pruebas #5 y #14 |
| Modelos y su custodia | `docs/auditoria_final/05`; hashes en doc 09; interpretación textual-vs-híbrido conforme a la tesis |
| Calidad de código | `docs/auditoria_final/08`; `python -m pyflakes app.py src/*.py` (0 hallazgos) |
| Pruebas y regresión | `docs/auditoria_final/07`; `tests/test_core.py` |
| Cambios de la auditoría y rollback | `docs/auditoria_final/09`; respaldos en `docs/backups_limpieza_final/` |
| Validación histórica en Ubuntu | `docs/checklist_pruebas.md` (dictamen APTO) y `docs/evidencias_ubuntu/` (capturas, reportes, auditorías) |
| Manuales | `docs/manual_tecnico.md`, `docs/manual_usuario.md` |

## 4. Verificaciones rápidas sugeridas en vivo

1. **Cero red:** desconecte la máquina de internet y repita un análisis híbrido — funciona igual (los modelos son locales).
2. **Entrada neutralizada:** pegue `hxxps://secure-login[.]example[.]com/verify` en el campo de URL — el sistema la analiza como texto sin error.
3. **Entradas vacías:** presione Analizar sin datos — mensaje de error claro, sin traceback.
4. **Comparación:** active "Comparar los tres modelos" con el ejemplo sospechoso del expander — tres tarjetas + tabla + reporte comparativo.
5. **Reporte:** descargue el TXT y confirme la neutralización y la advertencia metodológica final.
6. **Consola:** durante todo lo anterior, la terminal del servidor no muestra errores.

## 5. Preguntas de defensa que el software responde

- *¿Cómo garantizan que no visita URLs?* → Ausencia de primitivas de red en el código (doc 06, Evidencia 1) + prueba dinámica con sockets bloqueados (Evidencia 2) + telemetría del framework desactivada (Evidencia 3).
- *¿Qué recibe exactamente cada modelo?* → Textual: 1 texto; URL: DataFrame 1×27; Híbrido: DataFrame 1×28 (`text` + 27). Contratos blindados por pruebas #3 y #7.
- *¿Qué pasa con entradas maliciosas o malformadas?* → Se tratan como texto; `html.escape` en toda la UI dinámica; URL malformadas degradan sin abortar (fix H5); `ast.literal_eval` solo literales.
- *¿Los resultados de la tesis siguen siendo válidos tras la auditoría?* → Sí: modelos intactos (hashes en doc 09) y regresión de vectores idéntica bit a bit.

## 6. Limitaciones declaradas (transparencia)

Resultados orientativos; sin consulta de reputación; escala de riesgo didáctica; dominio de entrenamiento acotado (phishing en español latinoamericano institucional); desempeño fuera de dominio no garantizado. Ver doc 05 §Limitaciones.
