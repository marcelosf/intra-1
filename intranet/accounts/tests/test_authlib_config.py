from django.test import TestCase
from django.conf import settings
from authlib.integrations.django_client import OAuth

class TestAuthlibConfig(TestCase):
    def test_oauth(self):
        oauth = getattr(settings, 'USP_CLIENT', None)
        self.assertIsInstance(oauth, OAuth)

    def test_redirect_uri(self):
        uri = getattr(settings, 'REDIRECT_URI', None)
        self.assertNotEqual(None, uri)

    def test_authlib_oauth_clients(self):
        authlib = getattr(settings, 'AUTHLIB_OAUTH_CLIENTS', None)
        self.assertNotEqual(None, authlib)
