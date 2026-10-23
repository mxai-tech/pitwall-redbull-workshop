# Pit Wall · Workshop de agentes AI

Sitio educativo en español para participantes. Construyen un Agente Director con
Oracle Generative AI / Enterprise AI Responses API que consulta tres especialistas
preconstruidos y comunica su orden al servidor de carrera en OCI. Cada equipo
crea un entorno virtual, escribe código y pruebas, construye una imagen Docker,
la publica en OCIR y hace deploy desde Applications en OCI Console.

## Estructura

- Jekyll, Markdown, CSS y JavaScript sin dependencias del navegador.
- Ruta: fundamentos → arquitectura → reglas → preparación → Director → laboratorio → Docker y Applications → recursos.
- `despliegue/`: recorrido por Docker, OCIR, Applications y verificación del deployment.
- Configurador descargable de personalidad y laboratorio conceptual de energía.
- `kit-director/`: fuentes Python para participantes, derivadas de `pitwall-redbull/director`.
- `downloads/kit-director.zip`: paquete con Responses API, política Python, pruebas, runtime HTTP y Dockerfile; sin simulador.
- `.github/workflows/pages.yml`: construcción y publicación en GitHub Pages.

Diseño original azul marino / azul de la referencia, con rojo y amarillo. No contiene
logos, imágenes del auto ni recursos remotos. Tipografía del sistema.

## Vista local

Requiere Ruby 3.3 y Bundler:

```bash
bundle install
bundle exec jekyll serve --baseurl /pitwall-redbull-workshop
```

Abre http://localhost:4000/pitwall-redbull-workshop/.
Para otro nombre usa `--baseurl /NOMBRE` o cambia `_config.yml`.

## Publicación (la realiza el propietario)

Git se inicializó en `main`; no se añadió remoto ni se publicó el sitio.
Cuando crees el repositorio y subas los archivos, selecciona Settings → Pages →
Source: GitHub Actions. El workflow usa la ruta de Pages detectada por GitHub,
por lo que no requiere fijar el usuario o la organización en el código.
`url` queda vacío hasta conocer el dominio definitivo.

## Editar y verificar

- Texto: `index.md` y los directorios de cada sección.
- Navegación: `_data/navigation.yml`; estructura: `_layouts/page.html`.
- Paleta: variables al inicio de `assets/css/site.css`.
- Interacciones: `assets/js/site.js`.
- Después de cambiar el kit: `python3 scripts/package_kit.py`.
- Compilar: `bundle exec jekyll build`.
- Comprobar enlaces internos del resultado: `python3 scripts/check_site.py`.
- Pruebas del adaptador (con dependencias del kit instaladas):
  `python -m unittest discover -s tests -v`.
- Pruebas que ejecuta el participante: desde `kit-director`,
  `python -m unittest discover -s tests -v`.

## Alcance de esta primera versión

Las reglas se contrastaron con `config/coeficientes.json`, `server/sim/`,
`server/torneo.py`, los especialistas y el cliente del proyecto base el 22/10/2026.
Las referencias Oracle están enlazadas en Fundamentos y Recursos.
El contenido se concentra en participantes. No se publican configuración de equipos,
credenciales, administración, calibración ni narración del servidor.

El laboratorio web es una regla didáctica equivalente a Python; no ejecuta Python ni
llama a OCI. El kit usa Responses API real desde Python con credenciales del participante.
Las pruebas automáticas usan un cliente simulado; la validación con OCI y la carrera
requiere los recursos del evento y se realiza con `probar_oci.py` y el servidor.

Audiencia confirmada: Python intermedio, 90–120 minutos. La agenda base de 90 minutos
y la distribución de 120 están en Inicio. El despliegue forma parte de ambas rutas;
120 minutos deja más tiempo de práctica. Servidor de carrera confirmado en OCI,
accesible desde Applications. Por confirmar: región/modelo OCI, acceso de
participantes y coeficientes finales del juego. No se prometen tiempos de respuesta
del modelo.

## Runtime de Applications

`kit-director/app.py` sirve en 8080 con un solo worker. El lifespan inicia y detiene
el Director; `/health` y `/ready` verifican la tarea, `/status` distingue la bienvenida
de carrera y muestra la última fuente/latencia. La conexión a carrera es saliente;
no se cambió el contrato del servidor original. Configura una réplica mínima y máxima.
El diagnóstico se protege con OCI IAM en la plataforma.

La política verificable está en `director/politica_equipo.py` y se aplica después
del LLM y de las reglas. La plantilla conserva las paradas de la orden propuesta.
Cada equipo debe extenderla y añadir casos de prueba antes de empaquetar.
La ficha se incorpora a la imagen; `.env` solo se inyecta en ejecución.

La guía usa Linux amd64, 0.0.0.0:8080, health/readiness y el filesystem temporal
según los requisitos oficiales enlazados en Despliegue. Las credenciales de
inferencia, el Auth Token de OCIR y el IAM entrante son mecanismos distintos.

La construcción de imagen y el despliegue real requieren un daemon Docker operativo,
OCIR y acceso al tenancy. No se publicó ninguna imagen ni se crearon recursos OCI.
