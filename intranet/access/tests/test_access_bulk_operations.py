from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.contrib.auth.models import Group, Permission
from intranet.accounts.models import User
from intranet.access.models import Access
from intranet.access.forms import form_choices


class AccessBulkOprationsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(login='333', name='Tail', type='I', main_email='tail@test.com')
        can_add_access_perm = Permission.objects.get(name='Can add acesso') 
        user.user_permissions.add(can_add_access_perm)
        self.client.force_login(user)
        data = {
            'enable': True,
            'period_to': '2019-12-12',
            'period_from': '2019-12-20',
            'time_to': '13:13',
            'time_from': '20:20',
            'institution': 'IAG',
            'name': 'Marcelo',
            'job': 'Analista',
            'email': 'marcelo@test.com',
            'phone': '11912345678',
            'doc_type': 'RG',
            'doc_number': '202000002',
            'answerable': 'Pessoa1',
            'observation': 'Observações',
            'status': 'Autorizado',
            'created_by': user
        }

        data_2 = data.copy()
        Access.objects.create(**data)
        Access.objects.create(**data_2)

    def test_created_access(self):
        """Access must be created"""
        self.assertEqual(2, Access.objects.count())

    def test_access_form_action_period_to(self):
        """Period to must be 2020-01-05"""
        self.make_data()
        self.assertBulk(value='2020-01-05', field='period_to')

    def test_access_form_action_period_from(self):
        """Period from must be 2019-01-01"""
        self.make_data()
        self.assertBulk(value='2019-01-01', field='period_from')

    def test_access_form_action_time_to(self):
        """Time to must be 10:10"""
        self.make_data(time_to='10:10')
        self.assertBulk(value='10:10:00', field='time_to')

    def test_access_form_action_time_from(self):
        """Time to must be 10:10"""
        self.make_data(time_from='10:10')
        self.assertBulk(value='10:10:00', field='time_from')

    def test_access_form_action_incompleted(self):
        """It must update data with provided fields"""
        self.make_data(period_to='', period_from='', observation='obs')
        self.assertBulk('observation', 'obs')
        
    def assertBulk(self, field, value):
        """Test bulk operations"""
        obj = Access.objects.all()
        for item in obj:
            attr = getattr(item, field)
            with self.subTest():
                self.assertEqual(value, str(attr))
            with self.subTest():
                self.assertEqual(form_choices.WAITING, item.status)

    def make_data(self, **kwargs):
        obj = Access.objects.all()
        default = {
            'access': [obj[0].pk, obj[1].pk], 
            'period_from': '01/01/2019',
            'period_to': '01/05/2020',
            'time_from': '10:10',
            'time_to': '20:00',
            'enable': True,
            'observation': 'Observação'
        }

        data = dict(default, **kwargs)
        self.resp = self.client.post(r('access:access_list'), data=data)

