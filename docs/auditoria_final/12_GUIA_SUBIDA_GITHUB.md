# 12 — Guía de Subida a GitHub

Procedimiento verificado para publicar el proyecto auditado. El `.gitignore` ya fue corregido en esta auditoría (H3) y protege contra subir entornos virtuales, cachés y empaquetados.

## 0. Decisiones previas (1 minuto)

- **Visibilidad:** para una tesis en curso suele convenir un repositorio **privado** (con acceso otorgado a tutores) hasta la defensa; puede hacerse público después. Ambas opciones funcionan igual con esta guía.
- **Nombre sugerido:** `phishguard-antares`.
- **Tamaño:** el proyecto pesa ~35 MB con evidencias y capturas; el archivo más grande es de 4,2 MB. Está muy por debajo de los límites de GitHub (100 MB por archivo), por lo que **no** se requiere Git LFS.
- **Licencia:** decisión personal/institucional del tesista; si se desea, GitHub permite añadirla luego desde la web ("Add file → Create new file → LICENSE").

## 1. Crear el repositorio vacío en GitHub

1. Iniciar sesión en github.com → botón **New repository**.
2. Nombre: `phishguard-antares`. Descripción sugerida: `Prototipo académico local de detección de phishing en español latinoamericano (tesis de Ingeniería Informática). Streamlit + scikit-learn. 100% local, sin visitar URLs.`
3. Visibilidad: Private (recomendado hasta la defensa) o Public.
4. **Importante:** NO marcar "Add a README", ni .gitignore, ni licencia (el proyecto ya los trae; evitará conflictos en el primer push).
5. Crear y copiar la URL del repositorio.

## 2. Publicar desde la carpeta del proyecto (terminal)

Desde la raíz `phishguard-antares/` (la carpeta que contiene `app.py`):

```bash
# Identidad de git (una sola vez por máquina; use su nombre y su correo de GitHub)
git config --global user.name "Su Nombre"
git config --global user.email "su-correo@ejemplo.com"

# Inicializar y confirmar
git init
git add .
git status          # verificar: NO deben aparecer .venv*, __pycache__ ni *.7z
git commit -m "PhishGuard Antares v2.0 — versión auditada y optimizada (auditoría 03/07/2026)"
git branch -M main

# Conectar y subir (elija HTTPS o SSH según su configuración)
git remote add origin https://github.com/SU_USUARIO/phishguard-antares.git
git push -u origin main
```

**Autenticación HTTPS:** GitHub ya no acepta contraseña; al pedir credenciales use un *Personal Access Token* (github.com → Settings → Developer settings → Personal access tokens → *Generate new token (classic)* con alcance `repo`) como contraseña. Alternativa: `gh auth login` si tiene GitHub CLI, o llaves SSH.

## 3. Verificación posterior al push (2 minutos)

1. En GitHub, confirmar que el README se muestra como portada.
2. Confirmar presencia de: `app.py`, `src/`, `models/` (3 `.joblib`), `tests/`, `docs/auditoria_final/` (13 documentos), `docs/evidencias_ubuntu/`.
3. Confirmar **ausencia** de: `.venv*/`, `__pycache__/`, archivos `.7z`.
4. Opcional: en *About* del repo añadir *topics*: `phishing-detection`, `machine-learning`, `streamlit`, `scikit-learn`, `spanish`, `cybersecurity-education`, `thesis`.

## 4. Trabajo futuro (buenas prácticas)

```bash
git add -A
git commit -m "Descripción breve y honesta del cambio"
git push
```

- Un commit por cambio lógico; nunca commitear `.venv*` ni artefactos.
- Antes de cada push: `python -m unittest discover -s tests` en verde.
- Si algún día se reentrenan modelos: versionar como archivos nuevos y actualizar doc 05 + README, preservando los actuales como evidencia.

## 5. Clonación por terceros (tutores/tribunal)

```bash
git clone https://github.com/SU_USUARIO/phishguard-antares.git
cd phishguard-antares
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```
