"""Punto de extensión del equipo: restricciones verificables después del LLM.

Reto: implementa aquí tu política, añade pruebas y reconstruye tu imagen.
La política también se aplica a las decisiones por reglas.
"""
from copy import deepcopy


def ajustar_orden(orden: dict, ventana: dict, ficha: dict) -> dict:
    salida = deepcopy(orden)
    reserva = float(ficha.get("reserva_boost", 40))
    bateria = float(ventana.get("coche", {}).get("bateria_pct", 0))
    if salida.get("energia") == "BOOST" and bateria < reserva:
        salida["energia"] = "RECARGA"
        salida["razonamiento"] = (
            str(salida.get("razonamiento", "")) + " Política del equipo: reserva de batería."
        ).strip()[:600]
    return salida
