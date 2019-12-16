from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from intranet.accounts import views
from intranet.accounts.models import User
from unittest.mock import MagicMock, patch
import json


class TestOauthLogin(TestCase):
    def test_unidade_not_allowed(self):
        user = self.create_user()
        resp = views.validate_allowed_unidade(user)
        self.assertFalse(resp)
    
    def test_authorize(self):
        """It must be called"""
        origin = views.authorize
        views.authorize = MagicMock(return_value=True)
        views.authorize('request', key='value')
        views.authorize.assert_called_with('request', key='value')
        views.authorize = origin

    def test_update_user_if_alread_exists(self):
        """User data must be updated if alread exists"""
        user = dict(
            login='5554477',
            name='Thomas Fullstack Python', 
            type='I', 
            main_email='th@test.com'
        )

        self.create_user()
        user, created = User.objects.update_or_create_user(**user)
        self.assertFalse(created)

    def test_update_user_if_not_exists(self):
        """User must be creates if not exists"""
        user = dict(
            login='5554',
            name='Thomas Fullstack Python', 
            type='I', 
            main_email='th@test.com'
        )

        self.create_user()
        user, created = User.objects.update_or_create_user(**user)
        self.assertTrue(created)    

    def create_user(self):
        user = User.objects.create_user(
            login='5554477',
            name='Thomas Fullstack Python',
            type='I',
            main_email='thomas@test.com'
        )
        user.bond="[{'tipoVinculo': 'SERVIDOR', 'codigoUnidade': 12}]"
        return user

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

class TestAccountsLogin(TestCase):
    def setUp(self):
        origin = views.login
        views.login = MagicMock(return_value=HttpResponse(status=302))
        views.login('request', key='value')
        self.resp = views.login('request', key='value')
        views.login = origin

    def test_login_url(self):
        """It must redirect to login page"""
        self.assertEqual(302, self.resp.status_code)
