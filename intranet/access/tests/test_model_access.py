from django.test import TestCase
from intranet.accounts.models import User
from intranet.access.models import Access
from datetime import datetime
from django.shortcuts import resolve_url as r


class TestAccessModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.obj = self.make_data()

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

    def test_has_weekdays_field(self):
        fields = [str(item.name) for item in Access._meta.fields]
        self.assertIn('weekdays', fields)

    def test_weekdays_value(self):
        obj = self.make_data(weekdays=[0, 1])
        expected = [0, 1]
        self.assertListEqual(expected, obj.weekdays)

    def test_weekdays_not_required(self):
        """Weekdays should not be required"""
        field = Access.weekdays.field
        self.assertTrue(field.null)

    def test_weekdays_choices(self):
        """Weekdays should not be required"""
        field = Access.weekdays.field
        self.assertIsNotNone(field.choices)

    def test_get_week_names(self):
        """Access shoud have get_weekdays attribute"""
        self.assertTrue(hasattr(Access, 'get_week_name'))

    def test_get_week_names_value(self):
        """get_weekdays must return a list"""
        obj = self.make_data(weekdays=['0', '1'])
        expected = ['Segunda', 'Terça']
        self.assertListEqual(expected, obj.get_week_name())

    def test_get_weekdays(self):
        obj = self.make_data(weekdays="[1,2]")
        expected = [1,2]
        self.assertListEqual(expected, obj.get_weekdays())

    def test_has_manage_access_status_permission(self):
        """Model shoud have can_manage_access_status"""
        expected = ('can_manage_access_status', 'Can manage access status')
        permissions = self.obj._meta.permissions
        self.assertIn(expected, permissions)

    def make_data(self, **kwargs):
        default_data = dict(enable=True, period_to='2019-12-12', period_from='2019-12-20',
                        time_to='13:13', time_from='20:20', institution='IAG', 
                        name='Marcelo', job='Analista', email='marcelo@test.com',
                        phone='11912345678', doc_type='RG', doc_number='202000002',
                        answerable='Pessoa1', observation='Observações', 
                        status='Para autorização', created_by=self.user)
        data = dict(default_data, **kwargs)

        obj = Access.objects.create(**data)

        return obj        

