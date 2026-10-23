"""Pruebas del runtime alojado sin credenciales ni servidor de carrera."""
import asyncio
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit-director'))
from fastapi.testclient import TestClient
import app as hosted


class FakeDirector:
    def __init__(self):
        self.activo = True
        self.conectado = False
        self.ultima_fuente = None
        self.ultima_latencia_s = None
        self.cerebro = SimpleNamespace(llm=None)
        self.cancelado = False

    async def correr(self):
        self.conectado = True
        try:
            await asyncio.Event().wait()
        finally:
            self.cancelado = True
            self.conectado = False


class HostedAppTests(unittest.TestCase):
    def test_lifecycle_probes_and_private_status(self):
        director = FakeDirector()
        with patch.object(hosted, 'configurar_director', return_value=director):
            with TestClient(hosted.app) as client:
                self.assertEqual(client.get('/health').status_code, 200)
                self.assertEqual(client.get('/ready').status_code, 200)
                state = client.get('/status').json()
                self.assertTrue(state['carrera_conectada'])
                self.assertNotIn('token', state)
                self.assertNotIn('servidor', state)
                self.assertNotIn('api_key', state)
                # Desconectar la carrera no provoca reinicios en bucle del contenedor.
                director.conectado = False
                self.assertEqual(client.get('/health').status_code, 200)
                self.assertFalse(client.get('/status').json()['carrera_conectada'])
            self.assertTrue(director.cancelado)
            self.assertFalse(director.activo)

    def test_ended_worker_fails_probes(self):
        class Finished(FakeDirector):
            async def correr(self):
                return
        with patch.object(hosted, 'configurar_director', return_value=Finished()):
            with TestClient(hosted.app) as client:
                self.assertEqual(client.get('/ready').status_code, 503)
                self.assertEqual(client.get('/health').status_code, 503)
                self.assertEqual(client.get('/status').status_code, 503)

    def test_required_race_configuration(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(hosted, 'load_dotenv'):
            with self.assertRaisesRegex(ValueError, 'EQUIPO, TOKEN, SERVIDOR'):
                hosted.configurar_director()

    def test_race_url_scheme_validation(self):
        with patch.dict(os.environ, {'EQUIPO':'fake','TOKEN':'fake','SERVIDOR':'https://race.invalid'}, clear=True), patch.object(hosted, 'load_dotenv'):
            with self.assertRaisesRegex(ValueError, 'ws:// o wss://'):
                hosted.configurar_director()

class HostedSSETests(unittest.TestCase):
    def test_status_supports_sse_accept(self):
        with patch.object(hosted, 'configurar_director', return_value=FakeDirector()):
            with TestClient(hosted.app) as client:
                response = client.get('/status', headers={'Accept':'text/event-stream'})
                self.assertEqual(response.status_code, 200)
                self.assertIn('text/event-stream', response.headers['content-type'])
                self.assertIn('data: ', response.text)
