from django.test import TestCase
from django.core import mail
from intranet.accounts.models import User


class TestAccount(TestCase):
    def setUp(self):
        self.obj = User.objects.create_user(
            login='3544444',
            main_email='main@test.com',
            password='92874',
            name='Marc Stold Further',
            type='I '
        )

    def test_user_instance(self):
        """User models must exists"""
        user = User()
        self.assertIsInstance(user, User)

    def test_user_attr(self):
        """It must contain usp user attributes"""
        expected = [
            'login', 'name', 'type', 'main_email', 'alternative_email',
            'usp_email', 'formatted_phone', 'wsuserid', 'bond', 'is_staff',
            'is_active', 'date_joined' 
        ]

        for item in expected:
            with self.subTest():
                self.assertTrue(hasattr(self.obj, item))

    def test_create_user(self):
        """User must exists on database"""
        self.assertTrue(User.objects.exists())

    def test_get_full_name(self):
        self.assertEqual('Marc Stold Further', self.obj.get_full_name())

    def test_get_short_name(self):
        self.assertEqual('Marc', self.obj.get_short_name())

    def test_email_user(self):
        self.obj.email_user(subject='email test', message='message test', from_email='acesso@test.com')
        self.assertTrue(mail.outbox[0])

    def test_get_phone(self):
        self.obj.formatted_phone = '3334455'
        self.assertEqual('3334455', self.obj.get_phone())
    
    def test_is_servidor(self):
        self.obj.bond = "[{'tipoVinculo': 'ALUNO'}, {'tipoVinculo': 'SERVIDOR'}]"
        self.assertTrue(self.obj.is_servidor())

    def test_is_servidor_not(self):
        self.obj.bond = "[{'tipoVinculo': 'ALUNO'}, {'tipoVinculo': 'ALUNO'}]"
        self.assertFalse(self.obj.is_servidor())

    def test_unidade_is_allowed(self):
        self.obj.bond = "[{'codigoUnidade': '12'}, {'codigoUnidade': '14', 'tipoVinculo': 'SERVIDOR'}]"
        self.assertTrue(self.obj.unidade_is_allowed())

    def test_unidade_is_allowed_not(self):
        self.obj.bond = "[{'codigoUnidade': '12'}, {'codigoUnidade': '13', 'tipoVinculo': 'SERVIDOR'}]"
        self.assertFalse(self.obj.unidade_is_allowed())
