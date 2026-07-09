# Dataset multi-fuente V3 — PhishGuard Antares

## Propósito

Este documento describe la integración multi-fuente utilizada en PhishGuard Antares V3.0 Multidataset. La finalidad fue ampliar la base técnica del prototipo académico mediante fuentes complementarias para análisis textual y análisis URL.

## Fuentes utilizadas

| Fuente | Rol metodológico | Uso dentro del sistema |
|---|---|---|
| SpaPhish | Correos en español etiquetados | Entrenamiento textual |
| SpearPhishMX | Correos dirigidos en español etiquetados | Entrenamiento textual |
| PhishTank | URLs verificadas como phishing | Entrenamiento URL |
| Tranco | Dominios populares de control | Clase legítima/control para entrenamiento URL |

## Composición final normalizada

### Componente textual

- Total de registros textuales: **4401**
- Distribución por fuente: `{'spaphish': 1395, 'spearphishmx': 3006}`
- Distribución por etiqueta: `{'phishing': 2622, 'legitimo': 1779}`

### Componente URL

- Total de registros URL: **129284**
- Distribución por fuente: `{'phishtank': 64642, 'tranco': 64642}`
- Distribución por etiqueta: `{'phishing': 64642, 'legitimo_control': 64642}`

## Total técnico normalizado

El proceso técnico trabajó con:

- **4401** registros textuales.
- **129284** registros URL.
- **133685** registros normalizados en total.

## Aclaración metodológica importante

No debe afirmarse que el sistema fue entrenado con 133685 correos. La redacción correcta es que se trabajó con **4401 correos o mensajes textuales** y **129284 registros URL**.

## Tamaño físico de carpetas

El tamaño físico de las carpetas no representa directamente la cantidad de registros utilizados en el entrenamiento. Algunas fuentes, como SpaPhish, incluyen documentación complementaria, reportes HTML, figuras, archivos EPS, esquemas, tablas auxiliares y archivos comprimidos. Para el procesamiento computacional se utilizaron los archivos tabulares normalizados.

## Seguridad

Las URLs fueron tratadas como texto. El software no visita enlaces, no abre URLs y no consulta servicios externos.
