---
title: "Tu caja de herramientas"
lead: "Materiales para construir, probar y explicar el criterio de tu Director."
eyebrow: 06 / RECURSOS
---
## Developer kit del workshop

<div class="hero-callout"><div><span class="tag">CÓDIGO PARA TU EQUIPO</span><h2>kit-pitwall</h2><p>Clona el repositorio en tu computadora y personaliza el prompt y la ficha. Tu Director corre como un proceso local de Python y utiliza openai.gpt-oss-120b en OCI.</p><a class="button primary" href="https://github.com/mxai-tech/kit-pitwall" target="_blank" rel="noopener noreferrer">Abrir repositorio en GitHub ↗</a></div></div>

Continúa con el [Laboratorio completo]({{ '/laboratorio/' | relative_url }}) para configurar los accesos y conectar el equipo.

## Descargas del equipo

| Material | Para qué sirve |
| --- | --- |
| [agente.py con Responses API]({{ '/downloads/agente.py' | relative_url }}) | Referencia actualizada del cliente OCI del kit |
| [ejecutar_director.py]({{ '/downloads/ejecutar_director.py' | relative_url }}) | Arranque del proceso local y carga de `.env` |
| [probar_llm.py]({{ '/downloads/probar_llm.py' | relative_url }}) | Verificación de la API key y del modelo antes de conectar a carrera |
| [Orden de ejemplo]({{ '/downloads/orden-ejemplo.json' | relative_url }}) | Referencia del mensaje que acepta el servidor |
| [Bitácora de experimentos]({{ '/downloads/bitacora.csv' | relative_url }}) | Comparar hipótesis, órdenes y resultados |

Los materiales sirven como referencia para definir la personalidad, entender una orden y registrar experimentos. La organización indica cómo acceder al entorno del taller y a la aplicación de carrera.

## Referencias de Oracle

- [OCI Generative AI: visión general](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm).
- [Enterprise AI Agents: enfoques de construcción](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm).
- [OCI Responses API: peticiones, autenticación y herramientas](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm).
- [Modelos y regiones disponibles](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agentic-regions.htm).

El workshop usa la autenticación con [API keys de OCI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm), el endpoint de Chicago y `openai.gpt-oss-120b`. La organización entrega los accesos antes de comenzar.

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

Tu equipo debe definir su estrategia, obtener una respuesta del modelo y conectar su Director local usando el ID y token entregados por la organización. Identifica una decisión que mejorarías y una señal con la que evaluarías esa mejora.
