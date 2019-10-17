from django.test import TestCase
from django.shortcuts import resolve_url as r

class TestAccountsUrls(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('accounts:user'))
    
    def test_url(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'user.html')