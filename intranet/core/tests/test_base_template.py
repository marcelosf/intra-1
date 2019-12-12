from django.test import TestCase


class BaseTemplateTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'base.html')

    def test_navbar_fixed(self):
        self.assertContains(self.resp, 'fixed-top')