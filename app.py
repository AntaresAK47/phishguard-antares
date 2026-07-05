from html import escape
from pathlib import Path
import base64
import time

import pandas as pd
import streamlit as st

from src.config import APP_NAME, APP_SUBTITLE, APP_VERSION, MODEL_DISPLAY_NAMES
from src.predictor import analyze
from src.report_builder import build_report_text
from src.risk_rules import risk_profile
from src.ui_theme import APP_CSS


# ============================================================
# app.py
# PhishGuard Antares - Interfaz visual premium final v2.0.
#
# Prototipo académico local de detección de phishing.
# - No visita URLs.
# - No consulta APIs externas.
# - No guarda entradas sensibles automáticamente.
# - Usa modelos .joblib entrenados localmente.
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent
LOGO_PATH = ROOT_DIR / "assets" / "logo.png"


@st.cache_data(show_spinner=False)
def logo_data_uri() -> str | None:
    """Devuelve el logo local como data URI para integrarlo en bloques HTML propios."""
    if not LOGO_PATH.exists():
        return None
    try:
        encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    except OSError:
        return None
    return f"data:image/png;base64,{encoded}"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(APP_CSS, unsafe_allow_html=True)


MODEL_OPTIONS = {
    "hibrido": "Modelo híbrido",
    "textual": "Modelo textual",
    "url": "Modelo URL",
}

MODEL_HELP = {
    "hibrido": "Integra contenido textual y características URL/enlaces. Es el modo principal del prototipo.",
    "textual": "Analiza únicamente asunto y cuerpo del mensaje.",
    "url": "Analiza únicamente características léxicas de URL/enlaces.",
}

MODEL_SHORT = {
    "hibrido": "Texto + URL",
    "textual": "Solo texto",
    "url": "Solo URL",
}


# ------------------------------------------------------------
# Encabezado y navegación
# ------------------------------------------------------------

def render_header():
    """Renderiza el encabezado como un único bloque HTML válido y estable."""
    logo_uri = logo_data_uri()
    if logo_uri:
        logo_html = (
            f'<img class="pg-hero-logo-img" src="{logo_uri}" '
            'alt="Logo de PhishGuard Antares" />'
        )
    else:
        logo_html = '<div class="pg-logo-fallback" aria-hidden="true">PG</div>'

    st.markdown(
        f"""
        <section class="pg-hero" aria-labelledby="pg-app-title">
            <div class="pg-hero-core">
                <div class="pg-hero-logo-shell">{logo_html}</div>
                <div class="pg-hero-copy">
                    <div class="pg-kicker">Análisis local · Aprendizaje automático</div>
                    <div id="pg-app-title" class="pg-title" role="heading" aria-level="1">
                        {escape(APP_NAME)}
                    </div>
                    <div class="pg-subtitle">{escape(APP_SUBTITLE)}</div>
                </div>
                <div class="pg-version-badge" aria-label="Versión {escape(APP_VERSION)}">
                    <span>Versión</span>
                    <strong>{escape(APP_VERSION)}</strong>
                </div>
            </div>
            <div class="pg-alert">
                <div class="pg-alert-mark" aria-hidden="true">PG</div>
                <div class="pg-alert-copy">
                    <b>Uso académico y defensivo.</b>
                    <span>Este prototipo estima si un mensaje presenta patrones compatibles con phishing mediante modelos entrenados localmente. Las URL se procesan únicamente como texto: no se abren, no se visitan y no se consultan servicios externos.</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def init_session_defaults():
    """Inicializa y preserva preferencias aunque el panel deje de renderizar widgets."""
    st.session_state.setdefault("pg_command_open", True)

    st.session_state.setdefault(
        "pg_model_choice_persisted",
        st.session_state.get("pg_model_choice", "hibrido"),
    )
    st.session_state.setdefault(
        "pg_compare_all_persisted",
        bool(st.session_state.get("pg_compare_all", False)),
    )
    st.session_state.setdefault(
        "pg_show_advanced_persisted",
        bool(st.session_state.get("pg_show_advanced_option", False)),
    )

    # Streamlit elimina del estado las claves de widgets que dejan de renderizarse.
    # Se restauran desde claves duraderas cuando el centro de mando vuelve a abrirse.
    st.session_state.setdefault(
        "pg_model_choice",
        st.session_state["pg_model_choice_persisted"],
    )
    st.session_state.setdefault(
        "pg_compare_all",
        st.session_state["pg_compare_all_persisted"],
    )
    st.session_state.setdefault(
        "pg_show_advanced_option",
        st.session_state["pg_show_advanced_persisted"],
    )


def set_command_center_open(is_open: bool) -> None:
    """Actualiza el estado del centro de mando en el mismo rerun del widget."""
    st.session_state["pg_command_open"] = bool(is_open)


def render_status_bar():
    """Muestra el estado operativo del prototipo sin ocupar la barra nativa."""
    st.markdown(
        """
        <div class="pg-status-bar" role="status" aria-label="Estado del prototipo">
            <span class="pg-status-dot" aria-hidden="true"></span>
            <span>Modelos locales activos</span>
            <span class="pg-status-separator" aria-hidden="true">•</span>
            <span>Sin conexión externa</span>
            <span class="pg-status-separator" aria-hidden="true">•</span>
            <span>Análisis defensivo</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_command_center():
    """
    Renderiza el centro de mando dentro del layout principal.

    Se conserva el selector cerrado basado en expander + radio: no admite
    escritura libre, búsqueda ni valores ajenos a los tres modelos disponibles.
    """
    st.markdown(
        '<div class="pg-command-anchor pg-command-state-open" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    st.button(
        "‹",
        key="pg_close_command_center",
        help="Ocultar centro de mando",
        width="content",
        on_click=set_command_center_open,
        args=(False,),
    )

    logo_uri = logo_data_uri()
    if logo_uri:
        logo_html = f'<img class="pg-command-logo-img" src="{logo_uri}" alt="Logo de PhishGuard Antares" />'
    else:
        logo_html = '<div class="pg-command-logo-fallback" aria-hidden="true">PG</div>'

    st.markdown(
        f"""
        <section class="pg-command-head-premium">
            <div class="pg-command-logo-orbit">{logo_html}</div>
            <div class="pg-command-kicker">
                <span class="pg-command-pulse" aria-hidden="true"></span>
                Centro de mando
            </div>
            <div class="pg-command-title">Configuración</div>
            <div class="pg-command-subtitle">Seleccione el modo de análisis y ajuste la lectura del dictamen.</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pg-command-divider"></div>', unsafe_allow_html=True)

    current_model = st.session_state.get("pg_model_choice", "hibrido")
    if current_model not in MODEL_OPTIONS:
        current_model = "hibrido"
        st.session_state["pg_model_choice"] = current_model

    st.markdown('<div class="pg-sidebar-field-label">Modelo a utilizar</div>', unsafe_allow_html=True)
    with st.expander(f"{MODEL_OPTIONS[current_model]} · {MODEL_SHORT[current_model]}", expanded=False):
        st.radio(
            "Seleccione un modelo",
            options=["hibrido", "textual", "url"],
            format_func=lambda x: MODEL_OPTIONS[x],
            key="pg_model_choice",
            label_visibility="collapsed",
        )

    model_choice = st.session_state.get("pg_model_choice", "hibrido")

    st.markdown(
        f"""
        <section class="pg-active-model-card">
            <div class="pg-active-model-header">
                <div class="pg-active-model-topline">Modo activo</div>
                <div class="pg-active-model-local">Local</div>
            </div>
            <div class="pg-active-model-name">{escape(MODEL_OPTIONS[model_choice])}</div>
            <div class="pg-active-model-short">{escape(MODEL_SHORT[model_choice])}</div>
            <p>{escape(MODEL_HELP[model_choice])}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pg-command-section-title">Opciones de lectura</div>', unsafe_allow_html=True)
    compare_all = st.checkbox(
        "Comparar los tres modelos",
        key="pg_compare_all",
        help="Ejecuta textual, URL e híbrido cuando las entradas lo permiten.",
    )
    show_advanced = st.checkbox(
        "Abrir análisis avanzado al finalizar",
        key="pg_show_advanced_option",
        help="La ventana de resultado siempre trae un apartado avanzado; esta opción lo abre automáticamente.",
    )

    st.session_state["pg_model_choice_persisted"] = model_choice
    st.session_state["pg_compare_all_persisted"] = bool(compare_all)
    st.session_state["pg_show_advanced_persisted"] = bool(show_advanced)

    st.markdown('<div class="pg-command-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="pg-command-section-title pg-command-section-title-centered">Escala visual</div>
        <div class="pg-scale-mini pg-scale-mini-command" aria-label="Escala de riesgo de menor a mayor">
            <span style="background:#00e69a"></span>
            <span style="background:#ffd166"></span>
            <span style="background:#ff9f1c"></span>
            <span style="background:#ff2d75"></span>
            <span style="background:#ff1744"></span>
        </div>
        <p class="pg-sidebar-note">De verde a rojo: menor a mayor probabilidad estimada de phishing.</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pg-command-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="pg-command-footnote">
            Resultado orientativo. No sustituye herramientas profesionales de ciberseguridad.
        </div>
        """,
        unsafe_allow_html=True,
    )

    return model_choice, compare_all, show_advanced


def render_command_rail():
    """Renderiza una pestaña lateral compacta para reabrir el centro de mando."""
    st.markdown(
        '<div class="pg-command-anchor pg-command-state-closed pg-rail-anchor" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    logo_uri = logo_data_uri()
    if logo_uri:
        logo_html = f'<img class="pg-rail-logo-img" src="{logo_uri}" alt="" />'
    else:
        logo_html = '<div class="pg-rail-logo-fallback">PG</div>'

    st.markdown(
        f"""
        <div class="pg-rail-brand" aria-hidden="true">
            <div class="pg-rail-logo-shell">{logo_html}</div>
            <div class="pg-rail-label">MENÚ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button(
        "›",
        key="pg_open_command_center",
        help="Abrir centro de mando",
        width="content",
        on_click=set_command_center_open,
        args=(True,),
    )


def render_workspace(model_choice: str, compare_all: bool, show_advanced: bool):
    """Renderiza el área principal del prototipo."""
    render_status_bar()
    render_header()
    subject, body, urls_raw = render_input_area()

    st.markdown("---")
    analyze_button = st.button("Analizar", type="primary", width="stretch")

    if analyze_button:
        if compare_all:
            run_comparative_analysis(subject, body, urls_raw, show_advanced)
        else:
            run_single_analysis(model_choice, subject, body, urls_raw, show_advanced)

    render_persisted_result()
    maybe_open_result_dialog()

    st.markdown("---")
    st.caption(
        "PhishGuard Antares es un prototipo académico local. No visita enlaces, "
        "no guarda entradas sensibles y no reemplaza herramientas profesionales de ciberseguridad."
    )


# ------------------------------------------------------------
# Entradas
# ------------------------------------------------------------

def render_input_area():
    st.markdown('<div class="pg-section-title">Analizador de mensaje y enlaces</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="pg-section-note">Pegue el mensaje sospechoso o la URL. El análisis se ejecuta localmente y no abre enlaces.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        subject = st.text_input(
            "Asunto del mensaje",
            placeholder="Ejemplo: Verificación urgente de cuenta",
        )

        body = st.text_area(
            "Cuerpo del mensaje",
            height=230,
            placeholder="Pegue aquí el contenido del correo o mensaje sospechoso.",
        )

    with right:
        urls_raw = st.text_area(
            "URL o enlaces asociados",
            height=160,
            placeholder="Pegue aquí URL, enlaces mailto, cid u otros enlaces detectados.",
        )

        with st.expander("Ejemplos de prueba sugeridos"):
            st.markdown(
                """
                **Ejemplo sospechoso**
                - Asunto: `Verificación urgente`
                - Cuerpo: `Debe actualizar su cuenta para evitar suspensión del servicio.`
                - URL: `https://secure-login.example.com/verify?token=123`

                **Ejemplo con enlaces no web**
                - URL/enlaces: `mailto:soporte@banco.com, cid:image001.jpg, https://login-banco.example.com/actualizar`
                """
            )

    return subject, body, urls_raw


def validate_inputs(model_choice: str, subject: str, body: str, urls_raw: str):
    text = f"{subject}\n{body}".strip()
    urls = urls_raw.strip()

    if model_choice in ["textual", "hibrido"] and not text:
        st.error("Debe ingresar asunto o cuerpo del mensaje para usar el modelo textual o híbrido.")
        st.stop()

    if model_choice == "url" and not urls and not text:
        st.error("Debe ingresar al menos una URL/enlace o texto que contenga enlaces.")
        st.stop()


# ------------------------------------------------------------
# Animación de análisis fluida
# ------------------------------------------------------------

def current_stage(percent: int) -> tuple[str, list[str]]:
    stage_defs = [
        (0, "Validando entrada del usuario"),
        (15, "Normalizando texto y enlaces"),
        (30, "Extrayendo características URL/enlaces"),
        (45, "Preparando vector técnico"),
        (60, "Cargando modelo entrenado local"),
        (75, "Estimando probabilidad de phishing"),
        (90, "Organizando resultado para el usuario"),
        (100, "Análisis completado"),
    ]

    active = stage_defs[0][1]
    completed = []

    for threshold, label in stage_defs:
        if percent >= threshold:
            active = label
            if threshold < 100:
                completed.append(label)

    return active, completed


def run_loading_animation():
    """
    Muestra una animación circular flotante y fluida de 0 % a 100 %.

    Duración visual aproximada: 4,9 segundos. No representa conexión externa
    ni consulta remota; es retroalimentación visual del procesamiento local:
    validación, extracción de señales, carga del modelo y organización del dictamen.
    """
    loader = st.empty()

    for percent in range(0, 101):
        message, completed = current_stage(percent)
        items = "".join(f"<li>{escape(step)}</li>" for step in completed)

        loader.markdown(
            f"""
            <div class="pg-loader-overlay">
                <section class="pg-loader-card pg-loader-floating">
                    <div class="pg-loader-grid">
                        <div class="pg-ring-shell">
                            <div class="pg-ring" style="background: conic-gradient(#ff2d75 0% {percent}%, rgba(255,255,255,0.08) {percent}% 100%);">
                                <div class="pg-ring-inner">
                                    <div class="pg-ring-number">{percent}%</div>
                                    <div class="pg-ring-label">análisis IA</div>
                                </div>
                            </div>
                        </div>
                        <div class="pg-loader-copy">
                            <div class="pg-analysis-title">Análisis en curso</div>
                            <div class="pg-loader-status">{escape(message)}</div>
                            <ul class="pg-step-list">{items}</ul>
                            <div class="pg-loader-note">Procesamiento local · Sin abrir enlaces · Sin APIs externas</div>
                        </div>
                    </div>
                </section>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.045)

    loader.markdown(
        """
        <div class="pg-loader-overlay">
            <section class="pg-loader-card pg-loader-floating pg-loader-card-done">
                <div class="pg-analysis-done">Análisis completado. Preparando ventana de resultado...</div>
            </section>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(0.45)
    loader.empty()

# ------------------------------------------------------------
# Resultados: lectura simple y avanzada
# ------------------------------------------------------------

def probability_value(result: dict) -> float:
    prob = result.get("probabilidad_phishing")
    if prob is None:
        return 0.0
    return max(0.0, min(1.0, float(prob)))


def render_probability_meter(result: dict):
    prob = probability_value(result)
    percent = prob * 100

    st.markdown(
        f"""
        <div class="pg-meter-label-row">
            <span>0 %</span>
            <span>25 %</span>
            <span>50 %</span>
            <span>75 %</span>
            <span>100 %</span>
        </div>
        <div class="pg-meter-wrap">
            <div class="pg-meter-fill" style="width:{percent:.2f}%;"></div>
            <div class="pg-meter-pin" style="left:calc({percent:.2f}% - 8px);"></div>
        </div>
        <div class="pg-small" style="margin-top:0.45rem;">
            Escala visual orientativa: de menor a mayor probabilidad estimada de phishing.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result: dict):
    prob = probability_value(result)
    profile = risk_profile(prob)
    color = profile["color"]
    glow = profile["glow"]

    verdict = escape(str(result.get("clase_predicha", "No disponible")))
    prob_text = escape(str(result.get("probabilidad_formato", "No disponible")))
    risk = escape(str(profile["level"]))
    headline = escape(str(profile["headline"]))
    message = escape(str(profile["message"]))
    model_name = escape(str(result.get("modelo_nombre", "Modelo")))

    st.markdown(
        f"""
        <section class="pg-verdict-card" style="border-color:{color}; box-shadow:0 0 48px {glow};">
            <div class="pg-verdict-grid">
                <div>
                    <div class="pg-verdict-label">Dictamen principal · {model_name}</div>
                    <div class="pg-verdict-main" style="color:{color};">{verdict}</div>
                    <div class="pg-simple-advice"><b>{headline}</b></div>
                    <div class="pg-simple-advice">{message}</div>
                </div>
                <div class="pg-prob-panel" style="border-color:{color};">
                    <div class="pg-prob-number" style="color:{color};">{prob_text}</div>
                    <div class="pg-prob-caption">probabilidad estimada de phishing</div>
                    <div class="pg-risk-chip" style="background:{color};">{risk}</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    render_probability_meter(result)


def render_signal_pills(result: dict):
    summary = result.get("feature_summary") or {}
    if not summary:
        st.markdown('<span class="pg-pill">Sin señales URL para este modelo</span>', unsafe_allow_html=True)
        return

    important_keys = [
        "URL web detectadas",
        "Enlaces totales detectados",
        "Enlaces mailto",
        "Referencias cid",
        "Subdominios máximos",
        "Usa HTTPS",
        "Acortador detectado",
        "Palabras sospechosas en URL",
    ]

    pills = []
    for key in important_keys:
        if key in summary:
            pills.append(
                f'<span class="pg-pill">{escape(key)}: <b>{escape(str(summary[key]))}</b></span>'
            )

    st.markdown("".join(pills), unsafe_allow_html=True)


def render_advanced(result: dict, subject: str, body: str, urls_raw: str, expanded: bool = False):
    with st.expander("Ver análisis avanzado", expanded=expanded):
        st.markdown("#### Señales técnicas resumidas")
        summary = result.get("feature_summary") or {}
        if summary:
            summary_df = pd.DataFrame(
                [{"Señal técnica": key, "Valor": str(value)} for key, value in summary.items()]
            )
            st.dataframe(summary_df, width="stretch", hide_index=True)
        else:
            st.info("Este modelo no generó señales URL/enlaces.")

        features = result.get("features")
        if features is not None:
            st.markdown("#### Vector técnico usado por el modelo")
            st.dataframe(features, width="stretch", hide_index=True)

        report_text = build_report_text(result, subject=subject, body=body, urls_raw=urls_raw)
        st.download_button(
            "Descargar reporte local TXT",
            data=report_text,
            file_name="reporte_phishguard_antares.txt",
            mime="text/plain",
            width="stretch",
        )


def render_single_result_content(result: dict, subject: str, body: str, urls_raw: str, show_advanced: bool):
    st.markdown('<div class="pg-result-window-label">Ventana de resultado</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-section-title pg-section-title-result">Resultado para el usuario</div>', unsafe_allow_html=True)
    render_result_card(result)
    render_context_quality_note(subject, body, urls_raw)

    st.markdown("### Señales principales")
    render_signal_pills(result)
    render_advanced(result, subject, body, urls_raw, expanded=show_advanced)


def render_comparative_content(results: list[dict], main_result: dict, subject: str, body: str, urls_raw: str, show_advanced: bool):
    st.markdown('<div class="pg-result-window-label">Ventana de resultado</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-section-title pg-section-title-result">Comparación de modelos</div>', unsafe_allow_html=True)

    if results:
        cols = st.columns(len(results))
        for col, result in zip(cols, results):
            with col:
                render_model_mini_card(result)

    st.markdown("### Lectura principal")
    render_result_card(main_result)
    render_context_quality_note(subject, body, urls_raw)
    st.markdown("### Señales principales")
    render_signal_pills(main_result)

    with st.expander("Ver análisis avanzado por modelo", expanded=show_advanced):
        rows = []
        for result in results:
            rows.append(
                {
                    "Modelo": result["modelo_nombre"],
                    "Clase estimada": result["clase_predicha"],
                    "Probabilidad phishing": result["probabilidad_formato"],
                    "Riesgo": risk_profile(result.get("probabilidad_phishing"))["level"],
                }
            )

        st.markdown("#### Resumen comparativo")
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

        for result in results:
            st.markdown(f"#### {result['modelo_nombre']}")
            summary = result.get("feature_summary") or {}
            if summary:
                summary_df = pd.DataFrame(
                    [{"Señal técnica": key, "Valor": str(value)} for key, value in summary.items()]
                )
                st.dataframe(summary_df, width="stretch", hide_index=True)

            features = result.get("features")
            if features is not None:
                st.dataframe(features, width="stretch", hide_index=True)

        report_text = build_report_text(
            main_result,
            subject=subject,
            body=body,
            urls_raw=urls_raw,
            comparative_rows=rows,
        )
        st.download_button(
            "Descargar reporte comparativo TXT",
            data=report_text,
            file_name="reporte_comparativo_phishguard_antares.txt",
            mime="text/plain",
            width="stretch",
        )


def open_dialog(title: str, render_function):
    """
    Abre una ventana modal si la versión de Streamlit lo permite.
    Si no está disponible, renderiza el contenido en la página.
    """
    if hasattr(st, "dialog"):
        try:
            dialog_decorator = st.dialog(title, width="large")
        except TypeError:
            dialog_decorator = st.dialog(title)

        @dialog_decorator
        def _dialog():
            render_function()

        _dialog()
    else:
        render_function()


def render_model_mini_card(result: dict):
    profile = risk_profile(result.get("probabilidad_phishing"))
    color = profile["color"]
    model_name = escape(str(result.get("modelo_nombre", "Modelo")))
    predicted = escape(str(result.get("clase_predicha", "No disponible")))
    prob = escape(str(result.get("probabilidad_formato", "No disponible")))
    risk = escape(str(profile["level"]))

    st.markdown(
        f"""
        <div class="pg-mini-model" style="border-color:{color};">
            <div class="pg-mini-model-name">{model_name}</div>
            <div class="pg-mini-model-result" style="color:{color};">{predicted}</div>
            <div class="pg-mini-model-prob">{prob}</div>
            <span class="pg-mini-risk" style="background:{color};">{risk}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# Persistencia de resultado y notas de contexto
# ------------------------------------------------------------

def build_context_quality(subject: str, body: str, urls_raw: str) -> dict:
    text = f"{subject}\n{body}".strip()
    urls = urls_raw.strip()

    has_text = len(text) >= 35
    has_url = bool(urls)

    if has_text and has_url:
        return {
            "level": "Contexto completo",
            "message": "El análisis utilizó contenido textual y enlaces, por lo que la lectura es más informativa para el modo híbrido.",
            "show": False,
        }

    if has_url and not has_text:
        return {
            "level": "Contexto limitado",
            "message": "Se analizó principalmente una URL aislada. El prototipo no consulta reputación ni sabe si un dominio es popular o legítimo; evalúa patrones léxicos y estructurales. Para una lectura más sólida, agregue el asunto y cuerpo del mensaje.",
            "show": True,
        }

    if has_text and not has_url:
        return {
            "level": "Sin enlaces explícitos",
            "message": "Se analizó principalmente contenido textual. Si el mensaje incluye enlaces, conviene pegarlos en el campo de URL para activar las señales léxicas de enlaces.",
            "show": True,
        }

    return {
        "level": "Entrada mínima",
        "message": "La entrada contiene poca información. El resultado debe interpretarse con cautela.",
        "show": True,
    }


def render_context_quality_note(subject: str, body: str, urls_raw: str):
    note = build_context_quality(subject, body, urls_raw)
    if note.get("show"):
        html = (
            '<div class="pg-context-note">'
            f'<b>{escape(note["level"])}.</b> {escape(note["message"])}'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)


def store_single_result(result: dict, subject: str, body: str, urls_raw: str, show_advanced: bool):
    st.session_state["pg_result_mode"] = "single"
    st.session_state["pg_result"] = result
    st.session_state["pg_subject"] = subject
    st.session_state["pg_body"] = body
    st.session_state["pg_urls_raw"] = urls_raw
    st.session_state["pg_show_advanced"] = show_advanced
    st.session_state["pg_open_result_window"] = True


def store_comparative_result(results: list[dict], main_result: dict, subject: str, body: str, urls_raw: str, show_advanced: bool):
    st.session_state["pg_result_mode"] = "comparative"
    st.session_state["pg_results"] = results
    st.session_state["pg_main_result"] = main_result
    st.session_state["pg_subject"] = subject
    st.session_state["pg_body"] = body
    st.session_state["pg_urls_raw"] = urls_raw
    st.session_state["pg_show_advanced"] = show_advanced
    st.session_state["pg_open_result_window"] = True


def has_persisted_result() -> bool:
    return st.session_state.get("pg_result_mode") in {"single", "comparative"}


def compact_preview_data() -> dict | None:
    """Prepara una lectura compacta del resultado guardado en la sesión."""
    mode = st.session_state.get("pg_result_mode")

    if mode == "single":
        result = st.session_state.get("pg_result")
        if not result:
            return None
        profile = risk_profile(result.get("probabilidad_phishing"))
        return {
            "mode_label": "Último análisis",
            "title": result.get("clase_predicha", "Resultado disponible"),
            "model": result.get("modelo_nombre", "Modelo"),
            "probability": result.get("probabilidad_formato", "No disponible"),
            "risk": profile.get("level", "No disponible"),
            "color": profile.get("color", "#ff2d75"),
            "message": "El resultado permanece guardado en esta sesión. Puede abrir la ventana nuevamente sin repetir el análisis.",
        }

    if mode == "comparative":
        main_result = st.session_state.get("pg_main_result")
        results = st.session_state.get("pg_results", [])
        if not main_result:
            return None
        profile = risk_profile(main_result.get("probabilidad_phishing"))
        return {
            "mode_label": "Última comparación",
            "title": main_result.get("clase_predicha", "Resultado disponible"),
            "model": f"{len(results)} modelos evaluados · principal: {main_result.get('modelo_nombre', 'Modelo')}",
            "probability": main_result.get("probabilidad_formato", "No disponible"),
            "risk": profile.get("level", "No disponible"),
            "color": profile.get("color", "#ff2d75"),
            "message": "La comparación permanece guardada en esta sesión. Puede abrir la ventana nuevamente sin repetir el análisis.",
        }

    return None


def clear_persisted_result():
    """Limpia el último resultado sin modificar modelos ni entradas del usuario."""
    for key in [
        "pg_result_mode",
        "pg_result",
        "pg_results",
        "pg_main_result",
        "pg_subject",
        "pg_body",
        "pg_urls_raw",
        "pg_show_advanced",
        "pg_open_result_window",
    ]:
        st.session_state.pop(key, None)


def render_persisted_result():
    """
    Muestra solo una tarjeta compacta del último análisis.

    No se renderiza el dictamen completo detrás de la ventana modal; así se
    evita duplicación visual y se mantiene la persistencia del resultado.
    """
    if not has_persisted_result():
        return

    data = compact_preview_data()
    if not data:
        return

    color = escape(str(data["color"]))
    st.markdown("---")
    st.markdown(
        f"""
        <section class="pg-result-preview" style="border-color:{color};">
            <div class="pg-preview-kicker">{escape(str(data["mode_label"]))}</div>
            <div class="pg-preview-title" style="color:{color};">{escape(str(data["title"]))}</div>
            <div class="pg-preview-meta">{escape(str(data["model"]))} · {escape(str(data["probability"]))} · riesgo {escape(str(data["risk"]))}</div>
            <div class="pg-preview-note">{escape(str(data["message"]))}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([0.42, 0.29, 0.29])
    with middle:
        if st.button("Abrir ventana de resultado", width="stretch", key="pg_reopen_result_button"):
            st.session_state["pg_open_result_window"] = True
    with right:
        if st.button("Limpiar último resultado", width="stretch", key="pg_clear_result_button"):
            clear_persisted_result()
            st.rerun()

def maybe_open_result_dialog():
    if not st.session_state.get("pg_open_result_window"):
        return

    mode = st.session_state.get("pg_result_mode")
    subject = st.session_state.get("pg_subject", "")
    body = st.session_state.get("pg_body", "")
    urls_raw = st.session_state.get("pg_urls_raw", "")
    show_advanced = st.session_state.get("pg_show_advanced", False)

    st.session_state["pg_open_result_window"] = False

    if mode == "single" and st.session_state.get("pg_result"):
        result = st.session_state["pg_result"]
        open_dialog(
            "Resultado del análisis",
            lambda: render_single_result_content(result, subject, body, urls_raw, show_advanced),
        )

    if mode == "comparative" and st.session_state.get("pg_results") and st.session_state.get("pg_main_result"):
        results = st.session_state["pg_results"]
        main_result = st.session_state["pg_main_result"]
        open_dialog(
            "Resultado comparativo",
            lambda: render_comparative_content(results, main_result, subject, body, urls_raw, show_advanced),
        )

# ------------------------------------------------------------
# Ejecución de análisis
# ------------------------------------------------------------

def run_single_analysis(model_choice: str, subject: str, body: str, urls_raw: str, show_advanced: bool):
    validate_inputs(model_choice, subject, body, urls_raw)
    run_loading_animation()

    try:
        result = analyze(model_name=model_choice, subject=subject, body=body, urls_raw=urls_raw)
    except Exception as exc:
        st.error(f"No se pudo realizar el análisis: {exc}")
        st.stop()

    store_single_result(result, subject, body, urls_raw, show_advanced)

    return result


def run_comparative_analysis(subject: str, body: str, urls_raw: str, show_advanced: bool):
    validate_inputs("hibrido", subject, body, urls_raw)
    run_loading_animation()

    results = []
    error_rows = []

    for model_name in ["textual", "url", "hibrido"]:
        try:
            result = analyze(model_name=model_name, subject=subject, body=body, urls_raw=urls_raw)
            results.append(result)
        except Exception as exc:
            error_rows.append(
                {
                    "Modelo": MODEL_DISPLAY_NAMES.get(model_name, model_name),
                    "Observación": str(exc),
                }
            )

    if error_rows:
        st.warning("Algunos modelos no pudieron ejecutarse con la entrada proporcionada.")
        st.dataframe(pd.DataFrame(error_rows), width="stretch", hide_index=True)

    if results:
        main_result = next((r for r in results if r.get("modelo") == "hibrido"), results[0])
        store_comparative_result(results, main_result, subject, body, urls_raw, show_advanced)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    init_session_defaults()

    command_col, content_col = st.columns([0.245, 0.755], gap="large")
    command_open = bool(st.session_state.get("pg_command_open", True))

    with command_col:
        if command_open:
            model_choice, compare_all, show_advanced = render_command_center()
        else:
            render_command_rail()
            model_choice = st.session_state.get("pg_model_choice_persisted", "hibrido")
            compare_all = bool(st.session_state.get("pg_compare_all_persisted", False))
            show_advanced = bool(st.session_state.get("pg_show_advanced_persisted", False))

    with content_col:
        render_workspace(model_choice, compare_all, show_advanced)


if __name__ == "__main__":
    main()
