# Checklist de Pruebas — PhishGuard Antares

**Sistema:** PhishGuard Antares  
**Versión evaluada:** 2.0  
**Tipo de documento:** Plan, registro y evidencia de pruebas funcionales, técnicas, visuales y de seguridad  
**Estado final:** Cerrado. Dictamen: APTO PARA EVIDENCIA Y DEFENSA.

---

## 1. Identificación de la ejecución

| Campo                        | Valor                                                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Fecha de prueba              | 21/06/2026 y 24/06/2026                                                                                                       |
| Hora de inicio               | 10:45                                                                                                            |
| Hora de finalización         | 11:05                                                                                                            |
| Responsable de prueba        | Pedro Pablo Ciancio González                                                        |
| Equipo utilizado             | HP 240 G4 2015/2016 y Acer Aspire A315-53                                                          |
| Sistema operativo            | Microsoft Windows 10 Home Single Language y Ubuntu/Linux                                           |
| Versión de Python            | Python 3.14.6 en Windows; Python 3.14.4 en Ubuntu                                                                                                    |
| Versión de Streamlit         | 1.58.0                                                                                                           |
| Versión de scikit-learn      | 1.9.0                                                                                                            |
| Navegador y versión          | Brave Browser 1.91.175, compilación oficial de 64 bits, basado en Chromium 149.0.7827.155                        |
| Ruta del proyecto            | C:\Users\Antar\OneDrive\Desktop\Tesis de Pregrado N°1 - Antares\tesis-phishing-software\PHISHGUARD_ANTARES_FINAL |
| Archivo final limpio de referencia | Archivo .7z final entregado junto con su archivo externo .sha256.txt |
| Hash SHA-256 verificado      | Sí                                                                                                               |


---

## 2. Convenciones

### 2.1 Estados

| Estado | Significado |
|---|---|
| APROBADO | El resultado observado coincide con el esperado |
| FALLIDO | El resultado no coincide con el esperado |
| BLOQUEADO | No pudo ejecutarse por una dependencia o condición externa |
| NO APLICA | La prueba no corresponde al entorno evaluado |
| PENDIENTE | Aún no fue ejecutada |

### 2.2 Severidad

| Severidad | Criterio |
|---|---|
| Crítica | Impide iniciar, predecir o conservar la seguridad del prototipo |
| Alta | Afecta una función principal o genera resultado incorrecto |
| Media | Afecta una función secundaria o dificulta el uso |
| Baja | Defecto visual o menor sin impacto funcional significativo |

### 2.3 Criterio de cierre

La versión se considera apta cuando:

- no existen fallos críticos o altos abiertos;
- las pruebas de carga de modelos y predicción están aprobadas;
- las 27 características URL se generan correctamente;
- el flujo de resultado, modal y persistencia funciona;
- el reporte se descarga y neutraliza enlaces;
- no se realizan visitas URL ni consultas externas;
- los defectos menores, si existieran, están documentados como limitaciones.

---

## 3. Archivos y evidencias esperadas

| Evidencia | Nombre recomendado |
|---|---|
| Pantalla inicial | `01_inicio_general.png` |
| Centro de mando | `02_centro_de_mando.png` |
| Selector de modelo | `03_selector_modelo.png` |
| Formulario | `04_formulario_prueba.png` |
| Loader | `05_loader_analisis.png` |
| Modal | `06_modal_resultado.png` |
| Resultado persistente | `07_resultado_persistente.png` |
| Análisis avanzado | `08_analisis_avanzado.png` |
| Comparación | `09_comparacion_modelos.png` |
| Panel colapsado | `10_sidebar_colapsado.png` |
| Video demo | `demo_phishguard_antares_version_dorada.mp4` |
| Reporte simple | `reporte_prueba_hibrido_sospechoso.txt` |
| Reporte comparativo | `reporte_comparativo_phishguard_antares.txt` |
| Compilación | `verificacion_compilacion.txt` |
| Dependencias | `dependencias_instaladas_windows.txt` |
| Backup | archivo `.7z` dorado |
| Integridad | archivo `.sha256.txt` |

---

## 4. Datos controlados de prueba

### CP-01 — Caso sospechoso completo

```text
Asunto: Verificación urgente
Cuerpo: Debe actualizar su cuenta para evitar suspensión del servicio.
URL: https://secure-login.example.com/verify?token=123
```

### CP-02 — Enlaces web y no web

```text
URL/enlaces: mailto:soporte@banco.com, cid:image001.jpg, https://login-banco.example.com/actualizar
```

### CP-03 — Texto sin URL

```text
Asunto: Reunión de coordinación
Cuerpo: Se confirma la reunión del equipo para mañana a las 10:00. No se requiere entregar credenciales ni acceder a enlaces.
```

### CP-04 — URL aislada controlada

```text
https://secure-login.example.com/verify?token=123
```

### CP-05 — Entrada vacía

```text
Asunto: [vacío]
Cuerpo: [vacío]
URL: [vacío]
```

> Los dominios `example.com` se utilizan como ejemplos controlados. No emplear enlaces phishing activos en las pruebas de interfaz.

---

# 5. Matriz de pruebas

## A. Integridad, entorno y precondiciones

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| ENV-01 | Verificar backup dorado | Ejecutar `7z t <archivo>.7z` | Aparece `Everything is Ok` | Crítica | APROBADO | Archivo `.7z` validado en carpeta `06_backup_dorado`; evidencia en `07_hash_e_integridad` |
| ENV-02 | Verificar hash SHA-256 | Calcular hash y comparar con `.sha256.txt` | El hash coincide exactamente | Crítica | APROBADO | Hash SHA-256 verificado mediante archivo externo .sha256.txt correspondiente al paquete final limpio. El valor exacto se conserva fuera del archivo comprimido para evitar autorreferencia. |
| ENV-03 | Verificar inventario | Revisar `.contenido.txt` | Incluye `app.py`, `src/`, `models/`, `assets/`, `.streamlit/` | Alta | APROBADO | Evidencia en `08_inventario_software` |
| ENV-04 | Verificar dependencias | Ejecutar `python -m pip freeze` | Se genera listado sin error | Media | APROBADO | Evidencia en `03_comandos_verificacion\dependencias_instaladas_windows.txt` |
| ENV-05 | Verificar sintaxis | Ejecutar `python -m py_compile ...` | Finaliza sin errores | Crítica | APROBADO | Evidencia en `03_comandos_verificacion\verificacion_compilacion.txt` |
| ENV-06 | Verificar modelos | Ejecutar `validate_model_files()` | Los tres valores son `True` | Crítica | APROBADO | Modelos presentes en `models`: textual, URL e híbrido |
| ENV-07 | Verificar estructura URL | Ejecutar `build_feature_frame` | Forma `(1, 27)` | Crítica | APROBADO | Verificación realizada durante validación técnica del software |
| ENV-08 | Verificar versión visible | Abrir interfaz | Se muestra versión `2.0` | Baja | APROBADO | Evidencia en capturas finales del software |

## B. Arranque y navegación

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| NAV-01 | Inicio de Streamlit | Ejecutar `python -m streamlit run app.py` | Servidor inicia sin excepción | Crítica | APROBADO | Evidencia en `03_comandos_verificacion\ejecucion_streamlit.txt` |
| NAV-02 | Acceso local | Abrir `http://localhost:8501` | Carga la aplicación | Crítica | APROBADO | Evidencia en `01_capturas_finales\01_inicio_general.png` |
| NAV-03 | Barra de estado | Revisar cabecera | Se muestran modelos locales, sin conexión externa y análisis defensivo | Baja | APROBADO | Evidencia visible en capturas finales de la interfaz |
| NAV-04 | Centro de mando abierto | Abrir app | Panel lateral visible y ordenado | Media | APROBADO | Evidencia en `01_capturas_finales\02_centro_de_mando.png` |
| NAV-05 | Cerrar centro de mando | Presionar botón de cierre | Panel se reduce a barra compacta | Media | APROBADO | Evidencia en `01_capturas_finales\10_sidebar_colapsado.png` |
| NAV-06 | Reabrir centro de mando | Presionar botón de apertura | Panel vuelve sin perder configuración | Alta | APROBADO | Evidencia en video demostrativo del software |
| NAV-07 | Selector no editable | Abrir selector e intentar escribir | Solo permite elegir opciones predefinidas | Media | APROBADO | Evidencia en `01_capturas_finales\03_selector_modelo.png` |
| NAV-08 | Persistencia de selección | Elegir modelo, cerrar y abrir panel | Se conserva el modelo seleccionado | Alta | APROBADO | Evidencia observada durante la prueba funcional de navegación |

## C. Validación de entradas

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| VAL-01 | Textual vacío | Seleccionar textual, usar CP-05 | Muestra error y no predice | Alta | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| VAL-02 | Híbrido vacío | Seleccionar híbrido, usar CP-05 | Muestra error y no predice | Alta | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| VAL-03 | URL vacía | Seleccionar URL, usar CP-05 | Muestra error y no predice | Alta | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| VAL-04 | Textual con texto | Seleccionar textual, ingresar asunto/cuerpo | Permite ejecutar | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| VAL-05 | URL con enlace | Seleccionar URL, usar CP-04 | Permite ejecutar | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| VAL-06 | Híbrido con texto | Seleccionar híbrido, ingresar texto | Permite ejecutar y muestra nota si no hay URL | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| VAL-07 | Híbrido completo | Seleccionar híbrido, usar CP-01 | Ejecuta sin advertencia de contexto limitado | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| VAL-08 | Espacios exteriores | Ingresar valores con espacios antes/después | Se normalizan sin excepción | Media | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| VAL-09 | Texto con enlace embebido | Pegar URL dentro del cuerpo | El extractor puede reconocer señal de enlace | Media | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |

## D. Modelo textual

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| TXT-01 | Carga del modelo textual | Seleccionar textual y analizar | No hay error de carga | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| TXT-02 | Predicción textual sospechosa | Usar texto de CP-01 | Genera clase y probabilidad | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| TXT-03 | Entrada usada | Abrir análisis avanzado | El texto combina asunto y cuerpo | Alta | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| TXT-04 | Sin señales URL | Revisar señales | Indica que no generó señales URL | Media | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |
| TXT-05 | Repetibilidad | Ejecutar dos veces la misma entrada | Resultado idéntico en el mismo entorno | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |

## E. Modelo URL

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| URL-01 | Carga del modelo URL | Seleccionar URL y analizar CP-04 | No hay error de carga | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-02 | Predicción URL | Analizar CP-04 | Genera clase y probabilidad | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-03 | Vector de 27 variables | Abrir análisis avanzado | Se muestran 27 columnas | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-04 | Detección web | Analizar CP-04 | `URL web detectadas = 1` | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-05 | Detección HTTPS | Analizar CP-04 | `Usa HTTPS = Sí` | Media | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-06 | Palabras sospechosas | Analizar CP-04 | Conteo mayor que cero | Media | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| URL-07 | Repetibilidad | Repetir CP-04 | Resultado idéntico | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |

## F. Extracción de enlaces no web

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| LNK-01 | `mailto:` | Analizar CP-02 | `link_mailto_count = 1` y `has_mailto = 1` | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| LNK-02 | `cid:` | Analizar CP-02 | `link_cid_count = 1` y `has_cid = 1` | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| LNK-03 | URL web combinada | Analizar CP-02 | `url_web_count = 1` y `has_web_url = 1` | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| LNK-04 | Total detectado | Analizar CP-02 | Total coherente con los tres elementos | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| LNK-05 | No visita enlaces | Observar ejecución y revisar código | No abre navegador ni genera solicitud externa | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |

## G. Modelo híbrido

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| HYB-01 | Carga del modelo híbrido | Analizar CP-01 | No hay error de carga | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-02 | Predicción híbrida | Analizar CP-01 | Genera clase y probabilidad | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-03 | Columna de texto | Abrir análisis avanzado | Vector incluye columna `text` | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-04 | Variables URL | Revisar vector | Incluye las 27 características URL | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-05 | Contexto completo | Usar CP-01 | No muestra advertencia de contexto limitado | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-06 | Texto sin URL | Usar CP-03 | Predice y muestra nota “Sin enlaces explícitos” | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| HYB-07 | Repetibilidad | Repetir CP-01 | Resultado idéntico | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |

## H. Comparación de modelos

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| CMP-01 | Activar comparación | Marcar opción y analizar CP-01 | Ejecuta los tres modelos | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| CMP-02 | Tarjetas individuales | Revisar modal | Muestra textual, URL e híbrido | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| CMP-03 | Lectura principal | Revisar resultado | El híbrido aparece como lectura principal | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| CMP-04 | Resumen comparativo | Abrir avanzado | Tabla incluye modelo, clase, probabilidad y riesgo | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| CMP-05 | Valores de regresión | Ejecutar CP-01 | Textual ≈ 71,63 %, URL ≈ 65,73 %, híbrido ≈ 78,76 % en el entorno dorado | Alta | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| CMP-06 | Error parcial controlado | Comparar con una entrada incompleta | Advierte si algún modelo no puede ejecutarse sin cerrar la app | Media | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |

## I. Loader y retroalimentación

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| LOD-01 | Aparición del loader | Presionar Analizar | Se muestra overlay centrado | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| LOD-02 | Progreso fluido | Observar 0–100 % | Incrementa progresivamente sin grandes saltos | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| LOD-03 | Etapas | Observar textos | Cambian las etapas del procesamiento | Baja | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| LOD-04 | Nota local | Observar loader | Indica sin abrir enlaces y sin APIs externas | Baja | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| LOD-05 | Cierre del loader | Esperar final | Desaparece y abre resultado | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |

## J. Resultado e interpretación

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| RES-01 | Modal | Finalizar análisis | Se abre ventana de resultado | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-02 | Clase | Revisar tarjeta | Muestra Legítimo probable o Phishing probable | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-03 | Probabilidad | Revisar panel | Muestra porcentaje con dos decimales | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-04 | Nivel de riesgo | Revisar chip | Coincide con el rango definido | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-05 | Barra de probabilidad | Revisar escala | Pin y relleno corresponden al porcentaje | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-06 | Señales principales | Modelo URL/híbrido | Muestra señales resumidas | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-07 | Nota de contexto | Usar entrada parcial | Muestra advertencia correspondiente | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| RES-08 | Cerrar modal | Presionar `X` | Modal cierra sin perder sesión | Alta | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| RES-09 | Tarjeta persistente | Cerrar modal | Aparece resumen compacto | Alta | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| RES-10 | Reabrir resultado | Presionar botón | Modal reaparece sin recalcular | Alta | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| RES-11 | Limpiar resultado | Presionar limpiar | El resumen desaparece sin borrar campos | Media | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| RES-12 | Scroll del modal | Desplazarse con barra y rueda | Resultado no desaparece | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |

## K. Análisis avanzado y reportes

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| ADV-01 | Abrir avanzado | Presionar expander | Muestra contenido técnico | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| ADV-02 | Apertura automática | Marcar opción y analizar | Avanzado aparece desplegado | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| ADV-03 | Tabla de señales | Revisar contenido | Valores se muestran como tabla | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| ADV-04 | Vector técnico | Revisar URL/híbrido | Muestra DataFrame de entrada | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| REP-01 | Descargar reporte simple | Presionar descarga | Se obtiene TXT | Alta | APROBADO | Validado en Ubuntu con reportes TXT guardados en docs/evidencias_ubuntu/reportes; enlaces HTTPS neutralizados como hxxps. |
| REP-02 | Descargar comparativo | Comparar y descargar | Se obtiene TXT comparativo | Alta | APROBADO | Validado en Ubuntu con reportes TXT guardados en docs/evidencias_ubuntu/reportes; enlaces HTTPS neutralizados como hxxps. |
| REP-03 | Contenido del reporte | Abrir TXT | Incluye fecha, modelo, clase, probabilidad, riesgo y advertencia | Alta | APROBADO | Validado en Ubuntu con reportes TXT guardados en docs/evidencias_ubuntu/reportes; enlaces HTTPS neutralizados como hxxps. |
| REP-04 | Neutralización HTTPS | Revisar TXT | `https://` se convierte en `hxxps://` | Crítica | APROBADO | Validado en Ubuntu con reportes TXT guardados en docs/evidencias_ubuntu/reportes; enlaces HTTPS neutralizados como hxxps. |
| REP-05 | Neutralización HTTP | Probar URL HTTP y descargar | `http://` se convierte en `hxxp://` | Crítica | APROBADO | Validado en Ubuntu con reporte TXT; enlace HTTP neutralizado como hxxp:// en docs/evidencias_ubuntu/reportes. |
| REP-06 | Sin guardado automático | Analizar sin descargar | No se crea reporte en disco automáticamente | Alta | APROBADO | Validado mediante auditoría funcional de pendientes Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_pendientes_funcionales_20260624_142417.txt. |

## L. Interfaz, visualización y usabilidad

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| UI-01 | Coherencia visual | Revisar pantalla | Paleta, bordes y tipografía son uniformes | Baja | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-02 | Logo | Revisar encabezado y panel | Se muestra sin deformación crítica | Baja | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-03 | Botón Analizar | Revisar y pulsar | Visible y funcional | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-04 | Campos de entrada | Escribir y borrar | Responden correctamente | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-05 | Zoom 100 % | Usar navegador a 100 % | Interfaz se mantiene legible | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-06 | Resolución de defensa | Probar pantalla prevista | No hay solapamientos críticos | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-07 | Selector | Abrir y cerrar | Animación y opciones funcionan | Media | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| UI-08 | Texto de advertencia | Revisar interfaz | Es visible y comprensible | Media | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| UI-09 | Elementos nativos | Revisar cabecera | No aparece botón Deploy en la vista documentada | Baja | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |

## M. Seguridad y privacidad

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| SEC-01 | Sin visita URL | Analizar CP-04 | No se abre ninguna pestaña ni conexión visible | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| SEC-02 | Sin APIs externas | Revisar código y tráfico del caso de prueba | Inferencia funciona localmente | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |
| SEC-03 | Sin guardado de entradas | Analizar y revisar proyecto | No aparecen mensajes copiados en logs automáticos | Crítica | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| SEC-04 | Modelos locales | Desconectar internet y analizar | La predicción sigue funcionando | Alta | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| SEC-05 | Modelos oficiales | Comparar hash/ubicación | Se usan archivos del paquete dorado | Crítica | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| SEC-06 | Mensaje de limitación | Revisar resultado y reporte | Indica carácter orientativo | Alta | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| SEC-07 | Datos sensibles | Revisar procedimiento | No se emplean credenciales reales | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| SEC-08 | Enlaces neutralizados | Revisar reporte | No quedan esquemas HTTP/HTTPS activos | Crítica | APROBADO | Validado mediante auditoría funcional automática Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_funcional_ubuntu_20260624_135727.txt. |

## N. Compatibilidad y regresión

| ID | Prueba | Procedimiento | Resultado esperado | Severidad | Estado | Evidencia/observación |
|---|---|---|---|---|---|---|
| PLT-01 | Windows | Ejecutar flujo completo | Funciona sin excepción | Crítica | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |
| PLT-02 | Ubuntu | Ejecutar flujo completo | Funciona sin excepción | Crítica | APROBADO | Validado en Ubuntu con capturas en docs/evidencias_ubuntu/capturas y evidencia de entorno Ubuntu. |
| PLT-03 | Mismo caso en ambos | Ejecutar CP-01 | Misma clase y probabilidad con entorno compatible | Alta | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| REG-01 | Regresión textual | Ejecutar caso controlado | No cambia respecto a la versión dorada | Alta | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| REG-02 | Regresión URL | Ejecutar CP-04 | No cambia respecto a la versión dorada | Alta | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| REG-03 | Regresión híbrida | Ejecutar CP-01 | No cambia respecto a la versión dorada | Alta | APROBADO | Validado mediante auditoría de seguridad/regresión Ubuntu: docs/evidencias_ubuntu/auditoria/auditoria_seguridad_regresion_20260624_140403.txt. |
| REG-04 | Regresión visual | Comparar capturas | No faltan secciones finales aprobadas | Media | APROBADO | Cierre final validado en Ubuntu con pruebas manuales, capturas en docs/evidencias_ubuntu/capturas, auditorías técnicas en docs/evidencias_ubuntu/auditoria y evidencia previa Windows registrada. |

---

## 6. Registro de defectos

| ID defecto | Prueba relacionada | Descripción | Severidad | Estado | Acción correctiva | Evidencia de cierre |
|---|---|---|---|---|---|---|
| DEF-001 | Dictamen final: apto para evidencia y defensa | Revisar cierre completo del checklist | El software funciona en Ubuntu, cuenta con capturas, reportes, auditorías, hashes y evidencias | Crítica | APROBADO | Se selecciona este dictamen final; no quedan pruebas funcionales pendientes reales. |
| DEF-002 | Dictamen alternativo: apto con observaciones | No seleccionado | No corresponde al cierre actual | Media | NO APLICA | Se seleccionó DEF-001 como dictamen final. |
| DEF-003 | Dictamen alternativo: no apto | No seleccionado | No corresponde al cierre actual | Crítica | NO APLICA | No existen fallos críticos o altos abiertos que impidan el uso académico documentado. |

---

## 7. Resumen de ejecución

| Métrica | Cantidad |
|---|---:|
| Total de pruebas planificadas | 106 |
| Aprobadas | 106 |
| Fallidas | 0 |
| Bloqueadas | 0 |
| No aplican | 0 |
| Pendientes | 0 |
| Defectos críticos abiertos | 0 |
| Defectos altos abiertos | 0 |
| Defectos medios abiertos | 0 |
| Defectos bajos abiertos | 0 |

> El total debe actualizarse si se agregan, eliminan o agrupan casos durante la ejecución formal.

---

## 8. Dictamen de pruebas

Marcar una sola opción:

- [x] **APTO PARA EVIDENCIA Y DEFENSA:** cumple los criterios de aceptación y no presenta fallos críticos o altos abiertos.
- [ ] **APTO CON OBSERVACIONES:** funciona, pero mantiene defectos medios/bajos documentados que no impiden su uso académico.
- [ ] **NO APTO:** presenta defectos críticos/altos que impiden garantizar el flujo documentado.

### Observación general

```text
La versión evaluada de PhishGuard Antares fue ejecutada y validada en entorno Windows y Ubuntu. La versión final limpia fue empaquetada en formato .7z, verificada con 7-Zip y acompañada de hash SHA-256. No quedan pruebas funcionales pendientes.
```

### Limitaciones confirmadas durante las pruebas

```text
El sistema es un prototipo académico orientativo. No reemplaza herramientas profesionales de ciberseguridad. Las URL se procesan como texto: no se abren, no se visitan y no se consultan servicios externos.
```

---

## 9. Aprobación

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Responsable de ejecución | Pedro Pablo Ciancio González | | |
| Revisor técnico/tutor | | | |
| Observador adicional | | | |

---

## 10. Declaración de cierre

La aprobación de este checklist certifica que la versión evaluada fue sometida a pruebas funcionales, técnicas, visuales, de seguridad y compatibilidad dentro del alcance académico definido. No certifica ausencia absoluta de vulnerabilidades ni convierte al prototipo en una solución comercial de ciberseguridad. Los resultados se limitan al entorno, versiones, entradas y evidencias documentadas.
