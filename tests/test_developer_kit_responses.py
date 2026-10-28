"""Ejercita el agente descargable con el SDK real y HTTP simulado, sin acceso a OCI."""
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import AsyncMock, Mock, patch

import httpx
from openai import AsyncOpenAI

# La entrega se importa sin requerir una copia del developer kit en la máquina.
# Su contrato con estrategia.py se representa aquí; el archivo entregado conserva
# ese import y usa la implementación real del kit cuando se instala allí.
strategy = ModuleType('estrategia')
strategy.prompt = Mock(return_value=('instrucciones', 'telemetria'))
strategy.respaldo = Mock(return_value={'tipo': 'orden', 'ritmo': 'CARRERA', 'energia': 'EQUILIBRIO'})
strategy.validar = lambda mensaje, datos: datos
spec = importlib.util.spec_from_file_location('developer_kit_responses',
    Path(__file__).resolve().parents[1] / 'downloads/agente.py')
agente = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {'estrategia': strategy}):
    spec.loader.exec_module(agente)

ORDER = {'ritmo': 'ATAQUE', 'energia': 'BOOST', 'pits': {'compuesto': 'MEDIO', 'vuelta': 2},
         'radio': 'Box en dos vueltas', 'razonamiento': 'Llantas al límite'}
ENV = {'OCI_GENAI_REGION':'us-chicago-1', 'OCI_GENAI_MODEL':'modelo-prueba',
       'OCI_GENAI_API_KEY':'clave-ficticia',
       'OCI_GENAI_PROJECT_ID':'ocid1.generativeaiproject.oc1.fake',
       'EQUIPO':'equipo-prueba', 'TOKEN':'token-ficticio', 'SERVIDOR':'wss://carrera.invalid'}


def response(text, status='completed'):
    return {'id':'resp_fake', 'object':'response', 'created_at':0, 'model':'modelo-prueba',
            'status':status, 'output':[
                {'id':'rs_fake', 'type':'reasoning', 'summary':[]},
                {'id':'msg_fake', 'type':'message', 'role':'assistant', 'status':status,
                 'content':[{'type':'output_text', 'text':text, 'annotations':[]}]}]}


class DeveloperKitResponsesTests(unittest.IsolatedAsyncioTestCase):
    def configure(self, payload=None, timeout=False):
        self.requests = []
        def handler(request):
            self.requests.append(request)
            if timeout:
                raise httpx.ReadTimeout('timeout simulado', request=request)
            return httpx.Response(200, json=payload)
        def factory(**kwargs):
            return AsyncOpenAI(**kwargs, http_client=httpx.AsyncClient(
                transport=httpx.MockTransport(handler)))
        return patch.object(agente, 'AsyncOpenAI', side_effect=factory)

    async def test_real_sdk_posts_to_oci_responses_and_parses_output_text(self):
        with patch.dict(os.environ, ENV, clear=True), self.configure(response(json.dumps(ORDER))):
            model = agente.ModeloOCI()
            try:
                self.assertEqual(await model.consultar('sistema', 'usuario'), ORDER)
            finally:
                await model.cerrar()
        self.assertEqual(len(self.requests), 1)
        request = self.requests[0]
        self.assertEqual(str(request.url), 'https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/openai/v1/responses')
        self.assertEqual(request.headers['OpenAI-Project'], ENV['OCI_GENAI_PROJECT_ID'])
        self.assertEqual(json.loads(request.content), {'model':'modelo-prueba', 'instructions':'sistema',
            'input':'usuario', 'max_output_tokens':2048, 'store':False})

    async def test_incomplete_valid_json_is_rejected(self):
        with patch.dict(os.environ, ENV, clear=True), self.configure(response(json.dumps(ORDER), 'incomplete')):
            model = agente.ModeloOCI()
            try:
                with self.assertRaisesRegex(ValueError, 'no se completó'):
                    await model.consultar('s', 'u')
            finally:
                await model.cerrar()

    async def test_empty_or_non_json_is_rejected(self):
        for text in ('', 'No puedo generar una orden'):
            with self.subTest(text=text):
                with patch.dict(os.environ, ENV, clear=True), self.configure(response(text)):
                    model = agente.ModeloOCI()
                    try:
                        with self.assertRaisesRegex(ValueError, 'objeto JSON'):
                            await model.consultar('s', 'u')
                    finally:
                        await model.cerrar()

    async def test_timeout_uses_existing_race_fallback(self):
        message = {'tipo':'ventana', 'ventana':1, 'vuelta':6, 'limite_ms':10000}
        with patch.dict(os.environ, ENV, clear=True), self.configure(timeout=True):
            director = agente.Agente()
            director.ws = Mock(send=AsyncMock())
            director.consultar_auxiliar = AsyncMock(return_value={})
            try:
                await director._responder(message, None)
                director.ws.send.assert_awaited_once()
                sent = json.loads(director.ws.send.call_args.args[0])
                self.assertEqual(sent['energia'], 'EQUILIBRIO')
                strategy.respaldo.assert_called_with(message)
            finally:
                await director.modelo.cerrar()

    async def test_incomplete_response_uses_existing_race_fallback(self):
        with patch.dict(os.environ, ENV, clear=True), self.configure(response(json.dumps(ORDER), 'incomplete')):
            director = agente.Agente()
            director.ws = Mock(send=AsyncMock())
            director.consultar_auxiliar = AsyncMock(return_value={})
            try:
                await director._responder({'tipo':'ventana', 'ventana':1, 'vuelta':6}, None)
                sent = json.loads(director.ws.send.call_args.args[0])
                self.assertEqual(sent['energia'], 'EQUILIBRIO')
            finally:
                await director.modelo.cerrar()
