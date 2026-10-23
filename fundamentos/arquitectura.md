---
title: "Un muro. Cuatro agentes."
permalink: /fundamentos/arquitectura.html
lead: "Los especialistas comparten información. Tu Director conserva la responsabilidad de la decisión."
eyebrow: 02 / ARQUITECTURA DEL MURO
next_url: /reglas/
next_title: Aprende las reglas de la carrera
---
## El ciclo de una ventana

<div class="architecture"><div class="architecture-node server-node"><span>SERVIDOR DE CARRERA</span><strong>Abre una ventana y envía telemetría</strong><small>WebSocket · vuelta, batería, llantas, rivales y límite de tiempo</small></div><div class="connector" aria-hidden="true">↓</div><div class="card-grid three"><div class="mini-card"><span>AGENTE 01</span><h3>Llantas</h3><p>Desgaste, edad efectiva, acantilado y consejo.</p></div><div class="mini-card"><span>AGENTE 02</span><h3>Pista</h3><p>Clima, radar, Safety Car, gaps y rivales.</p></div><div class="mini-card"><span>AGENTE 03</span><h3>Estrategia</h3><p>Tres opciones con tiempo esperado y riesgo.</p></div></div><div class="connector" aria-hidden="true">↓ CONSULTAS HTTP EN PARALELO ↓</div><div class="architecture-node director-node"><span>TU AGENTE DIRECTOR + OCI RESPONSES API</span><strong>Contexto + personalidad → propuesta JSON</strong><small>Normaliza · valida · usa respaldo si hace falta</small></div><div class="connector" aria-hidden="true">↓ ORDEN POR WEBSOCKET ↓</div><div class="architecture-node server-node"><strong>El servidor valida y aplica la orden</strong><small>Nueva telemetría → siguiente decisión</small></div></div>

## Qué aportan los especialistas

**Llantas** estima cuánto falta para el acantilado al ritmo actual. Su edad efectiva cambia con tu ritmo, el alerón y las condiciones; no equivale siempre a vueltas de calendario.

**Pista** informa del clima y de los rivales. Su radar mira a 6 y 12 vueltas: detecta el 70 % de los cambios y puede dar falsas alarmas. Trata el pronóstico como una señal con incertidumbre.

**Estrategia** simula alternativas y entrega tres opciones. Sus supuestos incluyen ausencia de tráfico, rivales en `CARRERA` y clima según el radar. Compara sus propuestas con lo que ves en Pista y Llantas.

Los tres están preconstruidos en el servidor como servicios deterministas. No son tres LLM independientes. Todos los equipos reciben el mismo tipo de análisis para su propia situación.

## El contrato de tu Director

| Canal | Uso |
| --- | --- |
| `WS /ws/agente?equipo=ID&token=TOKEN` | Recibir ventanas y enviar órdenes |
| `GET /api/agentes/llantas` | Consultar desgaste y compuesto |
| `GET /api/agentes/pista` | Consultar clima y rivales |
| `GET /api/agentes/estrategia` | Consultar tres planes |

Las consultas HTTP también requieren `equipo` y `token`. El kit implementa estos canales; la configuración del servidor la proporciona la organización.

```json
{
  "tipo": "orden",
  "ventana": 5,
  "ritmo": "ATAQUE",
  "energia": "BOOST",
  "pits": {"compuesto": "MEDIO", "vuelta": 2},
  "radio": "Box en dos vueltas por medios. Empuja ahora.",
  "razonamiento": "Buscamos el undercut antes de que caigan las llantas."
}
```

`ventana` identifica la ventana recibida. `pits.vuelta` es relativa: si la ventana es en la vuelta 30, el valor 2 programa la parada al final de la 32. `NINGUNO` cancela una parada pendiente.

## Del LLM a una acción válida

El LLM devuelve los campos de decisión; el cliente agrega `tipo` y `ventana`. El kit intenta normalizar y validar la propuesta. Si falla OCI o el formato es inválido, usa reglas. Si el cerebro excede el tiempo disponible, el cliente envía una orden de respaldo conservando la parada ya programada.

El servidor confirma con `orden_ok` o rechaza con `orden_error`. Un rechazo mantiene la ventana abierta, pero **el cliente base solo registra el error: no implementa un segundo intento automático**. Observa los registros y corrige la causa antes de competir.

## Dónde corre tu Director

Durante el desarrollo ejecutas el kit en tu entorno virtual. Para competir, el mismo código vive en una imagen Docker desplegada en **Applications de Enterprise AI**. `app.py` expone diagnóstico HTTP y mantiene una tarea de fondo conectada al servidor de carrera, también alojado en OCI.

Usamos una réplica y un worker por equipo. La carrera no necesita invocar el endpoint HTTP para abrir ventanas: utiliza el WebSocket saliente ya establecido. El endpoint de Applications sirve para comprobar el runtime; su autenticación IAM es independiente de los tokens de carrera y de la clave de Responses API.

Continúa con [Docker y Applications]({{ '/despliegue/' | relative_url }}) después de implementar y probar tu política.

## Qué puedes cambiar

La ficha, el prompt y el criterio del Director son el trabajo del equipo. La simulación, los especialistas y la tabla de puntos son compartidos. Consulta las lecturas; combina o cuestiona sus recomendaciones con argumentos.
