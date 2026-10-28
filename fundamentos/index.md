---
title: "De un modelo a un agente"
lead: "Un modelo genera una respuesta. Un agente usa contexto, herramientas y reglas para decidir qué hacer con ella."
eyebrow: 01 / FUNDAMENTOS AI
next_url: /fundamentos/arquitectura.html
next_title: Conoce la arquitectura del muro
---
## Oracle Generative AI

OCI Generative AI ofrece modelos administrados para construir aplicaciones de IA. En este taller usaremos **OCI Responses API** para enviar al modelo la situación de carrera y recibir la propuesta del Director. Usaremos `openai.gpt-oss-120b` en `us-chicago-1`, con la API key entregada por la organización.

Una buena petición une tres piezas: **instrucciones** (rol y personalidad), **contexto** (telemetría y especialistas) y **formato de salida** (la orden JSON). El modelo propone; la aplicación comprueba la respuesta antes de actuar.

Fuente: [Visión general de OCI Generative AI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm).

## Enterprise AI en este workshop

Oracle presenta OCI Generative AI como su plataforma Enterprise AI. Para nuestro caso, esto significa conectar el modelo con un proceso completo de decisión: herramientas, estado, controles y ejecución. Responses API y las aplicaciones alojadas son formas de construir agentes en esa plataforma.

| Pieza | En el muro de tu equipo |
| --- | --- |
| Modelo | Interpreta la situación y propone una orden |
| Instrucciones | Definen estilo, tolerancia al riesgo y regla de oro |
| Herramientas | Consultan Llantas, Pista y Estrategia |
| Contexto | Reúne la telemetría y las tres lecturas actuales |
| Validación | Comprueba ritmo, energía y parada |
| Acción | Devuelve al servidor la decisión del Director |
| Evaluación | Compara resultado, fuente de la orden y tiempo de respuesta |

Fuente: [Enterprise AI Agents en OCI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm).

## Qué hace Responses API

Esta API permite generar respuestas y construir flujos con herramientas. Su interfaz compatible con el SDK de OpenAI se conecta al endpoint de OCI; el modelo se ejecuta en Oracle Cloud. La autenticación y los recursos pertenecen a OCI.

En los ejercicios de Responses API, las instrucciones y el contexto se envían al modelo para obtener una respuesta. El Director local recibe la telemetría de carrera y obtiene del mismo servidor las lecturas de los tres especialistas antes de consultar el modelo.

Fuente: [OCI Responses API](https://docs.oracle.com/en-us/iaas/Content/generative-ai/responses-api.htm).

## Lo que conviene distinguir

- **LLM y agente:** el modelo es una pieza del Director; el Director también consulta, valida y comunica.
- **Personalidad y reglas:** la personalidad orienta elecciones; el formato y el servidor fijan qué órdenes son válidas.
- **Predicción y certeza:** un tiempo esperado o un radar de lluvia no garantizan el resultado.
- **Respuesta y ejecución:** escribir “entramos a pits” en el radio no programa la parada; el campo `pits` sí.

## Tu proceso local y OCI

El Director corre en tu computadora; el modelo se ejecuta en OCI. El cliente del kit usa Responses API con API key sobre el endpoint `/20231130/actions/v1`. La organización entrega los accesos: en este taller no despliegas el Director en Applications.

Fuente: [API keys de OCI Generative AI](https://docs.oracle.com/en-us/iaas/Content/generative-ai/api-keys.htm).

## Más allá del primer Director

Enterprise AI también ofrece herramientas y componentes para recuperación de documentos, memoria y otros flujos. Son extensiones posibles; este reto se concentra en telemetría y decisiones de carrera. El diseño actual permite estudiar primero la separación entre razonamiento y ejecución.

**Pregunta para tu equipo:** si el modelo responde algo convincente pero inválido, ¿qué debería hacer el Director antes de que cierre la ventana?
