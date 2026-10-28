# Pit Wall · Workshop de agentes AI

Sitio educativo en español para participantes del workshop de agentes Director.
El proyecto de carrera de referencia está en `pitwall-redbull`, rama `tests`.

## Ruta publicada

Fundamentos → arquitectura → reglas → Director → laboratorio → recursos.
Las páginas de preparación local y despliegue se retiraron. Los participantes
trabajan en el entorno del taller; la ruta no exige Docker ni desarrollo local.
El registro de carrera recibe la URL del Director y exige una prueba de conexión.

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
