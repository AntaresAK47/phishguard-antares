# 00 — Resumen Ejecutivo del Software

**Sistema:** PhishGuard Antares — Versión 2.0
**Tipo:** Prototipo académico local de detección de phishing
**Tesis asociada:** "Modelo híbrido de aprendizaje automático para la detección de phishing en español latinoamericano mediante análisis integrado de contenido textual y características léxicas de URL en entornos institucionales."
**Fecha de auditoría:** 03/07/2026
**Dictamen general:** APTO CON OBSERVACIONES MENORES (todas corregidas y documentadas)

## 1. Qué es PhishGuard Antares

PhishGuard Antares es un prototipo académico desarrollado en Python 3 y Streamlit que estima, de forma local y orientativa, si un mensaje, correo o conjunto de enlaces presenta patrones compatibles con phishing. Ofrece tres modos de análisis basados en modelos de aprendizaje automático entrenados previamente y serializados en formato `.joblib`:

1. **Modelo textual:** analiza asunto y cuerpo del mensaje.
2. **Modelo URL:** analiza 27 características léxicas y estructurales de URL/enlaces, tratados exclusivamente como texto.
3. **Modelo híbrido texto–URL:** integra el contenido textual con las 27 características de enlaces.

## 2. Propósito académico

El software constituye la evidencia práctica de la tesis: materializa el modelo híbrido propuesto, permite compararlo con los modelos textual y URL, y genera reportes locales con enlaces neutralizados como evidencia reproducible. Interpretación técnica vigente (según la validación de la tesis): el modelo textual obtuvo el mejor desempeño global; el modelo híbrido aporta valor complementario por mayor exhaustividad y una leve reducción de falsos negativos. Las métricas formales residen en el libro de tesis y no se replican aquí para evitar inconsistencias.

## 3. Garantías de seguridad verificadas en esta auditoría

- **Procesamiento 100 % local.** No existe en el código ninguna llamada de red: no hay `requests`, `urllib.request`, `urlopen`, `http.client`, `socket`, `webbrowser` ni `subprocess`. El único uso de `urllib` es `urllib.parse.urlparse` (análisis léxico sin conexión).
- **Prueba de aislamiento:** la suite incluye una prueba que bloquea la red a nivel de `socket` y ejecuta un análisis híbrido completo con éxito (`tests/test_core.py::LocalOnlyInferenceTests`).
- **Telemetría desactivada:** se deshabilitó explícitamente la recolección de estadísticas de uso del framework Streamlit (`gatherUsageStats = false`).
- **Enlaces neutralizados en reportes** (`https://` → `hxxps://`, `www.` → `www[.]`), verificado por pruebas automáticas.
- **Sin persistencia automática de entradas sensibles:** los reportes solo se descargan por acción explícita del usuario.

## 4. Estado general

| Aspecto | Estado |
|---|---|
| Compilación (`py_compile`) | APROBADO |
| Suite de pruebas (14 pruebas) | APROBADO (14/14) |
| Análisis estático (`pyflakes`) | LIMPIO (0 hallazgos) |
| Arranque Streamlit local | APROBADO (HTTP 200, 0 errores en consola) |
| Carga de los 3 modelos `.joblib` | APROBADO |
| Análisis textual / URL / híbrido / comparativo | APROBADO |
| Reporte TXT con neutralización | APROBADO |
| Interfaz visual v2.0 | APROBADA sin cambios (validada visualmente el 24/06/2026) |

## 5. Alcance y limitaciones

- El resultado es **orientativo**: clasifica patrones compatibles con phishing; no verifica reputación de dominios ni consulta listas externas.
- No sustituye herramientas profesionales de ciberseguridad ni políticas institucionales.
- La escala de riesgo de 7 niveles es didáctica, no una calibración probabilística formal.
- Los modelos fueron entrenados con datos de la tesis; su desempeño fuera de ese dominio no está garantizado.

## 6. Intervención realizada (síntesis)

Se corrigieron 6 hallazgos (1 bug funcional de severidad media, 5 mejoras de higiene/seguridad de configuración), se amplió la suite de pruebas de 6 a 14 casos, y se generó la presente documentación de auditoría. Ningún modelo, métrica, firma pública ni comportamiento validado fue alterado; la regresión de vectores de características fue verificada como idéntica bit a bit. Detalle completo en `08_AUDITORIA_DE_CODIGO.md` y `09_REPORTE_DE_CAMBIOS.md`.
