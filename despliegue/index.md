---
title: "De tu código a Applications"
lead: "Construye la imagen de tu Director, publícala en OCIR y despliega tu aplicación desde la consola de Oracle Enterprise AI."
eyebrow: 07 / DOCKER Y DEPLOY EN OCI
next_url: /recursos/
next_title: Recursos y contrato de entrega
---
## Tu entregable

Un Director desarrollado por tu equipo, con pruebas, una imagen versionada en OCIR y un deployment activo en **Applications de OCI Generative AI / Enterprise AI**. El código hace la inferencia con Responses API; Applications aloja el runtime que ejecuta ese código.

El servidor de carrera también corre en OCI. La organización comparte su dirección WSS y garantiza la ruta de red desde las Applications a los tres especialistas y al canal WebSocket.

## 1. Revisa el servicio que vas a empaquetar

En el kit, `app.py` arranca el Director y ofrece `/health`, `/ready` y `/status`. Los dos primeros indican que el runtime sigue activo; `/status` distingue si el servidor de carrera confirmó la conexión. El Director sigue atendiendo las ventanas por su conexión **saliente** WebSocket: el servidor de carrera conserva su contrato actual.

La plataforma exige una imagen `linux/amd64`, escucha en `0.0.0.0:8080` y rutas `/ready` y `/health`. El Dockerfile del kit define ese arranque. No necesitas un volumen para el código: la ficha viaja dentro de la imagen. Usa `/tmp` para archivos temporales y no definas las variables reservadas del servicio, como `PORT`.

Fuente: [Preparar imágenes para Applications](https://docs.oracle.com/en-us/iaas/Content/generative-ai/prepare-artifacts.htm).

## 2. Construye y prueba tu imagen

Desde la raíz de `kit-director`, con Docker en ejecución:

```bash
python -m unittest discover -s tests -v
docker buildx build --platform linux/amd64 --load -t pitwall-director:v1 .
```

`--platform` también importa en Mac con Apple Silicon: la arquitectura de tu laptop puede ser distinta de la del runtime. El Dockerfile copia solo fuentes y dependencias; `.dockerignore` excluye configuración local.

Detén el Director local antes de arrancar el contenedor para conservar una sola conexión por equipo:

```bash
docker run --rm --name pitwall-director \
  --platform linux/amd64 \
  --read-only --tmpfs /tmp \
  --env-file .env \
  -p 127.0.0.1:8080:8080 pitwall-director:v1
```

En otra terminal:

```bash
curl -i http://localhost:8080/ready
curl http://localhost:8080/status
```

Espera `200` en readiness y `carrera_conectada: true` en el estado. **Readiness por sí sola no prueba acceso a OCI ni una conexión a carrera.** Comprueba también `python probar_oci.py` y una orden con fuente `llm`. Al finalizar detén el contenedor con `docker stop pitwall-director`.

## 3. Publica en Oracle Container Registry

Obtén el dominio de registry y namespace del evento, y crea o utiliza el repositorio privado asignado. En estos ejemplos sustituye `REGISTRO_OCIR`, `NAMESPACE` y `EQUIPO`:

```bash
docker login REGISTRO_OCIR
docker tag pitwall-director:v1 REGISTRO_OCIR/NAMESPACE/pitwall-director-EQUIPO:v1
docker push REGISTRO_OCIR/NAMESPACE/pitwall-director-EQUIPO:v1
```

El usuario de login incluye el namespace y, para identidades federadas, el dominio. Introduce un **Auth Token de OCI** cuando solicite la contraseña. Es distinto de la Generative AI API key que usa Responses API. Conserva el tag y digest de tu imagen como evidencia de la versión.

Fuente: [Enviar imágenes a OCIR](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm).

## 4. Crea tu Application en la consola

Ve a **Analytics & AI → Generative AI → Applications → Create application**. Usa la región y compartment del taller; asigna un nombre reconocible por equipo.

Configura **Minimum replicas = 1** y **Maximum replicas = 1**: este Director mantiene una sesión de carrera por proceso. En **Environment**, configura los valores de la tabla. En Networking usa la ruta preparada por la organización hacia carrera y OCI inference; en Authentication selecciona **OCI IAM**. Activa los logs de la aplicación. El taller no requiere almacenamiento persistente.

| Variable | Valor |
| --- | --- |
| `LLM_PROVEEDOR` | `oci` |
| `OCI_OPENAI_COMPATIBLE_ENDPOINT` | Endpoint de inferencia de la región, terminado en `/openai/v1` |
| `OCI_PROJECT_ID` | Proyecto de Generative AI del equipo |
| `OCI_LLM_MODEL` | Modelo habilitado |
| `OCI_GENAI_API_KEY` | Clave de Generative AI asignada al equipo |
| `EQUIPO` y `TOKEN` | Identidad y token de carrera |
| `SERVIDOR` | `wss://SERVIDOR_DE_CARRERA_EN_OCI` |

Los valores se inyectan al runtime; no se incorporan como `ARG` o `ENV` secretos en Dockerfile. La autenticación IAM del endpoint entrante es independiente de la clave usada por el Director para llamar a Responses API.

Fuentes: [Crear una Application](https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-application.htm), [permisos de despliegue e imagen](https://docs.oracle.com/en-us/iaas/Content/generative-ai/deploy-permissions.htm).

## 5. Crea y activa el deployment

Abre tu Application, entra en **Deployments** y crea un deployment. Selecciona tu repositorio OCIR y el tag que acabas de publicar. Activa la versión y espera a que termine su aprovisionamiento.

Si la imagen no se puede recuperar, revisa con la organización los permisos de lectura de OCIR. Cambiar el código local no modifica un deployment existente: construye otra versión, sube otro tag y despliega esa imagen.

Fuente: [Crear un deployment](https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-deployment.htm).

## 6. Verifica desde OCI

Copia el endpoint de la Application y añade `/ready` o `/status` al path de invocación indicado por la consola. Desde Cloud Shell con OCI CLI, o desde un perfil local configurado, ejecuta una petición **firmada con OCI IAM**. Sustituye el valor por el endpoint de invocación copiado, sin el path final:

```bash
export PITWALL_APP_URL="URL_DE_INVOCACION_COPIADA_DE_LA_CONSOLA"
oci raw-request --http-method GET --target-uri "${PITWALL_APP_URL}/status"
```

La respuesta de OCI CLI debe incluir estado 200 y `carrera_conectada: true`. Para un endpoint privado, ejecuta la petición desde una red con acceso a ese endpoint. Un `curl` sin autenticación no equivale a la prueba local.

Referencia: [OCI CLI raw-request](https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/raw-request.html).

En Applications con OCI IAM el endpoint usa `hostedApplicationsIam`; cópialo en lugar de construir una URL de memoria. Consulta también los logs del deployment: busca la bienvenida de carrera y la fuente `llm` en una ventana.

Fuente: [Usar el endpoint de Applications](https://docs.oracle.com/en-us/iaas/Content/generative-ai/use-applications.htm).

## 7. Itera una versión

Con la carrera pausada, modifica tu política, ejecuta las pruebas y reconstruye la imagen con `v2`. Publica y activa la nueva versión. Verifica que la versión anterior dejó de atender el equipo y que solo aparece una conexión. Evita deploys durante una ventana de decisión: activar una nueva versión puede interrumpir la sesión.

El patrón de sesión saliente requiere una réplica, un worker y cuidado durante cambios de versión. Si más adelante quieres escalar varios Directores, necesitarás asignar equipos y coordinar el estado fuera del proceso.

## Evidencia para tomar la salida

- Código modificado y al menos una prueba propia de tu política.
- Imagen `linux/amd64` con tag y digest en OCIR.
- Application y deployment activos en OCI Console.
- `/status` confirma conexión y los logs muestran órdenes válidas con fuente `llm`.
- Tu equipo explica una decisión observada y el costo de su estrategia.
