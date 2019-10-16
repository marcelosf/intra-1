from django.test import TestCase
from intranet.accounts.managers import UserManager


class TestUserManager(TestCase):
    def setUp(self):
        self.obj = UserManager()

    
    def test_user_manager(self):
        """It must exists"""
        self.assertIsInstance(self.obj, UserManager)
