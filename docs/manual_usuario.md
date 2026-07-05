# Manual de Usuario — PhishGuard Antares

**Sistema:** PhishGuard Antares  
**Versión del prototipo:** 2.0  
**Tipo de documento:** Manual de usuario  
**Ámbito de uso:** Académico, demostrativo y defensivo  
**Modalidad de ejecución:** Aplicación web local mediante Streamlit  
**Estado:** Versión dorada del prototipo  

---

## Control del documento

| Campo | Descripción |
|---|---|
| Nombre del sistema | PhishGuard Antares |
| Versión del sistema | 2.0 |
| Documento | Manual de Usuario |
| Público objetivo | Usuarios de servicios digitales, evaluadores académicos, docentes, estudiantes y personal institucional |
| Finalidad | Explicar el uso correcto, seguro e interpretativamente responsable del prototipo |
| Clasificación | Documento académico de apoyo y evidencia técnica |

---

## 1. Presentación

PhishGuard Antares es un prototipo académico local orientado a estimar si un mensaje digital presenta patrones compatibles con phishing. El sistema permite analizar el asunto, el cuerpo del mensaje y las direcciones URL o referencias de enlace asociadas mediante tres modelos de aprendizaje automático previamente entrenados:

1. **Modelo textual:** analiza el asunto y el cuerpo del mensaje.
2. **Modelo URL:** analiza características léxicas y estructurales de URL y enlaces.
3. **Modelo híbrido:** integra el contenido textual con las características de URL y enlaces.

El sistema muestra una clasificación orientativa —**Legítimo probable** o **Phishing probable**—, una probabilidad estimada, un nivel visual de riesgo, señales técnicas resumidas y, cuando corresponde, un análisis avanzado.

> **Advertencia fundamental:** PhishGuard Antares no determina con certeza absoluta que un mensaje sea seguro o fraudulento. Sus resultados son estimaciones producidas por modelos de clasificación y deben complementarse con procedimientos de verificación institucional y buenas prácticas de ciberseguridad.

---

## 2. Propósito del manual

Este manual tiene los siguientes propósitos:

- orientar al usuario durante la apertura y ejecución del sistema;
- explicar la función de cada elemento de la interfaz;
- describir los tres modos de análisis disponibles;
- establecer el procedimiento correcto para analizar un mensaje o enlace;
- facilitar la interpretación responsable de los resultados;
- explicar la consulta del análisis avanzado y la descarga de reportes;
- prevenir usos incorrectos o conclusiones exageradas;
- documentar las limitaciones y medidas de seguridad del prototipo.

---

## 3. Alcance funcional

PhishGuard Antares puede:

- recibir un asunto y un cuerpo de mensaje;
- recibir una o varias URL o referencias de enlace;
- reconocer URL web, referencias `mailto:`, referencias `cid:` y otros elementos de enlace;
- ejecutar el modelo textual, URL o híbrido;
- comparar los tres modelos en una misma operación;
- mostrar la clase estimada y la probabilidad de phishing;
- representar el resultado mediante una escala visual de riesgo;
- mostrar señales URL relevantes de forma resumida;
- mostrar el vector técnico empleado por el modelo URL o híbrido;
- generar un reporte local descargable en formato TXT;
- conservar temporalmente el último resultado dentro de la sesión activa;
- ejecutar el procesamiento sin abrir enlaces y sin consultar servicios externos.

PhishGuard Antares no realiza:

- navegación hacia las URL ingresadas;
- verificación de reputación en servicios externos;
- consulta de listas negras en internet;
- análisis dinámico de páginas web;
- inspección de archivos adjuntos;
- detección de malware;
- autenticación de remitentes mediante SPF, DKIM o DMARC;
- análisis de certificados digitales o antigüedad de dominios;
- monitoreo automático de cuentas de correo;
- almacenamiento automático de mensajes o credenciales;
- sustitución de herramientas profesionales de seguridad.

---

## 4. Requisitos para utilizar el sistema

### 4.1 Requisitos básicos del usuario

El usuario debe disponer de:

- una computadora con Windows o Ubuntu/Linux;
- Python y las dependencias del proyecto instaladas;
- un navegador web moderno;
- acceso local a la carpeta del proyecto;
- los tres archivos de modelo ubicados en la carpeta `models/`;
- autorización para analizar el contenido utilizado cuando este provenga de un entorno real.

### 4.2 Recomendaciones de seguridad

Antes de usar el sistema:

- no abra enlaces sospechosos en el navegador;
- no copie contraseñas, códigos de autenticación o información financiera real;
- anonimice datos personales cuando utilice mensajes reales;
- use ejemplos controlados o neutralizados durante demostraciones;
- no comparta reportes con contenido sensible sin revisar previamente su información;
- utilice el prototipo únicamente con fines académicos, educativos o defensivos.

---

## 5. Inicio del sistema

### 5.1 Inicio en Windows

1. Abra Visual Studio Code o PowerShell.
2. Ubíquese en la carpeta raíz del proyecto:

```powershell
cd "<ruta_del_proyecto>\PHISHGUARD_ANTARES_FINAL"
```

3. Active el entorno virtual, si existe:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Ejecute la aplicación:

```powershell
python -m streamlit run app.py
```

5. Abra en el navegador la dirección mostrada por Streamlit, normalmente:

```text
http://localhost:8501
```

### 5.2 Inicio en Ubuntu/Linux

1. Abra una terminal.
2. Ubíquese en la carpeta raíz del proyecto:

```bash
cd "<ruta_del_proyecto>/PHISHGUARD_ANTARES_FINAL"
```

3. Active el entorno virtual, si existe:

```bash
source .venv/bin/activate
```

4. Ejecute la aplicación:

```bash
python -m streamlit run app.py
```

5. Abra la dirección local indicada, normalmente:

```text
http://localhost:8501
```

### 5.3 Cierre del sistema

Para detener el servidor local:

1. Regrese a la terminal donde se ejecuta Streamlit.
2. Presione:

```text
Ctrl + C
```

3. Cierre la pestaña del navegador si ya no será utilizada.

---

## 6. Descripción general de la interfaz

La interfaz se divide en dos áreas principales:

- **Centro de mando lateral:** contiene las opciones de configuración.
- **Área de análisis:** contiene el encabezado, los campos de entrada, el botón de análisis y los resultados.

### 6.1 Barra de estado

En la parte superior se presenta una barra con los estados:

- **Modelos locales activos:** indica que los modelos se encuentran disponibles localmente.
- **Sin conexión externa:** informa que el análisis no depende de consultas a internet.
- **Análisis defensivo:** recuerda la finalidad académica y preventiva del prototipo.

### 6.2 Encabezado principal

El encabezado muestra:

- logotipo de PhishGuard Antares;
- nombre del sistema;
- subtítulo del prototipo;
- número de versión;
- aviso de uso académico y defensivo.

### 6.3 Centro de mando

El centro de mando permite:

- abrir o cerrar el panel lateral;
- seleccionar el modelo de análisis;
- consultar el modo actualmente activo;
- activar la comparación de los tres modelos;
- solicitar que el análisis avanzado se abra automáticamente;
- visualizar la escala de riesgo.

### 6.4 Campos de entrada

El área principal contiene:

- **Asunto del mensaje:** título o asunto del correo o mensaje.
- **Cuerpo del mensaje:** contenido textual que será examinado.
- **URL o enlaces asociados:** direcciones web, referencias `mailto:`, referencias `cid:` u otros enlaces detectados.

### 6.5 Botón Analizar

El botón **Analizar** inicia la validación de la entrada, la preparación de características, la carga del modelo y la generación del resultado.

### 6.6 Ventana de resultado

Al finalizar el análisis se abre una ventana modal que muestra:

- modelo utilizado;
- clase estimada;
- probabilidad estimada de phishing;
- nivel orientativo de riesgo;
- recomendación principal;
- escala visual;
- señales técnicas;
- apartado de análisis avanzado;
- opción de descarga del reporte local.

### 6.7 Resultado persistente

Cuando se cierra la ventana modal, el sistema conserva una tarjeta compacta con el último resultado. Desde esta tarjeta se puede:

- reabrir la ventana sin repetir el análisis;
- limpiar el resultado almacenado en la sesión.

---

## 7. Selección del modelo

### 7.1 Modelo híbrido

**Uso recomendado:** análisis integral de mensajes que contienen texto y enlaces.

**Entrada requerida:**

- asunto o cuerpo del mensaje;
- URL o enlace recomendado, aunque el modelo puede operar con texto y valores URL vacíos.

**Procesamiento:** combina el texto con 27 características URL/enlaces.

**Ventaja:** integra señales lingüísticas y estructurales en una sola predicción.

### 7.2 Modelo textual

**Uso recomendado:** mensajes cuyo contenido textual es el principal elemento disponible.

**Entrada requerida:** asunto, cuerpo o ambos.

**Procesamiento:** concatena el asunto y el cuerpo del mensaje y los representa mediante características TF-IDF.

**Limitación:** no utiliza las características técnicas de URL, aunque el texto contenga una dirección web.

### 7.3 Modelo URL

**Uso recomendado:** análisis de una o varias direcciones URL o referencias de enlace.

**Entrada requerida:** al menos una URL o señal de enlace reconocible.

**Procesamiento:** extrae 27 características cuantitativas y binarias relacionadas con longitud, símbolos, subdominios, HTTPS, IP, acortadores, palabras sospechosas y tipos de enlaces.

**Limitación:** no interpreta el significado general del mensaje.

### 7.4 Comparar los tres modelos

Al marcar **Comparar los tres modelos**, el sistema ejecuta:

1. modelo textual;
2. modelo URL;
3. modelo híbrido.

Para que la comparación se realice sin advertencias se recomienda proporcionar:

- asunto;
- cuerpo del mensaje;
- URL o enlaces asociados.

El modelo híbrido se utiliza como lectura principal dentro de la ventana comparativa, mientras los tres resultados se muestran de forma separada.

---

## 8. Procedimiento estándar de análisis

### 8.1 Análisis híbrido recomendado

1. Abra el centro de mando.
2. Seleccione **Modelo híbrido**.
3. Deje desmarcada la comparación si desea ejecutar solo ese modelo.
4. Escriba o pegue el asunto del mensaje.
5. Pegue el cuerpo del mensaje.
6. Pegue la URL o los enlaces asociados.
7. Revise que no haya datos personales o credenciales reales.
8. Presione **Analizar**.
9. Espere hasta que el indicador llegue al 100 %.
10. Lea la clase estimada, la probabilidad y el nivel de riesgo.
11. Revise las señales principales.
12. Abra el análisis avanzado cuando necesite información técnica.
13. Descargue el reporte TXT si requiere conservar evidencia.

### 8.2 Caso de prueba académico

```text
Asunto:
Verificación urgente

Cuerpo:
Debe actualizar su cuenta para evitar suspensión del servicio.

URL:
https://secure-login.example.com/verify?token=123
```

Este ejemplo usa el dominio reservado `example.com` y es adecuado para demostraciones controladas.

---

## 9. Animación de procesamiento

Después de presionar **Analizar**, el sistema muestra un indicador circular de 0 % a 100 % con las etapas:

1. validación de la entrada;
2. normalización del texto y enlaces;
3. extracción de características URL/enlaces;
4. preparación del vector técnico;
5. carga del modelo local;
6. estimación de la probabilidad de phishing;
7. organización del resultado.

La animación constituye una retroalimentación visual del flujo local. No significa que el sistema esté conectándose a servicios externos ni que esté visitando la URL ingresada.

---

## 10. Interpretación del resultado

### 10.1 Clase estimada

El sistema puede mostrar:

- **Legítimo probable:** el modelo asignó la clase legítima.
- **Phishing probable:** el modelo asignó la clase phishing.

La palabra **probable** es esencial: el resultado no representa certeza absoluta.

### 10.2 Probabilidad estimada de phishing

Se presenta como un porcentaje entre 0 % y 100 %. Expresa la estimación del modelo para la clase phishing sobre la entrada analizada.

La probabilidad:

- no equivale a una garantía de seguridad;
- no reemplaza una investigación técnica;
- puede verse afectada por la calidad y cantidad de información ingresada;
- puede producir falsos positivos o falsos negativos;
- debe interpretarse junto con el modelo utilizado, las señales observadas y el contexto.

### 10.3 Escala orientativa de riesgo

| Probabilidad estimada | Nivel visual | Interpretación general |
|---:|---|---|
| 0 % a < 5 % | Muy bajo | No se observan señales fuertes, sin garantía absoluta |
| 5 % a < 15 % | Bajo | Riesgo estimado bajo; mantener verificación habitual |
| 15 % a < 35 % | Precaución | Existen señales que conviene revisar |
| 35 % a < 50 % | Moderado | Requiere verificación cuidadosa |
| 50 % a < 70 % | Alto | Presenta patrones compatibles con phishing |
| 70 % a < 85 % | Muy alto | Alta probabilidad estimada de phishing |
| 85 % a 100 % | Crítico | Señales muy fuertes; evitar interacción y reportar |

> Esta escala es didáctica y orientativa. No constituye una calibración probabilística formal ni una política institucional de respuesta a incidentes.

### 10.4 Diferencia entre clase y nivel de riesgo

La clase es la decisión binaria del modelo. El nivel de riesgo es una interpretación visual adicional basada en rangos de probabilidad. Ambos elementos deben leerse conjuntamente, pero no son idénticos.

---

## 11. Señales principales

Cuando se utiliza el modelo URL o híbrido, la ventana puede mostrar:

- número de URL web detectadas;
- total de enlaces detectados;
- cantidad de referencias `mailto:`;
- cantidad de referencias `cid:`;
- máximo de subdominios;
- uso de HTTPS;
- presencia de acortadores;
- cantidad de palabras sospechosas en la URL.

Estas señales describen características del texto de la URL. No demuestran por sí solas que un enlace sea malicioso.

### 11.1 Consideraciones importantes

- **HTTPS no implica legitimidad:** un sitio fraudulento también puede usar HTTPS.
- **Una URL larga no es necesariamente maliciosa:** algunas plataformas legítimas generan direcciones extensas.
- **Una palabra como `login` o `secure` no confirma phishing:** se considera una señal contextual.
- **Los subdominios pueden ser legítimos:** deben evaluarse junto con el resto de características.
- **Una URL de apariencia normal puede seguir siendo riesgosa:** el prototipo no consulta reputación ni contenido remoto.

---

## 12. Calidad del contexto ingresado

El sistema puede mostrar notas complementarias:

### 12.1 Contexto completo

Existe texto suficiente y URL asociada. Es la entrada más informativa para el modelo híbrido.

### 12.2 Contexto limitado

Se ingresó principalmente una URL aislada. El sistema puede analizar su estructura, pero no conoce su reputación ni el contexto del mensaje.

### 12.3 Sin enlaces explícitos

Se ingresó texto, pero no se proporcionó una URL. El análisis textual continúa, aunque no se aprovechan señales léxicas de enlaces.

### 12.4 Entrada mínima

La información disponible es escasa. El resultado debe interpretarse con cautela.

---

## 13. Análisis avanzado

El apartado **Ver análisis avanzado** presenta información destinada a usuarios técnicos, docentes o evaluadores.

Puede incluir:

- tabla de señales resumidas;
- vector de características utilizado por el modelo;
- valores numéricos de las 27 características URL;
- columna textual en el modelo híbrido;
- resumen comparativo de los modelos;
- botón de descarga del reporte.

El usuario común no necesita interpretar cada variable para comprender el dictamen principal.

---

## 14. Reporte local TXT

### 14.1 Descarga

1. Abra el análisis avanzado.
2. Presione **Descargar reporte local TXT** o **Descargar reporte comparativo TXT**.
3. Seleccione una ubicación segura.
4. Renombre el archivo cuando corresponda a una prueba formal.

### 14.2 Contenido

El reporte incluye:

- fecha y hora local;
- modelo utilizado;
- clase estimada;
- probabilidad de phishing;
- nivel orientativo de riesgo;
- mensaje de riesgo;
- señales técnicas URL;
- comparación de modelos, cuando se haya solicitado;
- entrada analizada;
- advertencia metodológica y de seguridad.

### 14.3 Neutralización de enlaces

En el reporte descargable:

- `https://` se transforma en `hxxps://`;
- `http://` se transforma en `hxxp://`;
- `www.` se transforma en `www[.]`.

Esta neutralización reduce el riesgo de apertura accidental desde el archivo de texto.

---

## 15. Resultado persistente

Después de cerrar la ventana de resultado, el sistema conserva un resumen en la sesión actual.

Opciones disponibles:

- **Abrir ventana de resultado:** vuelve a mostrar el análisis sin ejecutarlo nuevamente.
- **Limpiar último resultado:** elimina el resultado temporal de la sesión.

El resultado persistente no constituye almacenamiento permanente. Al reiniciar el servidor o finalizar la sesión puede dejar de estar disponible.

---

## 16. Buenas prácticas de uso

- Analice el mensaje completo cuando sea posible.
- Proporcione el asunto, cuerpo y URL para el modelo híbrido.
- Verifique el remitente por un canal independiente.
- No abra enlaces desde el mensaje sospechoso.
- No introduzca contraseñas ni códigos de autenticación.
- Compare modelos únicamente cuando existan entradas apropiadas para los tres.
- Use el análisis avanzado como apoyo, no como evidencia única.
- Conserve reportes y capturas solo cuando no contengan información sensible.
- Ante riesgo alto, muy alto o crítico, siga el protocolo institucional de reporte.
- Ante un resultado bajo, mantenga igualmente hábitos normales de verificación.

---

## 17. Mensajes de validación y solución de problemas

### 17.1 “Debe ingresar asunto o cuerpo del mensaje”

**Causa:** se seleccionó el modelo textual o híbrido sin contenido textual.  
**Solución:** complete el asunto, el cuerpo o ambos.

### 17.2 “Debe ingresar al menos una URL/enlace”

**Causa:** se seleccionó el modelo URL sin una entrada reconocible.  
**Solución:** pegue una URL completa o una referencia de enlace válida.

### 17.3 “No se pudo realizar el análisis”

**Posibles causas:**

- falta un archivo `.joblib`;
- hay incompatibilidad de dependencias;
- la entrada no satisface los requisitos del modelo;
- las columnas generadas no coinciden con las esperadas;
- el entorno virtual no está correctamente configurado.

**Acción recomendada:** informe el mensaje completo al responsable técnico y consulte el manual técnico.

### 17.4 La página no abre

1. Verifique que Streamlit siga ejecutándose.
2. Confirme la dirección `http://localhost:8501`.
3. Revise que el puerto no esté siendo usado por otra aplicación.
4. Reinicie Streamlit.
5. Compruebe que las dependencias estén instaladas.

### 17.5 El resultado parece inesperado

- confirme qué modelo está seleccionado;
- revise si pegó el mensaje completo;
- verifique que la URL no contenga errores de copia;
- consulte la nota de calidad de contexto;
- compare los tres modelos;
- recuerde que pueden existir falsos positivos y falsos negativos.

---

## 18. Privacidad y tratamiento de datos

PhishGuard Antares fue diseñado para ejecución local. El sistema:

- no envía automáticamente el contenido a una API externa;
- no visita las URL ingresadas;
- no guarda automáticamente las entradas sensibles;
- no crea reportes sin acción explícita del usuario;
- conserva temporalmente el último resultado en la sesión de Streamlit.

El usuario sigue siendo responsable de:

- no introducir información cuya copia no esté autorizada;
- anonimizar datos personales;
- almacenar de forma segura los reportes descargados;
- eliminar evidencias sensibles cuando ya no sean necesarias;
- cumplir las políticas de seguridad y privacidad aplicables.

---

## 19. Limitaciones del prototipo

- Fue desarrollado como prototipo académico y no como producto comercial.
- Su desempeño depende de los datos utilizados durante el entrenamiento.
- Puede clasificar mensajes legítimos como phishing.
- Puede clasificar mensajes de phishing como legítimos.
- No consulta reputación de dominios.
- No analiza el contenido remoto de las páginas.
- No inspecciona archivos adjuntos.
- No reemplaza un centro de operaciones de seguridad.
- No ofrece garantía absoluta de protección.
- La escala de riesgo es explicativa y no una calibración formal.
- El modelo URL puede reaccionar a términos o estructuras presentes también en enlaces legítimos.
- El resultado debe contextualizarse con otras verificaciones.

---

## 20. Glosario básico

| Término | Definición |
|---|---|
| Phishing | Técnica de engaño orientada a obtener información sensible o inducir acciones perjudiciales |
| URL | Dirección utilizada para identificar un recurso en la web |
| Modelo textual | Clasificador que emplea contenido escrito |
| Modelo URL | Clasificador que emplea características de enlaces |
| Modelo híbrido | Clasificador que integra texto y características URL |
| Probabilidad estimada | Valor producido por el modelo para la clase phishing |
| Falso positivo | Mensaje legítimo clasificado como phishing |
| Falso negativo | Mensaje phishing clasificado como legítimo |
| `mailto:` | Referencia que representa una dirección de correo electrónico |
| `cid:` | Identificador interno de contenido empleado frecuentemente en correos HTML |
| TF-IDF | Técnica de representación numérica de términos en documentos |
| Inferencia | Aplicación de un modelo entrenado a una nueva entrada |
| Reporte neutralizado | Informe en el que las URL se transforman para reducir aperturas accidentales |

---

## 21. Evidencias relacionadas

Las evidencias de uso del sistema deben conservarse en la carpeta académica definida para el proyecto, incluyendo:

- capturas de la interfaz;
- video de demostración;
- reporte TXT generado;
- checklist de pruebas;
- registro de compilación;
- lista de dependencias;
- backup dorado;
- hash SHA-256;
- inventario del software.

---

## 22. Declaración final de uso

PhishGuard Antares debe utilizarse como una herramienta de apoyo académico y defensivo. La decisión de abrir un enlace, responder un mensaje, proporcionar información o reportar un incidente no debe depender exclusivamente del resultado del prototipo. Ante cualquier duda, se recomienda detener la interacción, verificar la fuente por un canal independiente y solicitar asistencia a personal competente en ciberseguridad.
