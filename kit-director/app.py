"""Runtime HTTP de Applications: un Director por proceso y por equipo.

No recibe órdenes desde el navegador; mantiene el protocolo saliente de carrera.
La autenticación del endpoint HTTP se configura en OCI Applications.
"""
from contextlib import asynccontextmanager, suppress
import asyncio
import os
import json
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from director.cliente import Director, cargar_ficha

BASE = Path(__file__).resolve().parent


def configurar_director() -> Director:
    load_dotenv(BASE / ".env")
    requeridas = ("EQUIPO", "TOKEN", "SERVIDOR")
    faltantes = [n for n in requeridas if not os.getenv(n, "").strip()]
    if faltantes:
        raise ValueError("Falta configuración: " + ", ".join(faltantes))
    servidor = os.environ["SERVIDOR"].strip()
    parsed = urlsplit(servidor)
    if parsed.scheme not in ("ws", "wss") or not parsed.hostname or parsed.query or parsed.fragment:
        raise ValueError("SERVIDOR debe ser una URL ws:// o wss:// sin query ni fragmento")
    ficha = cargar_ficha(BASE / "director/ficha.yaml")
    return Director(os.environ["EQUIPO"], os.environ["TOKEN"], servidor, ficha,
                    proveedor=os.getenv("LLM_PROVEEDOR", "oci"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    director = configurar_director()
    tarea = asyncio.create_task(director.correr(), name="director-carrera")
    app.state.director = director
    app.state.tarea = tarea
    try:
        yield
    finally:
        director.activo = False
        tarea.cancel()
        with suppress(asyncio.CancelledError, Exception):
            await tarea
        llm = director.cerebro.llm
        if llm is not None:
            await llm._cliente.close()


app = FastAPI(title="Pit Wall Director", lifespan=lifespan, docs_url=None, redoc_url=None,
              openapi_url=None)


def vivo() -> bool:
    tarea = getattr(app.state, "tarea", None)
    return tarea is not None and not tarea.done()


@app.get("/health")
async def health():
    # Una desconexión transitoria no es un fallo irrecuperable del proceso.
    return Response(status_code=200 if vivo() else 503, media_type="application/json")


@app.get("/ready")
async def ready():
    # Listo significa runtime inicializado; /status distingue conexión a carrera.
    return Response(status_code=200 if vivo() else 503, media_type="application/json")


@app.get("/status")
async def status(request: Request):
    director = getattr(app.state, "director", None)
    datos = {
        "runtime_activo": vivo(),
        "carrera_conectada": bool(director and director.conectado),
        "ultima_fuente": director.ultima_fuente if director else None,
        "ultima_latencia_s": director.ultima_latencia_s if director else None,
    }
    codigo = 200 if vivo() else 503
    if "text/event-stream" in request.headers.get("accept", ""):
        async def evento():
            yield "data: " + json.dumps(datos) + "\n\n"
        return StreamingResponse(evento(), status_code=codigo, media_type="text/event-stream")
    return JSONResponse(datos, status_code=codigo)
