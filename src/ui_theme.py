# ============================================================
# ui_theme.py
# Tema visual consolidado de PhishGuard Antares.
# Paleta: negro profundo, vino, carmesí, fucsia y morado neón.
# ============================================================

APP_CSS = """
<style>
:root {
    --pg-bg: #050309;
    --pg-bg-2: #0b0610;
    --pg-surface: rgba(16, 9, 23, 0.94);
    --pg-surface-2: rgba(35, 13, 39, 0.84);
    --pg-surface-soft: rgba(255, 255, 255, 0.052);
    --pg-border: rgba(255, 236, 248, 0.115);
    --pg-border-hot: rgba(255, 45, 117, 0.62);
    --pg-text: #fff7fc;
    --pg-muted: #d4c3df;
    --pg-dim: #9c88ab;
    --pg-crimson: #ff2d75;
    --pg-crimson-deep: #b7124e;
    --pg-fuchsia: #bd24ff;
    --pg-red: #ff1744;
    --pg-orange: #ff7a1a;
    --pg-green: #00e69a;
    --pg-shadow: 0 24px 80px rgba(0, 0, 0, 0.46);
    --pg-command-width: clamp(276px, 23vw, 308px);
    --pg-rail-width: 56px;
}

*, *::before, *::after {
    box-sizing: border-box;
}

html,
body,
[data-testid="stAppViewContainer"],
.stApp {
    font-family: Inter, Manrope, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--pg-text) !important;
    background:
        radial-gradient(circle at 12% 10%, rgba(189, 36, 255, 0.22), transparent 31%),
        radial-gradient(circle at 89% 8%, rgba(255, 45, 117, 0.24), transparent 29%),
        radial-gradient(circle at 66% 74%, rgba(255, 23, 68, 0.10), transparent 35%),
        linear-gradient(135deg, #050309 0%, #0b0610 38%, #16061c 67%, #07040b 100%) !important;
}

[data-testid="stAppViewContainer"] {
    background-attachment: fixed !important;
}

[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
}

#MainMenu,
footer,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stDeployButton"],
[data-testid="stToolbar"],
.stDeployButton,
button[title="Deploy"],
a[title="Deploy"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

.material-symbols-rounded,
.material-symbols-outlined,
[class*="material-symbols"],
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
}

.block-container,
[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: 1480px !important;
    padding: 1.55rem clamp(1rem, 4.2vw, 3.5rem) 2.75rem !important;
}

/* ------------------------------------------------------------
   Controles generales de Streamlit
   ------------------------------------------------------------ */

.stButton > button,
.stDownloadButton > button {
    min-height: 3.1rem !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 17px !important;
    background: linear-gradient(92deg, #ff1744 0%, #ff2d75 48%, #bd24ff 100%) !important;
    color: #ffffff !important;
    font-weight: 860 !important;
    letter-spacing: 0.015em !important;
    box-shadow: 0 0 30px rgba(255, 45, 117, 0.26) !important;
    transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease, filter 180ms ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 0 42px rgba(255, 45, 117, 0.42) !important;
    filter: saturate(1.06) brightness(1.04) !important;
}

.stButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 2px solid rgba(255, 151, 196, 0.95) !important;
    outline-offset: 3px !important;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stCheckbox label,
.stRadio label {
    color: #f8effc !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div {
    border: 1px solid rgba(255, 255, 255, 0.13) !important;
    border-radius: 17px !important;
    background:
        linear-gradient(145deg, rgba(255, 255, 255, 0.074), rgba(255, 255, 255, 0.043)),
        radial-gradient(circle at 14% 0%, rgba(255, 45, 117, 0.08), transparent 36%) !important;
    color: #fff8fd !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.045), 0 14px 36px rgba(0, 0, 0, 0.16) !important;
    transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease !important;
}

.stTextInput input:hover,
.stTextArea textarea:hover,
div[data-baseweb="select"] > div:hover {
    border-color: rgba(255, 45, 117, 0.38) !important;
    box-shadow: 0 0 0 1px rgba(255, 45, 117, 0.08), 0 0 28px rgba(255, 45, 117, 0.10) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(255, 45, 117, 0.86) !important;
    box-shadow: 0 0 0 1px rgba(255, 45, 117, 0.34), 0 0 32px rgba(255, 45, 117, 0.16) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(249, 243, 255, 0.50) !important;
}

.stTextArea textarea {
    line-height: 1.55 !important;
    resize: vertical !important;
}

[data-testid="stDataFrame"] {
    overflow: hidden !important;
    border: 1px solid rgba(255, 255, 255, 0.095) !important;
    border-radius: 16px !important;
    background: rgba(4, 3, 8, 0.62) !important;
}

hr {
    border-color: rgba(255, 255, 255, 0.095) !important;
    margin: 2rem 0 !important;
}

[data-testid="stMetricValue"] {
    font-weight: 900 !important;
}

/* ------------------------------------------------------------
   Barra operativa y encabezado principal
   ------------------------------------------------------------ */

.pg-status-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.66rem;
    min-height: 2.62rem;
    margin-bottom: 1.05rem;
    padding: 0.55rem 1rem;
    border: 1px solid rgba(255, 45, 117, 0.23);
    border-radius: 999px;
    background:
        linear-gradient(135deg, rgba(255, 45, 117, 0.10), rgba(189, 36, 255, 0.07)),
        rgba(10, 6, 16, 0.70);
    color: #ecdef5;
    font-size: 0.82rem;
    font-weight: 790;
    letter-spacing: 0.02em;
    box-shadow: 0 0 28px rgba(255, 45, 117, 0.10), inset 0 0 0 1px rgba(255, 255, 255, 0.025);
    animation: pgFadeRise 320ms ease both;
}

.pg-status-dot {
    width: 0.47rem;
    height: 0.47rem;
    flex: 0 0 auto;
    border-radius: 999px;
    background: var(--pg-green);
    box-shadow: 0 0 14px rgba(0, 230, 154, 0.86);
}

.pg-status-separator {
    color: rgba(255, 255, 255, 0.36);
}

.pg-hero {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    margin-bottom: 1.7rem;
    padding: 1.35rem 1.4rem 1.25rem;
    border: 1px solid rgba(255, 45, 117, 0.26);
    border-radius: 27px;
    background:
        radial-gradient(circle at 8% 6%, rgba(255, 45, 117, 0.20), transparent 35%),
        radial-gradient(circle at 96% 0%, rgba(189, 36, 255, 0.17), transparent 34%),
        linear-gradient(135deg, rgba(18, 8, 25, 0.96), rgba(34, 9, 34, 0.76));
    box-shadow: 0 0 58px rgba(255, 45, 117, 0.12), 0 22px 70px rgba(0, 0, 0, 0.30);
    animation: pgFadeRise 360ms ease both;
}

.pg-hero::after {
    content: "";
    position: absolute;
    z-index: -1;
    inset: 0;
    background: linear-gradient(110deg, transparent 0%, rgba(255, 255, 255, 0.025) 42%, transparent 68%);
    pointer-events: none;
}

.pg-hero-core {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 1rem;
    align-items: center;
}

.pg-hero-logo-shell {
    width: 76px;
    height: 76px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 45, 117, 0.34);
    border-radius: 21px;
    background:
        radial-gradient(circle at 34% 18%, rgba(255, 255, 255, 0.12), transparent 20%),
        rgba(6, 4, 11, 0.80);
    box-shadow: inset 0 0 18px rgba(255, 255, 255, 0.025), 0 0 28px rgba(255, 45, 117, 0.20);
}

.pg-hero-logo-img {
    display: block;
    width: 62px;
    height: 62px;
    object-fit: contain;
    border-radius: 16px;
    filter: drop-shadow(0 0 12px rgba(255, 45, 117, 0.44));
}

.pg-logo-fallback {
    width: 62px;
    height: 62px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 17px;
    color: #ffffff;
    font-weight: 900;
    background: linear-gradient(135deg, #ff1744, #ff2d75 58%, #bd24ff);
    box-shadow: 0 0 26px rgba(255, 45, 117, 0.38);
}

.pg-hero-copy {
    min-width: 0;
}

.pg-kicker {
    margin-bottom: 0.34rem;
    color: #ff8eb8;
    font-size: 0.73rem;
    font-weight: 880;
    letter-spacing: 0.17em;
    text-transform: uppercase;
}

.pg-title {
    margin: 0;
    color: var(--pg-text);
    font-size: clamp(2.25rem, 4.15vw, 3.65rem);
    font-weight: 930;
    letter-spacing: 0;
    line-height: 0.98;
    text-shadow: 0 0 24px rgba(255, 45, 117, 0.14);
}

.pg-subtitle {
    margin-top: 0.52rem;
    color: var(--pg-muted);
    font-size: clamp(1rem, 1.45vw, 1.16rem);
    line-height: 1.45;
}

.pg-version-badge {
    min-width: 74px;
    padding: 0.62rem 0.72rem;
    border: 1px solid rgba(255, 45, 117, 0.30);
    border-radius: 16px;
    background: rgba(8, 5, 13, 0.57);
    text-align: center;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.025);
}

.pg-version-badge span,
.pg-version-badge strong {
    display: block;
}

.pg-version-badge span {
    color: var(--pg-dim);
    font-size: 0.61rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.pg-version-badge strong {
    margin-top: 0.15rem;
    color: #ff8eb8;
    font-size: 1rem;
    font-weight: 900;
}

.pg-alert {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: 0.78rem;
    align-items: center;
    margin-top: 1.05rem;
    padding: 0.88rem 1rem;
    border: 1px solid rgba(255, 45, 117, 0.36);
    border-radius: 17px;
    background: linear-gradient(135deg, rgba(255, 45, 117, 0.13), rgba(189, 36, 255, 0.055));
    color: #fff2f8;
    line-height: 1.5;
}

.pg-alert-mark {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 143, 187, 0.42);
    border-radius: 12px;
    background: rgba(5, 3, 9, 0.50);
    color: #ff8eb8;
    font-size: 0.67rem;
    font-weight: 900;
    letter-spacing: 0.04em;
    box-shadow: 0 0 18px rgba(255, 45, 117, 0.16);
}

.pg-alert-copy b {
    color: #ffffff;
}

.pg-alert-copy span {
    color: #edd8e7;
}

.pg-section-title {
    margin: 0.9rem 0 0.28rem;
    color: var(--pg-text);
    font-size: clamp(2rem, 3.2vw, 2.72rem);
    font-weight: 910;
    letter-spacing: 0;
    line-height: 1.05;
    animation: pgFadeRise 360ms ease both;
}

.pg-section-note {
    margin-bottom: 1rem;
    color: var(--pg-muted);
    font-size: 1.03rem;
    line-height: 1.5;
    animation: pgFadeRise 380ms ease both;
}

/* ------------------------------------------------------------
   Carcasa estable del centro de mando y expansión del contenido
   ------------------------------------------------------------ */

.pg-command-anchor,
.pg-rail-anchor {
    width: 0;
    height: 0;
    overflow: hidden;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-anchor) {
    align-items: flex-start !important;
    gap: 2rem !important;
    transition: gap 180ms ease !important;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="stColumn"]:first-child,
[data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="column"]:first-child {
    flex: 0 0 var(--pg-command-width) !important;
    width: var(--pg-command-width) !important;
    min-width: var(--pg-command-width) !important;
    max-width: var(--pg-command-width) !important;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-state-closed) {
    gap: 0.95rem !important;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-state-closed) > [data-testid="stColumn"]:first-child,
[data-testid="stHorizontalBlock"]:has(.pg-command-state-closed) > [data-testid="column"]:first-child {
    flex: 0 0 var(--pg-rail-width) !important;
    width: var(--pg-rail-width) !important;
    min-width: var(--pg-rail-width) !important;
    max-width: var(--pg-rail-width) !important;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="stColumn"]:last-child,
[data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="column"]:last-child {
    flex: 1 1 0 !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
}

[data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="stColumn"],
[data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="column"] {
    min-width: 0 !important;
    transition: none !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) {
    position: sticky !important;
    top: 1rem !important;
    align-self: flex-start !important;
    min-height: calc(100vh - 2rem) !important;
    padding: 1.15rem 1.05rem 1.28rem !important;
    overflow: hidden !important;
    isolation: isolate;
    border: 1px solid rgba(255, 45, 117, 0.58) !important;
    border-radius: 29px !important;
    background:
        radial-gradient(circle at 12% 7%, rgba(255, 45, 117, 0.25), transparent 33%),
        radial-gradient(circle at 92% 0%, rgba(189, 36, 255, 0.21), transparent 31%),
        linear-gradient(180deg, rgba(45, 8, 43, 0.985), rgba(14, 7, 22, 0.985) 47%, rgba(20, 7, 29, 0.98)) !important;
    box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 0.035),
        0 0 38px rgba(255, 45, 117, 0.22),
        var(--pg-shadow) !important;
    animation: pgPanelReveal 310ms cubic-bezier(.2, .86, .2, 1) both;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open)::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: 9px;
    border: 1px solid rgba(255, 255, 255, 0.045);
    border-radius: 23px;
    pointer-events: none;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open)::after {
    content: "";
    position: absolute;
    top: 72px;
    right: -1px;
    width: 2px;
    height: 92px;
    border-radius: 999px;
    background: linear-gradient(180deg, transparent, #ff2d75 42%, #bd24ff 72%, transparent);
    box-shadow: 0 0 14px rgba(255, 45, 117, 0.72);
    pointer-events: none;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-command-head-premium,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-command-divider,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-sidebar-field-label,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) div[data-testid="stExpander"],
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-active-model-card,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-command-section-title,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .stCheckbox,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-scale-mini-command,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-sidebar-note,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.st-key-pg_close_command_center button:is(:active, :focus, :focus-visible)) .pg-command-footnote {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* Botón cerrar: integrado en la esquina superior del panel. */
.st-key-pg_close_command_center,
[data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="stColumn"]:first-child > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:nth-child(2),
[data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="column"]:first-child > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:nth-child(2) {
    position: absolute !important;
    z-index: 20 !important;
    top: 0.82rem !important;
    right: 0.78rem !important;
    width: 2.35rem !important;
}

.st-key-pg_close_command_center .stButton > button,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) .stButton > button {
    width: 2.35rem !important;
    min-width: 2.35rem !important;
    max-width: 2.35rem !important;
    height: 2.35rem !important;
    min-height: 2.35rem !important;
    padding: 0 0 0.08rem !important;
    border: 1px solid rgba(255, 95, 150, 0.55) !important;
    border-radius: 12px !important;
    background:
        radial-gradient(circle at 30% 18%, rgba(255, 255, 255, 0.12), transparent 22%),
        rgba(7, 4, 12, 0.72) !important;
    color: #fff8fd !important;
    font-size: 1.28rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    box-shadow: 0 0 18px rgba(255, 45, 117, 0.19), inset 0 0 0 1px rgba(255, 255, 255, 0.025) !important;
}

.st-key-pg_close_command_center .stButton > button:hover,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) .stButton > button:hover {
    transform: translateX(-1px) !important;
    border-color: rgba(255, 121, 172, 0.88) !important;
    background: linear-gradient(135deg, rgba(255, 45, 117, 0.28), rgba(189, 36, 255, 0.16)) !important;
    box-shadow: 0 0 28px rgba(255, 45, 117, 0.34) !important;
}

.pg-command-head-premium {
    padding: 0.38rem 0.35rem 0.16rem;
    text-align: center;
    overflow-wrap: anywhere;
}

.pg-command-logo-orbit {
    width: 84px;
    height: 84px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0.1rem auto 0.78rem;
    border: 1px solid rgba(255, 45, 117, 0.48);
    border-radius: 26px;
    background:
        radial-gradient(circle at 35% 18%, rgba(255, 255, 255, 0.14), transparent 18%),
        linear-gradient(145deg, rgba(255, 45, 117, 0.18), rgba(189, 36, 255, 0.13) 55%, rgba(4, 3, 9, 0.90));
    box-shadow: 0 0 34px rgba(255, 45, 117, 0.30), inset 0 0 18px rgba(255, 255, 255, 0.035);
}

.pg-command-logo-img {
    display: block;
    width: 63px !important;
    height: 63px !important;
    object-fit: contain !important;
    border-radius: 17px;
    filter: drop-shadow(0 0 14px rgba(255, 45, 117, 0.48));
}

.pg-command-logo-fallback {
    width: 63px;
    height: 63px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    color: #ffffff;
    font-weight: 900;
    background: linear-gradient(135deg, #ff1744, #ff2d75 60%, #bd24ff);
}

.pg-command-kicker {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.46rem;
    margin-bottom: 0.40rem;
    color: #ff91ba;
    font-size: 0.70rem;
    font-weight: 900;
    letter-spacing: 0.19em;
    text-transform: uppercase;
    text-shadow: 0 0 14px rgba(255, 45, 117, 0.28);
}

.pg-command-pulse {
    width: 0.42rem;
    height: 0.42rem;
    border-radius: 999px;
    background: #ff2d75;
    box-shadow: 0 0 12px rgba(255, 45, 117, 0.92);
}

.pg-command-title {
    color: #fff8fd;
    font-size: clamp(1.58rem, 2.2vw, 1.9rem);
    font-weight: 930;
    letter-spacing: 0;
    line-height: 1;
    text-shadow: 0 0 20px rgba(255, 45, 117, 0.20);
}

.pg-command-subtitle {
    max-width: 232px;
    margin: 0.62rem auto 0;
    color: #d9c7e5;
    font-size: 0.92rem;
    line-height: 1.5;
}

.pg-command-divider {
    height: 1px;
    margin: 1.03rem 0;
    background: linear-gradient(90deg, transparent, rgba(255, 45, 117, 0.54), rgba(189, 36, 255, 0.30), transparent);
}

.pg-sidebar-field-label,
.pg-command-section-title {
    margin-bottom: 0.55rem;
    color: #fff8fd;
    font-size: 0.94rem;
    font-weight: 880;
    letter-spacing: 0.018em;
    text-shadow: 0 0 12px rgba(255, 45, 117, 0.16);
}

.pg-command-section-title-centered {
    text-align: center;
}

/* Selector cerrado: expander + radio, sin búsqueda ni escritura libre. */
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[data-testid="stExpander"] {
    overflow: hidden !important;
    border: 1px solid rgba(255, 45, 117, 0.37) !important;
    border-radius: 16px !important;
    background:
        linear-gradient(135deg, rgba(255, 255, 255, 0.055), rgba(255, 45, 117, 0.052)),
        rgba(12, 7, 19, 0.90) !important;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03), 0 0 20px rgba(255, 45, 117, 0.11) !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[data-testid="stExpander"] summary {
    min-height: 2.75rem !important;
    padding: 0.68rem 0.82rem !important;
    color: #fff8fd !important;
    font-weight: 820 !important;
    letter-spacing: 0 !important;
    overflow-wrap: anywhere !important;
    transition: background 170ms ease !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[data-testid="stExpander"] summary:hover {
    background: rgba(255, 45, 117, 0.085) !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[data-testid="stExpander"] summary svg,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {
    color: #ff81ae !important;
    fill: #ff81ae !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[role="radiogroup"] {
    gap: 0.28rem !important;
    padding: 0.24rem 0.28rem 0.42rem !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[role="radiogroup"] label {
    width: 100% !important;
    min-height: 2.38rem !important;
    margin: 0.12rem 0 !important;
    padding: 0.48rem 0.58rem !important;
    border: 1px solid rgba(255, 255, 255, 0.085) !important;
    border-radius: 12px !important;
    background: rgba(255, 255, 255, 0.028) !important;
    color: #fff8fd !important;
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease, box-shadow 160ms ease !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[role="radiogroup"] label:hover {
    transform: translateX(1px) !important;
    border-color: rgba(255, 45, 117, 0.44) !important;
    background: linear-gradient(90deg, rgba(255, 45, 117, 0.15), rgba(189, 36, 255, 0.08)) !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[role="radiogroup"] label:has(input:checked) {
    border-color: rgba(255, 45, 117, 0.66) !important;
    background: linear-gradient(90deg, rgba(255, 45, 117, 0.23), rgba(189, 36, 255, 0.11)) !important;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.025), 0 0 16px rgba(255, 45, 117, 0.12) !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) div[role="radiogroup"] label p {
    color: #fff8fd !important;
    font-size: 0.89rem !important;
}

.pg-active-model-card {
    margin: 0.88rem 0 1.04rem;
    padding: 0.96rem 0.98rem;
    border: 1px solid rgba(255, 45, 117, 0.48);
    border-radius: 20px;
    background:
        radial-gradient(circle at 0% 0%, rgba(255, 45, 117, 0.21), transparent 39%),
        radial-gradient(circle at 96% 15%, rgba(189, 36, 255, 0.17), transparent 34%),
        linear-gradient(135deg, rgba(34, 9, 38, 0.94), rgba(12, 7, 20, 0.91));
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.035), 0 0 28px rgba(255, 45, 117, 0.15);
    overflow-wrap: anywhere;
}

.pg-active-model-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.42rem;
}

.pg-active-model-topline {
    color: #ff91ba;
    font-size: 0.67rem;
    font-weight: 900;
    letter-spacing: 0.17em;
    text-transform: uppercase;
}

.pg-active-model-local {
    padding: 0.19rem 0.45rem;
    border: 1px solid rgba(0, 230, 154, 0.28);
    border-radius: 999px;
    background: rgba(0, 230, 154, 0.07);
    color: #84f3cc;
    font-size: 0.62rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.pg-active-model-name {
    margin-bottom: 0.12rem;
    color: #fff8fd;
    font-size: 1.08rem;
    font-weight: 900;
    letter-spacing: 0;
}

.pg-active-model-short {
    margin-bottom: 0.40rem;
    color: #ff4f91;
    font-size: 0.83rem;
    font-weight: 860;
}

.pg-active-model-card p {
    margin: 0 !important;
    color: #efd4e3 !important;
    font-size: 0.89rem !important;
    line-height: 1.53 !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) .stCheckbox {
    margin: 0.22rem 0 !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) .stCheckbox label {
    align-items: flex-start !important;
    gap: 0.35rem !important;
}

div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) .stCheckbox label p {
    color: #f4e9fb !important;
    font-size: 0.88rem !important;
    line-height: 1.42 !important;
}

.pg-scale-mini {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
    margin: 0.5rem 0 0.25rem;
}

.pg-scale-mini span {
    display: block;
    height: 10px;
    border-radius: 999px;
}

.pg-scale-mini-command {
    gap: 5px;
    margin: 0.58rem auto 0.35rem;
}

.pg-scale-mini-command span {
    height: 10px;
    box-shadow: 0 0 11px rgba(255, 45, 117, 0.17);
}

.pg-sidebar-note {
    margin: 0.3rem 0 0;
    color: #d9c7e5;
    font-size: 0.86rem;
    line-height: 1.52;
    text-align: center;
}

.pg-command-footnote {
    padding: 0.15rem 0.16rem 0.02rem;
    color: #a992b7;
    font-size: 0.82rem;
    line-height: 1.52;
    text-align: center;
}

/* Pestaña cerrada: visible, integrada y compacta. */
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-closed) {
    position: sticky !important;
    top: 1rem !important;
    align-self: flex-start !important;
    min-height: 188px !important;
    padding: 0.58rem 0.42rem 0.50rem !important;
    overflow: hidden !important;
    border: 1px solid rgba(255, 45, 117, 0.52) !important;
    border-radius: 17px !important;
    background:
        radial-gradient(circle at 50% 4%, rgba(255, 45, 117, 0.22), transparent 34%),
        linear-gradient(180deg, rgba(37, 8, 39, 0.97), rgba(10, 6, 17, 0.97)) !important;
    box-shadow: 0 0 28px rgba(255, 45, 117, 0.18), 0 18px 50px rgba(0, 0, 0, 0.38) !important;
    animation: pgRailReveal 260ms ease both;
}

.pg-rail-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.58rem;
}

.pg-rail-logo-shell {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 45, 117, 0.36);
    border-radius: 12px;
    background: rgba(5, 3, 9, 0.72);
    box-shadow: 0 0 18px rgba(255, 45, 117, 0.19);
}

.pg-rail-logo-img {
    width: 31px;
    height: 31px;
    object-fit: contain;
    border-radius: 9px;
}

.pg-rail-logo-fallback {
    color: #ff8eb8;
    font-size: 0.68rem;
    font-weight: 900;
}

.pg-rail-label {
    color: #ff91ba;
    font-size: 0.58rem;
    font-weight: 900;
    letter-spacing: 0.18em;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
}

.st-key-pg_open_command_center {
    width: 38px !important;
    margin: 0.58rem auto 0 !important;
}

.st-key-pg_open_command_center .stButton > button,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-closed) .stButton > button {
    width: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;
    height: 38px !important;
    min-height: 38px !important;
    padding: 0 0 0.08rem !important;
    border: 1px solid rgba(255, 76, 139, 0.68) !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, rgba(255, 45, 117, 0.30), rgba(189, 36, 255, 0.18)) !important;
    color: #fff8fd !important;
    font-size: 1.28rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    box-shadow: 0 0 20px rgba(255, 45, 117, 0.24) !important;
}

.st-key-pg_open_command_center .stButton > button:hover,
div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-closed) .stButton > button:hover {
    transform: translateX(1px) !important;
    border-color: rgba(255, 129, 176, 0.90) !important;
    box-shadow: 0 0 30px rgba(255, 45, 117, 0.40) !important;
}

/* ------------------------------------------------------------
   Tarjetas de resultado y escala de riesgo
   ------------------------------------------------------------ */

.pg-verdict-card {
    max-width: 1020px;
    margin: 0.45rem auto 1rem;
    padding: 1.55rem;
    border: 1px solid var(--pg-border);
    border-radius: 30px;
    background:
        radial-gradient(circle at 92% 10%, rgba(255, 45, 117, 0.13), transparent 28%),
        linear-gradient(135deg, rgba(22, 16, 32, 0.97), rgba(11, 8, 18, 0.95));
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.30);
}

.pg-verdict-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(220px, 280px);
    gap: 1.2rem;
    align-items: center;
}

.pg-verdict-label {
    margin-bottom: 0.45rem;
    color: var(--pg-muted);
    font-size: 0.78rem;
    font-weight: 820;
    letter-spacing: 0.10em;
    text-transform: uppercase;
}

.pg-verdict-main {
    font-size: clamp(2.8rem, 5.6vw, 4.65rem);
    font-weight: 930;
    letter-spacing: 0;
    line-height: 1.01;
}

.pg-prob-panel {
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.042);
    text-align: center;
}

.pg-prob-number {
    font-size: 2.65rem;
    font-weight: 930;
    letter-spacing: 0;
}

.pg-prob-caption {
    margin-top: -0.2rem;
    color: var(--pg-muted);
    font-size: 0.84rem;
}

.pg-risk-chip {
    display: inline-block;
    margin-top: 0.78rem;
    padding: 0.43rem 0.76rem;
    border-radius: 999px;
    color: #09070d;
    font-weight: 900;
}

.pg-simple-advice {
    margin-top: 0.72rem;
    color: var(--pg-muted);
    font-size: 1rem;
    line-height: 1.58;
}

.pg-meter-label-row {
    display: flex;
    justify-content: space-between;
    margin: 0.82rem 0 0.25rem;
    color: var(--pg-dim);
    font-size: 0.76rem;
}

.pg-meter-wrap {
    position: relative;
    width: 100%;
    height: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.075);
}

.pg-meter-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #00e69a 0%, #7cff6b 12%, #ffd166 28%, #ff9f1c 48%, #ff5c33 62%, #ff2d75 78%, #ff1744 100%);
    box-shadow: 0 0 24px rgba(255, 45, 117, 0.40);
}

.pg-meter-pin {
    position: absolute;
    top: -3px;
    width: 16px;
    height: 26px;
    border-radius: 999px;
    background: #ffffff;
    opacity: 0.96;
    box-shadow: 0 0 18px rgba(255, 255, 255, 0.55);
}

.pg-small {
    color: var(--pg-muted);
    font-size: 0.88rem;
}

.pg-pill {
    display: inline-block;
    margin: 0.18rem 0.22rem 0.18rem 0;
    padding: 0.37rem 0.64rem;
    border: 1px solid rgba(255, 45, 117, 0.25);
    border-radius: 999px;
    background: rgba(255, 45, 117, 0.11);
    color: #ffeaf3;
    font-size: 0.85rem;
}

.pg-mini-model {
    min-height: 146px;
    padding: 0.96rem;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 20px;
    background: rgba(22, 16, 32, 0.82);
}

.pg-mini-model-name {
    margin-bottom: 0.52rem;
    color: var(--pg-muted);
    font-size: 0.83rem;
    font-weight: 820;
}

.pg-mini-model-result {
    font-size: 1.28rem;
    font-weight: 910;
    letter-spacing: 0;
}

.pg-mini-model-prob {
    margin-top: 0.34rem;
    color: #ffffff;
    font-size: 1.02rem;
    font-weight: 800;
}

.pg-mini-risk {
    display: inline-block;
    margin-top: 0.54rem;
    padding: 0.27rem 0.56rem;
    border-radius: 999px;
    color: #09070d;
    font-size: 0.76rem;
    font-weight: 900;
}

/* ------------------------------------------------------------
   Loader local y modal de resultado
   ------------------------------------------------------------ */

.pg-loader-overlay {
    position: fixed;
    z-index: 999999;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background:
        radial-gradient(circle at 20% 12%, rgba(189, 36, 255, 0.16), transparent 34%),
        radial-gradient(circle at 82% 18%, rgba(255, 45, 117, 0.16), transparent 28%),
        rgba(6, 5, 10, 0.64);
    backdrop-filter: blur(10px) saturate(120%);
    -webkit-backdrop-filter: blur(10px) saturate(120%);
    animation: pgOverlayIn 220ms ease-out both;
}

.pg-loader-card {
    width: min(920px, 92vw);
    margin: 0;
    padding: 1.35rem 1.55rem;
    border: 1px solid rgba(255, 45, 117, 0.27);
    border-radius: 30px;
    background:
        radial-gradient(circle at 18% 20%, rgba(189, 36, 255, 0.18), transparent 32%),
        linear-gradient(135deg, rgba(20, 13, 32, 0.97), rgba(9, 7, 15, 0.96));
    box-shadow: 0 0 52px rgba(255, 45, 117, 0.18), 0 22px 70px rgba(0, 0, 0, 0.36);
}

.pg-loader-floating {
    transform-origin: center;
    animation: pgFloatIn 330ms cubic-bezier(.2, .9, .2, 1) both;
}

.pg-loader-grid {
    display: grid;
    grid-template-columns: 170px minmax(0, 1fr);
    gap: 1.35rem;
    align-items: center;
}

.pg-ring-shell {
    display: flex;
    align-items: center;
    justify-content: center;
}

.pg-ring {
    position: relative;
    width: 142px;
    height: 142px;
    padding: 10px;
    border-radius: 50%;
    box-shadow: 0 0 36px rgba(255, 45, 117, 0.38), inset 0 0 22px rgba(189, 36, 255, 0.16);
    transition: background 45ms linear, filter 120ms ease;
}

.pg-ring::after {
    content: "";
    position: absolute;
    inset: -8px;
    border: 1px solid rgba(255, 45, 117, 0.24);
    border-radius: 50%;
    box-shadow: 0 0 34px rgba(255, 45, 117, 0.22);
    animation: pgPulseRing 1.35s ease-in-out infinite;
}

.pg-ring-inner {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 50%;
    background: linear-gradient(145deg, #130d1d, #08070d);
}

.pg-ring-number {
    color: #ffffff;
    font-size: 2.4rem;
    font-weight: 930;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0;
}

.pg-ring-label {
    margin-top: 0.14rem;
    color: #ff86b0;
    font-size: 0.67rem;
    font-weight: 850;
    letter-spacing: 0.13em;
    text-transform: uppercase;
}

.pg-loader-copy {
    min-width: 0;
}

.pg-analysis-title {
    margin-bottom: 0.66rem;
    color: #ffe8f1;
    font-size: 1.02rem;
    font-weight: 850;
}

.pg-loader-status {
    margin-bottom: 0.3rem;
    color: #ffe9f2;
    font-size: 1.18rem;
    font-weight: 850;
}

.pg-step-list {
    margin: 0.78rem 0 0.38rem 1.08rem;
    padding: 0;
    color: var(--pg-muted);
    font-size: 0.98rem;
    line-height: 1.55;
}

.pg-step-list li::marker {
    color: var(--pg-crimson);
}

.pg-loader-note {
    margin-top: 0.72rem;
    color: #ff9fc0;
    font-size: 0.76rem;
    font-weight: 850;
    letter-spacing: 0.10em;
    text-transform: uppercase;
}

.pg-loader-card-done {
    width: min(720px, 88vw);
    padding: 0.86rem 1rem;
    text-align: center;
}

.pg-analysis-done {
    color: #bafde5;
    font-weight: 780;
}

div[data-testid="stDialog"] {
    backdrop-filter: blur(8px) saturate(125%) !important;
    -webkit-backdrop-filter: blur(8px) saturate(125%) !important;
}

div[data-testid="stDialog"] div[role="dialog"] {
    max-width: min(1120px, 94vw) !important;
    max-height: 88vh !important;
    overflow-y: auto !important;
    border: 1px solid rgba(255, 45, 117, 0.39) !important;
    border-radius: 29px !important;
    background:
        radial-gradient(circle at 18% 8%, rgba(189, 36, 255, 0.18), transparent 32%),
        radial-gradient(circle at 90% 10%, rgba(255, 45, 117, 0.18), transparent 30%),
        linear-gradient(135deg, #0b0712 0%, #13091b 48%, #08070d 100%) !important;
    color: var(--pg-text) !important;
    box-shadow: 0 0 80px rgba(255, 45, 117, 0.22), 0 24px 120px rgba(0, 0, 0, 0.72) !important;
    animation: pgModalIn 280ms cubic-bezier(.18, .92, .24, 1) both !important;
}

div[data-testid="stDialog"] h1,
div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] h3,
div[data-testid="stDialog"] h4,
div[data-testid="stDialog"] p,
div[data-testid="stDialog"] span,
div[data-testid="stDialog"] label {
    color: var(--pg-text);
}

div[data-testid="stDialog"] .pg-verdict-card {
    margin-top: 0.45rem;
    margin-bottom: 1.18rem;
}

.pg-result-window-label {
    display: inline-flex;
    align-items: center;
    margin: 0.42rem 0 0.42rem;
    padding: 0.36rem 0.68rem;
    border: 1px solid rgba(255, 45, 117, 0.24);
    border-radius: 999px;
    background: rgba(255, 45, 117, 0.11);
    color: #ff86b0;
    font-size: 0.75rem;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.pg-section-title-result {
    margin-top: 0.34rem;
    font-size: clamp(2.05rem, 3.3vw, 2.85rem);
    text-align: left;
}

.pg-context-note {
    margin: 0.84rem 0 1rem;
    padding: 0.82rem 0.96rem;
    border: 1px solid rgba(255, 209, 102, 0.34);
    border-radius: 17px;
    background: rgba(255, 209, 102, 0.072);
    color: #ffe9bd;
    font-size: 0.95rem;
    line-height: 1.55;
}

.pg-result-preview {
    margin: 1.02rem 0 0.84rem;
    padding: 1.02rem 1.12rem;
    border: 1px solid rgba(255, 45, 117, 0.34);
    border-radius: 22px;
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 45, 117, 0.15), transparent 28%),
        linear-gradient(135deg, rgba(22, 17, 32, 0.88), rgba(11, 8, 18, 0.88));
    box-shadow: 0 0 32px rgba(255, 45, 117, 0.13), inset 0 0 0 1px rgba(255, 255, 255, 0.03);
    animation: pgFadeRise 300ms ease-out both;
}

.pg-preview-kicker {
    margin-bottom: 0.24rem;
    color: #ff86b0;
    font-size: 0.70rem;
    font-weight: 900;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.pg-preview-title {
    font-size: clamp(1.42rem, 2.4vw, 2rem);
    font-weight: 920;
    letter-spacing: 0;
    line-height: 1.05;
}

.pg-preview-meta {
    margin-top: 0.31rem;
    color: #f5e6ff;
    font-size: 0.95rem;
    font-weight: 750;
}

.pg-preview-note {
    margin-top: 0.31rem;
    color: var(--pg-muted);
    font-size: 0.90rem;
    line-height: 1.5;
}

/* Expanders generales de resultados. */
div[data-testid="stExpander"] {
    border-color: rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    background: rgba(10, 7, 16, 0.36) !important;
}

/* ------------------------------------------------------------
   Animaciones y comportamiento responsive
   ------------------------------------------------------------ */

@keyframes pgFadeRise {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pgPanelReveal {
    from { opacity: 0; transform: translateX(-8px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pgRailReveal {
    from { opacity: 0; transform: translateX(-5px) scale(0.98); }
    to { opacity: 1; transform: translateX(0) scale(1); }
}

@keyframes pgOverlayIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pgFloatIn {
    from { opacity: 0; transform: translateY(16px) scale(0.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes pgPulseRing {
    0%, 100% { opacity: 0.42; transform: scale(1); }
    50% { opacity: 0.88; transform: scale(1.05); }
}

@keyframes pgModalIn {
    from { opacity: 0; transform: translateY(18px) scale(0.982); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@media (max-width: 1120px) {
    :root {
        --pg-command-width: 270px;
    }

    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) {
        gap: 1.35rem !important;
    }

    .pg-command-subtitle {
        max-width: 220px;
    }
}

@media (max-width: 980px) {
    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) {
        flex-direction: column !important;
        gap: 1rem !important;
    }

    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="stColumn"]:first-child,
    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="column"]:first-child,
    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="stColumn"]:last-child,
    [data-testid="stHorizontalBlock"]:has(.pg-command-state-open) > [data-testid="column"]:last-child {
        flex: 1 1 auto !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
    }

    div:is([data-testid="stColumn"], [data-testid="column"]):has(.pg-command-state-open) {
        position: relative !important;
        top: auto !important;
        min-height: auto !important;
    }

    .pg-command-subtitle,
    .pg-sidebar-note,
    .pg-command-footnote {
        max-width: none;
    }

    .pg-verdict-grid,
    .pg-loader-grid {
        grid-template-columns: 1fr;
    }

    .pg-ring {
        width: 122px;
        height: 122px;
    }

    div[data-testid="stDialog"] div[role="dialog"] {
        width: 96vw !important;
    }
}

@media (max-width: 760px) {
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding: 1rem 0.85rem 2.25rem !important;
    }

    .pg-status-bar {
        flex-wrap: wrap;
        gap: 0.4rem 0.55rem;
        border-radius: 18px;
        font-size: 0.76rem;
    }

    .pg-hero {
        padding: 1.08rem;
        border-radius: 22px;
    }

    .pg-hero-core {
        grid-template-columns: auto minmax(0, 1fr);
    }

    .pg-version-badge {
        grid-column: 1 / -1;
        width: fit-content;
        min-width: 82px;
        margin-left: auto;
    }

    .pg-alert {
        align-items: flex-start;
    }

    .pg-loader-overlay {
        align-items: flex-start;
        padding: 4.5rem 0.85rem 1rem;
    }
}

@media (max-width: 560px) {
    [data-testid="stHorizontalBlock"]:has(.pg-command-state-closed) {
        gap: 0.62rem !important;
    }

    .pg-hero-logo-shell {
        width: 62px;
        height: 62px;
        border-radius: 18px;
    }

    .pg-hero-logo-img,
    .pg-logo-fallback {
        width: 50px;
        height: 50px;
    }

    .pg-kicker {
        font-size: 0.64rem;
        letter-spacing: 0.12em;
    }

    .pg-title {
        font-size: 2rem;
    }

    .pg-alert-mark {
        display: none;
    }

    .pg-alert {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stHorizontalBlock"]:has(.pg-command-anchor),
    [data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="stColumn"],
    [data-testid="stHorizontalBlock"]:has(.pg-command-anchor) > [data-testid="column"],
    .pg-hero,
    .pg-status-bar,
    .pg-result-preview,
    .pg-loader-overlay,
    .pg-loader-floating,
    div[data-testid="stDialog"] div[role="dialog"] {
        animation: none !important;
        transition-duration: 1ms !important;
    }

    .pg-ring::after {
        animation: none !important;
    }
}
</style>
"""
