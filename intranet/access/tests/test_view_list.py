from django.test import TestCase
from django.contrib.auth.models import Group
from intranet.access.models import Access
from intranet.access.filters import PERPAGE
from django.core.paginator import Page
from django.shortcuts import resolve_url as r
from intranet.accounts.models import User


class AccessListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
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
            ('<li class="waves-effect"', num_of_pages - 1),
            ('<li class="active"', 1)
        )
           
        for expected , count in content:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_include_pagination(self):
        self.assertTemplateUsed(self.resp, 'pagination.html')



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
        group = Group.objects.create(name='portaria')
        user.groups.add(group)
        self.client.force_login(user)   
        self.resp = self.client.get(r('access:access_list'))

    def test_portaria_list_view(self):
        """Portaria group must view only authorized access"""
        restricted_status = ['>Para autorização\n', '>Não autorizado\n']

        for status in restricted_status:
            with self.subTest():
                self.assertNotContains(self.resp, status)
                self.assertContains(self.resp, '>Autorizado\n')