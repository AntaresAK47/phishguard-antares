from functools import lru_cache
import re
from typing import Any

import joblib
import pandas as pd

from src.config import MODEL_DISPLAY_NAMES, MODEL_PATHS, POSITIVE_LABEL
from src.risk_rules import label_name, probability_percent, risk_level, risk_message
from src.url_features import (
    URL_FEATURES,
    build_feature_frame,
    build_hybrid_frame,
    safe_text,
    summarize_features,
)


# ============================================================
# predictor.py
# Carga de modelos y predicción para PhishGuard Antares.
#
# Seguridad:
# - No visita enlaces.
# - No consulta APIs externas.
# - No modifica los modelos.
# - Solo usa los modelos .joblib entrenados localmente.
# ============================================================


LINK_SIGNAL_PATTERN = re.compile(
    r"(hxxps?://|https?://|www\.|mailto:|cid:|\[\.\]|\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b)",
    re.IGNORECASE,
)


def normalize_model_name(model_name: str) -> str:
    """
    Normaliza y valida el nombre interno del modelo.
    """
    model_name = safe_text(model_name).lower()

    aliases = {
        "textual": "textual",
        "texto": "textual",
        "url": "url",
        "urls": "url",
        "hibrido": "hibrido",
        "híbrido": "hibrido",
        "hybrid": "hibrido",
    }

    if model_name not in aliases:
        valid = ", ".join(MODEL_PATHS.keys())
        raise ValueError(f"Modelo no reconocido: {model_name}. Modelos válidos: {valid}")

    return aliases[model_name]


@lru_cache(maxsize=3)
def load_model(model_name: str):
    """
    Carga un modelo .joblib desde la carpeta models.

    Se usa caché para evitar cargar el mismo modelo varias veces
    durante una sesión de uso del prototipo.
    """
    model_name = normalize_model_name(model_name)
    model_path = MODEL_PATHS[model_name]

    if not model_path.exists():
        raise FileNotFoundError(f"No se encontró el modelo {model_name}: {model_path}")

    return joblib.load(model_path)


def load_all_models() -> dict:
    """
    Carga los tres modelos entrenados.
    """
    return {
        model_name: load_model(model_name)
        for model_name in MODEL_PATHS.keys()
    }


def build_text_input(subject: str = "", body: str = "") -> str:
    """
    Construye el texto que será enviado al modelo textual o híbrido.
    """
    subject = safe_text(subject)
    body = safe_text(body)

    return f"{subject}\n{body}".strip()


def build_url_input(subject: str = "", body: str = "", urls_raw: str = "") -> str:
    """
    Construye la entrada de enlaces para el extractor URL.

    Regla importante:
    - Siempre usa el campo urls_raw si el usuario lo proporciona.
    - Solo añade asunto/cuerpo si contienen señales reales de enlace.
      Esto evita que texto normal sea contado como enlaces no web.
    """
    parts = []

    urls_raw = safe_text(urls_raw)
    if urls_raw:
        parts.append(urls_raw)

    text = build_text_input(subject, body)
    if text and LINK_SIGNAL_PATTERN.search(text):
        parts.append(text)

    return "\n".join(parts).strip()


def positive_probability(model: Any, X) -> float | None:
    """
    Obtiene la probabilidad asociada a la clase positiva:
    1 = phishing.

    Retorna None si el modelo no soporta predict_proba.
    """
    if not hasattr(model, "predict_proba"):
        return None

    probabilities = model.predict_proba(X)[0]
    classes = list(model.classes_)

    if POSITIVE_LABEL not in classes:
        raise ValueError(
            f"El modelo no contiene la clase positiva esperada: {POSITIVE_LABEL}. "
            f"Clases encontradas: {classes}"
        )

    positive_index = classes.index(POSITIVE_LABEL)
    return float(probabilities[positive_index])


def build_result(
    model_name: str,
    prediction: int,
    probability: float | None,
    features: pd.DataFrame | None = None,
    text_used: str = "",
    urls_used: str = "",
) -> dict:
    """
    Construye un resultado estándar para la interfaz.
    """
    model_name = normalize_model_name(model_name)

    result = {
        "modelo": model_name,
        "modelo_nombre": MODEL_DISPLAY_NAMES.get(model_name, model_name),
        "label_predicho": int(prediction),
        "clase_predicha": label_name(int(prediction)),
        "probabilidad_phishing": probability,
        "probabilidad_formato": probability_percent(probability),
        "nivel_riesgo": risk_level(probability),
        "mensaje_riesgo": risk_message(probability),
        "texto_usado": safe_text(text_used),
        "enlaces_usados": safe_text(urls_used),
        "features": features,
        "feature_summary": summarize_features(urls_used) if urls_used else {},
    }

    return result


def predict_textual(model, text: str) -> tuple[int, float | None]:
    """
    Predicción usando únicamente contenido textual.
    """
    text = safe_text(text)

    if not text:
        raise ValueError("El modelo textual requiere contenido de texto.")

    X = pd.Series([text])
    prediction = int(model.predict(X)[0])
    probability = positive_probability(model, X)

    return prediction, probability


def predict_url(model, urls_raw: str) -> tuple[int, float | None, pd.DataFrame]:
    """
    Predicción usando únicamente características URL/enlaces.
    """
    urls_raw = safe_text(urls_raw)

    if not urls_raw:
        raise ValueError("El modelo URL requiere al menos una URL o enlace.")

    X = build_feature_frame(urls_raw)
    prediction = int(model.predict(X)[0])
    probability = positive_probability(model, X)

    return prediction, probability, X


def predict_hybrid(model, text: str, urls_raw: str) -> tuple[int, float | None, pd.DataFrame]:
    """
    Predicción usando texto + características URL/enlaces.
    """
    text = safe_text(text)

    if not text:
        raise ValueError("El modelo híbrido requiere contenido de texto.")

    X = build_hybrid_frame(text, urls_raw)
    prediction = int(model.predict(X)[0])
    probability = positive_probability(model, X)

    return prediction, probability, X


def analyze(
    model_name: str,
    subject: str = "",
    body: str = "",
    urls_raw: str = "",
) -> dict:
    """
    Función principal de análisis para la aplicación.

    Parámetros:
    - model_name: textual, url o hibrido.
    - subject: asunto del mensaje.
    - body: cuerpo del mensaje.
    - urls_raw: URL/enlaces pegados por el usuario.

    Retorna:
    - Diccionario con clase predicha, probabilidad, riesgo y señales.
    """
    model_name = normalize_model_name(model_name)
    text = build_text_input(subject, body)
    urls_input = build_url_input(subject, body, urls_raw)

    model = load_model(model_name)

    if model_name == "textual":
        prediction, probability = predict_textual(model, text)

        return build_result(
            model_name=model_name,
            prediction=prediction,
            probability=probability,
            features=None,
            text_used=text,
            urls_used="",
        )

    if model_name == "url":
        prediction, probability, features = predict_url(model, urls_input)

        return build_result(
            model_name=model_name,
            prediction=prediction,
            probability=probability,
            features=features,
            text_used="",
            urls_used=urls_input,
        )

    if model_name == "hibrido":
        prediction, probability, features = predict_hybrid(model, text, urls_input)

        return build_result(
            model_name=model_name,
            prediction=prediction,
            probability=probability,
            features=features,
            text_used=text,
            urls_used=urls_input,
        )

    raise ValueError(f"Modelo no reconocido: {model_name}")


def compact_result(result: dict) -> dict:
    """
    Versión resumida del resultado para imprimir en pruebas de terminal.
    """
    return {
        "modelo": result.get("modelo_nombre"),
        "clase_predicha": result.get("clase_predicha"),
        "probabilidad_phishing": result.get("probabilidad_formato"),
        "nivel_riesgo": result.get("nivel_riesgo"),
        "mensaje_riesgo": result.get("mensaje_riesgo"),
        "feature_summary": result.get("feature_summary"),
    }
