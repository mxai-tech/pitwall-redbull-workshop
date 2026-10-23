---
title: "Prepara tu equipo"
lead: "Conecta primero un Director que funcione. Después mejora su criterio."
eyebrow: 04 / PREPARACIÓN
next_url: /director/
next_title: Diseña la personalidad de tu Director
---
## Antes de iniciar el taller

El taller asume Python intermedio: funciones, diccionarios, JSON y lectura de código asíncrono. Instala Python, un editor y Docker con Buildx antes del evento. Comprueba `docker version` y `docker buildx version`; el daemon debe estar en ejecución. Usarás OCI CLI desde Cloud Shell para verificar el endpoint desplegado; si prefieres la terminal local, configura también OCI CLI y tu perfil. La organización debe preparar región, proyecto, permisos de Applications y lectura de imágenes, repositorio privado OCIR, Auth Token para publicar y conectividad hacia el servidor de carrera en OCI.

Reserva el bloque de preparación para crear el entorno, validar OCI y conectar el Director. Así tendrás tiempo para construir y probar tu criterio durante el taller.

## Lo que necesitas

- Python 3.12 o posterior, editor de código y Docker con soporte Buildx.
- Acceso a OCI Console, OCIR y Applications en el compartment del evento.
- El [kit del Director]({{ '/downloads/kit-director.zip' | relative_url }}), incluido en este sitio.
- Datos del evento: **ID de equipo, token y dirección WSS del servidor en OCI**.
- Acceso a OCI Generative AI: **endpoint, proyecto, modelo habilitado y autenticación**. La organización confirma región y recursos antes del taller.

Los especialistas y la simulación están en el servidor de la organización. El kit solo contiene el Director; no necesitas instalar ni administrar ese servidor.

## Instala el kit

Descomprime el archivo y abre una terminal en `kit-director`:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-director.txt
cp .env.example .env
```

En Windows activa el entorno con `.venv\Scripts\Activate.ps1`. Si tu instalación usa `python` en lugar de `python3.12`, comprueba que sea 3.12 o posterior.

## Configura Oracle Responses API

Edita `.env` con los datos de tu acceso. El kit usa una **Generative AI API key de OCI**, y la asocia al proyecto configurado. Esta clave es distinta de una clave de otro proveedor y de la clave privada de un perfil OCI.

```dotenv
LLM_PROVEEDOR=oci
OCI_OPENAI_COMPATIBLE_ENDPOINT=https://inference.generativeai.REGION.oci.oraclecloud.com/openai/v1
OCI_GENAI_API_KEY=TU_API_KEY_DE_OCI
OCI_PROJECT_ID=TU_OCID_DE_PROYECTO
OCI_LLM_MODEL=TU_MODELO_HABILITADO
EQUIPO=TU_ID
TOKEN=TU_TOKEN
SERVIDOR=wss://SERVIDOR_DE_CARRERA_EN_OCI
```

La documentación de OCI requiere un proyecto para estas llamadas. Confirma el modelo disponible en tu región; la disponibilidad de herramientas y modelos varía. La clave queda en tu archivo local `.env`.

Consulta [OCI Responses API](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm) y [modelos y regiones](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agentic-regions.htm).

## Verifica OCI antes de competir

Desde la carpeta del kit, ejecuta:

```bash
python probar_oci.py
```

La prueba pide una orden pequeña y verifica que se pueda normalizar y validar. Debe imprimir `OCI OK`. Si faltan variables o la llamada falla, termina con error: esta prueba permite distinguir el acceso real a OCI del modo de respaldo.

## Conecta tu Director

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1
```

El runtime HTTP arranca el Director como tarea de fondo. En otra terminal, consulta `curl http://localhost:8080/status`; espera `carrera_conectada: true`. No ejecutes otro `python -m director` con el mismo equipo. Espera el mensaje de bienvenida. La organización inicia la pre-carrera. El cliente elige el setup y luego atiende las ventanas automáticamente.

Abre el muro que te comparta la organización: `https://SERVIDOR_DE_CARRERA_EN_OCI/equipo.html?equipo=TU_ID&token=TU_TOKEN`. Verás telemetría, lecturas y órdenes del equipo.

## Comprueba tu primera ventana

- El equipo se conecta con un solo Director activo.
- Llega una ventana y las consultas a especialistas terminan.
- El registro indica la fuente `llm`, `reglas` o `respaldo`.
- La orden llega antes del límite y no aparece `orden_error`.
- La explicación es consistente con la ficha y con las lecturas.

**Una carrera completada con `reglas` no demuestra que OCI haya respondido.** Confirma primero la prueba de OCI y después la fuente de las órdenes en el registro.

## Si algo falla

| Síntoma | Qué revisar |
| --- | --- |
| Falta configuración OCI | Completa las cuatro variables OCI del ejemplo |
| 401 o 403 desde OCI | Clave de Generative AI, acceso al proyecto y permisos |
| Modelo o endpoint inválidos | Región, modelo habilitado y base URL terminada en `/openai/v1` |
| Siempre usa reglas | Mensajes `[llm]`, latencia y validez del JSON |
| No conecta al servidor | URL WSS del servidor en OCI, ruta de red y permisos de acceso desde tu entorno |
| Otra conexión tomó el control | Cierra el segundo Director que usa el mismo equipo |
| Respuesta rechazada | Valores permitidos y número de ventana |

Para verificar el transporte sin consumir OCI puedes usar `--proveedor ninguno`. Luego vuelve a OCI para el reto de agentes.
