---
title: "Dale criterio a tu Director"
lead: "La personalidad se traduce en decisiones: cuánto arriesgar, a quién escuchar y qué proteger."
eyebrow: 05 / DISEÑA TU DIRECTOR
next_url: /laboratorio/
next_title: Prueba una decisión en el laboratorio
---
## Ajusta tu ficha

Este configurador genera `ficha.yaml` para el kit. No llama a OCI. Descarga la ficha y reemplaza `director/ficha.yaml` antes de reiniciar el Director.

<div class="personality-tool" id="personality-tool"><div class="control-panel"><label for="engineer">Ingeniero de carrera</label><input id="engineer" value="Lupita Torres" maxlength="60"><label for="driver">Piloto ficticio</label><input id="driver" value="Paco Rendón" maxlength="60"><label for="number">Número (1–99, excepto 3 y 6)</label><input id="number" type="number" min="1" max="99" value="27"><label for="style">Estilo</label><select id="style"><option value="calculador">Calculador</option><option value="agresivo">Agresivo</option><option value="conservador">Conservador</option></select><label for="risk">Tolerancia al riesgo <output id="risk-value" for="risk">3 / 5</output></label><input id="risk" type="range" min="1" max="5" value="3"><label for="relation">Relación con Estrategia</label><select id="relation"><option value="cuestiona">Cuestiona: compara antes de elegir</option><option value="sigue">Sigue: confía en sus opciones</option><option value="solo">Solo: decide con criterio propio</option></select><label for="golden">Regla de oro</label><input id="golden" value="Nunca pasamos el acantilado de las llantas" maxlength="160"><label for="radio">Frase de radio</label><input id="radio" value="Vamos, vamos, es nuestra" maxlength="100"><p class="form-error" id="profile-error" role="status"></p><button type="button" class="button primary" id="download-profile">Descargar ficha.yaml ↓</button></div><div class="preview-panel"><span class="tag">TU FICHA / YAML</span><pre><code id="profile-preview"></code></pre><p id="profile-summary" class="muted"></p></div></div>

## Qué significa cada parámetro

| Parámetro | Efecto buscado |
| --- | --- |
| `estilo` | Agresivo busca oportunidades; calculador balancea; conservador prioriza recursos |
| `riesgo` | 1 a 5: desde evitar apuestas hasta aceptar decisiones dependientes del radar |
| `relacion` | Seguir, cuestionar o usar criterio propio frente a Estrategia |
| `regla_de_oro` | Principio que el prompt pide respetar |
| `frase_radio` | Voz del equipo en los mensajes al piloto |
| Ingeniero, piloto y número | Identidad ficticia para reconocer a tu equipo |

Con LLM son instrucciones interpretadas por el modelo. En el respaldo por reglas, estilo, riesgo y relación seleccionan heurísticas concretas; la regla de oro en texto libre no se evalúa como una condición de código.

## Tu entrega de desarrollo

Trabaja directamente en el editor. En la ruta base tienes 20 minutos; en la sesión de 120 minutos, 30. Entrega cambios de código y una prueba, además de la ficha.

1. Revisa `director/llm.py`: identifica `instructions`, `input`, modelo y límite de salida en `responses.create`.
2. Modifica `director/prompt.py`: obliga a comparar dos señales que puedan entrar en conflicto y a explicar la elección.
3. Extiende `director/politica_equipo.py`: la base cambia BOOST por RECARGA si no alcanza `reserva_boost`. Añade otra condición propia, por ejemplo impedir ataque cuando el coche informa sobrecalentamiento.
4. Añade a `tests/test_politica.py` una prueba para tu nueva condición y otra para una situación en la que no debe intervenir.
5. Ejecuta `python -m unittest discover -s tests -v` y observa una ventana local con OCI.

La función `ajustar_orden(orden, ventana, ficha)` se aplica después del LLM y de las reglas; devuelve una copia sin perder la parada de la propuesta. Mantén el contrato JSON y vuelve a validar. Los errores de la política hacen que el cliente use el respaldo de transporte.

El configurador sigue siendo útil para explorar, pero la entrega incluye código, pruebas y una imagen Docker desplegada. Ajusta también `reserva_boost` en YAML; las descargas del configurador la inician en 40 %.

## Escribe una condición verificable

Como primera ampliación, añade esta condición a `ajustar_orden`, antes de devolver `salida`:

```python
if ventana.get("coche", {}).get("sobrecalentado"):
    salida["ritmo"] = "CONSERVAR"
```

Escribe una prueba con `sobrecalentado=True` y otra con `False`. En ambas comprueba que se conserva `pits`. Después reemplaza o amplía el ejemplo con el criterio propio de tu equipo: cuánta batería reservar según el riesgo, o cuándo cuestionar una propuesta de Estrategia.

## Diseña el prompt

En el kit, edita `director/prompt.py`. La función `sistema(ficha)` construye instrucciones; `usuario_ventana(...)` reúne la telemetría y las tres lecturas.

Prueba una instrucción concreta como esta:

> Antes de elegir, compara batería para toda la ventana, vueltas hasta el acantilado y costo de pits. Cuestiona al Agente 3 si su plan depende de un radar incierto. Explica tu decisión en dos frases y devuelve solo el JSON solicitado.

No cambies los nombres ni los valores permitidos del contrato. Primero ejecuta una decisión válida; después afina cuándo conviene atacar, recargar o parar.

## De una preferencia a un límite

“Cuidar batería” es una preferencia ambigua. “No iniciar BOOST cuando la reserva no cubra la ventana prevista” se puede verificar. Escribe tu regla en el prompt y, si debe cumplirse siempre, implementa la comprobación en `director/politica_equipo.py`; `director/cerebro.py` ya llama a esta función antes de validar y devolver la orden.

Comprueba también que una nueva orden no cancele una parada pendiente por accidente: `pits.compuesto = NINGUNO` la cancela.

## El ciclo de mejora

1. Formula una hipótesis: “con más riesgo aceptaremos antes una apuesta al radar”.
2. Mantén el resto de la ficha y la situación iguales.
3. Compara varias respuestas: orden, explicación, latencia y fuente.
4. Prueba en una carrera y observa batería, llantas y silencios.
5. Conserva el cambio solo si mejora el comportamiento buscado.

Una personalidad no garantiza ganar. El objetivo es construir un Director que tenga criterio reconocible y que puedas evaluar.
