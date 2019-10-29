from django.test import TestCase
from django.shortcuts import resolve_url as r
from intranet.accounts.models import User


class TestAccountsUrls(TestCase):
    def setUp(self):
        user = User.objects.create(
            login='3333333',
            name='Marc Thompson',
            type='I',
            main_email='marc@test.com',
            is_staff=False,
            is_active=True
        )
        self.client.force_login(user)
        self.resp = self.client.get(r('accounts:user'))

    def test_url(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'user.html')

    def test_content(self):
        words = (
            ('Marc Thompson'),
            ('3333333'),
            ('marc@test.com')
        )

        for item in words:
            with self.subTest():
                self.assertContains(self.resp, item)



class TestAccountsUrlLoggedOut(TestCase):
    def test_user_url(self):
        """User must be logged in to access user url"""
        resp = self.client.get(r('accounts:user'))
        self.assertEqual(302, resp.status_code)
