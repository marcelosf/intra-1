from django.test import TestCase
from django.shortcuts import resolve_url as r
from intranet.accounts.models import User


class BaseTemplateLoggedInTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            login='2222222',
            name='Marc',
            main_email='marc@test.com',
            type='I'
        )
        self.client.force_login(user)
        self.resp = self.client.get('/')

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'base.html')

    def test_navbar_fixed(self):
        self.assertContains(self.resp, 'fixed-top')

    def test_logout_html_button(self):
        self.assertContains(self.resp, 'Logout')

    def test_logout_link(self):
        self.assertContains(self.resp, r('accounts:logout'))

    def test_show_user_name(self):
        expected = 'Marc'
        self.assertContains(self.resp, expected)

    def test_has_no_login_button(self):
        self.assertNotContains(self.resp, 'Login')
        

class BaseTemplateLoggedOutTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_has_login_button(self):
        self.assertContains(self.resp, 'Login')

    def test_has_no_logout_button(self):
        self.assertNotContains(self.resp, 'Logout')