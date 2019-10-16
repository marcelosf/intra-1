from django.test import TestCase
from django.core import mail
from intranet.accounts.models import User


class TestAccount(TestCase):
    def setUp(self):
        self.obj = User()


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
        User.objects.create_user(
            login='3544444',
            main_email='main@test.com',
            password='92874',
            name='Marc',
            type='I '
        )
        self.assertTrue(User.objects.exists())


    def test_get_full_name(self):
        user = self.create_user()
        self.assertEqual('Marc Stold Further', user.get_full_name())


    def test_get_short_name(self):
        user = self.create_user()
        self.assertEqual('Marc', user.get_short_name())


    def test_email_user(self):
        user = self.create_user()
        user.email_user(subject='email test', message='message test', from_email='acesso@test.com')
        self.assertTrue(mail.outbox[0])


    def create_user(self):
        user = User.objects.create_user(
            login='3544444',
            main_email='main@test.com',
            password='92874',
            name='Marc Stold Further',
            type='I '
        )

        return user