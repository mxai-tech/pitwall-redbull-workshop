"""Verifica el arranque local y la prueba de inferencia sin conexiones externas."""
import asyncio
from contextlib import redirect_stdout
import importlib.util
import io
import os
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import patch

import httpx
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'downloads' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class FakeDirector:
    error = None
    def iniciar(self):
        self.tarea = asyncio.create_task(asyncio.sleep(0))
    async def cerrar(self):
        self.closed = True

stub = ModuleType('agente')
stub.Agente = FakeDirector
with patch.dict(sys.modules, {'agente':stub}):
    runner = load('local_runner', 'ejecutar_director.py')
probe = load('local_probe', 'probar_llm.py')

class LocalRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_loads_adjacent_env_and_closes_director(self):
        director = FakeDirector()
        with patch.object(runner, 'load_dotenv') as env, patch.object(runner, 'Agente', return_value=director):
            await runner.ejecutar()
        env.assert_called_once_with(ROOT / 'downloads/.env', override=True)
        self.assertTrue(director.closed)

    async def test_authentication_failure_closes_and_reports_error(self):
        director = FakeDirector()
        director.error = 'autenticacion_rechazada'
        with patch.object(runner, 'load_dotenv'), patch.object(runner, 'Agente', return_value=director):
            with self.assertRaisesRegex(RuntimeError, 'autenticacion_rechazada'):
                await runner.ejecutar()
        self.assertTrue(director.closed)

    async def test_cancellation_closes_director(self):
        started = asyncio.Event()
        class Waiting(FakeDirector):
            def iniciar(self):
                self.tarea = asyncio.create_task(asyncio.Event().wait())
                started.set()
        director = Waiting()
        with patch.object(runner, 'load_dotenv'), patch.object(runner, 'Agente', return_value=director):
            task = asyncio.create_task(runner.ejecutar())
            await started.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(director.closed)
        self.assertTrue(director.tarea.cancelled())

class LocalProbeTests(unittest.TestCase):
    def test_uses_api_key_endpoint_and_120b_without_project(self):
        requests = []
        def handler(request):
            requests.append(request)
            return httpx.Response(200, json={
                'id':'resp_probe','object':'response','created_at':0,'status':'completed',
                'model':'openai.gpt-oss-120b', 'output':[
                    {'id':'msg_probe','type':'message','role':'assistant','status':'completed',
                     'content':[{'type':'output_text','text':'OK','annotations':[]}]}]})
        def factory(**kwargs):
            return OpenAI(**kwargs, http_client=httpx.Client(transport=httpx.MockTransport(handler)))
        out = io.StringIO()
        with patch.dict(os.environ, {'OCI_GENAI_API_KEY':'clave-ficticia'}, clear=True), patch.object(probe,'load_dotenv'), patch.object(probe,'OpenAI',side_effect=factory), redirect_stdout(out):
            probe.main()
        self.assertIn('OCI OK: openai.gpt-oss-120b', out.getvalue())
        self.assertNotIn('clave-ficticia', out.getvalue())
        self.assertEqual(str(requests[0].url), 'https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1/responses')
        self.assertNotIn('OpenAI-Project', requests[0].headers)

    def test_missing_key_never_calls_model(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(probe,'load_dotenv'), patch.object(probe,'OpenAI') as client:
            with self.assertRaisesRegex(ValueError,'OCI_GENAI_API_KEY'):
                probe.main()
            client.assert_not_called()
