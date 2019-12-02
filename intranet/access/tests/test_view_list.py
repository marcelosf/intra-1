from django.test import TestCase
from intranet.access.models import Access
from intranet.access.filters import PERPAGE
from django.core.paginator import Page
from django.shortcuts import resolve_url as r
from intranet.accounts.models import User


class AccessListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
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
