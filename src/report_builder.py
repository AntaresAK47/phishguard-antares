from datetime import datetime
from typing import Iterable


# ============================================================
# report_builder.py
# Generación de reportes locales simples para el prototipo.
#
# Seguridad:
# - No guarda reportes automáticamente.
# - No visita enlaces.
# - Neutraliza enlaces en el texto del reporte descargable.
# ============================================================


def neutralize_links(text: str) -> str:
    """
    Neutraliza enlaces para que no queden como URLs clicables en reportes.
    """
    if text is None:
        return ""

    value = str(text)
    value = value.replace("https://", "hxxps://")
    value = value.replace("http://", "hxxp://")
    value = value.replace("www.", "www[.]")
    return value


def _line(key: str, value) -> str:
    return f"{key}: {value}"


def build_report_text(
    result: dict,
    subject: str = "",
    body: str = "",
    urls_raw: str = "",
    comparative_rows: Iterable[dict] | None = None,
) -> str:
    """
    Construye un reporte TXT descargable para evidencias o revisión.
    """
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("PHISHGUARD ANTARES - REPORTE LOCAL DE ANALISIS")
    lines.append("=" * 62)
    lines.append(_line("Fecha y hora local", created_at))
    lines.append(_line("Modelo utilizado", result.get("modelo_nombre", "No disponible")))
    lines.append(_line("Clase estimada", result.get("clase_predicha", "No disponible")))
    lines.append(_line("Probabilidad estimada de phishing", result.get("probabilidad_formato", "No disponible")))
    lines.append(_line("Nivel orientativo de riesgo", result.get("nivel_riesgo", "No disponible")))
    lines.append("")
    lines.append("MENSAJE DE RIESGO")
    lines.append("-" * 62)
    lines.append(str(result.get("mensaje_riesgo", "No disponible")))
    lines.append("")

    summary = result.get("feature_summary") or {}
    if summary:
        lines.append("SENALES TECNICAS URL/ENLACES")
        lines.append("-" * 62)
        for key, value in summary.items():
            lines.append(_line(key, value))
        lines.append("")

    if comparative_rows:
        lines.append("COMPARACION DE MODELOS")
        lines.append("-" * 62)
        for row in comparative_rows:
            risk = row.get("Riesgo", row.get("Nivel orientativo", "No disponible"))
            lines.append(
                f"{row.get('Modelo', 'Modelo')}: "
                f"{row.get('Clase estimada', 'No disponible')} | "
                f"Probabilidad: {row.get('Probabilidad phishing', 'No disponible')} | "
                f"Riesgo: {risk}"
            )
        lines.append("")

    lines.append("ENTRADA ANALIZADA - NEUTRALIZADA")
    lines.append("-" * 62)
    lines.append(_line("Asunto", neutralize_links(subject)))
    lines.append(_line("URL/enlaces", neutralize_links(urls_raw)))
    lines.append("Cuerpo:")
    lines.append(neutralize_links(body))
    lines.append("")

    lines.append("ADVERTENCIA")
    lines.append("-" * 62)
    lines.append(
        "Este reporte fue generado por un prototipo academico local. "
        "El resultado es orientativo, no sustituye herramientas profesionales de ciberseguridad "
        "y no constituye una decision definitiva de seguridad."
    )
    lines.append(
        "Las URL fueron tratadas como texto; el prototipo no visito enlaces ni consulto servicios externos."
    )

    return "\n".join(lines)
