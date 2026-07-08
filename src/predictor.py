from functools import lru_cache
import html
import math
import re
from collections import Counter
from typing import Any
from urllib.parse import urlparse

import joblib
import pandas as pd

from src.config import MODEL_DISPLAY_NAMES, MODEL_PATHS, POSITIVE_LABEL
from src.risk_rules import label_name, probability_percent, risk_level, risk_message
from src.url_features import (
    build_feature_frame,
    build_hybrid_frame,
    safe_text,
    summarize_features,
)


LINK_SIGNAL_PATTERN = re.compile(
    r"(hxxps?://|https?://|www\.|mailto:|cid:|\[\.\]|\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b)",
    re.IGNORECASE,
)

GLOBAL_URL_FEATURES = [
    "url_len", "hostname_len", "path_len", "query_len",
    "digits_count", "special_count", "dot_count", "hyphen_count",
    "at_count", "question_count", "equal_count", "ampersand_count",
    "percent_count", "slash_count", "subdomain_count",
    "contains_ip", "uses_https", "suspicious_words_count",
    "shortener_present", "entropy",
]

SUSPICIOUS_WORDS = [
    "login", "verify", "verification", "account", "secure", "update", "password",
    "bank", "wallet", "confirm", "urgent", "support", "signin", "session",
    "validate", "token", "bonus", "reward", "free", "invoice", "payment",
    "verificar", "cuenta", "seguridad", "urgente", "contraseña", "banco",
    "actualizar", "confirmar", "validar", "premio", "pago",
]

SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "cutt.ly", "rebrand.ly", "shorturl.at",
]


def normalize_model_name(model_name: str) -> str:
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
    model_name = normalize_model_name(model_name)
    model_path = MODEL_PATHS[model_name]

    if not model_path.exists():
        raise FileNotFoundError(f"No se encontró el modelo {model_name}: {model_path}")

    return joblib.load(model_path)


def load_all_models() -> dict:
    return {
        model_name: load_model(model_name)
        for model_name in MODEL_PATHS.keys()
    }


def unwrap_model(model: Any) -> tuple[Any, list[str] | None]:
    if isinstance(model, dict) and "model" in model:
        return model["model"], model.get("feature_names")
    return model, None


def is_global_url_model(model: Any) -> bool:
    _, feature_names = unwrap_model(model)
    return bool(feature_names and "url_len" in feature_names)


def is_global_fusion_model(model: Any) -> bool:
    _, feature_names = unwrap_model(model)
    return bool(feature_names and "text_prob" in feature_names)


def build_text_input(subject: str = "", body: str = "") -> str:
    subject = safe_text(subject)
    body = safe_text(body)
    return f"{subject}\n{body}".strip()


def build_url_input(subject: str = "", body: str = "", urls_raw: str = "") -> str:
    parts = []

    urls_raw = safe_text(urls_raw)
    if urls_raw:
        parts.append(urls_raw)

    text = build_text_input(subject, body)
    if text and LINK_SIGNAL_PATTERN.search(text):
        parts.append(text)

    return "\n".join(parts).strip()


def deneutralize_url(value: str) -> str:
    value = safe_text(value)
    value = html.unescape(value)
    value = value.replace("hxxps://", "https://").replace("hxxp://", "http://")
    value = value.replace("[.]", ".")
    value = value.replace("\\/", "/")
    return value.strip().strip("[]'\"<> .,;")


def entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = Counter(value)
    total = len(value)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def extract_candidate_urls(value: str) -> list[str]:
    text = deneutralize_url(value)

    pattern = re.compile(
        r"(?:https?://[^\s,\]\)\"'<>]+|www\.[^\s,\]\)\"'<>]+|\b[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s,\]\)\"'<>]*)?)",
        re.IGNORECASE,
    )

    candidates = []
    for match in pattern.findall(text):
        candidate = deneutralize_url(match)
        if candidate and "." in candidate:
            candidates.append(candidate)

    if not candidates and text and "." in text and LINK_SIGNAL_PATTERN.search(text):
        candidates.append(text)

    unique = []
    seen = set()
    for candidate in candidates:
        key = candidate.lower()
        if key not in seen:
            unique.append(candidate)
            seen.add(key)

    return unique


def url_features_one(url: str) -> dict:
    raw = deneutralize_url(url)
    parsed_input = raw if re.match(r"^[a-zA-Z]+://", raw) else "http://" + raw

    try:
        parsed = urlparse(parsed_input)
        host = (parsed.hostname or parsed.netloc or "").lower()
        path = parsed.path or ""
        query = parsed.query or ""
    except Exception:
        host = ""
        path = raw
        query = ""

    full = raw.lower()
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    subdomain_count = max(0, len(host.split(".")) - 2) if host else 0

    return {
        "url_len": len(raw),
        "hostname_len": len(host),
        "path_len": len(path),
        "query_len": len(query),
        "digits_count": sum(ch.isdigit() for ch in raw),
        "special_count": sum(not ch.isalnum() for ch in raw),
        "dot_count": raw.count("."),
        "hyphen_count": raw.count("-"),
        "at_count": raw.count("@"),
        "question_count": raw.count("?"),
        "equal_count": raw.count("="),
        "ampersand_count": raw.count("&"),
        "percent_count": raw.count("%"),
        "slash_count": raw.count("/"),
        "subdomain_count": subdomain_count,
        "contains_ip": int(bool(re.search(ip_pattern, host))),
        "uses_https": int(raw.startswith("https://")),
        "suspicious_words_count": sum(word in full for word in SUSPICIOUS_WORDS),
        "shortener_present": int(any(shortener in host for shortener in SHORTENERS)),
        "entropy": entropy(raw),
    }


def build_global_url_feature_frame(urls_raw: str, feature_names: list[str] | None = None) -> pd.DataFrame:
    feature_names = feature_names or GLOBAL_URL_FEATURES
    urls = extract_candidate_urls(urls_raw)
    rows = [url_features_one(url) for url in urls]

    if not rows:
        return pd.DataFrame(columns=feature_names)

    return pd.DataFrame(rows).reindex(columns=feature_names, fill_value=0).fillna(0)


def positive_probabilities(model: Any, X) -> list[float] | None:
    core_model, _ = unwrap_model(model)

    if not hasattr(core_model, "predict_proba"):
        return None

    probabilities = core_model.predict_proba(X)
    classes = list(core_model.classes_)

    if POSITIVE_LABEL not in classes:
        raise ValueError(
            f"El modelo no contiene la clase positiva esperada: {POSITIVE_LABEL}. "
            f"Clases encontradas: {classes}"
        )

    positive_index = classes.index(POSITIVE_LABEL)
    return [float(row[positive_index]) for row in probabilities]


def positive_probability(model: Any, X) -> float | None:
    probabilities = positive_probabilities(model, X)
    if not probabilities:
        return None
    return probabilities[0]


def build_result(
    model_name: str,
    prediction: int,
    probability: float | None,
    features: pd.DataFrame | None = None,
    text_used: str = "",
    urls_used: str = "",
) -> dict:
    model_name = normalize_model_name(model_name)

    return {
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


def predict_textual(model: Any, text: str) -> tuple[int, float | None]:
    text = safe_text(text)

    if not text:
        raise ValueError("El modelo textual requiere contenido de texto.")

    core_model, _ = unwrap_model(model)
    X = pd.Series([text])
    prediction = int(core_model.predict(X)[0])
    probability = positive_probability(core_model, X)

    return prediction, probability


def predict_url(model: Any, urls_raw: str) -> tuple[int, float | None, pd.DataFrame]:
    urls_raw = safe_text(urls_raw)

    if not urls_raw:
        raise ValueError("El modelo URL requiere al menos una URL o enlace.")

    core_model, feature_names = unwrap_model(model)

    if is_global_url_model(model):
        X = build_global_url_feature_frame(urls_raw, feature_names)
        if X.empty:
            raise ValueError("El modelo URL requiere al menos una URL o enlace válido.")

        probabilities = positive_probabilities(core_model, X)
        if not probabilities:
            prediction = int(core_model.predict(X)[0])
            return prediction, None, X.iloc[[0]].copy()

        best_index = max(range(len(probabilities)), key=lambda idx: probabilities[idx])
        probability = probabilities[best_index]
        prediction = int(probability >= 0.5)

        return prediction, probability, X.iloc[[best_index]].copy()

    X = build_feature_frame(urls_raw)
    prediction = int(core_model.predict(X)[0])
    probability = positive_probability(core_model, X)

    return prediction, probability, X


def url_probability_from_field(urls_raw: str, url_model: Any) -> tuple[float, int]:
    urls = extract_candidate_urls(urls_raw)
    if not urls:
        return 0.5, 0

    core_model, feature_names = unwrap_model(url_model)

    if is_global_url_model(url_model):
        X = build_global_url_feature_frame("\n".join(urls), feature_names)
    else:
        X = build_feature_frame("\n".join(urls))

    probabilities = positive_probabilities(core_model, X)
    if not probabilities:
        return 0.5, len(urls)

    return max(probabilities), len(urls)


def predict_hybrid(model: Any, text: str, urls_raw: str) -> tuple[int, float | None, pd.DataFrame]:
    text = safe_text(text)
    urls_raw = safe_text(urls_raw)

    if not text:
        raise ValueError("El modelo híbrido requiere contenido de texto.")

    core_model, feature_names = unwrap_model(model)

    if is_global_fusion_model(model):
        text_model = load_model("textual")
        url_model = load_model("url")

        _, text_probability = predict_textual(text_model, text)
        url_probability, url_count = url_probability_from_field(urls_raw, url_model)

        X = pd.DataFrame([{
            "text_prob": 0.5 if text_probability is None else text_probability,
            "url_prob": url_probability,
            "has_url": int(url_count > 0),
            "url_count": int(url_count),
        }]).reindex(columns=feature_names, fill_value=0).fillna(0)

        probability = positive_probability(core_model, X)
        if probability is None:
            prediction = int(core_model.predict(X)[0])
        else:
            prediction = int(probability >= 0.5)

        return prediction, probability, X

    X = build_hybrid_frame(text, urls_raw)
    prediction = int(core_model.predict(X)[0])
    probability = positive_probability(core_model, X)

    return prediction, probability, X


def analyze(
    model_name: str,
    subject: str = "",
    body: str = "",
    urls_raw: str = "",
) -> dict:
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
    return {
        "modelo": result.get("modelo_nombre"),
        "clase_predicha": result.get("clase_predicha"),
        "probabilidad_phishing": result.get("probabilidad_formato"),
        "nivel_riesgo": result.get("nivel_riesgo"),
        "mensaje_riesgo": result.get("mensaje_riesgo"),
        "feature_summary": result.get("feature_summary"),
    }
