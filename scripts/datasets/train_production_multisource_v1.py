import os, re, json, html, math
from urllib.parse import urlparse
from collections import Counter

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score


TEXT_TRAIN = os.environ["TEXT_TRAIN"]
TEXT_TEST = os.environ["TEXT_TEST"]
URL_TRAIN = os.environ["URL_TRAIN"]
URL_TEST = os.environ["URL_TEST"]
MODEL_DIR = os.environ["MODEL_DIR"]
REPORT = os.environ["REPORT"]
METRICS = os.environ["METRICS"]

SEED = 42


def clean_text(s):
    if pd.isna(s):
        return ""
    return html.unescape(str(s)).strip()


def combine_text(df):
    return (
        df["subject"].fillna("").astype(str) + " " +
        df["body"].fillna("").astype(str) + " " +
        df["urls"].fillna("").astype(str)
    ).map(clean_text)



def deneutralize_url(s):
    if pd.isna(s):
        return ""
    s = html.unescape(str(s))
    s = s.replace("hxxps://", "https://").replace("hxxp://", "http://")
    s = s.replace("[.]", ".")
    s = s.replace("\\/", "/")
    s = s.strip().strip("[]'\"<> .,;")
    return s


def entropy(s):
    if not s:
        return 0.0
    counts = Counter(s)
    n = len(s)
    return -sum((v/n) * math.log2(v/n) for v in counts.values())


SUSPICIOUS_WORDS = [
    "login", "verify", "verification", "account", "secure", "update", "password",
    "bank", "wallet", "confirm", "urgent", "support", "signin", "session",
    "validate", "token", "bonus", "reward", "free", "invoice", "payment",
    "verificar", "cuenta", "seguridad", "urgente", "contraseña", "banco",
    "actualizar", "confirmar", "validar", "premio", "pago"
]

SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "cutt.ly", "rebrand.ly", "shorturl.at"
]

URL_FEATURES = [
    "url_len", "hostname_len", "path_len", "query_len",
    "digits_count", "special_count", "dot_count", "hyphen_count",
    "at_count", "question_count", "equal_count", "ampersand_count",
    "percent_count", "slash_count", "subdomain_count",
    "contains_ip", "uses_https", "suspicious_words_count",
    "shortener_present", "entropy"
]


def url_features_one(url):
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
        "suspicious_words_count": sum(w in full for w in SUSPICIOUS_WORDS),
        "shortener_present": int(any(s in host for s in SHORTENERS)),
        "entropy": entropy(raw),
    }


def url_matrix(urls):
    return pd.DataFrame([url_features_one(u) for u in urls], columns=URL_FEATURES).fillna(0)


def extract_urls_from_field(value):
    s = deneutralize_url(value)
    found = re.findall(r"https?://[^\s,\]'\"]+", s)
    if found:
        return found
    if s and "." in s:
        return [s]
    return []


def url_probability_from_field(value, url_model):
    urls = extract_urls_from_field(value)
    if not urls:
        return 0.5, 0
    probs = url_model.predict_proba(url_matrix(urls))[:, 1]
    return float(np.max(probs)), len(urls)


def metrics_dict(y_true, y_prob):
    y_pred = (y_prob >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


text_train = pd.read_csv(TEXT_TRAIN)
text_test = pd.read_csv(TEXT_TEST)
url_train = pd.read_csv(URL_TRAIN)
url_test = pd.read_csv(URL_TEST)

y_text_train = text_train["label_binary"].astype(int).values
y_text_test = text_test["label_binary"].astype(int).values
y_url_train = url_train["label_binary"].astype(int).values
y_url_test = url_test["label_binary"].astype(int).values

X_text_train = combine_text(text_train)
X_text_test = combine_text(text_test)

text_model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=2,
        max_features=50000
    )),
    ("clf", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
        random_state=SEED
    ))
])

url_model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=SEED
    ))
])

print("Entrenando modelo URL...")
X_url_train = url_matrix(url_train["url"])
X_url_test = url_matrix(url_test["url"])
url_model.fit(X_url_train, y_url_train)
url_prob_test = url_model.predict_proba(X_url_test)[:, 1]

print("Generando probabilidades OOF del modelo textual...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
text_oof_prob = cross_val_predict(
    clone(text_model),
    X_text_train,
    y_text_train,
    cv=cv,
    method="predict_proba"
)[:, 1]

print("Entrenando modelo textual final...")
text_model.fit(X_text_train, y_text_train)
text_prob_test = text_model.predict_proba(X_text_test)[:, 1]

print("Construyendo modelo de fusión...")
train_url_pairs = [url_probability_from_field(v, url_model) for v in text_train["urls"].fillna("")]
test_url_pairs = [url_probability_from_field(v, url_model) for v in text_test["urls"].fillna("")]

train_url_prob = np.array([p for p, c in train_url_pairs])
test_url_prob = np.array([p for p, c in test_url_pairs])
train_has_url = np.array([1 if c > 0 else 0 for p, c in train_url_pairs])
test_has_url = np.array([1 if c > 0 else 0 for p, c in test_url_pairs])
train_url_count = np.array([c for p, c in train_url_pairs])
test_url_count = np.array([c for p, c in test_url_pairs])

fusion_train = pd.DataFrame({
    "text_prob": text_oof_prob,
    "url_prob": train_url_prob,
    "has_url": train_has_url,
    "url_count": train_url_count
})

fusion_test = pd.DataFrame({
    "text_prob": text_prob_test,
    "url_prob": test_url_prob,
    "has_url": test_has_url,
    "url_count": test_url_count
})

fusion_model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED))
])

fusion_model.fit(fusion_train, y_text_train)
fusion_prob_test = fusion_model.predict_proba(fusion_test)[:, 1]

metrics = {
    "seed": SEED,
    "files": {
        "text_train": TEXT_TRAIN,
        "text_test": TEXT_TEST,
        "url_train": URL_TRAIN,
        "url_test": URL_TEST
    },
    "textual_global": metrics_dict(y_text_test, text_prob_test),
    "url_global": metrics_dict(y_url_test, url_prob_test),
    "fusion_hibrido_global": metrics_dict(y_text_test, fusion_prob_test),
    "dataset_counts": {
        "text_train": int(len(text_train)),
        "text_test": int(len(text_test)),
        "url_train": int(len(url_train)),
        "url_test": int(len(url_test)),
    },
    "feature_sets": {
        "url_features": URL_FEATURES,
        "fusion_features": ["text_prob", "url_prob", "has_url", "url_count"]
    }
}

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(text_model, os.path.join(MODEL_DIR, "modelo_textual_global.joblib"))
joblib.dump({"model": url_model, "feature_names": URL_FEATURES}, os.path.join(MODEL_DIR, "modelo_url_global.joblib"))
joblib.dump({"model": fusion_model, "feature_names": ["text_prob", "url_prob", "has_url", "url_count"]}, os.path.join(MODEL_DIR, "modelo_fusion_hibrido_global.joblib"))

with open(os.path.join(MODEL_DIR, "thresholds.json"), "w", encoding="utf-8") as f:
    json.dump({"default_threshold": 0.5}, f, indent=2, ensure_ascii=False)

with open(METRICS, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)

with open(os.path.join(MODEL_DIR, "model_card.md"), "w", encoding="utf-8") as f:
    f.write("# Model Card — production_multisource_v1\n\n")
    f.write("Modelos entrenados con SpaPhish, SpearPhishMX, PhishTank y Tranco.\n\n")
    f.write("## Uso metodológico\n\n")
    f.write("- Textual global: SpaPhish + SpearPhishMX.\n")
    f.write("- URL global: PhishTank + Tranco.\n")
    f.write("- Fusión híbrida: combina probabilidad textual y probabilidad URL.\n")
    f.write("- Las URLs se procesan como texto; no se visitan enlaces.\n")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write("# Entrenamiento production_multisource_v1 — PhishGuard Antares\n\n")
    for name in ["textual_global", "url_global", "fusion_hibrido_global"]:
        m = metrics[name]
        f.write(f"## {name}\n\n")
        f.write(f"- Accuracy: {m['accuracy']:.4f}\n")
        f.write(f"- Precision: {m['precision']:.4f}\n")
        f.write(f"- Recall: {m['recall']:.4f}\n")
        f.write(f"- F1: {m['f1']:.4f}\n")
        f.write(f"- ROC-AUC: {m['roc_auc']:.4f}\n")
        f.write(f"- TN: {m['tn']} | FP: {m['fp']} | FN: {m['fn']} | TP: {m['tp']}\n\n")

print("RESUMEN ENTRENAMIENTO")
print("=====================")
for name in ["textual_global", "url_global", "fusion_hibrido_global"]:
    print(name, metrics[name])

print()
print("MODELOS_GUARDADOS:", MODEL_DIR)
print("METRICS:", METRICS)
print("REPORT:", REPORT)
