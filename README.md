# Pit Wall · Workshop de agentes AI

Sitio educativo en español para participantes del workshop de agentes Director.
El proyecto de carrera de referencia está en `pitwall-redbull`, rama `tests`.

## Ruta publicada

Fundamentos → arquitectura → reglas → Director → laboratorio → recursos.
Las páginas de preparación local y despliegue se retiraron. Los participantes
trabajan localmente con Python; la ruta no exige Docker ni un despliegue en OCI.
La organización entrega servidor, ID, token de equipo y API key del LLM.
Laboratorio contiene la secuencia completa para configurar y ejecutar el proceso.

`kit-director/` y `downloads/kit-director.zip` conservan material de la dinámica
anterior para revisión posterior. El ZIP se excluye del sitio publicado y no se
enlaza en la navegación. No debe usarse como guía de la dinámica actual.
El resto de contenidos se seguirá ajustando por etapas a la nueva dinámica.

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

## Alcance actual

El 27/10/2026 se revisaron README, guía de equipos y plantilla HTTP de la rama
`tests` del proyecto de carrera. Se retiraron las dos páginas solicitadas y se
ajustaron navegación, enlaces y requisitos contradictorios de las páginas restantes.
La adaptación completa de reglas, ejercicios y materiales continuará por etapas.
El historial de las decisiones anteriores está en `docs/REVISION.md`.

## Ejecución local confirmada

El recorrido actual usa el developer kit público `https://github.com/mxai-tech/kit-pitwall`,
revisión consultada `75724a800d7d7208c84027145d8314fbc89562a3`. La inferencia usa API key
sobre `/20231130/actions/v1` en Chicago y el modelo `openai.gpt-oss-120b`. No exige
proyecto ni perfil IAM. `downloads/agente.py` refleja ese cliente, con 120b como
valor predeterminado del workshop.

`downloads/ejecutar_director.py` carga el `.env` contiguo, inicia `Agente`, espera su
tarea y cierra recursos al salir. `downloads/probar_llm.py` comprueba el acceso al
modelo antes de abrir la conexión de carrera. Ambos requieren `python-dotenv`,
que el laboratorio instala expresamente además de las dependencias del kit.

El proceso de carrera conserva el WebSocket saliente y las tres consultas HTTP
internas ya implementadas en el kit. Las rutas se verificaron contra el servidor
y no se muestran en las instrucciones para participantes. No se solicita URL
de invocación, publicación en OCIR ni registro de una aplicación hospedada.

La prueba real de inferencia y carrera requiere las credenciales del evento;
las comprobaciones automatizadas usan transporte simulado y claves ficticias.
