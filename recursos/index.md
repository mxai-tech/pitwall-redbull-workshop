---
title: "Tu caja de herramientas"
lead: "Materiales para construir, probar y explicar el criterio de tu Director."
eyebrow: 08 / RECURSOS
---
## Descargas del equipo

| Material | Para qué sirve |
| --- | --- |
| [Kit del Director con OCI]({{ '/downloads/kit-director.zip' | relative_url }}) | Python, pruebas, Responses API, runtime HTTP, Dockerfile y transporte al servidor |
| [Ficha de ejemplo]({{ '/downloads/ficha.yaml' | relative_url }}) | Personalidad inicial para editar en equipo |
| [Orden de ejemplo]({{ '/downloads/orden-ejemplo.json' | relative_url }}) | Referencia del mensaje que acepta el servidor |
| [Bitácora de experimentos]({{ '/downloads/bitacora.csv' | relative_url }}) | Comparar hipótesis, órdenes y resultados |

El kit se deriva del Director del proyecto `pitwall-redbull`, con un adaptador OCI Responses API para este taller. No contiene el motor de carrera, herramientas de administración, tokens del evento ni credenciales OCI. La prueba local verifica la conexión cuando aportes tus credenciales.

## Dónde trabajar en el kit

| Archivo | Tu intervención |
| --- | --- |
| `director/ficha.yaml` | Cambiar personalidad e identidad ficticia |
| `director/prompt.py` | Precisar cómo interpreta y elige el Director |
| `director/cerebro.py` | Combinar herramientas y añadir límites de decisión |
| `director/reglas.py` | Mejorar la política de respaldo |
| `director/politica_equipo.py` | Desarrollar restricciones verificables |
| `tests/test_politica.py` | Probar condiciones y límites de tu política |
| `app.py` | Revisar ciclo de vida HTTP y conexión a carrera |
| `Dockerfile` y `.dockerignore` | Construir la imagen sin configuración local |
| `director/llm.py` | Ver la petición a OCI Responses API |
| `director/validar.py` | Entender normalización y validación |
| `director/herramientas.py` | Ver las tres consultas HTTP |
| `director/cliente.py` | Entender ventanas, tiempos y envío de órdenes |

## Referencias de Oracle

- [OCI Generative AI: visión general](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm).
- [Enterprise AI Agents: enfoques de construcción](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm).
- [OCI Responses API: peticiones, autenticación y herramientas](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm).
- [Modelos y regiones disponibles](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agentic-regions.htm).

Las referencias técnicas se revisaron el 22 de octubre de 2026. Confirma modelo, región, permisos y recursos disponibles para tu evento con la organización.

## Referencias para el deployment

- [Preparar imágenes de Applications](https://docs.oracle.com/en-us/iaas/Content/generative-ai/prepare-artifacts.htm).
- [Publicar en OCIR](https://docs.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm).
- [Crear una Application](https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-application.htm).
- [Crear el deployment](https://docs.oracle.com/en-us/iaas/Content/generative-ai/create-deployment.htm).
- [Permisos para aplicaciones e imágenes](https://docs.oracle.com/en-us/iaas/Content/generative-ai/deploy-permissions.htm).
- [Invocar la Application](https://docs.oracle.com/en-us/iaas/Content/generative-ai/use-applications.htm).

## Glosario del muro

| Término | Significado |
| --- | --- |
| Ventana | Oportunidad limitada para enviar una nueva orden |
| Stint | Tramo entre cambios de llantas |
| Undercut | Parar antes que un rival para aprovechar llantas nuevas |
| Acantilado | Umbral de edad efectiva a partir del cual aumenta la degradación |
| Gap | Diferencia de tiempo respecto a otro auto |
| Respaldo | Orden o política que evita depender de una respuesta tardía o inválida |

## Antes de tomar la salida

Tu equipo debe presentar código y pruebas, una llamada real a OCI, la imagen en OCIR y un deployment de Applications conectado al servidor de carrera. Identifica una decisión que mejorarías y una señal con la que evaluarías esa mejora.
