from django.test import TestCase
from intranet.access.models import Access
from django.shortcuts import resolve_url as r
from intranet.access.models import Access
from intranet.accounts.models import User


class DetailViewLoggedInTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(user)
        access = Access.objects.create(enable=True, period_to='2019-12-12', period_from='2019-12-01',
                                            time_to='15:00', time_from='12:12', institution='IAG',
                                            name='Thomas Helperson', job='Analista', email='th@ia.com',
                                            phone='988889922', doc_type='RG', doc_number='3939393993', 
                                            answerable='Paul Gerdeson', observation='Observation', 
                                            status='Para autorização')
        self.response = self.client.get(r('access:access_detail', slug=access.uuid))
    
    def test_view(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'access/access_detail.html')

    def test_html(self):
        content = [
            'Ativo', 'Data inicial', 'Data final', 'Período', 'Instituição', 'Nome', 'Cargo',
            'Email', 'Telefone', 'Tipo de documento', 'Número do documento', 'Responsável',
            'Observação', 'Status', 'Data de criação'
        ]

        for expected in content:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_theme(self):
        """Template must be loaded"""
        self.assertTemplateUsed(self.response, 'base.html')

    def test_title(self):
        """It must show the title"""
        self.assertContains(self.response, 'Detalhes do acesso')

    def test_context(self):
        access = self.response.context['access']
        self.assertIsInstance(access, Access)

    def test_content(self):
        content = [
            '12/12/2019', '01/12/2019', '12:12', '15:00', 'IAG', 'Thomas Helperson', 'Analista',
            'th@ia.com', '988889922', 'RG', '3939393993', 'Paul Gerdeson', 'Observation', 
            'Para autorização'
        ]

        for expected in content:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_actions_menu(self):
        """Check if actions menu exists"""
        items = (
            ('Listar', 1),
            ('Adicionar', 1),
            ('Editar', 1),
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.response, expected, count)

class DetailViewTestLoggedOut(TestCase):
    def setUp(self):
        access = Access.objects.create(enable=True, period_to='2019-12-12', period_from='2019-12-01',
                                            time_to='15:00', time_from='12:12', institution='IAG',
                                            name='Thomas Helperson', job='Analista', email='th@ia.com',
                                            phone='988889922', doc_type='RG', doc_number='3939393993', 
                                            answerable='Paul Gerdeson', observation='Observation', 
                                            status='Para autorização')
        self.response = self.client.get(r('access:access_detail', slug=access.uuid))
    
    def test_url(self):
        """User must be loged in to access details"""
        self.assertEqual(302, self.response.status_code)
