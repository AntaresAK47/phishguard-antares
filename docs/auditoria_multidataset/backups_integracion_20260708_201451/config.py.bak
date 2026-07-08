from pathlib import Path


# ============================================================
# config.py
# Configuración central del prototipo académico PhishGuard Antares.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
LOGS_DIR = OUTPUTS_DIR / "logs"

MODEL_PATHS = {
    "textual": MODELS_DIR / "modelo_textual.joblib",
    "url": MODELS_DIR / "modelo_url.joblib",
    "hibrido": MODELS_DIR / "modelo_hibrido.joblib",
}

MODEL_DISPLAY_NAMES = {
    "textual": "Modelo textual",
    "url": "Modelo URL",
    "hibrido": "Modelo híbrido",
}

POSITIVE_LABEL = 1
NEGATIVE_LABEL = 0

LABEL_NAMES = {
    0: "Legítimo probable",
    1: "Phishing probable",
}

RISK_THRESHOLDS = {
    "alto": 0.85,
    "medio": 0.60,
}

APP_NAME = "PhishGuard Antares"
APP_SUBTITLE = "Prototipo académico de detección de phishing"
APP_VERSION = "2.0"


def validate_model_files() -> dict:
    """
    Verifica si los archivos de modelos existen en la carpeta models.
    Retorna un diccionario con True/False por cada modelo.
    """
    return {
        model_name: model_path.exists()
        for model_name, model_path in MODEL_PATHS.items()
    }
