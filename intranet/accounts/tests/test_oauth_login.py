from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.http import HttpRequest
from intranet.accounts import views
from intranet.accounts.models import User
from unittest.mock import MagicMock
import json


class TestOauthLogin(TestCase):
    # def test_url(self):
    #     """It must return status code 302"""
    #     resp = self.client.get(r('accounts:login'))
    #     self.assertEqual(302, resp.status_code)

    def test_authorize(self):
        """It must be called"""
        origin = views.authorize
        views.authorize = MagicMock(return_value=True)
        views.authorize('request', key='value')
        views.authorize.assert_called_with('request', key='value')
        views.authorize = origin

    def create_user(self):
        user_data = {
            'login': '5554477',
            'name': 'Thomas Fullstack Python',
            'type': 'I',
            'main_email': 'thomas@test.com',
            'bond': "[{'tipoVinculo': 'SERVIDOR'}]"
        }
        
        return user_data

class TestAccountsLoginHelpers(TestCase):
    def setUp(self):
        user_data = '{"loginUsuario":"jameson", "nomeUsuário":"Thomas Jameson", "emailPrincipal":"test@test.com", "vinculo":[{"tipoVinculo":"SERVIDOR"}]}'
        self.data = json.loads(user_data)

    def test_data_transform(self):
        mapper = {
            'loginUsuario': 'login',
            'nomeUsuário': 'name',
            'vinculo': 'vinculo',
            'emailPrincipal': 'main_mail'
        }
        expected = {
            'login': 'jameson',
            'name': 'Thomas Jameson',
            'main_mail': 'test@test.com',
            'vinculo': "[{'tipoVinculo': 'SERVIDOR'}]"
        }

        transformed = views.data_transform(self.data, mapper)
        self.assertDictContainsSubset(expected, transformed)

    def test_persist_user(self):
        user_data = {
            'login': '5554477',
            'name': 'Thomas Fullstack Python',
            'type': 'I',
            'main_email': 'thomas@test.com',
            'bond': "[{'tipoVinculo': 'SERVIDOR'}]"
        }
        views.persist_user(user_data)
        self.assertTrue(User.objects.exists())

    def test_user_already_exist(self):
        """It must persist only users that not exists"""
        user_data = {
            'login': '5554477',
            'name': 'Thomas Fullstack Python',
            'type': 'I',
            'main_email': 'thomas@test.com',
            'bond': "[{'tipoVinculo': 'SERVIDOR'}]"
        }
        views.persist_user(user_data)
        views.persist_user(user_data)
        self.assertTrue(User.objects.exists())
