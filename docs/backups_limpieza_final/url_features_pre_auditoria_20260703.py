import ast
import ipaddress
import re
import warnings
from urllib.parse import urlparse

import pandas as pd


# ============================================================
# url_features.py
# Extracción de 27 características URL/enlaces para inferencia.
#
# Seguridad:
# - Este módulo NO visita enlaces.
# - Este módulo NO hace requests HTTP/HTTPS.
# - Todo se procesa únicamente como texto.
# ============================================================


URL_FEATURES = [
    "url_web_count",
    "url_max_len",
    "url_mean_len",
    "url_total_len",
    "url_digits_count",
    "url_special_count",
    "url_hyphen_count",
    "url_dot_count",
    "url_at_count",
    "url_question_count",
    "url_equal_count",
    "url_ampersand_count",
    "url_percent_count",
    "url_slash_count",
    "url_subdomain_max",
    "url_contains_ip",
    "url_uses_https",
    "url_shortener_present",
    "url_suspicious_words_count",
    "link_total_detected_count",
    "link_mailto_count",
    "link_cid_count",
    "link_other_count",
    "has_web_url",
    "has_mailto",
    "has_cid",
    "has_other_link",
]


SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "verification",
    "account",
    "secure",
    "security",
    "update",
    "validate",
    "password",
    "pass",
    "bank",
    "banking",
    "banco",
    "cuenta",
    "clave",
    "seguridad",
    "verificar",
    "actualizar",
    "confirmar",
    "confirmacion",
    "confirmación",
    "bloqueo",
    "bloqueada",
    "suspension",
    "suspensión",
    "suspendida",
    "soporte",
    "cliente",
    "access",
    "signin",
    "sign-in",
    "auth",
    "authentication",
    "token",
]


SHORTENER_DOMAINS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
    "rebrand.ly",
    "shorturl.at",
]


def safe_text(value) -> str:
    """
    Convierte cualquier entrada en texto seguro.
    Evita errores por None, NaN u otros tipos de datos.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass

    return str(value).strip()


def merge_url_inputs(*values) -> str:
    """
    Une varias fuentes posibles de enlaces:
    asunto, cuerpo, campo manual de URL, etc.

    Esto permite que la app pueda detectar enlaces pegados
    tanto en el campo de URL como dentro del texto del mensaje.
    """
    clean_values = []
    for value in values:
        clean = safe_text(value)
        if clean:
            clean_values.append(clean)
    return "\n".join(clean_values)


def normalize_url_for_parsing(url: str) -> str:
    """
    Normaliza una URL únicamente para análisis local.
    No visita la URL ni realiza conexiones externas.
    """
    u = safe_text(url)

    if not u:
        return ""

    replacements = {
        "hxxps://": "https://",
        "hxxp://": "http://",
        "[.]": ".",
        "(.)": ".",
        "[:]": ":",
    }

    for old, new in replacements.items():
        u = u.replace(old, new)

    u = u.strip().strip("[]'\"(),;")

    if u.startswith("www."):
        u = "http://" + u

    return u


def split_raw_links(value):
    """
    Extrae elementos tipo enlace desde un texto.

    Puede detectar:
    - URLs web: http, https, hxxp, hxxps, www
    - mailto:
    - cid:
    - listas representadas como texto
    - dominios neutralizados con [.]

    Retorna una lista de enlaces o referencias encontradas.
    """
    raw = safe_text(value)

    if not raw:
        return []

    links = []

    # Caso 1: lista representada como string: ['url1', 'url2']
    # Se intenta solo si parece lista, para evitar warnings innecesarios.
    if raw.startswith("[") and raw.endswith("]"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                parsed = ast.literal_eval(raw)

            if isinstance(parsed, list):
                links = [safe_text(x) for x in parsed if safe_text(x)]
        except Exception:
            links = []

    # Caso 2: regex sobre texto completo.
    if not links:
        pattern = r"(?:hxxps?://|https?://|www\.|mailto:|cid:)[^\s,\];|]+"
        links = re.findall(pattern, raw, flags=re.IGNORECASE)

    # Caso 3: dominios neutralizados o dominios simples dentro del texto.
    if not links:
        domain_pattern = r"\b[a-zA-Z0-9-]+(?:\.|\[\.\])[a-zA-Z0-9.-]+(?:/[^\s]*)?"
        links = re.findall(domain_pattern, raw)

    # Caso 4: separación simple por espacios, coma, punto y coma o pipe.
    if not links:
        parts = re.split(r"[\s,;|]+", raw)
        links = [
            p.strip().strip("[]'\"(),;")
            for p in parts
            if p.strip()
        ]

    return [link for link in links if safe_text(link)]


def classify_links(raw_links):
    """
    Clasifica enlaces en cuatro grupos:
    - web_urls: URL web o dominios analizables.
    - mailto_links: enlaces de correo.
    - cid_links: referencias internas de correo.
    - other_links: otros elementos detectados.
    """
    web_urls = []
    mailto_links = []
    cid_links = []
    other_links = []

    for link in raw_links:
        l = safe_text(link)
        low = l.lower()

        if not l:
            continue

        if low.startswith("mailto:"):
            mailto_links.append(l)
            continue

        if low.startswith("cid:"):
            cid_links.append(l)
            continue

        if low.startswith(("http://", "https://", "hxxp://", "hxxps://", "www.")):
            web_urls.append(normalize_url_for_parsing(l))
            continue

        # Dominios neutralizados o dominios simples.
        # Se evita tratar correos con @ como URL web.
        domain_like = re.search(
            r"(^|[^\w@])([a-z0-9-]+(\.|\[\.\]))+[a-z]{2,}(/[^\s]*)?",
            low,
        )

        if domain_like and "@" not in low:
            web_urls.append(normalize_url_for_parsing(l))
        else:
            other_links.append(l)

    return web_urls, mailto_links, cid_links, other_links


def is_ip_address(host: str) -> int:
    """
    Retorna 1 si el host corresponde a una dirección IP; de lo contrario, 0.
    """
    host = safe_text(host)

    if not host:
        return 0

    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0


def count_subdomains(host: str) -> int:
    """
    Cuenta subdominios de forma aproximada.
    Ejemplo:
    - dominio.com => 0
    - login.dominio.com => 1
    - a.b.dominio.com => 2
    """
    host = safe_text(host).lower()

    if not host:
        return 0

    if is_ip_address(host):
        return 0

    parts = [p for p in host.split(".") if p]

    if len(parts) <= 2:
        return 0

    return max(0, len(parts) - 2)


def contains_shortener(host: str) -> int:
    """
    Retorna 1 si el host parece pertenecer a un acortador conocido.
    """
    host = safe_text(host).lower()
    return int(any(domain in host for domain in SHORTENER_DOMAINS))


def web_features(web_urls):
    """
    Calcula características léxicas sobre URLs web.

    Importante:
    - No incluye mailto ni cid.
    - No abre enlaces.
    - No consulta internet.
    """
    if not web_urls:
        return {
            "url_web_count": 0,
            "url_max_len": 0,
            "url_mean_len": 0,
            "url_total_len": 0,
            "url_digits_count": 0,
            "url_special_count": 0,
            "url_hyphen_count": 0,
            "url_dot_count": 0,
            "url_at_count": 0,
            "url_question_count": 0,
            "url_equal_count": 0,
            "url_ampersand_count": 0,
            "url_percent_count": 0,
            "url_slash_count": 0,
            "url_subdomain_max": 0,
            "url_contains_ip": 0,
            "url_uses_https": 0,
            "url_shortener_present": 0,
            "url_suspicious_words_count": 0,
        }

    lengths = []
    digits_count = 0
    special_count = 0
    hyphen_count = 0
    dot_count = 0
    at_count = 0
    question_count = 0
    equal_count = 0
    ampersand_count = 0
    percent_count = 0
    slash_count = 0
    subdomain_values = []
    contains_ip = 0
    uses_https = 0
    shortener_present = 0
    suspicious_words_count = 0

    for url in web_urls:
        u = normalize_url_for_parsing(url)
        parsed = urlparse(u if "://" in u else "http://" + u)

        host = parsed.netloc.lower()
        full_text = u.lower()

        lengths.append(len(u))
        digits_count += sum(ch.isdigit() for ch in u)
        special_count += sum(ch in "-_%?&=@#" for ch in u)

        hyphen_count += u.count("-")
        dot_count += u.count(".")
        at_count += u.count("@")
        question_count += u.count("?")
        equal_count += u.count("=")
        ampersand_count += u.count("&")
        percent_count += u.count("%")
        slash_count += u.count("/")

        subdomain_values.append(count_subdomains(host))

        contains_ip = max(contains_ip, is_ip_address(host))
        uses_https = max(uses_https, int(parsed.scheme == "https"))
        shortener_present = max(shortener_present, contains_shortener(host))

        suspicious_words_count += sum(
            1 for word in SUSPICIOUS_WORDS if word in full_text
        )

    return {
        "url_web_count": len(web_urls),
        "url_max_len": max(lengths),
        "url_mean_len": round(sum(lengths) / len(lengths), 4),
        "url_total_len": sum(lengths),
        "url_digits_count": digits_count,
        "url_special_count": special_count,
        "url_hyphen_count": hyphen_count,
        "url_dot_count": dot_count,
        "url_at_count": at_count,
        "url_question_count": question_count,
        "url_equal_count": equal_count,
        "url_ampersand_count": ampersand_count,
        "url_percent_count": percent_count,
        "url_slash_count": slash_count,
        "url_subdomain_max": max(subdomain_values) if subdomain_values else 0,
        "url_contains_ip": contains_ip,
        "url_uses_https": uses_https,
        "url_shortener_present": shortener_present,
        "url_suspicious_words_count": suspicious_words_count,
    }


def extract_all_features(value):
    """
    Extrae las 27 características esperadas por el modelo URL e híbrido.
    """
    raw_links = split_raw_links(value)
    web_urls, mailto_links, cid_links, other_links = classify_links(raw_links)

    features = web_features(web_urls)

    features["link_total_detected_count"] = len(raw_links)
    features["link_mailto_count"] = len(mailto_links)
    features["link_cid_count"] = len(cid_links)
    features["link_other_count"] = len(other_links)

    features["has_web_url"] = int(len(web_urls) > 0)
    features["has_mailto"] = int(len(mailto_links) > 0)
    features["has_cid"] = int(len(cid_links) > 0)
    features["has_other_link"] = int(len(other_links) > 0)

    return features


def build_feature_frame(urls_raw: str) -> pd.DataFrame:
    """
    Construye un DataFrame de una fila con las 27 columnas exactas
    utilizadas durante el entrenamiento.

    Este DataFrame es el que debe recibir el modelo URL.
    """
    features = extract_all_features(urls_raw)
    row = {col: features.get(col, 0) for col in URL_FEATURES}

    df = pd.DataFrame([row], columns=URL_FEATURES)

    # Asegurar valores numéricos.
    for col in URL_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def build_hybrid_frame(text: str, urls_raw: str) -> pd.DataFrame:
    """
    Construye el DataFrame que debe recibir el modelo híbrido:
    columna text + las 27 características URL/enlaces.
    """
    url_df = build_feature_frame(urls_raw)
    hybrid_df = url_df.copy()
    hybrid_df.insert(0, "text", safe_text(text))

    return hybrid_df


def summarize_features(urls_raw: str) -> dict:
    """
    Retorna un resumen simple de señales para mostrar en la interfaz.
    """
    features = extract_all_features(urls_raw)

    return {
        "URL web detectadas": features.get("url_web_count", 0),
        "Enlaces totales detectados": features.get("link_total_detected_count", 0),
        "Enlaces mailto": features.get("link_mailto_count", 0),
        "Referencias cid": features.get("link_cid_count", 0),
        "Otros enlaces": features.get("link_other_count", 0),
        "Longitud máxima de URL": features.get("url_max_len", 0),
        "Subdominios máximos": features.get("url_subdomain_max", 0),
        "Contiene IP": "Sí" if features.get("url_contains_ip", 0) else "No",
        "Usa HTTPS": "Sí" if features.get("url_uses_https", 0) else "No",
        "Acortador detectado": "Sí" if features.get("url_shortener_present", 0) else "No",
        "Palabras sospechosas en URL": features.get("url_suspicious_words_count", 0),
    }
