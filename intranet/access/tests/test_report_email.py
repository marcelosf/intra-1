from django.test import TestCase
from django.core import mail
from intranet.accounts.models import User
from django.shortcuts import resolve_url as r


class TestReportEmail(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(user)
        data = {
            'enable': True,
            'period_to': '2019-12-20',
            'period_from': '2019-12-12',
            'time_to': '13:13',
            'time_from': '20:20',
            'institution': 'IAG',
            'name': 'Marcelo',
            'job': 'Analista',
            'email': 'marcelo@test.com',
            'phone': '11912345678',
            'doc_type': 'RG',
            'doc_number': '202000002',
            'answerable': 'Pessoa1',
            'observation': 'Observações',
            'status': 'Para autorização',
        }

        self.resp = self.client.post(r('access:new'), data)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        expect = '[IAG-INTRANET] Solicitação de acesso'
        self.assertEqual(expect, self.email.subject)

    def test_email_body(self):
        contents = [
            '12/12/2019',
            '20/12/2019',
            'Marcelo',
            'Pessoa1',
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

