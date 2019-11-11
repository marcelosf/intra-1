from django.test import TestCase
from intranet.accounts.models import User
from intranet.access.models import Access
from datetime import datetime
from django.shortcuts import resolve_url as r


class TestAccessModel(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.obj = Access(
            enable=True,
            period_to='2019-12-12',
            period_from='2019-12-20',
            time_to='13:13',
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
            created_by=user
        )

        self.obj.save()

    def test_instance(self):
        """Must be an Instance of Access model"""
        access = Access()
        self.assertIsInstance(access, Access)

    def test_create(self):
        """Must exists on database"""
        self.assertTrue(Access.objects.exists())

    def test_created_at(self):
        """Must have an auto created attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_created_by(self):
        """Must have a created by attr"""
        self.assertIsInstance(self.obj.created_by, User)

    def test_uuid_field(self):
        """Access must have a uuid field"""
        self.assertTrue(Access._meta.get_field('uuid'))

    def test_uuid_field_unique(self):
        uuid_field = Access._meta.get_field('uuid')
        self.assertTrue(uuid_field.unique)

    def test_get_absolute_url(self):
        url = r('access:access_detail', slug=self.obj.uuid)
        self.assertEqual(url, self.obj.get_absolute_url())


