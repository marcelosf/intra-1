from django.test import TestCase
from intranet.access import resources
import json


class AccessResourcesTest(TestCase):
    def setUp(self):
        self.resp = resources

    def test_status_code(self):
        """Status code should be 200"""
        self.assertEqual(200, self.resp.get_alunos().status_code)

    def test_get_alunos(self):
        """It should get alunos data"""
        expected = self.make_json()
        self.assertEqual(expected, self.resp.get_alunos().json())

    def test_get_alunos_by_name(self):
        """It should get alunos by name"""
        data = '[{"nome": "Capistrano", "cargo": "Aluno graduação", "email": "capis@usp.com",\
                    "phone": "1112233", "doc": "usp", "doc_num": "456666", "answerable": "Shista",\
                    "departament": "ACA" }]'

        expected = self.make_json(data=data)
        query = {'replicated': 'students', 'name': 'Capistrano'}
        self.assertEqual(expected, self.resp.get_alunos(query=query).json())


    def make_json(self, data=None):
        if not data:
            data = '[{"nome": "Capistrano", "cargo": "Aluno graduação", "email": "capis@usp.com",\
                        "phone": "1112233", "doc": "usp", "doc_num": "456666", "answerable": "Shista",\
                        "departament": "ACA" }, {"nome": "Tentaculous", "cargo": "Aluno graduação",\
                        "email": "tents@usp.com", "phone": "187632433", "doc": "usp", "doc_num": "9823456",\
                        "answerable": "sheba", "deoartament": "ACA"}, {"nome": "Zibauwe", "cargo": "Aluno graduação",\
                        "email": "zin@usp.com", "phone": "1879999433", "doc": "usp", "doc_num": "9823333",\
                        "answerable": "sheba", "departament": "AGG"}]'


        json_data = json.loads(data)
        return json_data
            

