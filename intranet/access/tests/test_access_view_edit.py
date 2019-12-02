from django.test import TestCase
from django.shortcuts import resolve_url as r
from intranet.access.models import Access
from intranet.accounts.models import User
from intranet.access.forms.forms import AccessForm


class AccessViewEditTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        obj = Access(
            enable=True,
            period_to='2019-12-12',
            period_from='2019-12-20',
            time_to='13:13',
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
        )
        obj.save()

        self.resp = self.client.get(r('access:access_edit', slug=obj.uuid))

    def test_url(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)
        
    def test_template(self):
        """It must render /access/access_edit.html"""
        self.assertTemplateUsed(self.resp, 'access/access_edit.html')

    def test_base_template(self):
        """It must extends base.html"""
        self.assertTemplateUsed(self.resp, 'base.html')
    
    def test_html(self):
        items = (
            ('<select', 3),
            ('type="date"', 2),
            ('type="time"', 2),
            ('type="text"', 5),
            ('type="email"', 1),
            ('type="checkbox"', 1),
            ('<textarea', 1)
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, AccessForm)

    def test_form_is_bound(self):
        form = self.resp.context['form']
        self.assertTrue(form.is_bound)

    def test_form_content(self):
        items = [
            '2019-12-12',
            '2019-12-20',
            '13:13',
            '20:20',
            'IAG',
            'Marcelo',
            'Analista',
            'marcelo@test.com',
            '11912345678',
            'RG',
            '202000002',
            'Pessoa1',
            'Observações',
            'Para autorização',
        ]

        for expected in items:
            with self.subTest():
                self.assertContains(self.resp, expected)
