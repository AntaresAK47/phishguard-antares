# 11 — Checklist Final del Software (Auditoría 03/07/2026)

Estados posibles: APROBADO · PENDIENTE · NO APLICA · REVISAR

## Funcionalidad

| Ítem | Estado | Evidencia |
|---|---|---|
| La aplicación arranca localmente | APROBADO | HTTP 200, consola sin errores |
| Carga modelo textual | APROBADO | Smoke + prueba #12 |
| Carga modelo URL | APROBADO | Smoke |
| Carga modelo híbrido | APROBADO | Smoke + prueba #12 |
| Análisis textual | APROBADO | Smoke caso 2 |
| Análisis URL | APROBADO | Smoke caso 3 |
| Análisis híbrido | APROBADO | Smoke casos 1 y 4 |
| Comparación de los tres modelos | APROBADO | Código + evidencias 24/06; flujo tolerante a fallos por modelo |
| Reporte TXT simple y comparativo | APROBADO | Pruebas #5, #6, #14 + reportes de evidencia |
| Persistencia/reapertura/limpieza de resultado | APROBADO | Código revisado + checklist histórico |
| Manejo de entradas vacías | APROBADO | Prueba #11 + validate_inputs |
| Texto con enlaces embebidos | APROBADO | LINK_SIGNAL_PATTERN + prueba #14 |
| URL neutralizadas como entrada (hxxps, `[.]`) | APROBADO | Fix H5 + prueba #8 |

## Seguridad y privacidad

| Ítem | Estado | Evidencia |
|---|---|---|
| No visita URLs / cero llamadas de red | APROBADO | Doc 06 (estática + dinámica) |
| No consulta APIs externas | APROBADO | Doc 06 |
| Telemetría del framework desactivada | APROBADO | config.toml + arranque verificado |
| Enlaces neutralizados en reportes | APROBADO | Pruebas #5 y #14 |
| Sin guardado automático de entradas sensibles | APROBADO | Revisión: solo download_button; outputs/ sin escritura |
| Escapado HTML de datos del usuario en la UI | APROBADO | Revisión de todos los bloques unsafe_allow_html |
| Sin funcionalidades ofensivas | APROBADO | Revisión integral |
| Modelos `.joblib` íntegros y sin cambios | APROBADO | Hashes SHA-256 (doc 09) |

## Calidad de código y pruebas

| Ítem | Estado | Evidencia |
|---|---|---|
| `py_compile` app+src+tests | APROBADO | Ejecutado 03/07/2026 |
| Suite unittest | APROBADO | 14/14 |
| pyflakes | APROBADO | 0 hallazgos |
| Firma pública `analyze` preservada | APROBADO | Prueba #9 |
| Regresión de vectores pre/post-fix | APROBADO | Idénticos en 5 entradas de referencia |
| Dependencias mínimas y reales | APROBADO | requirements sin matplotlib; validado empíricamente |
| Respaldos de archivos modificados | APROBADO | docs/backups_limpieza_final/ |

## Interfaz

| Ítem | Estado | Evidencia |
|---|---|---|
| Identidad visual carmesí/magenta/morado, estilo centro de comando | APROBADO | ui_theme v2.0 + capturas 24/06/2026 |
| Animación de análisis 0–100 % conservada | APROBADO | Código intacto |
| Ventana/modal de resultados y comparación | APROBADO | Código + capturas |
| Responsive y accesibilidad básica (contraste, focus-visible, reduced-motion) | APROBADO | ui_theme (5 breakpoints, media queries) |
| Verificación visual en navegador posterior a esta auditoría | PENDIENTE (tarea del tesista, 5 min) | Checklist manual del doc 07 §manual |

## Empaquetado y publicación

| Ítem | Estado | Evidencia |
|---|---|---|
| Export limpio 7z + SHA-256 | APROBADO | Generado por esta auditoría |
| `.gitignore` apto para GitHub | APROBADO | Reescrito (H3) |
| Guía de subida a GitHub | APROBADO | Doc 12 |
| Publicación efectiva en GitHub | PENDIENTE (acción del tesista con sus credenciales) | Doc 12 |

**DICTAMEN FINAL: APTO** — con dos pendientes menores de ejecución personal del tesista (verificación visual de 5 minutos y push a GitHub), ambos con procedimiento documentado.
