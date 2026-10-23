"""Director por reglas: decide sin LLM según la personalidad de la ficha.

Lo usan los bots, el modo sin internet y el respaldo cuando el LLM tarda o
responde mal. También sirve de ejemplo: un equipo puede mejorar estas reglas
en lugar de (o además de) usar un LLM.
"""
from __future__ import annotations

import random

from .validar import COMPUESTOS, ENERGIAS, MOJADOS, RITMOS, SECOS

NIVEL_RIESGO = {"bajo": 0, "medio": 1, "alto": 2}
NOMBRE = {"BLANDO": "blandos", "MEDIO": "medios", "DURO": "duros", "INTER": "intermedios", "LLUVIA": "de lluvia"}


def _perfil(ficha: dict) -> tuple[str, int, str]:
    estilo = str(ficha.get("estilo", "calculador")).lower()
    try:
        riesgo = max(1, min(5, int(ficha.get("riesgo", 3))))
    except (TypeError, ValueError):
        riesgo = 3
    relacion = str(ficha.get("relacion", "cuestiona")).lower()
    return estilo, riesgo, relacion


def _agresividad(o: dict) -> int:
    orden = o["orden"]
    return (orden["ritmo"] == "ATAQUE") * 2 + (orden["energia"] == "BOOST") - (orden["ritmo"] == "CONSERVAR") * 2


def compuesto_para(restantes: int, usados: list[str], lluvia: int) -> str:
    if lluvia >= 3:
        return "LLUVIA"
    if lluvia >= 1:
        return "INTER"
    if restantes <= 24:
        elegido = "BLANDO"
    elif restantes <= 44:
        elegido = "MEDIO"
    else:
        elegido = "DURO"
    secos = {u for u in usados if u in SECOS}
    if len(secos) == 1 and elegido in secos:
        elegido = "MEDIO" if elegido != "MEDIO" else ("BLANDO" if restantes <= 30 else "DURO")
    return elegido


def _propia(ventana: dict, agentes: dict, estilo: str, riesgo: int) -> tuple[dict, str]:
    coche = ventana["coche"]
    pista_t = ventana["pista"]
    llan = agentes.get("llantas") or {}
    restantes = int(ventana.get("vueltas_restantes", 30))
    comp = coche["llanta"]["compuesto"]
    lluvia = int(pista_t.get("lluvia", 0))
    sc = bool(pista_t.get("safety_car"))
    pron = pista_t.get("pronostico") or []
    usados = coche.get("compuestos_usados", [comp])
    antes_cliff = float(llan.get("vueltas_antes_acantilado", 30))
    desgaste = float(llan.get("desgaste_pct", 0))
    pits = {"compuesto": "NINGUNO"}
    motivo = "seguimos con el plan"

    if lluvia >= 2 and comp not in MOJADOS:
        pits, motivo = {"compuesto": compuesto_para(restantes, usados, lluvia), "vuelta": 1}, "slicks en mojado"
    elif lluvia == 0 and comp in MOJADOS and not any(p["lluvia"] >= 1 for p in pron[:1]):
        pits, motivo = {"compuesto": compuesto_para(restantes, usados, 0), "vuelta": 1}, "pista seca otra vez"
    elif riesgo >= 4 and comp in SECOS and pron and pron[0]["lluvia"] >= 2:
        pits, motivo = {"compuesto": "INTER", "vuelta": 5}, "apuesta a la lluvia del radar"
    elif sc and restantes > 10 and desgaste > 35:
        pits, motivo = {"compuesto": compuesto_para(restantes, usados, lluvia), "vuelta": 1}, "parada barata con Safety Car"
    elif antes_cliff <= 7 and restantes > antes_cliff:
        k = max(1, min(6, int(antes_cliff) - (1 if riesgo <= 2 else 0)))
        pits, motivo = {"compuesto": compuesto_para(restantes - k, usados, lluvia), "vuelta": k}, "se acerca el acantilado"
    elif len({u for u in usados if u in SECOS}) < 2 and lluvia == 0 and restantes <= 14:
        pits, motivo = {"compuesto": compuesto_para(restantes, usados, 0), "vuelta": 1}, "falta el segundo compuesto"

    gap = coche.get("gap_adelante_s")
    if estilo == "agresivo":
        ritmo = "ATAQUE" if desgaste < 65 else "CARRERA"
    elif estilo == "conservador":
        ritmo = "CONSERVAR" if restantes > 8 and (gap is None or gap > 1.5) else "CARRERA"
    else:
        ritmo = "ATAQUE" if gap is not None and gap < 1.2 and desgaste < 55 else "CARRERA"
    return {"ritmo": ritmo, "energia": "EQUILIBRIO", "pits": pits}, motivo


def _energia(orden: dict, ventana: dict, estilo: str) -> dict:
    coche = ventana["coche"]
    bat = float(coche.get("bateria_pct", 50))
    gap = coche.get("gap_adelante_s")
    atras = coche.get("gap_atras_s")
    sc = bool(ventana["pista"].get("safety_car"))
    if sc:
        orden["energia"] = "EQUILIBRIO"
        return orden
    if estilo == "agresivo":
        orden["energia"] = "BOOST" if bat >= 35 else "RECARGA" if bat < 20 else "EQUILIBRIO"
    elif estilo == "conservador":
        orden["energia"] = "RECARGA" if bat < 70 else "EQUILIBRIO"
    else:
        if gap is not None and gap < 1.0 and bat >= 30:
            orden["energia"] = "BOOST"
        elif atras is not None and atras < 0.8 and bat >= 40:
            orden["energia"] = "BOOST"
        elif bat < 40:
            orden["energia"] = "RECARGA"
    if orden["energia"] == "BOOST" and bat < 15:
        orden["energia"] = "RECARGA"
    return orden


def radio(orden: dict, ventana: dict, ficha: dict, rng: random.Random) -> str:
    coche = ventana["coche"]
    pista_t = ventana["pista"]
    frase = ficha.get("frase_radio") or "Vamos"
    pits = orden.get("pits") or {}
    if pits.get("compuesto", "NINGUNO") != "NINGUNO":
        v = pits.get("vuelta", 1)
        cuando = "esta vuelta" if v == 1 else f"en {v} vueltas"
        return rng.choice([f"Box, box {cuando}. {NOMBRE[pits['compuesto']].capitalize()} listos.",
                           f"Entramos {cuando} por {NOMBRE[pits['compuesto']]}. Confirma.",
                           f"Plan de pits: {cuando}, {NOMBRE[pits['compuesto']]}. {frase}"])
    if pista_t.get("safety_car"):
        return "Safety Car en pista. Respeta el delta y calienta llantas."
    if coche.get("overtake_mode") and orden["energia"] == "BOOST":
        return rng.choice(["Tienes Overtake Mode, BOOST activado: ¡ataca en la curva 1!", f"Overtake Mode listo. {frase}"])
    if pista_t.get("lluvia", 0) >= 1:
        return "Pista mojada, cuida la tracción a la salida de las curvas."
    if orden["ritmo"] == "CONSERVAR":
        return rng.choice(["Cuida las llantas, el plan sigue.", "Gestiona, gestiona. Todavía falta."])
    if orden["ritmo"] == "ATAQUE":
        return rng.choice(["Empuja ahora, es el momento.", f"Modo ataque. {frase}"])
    return rng.choice(["Buen ritmo, mantén el plan.", "Todo en orden, sigue así.", "Copiado. Ritmo de carrera."])


def decidir(ventana: dict, agentes: dict, ficha: dict, rng: random.Random | None = None) -> dict:
    rng = rng or random.Random()
    estilo, riesgo, relacion = _perfil(ficha)
    ops = (agentes.get("estrategia") or {}).get("opciones") or []
    max_riesgo = 0 if riesgo <= 1 else 1 if riesgo <= 3 else 2
    motivo = ""
    if relacion in ("sigue", "cuestiona") and ops:
        aceptables = [o for o in ops if NIVEL_RIESGO.get(o["riesgo"], 1) <= max_riesgo] or ops
        mejor_t = min(o["tiempo_esperado_s"] for o in aceptables)
        if relacion == "sigue":
            elegido = min(aceptables, key=lambda o: o["tiempo_esperado_s"])
        else:
            cerca = [o for o in aceptables if o["tiempo_esperado_s"] <= mejor_t + 3.0]
            if estilo == "agresivo":
                elegido = max(cerca, key=lambda o: (_agresividad(o), -o["tiempo_esperado_s"]))
            elif estilo == "conservador":
                elegido = min(cerca, key=lambda o: (NIVEL_RIESGO.get(o["riesgo"], 1), _agresividad(o)))
            else:
                elegido = min(cerca, key=lambda o: o["tiempo_esperado_s"])
        orden = {k: (dict(v) if isinstance(v, dict) else v) for k, v in elegido["orden"].items()}
        motivo = f"opción del Agente 3: {elegido['nota']} (riesgo {elegido['riesgo']})"
        if relacion == "cuestiona":
            orden = _energia(orden, ventana, estilo)
    else:
        orden, motivo = _propia(ventana, agentes, estilo, riesgo)
        orden = _energia(orden, ventana, estilo)
    orden["radio"] = radio(orden, ventana, ficha, rng)
    orden["razonamiento"] = f"Reglas ({estilo}, riesgo {riesgo}, {relacion}): {motivo}."
    return orden


def pre_carrera(msg: dict, ficha: dict) -> dict:
    estilo, riesgo, _ = _perfil(ficha)
    lluvia = int((msg.get("pista") or {}).get("lluvia", 0))
    permitidas = (msg.get("opciones") or {}).get("llanta_salida", list(SECOS))
    if lluvia >= 2 and "INTER" in permitidas:
        llanta = "LLUVIA" if lluvia >= 3 and "LLUVIA" in permitidas else "INTER"
    elif estilo == "agresivo":
        llanta = "BLANDO"
    elif estilo == "conservador":
        llanta = "MEDIO" if riesgo >= 2 else "DURO"
    else:
        llanta = "MEDIO"
    return {
        "llanta_salida": llanta,
        "aleron": "MEDIA_CARGA" if estilo == "agresivo" else "ALTA_CARGA",
        "ritmo": "ATAQUE" if estilo == "agresivo" or (riesgo >= 4 and msg.get("coche", {}).get("parrilla", 1) > 1) else "CARRERA",
        "energia": "BOOST" if estilo == "agresivo" else "EQUILIBRIO",
        "radio": f"Luces fuera y a la curva 1. {ficha.get('frase_radio', '')}".strip(),
        "razonamiento": f"Reglas ({estilo}, riesgo {riesgo}): salida con {NOMBRE.get(llanta, llanta)}.",
    }


def momento(msg: dict, ficha: dict) -> dict:
    estilo, riesgo, _ = _perfil(ficha)
    i = msg.get("id")
    if i == 1:
        vuelta = {"agresivo": 22, "conservador": 28}.get(estilo, 25)
        return {"respuesta": {"vuelta_parada": vuelta, "compuesto": "MEDIO"},
                "razon": "Blandos usados no aguantan mucho: medios hasta el final."}
    if i == 2:
        dec = "ATACAR" if estilo == "agresivo" or riesgo >= 4 else "CUIDAR" if estilo == "conservador" else "SEGUIR"
        return {"respuesta": {"decision": dec}, "razon": "La curva 1 de México se gana o se pierde en la recta."}
    if i == 3:
        e = "EQUILIBRIO" if estilo == "conservador" and riesgo <= 2 else "BOOST"
        return {"respuesta": {"energia": e}, "razon": "Quedan pocas vueltas: la batería es para usarse."}
    return {"respuesta": dict(msg.get("ejemplo") or {}), "razon": ""}


def azar(ventana: dict, rng: random.Random) -> dict:
    """Bot de prueba: órdenes válidas al azar (con un poco de sentido para no ser ridículo)."""
    coche = ventana["coche"]
    restantes = int(ventana.get("vueltas_restantes", 30))
    pits = {"compuesto": "NINGUNO"}
    if rng.random() < 0.25 and restantes > 5:
        pits = {"compuesto": rng.choice(list(SECOS) + (list(MOJADOS) if ventana["pista"]["lluvia"] else [])),
                "vuelta": rng.randint(1, 6)}
    orden = {"ritmo": rng.choice(RITMOS), "energia": rng.choice(ENERGIAS), "pits": pits}
    if coche.get("bateria_pct", 50) < 15 and orden["energia"] == "BOOST":
        orden["energia"] = "RECARGA"
    orden["radio"] = rng.choice(["¿Y si probamos algo distinto?", "Plan B, o C, o D.", "Confía en el dado."])
    orden["razonamiento"] = "Bot azar: orden aleatoria válida."
    return orden


__all__ = ["decidir", "pre_carrera", "momento", "azar", "compuesto_para", "COMPUESTOS"]
