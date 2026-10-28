---
title: "Un muro. Cuatro agentes."
permalink: /fundamentos/arquitectura.html
lead: "Los especialistas comparten información. Tu Director conserva la responsabilidad de la decisión."
eyebrow: 02 / ARQUITECTURA DEL MURO
next_url: /reglas/
next_title: Aprende las reglas de la carrera
---
## El ciclo de una ventana

<div class="architecture"><div class="architecture-node server-node"><span>SERVIDOR DE CARRERA</span><strong>Abre una ventana y envía telemetría</strong><small>Llamada HTTP · telemetría, especialistas y límite de tiempo</small></div><div class="connector" aria-hidden="true">↓</div><div class="card-grid three"><div class="mini-card"><span>AGENTE 01</span><h3>Llantas</h3><p>Desgaste, edad efectiva, acantilado y consejo.</p></div><div class="mini-card"><span>AGENTE 02</span><h3>Pista</h3><p>Clima, radar, Safety Car, gaps y rivales.</p></div><div class="mini-card"><span>AGENTE 03</span><h3>Estrategia</h3><p>Tres opciones con tiempo esperado y riesgo.</p></div></div><div class="connector" aria-hidden="true">↓ LECTURAS INCLUIDAS EN LA LLAMADA ↓</div><div class="architecture-node director-node"><span>TU AGENTE DIRECTOR + OCI RESPONSES API</span><strong>Contexto + personalidad → propuesta JSON</strong><small>Normaliza · valida · usa respaldo si hace falta</small></div><div class="connector" aria-hidden="true">↓ RESPUESTA JSON ↓</div><div class="architecture-node server-node"><strong>El servidor valida y aplica la orden</strong><small>Nueva telemetría → siguiente decisión</small></div></div>

## Qué aportan los especialistas

**Llantas** estima cuánto falta para el acantilado al ritmo actual. Su edad efectiva cambia con tu ritmo, el alerón y las condiciones; no equivale siempre a vueltas de calendario.

**Pista** informa del clima y de los rivales. Su radar mira a 6 y 12 vueltas: detecta el 70 % de los cambios y puede dar falsas alarmas. Trata el pronóstico como una señal con incertidumbre.

**Estrategia** simula alternativas y entrega tres opciones. Sus supuestos incluyen ausencia de tráfico, rivales en `CARRERA` y clima según el radar. Compara sus propuestas con lo que ves en Pista y Llantas.

Los tres están preconstruidos en el servidor como servicios deterministas. No son tres LLM independientes. Todos los equipos reciben el mismo tipo de análisis para su propia situación.

## Cómo se conecta el equipo

La aplicación de carrera llama a la URL del Director mediante HTTP. En cada ventana envía la telemetría, las lecturas de los especialistas y el formato esperado de respuesta. El Director devuelve su decisión al servidor de carrera.

Durante el registro, el equipo proporciona la URL de su Director y usa **Probar conexión**. Esta prueba comprueba que la aplicación puede llamar al agente y entender su respuesta antes de aceptar el registro.

## El entorno del taller

La organización proporciona el entorno para trabajar con el Director. Los participantes definen su personalidad e instrucciones, realizan pruebas y observan sus decisiones durante la competición.

## Qué puedes cambiar

La personalidad y el criterio del Director distinguen a tu equipo. La simulación y los especialistas son compartidos. Combina o cuestiona sus recomendaciones con argumentos y evalúa el resultado frente a los demás participantes.
