"""Amplía estas pruebas con una situación propia antes de generar tu imagen."""
import unittest
from director.politica_equipo import ajustar_orden


class PoliticaTests(unittest.TestCase):
    def orden(self):
        return {"ritmo": "CARRERA", "energia": "BOOST", "pits": {"compuesto": "DURO", "vuelta": 2},
                "radio": "Vamos", "razonamiento": "Rival cerca"}

    def test_reserva_impide_boost_y_conserva_parada(self):
        original = self.orden()
        resultado = ajustar_orden(original, {"coche": {"bateria_pct": 30}}, {"reserva_boost": 40})
        self.assertEqual(resultado["energia"], "RECARGA")
        self.assertEqual(resultado["pits"], original["pits"])
        self.assertEqual(original["energia"], "BOOST")

    def test_reserva_suficiente_permite_boost(self):
        self.assertEqual(ajustar_orden(self.orden(), {"coche": {"bateria_pct": 40}},
                                      {"reserva_boost": 40})["energia"], "BOOST")

    def test_umbral_personalizado(self):
        self.assertEqual(ajustar_orden(self.orden(), {"coche": {"bateria_pct": 50}},
                                      {"reserva_boost": 72})["energia"], "RECARGA")
