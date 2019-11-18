from django.test import TestCase
from django.test.utils import override_settings


class CoreHttpErrorsTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/no-exists/')

    def test_status_code(self):
        """Status code must be 404"""
        self.assertEqual(404, self.resp.status_code)

    @override_settings(DEBUG=False)
    def test_404_message(self):
        """It must show a 404 message"""
        message = 'Desculpe, não encontramos o endereço requisitado.'
        self.assertIn(message, str(self.resp.content.decode('utf-8')))