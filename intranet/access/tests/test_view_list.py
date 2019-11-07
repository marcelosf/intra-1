from django.test import TestCase
from intranet.access.models import Access


class AccessListViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/access/')

    def test_url(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'access/report_list.html')

    def test_html(self):
        content = ['Nome', 'Instituição', 'Período', 'Autorização', 'Detalhar']

        for expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_context(self):
        form = self.resp.context
        self.assertIn('list', form)

    def test_filter(self):
        content = ['name', 'period_to', 'period_from', 'enable']

        for expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected)




        
    