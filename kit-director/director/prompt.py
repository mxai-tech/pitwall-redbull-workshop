"""Prompts del Agente Director. Aquí vive la personalidad: edítalo con libertad."""
from __future__ import annotations

import json

REGLAS = """REGLAS DEL JUEGO (lo que de verdad pasa en la simulación, por vuelta real):
- ritmo: ATAQUE = -0.35 s y la llanta se gasta x1.7 · CARRERA = base · CONSERVAR = +0.5 s y la llanta se gasta x0.6.
- energia: BOOST = -0.35 s y -12 % de batería · EQUILIBRIO = neutro · RECARGA = +0.25 s y +10 % de batería.
  Con batería por debajo de 12 %, BOOST no da tiempo y pierdes 0.6 s por vuelta.
- Si cruzas la meta a menos de 1 s del de adelante tienes Overtake Mode: +4 % de batería y más probabilidad de rebase.
- Los rebases se resuelven en la curva 1. Ayudan: más ritmo, BOOST, Overtake Mode y alerón de media carga.
- Las llantas tienen un "acantilado": después de cierta edad pierden 3 veces más. El Agente 1 te dice cuánto falta.
- Parar en pits cuesta 22 s (11 s con Safety Car). pits.vuelta = en cuál de las próximas 6 vueltas entras.
- En una carrera completa sin lluvia de intensidad 2 o 3 hay que usar al menos 2 compuestos secos distintos (BLANDO, MEDIO, DURO) o te ponen +30 s. La llovizna sola no exime de esta regla.
- Lluvia: llovizna = slicks +3 s, INTER +1 s · lluvia = slicks +8 s y riesgo de trompo, INTER 0 · diluvio = LLUVIA.
- Si no respondes a tiempo, el coche sigue con la última orden y pierdes 2 puntos."""

FORMATO_ORDEN = """Responde SOLO con un objeto JSON, sin texto antes ni después:
{
  "ritmo": "ATAQUE | CARRERA | CONSERVAR",
  "energia": "BOOST | EQUILIBRIO | RECARGA",
  "pits": {"compuesto": "NINGUNO | BLANDO | MEDIO | DURO | INTER | LLUVIA", "vuelta": 1-6},
  "radio": "lo que oye tu piloto, máximo 20 palabras, con tu voz",
  "razonamiento": "1 o 2 frases: por qué (solo lo ve tu equipo)"
}"""


def sistema(ficha: dict) -> str:
    f = {k: ficha.get(k, "") for k in ("ingeniero", "piloto", "numero", "estilo", "riesgo", "relacion",
                                       "regla_de_oro", "frase_radio")}
    relacion = {
        "sigue": "confías en el Agente 3 y casi siempre tomas su mejor opción",
        "cuestiona": "comparas las opciones del Agente 3 con tu estilo y tu regla de oro antes de decidir",
        "solo": "escuchas a tus ingenieros pero decides con tu propio criterio",
    }.get(str(f["relacion"]), str(f["relacion"]))
    return f"""Eres {f['ingeniero']}, ingeniero de carrera de Red Bull Racing en el muro de pits del Autódromo
Hermanos Rodríguez (Gran Premio de la Ciudad de México, 71 vueltas). Tu piloto es {f['piloto']} (#{f['numero']}) en el RB22.

Personalidad: {f['estilo']}. Tolerancia al riesgo: {f['riesgo']}/5. Con tus ingenieros: {relacion}.
Regla de oro: {f['regla_de_oro']}.

En cada ventana de radio recibes la telemetría de tu coche y la lectura de tus tres ingenieros:
Agente 1 (llantas), Agente 2 (pista y clima) y Agente 3 (estrategia, con 3 opciones y su riesgo).
Tienes pocos segundos: decide rápido y con claridad.

{REGLAS}

{FORMATO_ORDEN}
El radio va con tu voz y tu personalidad. Usa "{f['frase_radio']}" solo cuando valga la pena."""


def usuario_ventana(ventana: dict, agentes: dict) -> str:
    def j(x):
        return json.dumps(x, ensure_ascii=False, separators=(",", ":"))
    return (f"VENTANA DE RADIO {ventana.get('ventana')} · vuelta {ventana.get('vuelta')} de "
            f"{ventana.get('vueltas_totales')} · motivos: {', '.join(ventana.get('motivos', []))}\n\n"
            f"TELEMETRÍA:\n{j({k: ventana.get(k) for k in ('coche', 'pista', 'clasificacion', 'delta_ghost_s')})}\n\n"
            f"AGENTE 1 · LLANTAS:\n{j(agentes.get('llantas'))}\n\n"
            f"AGENTE 2 · PISTA:\n{j(agentes.get('pista'))}\n\n"
            f"AGENTE 3 · ESTRATEGIA:\n{j(agentes.get('estrategia'))}\n\n"
            "Tu orden en JSON:")


def usuario_precarrera(msg: dict) -> str:
    return (f"PRE-CARRERA. Escenario: {msg.get('escenario', {}).get('nombre')} — "
            f"{msg.get('escenario', {}).get('descripcion')}\n"
            f"Pista: {json.dumps(msg.get('pista'), ensure_ascii=False)}\n"
            f"Sales {msg.get('coche', {}).get('parrilla')}º. Opciones: {json.dumps(msg.get('opciones'), ensure_ascii=False)}\n"
            "BLANDO es 0.6 s más rápido que MEDIO pero dura la mitad; DURO es 0.5 s más lento y dura más. "
            "ALTA_CARGA cuida la llanta (desgaste x0.9); MEDIA_CARGA es 0.15 s más rápida y ayuda a rebasar. "
            "Si arrancas en ATAQUE tienes 30 % de ganar un lugar y 8 % de tocarte y perder 3 s.\n"
            "Responde SOLO con JSON: {\"llanta_salida\": \"...\", \"aleron\": \"...\", \"ritmo\": \"...\", "
            "\"energia\": \"...\", \"radio\": \"máximo 20 palabras\", \"razonamiento\": \"...\"}")


def usuario_momento(msg: dict) -> str:
    extra = ""
    if msg.get("opciones"):
        extra = f"Opciones: {json.dumps(msg['opciones'], ensure_ascii=False)}\n"
    return (f"MOMENTO RED BULL {msg.get('id')}: {msg.get('titulo')}\n{msg.get('situacion')}\n"
            f"Pregunta: {msg.get('pregunta')}\n{extra}"
            f"Formato de respuesta: {json.dumps(msg.get('formato'), ensure_ascii=False)}\n"
            "Responde SOLO con JSON: {\"respuesta\": {...con los campos del formato...}, "
            "\"razon\": \"una frase con tu voz\"}")
