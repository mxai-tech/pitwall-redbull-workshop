"""Prueba real de acceso OCI: falla explícitamente si OCI no devuelve una orden válida."""
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from director.llm import crear_llm
from director.validar import normalizar_orden, validar_orden

async def main():
    load_dotenv(Path(__file__).with_name(".env"))
    llm = crear_llm("oci")
    result = await llm.json(
        'Responde solo JSON con ritmo=CARRERA, energia=EQUILIBRIO, pits={"compuesto":"NINGUNO"}, radio y razonamiento.',
        'Prueba de conexión del taller. Devuelve la orden de verificación.',
    )
    # Comprueba también el objeto original: la normalización por sí sola puede completar campos.
    required = {"ritmo", "energia", "pits", "radio", "razonamiento"}
    if not required.issubset(result):
        raise ValueError("La respuesta OCI no incluye todos los campos de una orden")
    orden = normalizar_orden(result)
    errores = validar_orden(orden)
    if errores:
        raise ValueError("; ".join(errores))
    print("OCI OK: recibimos una orden válida desde Responses API.")
    print(orden)

if __name__ == "__main__":
    asyncio.run(main())
