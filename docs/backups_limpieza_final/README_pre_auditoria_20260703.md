# PhishGuard Antares

PhishGuard Antares es un prototipo académico local desarrollado en Python y Streamlit para estimar si un mensaje, correo o enlace presenta patrones compatibles con phishing.

El sistema forma parte de una tesis de pregrado en Ingeniería Informática sobre detección de phishing en español latinoamericano mediante aprendizaje automático.

## Características principales

- Análisis local de mensajes y enlaces.
- Tres modelos locales: textual, URL e híbrido.
- Interfaz gráfica en Streamlit.
- No visita enlaces.
- No abre URLs.
- No consulta APIs externas.
- Genera reportes TXT con enlaces neutralizados.
- Permite comparar los tres modelos.
- Incluye evidencias técnicas en docs/evidencias_ubuntu/.

## Estructura principal

phishguard-antares/
- app.py
- models/
- src/
- docs/
- assets/
- outputs/
- tests/
- requirements.txt
- README.md

## Requisitos

- Python 3.14 o superior.
- Ubuntu o Windows.
- Entorno virtual recomendado.
- Dependencias incluidas en requirements.txt.

## Ejecución en Ubuntu

Desde la carpeta del proyecto:

source .venv_ubuntu/bin/activate

python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501

Luego abrir en el navegador:

http://127.0.0.1:8501

## Evidencias de validación

El software fue validado en Ubuntu mediante:

- Compilación del código Python.
- Carga correcta de los tres modelos .joblib.
- Ejecución local de Streamlit.
- Pruebas funcionales con casos sospechosos y legítimos.
- Reportes TXT con neutralización de enlaces.
- Auditorías funcionales automáticas.
- Checklist de pruebas cerrado con dictamen apto para evidencia y defensa.

Las evidencias se encuentran en:

docs/evidencias_ubuntu/

## Limitaciones

Este software es un prototipo académico. Sus resultados son orientativos y no sustituyen herramientas profesionales de ciberseguridad.

## Seguridad

PhishGuard Antares procesa las entradas de forma local. Las URL se tratan como texto y no son visitadas, abiertas ni consultadas mediante servicios externos.
