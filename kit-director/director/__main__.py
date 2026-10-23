"""Corre tu Agente Director.

    python -m director --equipo TU_ID --token TU_TOKEN
    python -m director --equipo TU_ID --token TU_TOKEN --servidor ws://192.168.1.50:8000
    python -m director --equipo TU_ID --token TU_TOKEN --proveedor oci

Lee la personalidad de director/ficha.yaml (o --ficha otra.yaml) y el LLM del
archivo .env (LLM_PROVEEDOR). Sin LLM decide con reglas.
"""
from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from .cliente import Director, cargar_ficha

RAIZ = Path(__file__).resolve().parents[1]


def main() -> None:
    load_dotenv(RAIZ / ".env")
    p = argparse.ArgumentParser(description="Agente Director · Pit Wall Red Bull")
    p.add_argument("--equipo", default=os.getenv("EQUIPO"))
    p.add_argument("--token", default=os.getenv("TOKEN"))
    p.add_argument("--servidor", default=os.getenv("SERVIDOR", "ws://localhost:8000"))
    p.add_argument("--ficha", default=str(Path(__file__).with_name("ficha.yaml")))
    p.add_argument("--proveedor", default=None, help="oci | ninguno (por defecto, el del .env)")
    p.add_argument("--politica", default="auto", choices=["auto", "llm", "reglas", "azar"],
                   help="auto = LLM si hay, si no reglas")
    a = p.parse_args()
    if not a.equipo or not a.token:
        p.error("Configura EQUIPO y TOKEN en .env o usa --equipo y --token")
    ficha = cargar_ficha(a.ficha)
    d = Director(a.equipo, a.token, a.servidor, ficha, a.proveedor, a.politica)
    modo = d.cerebro.llm or "reglas"
    print(f"\n  Agente Director de {a.equipo} · {ficha.get('ingeniero')} en el radio · cerebro: {modo}")
    print(f"  Servidor: {a.servidor}   (Ctrl+C para salir)\n")
    try:
        asyncio.run(d.correr())
    except KeyboardInterrupt:
        print("\n  Director desconectado.")


if __name__ == "__main__":
    main()
