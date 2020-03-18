from django.test import TestCase
from django.conf import settings
from intranet.access import resources
import json
import httpretty


class MockApi():
    def make_json(self, data):
        json_data = json.loads(data)
        return json_data

    def mock_api(self, uri, body, query=None):
        httpretty.enable()
        httpretty.register_uri(
            method=httpretty.GET,
            uri=uri,
            status=200,
            content_type='application/json',
            body=body
        )
        resp = resources.get_alunos(query=query)
        return resp


class AccessResourcesAllTest(TestCase):
    def setUp(self):
        self.mock_api = MockApi()
        body = self.make_data()
        self.resp_all = self.mock_api.mock_api(
            uri=settings.ALUNOS_RESOURCES,
            body=body,
        )
    
    def tearDown(self):
        return super().tearDown()
        httpretty.disable()

    def test_status_code(self):
        """Status code should be 200"""
        self.assertEqual(200, self.resp_all.status_code)

    def test_get_alunos(self):
        """It should get alunos data"""
        data = self.make_data()
        expected = self.mock_api.make_json(data=data)
        self.assertEqual(expected, self.resp_all.json())

    def make_data(self):
        data = '[{"nome": "Capistrano", "cargo": "Aluno graduação", "email": "capis@usp.com",\
                        "phone": "1112233", "doc": "usp", "doc_num": "456666", "answerable": "Shista",\
                        "departament": "ACA" }, {"nome": "Tentaculous", "cargo": "Aluno graduação",\
                        "email": "tents@usp.com", "phone": "187632433", "doc": "usp", "doc_num": "9823456",\
                        "answerable": "sheba", "deoartament": "ACA"}, {"nome": "Zibauwe", "cargo": "Aluno graduação",\
                        "email": "zin@usp.com", "phone": "1879999433", "doc": "usp", "doc_num": "9823333",\
                        "answerable": "sheba", "departament": "AGG"}]'
        return data


class AccessResourcesUniqueTest(TestCase):
    def setUp(self):
        self.mock_api = MockApi()
        self.resp_unique = self.mock_api.mock_api(
            uri='http://api.iag.usp.br/replicado/alunos/name/Capistrano',
            body=self.make_data(),
            query={'replicado': 'alunos', 'name': 'Capistrano'}
        )

    def tearDown(self):
        return super().tearDown()
        httpretty.disable()

    def test_get_alunos_by_name(self):
        """It should get alunos by name"""
        data = self.make_data()
        expected = self.mock_api.make_json(data=data)
        self.assertEqual(expected, self.resp_unique.json())

    def make_data(self):    
        data = '[{"nome": "Capistrano", "cargo": "Aluno graduação", "email": "capis@usp.com",\
                    "phone": "1112233", "doc": "usp", "doc_num": "456666", "answerable": "Shista",\
                    "departament": "ACA"}]'
        return data
