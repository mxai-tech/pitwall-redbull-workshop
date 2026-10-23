# Revisión para la primera edición

Fecha: 22 de octubre de 2026. Origen: proyecto local `pitwall-redbull`.

| Área revisada | Decisión para el sitio |
| --- | --- |
| README y docs/GUIA_EQUIPOS.md | Extraer misión, preparación, personalidad y conceptos de estrategia |
| docs/CONTRATO.md y server/main.py | Explicar únicamente canales y mensajes del participante |
| director/ completo | Derivar el kit; conservar transporte, normalización y respaldo; reemplazar proveedor por OCI Responses API |
| server/agentes/ | Explicar los tres servicios deterministas y los supuestos de Estrategia |
| config/coeficientes.json y server/sim/ | Contrastar cifras de ritmo, energía, pits, llantas, clima y penalización |
| server/sim/puntaje.py y server/torneo.py | Explicar bonos, silencios, acumulación previa y orden de la final |
| config/escenarios/ y laboratorio/ | Usar como contexto para evaluar escenarios; no publicar escenarios internos ni simulador |
| server/sesion.py y server/ajustes.py | Confirmar límites configurables, ventanas, publicación del radio y confirmaciones |
| server/oci_narrador.py | Identificar el uso existente de Responses en OCI, sin reutilizar secretos ni dependencias del servidor |
| web/ | Distinguir muro de equipo de pantallas públicas y Control; no copiar la aplicación de carrera |
| bots/, tests/, scripts/ y calibracion/ | Entender práctica y entrega del kit; omitir operación y calibración en la guía de participantes |
| server/avatar.py, filtro.py, momentos.py, narrador.py y registro.py | Resumir solo radio, identidad ficticia y clasificación relevantes para el jugador |
| docs/INTEGRACION_MINI_CIRCUIT.md | Fuera del sitio: integración de visualización del servidor |
| aidp-churn-workshop | Tomar como referencia Jekyll/Markdown, navegación por secciones, índice de página y workflow de Pages |

## Diferencias que evita arrastrar la guía

- El Director original no tenía OCI Responses; la integración OCI existente era del narrador.
- Los especialistas actuales no son tres LLM: son consultas deterministas del servidor.
- Hay once ventanas programadas (6 a 66), además de pre-carrera y posibles extras.
- BOOST falla por batería insuficiente para el consumo de una vuelta, incluso con una reserva mayor que cero.
- La llovizna no exime de la penalización por dos compuestos secos.
- A 55 °C crece el factor térmico del término de degradación, no el incremento de edad directamente.
- Los puntos previos seleccionan finalistas; la llegada en la final determina su orden final.
- El cliente original registra un rechazo del servidor, pero no reintenta automáticamente.
- Una regla de oro en texto libre no es una condición obligatoria del respaldo por reglas.

## Validación realizada

- Jekyll con validación estricta del front matter.
- Nueve páginas compiladas (ocho de contenido y 404).
- 137 enlaces internos sin destinos ausentes.
- Sintaxis JavaScript comprobada.
- Seis pruebas del contrato OCI y del respaldo, con cliente simulado.
- Navegador: BOOST con reserva suficiente; EQUILIBRIO con reserva insuficiente;
  ausencia de rival y desactivación de la condición; validación de número en la ficha.
- Contenido del ZIP limitado a una lista de fuentes de participantes.

La prueba real de inferencia y la carrera con el kit requieren credenciales y servidor del evento.
No se hizo una llamada pagada a OCI. No se modificó el repositorio original ni el proyecto de referencia.

## Ajuste para evento de desarrolladores

Solicitud posterior: entorno virtual, desarrollo de código, Responses API, imagen
Docker y deploy en Applications de Enterprise AI desde OCI Console. El propietario
confirmó que el servidor de carrera corre en OCI y es accesible desde Applications.

La agenda ahora incluye desarrollo y despliegue en ambas duraciones. Se agregó
`despliegue/index.md`, runtime HTTP con lifespan, Dockerfile, contexto limitado de
build, política extensible y pruebas para participantes. El kit tiene 20 archivos.
La política se aplica a órdenes del LLM y de reglas antes de devolverlas. El proceso
mantiene el canal WebSocket saliente para conservar el contrato de carrera.

Referencias consultadas el 22/10/2026: prepare-artifacts, create-application,
create-deployment, deploy-permissions y use-applications de OCI Generative AI,
y registrypushingimagesusingthedockercli de OCI Registry. Se enlazan desde el sitio.

Validación de la revisión: diez páginas, 163 enlaces internos; pruebas de contrato
OCI, ciclo de vida HTTP, diagnóstico y política. No se construyó una imagen local:
Docker no tiene daemon activo y la VM de Podman está detenida. No se hizo push ni
deploy real. La prueba de red e inferencia requiere los recursos del evento.

## Para la siguiente iteración

Duración y audiencia confirmadas: 90–120 minutos, Python intermedio.
Confirmar región/modelo/proyecto de OCI, distribución de accesos,
coeficientes definitivos y cuánto código deben construir frente al transporte ya proporcionado.
