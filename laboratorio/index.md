---
title: "Programa una decisión"
lead: "Mueve un parámetro, prepara una situación y descubre por qué tu Director activaría BOOST."
eyebrow: 05 / LABORATORIO DE TU ESCUDERÍA
next_url: /recursos/
next_title: Consulta los recursos del taller
---
## Explora el criterio de tu equipo

Usa este laboratorio para anticipar una decisión. Cambia una condición a la vez y explica por qué elegirías BOOST o EQUILIBRIO. Después contrasta tu hipótesis con las decisiones del Director en el entorno del workshop.

## Tu primera regla de energía

Este ejercicio reproduce la idea de la referencia visual: cambia una reserva mínima y observa una decisión. **Es una regla didáctica ejecutada en JavaScript**, equivalente al Python mostrado. No ejecuta Python, no consulta OCI y no envía órdenes a la carrera.

<div id="energy-lab" class="lab-grid"><section class="lab-card"><span class="tag">01 / TU MISIÓN</span><h3>¿Cuándo usar BOOST?</h3><p>Compara la batería disponible con tu reserva mínima. Después exige también que haya un rival cerca.</p><label class="check-label"><input id="require-rival" type="checkbox" checked> Exigir un rival cercano</label><div class="lab-tip"><strong>Piensa en seis vueltas</strong><p>Una decisión permanece activa entre ventanas. Activar BOOST con reserva suficiente para una vuelta no garantiza energía para las siguientes.</p></div></section><section class="lab-card code-card"><span class="tag">02 / TU CÓDIGO PYTHON</span><h3>La función de energía</h3><pre><code id="energy-code"></code></pre><p class="muted">El código se actualiza con los controles. Úsalo para comprender la condición que representa cada control.</p><button type="button" class="button secondary" id="download-energy">Descargar fragmento .py ↓</button></section><section class="lab-card"><span class="tag">03 / EXPERIMENTA</span><h3>Tu reserva de batería</h3><label for="threshold">Reserva mínima <output id="threshold-value" for="threshold">40 %</output></label><input id="threshold" type="range" min="12" max="100" value="40"><label for="rival-gap">Rival cercano: menos de <output id="gap-value" for="rival-gap">1.0 s</output></label><input id="rival-gap" type="range" min="0.1" max="3" step="0.1" value="1"><hr><h4>Prepara una situación</h4><label for="battery">Batería disponible (%)</label><input id="battery" type="number" min="0" max="100" value="50"><label class="check-label"><input id="has-rival" type="checkbox" checked> Hay un rival adelante</label><label for="distance">Distancia al rival (segundos)</label><input id="distance" type="number" min="0" step="0.1" value="0.8"><div class="button-row"><button type="button" class="button primary" id="test-energy">Probar decisión →</button><button type="button" class="button secondary" id="reset-energy">Restaurar</button></div></section></div>
<div class="decision-result" id="energy-result" role="status" aria-live="polite"><span class="tag">¿QUÉ DECIDIÓ TU DIRECTOR?</span><p>Prepara tu primera prueba y pulsa “Probar decisión”.</p></div>

## Tres pruebas para discutir

| Situación | Qué investigar |
| --- | --- |
| 50 % de batería; rival a 0.8 s; reserva 40 % | Por qué se activa BOOST |
| 30 % de batería; mismo rival y reserva | Qué condición lo impide |
| 80 % de batería; sin rival adelante | Cómo cambia al quitar “Exigir un rival cercano” |

La función devuelve `EQUILIBRIO` cuando no se cumplen las condiciones. No incluye recarga, lluvia, Safety Car, desgaste ni defensa. En el Director completo debes incorporar esas señales y evaluar una orden de varios campos.

## Lleva el experimento a OCI

1. Describe esta regla en el prompt y prepara una ventana comparable.
2. Prueba el Director en el entorno del workshop y observa su respuesta.
3. Observa si el modelo sigue el criterio o justifica una excepción.
4. Compara la orden con el límite que habías definido y detecta posibles excepciones.
5. Registra la decisión y el tiempo de respuesta para comparar intentos.

## Registra lo que aprendiste

Descarga la [bitácora de experimentos]({{ '/downloads/bitacora.csv' | relative_url }}) y guarda una fila por intento. Incluye ficha, escenario, orden, fuente, latencia y resultado. Cambia una variable a la vez y evita decidir a partir de una sola carrera.
