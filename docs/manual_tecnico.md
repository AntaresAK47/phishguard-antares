# Manual Técnico — PhishGuard Antares

**Sistema:** PhishGuard Antares  
**Versión funcional documentada:** 2.0  
**Tipo de documento:** Manual técnico de instalación, arquitectura, operación y mantenimiento  
**Ámbito:** Prototipo académico local de aprendizaje automático aplicado a la detección de phishing  
**Estado:** Versión dorada del prototipo  

---

## Control del documento

| Campo | Descripción |
|---|---|
| Nombre del sistema | PhishGuard Antares |
| Versión del sistema | 2.0 |
| Documento | Manual Técnico |
| Audiencia | Tesista, tutor, jurado, desarrolladores, revisores técnicos y responsables de soporte |
| Finalidad | Documentar arquitectura, dependencias, modelos, inferencia, seguridad, pruebas y mantenimiento |
| Modalidad | Ejecución local mediante Streamlit |
| Clasificación | Evidencia técnica académica |

---

## 1. Introducción

PhishGuard Antares es un prototipo académico de clasificación binaria que integra modelos de aprendizaje automático entrenados para estimar si un mensaje presenta patrones compatibles con phishing. El sistema dispone de tres enfoques:

- clasificación basada en contenido textual;
- clasificación basada en 27 características de URL y enlaces;
- clasificación híbrida basada en texto y características URL.

La aplicación se ejecuta localmente, carga modelos persistidos en formato `.joblib`, recibe nuevas entradas desde una interfaz Streamlit y genera una salida interpretable para usuarios comunes y técnicos.

La finalidad del prototipo es demostrar la aplicación práctica del componente computacional de la investigación. No fue diseñado como servicio comercial, gateway de correo, antivirus, sandbox, motor de reputación ni sustituto de plataformas profesionales de ciberseguridad.

---

## 2. Objetivos técnicos

### 2.1 Objetivo general

Implementar una aplicación local, reproducible y auditable que permita aplicar modelos textual, URL e híbrido a nuevas entradas y presentar sus resultados de manera comprensible y técnicamente trazable.

### 2.2 Objetivos específicos

- cargar los tres modelos entrenados desde archivos `.joblib`;
- validar las entradas requeridas por cada modelo;
- reutilizar la misma estructura de características empleada durante el entrenamiento;
- generar exactamente 27 características URL/enlaces en el orden esperado;
- ejecutar predicción binaria y estimación de probabilidad;
- presentar clase, probabilidad y nivel orientativo de riesgo;
- permitir comparación entre modelos;
- mostrar señales técnicas y vectores de entrada;
- generar reportes locales neutralizados;
- evitar visitas a URL y llamadas a APIs externas;
- conservar evidencia técnica para la tesis.

---

## 3. Alineación con la investigación

El software cumple una función demostrativa y aplicada dentro de la tesis:

- materializa el análisis textual mediante el modelo textual;
- materializa el análisis léxico de URL mediante el modelo URL;
- materializa la integración de ambas dimensiones mediante el modelo híbrido;
- permite comparar los enfoques evaluados en la investigación;
- proporciona evidencia visual y técnica para anexos y defensa;
- mantiene separada la fase de entrenamiento de la fase de inferencia.

El dataset no se carga como base viva durante cada predicción. Su función fue entrenar y evaluar los modelos. En la aplicación final, el conocimiento aprendido se encuentra representado en los archivos `.joblib`.

---

## 4. Arquitectura general

### 4.1 Vista lógica

```text
Usuario
  │
  ▼
Interfaz Streamlit (app.py)
  │
  ├── Validación de entrada
  ├── Selección de modelo
  ├── Control de sesión y modal
  │
  ▼
Orquestador de inferencia (src/predictor.py)
  │
  ├── Entrada textual
  ├── Entrada URL/enlaces
  ├── Carga de modelo .joblib
  │
  ├───────────────┬──────────────────┐
  ▼               ▼                  ▼
Modelo textual    Modelo URL         Modelo híbrido
TF-IDF + LR       27 features + LR   TF-IDF + 27 features + LR
  │               │                  │
  └───────────────┴──────────────────┘
                  │
                  ▼
Resultado normalizado
  │
  ├── Clase estimada
  ├── Probabilidad phishing
  ├── Nivel orientativo
  ├── Señales técnicas
  ├── Vector de características
  └── Reporte TXT neutralizado
```

### 4.2 Capas del sistema

| Capa | Responsabilidad | Archivos principales |
|---|---|---|
| Presentación | Interfaz, navegación, entradas, loader, resultados, modal | `app.py`, `src/ui_theme.py` |
| Configuración | Rutas, nombres, etiquetas y versión | `src/config.py` |
| Inferencia | Carga de modelos, preparación de entradas y predicción | `src/predictor.py` |
| Características | Detección de enlaces y extracción de 27 variables | `src/url_features.py` |
| Interpretación | Etiquetas y escala visual orientativa | `src/risk_rules.py` |
| Reportes | Generación de informe TXT y neutralización | `src/report_builder.py` |
| Persistencia del modelo | Parámetros aprendidos | `models/*.joblib` |
| Configuración Streamlit | Tema oscuro, servidor y barra de herramientas | `.streamlit/config.toml` |

---

## 5. Estructura de directorios

```text
PHISHGUARD_ANTARES_FINAL/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── logo.png
│   └── screenshots/
│
├── docs/
│   ├── manual_usuario.md
│   ├── manual_tecnico.md
│   ├── checklist_pruebas.md
│   └── archivos de inventario/estructura
│
├── models/
│   ├── modelo_textual.joblib
│   ├── modelo_url.joblib
│   └── modelo_hibrido.joblib
│
├── outputs/
│   ├── logs/
│   └── reports/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── predictor.py
│   ├── report_builder.py
│   ├── risk_rules.py
│   ├── ui_theme.py
│   └── url_features.py
│
└── tests/
```

### 5.1 Descripción de archivos críticos

#### `app.py`

Punto de entrada de la aplicación. Controla:

- configuración de página;
- renderizado del centro de mando;
- selección de modelo;
- campos de entrada;
- validación;
- animación de carga;
- ejecución simple o comparativa;
- modal de resultado;
- persistencia temporal de sesión;
- análisis avanzado;
- descarga de reportes.

#### `src/ui_theme.py`

Contiene el CSS integral de la interfaz:

- paleta de colores;
- tipografía;
- distribución visual;
- centro de mando;
- botones;
- loader;
- tarjetas;
- modal;
- tablas;
- adaptaciones responsivas.

#### `src/config.py`

Centraliza:

- raíz del proyecto;
- directorios de modelos y salidas;
- rutas de los modelos;
- nombres de visualización;
- etiquetas positiva y negativa;
- nombre, subtítulo y versión del sistema.

#### `src/predictor.py`

Implementa:

- normalización del nombre de modelo;
- carga en caché de archivos `.joblib`;
- construcción de entrada textual;
- construcción de entrada URL;
- extracción de probabilidad positiva;
- ejecución de cada modelo;
- normalización del resultado final.

#### `src/url_features.py`

Implementa:

- reconocimiento de URL web;
- detección de `mailto:` y `cid:`;
- normalización de enlaces neutralizados;
- clasificación de tipos de enlace;
- cálculo de 27 características;
- construcción de `DataFrame` URL e híbrido;
- resumen de señales para la interfaz.

#### `src/risk_rules.py`

Transforma la probabilidad en:

- etiqueta visual de riesgo;
- color;
- mensaje explicativo;
- recomendación para el usuario.

La escala es didáctica y no una calibración formal.

#### `src/report_builder.py`

Genera reportes TXT descargables. Neutraliza las URL para reducir aperturas accidentales y no escribe archivos automáticamente.

---

## 6. Tecnologías y dependencias

### 6.1 Tecnologías principales

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Interfaz web local |
| pandas | Construcción y visualización de estructuras tabulares |
| NumPy | Soporte numérico indirecto de modelos y dependencias |
| scikit-learn | Pipelines, vectorización, escalado y clasificación |
| joblib | Serialización y carga de modelos |
| Matplotlib | Dependencia disponible para recursos gráficos y compatibilidad del proyecto |

### 6.2 Dependencias mínimas declaradas

```text
streamlit
pandas
numpy
scikit-learn
joblib
matplotlib
```

### 6.3 Compatibilidad de modelos

Los archivos `.joblib` fueron serializados con componentes de scikit-learn. Para máxima reproducibilidad se recomienda:

- conservar el archivo `dependencias_instaladas_windows.txt` generado como evidencia;
- utilizar el mismo entorno o las mismas versiones utilizadas al congelar la versión dorada;
- mantener scikit-learn compatible con la versión de serialización observada en los modelos;
- no cargar archivos `.joblib` provenientes de fuentes no confiables.

**Versión de serialización observada en los artefactos:** scikit-learn 1.9.0.

> Los objetos serializados con joblib/pickle pueden ejecutar código durante su carga. Solo deben utilizarse los tres modelos oficiales conservados en la versión dorada y verificados mediante la cadena de custodia del proyecto.

---

## 7. Modelos de aprendizaje automático

### 7.1 Convención de clases

| Clase | Valor | Interpretación |
|---|---:|---|
| Legítimo | 0 | Registro estimado como legítimo |
| Phishing | 1 | Registro estimado como phishing |

La probabilidad mostrada corresponde a la clase positiva `1 = phishing`.

### 7.2 Modelo textual

**Archivo:** `models/modelo_textual.joblib`

**Pipeline:**

1. `TfidfVectorizer`
2. `LogisticRegression`

**Parámetros observados:**

- n-gramas: `(1, 2)`;
- máximo de características: `8000`;
- frecuencia mínima documental: `2`;
- normalización de acentos: `unicode`;
- ponderación sublineal TF: activada;
- regresión logística: `max_iter=1000`;
- solver: `lbfgs`;
- `random_state=42`.

**Entrada:** serie de pandas con asunto y cuerpo concatenados.

### 7.3 Modelo URL

**Archivo:** `models/modelo_url.joblib`

**Pipeline:**

1. `StandardScaler`
2. `LogisticRegression`

**Parámetros observados:**

- escalado con media y desviación estándar;
- regresión logística: `max_iter=1000`;
- solver: `lbfgs`;
- `random_state=42`.

**Entrada:** `DataFrame` de una fila con las 27 características URL en orden fijo.

### 7.4 Modelo híbrido

**Archivo:** `models/modelo_hibrido.joblib`

**Pipeline:**

1. `ColumnTransformer` para integrar:
   - columna `text` mediante `TfidfVectorizer`;
   - 27 columnas URL mediante `StandardScaler`;
2. `LogisticRegression`.

**Configuración textual:** equivalente al modelo textual:

- n-gramas `(1, 2)`;
- máximo `8000` características;
- `min_df=2`;
- `strip_accents='unicode'`;
- `sublinear_tf=True`.

**Clasificador:**

- `max_iter=1000`;
- solver `lbfgs`;
- `random_state=42`.

**Entrada:** `DataFrame` con columna `text` seguida de las 27 variables URL.

---

## 8. Características URL/enlaces

### 8.1 Regla de compatibilidad

El orden, nombre y tipo de las 27 columnas deben coincidir exactamente con el entrenamiento. Una modificación arbitraria puede producir errores, incompatibilidad o predicciones no válidas.

### 8.2 Diccionario de características

| Nº | Variable | Tipo | Descripción operativa |
|---:|---|---|---|
| 1 | `url_web_count` | Numérica | Cantidad de URL web reconocidas |
| 2 | `url_max_len` | Numérica | Longitud máxima entre las URL detectadas |
| 3 | `url_mean_len` | Numérica | Longitud promedio de las URL |
| 4 | `url_total_len` | Numérica | Suma de longitudes de todas las URL |
| 5 | `url_digits_count` | Numérica | Total de caracteres numéricos |
| 6 | `url_special_count` | Numérica | Conteo de caracteres especiales definidos por el extractor |
| 7 | `url_hyphen_count` | Numérica | Cantidad de guiones `-` |
| 8 | `url_dot_count` | Numérica | Cantidad de puntos `.` |
| 9 | `url_at_count` | Numérica | Cantidad de símbolos `@` |
| 10 | `url_question_count` | Numérica | Cantidad de signos `?` |
| 11 | `url_equal_count` | Numérica | Cantidad de signos `=` |
| 12 | `url_ampersand_count` | Numérica | Cantidad de símbolos `&` |
| 13 | `url_percent_count` | Numérica | Cantidad de símbolos `%` |
| 14 | `url_slash_count` | Numérica | Cantidad de barras `/` |
| 15 | `url_subdomain_max` | Numérica | Máximo aproximado de subdominios |
| 16 | `url_contains_ip` | Binaria | Indica si alguna URL utiliza una IP como host |
| 17 | `url_uses_https` | Binaria | Indica si se detectó al menos una URL HTTPS |
| 18 | `url_shortener_present` | Binaria | Indica presencia de un acortador conocido |
| 19 | `url_suspicious_words_count` | Numérica | Conteo de palabras definidas como señales sospechosas |
| 20 | `link_total_detected_count` | Numérica | Total de elementos tipo enlace reconocidos |
| 21 | `link_mailto_count` | Numérica | Cantidad de referencias `mailto:` |
| 22 | `link_cid_count` | Numérica | Cantidad de referencias `cid:` |
| 23 | `link_other_count` | Numérica | Cantidad de enlaces o referencias no clasificadas |
| 24 | `has_web_url` | Binaria | Presencia de al menos una URL web |
| 25 | `has_mailto` | Binaria | Presencia de al menos una referencia `mailto:` |
| 26 | `has_cid` | Binaria | Presencia de al menos una referencia `cid:` |
| 27 | `has_other_link` | Binaria | Presencia de otros enlaces |

### 8.3 Tipos de enlace reconocidos

- `http://`
- `https://`
- `hxxp://`
- `hxxps://`
- `www.`
- `mailto:`
- `cid:`
- dominios simples;
- dominios neutralizados con `[.]`;
- listas de enlaces representadas como texto.

### 8.4 Palabras consideradas señales URL

El extractor contempla términos en español e inglés asociados a autenticación, seguridad, actualización, bloqueo, banco, cuenta, contraseña, verificación, soporte y token. Su presencia se considera una señal cuantitativa, no una prueba concluyente de phishing.

### 8.5 Acortadores reconocidos

La lista incluye dominios como `bit.ly`, `tinyurl.com`, `t.co`, `ow.ly`, `is.gd`, `cutt.ly`, `rebrand.ly` y otros definidos en el módulo.

---

## 9. Flujo de inferencia

### 9.1 Preparación textual

```text
texto = asunto + salto de línea + cuerpo
```

Los valores se convierten a texto seguro y se eliminan espacios exteriores.

### 9.2 Preparación URL

1. Se incorpora el campo manual de URL si fue proporcionado.
2. Se revisa el asunto/cuerpo únicamente para añadirlo cuando contiene señales reales de enlace.
3. Se extraen y clasifican las referencias detectadas.
4. Se calculan las 27 características.

### 9.3 Carga del modelo

- El nombre del modelo se normaliza.
- La ruta se obtiene desde `src/config.py`.
- El archivo se carga con `joblib.load`.
- Se utiliza caché LRU con máximo de tres modelos para evitar cargas repetidas durante la sesión.

### 9.4 Predicción

1. El modelo ejecuta `predict` para obtener la clase.
2. Si está disponible, ejecuta `predict_proba`.
3. Se localiza la probabilidad correspondiente a la clase positiva `1`.
4. Se construye un diccionario de resultado uniforme.

### 9.5 Resultado estándar

El resultado contiene:

```text
modelo
modelo_nombre
label_predicho
clase_predicha
probabilidad_phishing
probabilidad_formato
nivel_riesgo
mensaje_riesgo
texto_usado
enlaces_usados
features
feature_summary
```

---

## 10. Escala de riesgo

| Probabilidad | Nivel | Color de referencia |
|---:|---|---|
| 0 a < 0,05 | Muy bajo | Verde |
| 0,05 a < 0,15 | Bajo | Verde claro |
| 0,15 a < 0,35 | Precaución | Amarillo |
| 0,35 a < 0,50 | Moderado | Naranja |
| 0,50 a < 0,70 | Alto | Naranja rojizo |
| 0,70 a < 0,85 | Muy alto | Fucsia/carmesí |
| 0,85 a 1,00 | Crítico | Rojo |

La clasificación binaria proviene del modelo. La escala de riesgo es una capa narrativa y visual adicional destinada a facilitar la comprensión del usuario.

---

## 11. Interfaz y estado de sesión

### 11.1 Configuración de página

La aplicación usa:

- título de página basado en `APP_NAME`;
- diseño ancho;
- panel nativo de Streamlit colapsado;
- interfaz personalizada mediante columnas y CSS.

### 11.2 Centro de mando

El panel lateral personalizado conserva en `st.session_state`:

- estado abierto/cerrado;
- modelo seleccionado;
- opción de comparación;
- opción de análisis avanzado.

Se utilizan claves persistentes para evitar que Streamlit elimine valores cuando los widgets dejan de renderizarse.

### 11.3 Animación de carga

El loader recorre valores de 0 a 100 con pausa aproximada de 0,045 segundos por incremento, más una pausa final. Su duración visual aproximada es de 4,9 a 5 segundos.

La animación no representa actividad de red; comunica etapas de procesamiento local.

### 11.4 Modal y fallback

Si la versión de Streamlit dispone de `st.dialog`, el resultado se presenta como ventana modal. En caso contrario, el contenido se renderiza dentro de la página.

### 11.5 Persistencia temporal

La última predicción se conserva en `st.session_state` y puede reabrirse sin recalcular. No se persiste automáticamente en disco.

---

## 12. Reportes

### 12.1 Generación

Los reportes se generan en memoria mediante `build_report_text`. Solo se escriben en el equipo cuando el usuario utiliza el botón de descarga del navegador.

### 12.2 Neutralización

- `https://` → `hxxps://`
- `http://` → `hxxp://`
- `www.` → `www[.]`

### 12.3 Contenido del reporte

- fecha y hora;
- modelo;
- clase;
- probabilidad;
- nivel de riesgo;
- mensaje interpretativo;
- señales técnicas;
- comparación, si corresponde;
- entrada neutralizada;
- advertencia.

---

## 13. Instalación

### 13.1 Recomendación previa

Trabajar siempre sobre una copia del proyecto. No modificar la versión dorada ni sus hashes.

### 13.2 Windows

```powershell
cd "<ruta_del_proyecto>\PHISHGUARD_ANTARES_FINAL"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### 13.3 Ubuntu/Linux

```bash
cd "<ruta_del_proyecto>/PHISHGUARD_ANTARES_FINAL"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### 13.4 Instalación reproducible recomendada

Para replicar exactamente el entorno de la versión documentada:

1. consulte `dependencias_instaladas_windows.txt`;
2. use las versiones allí registradas;
3. preserve la versión de scikit-learn compatible con los modelos;
4. verifique la carga de los tres `.joblib` antes de ejecutar pruebas.

---

## 14. Ejecución y verificación

### 14.1 Verificación de sintaxis

```powershell
python -m py_compile app.py src\ui_theme.py src\predictor.py src\url_features.py src\risk_rules.py src\report_builder.py src\config.py
```

Ubuntu/Linux:

```bash
python -m py_compile app.py src/ui_theme.py src/predictor.py src/url_features.py src/risk_rules.py src/report_builder.py src/config.py
```

Una ejecución sin salida y con código de retorno cero indica que no se detectaron errores de sintaxis.

### 14.2 Verificación de modelos

```powershell
python -c "from src.config import validate_model_files; print(validate_model_files())"
```

Resultado esperado:

```text
{'textual': True, 'url': True, 'hibrido': True}
```

### 14.3 Verificación de características

```powershell
python -c "from src.url_features import build_feature_frame; df=build_feature_frame('https://secure-login.example.com/verify?token=123'); print(df.shape)"
```

Resultado esperado:

```text
(1, 27)
```

### 14.4 Ejecución

```powershell
python -m streamlit run app.py
```

Dirección habitual:

```text
http://localhost:8501
```

---

## 15. Resultados técnicos de referencia

La muestra técnica final estuvo compuesta por 1.000 registros balanceados:

- 500 legítimos;
- 500 phishing;
- 800 registros para entrenamiento;
- 200 registros para prueba;
- 100 legítimos y 100 phishing en el subconjunto de prueba.

### 15.1 Métricas de referencia

| Modelo | Accuracy | Precisión | Recall | F1-score | VN | FP | FN | VP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Textual | 94,0 % | 100,00 % | 88,0 % | 93,62 % | 100 | 0 | 12 | 88 |
| URL | 72,5 % | 68,29 % | 84,0 % | 75,34 % | 61 | 39 | 16 | 84 |
| Híbrido | 92,5 % | 95,70 % | 89,0 % | 92,23 % | 96 | 4 | 11 | 89 |

### 15.2 Interpretación técnica correcta

- El modelo textual obtuvo el mejor desempeño global en accuracy, precisión y F1-score.
- El modelo híbrido presentó desempeño cercano al textual y redujo los falsos negativos de 12 a 11.
- El modelo URL tuvo menor desempeño global y más falsos positivos.
- El software no debe afirmar que el modelo híbrido fue superior en todas las métricas.
- La utilidad del enfoque híbrido radica en integrar dos dimensiones de análisis y mejorar ligeramente la detección de phishing respecto al textual en recall/falsos negativos.

---

## 16. Seguridad y privacidad por diseño

### 16.1 Controles implementados

- No se importan bibliotecas para realizar solicitudes HTTP en la ruta de inferencia.
- Las URL se procesan como cadenas de texto.
- No se realizan consultas a APIs externas.
- Los modelos se cargan desde archivos locales.
- No se guarda automáticamente el contenido ingresado.
- Los reportes se generan únicamente por acción del usuario.
- Las URL se neutralizan en el reporte.
- El sistema informa que el resultado es orientativo.

### 16.2 Riesgos residuales

- exposición de datos sensibles si el usuario los copia manualmente;
- descarga insegura del reporte en una ubicación compartida;
- ejecución de modelos joblib adulterados;
- incompatibilidad de versiones;
- falsa confianza por una probabilidad baja;
- reacción excesiva ante un falso positivo;
- interpretación incorrecta de HTTPS como legitimidad.

### 16.3 Medidas administrativas recomendadas

- trabajar con ejemplos anonimizados;
- preservar el hash de la versión dorada;
- restringir modificación de los modelos;
- documentar cualquier actualización;
- no publicar mensajes reales con datos identificables;
- ejecutar el sistema en un entorno controlado;
- mantener copias de seguridad separadas.

---

## 17. Limitaciones técnicas

- No consulta reputación de dominios.
- No inspecciona DNS, WHOIS o antigüedad del dominio.
- No valida certificados TLS.
- No analiza redirecciones.
- No visita el contenido de páginas.
- No analiza adjuntos.
- No detecta malware.
- No integra correo en tiempo real.
- No realiza aprendizaje continuo.
- No calibra formalmente la escala visual de riesgo.
- No garantiza generalización a todas las campañas de phishing.
- Puede verse afectado por cambios lingüísticos y tácticas nuevas.
- El modelo URL puede producir falsos positivos con enlaces legítimos complejos.
- La compatibilidad de `.joblib` depende de versiones de biblioteca.

---

## 18. Mantenimiento

### 18.1 Reemplazo del logotipo

1. Prepare una imagen PNG con transparencia.
2. Mantenga el nombre `logo.png`.
3. Reemplace `assets/logo.png` en una copia de trabajo.
4. Ejecute la aplicación y verifique encabezado y centro de mando.
5. Genere un nuevo backup y hash si el cambio se incorpora a una versión oficial.

### 18.2 Reemplazo de modelos

No sustituir modelos sin:

- documentar el dataset y versión;
- reproducir el preprocesamiento;
- conservar exactamente las 27 columnas URL;
- volver a evaluar métricas;
- actualizar el manual técnico;
- ejecutar el checklist completo;
- incrementar la versión del sistema;
- generar nueva versión dorada y hash.

### 18.3 Modificación de características URL

Cualquier cambio en nombres, orden o semántica exige reentrenamiento. No debe modificarse únicamente la inferencia manteniendo modelos anteriores.

### 18.4 Actualización de dependencias

1. Cree un entorno nuevo.
2. Instale versiones candidatas.
3. Pruebe carga de los modelos.
4. Ejecute regresión con casos conocidos.
5. Compare probabilidades con la versión dorada.
6. Documente cambios.
7. No reemplace el entorno estable hasta concluir las pruebas.

---

## 19. Solución de problemas

### 19.1 `ModuleNotFoundError`

**Causa:** dependencia no instalada o entorno incorrecto.  
**Solución:** active `.venv` y ejecute `python -m pip install -r requirements.txt`.

### 19.2 `FileNotFoundError` del modelo

**Causa:** falta un archivo dentro de `models/`.  
**Solución:** restaure los tres modelos oficiales desde el backup dorado.

### 19.3 Error de columnas o forma

**Causa:** las características no coinciden con el entrenamiento.  
**Solución:** verifique `URL_FEATURES`, su orden y `build_feature_frame`.

### 19.4 Advertencia de versión de scikit-learn

**Causa:** el modelo fue serializado con otra versión.  
**Solución:** utilice el entorno documentado o instale la versión compatible; no ignore la advertencia en una validación formal.

### 19.5 Puerto 8501 ocupado

```powershell
python -m streamlit run app.py --server.port 8502
```

### 19.6 El modal no aparece

Puede deberse a una versión de Streamlit sin `st.dialog`. La aplicación incluye una salida alternativa dentro de la página. Para reproducir la interfaz documentada use la versión registrada en las evidencias.

### 19.7 El reporte no se guarda

El reporte se descarga mediante el navegador. Revise la carpeta de descargas y permisos del navegador.

---

## 20. Pruebas y criterios de aceptación

El software se considera aceptable para la tesis cuando:

- compila sin errores de sintaxis;
- carga los tres modelos;
- produce una matriz de una fila y 27 columnas URL;
- ejecuta predicción textual;
- ejecuta predicción URL;
- ejecuta predicción híbrida;
- ejecuta comparación de modelos;
- presenta clase y probabilidad;
- muestra escala de riesgo;
- presenta modal y resultado persistente;
- permite análisis avanzado;
- genera reporte TXT neutralizado;
- abre y cierra el centro de mando;
- no visita URL;
- no consulta servicios externos;
- funciona en los entornos Windows y Ubuntu documentados;
- cuenta con evidencias, manuales, backup e integridad SHA-256.

La ejecución detallada se documenta en `checklist_pruebas.md`.

---

## 21. Reproducibilidad e integridad

La versión dorada debe conservar:

- archivo `.7z` del proyecto;
- hash SHA-256;
- inventario del contenido;
- salida de compilación;
- listado de dependencias;
- capturas;
- video;
- reportes;
- manual de usuario;
- manual técnico;
- checklist de pruebas.

El hash permite comprobar si el archivo comprimido fue alterado. Una nueva modificación del código, logo, modelos o documentación requiere generar un nuevo paquete y un nuevo hash.

---

## 22. Integración como evidencia de tesis

Los productos técnicos del software pueden utilizarse como:

- evidencia del procedimiento adoptado;
- demostración de implementación del modelo;
- soporte para presentación de resultados;
- evidencia de reproducibilidad;
- material de anexo;
- apoyo visual durante la defensa;
- base para explicar limitaciones y trabajo futuro.

Las métricas del entrenamiento y prueba pertenecen al análisis de resultados. La interfaz constituye la aplicación práctica y no reemplaza la discusión estadística del Capítulo IV.

---

## 23. Líneas futuras

- integración controlada con sistemas de correo;
- validación externa con corpus adicionales;
- calibración formal de probabilidades;
- análisis de remitente, encabezados y autenticación;
- reputación de dominio mediante servicios autorizados;
- análisis de adjuntos en sandbox;
- explicaciones basadas en importancia de características;
- aprendizaje continuo con revisión experta;
- evaluación de robustez ante evasión;
- empaquetado de escritorio o despliegue institucional;
- monitoreo y registro con políticas de privacidad.

---

## 24. Conclusión técnica

PhishGuard Antares implementa una arquitectura local, modular y auditable que separa presentación, configuración, extracción de características, inferencia, interpretación y reportes. La conservación de la versión dorada, la compatibilidad de las 27 variables URL y la documentación de los modelos son condiciones esenciales para mantener la reproducibilidad. Su uso debe permanecer académico y defensivo, con interpretación prudente de las probabilidades y reconocimiento explícito de sus limitaciones.
