---
title: "Diseña tu Director"
lead: "Personaliza el prompt, la ficha y el modelo de tu equipo desde la terminal de OCI."
eyebrow: 04 / DISEÑA TU DIRECTOR
next_url: /laboratorio/
next_title: Continúa con los componentes y la publicación en OCI
---
## Tres archivos para definir tu estrategia

Tu punto de partida es el [developer kit `mxai-tech/kit-pitwall`](https://github.com/mxai-tech/kit-pitwall). Trabajarás en **Cloud Shell, la terminal de la consola de OCI**, con una copia del repositorio para tu equipo.

En esta sección preparas la personalidad y el criterio del Director. En **Laboratorio** continuaremos con los componentes que hay que crear dentro de OCI, la configuración de ejecución y la publicación de la aplicación.

| Archivo del kit | Qué personalizas | Qué debe expresar |
| --- | --- | --- |
| `estrategia.py` | La cadena `INSTRUCCIONES` | Cómo comparar señales, priorizar objetivos y tomar decisiones |
| `agente.py` | El diccionario `FICHA` | Identidad, estilo, riesgo y regla de oro del equipo |
| `.env` | La variable `OCI_GENAI_MODEL` | El identificador del modelo de OCI elegido para el Director |

El Director usa **OCI Responses API**: envía las instrucciones y la ficha como `instructions`, la situación de carrera como `input` y lee el resultado en `output_text`. Una personalidad útil debe reflejarse en decisiones que puedas explicar y comparar.

## 1. Abre Cloud Shell y clona el kit

Entra a la consola de OCI con el acceso del workshop. Selecciona el icono **Cloud Shell / Code Editor** de la cabecera, elige **Cloud Shell** y espera a que aparezca la terminal. Consulta [cómo abrir Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devcloudshellgettingstarted.htm).

Ejecuta:

```bash
git clone https://github.com/mxai-tech/kit-pitwall.git
cd kit-pitwall
ls -a
```

Comprueba que aparecen `estrategia.py`, `agente.py` y `.env.example`. Usa la [versión de agente.py con Responses API]({{ '/downloads/agente.py' | relative_url }}) como reemplazo del archivo del kit antes de personalizar la ficha. Mantén esta copia para continuar en Laboratorio. Si ya la clonaste, entra a su carpeta y conserva tus cambios antes de actualizarla.

Puedes editar los archivos desde un editor disponible en Cloud Shell. Por ejemplo, con `vi`:

```bash
vi estrategia.py
```

En `vi`, pulsa `i` para editar; al terminar, pulsa `Esc`, escribe `:wq` y presiona Enter para guardar y salir. Repite el mismo procedimiento para los otros archivos.

## 2. Modifica el prompt en estrategia.py

Abre [`estrategia.py`](https://github.com/mxai-tech/kit-pitwall/blob/main/estrategia.py) y busca `INSTRUCCIONES`. Es el texto que define las prioridades de tu Director.

Conserva las reglas y el formato de respuesta existentes. Añade tus criterios dentro de la cadena, antes de las comillas triples de cierre. Por ejemplo:

```text
Prioriza terminar cada ventana con recursos para la siguiente decisión.
Compara el desgaste informado por Llantas con el tiempo esperado de Estrategia.
Usa la información de Pista para detectar si una opción depende de lluvia incierta.
Si dos planes tienen tiempos cercanos, elige el de menor riesgo.
Explica qué señal determinó la decisión y respeta la regla de oro del equipo.
```

Tu prompt debe responder cuatro preguntas:

- **Objetivo:** ¿cuándo vale la pena ganar tiempo y cuándo conviene conservar recursos?
- **Evidencia:** ¿qué señal de Llantas, Pista o Estrategia pesa más en un conflicto?
- **Incertidumbre:** ¿cómo reaccionas si el radar y el estado actual no coinciden?
- **Comunicación:** ¿cómo explicas la orden y qué dice el radio del equipo?

Mantén la respuesta en JSON y los valores permitidos de ritmo, energía y pits. La regla de radio sigue siendo un máximo de 20 palabras. Para este ejercicio modifica el prompt; conserva las funciones de validación y respaldo del kit.

## 3. Personaliza la ficha en agente.py

Abre [`agente.py`](https://github.com/mxai-tech/kit-pitwall/blob/main/agente.py) y busca el diccionario `FICHA`. Edita sus valores en Python. Puedes partir de una ficha como esta:

```python
FICHA = {
    "ingeniero": "Ana Vega",
    "piloto": "Leo Montes",
    "numero": 27,
    "estilo": "calculador",
    "riesgo": 3,
    "relacion": "cuestiona",
    "regla_de_oro": "No sacrificar las llantas por una ventaja momentánea",
    "frase_radio": "Cada vuelta cuenta, equipo",
    "descripcion_avatar": "Piloto ficticio con casco azul",
}
```

| Campo | Valores y propósito |
| --- | --- |
| `ingeniero` y `piloto` | Nombres de la voz de estrategia y del piloto ficticio |
| `numero` | Entero de 1 a 99; el kit excluye 3 y 6 |
| `estilo` | `agresivo`, `calculador` o `conservador` |
| `riesgo` | Entero de 1 a 5: tolerancia al riesgo que interpretarás en el prompt |
| `relacion` | `sigue`, `cuestiona` o `solo`, según cómo use las propuestas de Estrategia |
| `regla_de_oro` | Principio que orienta las decisiones del Director |
| `frase_radio` | Una frase reconocible de tu equipo |
| `descripcion_avatar` | Descripción del piloto ficticio |

Conserva comillas, comas y llaves. `numero` y `riesgo` son números, sin comillas. El resto de campos de este ejemplo contiene texto.

La ficha se incorpora a las instrucciones del modelo: no es un conjunto de reglas ejecutables. Si escribes “nunca gastar toda la batería”, después tendrás que observar si el Director interpreta y cumple esa instrucción.

El kit permite sustituir la ficha con `DIRECTOR_FICHA_JSON`. Para que se utilicen tus cambios en `agente.py`, deja esa variable sin definir.

## 4. Prepara .env y elige el modelo

El archivo se llama **`.env`**, con un punto al inicio. Crea tu copia a partir de la plantilla pública:

```bash
cp .env.example .env
vi .env
```

Ejecuta la copia solo al preparar el archivo por primera vez: repetirla sobrescribiría los valores que hayas editado.

Localiza `OCI_GENAI_MODEL`. El valor debe ser el **identificador exacto de OCI**, no solo el nombre comercial “Gemini” o “GPT”. Usaremos las opciones de Gemini y GPT que confirme la organización para el proyecto y la región del evento.

La plantilla actual contiene este ejemplo:

```dotenv
OCI_GENAI_REGION=us-chicago-1
OCI_GENAI_MODEL=openai.gpt-oss-20b
```

`openai.gpt-oss-20b` es el valor predeterminado del repositorio; no representa por sí solo la lista de modelos del workshop. Sustitúyelo por el identificador de la opción que elijas entre las habilitadas por la organización.

Mantén el resto de variables de la plantilla. En Laboratorio completaremos los valores de acceso y ejecución —como proyecto, API key y conexión a carrera— con los datos del entorno de OCI. Conserva `.env` fuera de Git.

**Guardar `.env` prepara la configuración; no la aplica a un proceso.** El Director del kit lee variables de entorno y no carga ese archivo automáticamente. La forma de inyectar los valores al publicar la aplicación se explicará en Laboratorio.

## 5. Revisa tu diseño antes de continuar

Desde la carpeta del repositorio puedes comprobar la sintaxis de los dos módulos sin iniciar el Director ni consultar un modelo:

```bash
python3 -c 'import ast; from pathlib import Path; [ast.parse(Path(p).read_text(), filename=p) for p in ("estrategia.py", "agente.py")]; print("Sintaxis Python correcta")'
```

Esto detecta errores de Python, como comillas sin cerrar. No comprueba credenciales, disponibilidad del modelo ni calidad de la estrategia.

Revisa únicamente los cambios de código:

```bash
git diff -- estrategia.py agente.py
```

Antes de pasar a Laboratorio, tu equipo debe tener:

- Un prompt con prioridades concretas y una regla para resolver señales en conflicto.
- Una ficha coherente con ese prompt.
- La elección de modelo identificada en `.env`.
- Una hipótesis que pueda ponerse a prueba, por ejemplo: “conservaremos batería cuando no haya una oportunidad clara de rebase”.

## Qué observarás durante las pruebas

Compara la orden, su explicación, el radio y el tiempo de respuesta. Cambia una variable a la vez: primero el prompt, después el riesgo o el modelo. Así podrás reconocer qué ajuste produjo un comportamiento distinto.

Una personalidad no garantiza ganar. Tu objetivo es construir un criterio reconocible y comprobar cómo compite frente a los demás equipos participantes.

## Referencia del código

Esta guía utiliza los nombres de archivos y variables del [kit público](https://github.com/mxai-tech/kit-pitwall) y la [versión de agente.py con Responses API]({{ '/downloads/agente.py' | relative_url }}). El archivo conserva la ficha, las variables de entorno, la validación y el respaldo del Director. Consulta la [documentación de OCI Responses API](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm). Elige un modelo con soporte para esta API en la región del evento.
