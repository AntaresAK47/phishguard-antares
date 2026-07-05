# ============================================================
# risk_rules.py
# Reglas de presentación de resultado y nivel de riesgo.
#
# Nota metodológica:
# Los niveles de riesgo son orientativos y didácticos.
# No representan una calibración probabilística formal.
# ============================================================


def label_name(label: int) -> str:
    """
    Convierte la etiqueta numérica del modelo en texto comprensible.
    1 = phishing probable.
    0 = legítimo probable.
    """
    if int(label) == 1:
        return "Phishing probable"
    return "Legítimo probable"


def probability_percent(prob_phishing: float | None) -> str:
    """
    Formatea la probabilidad para mostrarla en interfaz.
    """
    if prob_phishing is None:
        return "No disponible"
    return f"{prob_phishing * 100:.2f}%"


def risk_profile(prob_phishing: float | None) -> dict:
    """
    Devuelve un perfil visual y narrativo del nivel de riesgo.

    Escala didáctica utilizada por el prototipo:
    - 0 % a < 5 %: Muy bajo
    - 5 % a < 15 %: Bajo
    - 15 % a < 35 %: Precaución
    - 35 % a < 50 %: Moderado
    - 50 % a < 70 %: Alto
    - 70 % a < 85 %: Muy alto
    - 85 % a 100 %: Crítico

    Esta escala ayuda al usuario común a interpretar la salida.
    No debe presentarse como calibración probabilística formal.
    """
    if prob_phishing is None:
        return {
            "level": "No disponible",
            "short": "Sin probabilidad",
            "color": "#9ca3af",
            "glow": "rgba(156, 163, 175, 0.28)",
            "icon": "?",
            "headline": "No se pudo estimar una probabilidad.",
            "message": (
                "El modelo no proporcionó una probabilidad estimada. "
                "Interprete el resultado únicamente como una clasificación orientativa."
            ),
        }

    p = max(0.0, min(1.0, float(prob_phishing)))

    if p < 0.05:
        return {
            "level": "Muy bajo",
            "short": "Riesgo muy bajo",
            "color": "#00e69a",
            "glow": "rgba(0, 230, 154, 0.32)",
            "icon": "OK",
            "headline": "No se observan señales fuertes de phishing.",
            "message": (
                "La probabilidad estimada de phishing es muy baja. "
                "Aun así, el resultado no debe interpretarse como garantía absoluta de seguridad."
            ),
        }

    if p < 0.15:
        return {
            "level": "Bajo",
            "short": "Riesgo bajo",
            "color": "#7CFF6B",
            "glow": "rgba(124, 255, 107, 0.28)",
            "icon": "OK",
            "headline": "El riesgo estimado es bajo.",
            "message": (
                "El mensaje presenta baja probabilidad estimada de phishing. "
                "Se recomienda mantener hábitos normales de verificación."
            ),
        }

    if p < 0.35:
        return {
            "level": "Precaución",
            "short": "Precaución",
            "color": "#FFD166",
            "glow": "rgba(255, 209, 102, 0.30)",
            "icon": "!",
            "headline": "Existen señales que conviene revisar.",
            "message": (
                "El mensaje no alcanza un nivel alto de riesgo, pero contiene señales que ameritan revisión. "
                "Verifique remitente, enlaces y contexto antes de actuar."
            ),
        }

    if p < 0.50:
        return {
            "level": "Moderado",
            "short": "Riesgo moderado",
            "color": "#FF9F1C",
            "glow": "rgba(255, 159, 28, 0.34)",
            "icon": "!",
            "headline": "El mensaje requiere verificación cuidadosa.",
            "message": (
                "El resultado sugiere un riesgo moderado. Antes de abrir enlaces o ingresar datos, "
                "revise cuidadosamente el origen del mensaje y sus URL asociadas."
            ),
        }

    if p < 0.70:
        return {
            "level": "Alto",
            "short": "Riesgo alto",
            "color": "#FF5C33",
            "glow": "rgba(255, 92, 51, 0.36)",
            "icon": "!!",
            "headline": "El mensaje presenta patrones compatibles con phishing.",
            "message": (
                "La probabilidad estimada supera el umbral de decisión del modelo. "
                "Se recomienda no abrir enlaces ni ingresar credenciales sin verificación externa."
            ),
        }

    if p < 0.85:
        return {
            "level": "Muy alto",
            "short": "Riesgo muy alto",
            "color": "#FF2D75",
            "glow": "rgba(255, 45, 117, 0.42)",
            "icon": "!!",
            "headline": "Alta probabilidad de phishing.",
            "message": (
                "El mensaje presenta una probabilidad elevada de contener patrones compatibles con phishing. "
                "Evite abrir enlaces, descargar archivos o ingresar información sensible."
            ),
        }

    return {
        "level": "Crítico",
        "short": "Riesgo crítico",
        "color": "#FF1744",
        "glow": "rgba(255, 23, 68, 0.48)",
        "icon": "!!!",
        "headline": "Riesgo crítico de phishing.",
        "message": (
            "El mensaje presenta señales muy fuertes compatibles con phishing. "
            "No abra enlaces, no ingrese credenciales y reporte el caso según el procedimiento institucional."
        ),
    }


def risk_level(prob_phishing: float | None) -> str:
    """
    Mantiene compatibilidad con predictor.py y devuelve solo el nombre del nivel.
    """
    return risk_profile(prob_phishing)["level"]


def risk_message(prob_phishing: float | None) -> str:
    """
    Mantiene compatibilidad con predictor.py y devuelve el mensaje explicativo.
    """
    return risk_profile(prob_phishing)["message"]


def risk_color(prob_phishing: float | None) -> str:
    """
    Devuelve el color asociado al nivel de riesgo.
    """
    return risk_profile(prob_phishing)["color"]
