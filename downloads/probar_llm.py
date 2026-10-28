"""Prueba de Responses API para el workshop. Lee .env y nunca imprime la API key."""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIStatusError, APITimeoutError


def main():
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    clave = os.getenv("OCI_GENAI_API_KEY", "").strip()
    if not clave:
        raise ValueError("Completa OCI_GENAI_API_KEY en .env")
    region = os.getenv("OCI_GENAI_REGION", "us-chicago-1")
    modelo = os.getenv("OCI_GENAI_MODEL", "openai.gpt-oss-120b")
    with OpenAI(
        base_url=f"https://inference.generativeai.{region}.oci.oraclecloud.com/20231130/actions/v1",
        api_key=clave, timeout=60, max_retries=0,
    ) as cliente:
        respuesta = cliente.responses.create(
            model=modelo, input="Responde únicamente OK.", max_output_tokens=2048, store=False,
        )
        if respuesta.status != "completed" or not respuesta.output_text.strip():
            raise ValueError("La respuesta no se completó o no contiene texto")
    print(f"OCI OK: {modelo} respondió mediante Responses API.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, APITimeoutError) as exc:
        mensaje = str(exc) if isinstance(exc, ValueError) else "OCI no respondió en 60 segundos"
        raise SystemExit(mensaje) from None
    except APIStatusError as exc:
        raise SystemExit(f"OCI devolvió HTTP {exc.status_code}; revisa acceso, región y modelo") from None
    except APIConnectionError:
        raise SystemExit("No se pudo conectar con OCI; revisa la conexión de red") from None
