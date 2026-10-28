---
title: "Diseña tu Director"
lead: "Personaliza el prompt, la ficha y el modelo de tu equipo para ejecutarlo localmente en Python."
eyebrow: 04 / DISEÑA TU DIRECTOR
next_url: /laboratorio/
next_title: Configura y ejecuta tu Director local
---
## Tres archivos para definir tu estrategia

Tu punto de partida es el [developer kit `mxai-tech/kit-pitwall`](https://github.com/mxai-tech/kit-pitwall). Trabajarás con una copia del repositorio en tu computadora. El Director se ejecuta como un proceso de Python y consulta el modelo en OCI mediante una API key.

En esta sección preparas la personalidad y el criterio del Director. En **Laboratorio** encontrarás todas las tareas: preparar Python, clonar el kit, configurar los accesos entregados, probar el modelo y conectar el Director al servidor de carrera.

| Archivo del kit | Qué personalizas | Qué debe expresar |
| --- | --- | --- |
| `estrategia.py` | La cadena `INSTRUCCIONES` | Cómo comparar señales, priorizar objetivos y tomar decisiones |
| `agente.py` | El diccionario `FICHA` | Identidad, estilo, riesgo y regla de oro del equipo |
| `.env` | Accesos de carrera, API key y modelo | `openai.gpt-oss-120b` en `us-chicago-1` |

El Director usa **OCI Responses API**: envía las instrucciones y la ficha como `instructions`, la situación de carrera como `input` y lee el resultado en `output_text`. Una personalidad útil debe reflejarse en decisiones que puedas explicar y comparar.

## 1. Ubica los archivos del kit

Sigue el [Laboratorio]({{ '/laboratorio/' | relative_url }}) para clonar el repositorio y preparar tu entorno local. Abre `estrategia.py` y `agente.py` en tu editor; conserva los archivos de ejecución y el contrato del kit.

La organización entrega antes del taller la URL del servidor de carrera, el ID y token de tu equipo y la API key de OCI. No necesitas desplegar una aplicación ni instalar Docker.

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

## 4. Configura el modelo del workshop

Todos los equipos usan **`openai.gpt-oss-120b`**, con API key y el endpoint de Chicago. El archivo `.env` debe incluir:

```dotenv
OCI_GENAI_REGION=us-chicago-1
OCI_GENAI_MODEL=openai.gpt-oss-120b
OCI_GENAI_API_KEY=REEMPLAZAR_POR_LA_CLAVE_ENTREGADA
```

El cliente construye esta base URL:

```text
https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1
```

No necesitas configurar `OCI_GENAI_PROJECT_ID` para este recorrido con API key. El [Laboratorio]({{ '/laboratorio/' | relative_url }}) explica cómo completar también el servidor, el ID y token de carrera, cargar `.env` e iniciar el proceso local.

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
- El modelo `openai.gpt-oss-120b` y los accesos entregados configurados en `.env`.
- Una hipótesis que pueda ponerse a prueba, por ejemplo: “conservaremos batería cuando no haya una oportunidad clara de rebase”.

## Qué observarás durante las pruebas

Compara la orden, su explicación, el radio y el tiempo de respuesta. Cambia una variable a la vez: primero el prompt y después el nivel de riesgo, manteniendo el modelo del workshop. Así podrás reconocer qué ajuste produjo un comportamiento distinto.

Una personalidad no garantiza ganar. Tu objetivo es construir un criterio reconocible y comprobar cómo compite frente a los demás equipos participantes.

## Referencia del código

Esta guía utiliza los nombres de archivos y variables del [kit público](https://github.com/mxai-tech/kit-pitwall) El archivo agente.py usa el endpoint de API keys del workshop y conserva la ficha, la validación, el respaldo y la comunicación con carrera. Consulta la [documentación de OCI Responses API](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm). El modelo del workshop es `openai.gpt-oss-120b`.
