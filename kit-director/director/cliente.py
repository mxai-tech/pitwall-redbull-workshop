"""Cliente WebSocket del Director: se conecta al servidor y contesta cada ventana."""
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path

import httpx
import websockets
import yaml

from .cerebro import Cerebro, orden_de_respaldo
from .herramientas import HerramientasHTTP
from .llm import crear_llm

GRIS, VERDE, ROJO, AMARILLO, AZUL, NEGRITA, FIN = "\033[90m", "\033[92m", "\033[91m", "\033[93m", "\033[94m", "\033[1m", "\033[0m"


def cargar_ficha(ruta: str | Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class Director:
    def __init__(self, equipo: str, token: str, servidor: str = "ws://localhost:8000", ficha: dict | None = None,
                 proveedor: str | None = None, politica: str = "auto", silencioso: bool = False,
                 margen_s: float = 2.0, semilla: int | None = None):
        self.equipo = equipo
        self.token = token
        self.servidor = servidor.rstrip("/")
        self.http = self.servidor.replace("ws://", "http://").replace("wss://", "https://")
        self.ficha = ficha or {}
        self.silencioso = silencioso
        self.margen_s = margen_s
        llm = crear_llm(proveedor) if politica in ("auto", "llm") else None
        self.cerebro = Cerebro(self.ficha, llm, politica, semilla=semilla, log=self.log)
        self.ultima: dict | None = None
        self.activo = True
        self.ws = None
        self.conectado = False
        self.ultima_fuente = None
        self.ultima_latencia_s = None
        self.etiqueta = f"{NEGRITA}{equipo}{FIN}"

    def log(self, texto: str) -> None:
        if not self.silencioso:
            print(f"{GRIS}{time.strftime('%H:%M:%S')}{FIN} {self.etiqueta} {texto}", flush=True)

    async def _enviar(self, msg: dict) -> None:
        if self.ws is not None:
            await self.ws.send(json.dumps(msg, ensure_ascii=False))

    async def _ventana(self, msg: dict, herramientas) -> None:
        t0 = time.monotonic()
        limite = msg.get("limite_ms", 10000) / 1000
        try:
            orden = await asyncio.wait_for(self.cerebro.decidir(msg, herramientas),
                                           timeout=max(1.0, limite - self.margen_s))
        except Exception as e:  # noqa: BLE001
            self.log(f"{AMARILLO}no alcancé a decidir ({type(e).__name__}): mando respaldo{FIN}")
            orden = orden_de_respaldo(msg, self.ultima)
        dt = time.monotonic() - t0
        fuente = orden.pop("fuente", "?")
        self.ultima_fuente = fuente
        self.ultima_latencia_s = round(dt, 3)
        orden.pop("agentes", None)
        envio = {"tipo": "orden", "ventana": msg["ventana"], **orden}
        await self._enviar(envio)
        self.ultima = orden
        c = msg.get("coche", {})
        pits = orden.get("pits", {})
        pit_txt = (f" · {AMARILLO}BOX en {pits.get('vuelta')} por {pits['compuesto']}{FIN}"
                   if pits.get("compuesto", "NINGUNO") != "NINGUNO" else "")
        self.log(f"V{msg.get('vuelta'):>2} P{c.get('posicion')} {c.get('llanta', {}).get('compuesto')} "
                 f"{c.get('llanta', {}).get('edad_efectiva')} bat {c.get('bateria_pct')}% → "
                 f"{AZUL}{orden['ritmo']}/{orden['energia']}{FIN}{pit_txt} {GRIS}({fuente} {dt:.1f}s){FIN}")
        if orden.get("radio"):
            self.log(f"   📻 {orden['radio']}")

    async def _pre_carrera(self, msg: dict) -> None:
        setup = await self.cerebro.pre_carrera(msg)
        fuente = setup.pop("fuente", "?")
        await self._enviar({"tipo": "setup", "ventana": 0, **setup})
        self.log(f"Pre-carrera: sale {msg.get('coche', {}).get('parrilla')}º con {setup['llanta_salida']}, "
                 f"{setup['aleron']}, {setup['ritmo']}/{setup['energia']} {GRIS}({fuente}){FIN}")

    async def _momento(self, msg: dict) -> None:
        r = await self.cerebro.momento(msg)
        fuente = r.pop("fuente", "?")
        await self._enviar({"tipo": "respuesta_momento", "id": msg["id"], **r})
        self.log(f"Momento {msg['id']} ({msg.get('titulo')}): {r['respuesta']} {GRIS}({fuente}){FIN}")

    async def correr(self) -> None:
        url = f"{self.servidor}/ws/agente?equipo={self.equipo}&token={self.token}"
        espera = 1.0
        async with httpx.AsyncClient() as http:
            herramientas = HerramientasHTTP(self.http, self.equipo, self.token, http)
            while self.activo:
                tareas = set()
                try:
                    async with websockets.connect(url, ping_interval=20, max_size=2 ** 22) as ws:
                        self.ws = ws
                        espera = 1.0
                        await self._enviar({"tipo": "hola", "ficha": self.ficha})
                        async for crudo in ws:
                            msg = json.loads(crudo)
                            t = msg.get("tipo")
                            coro = None
                            if t == "ventana":
                                coro = self._ventana(msg, herramientas)
                            elif t == "pre_carrera":
                                coro = self._pre_carrera(msg)
                            elif t == "momento":
                                coro = self._momento(msg)
                            elif t == "bienvenida":
                                self.conectado = True
                                self.log(f"{VERDE}conectado como {msg.get('nombre')}{FIN}"
                                         + (f" · avisos: {msg['avisos']}" if msg.get("avisos") else ""))
                            elif t in ("orden_error", "setup_error", "momento_error"):
                                self.log(f"{ROJO}{t}: {msg.get('errores') or msg.get('mensaje')}{FIN}")
                            elif t == "ventana_cerrada":
                                self.log(f"{ROJO}ventana {msg.get('ventana')} cerrada: {msg.get('motivo')}{FIN}")
                            elif t == "carrera_nueva":
                                self.log(f"nueva carrera: {msg['carrera'].get('id')} ({msg['carrera'].get('escenario')})")
                            elif t == "momento_resultado":
                                mio = next((r for r in msg.get("respuestas", []) if r["equipo"] == self.equipo), None)
                                if mio:
                                    self.log(f"Momento {msg['id']}: {mio['puntos']} pts · {mio['comentario']}")
                            elif t == "fin_carrera":
                                mio = next((r for r in msg.get("resultados", []) if r["equipo"] == self.equipo), {})
                                pts = (msg.get("puntos") or {}).get(self.equipo, {}).get("total")
                                self.log(f"{VERDE}{NEGRITA}META: P{mio.get('posicion')} · {pts} puntos{FIN}")
                            elif t == "error":
                                self.log(f"{ROJO}error: {msg.get('errores')}{FIN}")
                            if coro is not None:
                                tarea = asyncio.create_task(coro)
                                tareas.add(tarea)
                                tarea.add_done_callback(tareas.discard)
                except (OSError, websockets.exceptions.WebSocketException) as e:
                    codigo = getattr(getattr(e, "rcvd", None), "code", None)
                    if codigo == 4401:
                        self.log(f"{ROJO}equipo o token inválido: revisa --equipo y --token{FIN}")
                        return
                    self.log(f"{GRIS}sin conexión con {self.servidor} ({type(e).__name__}); reintento en {espera:.0f} s{FIN}")
                finally:
                    self.conectado = False
                    self.ws = None
                    for tarea in tareas:
                        tarea.cancel()
                    if tareas:
                        await asyncio.gather(*tareas, return_exceptions=True)
                await asyncio.sleep(espera)
                espera = min(10.0, espera * 2)
