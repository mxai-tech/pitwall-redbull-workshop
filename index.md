---
title: "Tu estrategia.<br>Tu agente. Tu carrera."
eyebrow: PIT WALL / ORACLE AI WORKSHOP
lead: "Construye un Director que escuche a sus especialistas, tome decisiones con personalidad y lleve a tu equipo hasta la meta desde OCI Applications."
caption: "AUTÓDROMO HERMANOS RODRÍGUEZ / 71 VUELTAS / UN MURO CON CRITERIO"
next_url: /fundamentos/
next_title: Entiende las piezas de Oracle AI
---
<div class="hero-callout"><div><span class="tag">EL RETO DEL WORKSHOP</span><h2>No conduces el auto.<br>Diseñas quién decide.</h2><p>Tu equipo desarrolla en Python, usa Responses API, genera su imagen Docker y despliega su Agente Director en Applications de Oracle Enterprise AI. Recibe telemetría, consulta tres agentes preconstruidos y convierte la información en una orden para el servidor de carrera. La competición es exclusivamente entre los equipos participantes del workshop.</p><a class="button primary" href="{{ '/preparacion/' | relative_url }}">Preparar mi equipo <span aria-hidden="true">→</span></a><a class="text-link" href="{{ '/reglas/' | relative_url }}">Conocer las reglas ↗</a></div><div class="hero-telemetry" aria-label="Datos del reto"><div><strong>03</strong><span>AGENTES ESPECIALISTAS</span></div><div><strong>06</strong><span>VUELTAS ENTRE DECISIONES</span></div><div><strong>10<span>s</span></strong><span>VENTANA DE RESPUESTA BASE</span></div></div></div>

## Del dato a la orden

<div class="flow" aria-label="Ciclo de decisión"><div><span>01 / OBSERVA</span><strong>Telemetría</strong><p>Lee llantas, batería, clima y rivales.</p></div><div><span>02 / CONSULTA</span><strong>Tres especialistas</strong><p>Combina señales y compara opciones.</p></div><div><span>03 / DECIDE</span><strong>Tu Director</strong><p>Aplica personalidad y devuelve JSON.</p></div><div><span>04 / ACTÚA</span><strong>Servidor de carrera</strong><p>Valida la orden y simula sus efectos.</p></div></div>

## Qué vas a aprender

- **Oracle Generative AI:** usar un modelo para interpretar contexto y producir una decisión estructurada.
- **Enterprise AI:** conectar razonamiento, herramientas, identidad, validación y observabilidad en un flujo útil.
- **Diseño de agentes:** definir una personalidad, gestionar incertidumbre y responder dentro de un presupuesto de tiempo.
- **Evaluación:** comparar órdenes, latencia y resultados; mejorar con evidencia.

## Agenda de 90–120 minutos

Pensado para asistentes con **Python intermedio**. Cada equipo crea su entorno virtual, modifica código del Director, prueba Responses API, construye la imagen y hace el deployment en la consola de OCI.

| Bloque | Base de 90 min | Sesión de 120 min | Entregable |
| --- | --- | --- | --- |
| Arquitectura y reglas | 10 | 10 | Contrato de decisión comprendido |
| Entorno virtual y acceso OCI | 15 | 15 | Dependencias y llamada Responses verificadas |
| Código del Director y pruebas | 20 | 30 | Prompt, política Python y una prueba propia |
| Imagen Docker y prueba local | 15 | 20 | Imagen `linux/amd64` verificada |
| OCIR y Applications en OCI Console | 20 | 25 | Imagen publicada y deployment activo |
| Carrera y revisión | 10 | 20 | Decisión observada y mejora propuesta |

La ruta completa es más cómoda en **120 minutos**. Para cubrirla en 90, Docker debe estar operativo y los accesos, red, repositorio OCIR y permisos deben quedar preparados antes del evento. Los tiempos de build y aprovisionamiento dependen del entorno.

## Tu ruta de trabajo

<div class="card-grid"><a class="route-card" href="{{ '/fundamentos/' | relative_url }}"><span>01 — COMPRENDE</span><h3>Del modelo al agente</h3><p>Qué aporta OCI y cómo se conectan las piezas de tu muro.</p><b>Explorar fundamentos →</b></a><a class="route-card" href="{{ '/reglas/' | relative_url }}"><span>02 — PLANEA</span><h3>Conoce el juego</h3><p>Llantas, energía, ventanas, puntos y decisiones que tienen un costo.</p><b>Leer las reglas →</b></a><a class="route-card" href="{{ '/director/' | relative_url }}"><span>03 — CONSTRUYE</span><h3>Dale personalidad</h3><p>Ajusta el estilo, el riesgo y la relación con Estrategia.</p><b>Diseñar mi Director →</b></a><a class="route-card" href="{{ '/laboratorio/' | relative_url }}"><span>04 — EXPERIMENTA</span><h3>Desarrolla y despliega</h3><p>Escribe una política, pruébala y continúa con Docker y Applications.</p><b>Abrir el laboratorio →</b></a></div>

## Qué construye tu equipo

Desarrollarás la personalidad, el prompt y una política verificable en Python, con sus pruebas. Revisarás la llamada a Responses API y empaquetarás el runtime HTTP del Director en Docker. Publicarás la imagen en OCIR y crearás tu Application y deployment en OCI Console. El kit aporta el transporte y una base ejecutable; la organización prepara el servidor de carrera en OCI, los especialistas y los accesos.

<div class="notice"><strong>Esta web es tu guía y tu banco de pruebas conceptual.</strong> Desarrolla localmente y ejecuta la versión final en Applications. Descarga el kit y sigue la ruta hasta el deployment.</div>
