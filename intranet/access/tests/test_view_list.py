from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from intranet.access.models import Access
from intranet.access.filters import PERPAGE
from intranet.access.forms import form_choices, forms
from django.core.paginator import Page
from django.shortcuts import resolve_url as r
from intranet.accounts.models import User


class AccessListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        can_add_access_perm = Permission.objects.get(name='Can add acesso')
        can_change_access_perm = Permission.objects.get(name='Can change acesso')
        user.user_permissions.set([can_add_access_perm, can_change_access_perm])
        self.client.force_login(user)
        for i in range(40):
            self.obj = Access.objects.create(
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
    
        self.resp = self.client.get(r('access:access_list'))

    def test_url(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'access/access_list.html')

    def test_html(self):
        content = ['Nome', 'Instituição', 'Período', 'Autorização', 'Detalhar']

        for expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_context(self):
        form = self.resp.context
        self.assertIn('list', form)

    def test_filter(self):
        content = ['name', 'period_to', 'period_from', 'status']

        for expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_paginator_context(self):
        access_list = self.resp.context['list']
        self.assertIsInstance(access_list.qs, Page)

    def test_paginator_range(self):
        page_range = self.resp.context['page_list']
        self.assertIsInstance(page_range, list)

    def test_paginator_range_content(self):
        page_range = self.resp.context['page_list']
        expected = list(range(1,5))
        self.assertListEqual(expected, page_range)

    def test_paginator_html(self):
        num_of_pages = 40//PERPAGE
        content = (
            ('page-item', num_of_pages + 2),
            ('page-item active', 1)
        )
           
        for expected , count in content:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_include_pagination(self):
        self.assertTemplateUsed(self.resp, 'pagination.html')

    def test_actions_menu(self):
        """Check if actions menu exists"""
        items = (
            ('Buscar', 1),
            ('Adicionar', 1),
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_context_has_actions_form(self):
        """Context should have an actions_form"""
        self.assertIn('actions_form', self.resp.context)

    def test_select_checkbox(self):
        """List item should have checkbox"""
        count = PERPAGE + 2
        self.assertContains(self.resp, 'type="checkbox"', count)

    def test_html_actions_form(self):
        """Template should have actions field"""
        content = (
            'Ativo',
            'Data de início', 
            'Data de término',
            'Hora de início', 
            'Hora de término',
            'Observação',
            '>OK<'
        )

        for expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_form_no_validate(self):
        """Don't validate data on form"""
        self.assertContains(self.resp, 'novalidate')

class AccessListPostTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(login='333', name='Tail', type='I', main_email='tail@test.com')
        can_change_access_perm = Permission.objects.get(name='Can change acesso') 
        user.user_permissions.add(can_change_access_perm)
        self.client.force_login(user)
        data = {
            'enable': True,
            'period_to': '2020-12-12',
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
    
    def test_access_created(self):
        """Access must be created"""
        self.assertEqual(2, Access.objects.count())

    def test_bulk_update(self):
        """Period to should be 10/10/2020"""
        self.make_request()
        self.assertContains(self.resp, '10/10/2020', 2)

    def test_form_errors(self):
        """Form must contain errors"""
        self.make_request(period_from='10/20/2020')
        form = self.resp.context['actions_form']
        self.assertGreater(len(form.errors.keys()), 0)
    
    def test_non_fields_error_message(self):
        """It must contain the error message"""
        self.make_request(period_from='10/20/2020')
        expected = 'A Data de início deve ser menor do que a Data de término'
        self.assertContains(self.resp, expected)

    def make_request(self, **kwargs):
        access = Access.objects.all()
        default = {
            'access': [access[0].pk, access[1].pk], 
            'period_from': '01/01/2019',
            'period_to': '10/10/2020',
            'time_from': '10:10',
            'time_to': '20:00',
            'enable': True,
            'observation': 'Observação'
        }

        data = dict(default, **kwargs)
        self.resp = self.client.post(r('access:access_list'), data)

        

class AccessListPortariaTest(TestCase):
    def setUp(self):
        status_list = ['Para autorização', 'Não autorizado', 'Autorizado']
        user = User.objects.create_user(login='333', name='Tail', type='I', main_email='tail@test.com')
        for status in status_list:
            Access.objects.create(
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
                status=status,
                created_by=user
            )

        user = User.objects.create_user(login='444', name='Tail', type='I', main_email='tail@test.com')
        group = Group.objects.create(name=settings.PORTARIA_GROUP_NAME)
        user.groups.add(group)
        self.client.force_login(user)   
        self.resp = self.client.get(r('access:access_list'))

    def test_portaria_list_view(self):
        """Portaria group must view only authorized access"""
        wating = 'btn-info'
        not_authorized = 'btn-danger'
        authorized = 'btn-success'

        restricted_status = [wating, not_authorized]

        for status in restricted_status:
            with self.subTest():
                self.assertNotContains(self.resp, status)
                self.assertContains(self.resp, authorized)

    def test_actions_menu(self):
        """Add button can not be showed"""
        self.assertNotContains(self.resp, 'Adicionar')

    def test_not_see_checkbox_list_item(self):
        """Portaria group do not see checkbox items"""
        self.assertNotContains(self.resp, 'type="checkbox"')