"""Herramientas del Director: los Agentes 1, 2 y 3 por HTTP."""
from __future__ import annotations

import httpx


class HerramientasHTTP:
    def __init__(self, base_http: str, equipo: str, token: str, cliente: httpx.AsyncClient):
        self.base = base_http.rstrip("/")
        self.params = {"equipo": equipo, "token": token}
        self.cliente = cliente

    async def _get(self, nombre: str) -> dict:
        r = await self.cliente.get(f"{self.base}/api/agentes/{nombre}", params=self.params, timeout=4.0)
        r.raise_for_status()
        return r.json()

    async def llantas(self) -> dict:
        return await self._get("llantas")

    async def pista(self) -> dict:
        return await self._get("pista")

    async def estrategia(self) -> dict:
        return await self._get("estrategia")
