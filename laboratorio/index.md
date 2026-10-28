---
title: "Conecta tu Director a la carrera"
lead: "Prepara Python, configura los accesos entregados, personaliza tu estrategia y ejecuta el Director localmente."
eyebrow: 05 / LABORATORIO
next_url: /recursos/
next_title: Consulta el developer kit y los materiales
---
## Lo que vas a completar

Al finalizar tendrás un **proceso de Python en tu computadora** que recibe telemetría de carrera, obtiene las recomendaciones de los tres especialistas, consulta `openai.gpt-oss-120b` mediante Responses API y envía una decisión al servidor.

La organización te entrega **antes de comenzar** cuatro datos: la URL del servidor de carrera, el ID de tu equipo, su token y la API key de OCI. No necesitas Docker ni publicar tu Director como aplicación en OCI.

## 1. Prepara tu computadora

Necesitas Python 3.11 o posterior, Git, un editor y acceso de red al servidor de carrera y al servicio de OCI. Comprueba en una terminal:

```bash
python3 --version
git --version
```

En Windows puedes usar `python --version`. Los ejemplos siguientes usan `python` después de activar el entorno virtual. Si tienes varias versiones, utiliza una compatible para crearlo.

## 2. Clona el developer kit y crea el entorno

Abre una terminal en la carpeta donde guardarás el proyecto:

```bash
git clone https://github.com/mxai-tech/kit-pitwall.git
cd kit-pitwall
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En PowerShell de Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias del kit y el lector de `.env` que usan los scripts de este laboratorio:

```bash
python -m pip install -r requirements.txt
python -m pip install python-dotenv
```

**Comprueba:** la instalación termina sin errores y `python --version` muestra la versión elegida. Mantén el entorno activado en las terminales desde las que ejecutes el Director.

## 3. Añade los scripts de ejecución local

Descarga estos dos archivos y guárdalos **en la raíz de `kit-pitwall`**, junto a `agente.py` y `estrategia.py`:

| Archivo | Función |
| --- | --- |
| [probar_llm.py]({{ '/downloads/probar_llm.py' | relative_url }}) | Verificar la API key y obtener una respuesta del modelo |
| [ejecutar_director.py]({{ '/downloads/ejecutar_director.py' | relative_url }}) | Cargar `.env` y mantener el Director conectado a carrera |

El kit público utiliza Responses API con el endpoint de API keys. 

La carpeta debe contener al menos:

```text
kit-pitwall/
  agente.py
  estrategia.py
  requirements.txt
  .env.example
  probar_llm.py
  ejecutar_director.py
  .venv/
```

Estos scripts arrancan un proceso local; no necesitas utilizar el servidor HTTP de `main.py` para este recorrido.

## 4. Configura los accesos en .env

La primera vez, copia la plantilla. En macOS o Linux:

```bash
cp .env.example .env
```

En PowerShell:

```powershell
Copy-Item .env.example .env
```

Abre `.env` en tu editor y reemplaza los marcadores con los datos entregados:

```dotenv
EQUIPO=REEMPLAZAR_ID_DEL_EQUIPO
TOKEN=REEMPLAZAR_TOKEN_DE_CARRERA
SERVIDOR=wss://REEMPLAZAR_HOST_DE_CARRERA
OCI_GENAI_REGION=us-chicago-1
OCI_GENAI_MODEL=openai.gpt-oss-120b
OCI_GENAI_API_KEY=REEMPLAZAR_API_KEY_ENTREGADA
```

| Valor | Cómo completarlo |
| --- | --- |
| `EQUIPO` | ID exacto que asignó la organización |
| `TOKEN` | Token de ese equipo; es distinto de la API key del modelo |
| `SERVIDOR` | URL base de carrera para la conexión del Director |
| `OCI_GENAI_REGION` | `us-chicago-1` |
| `OCI_GENAI_MODEL` | `openai.gpt-oss-120b` |
| `OCI_GENAI_API_KEY` | Clave entregada para la inferencia en OCI |

Si te entregan una dirección web `https://HOST`, usa `wss://HOST` para `SERVIDOR`; si es `http://HOST:PUERTO`, usa `ws://HOST:PUERTO`. Conserva el puerto indicado y utiliza solo la base, sin rutas de pantallas ni parámetros. La organización puede entregarte directamente la dirección con `ws://` o `wss://`.

La base URL de inferencia que construye el kit es:

```text
https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1
```

Este recorrido usa **API key**, sin `OCI_GENAI_PROJECT_ID`, perfil IAM ni configuración de un proyecto nuevo. El cliente envía las peticiones a `/responses` sobre esa base, de acuerdo con la [documentación de API keys de OCI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm).

Conserva `.env` en tu computadora y fuera de Git. No vuelvas a copiar la plantilla sobre un archivo ya configurado. Los scripts descargados cargan `.env` al arrancar y dan prioridad a sus valores frente a variables previas de la terminal.

## 5. Comprueba el acceso al modelo

Antes de conectar a carrera, ejecuta:

```bash
python probar_llm.py
```

El script envía una petición pequeña con la API key de tu archivo. El resultado esperado es:

```text
OCI OK: openai.gpt-oss-120b respondió mediante Responses API.
```

Esta prueba solo verifica la inferencia: no registra equipos ni conecta al servidor de carrera. Puede esperar hasta 60 segundos; el Director tiene un presupuesto menor durante una ventana real.

La llamada tiene esta forma; la clave se lee del entorno, no se escribe en el código:

```python
cliente = OpenAI(
    base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
    api_key=os.environ["OCI_GENAI_API_KEY"],
)
respuesta = cliente.responses.create(
    model="openai.gpt-oss-120b",
    input="Responde únicamente OK.",
)
```

**Comprueba:** obtienes `OCI OK`. Si aparece un error, resuélvelo antes de iniciar el Director; el respaldo de carrera no demostraría que el LLM está funcionando.

## 6. Personaliza tu Director

Sigue [Diseña tu Director]({{ '/director/' | relative_url }}) y realiza estas tareas en el editor:

1. En `agente.py`, modifica `FICHA`: nombres, estilo, riesgo, relación con Estrategia, regla de oro y frase de radio.
2. En `estrategia.py`, modifica `INSTRUCCIONES`: explica cómo priorizar tiempo, llantas, batería y riesgo ante señales en conflicto.
3. Conserva el modelo `openai.gpt-oss-120b` en `.env`. Así los equipos comparan estrategias con el mismo modelo.
4. Conserva el formato JSON, las funciones de validación y el respaldo del kit.

Por ejemplo, añade al prompt un criterio verificable:

```text
Si la oportunidad de rebase es incierta, prioriza conservar batería.
Compara el tiempo esperado de Estrategia con el desgaste de Llantas.
Explica qué señal determinó la orden y qué recurso estás sacrificando.
```

Define una hipótesis: “un perfil conservador preservará batería durante ventanas sin oportunidades claras”. No necesitas configurar ni llamar por separado a los auxiliares: el Director obtiene sus recomendaciones desde el servidor.

Comprueba la sintaxis sin arrancar la carrera:

```bash
python -c 'import ast; from pathlib import Path; [ast.parse(Path(p).read_text(), filename=p) for p in ("agente.py", "estrategia.py", "ejecutar_director.py")]; print("Sintaxis correcta")'
```

Esto detecta errores de Python, pero no evalúa tu estrategia ni los accesos.

## 7. Ejecuta el Director local

Con `.venv` activo, los archivos guardados y los accesos completos:

```bash
python ejecutar_director.py
```

Espera el mensaje:

```text
Director conectado y autenticado
```

El proceso permanece abierto esperando solicitudes. No necesita que la carrera ya haya arrancado para autenticarse. El kit mantiene la conexión y reconecta ante interrupciones transitorias de red.

**Mantén la terminal y tu computadora activas durante la competición.** Ejecuta un solo Director por ID: si otro proceso toma el control del equipo, la instancia anterior puede detenerse.

## 8. Observa una ventana de prueba

Cuando la organización abra una pre-carrera o una ventana, tu Director:

1. Recibe la situación desde carrera.
2. Obtiene las lecturas de Llantas, Pista y Estrategia.
3. Combina esas señales con tu ficha y prompt.
4. Consulta el LLM por Responses API.
5. Valida la respuesta y envía la orden al servidor.

En los registros busca:

| Registro | Qué demuestra |
| --- | --- |
| `LLM_RESPUESTA` | El modelo devolvió contenido y cuánto duró la consulta |
| `SERVIDOR_RESPUESTA_ENVIADA` con `fuente: llm` | Se envió una orden a partir de la respuesta del modelo |
| `SERVIDOR_RESPUESTA_ENVIADA` con `fuente: respaldo` | Se usó la continuidad mínima por error, demora o respuesta inválida |
| `Servidor rechazó respuesta` | El servidor no aceptó la orden; revisa el mensaje y el formato |

El evento de envío confirma el transporte, no la aceptación del servidor. Revisa también las pantallas de carrera que comparta la organización y los posibles rechazos.

El kit reserva **6.5 segundos para auxiliares y LLM** durante una ventana de carrera, con margen antes del límite del servidor. Si no obtiene una orden válida a tiempo, usa el respaldo. Ajusta la extensión de las instrucciones y comprueba la latencia real con el modelo del evento.

## 9. Ajusta, reinicia y compara

Detén tu Director con **Ctrl+C**. Modifica una sola variable de estrategia —el prompt o el riesgo de la ficha—, guarda los archivos y vuelve a ejecutar:

```bash
python ejecutar_director.py
```

El proceso lee tus cambios al reiniciar. Conserva el ID y token del equipo; no arranques una segunda copia para aplicar la nueva versión.

Descarga la [bitácora de experimentos]({{ '/downloads/bitacora.csv' | relative_url }}) y registra hipótesis, orden, explicación, fuente, latencia y resultado. Compara situaciones similares antes de atribuir una mejora a tu cambio.

## 10. Toma la salida

Antes de la carrera, confirma con tu equipo:

- El modelo respondió en la prueba de OCI.
- El Director local se autenticó con el ID y token entregados.
- Una ventana produjo una orden válida a partir del LLM.
- El radio y la decisión reflejan la personalidad definida.
- La terminal permanecerá abierta con un solo proceso del equipo.

La competición es exclusivamente entre los equipos participantes. Evalúa el resultado de tu estrategia con las reglas y puntos del torneo.

## Si algo falla

| Síntoma | Qué hacer |
| --- | --- |
| No encuentra `agente` o `estrategia` | Ejecuta desde la raíz del kit, junto a los scripts descargados |
| `No module named dotenv` | Activa `.venv` e instala `python-dotenv` en ese entorno |
| Falta una variable | Revisa `.env`, su nombre y que esté junto al script |
| Error OCI 401 o 403 | Confirma la API key y el acceso con la organización |
| Error OCI 400 o 404 | Verifica el endpoint indicado, región y `openai.gpt-oss-120b` |
| No conecta a carrera | Revisa URL base, puerto y conectividad desde tu computadora |
| `autenticacion_rechazada` | Revisa el ID y token de carrera entregados |
| `otro_director_tomo_control` | Detén la otra instancia y vuelve a iniciar una sola copia |
| Siempre usa `respaldo` | Revisa latencia, respuesta JSON y acceso al modelo; repite `probar_llm.py` |

Si falla una dependencia con tu versión de Python, comparte el error con la organización antes de cambiar librerías o modificar la conexión del kit.
