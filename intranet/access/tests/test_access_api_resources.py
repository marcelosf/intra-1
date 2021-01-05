import requests
from django.test import TestCase

from ..api_resources import Resource
from . import mock


class ResourceTest(TestCase):
    def setUp(self):
        self.obj = Resource()

    def test_has_attribute_get_alunos(self):
        self.assertTrue(hasattr(self.obj, 'get_alunos'))

    @mock.mock_api
    def test_get_alunos(self):
        alunos = self.obj.get_alunos()
        expected = mock.alunos_by_tipo_vinculo
        self.assertEqual(expected, alunos)

    def test_set_headers(self):
        self.obj.set_headers()
        expected = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.assertEqual(expected, self.obj.headers)

    @mock.mock_api
    def test_get_token(self):
        self.obj.set_headers()
        self.obj.get_token()
        expected = mock.token_payload
        self.assertEqual(expected, self.obj.token)

    @mock.mock_api
    def test_get_bearer(self):
        self.obj.set_headers()
        self.obj.get_token()
        self.obj.get_bearer()
        bearer = 'Bearer {}'.format(mock.token_payload.get('access_token'))
        expected = {'Authorization': bearer}
        self.assertEqual(expected, self.obj.bearer)
