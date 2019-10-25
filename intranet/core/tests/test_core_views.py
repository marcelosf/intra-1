from django.test import TestCase
from django.shortcuts import resolve_url as r


class TestCoreViews(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:main'))
    
    def test_url(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """It must render main template"""
        self.assertTemplateUsed(self.resp, 'main.html')

    def test_template_inheritance(self):
        """It must render base template"""
        self.assertTemplateUsed(self.resp, 'base.html')

    def test_has_nav_bar(self):
        """It must contain a nav bar"""
        self.assertContains(self.resp, '<nav')


