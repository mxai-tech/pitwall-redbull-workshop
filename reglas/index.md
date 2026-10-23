---
title: "Las reglas del juego"
lead: "Gana con decisiones consistentes: administra llantas y batería, responde a tiempo y adapta tu plan cuando cambie la pista."
eyebrow: 03 / REGLAMENTO DEL WORKSHOP
next_url: /preparacion/
next_title: Prepara tu equipo y conecta OCI
---
## La misión

Tu equipo es un muro de estrategia o "pit wall" en una simulación de Formula 1, a **71 vueltas** en el Autódromo Hermanos Rodríguez. El servidor conduce el auto. Tu Director elige el plan; compite contra otros equipos y contra un **ghost simulado** basado en la estrategia de México 2022. El ghost es una referencia del juego, no una reproducción exacta de la carrera real.

## Cuándo decides

1. **Pre-carrera:** eliges llanta de salida, alerón, ritmo y energía. Límite base: 60 segundos.
2. **Durante la carrera:** hay ventanas en las vueltas 6, 12, 18… 66; pueden abrirse ventanas extra por lluvia o Safety Car.
3. **Cada ventana:** consulta, decide y responde. El límite base es **10 segundos**, configurable por la organización; el mensaje incluye `limite_ms`.
4. **Entre ventanas:** tu orden sigue activa. Piensa en su efecto sobre varias vueltas.

Si no llega una orden válida a tiempo, el auto mantiene su orden anterior y acumula un silencio: **−2 puntos**. Un JSON inválido se rechaza y puedes corregirlo mientras la ventana siga abierta.

## Ritmo: velocidad frente a desgaste

| Ritmo | Cambio de tiempo por vuelta | Multiplicador de edad de llanta |
| --- | --- | --- |
| `ATAQUE` | −0.35 s | ×1.7 |
| `CARRERA` | Base | ×1.0 |
| `CONSERVAR` | +0.50 s | ×0.6 |

## Energía: ahora o después

| Energía | Cambio de tiempo por vuelta | Cambio de batería |
| --- | --- | --- |
| `BOOST` | −0.35 s, si hay batería suficiente | −12 puntos porcentuales |
| `EQUILIBRIO` | Neutro | 0 |
| `RECARGA` | +0.25 s | +10 puntos porcentuales; +7 con calor desde 50 °C |

Con menos de 12 % de batería al iniciar una vuelta en `BOOST`, no recibes su beneficio y sumas 0.6 s. Las reglas de energía anteriores no se aplican igual bajo Safety Car: el motor mantiene la batería durante esas vueltas.

**Piensa en toda la ventana:** seis vueltas de BOOST necesitan hasta 72 puntos de batería, antes de considerar beneficios como Overtake Mode.

## Llantas y paradas

- Secos: `BLANDO`, `MEDIO`, `DURO`. Mojados: `INTER`, `LLUVIA`.
- Acantilados base: 27, 48 y 65 de **edad efectiva** para blando, medio y duro. Al rebasarlos, el término de degradación se multiplica por 3.
- Una parada cuesta **22 s**; bajo Safety Car, **11 s**. Hay una probabilidad de parada lenta.
- `pits.vuelta` va de 1 a 6: en cuál de las siguientes vueltas entras.
- En una carrera completa sin lluvia de intensidad 2 o 3, usa al menos **dos compuestos secos distintos**. Si no lo haces, se suman **30 s**. La llovizna por sí sola no elimina esta regla.

El alerón se elige antes de arrancar: `ALTA_CARGA` reduce el incremento de edad de llanta (×0.9); `MEDIA_CARGA` reduce 0.15 s por vuelta y ayuda al rebase.

## Pista e incertidumbre

| Situación | Implicación |
| --- | --- |
| Llovizna, intensidad 1 | Slicks +3 s por vuelta; INTER +1 s |
| Lluvia, intensidad 2 | Slicks +8 s y riesgo de trompo; INTER sin penalización climática |
| Diluvio, intensidad 3 | LLUVIA sin penalización climática |
| Pista a 55 °C | El término de degradación térmica aumenta ×1.3; la edad no aumenta por temperatura directamente |
| Ataque prolongado desde 50 °C | Más de 18 vueltas consecutivas puede activar sobrecalentamiento y forzar 6 vueltas de conservación |
| Rival a menos de 1 s al cruzar meta | Overtake Mode: +4 puntos de batería y ayuda al rebase |
| Safety Car | Reduce gaps, desgaste y costo de pits |

Son reglas de la simulación del workshop. Los coeficientes pueden ajustarse antes del evento; la organización confirmará los valores vigentes.

## Cómo se gana

| Concepto | Puntos |
| --- | --- |
| Posición en un heat de cuatro equipos | 25 · 18 · 15 · 12 |
| Terminar antes que el ghost | +10 |
| Terminar igual o hasta 5 s después del ghost | +5 |
| Vuelta más rápida | +3 |
| Premio de radio | 0 a 5, asignados por la organización con voto del público |
| Cada silencio | −2 |
| Momentos de clasificación | 0 a 9, una vez para el torneo |

Los Momentos ordenan la parrilla de los heats. La tabla acumula sus puntos y los de las carreras previas a la final. Los cuatro mejores pasan a la final; **la posición de llegada en la final determina el orden final entre los finalistas** en la implementación actual.

## Radio y personalidad

El radio se limita a **20 palabras** y se publica con una ventana de retraso. No cambia el tiempo del auto; sí hace visible la personalidad de tu equipo y participa en el premio de radio. El campo `razonamiento` queda en la vista privada del equipo: úsalo como una explicación breve basada en las señales observadas.

Una regla de oro escrita en un prompt orienta al LLM; no garantiza su cumplimiento. Si tu equipo necesita un límite estricto, debe comprobarlo en código antes de enviar la orden.
