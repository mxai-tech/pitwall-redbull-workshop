"""Ejecuta el Director del developer kit como proceso local, sin servidor HTTP."""
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from agente import Agente


async def ejecutar():
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    director = Agente()
    try:
        director.iniciar()
        await director.tarea
        if director.error:
            raise RuntimeError("El Director se detuvo: " + director.error)
    finally:
        await director.cerrar()


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    for nombre in ("httpx", "httpcore", "openai", "websockets.client"):
        logging.getLogger(nombre).setLevel(logging.WARNING)
    try:
        asyncio.run(ejecutar())
    except KeyboardInterrupt:
        print("Director detenido.")
    except (ValueError, RuntimeError) as exc:
        raise SystemExit(str(exc)) from None


if __name__ == "__main__":
    main()
