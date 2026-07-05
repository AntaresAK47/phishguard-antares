# 02 — Arquitectura Funcional

## Flujo general

```text
Entrada del usuario (asunto, cuerpo, URL/enlaces)
        │
        ▼
Validación de entradas (app.py::validate_inputs)
        │
        ▼
Construcción de insumos (predictor.build_text_input / build_url_input)
        │
        ▼
Extracción de señales URL como texto (url_features — 27 características)
        │
        ▼
Modelo local .joblib (textual | url | hibrido, con caché lru_cache)
        │
        ▼
Resultado estandarizado (predictor.build_result + risk_rules.risk_profile)
        │
        ▼
Presentación (ventana modal, tarjeta de dictamen, medidor, señales)
        │
        ▼
Reporte TXT descargable con enlaces neutralizados (report_builder)
```

## Capas y responsabilidades

| Capa | Módulos | Responsabilidad |
|---|---|---|
| Presentación | `app.py`, `src/ui_theme.py`, `.streamlit/config.toml` | Formularios, centro de mando, animación 0–100 %, ventana de resultado, comparación, descarga de reporte, persistencia de sesión. |
| Dominio / inferencia | `src/predictor.py` | Normalización de nombre de modelo, carga cacheada de `.joblib`, orquestación de los tres modos, contrato `analyze()`. |
| Extracción de señales | `src/url_features.py` | Detección y clasificación de enlaces (web, mailto, cid, otros), 27 características léxicas, DataFrames para modelo URL e híbrido. Todo como texto. |
| Interpretación | `src/risk_rules.py` | Escala didáctica de 7 niveles (Muy bajo → Crítico), colores, mensajes. No reemplaza a los modelos. |
| Evidencia | `src/report_builder.py` | Reporte TXT, neutralización `https→hxxps`, `www.→www[.]`, advertencias metodológicas. |
| Configuración | `src/config.py` | Rutas absolutas derivadas de `Path(__file__)`, nombres de modelos, textos de la app. |

## Decisiones de diseño relevantes

1. **Separación UI/lógica:** `app.py` no calcula características ni carga modelos directamente; delega en `src/`. Esto permite probar el núcleo sin Streamlit (la suite de tests no importa Streamlit).
2. **Contrato público estable:** `analyze(model_name, subject='', body='', urls_raw='') -> dict` es la única puerta de entrada de la UI a la inferencia. Está blindado por prueba de firma (`PredictorContractTests`).
3. **Caché de modelos:** `@lru_cache(maxsize=3)` evita recargar los `.joblib` en cada rerun de Streamlit.
4. **Estado de sesión con claves duraderas:** las preferencias del centro de mando se duplican en claves `*_persisted` porque Streamlit descarta las claves de widgets que dejan de renderizarse (patrón documentado en `app.py::init_session_defaults`).
5. **Modal con degradación:** `open_dialog` usa `st.dialog` si existe; si la versión de Streamlit no lo soporta, renderiza en página. Garantiza compatibilidad hacia atrás.
6. **URL como texto adversario:** ninguna URL se visita; el extractor tolera formatos neutralizados (`hxxps://`, `dominio[.]tld`) y, tras esta auditoría, degrada con elegancia ante URL malformadas en lugar de abortar.
