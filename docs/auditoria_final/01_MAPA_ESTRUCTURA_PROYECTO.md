# 01 — Mapa de Estructura del Proyecto

Estructura real verificada el 03/07/2026 (67 archivos):

```text
phishguard-antares/
├── app.py                      # Entry point: interfaz Streamlit completa
├── README.md                   # Presentación, instalación y ejecución
├── requirements.txt            # Dependencias mínimas de ejecución
├── requirements-ubuntu-lock.txt# Versiones exactas validadas en Ubuntu
├── .gitignore                  # Exclusiones para control de versiones
├── .streamlit/
│   └── config.toml             # Tema oscuro, headless, telemetría OFF
├── assets/
│   ├── logo.png                # Logo activo usado por la app
│   ├── logo pro.png            # Variantes históricas (no usadas por el código)
│   ├── logo.jpeg               #   "
│   ├── logo1.png               #   "
│   ├── logo2.png               #   "
│   ├── logoanterior.png        #   "
│   └── screenshots/            # (vacía)
├── docs/
│   ├── checklist_pruebas.md    # Plan y registro de pruebas (dictamen APTO)
│   ├── manual_tecnico.md       # Manual técnico v2.0
│   ├── manual_usuario.md       # Manual de usuario v2.0
│   ├── estructura_*.txt        # Evidencias históricas de limpieza
│   ├── backups_limpieza_final/ # Respaldos fechados de archivos modificados
│   ├── evidencias_ubuntu/      # Capturas, reportes y auditorías previas
│   └── auditoria_final/        # ESTA documentación (12 documentos + guía GitHub)
├── models/
│   ├── modelo_textual.joblib   # Pipeline sklearn — 381 KB
│   ├── modelo_url.joblib       # Pipeline sklearn — 3 KB
│   └── modelo_hibrido.joblib   # Pipeline sklearn — 385 KB
├── outputs/
│   ├── logs/                   # Reservada (con .gitkeep; no se escribe automáticamente)
│   └── reports/                # Reservada (con .gitkeep; no se escribe automáticamente)
├── src/
│   ├── __init__.py             # Marca de paquete (vacío)
│   ├── config.py               # Rutas, nombres de modelos, constantes
│   ├── predictor.py            # Carga de modelos y función analyze()
│   ├── url_features.py         # Extracción de 27 características de URL como texto
│   ├── risk_rules.py           # Escala de riesgo de 7 niveles (presentación)
│   ├── report_builder.py       # Reporte TXT con neutralización de enlaces
│   └── ui_theme.py             # CSS consolidado del tema visual
└── tests/
    └── test_core.py            # 14 pruebas unitarias y de regresión
```

## Función de cada carpeta

- **Raíz:** entry point, dependencias y presentación del proyecto.
- **`.streamlit/`:** configuración del framework; incluye el tema base y la desactivación de telemetría.
- **`assets/`:** recursos gráficos. Solo `logo.png` es referenciado por el código (`app.py` → `LOGO_PATH`). Las cinco variantes restantes (~7,8 MB) se conservan como material histórico de diseño; ver recomendación en `08_AUDITORIA_DE_CODIGO.md`.
- **`docs/`:** manuales, checklist cerrado, evidencias de validación en Ubuntu, respaldos fechados y la presente auditoría.
- **`models/`:** los tres artefactos `.joblib` validados de la tesis. **No modificar, sobrescribir ni reentrenar.**
- **`outputs/`:** estructura reservada para salidas locales. El prototipo **no** escribe allí automáticamente (los reportes se descargan vía navegador); se mantiene con `.gitkeep` por trazabilidad de estructura.
- **`src/`:** lógica del sistema, separada de la interfaz.
- **`tests/`:** suite de regresión ejecutable con `python -m unittest discover -s tests`.
