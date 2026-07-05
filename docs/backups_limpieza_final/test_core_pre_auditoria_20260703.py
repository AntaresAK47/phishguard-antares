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


if __name__ == "__main__":
    unittest.main()
