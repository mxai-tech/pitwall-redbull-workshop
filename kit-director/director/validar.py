"""Validación y limpieza de órdenes del lado del Director.

Es la misma regla que aplica el servidor: así el Director corrige antes de
mandar y no pierde la ventana por un campo mal escrito.
"""
from __future__ import annotations

SECOS = ("BLANDO", "MEDIO", "DURO")
MOJADOS = ("INTER", "LLUVIA")
COMPUESTOS = SECOS + MOJADOS
RITMOS = ("ATAQUE", "CARRERA", "CONSERVAR")
ENERGIAS = ("BOOST", "EQUILIBRIO", "RECARGA")
ALERONES = ("ALTA_CARGA", "MEDIA_CARGA")

SINONIMOS = {
    "SOFT": "BLANDO", "MEDIUM": "MEDIO", "HARD": "DURO", "INTERMEDIA": "INTER", "INTERMEDIO": "INTER",
    "INTERMEDIOS": "INTER", "WET": "LLUVIA", "BLANDOS": "BLANDO", "MEDIOS": "MEDIO", "DUROS": "DURO",
    "NONE": "NINGUNO", "NO": "NINGUNO", "NADA": "NINGUNO", "": "NINGUNO",
    "ATTACK": "ATAQUE", "PUSH": "ATAQUE", "CONSERVE": "CONSERVAR", "RACE": "CARRERA",
    "BALANCE": "EQUILIBRIO", "RECHARGE": "RECARGA", "ALTA": "ALTA_CARGA", "MEDIA": "MEDIA_CARGA",
}


def _mayus(v) -> str:
    s = str(v or "").strip().upper().replace(" ", "_")
    return SINONIMOS.get(s, s)


def recortar(texto, palabras: int = 20) -> str:
    return " ".join(str(texto or "").replace("\n", " ").split()[:palabras])


def normalizar_orden(d: dict) -> dict:
    """Acepta respuestas un poco desordenadas del LLM y las deja en el formato del contrato."""
    pits = d.get("pits", "NINGUNO")
    if isinstance(pits, str):
        pits = {"compuesto": pits}
    if not isinstance(pits, dict):
        pits = {"compuesto": "NINGUNO"}
    comp = _mayus(pits.get("compuesto", "NINGUNO"))
    salida_pits = {"compuesto": comp}
    if comp != "NINGUNO":
        try:
            v = int(pits.get("vuelta", 1))
        except (TypeError, ValueError):
            v = 1
        salida_pits["vuelta"] = max(1, min(6, v))
    return {
        "ritmo": _mayus(d.get("ritmo", "CARRERA")),
        "energia": _mayus(d.get("energia", "EQUILIBRIO")),
        "pits": salida_pits,
        "radio": recortar(d.get("radio", "")),
        "razonamiento": str(d.get("razonamiento", ""))[:600],
    }


def validar_orden(d: dict) -> list[str]:
    errores = []
    if d.get("ritmo") not in RITMOS:
        errores.append(f"ritmo debe ser uno de {list(RITMOS)}")
    if d.get("energia") not in ENERGIAS:
        errores.append(f"energia debe ser uno de {list(ENERGIAS)}")
    pits = d.get("pits") or {}
    comp = pits.get("compuesto", "NINGUNO")
    if comp not in ("NINGUNO",) + COMPUESTOS:
        errores.append(f"pits.compuesto debe ser NINGUNO o uno de {list(COMPUESTOS)}")
    if comp != "NINGUNO" and not (isinstance(pits.get("vuelta"), int) and 1 <= pits["vuelta"] <= 6):
        errores.append("pits.vuelta debe ser un entero de 1 a 6")
    return errores


def normalizar_setup(d: dict, permitidas: list[str] | None = None) -> dict:
    return {
        "llanta_salida": _mayus(d.get("llanta_salida", "MEDIO")),
        "aleron": _mayus(d.get("aleron", "ALTA_CARGA")),
        "ritmo": _mayus(d.get("ritmo", "CARRERA")),
        "energia": _mayus(d.get("energia", "EQUILIBRIO")),
        "radio": recortar(d.get("radio", "")),
        "razonamiento": str(d.get("razonamiento", ""))[:600],
    }


def validar_setup(d: dict, permitidas: list[str]) -> list[str]:
    errores = []
    if d.get("llanta_salida") not in permitidas:
        errores.append(f"llanta_salida debe ser una de {permitidas}")
    if d.get("aleron") not in ALERONES:
        errores.append(f"aleron debe ser uno de {list(ALERONES)}")
    if d.get("ritmo") not in RITMOS:
        errores.append(f"ritmo debe ser uno de {list(RITMOS)}")
    if d.get("energia") not in ENERGIAS:
        errores.append(f"energia debe ser uno de {list(ENERGIAS)}")
    return errores
