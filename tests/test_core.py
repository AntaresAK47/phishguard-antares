import unittest

from src.report_builder import build_report_text, neutralize_links
from src.url_features import build_feature_frame, safe_text, split_raw_links, summarize_features


class UrlFeatureTests(unittest.TestCase):
    def test_safe_text_accepts_none_and_lists(self):
        self.assertEqual(safe_text(None), "")
        self.assertEqual(safe_text(["https://example.com"]), "['https://example.com']")

    def test_split_raw_links_detects_common_link_types(self):
        links = split_raw_links("Ver https://login.example.com mailto:soporte@example.com cid:image001.jpg")
        self.assertIn("https://login.example.com", links)
        self.assertIn("mailto:soporte@example.com", links)
        self.assertIn("cid:image001.jpg", links)

    def test_feature_frame_keeps_expected_shape(self):
        frame = build_feature_frame("https://secure-login.example.com/verify?token=123")
        self.assertEqual(frame.shape, (1, 27))
        self.assertEqual(int(frame.loc[0, "has_web_url"]), 1)

    def test_summary_has_user_facing_keys(self):
        summary = summarize_features("https://secure-login.example.com/verify?token=123")
        self.assertEqual(summary["URL web detectadas"], 1)
        self.assertEqual(summary["Usa HTTPS"], "Sí")


class ReportBuilderTests(unittest.TestCase):
    def test_neutralize_links_makes_urls_non_clickable(self):
        text = neutralize_links("https://example.com http://test.com www.site.com")
        self.assertIn("hxxps://example.com", text)
        self.assertIn("hxxp://test.com", text)
        self.assertIn("www[.]site.com", text)

    def test_comparative_report_uses_riesgo_key(self):
        report = build_report_text(
            {
                "modelo_nombre": "Modelo híbrido",
                "clase_predicha": "Phishing probable",
                "probabilidad_formato": "91.00%",
                "nivel_riesgo": "Crítico",
                "mensaje_riesgo": "Riesgo alto.",
            },
            comparative_rows=[
                {
                    "Modelo": "Modelo híbrido",
                    "Clase estimada": "Phishing probable",
                    "Probabilidad phishing": "91.00%",
                    "Riesgo": "Crítico",
                }
            ],
        )
        self.assertIn("Riesgo: Crítico", report)


class HybridFrameTests(unittest.TestCase):
    def test_hybrid_frame_has_text_plus_27_features(self):
        from src.url_features import build_hybrid_frame

        frame = build_hybrid_frame("mensaje de prueba", "https://example.com/login")
        self.assertEqual(frame.shape, (1, 28))
        self.assertEqual(frame.columns[0], "text")

    def test_neutralized_urls_are_treated_as_text_links(self):
        # Entradas defensivas hxxps:// y dominio[.]tld deben contarse como URL web
        # sin necesidad de reactivarlas ni visitarlas.
        frame = build_feature_frame("hxxps://secure-login[.]example[.]com/verify")
        self.assertEqual(int(frame.loc[0, "has_web_url"]), 1)
        self.assertGreaterEqual(int(frame.loc[0, "url_web_count"]), 1)


class PredictorContractTests(unittest.TestCase):
    """Blinda el contrato público validado de src.predictor.analyze."""

    def test_analyze_signature_is_preserved(self):
        import inspect

        from src.predictor import analyze

        signature = inspect.signature(analyze)
        parameters = list(signature.parameters.items())
        self.assertEqual(
            [name for name, _ in parameters],
            ["model_name", "subject", "body", "urls_raw"],
        )
        self.assertEqual(parameters[1][1].default, "")
        self.assertEqual(parameters[2][1].default, "")
        self.assertEqual(parameters[3][1].default, "")

    def test_normalize_model_name_accepts_documented_aliases(self):
        from src.predictor import normalize_model_name

        self.assertEqual(normalize_model_name("Híbrido"), "hibrido")
        self.assertEqual(normalize_model_name("texto"), "textual")
        self.assertEqual(normalize_model_name("URLS"), "url")
        with self.assertRaises(ValueError):
            normalize_model_name("desconocido")

    def test_empty_inputs_raise_controlled_value_error(self):
        from src.predictor import analyze

        for model_name in ("textual", "url", "hibrido"):
            with self.assertRaises(ValueError):
                analyze(model_name=model_name)


class LocalOnlyInferenceTests(unittest.TestCase):
    """
    Evidencia de seguridad: la inferencia completa debe funcionar con la red
    bloqueada a nivel de socket. Cualquier intento de conexión rompe la prueba.
    """

    def test_full_analysis_works_with_network_blocked(self):
        import socket

        from src.predictor import analyze

        def _blocked(*args, **kwargs):
            raise AssertionError("Intento de conexión de red durante la inferencia")

        original_connect = socket.socket.connect
        original_create = socket.create_connection
        original_getaddrinfo = socket.getaddrinfo
        socket.socket.connect = _blocked
        socket.create_connection = _blocked
        socket.getaddrinfo = _blocked
        try:
            result = analyze(
                model_name="hibrido",
                subject="Verificación urgente",
                body="Debe actualizar su cuenta para evitar suspensión.",
                urls_raw="https://secure-login.example.com/verify?token=123",
            )
        finally:
            socket.socket.connect = original_connect
            socket.create_connection = original_create
            socket.getaddrinfo = original_getaddrinfo

        self.assertIn(result["clase_predicha"], {"Phishing probable", "Legítimo probable"})
        self.assertIsNotNone(result["probabilidad_phishing"])

    def test_analysis_is_repeatable(self):
        from src.predictor import analyze

        kwargs = {
            "model_name": "textual",
            "subject": "Reunión de equipo",
            "body": "La reunión de mañana queda confirmada a las 10:00.",
        }
        first = analyze(**kwargs)
        second = analyze(**kwargs)
        self.assertEqual(first["label_predicho"], second["label_predicho"])
        self.assertEqual(first["probabilidad_phishing"], second["probabilidad_phishing"])


class ReportNeutralizationTests(unittest.TestCase):
    def test_report_neutralizes_links_embedded_in_body(self):
        report = build_report_text(
            {
                "modelo_nombre": "Modelo híbrido",
                "clase_predicha": "Phishing probable",
                "probabilidad_formato": "80.00%",
                "nivel_riesgo": "Muy alto",
                "mensaje_riesgo": "Riesgo elevado.",
            },
            subject="Aviso https://alerta.example.com",
            body="Ingrese en http://login.example.com o www.example.com ahora.",
            urls_raw="https://secure-login.example.com/verify",
        )
        self.assertNotIn("https://", report)
        self.assertNotIn("http://", report.replace("hxxp://", "").replace("hxxps://", ""))
        self.assertIn("hxxps://", report)
        self.assertIn("www[.]", report)


if __name__ == "__main__":
    unittest.main()
