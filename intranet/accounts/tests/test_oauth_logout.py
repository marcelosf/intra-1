from django.test import TestCase
from intranet.accounts.models import User
from django.shortcuts import resolve_url as r


class TestOauthLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Marc','marc@email.com', 'marcpass')

    def test_logout(self):
        """User must be logged out"""
        self.client.force_login(self.user)
        self.client.get(r('accounts:logout'))
        resp = self.client.get(r('access:new'))
        self.assertEqual(302, resp.status_code)
