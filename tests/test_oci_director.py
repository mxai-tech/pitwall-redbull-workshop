"""Verifica el contrato OCI y la salida segura del Director, sin consumir la API."""
import asyncio
import importlib
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit-director'))
from director.llm import LLM, crear_llm
from director.cerebro import Cerebro, orden_de_respaldo

VALID = {'ritmo': 'CARRERA', 'energia': 'EQUILIBRIO', 'pits': {'compuesto': 'NINGUNO'},
         'radio': 'Vamos con el plan', 'razonamiento': 'Cuidamos los recursos.'}
CONFIG = {'OCI_LLM_MODEL': 'modelo-de-prueba', 'OCI_GENAI_API_KEY': 'clave-ficticia',
          'OCI_PROJECT_ID': 'proyecto-ficticio',
          'OCI_OPENAI_COMPATIBLE_ENDPOINT': 'https://inference.generativeai.region.oci.oraclecloud.com/openai/v1'}

class OCIAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_config_and_responses_contract(self):
        import json
        client = SimpleNamespace(responses=SimpleNamespace(create=AsyncMock(
            return_value=SimpleNamespace(status='completed', output_text=json.dumps(VALID)))))
        with patch.dict(os.environ, CONFIG, clear=True), patch('openai.AsyncOpenAI', return_value=client) as constructor:
            llm = crear_llm('oci')
            constructor.assert_called_once_with(api_key='clave-ficticia', base_url=CONFIG['OCI_OPENAI_COMPATIBLE_ENDPOINT'],
                                                project='proyecto-ficticio', timeout=6.0, max_retries=0)
            self.assertEqual(await llm.json('sistema', 'telemetria'), VALID)
            client.responses.create.assert_awaited_once_with(model='modelo-de-prueba', instructions='sistema',
                input='telemetria', max_output_tokens=1024, store=False)

    async def test_incomplete_response_is_never_executed(self):
        with patch('openai.AsyncOpenAI') as constructor:
            constructor.return_value.responses.create = AsyncMock(return_value=SimpleNamespace(
                status='incomplete', output_text='{"ritmo":"ATAQUE"}'))
            llm = LLM('m', 'fake', CONFIG['OCI_OPENAI_COMPATIBLE_ENDPOINT'], 'fake-project')
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                await llm.json('s', 'u')

    async def test_missing_config_and_rules_are_distinct(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'Falta configuración OCI'):
                crear_llm('oci')
            self.assertIsNone(crear_llm('ninguno'))

    async def test_non_https_endpoint_is_rejected(self):
        config = {**CONFIG, 'OCI_OPENAI_COMPATIBLE_ENDPOINT': 'http://localhost/openai/v1'}
        with patch.dict(os.environ, config, clear=True):
            with self.assertRaisesRegex(ValueError, 'HTTPS'):
                crear_llm('oci')

    async def test_invalid_model_order_falls_back_to_rules(self):
        llm = SimpleNamespace(json=AsyncMock(return_value={**VALID, 'ritmo': 'VOLAR'}))
        tools = SimpleNamespace(llantas=AsyncMock(return_value={}), pista=AsyncMock(return_value={}),
                                estrategia=AsyncMock(return_value={}))
        cerebro = Cerebro({'estilo':'calculador','riesgo':3}, llm, log=lambda *_: None)
        with patch('director.reglas.decidir', return_value=dict(VALID)) as rules:
            result = await cerebro.decidir({'coche': {}, 'pista': {}}, tools)
            self.assertEqual(result['fuente'], 'reglas')
            rules.assert_called_once()

    async def test_timeout_falls_back_and_preserves_pending_pit(self):
        llm = SimpleNamespace(json=AsyncMock(side_effect=asyncio.TimeoutError))
        tools = SimpleNamespace(llantas=AsyncMock(return_value={}), pista=AsyncMock(return_value={}),
                                estrategia=AsyncMock(return_value={}))
        cerebro = Cerebro({}, llm, log=lambda *_: None)
        with patch('director.reglas.decidir', return_value=dict(VALID)):
            result = await cerebro.decidir({'coche': {}, 'pista': {}}, tools)
            self.assertEqual(result['fuente'], 'reglas')
        fallback = orden_de_respaldo({'vuelta': 30, 'coche': {
            'ritmo':'CARRERA', 'energia':'RECARGA', 'pit_programado': {'vuelta':32,'compuesto':'DURO'}}}, None)
        self.assertEqual(fallback['pits'], {'compuesto':'DURO', 'vuelta':2})
        self.assertEqual(fallback['energia'], 'RECARGA')

class TeamPolicyIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_guardrail_changes_llm_energy_before_send(self):
        llm = SimpleNamespace(json=AsyncMock(return_value={**VALID, 'energia':'BOOST'}))
        tools = SimpleNamespace(llantas=AsyncMock(return_value={}), pista=AsyncMock(return_value={}),
                                estrategia=AsyncMock(return_value={}))
        cerebro = Cerebro({'reserva_boost':40}, llm, log=lambda *_: None)
        result = await cerebro.decidir({'coche':{'bateria_pct':30},'pista':{}}, tools)
        self.assertEqual(result['energia'], 'RECARGA')
        self.assertEqual(result['fuente'], 'llm')

    async def test_guardrail_also_applies_to_rules(self):
        cerebro = Cerebro({'reserva_boost':40}, log=lambda *_: None)
        tools = SimpleNamespace(llantas=AsyncMock(return_value={}), pista=AsyncMock(return_value={}),
                                estrategia=AsyncMock(return_value={}))
        with patch('director.reglas.decidir', return_value={**VALID, 'energia':'BOOST'}):
            result = await cerebro.decidir({'coche':{'bateria_pct':30},'pista':{}}, tools)
        self.assertEqual(result['energia'], 'RECARGA')
        self.assertEqual(result['fuente'], 'reglas')


if __name__ == "__main__":
    unittest.main()
