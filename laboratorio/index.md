---
title: "Programa una decisión"
lead: "Mueve un parámetro, prepara una situación y descubre por qué tu Director activaría BOOST."
eyebrow: 06 / LABORATORIO DE TU ESCUDERÍA
next_url: /despliegue/
next_title: Construye Docker y despliega en Applications
---
## Laboratorio de código: de una regla a un deployment

El trabajo principal sucede en tu editor: modifica `director/politica_equipo.py`, añade pruebas y ejecuta el runtime del kit. Usa los controles de abajo como exploración breve; después implementa tu criterio en Python.

```bash
python -m unittest discover -s tests -v
python probar_oci.py
python -m uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1
```

Tu entrega debe incluir una condición nueva, dos casos de prueba y una decisión observada. Al terminar, detén el proceso local y continúa con [Docker y Applications]({{ '/despliegue/' | relative_url }}).

## Tu primera regla de energía

Este ejercicio reproduce la idea de la referencia visual: cambia una reserva mínima y observa una decisión. **Es una regla didáctica ejecutada en JavaScript**, equivalente al Python mostrado. No ejecuta Python, no consulta OCI y no envía órdenes a la carrera.

<div id="energy-lab" class="lab-grid"><section class="lab-card"><span class="tag">01 / TU MISIÓN</span><h3>¿Cuándo usar BOOST?</h3><p>Compara la batería disponible con tu reserva mínima. Después exige también que haya un rival cerca.</p><label class="check-label"><input id="require-rival" type="checkbox" checked> Exigir un rival cercano</label><div class="lab-tip"><strong>Piensa en seis vueltas</strong><p>Una decisión permanece activa entre ventanas. Activar BOOST con reserva suficiente para una vuelta no garantiza energía para las siguientes.</p></div></section><section class="lab-card code-card"><span class="tag">02 / TU CÓDIGO PYTHON</span><h3>La función de energía</h3><pre><code id="energy-code"></code></pre><p class="muted">El código se actualiza con los controles. Descarga el fragmento y úsalo como punto de partida en tu Director.</p><button type="button" class="button secondary" id="download-energy">Descargar fragmento .py ↓</button></section><section class="lab-card"><span class="tag">03 / EXPERIMENTA</span><h3>Tu reserva de batería</h3><label for="threshold">Reserva mínima <output id="threshold-value" for="threshold">40 %</output></label><input id="threshold" type="range" min="12" max="100" value="40"><label for="rival-gap">Rival cercano: menos de <output id="gap-value" for="rival-gap">1.0 s</output></label><input id="rival-gap" type="range" min="0.1" max="3" step="0.1" value="1"><hr><h4>Prepara una situación</h4><label for="battery">Batería disponible (%)</label><input id="battery" type="number" min="0" max="100" value="50"><label class="check-label"><input id="has-rival" type="checkbox" checked> Hay un rival adelante</label><label for="distance">Distancia al rival (segundos)</label><input id="distance" type="number" min="0" step="0.1" value="0.8"><div class="button-row"><button type="button" class="button primary" id="test-energy">Probar decisión →</button><button type="button" class="button secondary" id="reset-energy">Restaurar</button></div></section></div>
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
2. Ejecuta tu Director con OCI y comprueba que la fuente sea `llm`.
3. Observa si el modelo sigue el criterio o justifica una excepción.
4. Si el límite debe ser obligatorio, impleméntalo como validación en Python.
5. Compara con el respaldo por reglas; registra también la latencia.

## Registra lo que aprendiste

Descarga la [bitácora de experimentos]({{ '/downloads/bitacora.csv' | relative_url }}) y guarda una fila por intento. Incluye ficha, escenario, orden, fuente, latencia y resultado. Cambia una variable a la vez y evita decidir a partir de una sola carrera.
