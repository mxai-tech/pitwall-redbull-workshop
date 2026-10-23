"""Cerebro del Agente Director: consulta a los Agentes 1, 2 y 3 y decide.

Flujo de cada ventana de radio:
1. Consulta a los tres agentes en paralelo (tarda menos de 1 s).
2. Si hay LLM, le pasa la telemetría y las tres lecturas con la personalidad de
   la ficha y le pide la orden en JSON.
3. Si el LLM tarda, falla o responde algo inválido, decide con reglas.

Para personalizar tu Director edita la ficha, el prompt (prompt.py) o estas
funciones. Lo único fijo es el formato de la orden.
"""
from __future__ import annotations

import asyncio
import random
import time

from . import prompt, reglas
from .politica_equipo import ajustar_orden
from .validar import normalizar_orden, normalizar_setup, validar_orden, validar_setup


class Cerebro:
    def __init__(self, ficha: dict, llm=None, politica: str = "auto", semilla: int | None = None,
                 timeout_llm: float = 6.5, log=print):
        self.ficha = ficha
        self.llm = llm if politica in ("auto", "llm") else None
        self.politica = politica
        self.timeout_llm = timeout_llm
        self.rng = random.Random(semilla)
        self.log = log
        self.sistema = prompt.sistema(ficha)

    async def consultar(self, herramientas) -> dict:
        nombres = ("llantas", "pista", "estrategia")
        res = await asyncio.gather(herramientas.llantas(), herramientas.pista(), herramientas.estrategia(),
                                   return_exceptions=True)
        agentes = {}
        for n, r in zip(nombres, res):
            agentes[n] = {"error": repr(r)} if isinstance(r, Exception) else r
        return agentes

    async def decidir(self, ventana: dict, herramientas) -> dict:
        t0 = time.monotonic()
        if self.politica == "azar":
            orden = reglas.azar(ventana, self.rng)
            orden["fuente"] = "azar"
            return orden
        agentes = await self.consultar(herramientas)
        if self.llm is not None:
            try:
                restante = max(1.0, self.timeout_llm - (time.monotonic() - t0))
                crudo = await asyncio.wait_for(self.llm.json(self.sistema, prompt.usuario_ventana(ventana, agentes)),
                                               timeout=restante)
                orden = normalizar_orden(crudo)
                orden = ajustar_orden(orden, ventana, self.ficha)
                errores = validar_orden(orden)
                if not errores:
                    orden["fuente"] = "llm"
                    orden["agentes"] = agentes
                    return orden
                self.log(f"  [llm] orden inválida ({'; '.join(errores)}): uso reglas")
            except asyncio.TimeoutError:
                self.log("  [llm] tardó demasiado: uso reglas")
            except Exception as e:  # noqa: BLE001
                self.log(f"  [llm] falló ({type(e).__name__}: {e}): uso reglas")
        orden = reglas.decidir(ventana, agentes, self.ficha, self.rng)
        orden = ajustar_orden(orden, ventana, self.ficha)
        errores = validar_orden(orden)
        if errores:
            raise ValueError("Política del equipo inválida: " + "; ".join(errores))
        orden["fuente"] = "reglas"
        orden["agentes"] = agentes
        return orden

    async def pre_carrera(self, msg: dict) -> dict:
        permitidas = (msg.get("opciones") or {}).get("llanta_salida", ["BLANDO", "MEDIO", "DURO"])
        if self.llm is not None:
            try:
                crudo = await asyncio.wait_for(self.llm.json(self.sistema, prompt.usuario_precarrera(msg)),
                                               timeout=min(20.0, msg.get("limite_ms", 60000) / 1000 - 5))
                setup = normalizar_setup(crudo)
                if not validar_setup(setup, permitidas):
                    setup["fuente"] = "llm"
                    return setup
            except Exception as e:  # noqa: BLE001
                self.log(f"  [llm] pre-carrera falló ({type(e).__name__}): uso reglas")
        setup = reglas.pre_carrera(msg, self.ficha)
        setup["fuente"] = "reglas"
        return setup

    async def momento(self, msg: dict) -> dict:
        if self.llm is not None:
            try:
                crudo = await asyncio.wait_for(self.llm.json(self.sistema, prompt.usuario_momento(msg)),
                                               timeout=min(20.0, msg.get("limite_ms", 60000) / 1000 - 5))
                if isinstance(crudo.get("respuesta"), dict):
                    return {"respuesta": crudo["respuesta"], "razon": str(crudo.get("razon", ""))[:300],
                            "fuente": "llm"}
            except Exception as e:  # noqa: BLE001
                self.log(f"  [llm] momento falló ({type(e).__name__}): uso reglas")
        r = reglas.momento(msg, self.ficha)
        r["fuente"] = "reglas"
        return r


def orden_de_respaldo(ventana: dict, ultima: dict | None) -> dict:
    """Si el cerebro no alcanza a responder: mismo ritmo y energía, y respeta la parada ya programada."""
    ultima = ultima or {}
    coche = ventana.get("coche", {})
    pits = {"compuesto": "NINGUNO"}
    prog = coche.get("pit_programado")
    if prog:
        pits = {"compuesto": prog["compuesto"], "vuelta": max(1, min(6, prog["vuelta"] - ventana.get("vuelta", 0)))}
    return {"ritmo": ultima.get("ritmo", coche.get("ritmo", "CARRERA")),
            "energia": ultima.get("energia", coche.get("energia", "EQUILIBRIO")),
            "pits": pits, "radio": "", "razonamiento": "Respaldo: el cerebro no respondió a tiempo.",
            "fuente": "respaldo"}
