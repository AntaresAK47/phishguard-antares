# 05 — Modelos y Datos

## Artefactos

| Modelo | Archivo | Tamaño | Tipo verificado | Entrada esperada |
|---|---|---|---|---|
| Textual | `models/modelo_textual.joblib` | 381 KB | `sklearn.pipeline.Pipeline` | `pd.Series` de 1 texto (asunto + cuerpo) |
| URL | `models/modelo_url.joblib` | 3 KB | `sklearn.pipeline.Pipeline` | `pd.DataFrame` 1×27 (columnas `URL_FEATURES`) |
| Híbrido | `models/modelo_hibrido.joblib` | 385 KB | `sklearn.pipeline.Pipeline` | `pd.DataFrame` 1×28 (`text` + 27 características) |

La carga se realiza exclusivamente desde rutas locales fijas (`src/config.MODEL_PATHS`), con caché `lru_cache(3)`. La etiqueta positiva es `1 = phishing` (`config.POSITIVE_LABEL`), localizada dinámicamente en `model.classes_` para robustez ante el orden de clases.

## Relación con la tesis

- Los tres artefactos son los **modelos validados** de la investigación. Esta auditoría **no** los modificó, reentrenó ni recalibró (verificable por hash; ver doc 09 §Integridad).
- **Interpretación técnica oficial** (regla metodológica del proyecto): el modelo **textual** obtuvo el mejor desempeño global en la validación; el modelo **híbrido** aporta valor complementario por mayor exhaustividad (recall) y una leve reducción de falsos negativos. Ninguna afirmación de esta documentación contradice esa lectura.
- Las métricas cuantitativas (matrices de confusión, precisión, recall, F1, etc.) **residen únicamente en el libro de tesis y sus evidencias**; no se transcriben aquí para evitar duplicidad divergente, y esta auditoría no inventa ni estima métricas.

## Datos procesados por el prototipo

- **En ejecución:** solo el texto que el usuario pega (asunto, cuerpo, enlaces). Se procesa en memoria; no se persiste automáticamente; no se envía a ningún servicio.
- **De entrenamiento:** no forman parte de este repositorio; pertenecen al proceso metodológico documentado en la tesis.

## Limitaciones de los modelos

1. Analizan **patrones léxicos y estructurales**; no consultan reputación, WHOIS, DNS ni contenido real de las páginas.
2. Un dominio legítimo con URL "rara" puede elevar el riesgo, y un phishing con URL "limpia" puede reducirlo: por eso la app muestra la **nota de calidad de contexto** que recomienda aportar texto + enlaces.
3. Dominio de entrenamiento: phishing en español latinoamericano en contexto institucional; la generalización fuera de ese dominio no está garantizada.
4. La probabilidad mostrada no es una calibración formal; la escala de 7 niveles es didáctica (declarado en `risk_rules.py` y en el propio reporte).

## Regla de custodia

Los `.joblib` no deben modificarse, renombrarse ni sobrescribirse sin autorización explícita y actualización coordinada de código, pruebas, README y manuales. Cualquier reentrenamiento futuro debe versionarse como artefactos nuevos, preservando estos como evidencia.
