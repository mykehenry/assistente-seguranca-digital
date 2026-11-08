from django.test import SimpleTestCase
from django.urls import reverse

from .analysis import analyze


class AnalysisTests(SimpleTestCase):
    def test_urgency_and_secret_are_explained(self):
        result = analyze("Urgente: sua conta será bloqueada. Informe sua senha agora.")
        self.assertEqual(result.level, "alto")
        self.assertIn("Pressão para agir rápido", [item.title for item in result.findings])
        self.assertIn("Pedido de informação sensível", [item.title for item in result.findings])

    def test_url_patterns(self):
        result = analyze("http://usuario@203.0.113.7:8080/login")
        titles = [item.title for item in result.findings]
        self.assertIn("Conexão sem HTTPS", titles)
        self.assertIn("Domínio disfarçado", titles)
        self.assertIn("Endereço por IP", titles)
        self.assertIn("Porta incomum", titles)

    def test_no_signal_never_claims_safety(self):
        result = analyze("Nossa reunião será amanhã às 14h.")
        self.assertEqual(result.level, "indefinido")
        self.assertIn("não confirma", result.summary)

    def test_invalid_input(self):
        for content in ("", " " * 4, "a" * 1001):
            with self.subTest(content=content[:10]), self.assertRaises(ValueError):
                analyze(content)


class ViewTests(SimpleTestCase):
    def test_home_and_security_headers(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "não abre os links")
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertIn("default-src 'self'", response["Content-Security-Policy"])

    def test_post_does_not_echo_input(self):
        response = self.client.post(reverse("home"), {"content": "Urgente: senha SEGREDO-EXEMPLO"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sinais encontrados")
        self.assertNotContains(response, "SEGREDO-EXEMPLO")

    def test_too_long_input_shows_error(self):
        response = self.client.post(reverse("home"), {"content": "a" * 1001})
        self.assertContains(response, "até 1.000 caracteres")
