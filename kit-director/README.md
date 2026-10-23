# Director · Código → Docker → Oracle Enterprise AI Applications

Taller de 90–120 minutos para Python intermedio. El servidor de carrera y los tres
especialistas corren en OCI y los prepara la organización.

## Desarrollo local

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-director.txt
cp .env.example .env
```

En Windows: `.venv\Scripts\Activate.ps1`. Completa `.env` con los accesos del evento.
`OCI_GENAI_API_KEY` es una Generative AI API key de OCI; no es el Auth Token de OCIR.
`SERVIDOR` es la URL WSS del servidor de carrera accesible desde la Application.

```bash
python probar_oci.py
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1
```

Desde otra terminal: `curl -i http://localhost:8080/ready` y
`curl http://localhost:8080/status`. No ejecutes a la vez `python -m director`
con el mismo equipo: ambos modos abren la conexión de carrera.

## Trabajo del equipo

1. Modifica `director/prompt.py` y `director/ficha.yaml`.
2. Extiende `director/politica_equipo.py` con una restricción propia y añade una
   prueba a `tests/test_politica.py`. La política se aplica después del LLM y de
   las reglas; los límites físicos siguen siendo responsabilidad del servidor.
3. Revisa la petición `responses.create` de `director/llm.py` y el ensamblado de
   contexto de `director/cerebro.py`.
4. Construye, prueba, etiqueta y sube tu imagen; crea tu Application en OCI Console.

## Imagen y prueba local

```bash
docker buildx build --platform linux/amd64 --load -t pitwall-director:v1 .
docker run --rm --name pitwall-director --platform linux/amd64 --read-only --tmpfs /tmp --env-file .env -p 127.0.0.1:8080:8080 pitwall-director:v1
```

Detén primero el proceso local. Desde otra terminal consulta `/ready` y `/status`.
La imagen no incluye `.env`; los valores se inyectan al arrancar. La ficha sí está
incluida: cada cambio de código o ficha exige otra imagen/tag.

## Publicación de la imagen

Sustituye registro, namespace y repositorio por los del evento:

```bash
docker login REGISTRO_OCIR
docker tag pitwall-director:v1 REGISTRO_OCIR/NAMESPACE/pitwall-director-EQUIPO:v1
docker push REGISTRO_OCIR/NAMESPACE/pitwall-director-EQUIPO:v1
```

El login usa un Auth Token de OCI y el usuario indicado para tu dominio.
En Console → Generative AI → Applications crea la aplicación, configura las variables
de `.env` mediante Environment (sin subir el archivo), crea el deployment con tu
imagen y activa la versión. Usa una réplica mínima y máxima y OCI IAM para autenticar
las peticiones HTTP. Activa logs. La organización proporciona permisos y red.

Verifica `/ready`, `/status` y logs mediante el endpoint y las peticiones firmadas
que indique la organización. `carrera_conectada=true` confirma la bienvenida del
servidor. Una orden con fuente `llm` confirma uso real de OCI durante la carrera.

Este patrón mantiene una conexión saliente de carrera por réplica. No habilites
escalado horizontal ni varios workers; para un despliegue gradual pausa la carrera
y evita dos versiones activas con el mismo equipo. El estado temporal no se comparte
entre instancias. Si tu caso requiere escalado, hay que rediseñar la coordinación.

Las llamadas tienen presupuestos de tiempo y respaldo. Un rechazo `orden_error`
se registra pero no tiene un segundo intento automático. `pits=NINGUNO` cancela una
parada pendiente. La política de ejemplo respeta la parada de la propuesta recibida;
el respaldo del transporte conserva la parada programada.

Referencias:
https://docs.oracle.com/en-us/iaas/Content/generative-ai/prepare-artifacts.htm
https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-application.htm
https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-deployment.htm
