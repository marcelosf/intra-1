from django.test import TestCase
from intranet.accounts.models import User
from django.shortcuts import resolve_url as r


class TestOauthLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(self.user)
        self.resp = self.client.get(r('accounts:logout'))

    def test_logout(self):
        """User must be logged out"""
        resp = self.client.get(r('access:new'))
        self.assertEqual(302, resp.status_code)

    def test_logout_redirect(self):
        """User must be redirected to home after legged out"""
        self.assertURLEqual(self.resp.url, '/')


    
