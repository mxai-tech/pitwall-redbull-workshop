"""Adaptador del workshop para OCI Generative AI Responses API.

La clave es una Generative AI API key de OCI asociada al proyecto del taller.
El transporte a carrera no depende de este proveedor.
"""
from __future__ import annotations
import os
import json
import re

def extraer_json(texto: str) -> dict:
    """Saca el primer objeto JSON de una respuesta (tolera texto o ```json alrededor)."""
    if not texto:
        raise ValueError("Respuesta vacía del LLM")
    texto = re.sub(r"```(?:json)?", "", texto)
    inicio = texto.find("{")
    while inicio != -1:
        nivel = 0
        en_cadena = False
        escape = False
        for i in range(inicio, len(texto)):
            ch = texto[i]
            if en_cadena:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    en_cadena = False
                continue
            if ch == '"':
                en_cadena = True
            elif ch == "{":
                nivel += 1
            elif ch == "}":
                nivel -= 1
                if nivel == 0:
                    try:
                        return json.loads(texto[inicio:i + 1])
                    except json.JSONDecodeError:
                        break
        inicio = texto.find("{", inicio + 1)
    raise ValueError("No encontré JSON en la respuesta del LLM")


class LLM:
    def __init__(self, modelo: str, api_key: str, base_url: str, project: str, timeout: float = 6.0):
        from openai import AsyncOpenAI
        self.modelo = modelo
        self.timeout = timeout
        self._cliente = AsyncOpenAI(
            api_key=api_key, base_url=base_url.rstrip("/"), project=project,
            timeout=timeout, max_retries=0,
        )

    def __repr__(self) -> str:
        return f"OCI Responses API ({self.modelo})"

    async def texto(self, sistema: str, usuario: str, max_tokens: int = 1024) -> str:
        response = await self._cliente.responses.create(
            model=self.modelo,
            instructions=sistema,
            input=usuario,
            max_output_tokens=max_tokens,
            store=False,
        )
        if response.status != "completed":
            raise ValueError(f"OCI terminó con estado {response.status}; no se ejecuta una respuesta incompleta")
        return response.output_text or ""

    async def json(self, sistema: str, usuario: str, max_tokens: int = 1024) -> dict:
        result = extraer_json(await self.texto(sistema, usuario, max_tokens))
        if not isinstance(result, dict):
            raise ValueError("OCI debe devolver un objeto JSON")
        return result


def crear_llm(proveedor: str | None = None, timeout: float = 6.0) -> LLM | None:
    p = (proveedor or os.getenv("LLM_PROVEEDOR", "oci")).strip().lower()
    if p in ("ninguno", "none", "reglas"):
        return None
    if p != "oci":
        raise ValueError("Este kit usa LLM_PROVEEDOR=oci o ninguno para verificar el transporte")
    names = ("OCI_LLM_MODEL", "OCI_GENAI_API_KEY", "OCI_OPENAI_COMPATIBLE_ENDPOINT", "OCI_PROJECT_ID")
    values = {name: os.getenv(name, "").strip() for name in names}
    missing = [name for name in names if not values[name]]
    if missing:
        raise ValueError("Falta configuración OCI: " + ", ".join(missing))
    endpoint = values["OCI_OPENAI_COMPATIBLE_ENDPOINT"].rstrip("/")
    if not endpoint.startswith("https://") or not endpoint.endswith("/openai/v1"):
        raise ValueError("El endpoint OCI debe ser HTTPS y terminar en /openai/v1")
    return LLM(values["OCI_LLM_MODEL"], values["OCI_GENAI_API_KEY"], endpoint, values["OCI_PROJECT_ID"], timeout)
