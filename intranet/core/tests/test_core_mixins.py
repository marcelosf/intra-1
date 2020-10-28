from django.test import TestCase
from django.db.models.query import QuerySet
from intranet.core.mixins import PaginatorMixin
from intranet.access.models import Access
from intranet.access.filters import AccessFilter
from django.http import HttpRequest
from django.core.paginator import Page


class CorePaginatorMixinsDefaultsTest(TestCase):
    def setUp(self):
        self.paginator = PaginatorMixin(queryset=Access.objects.all(), filterset=AccessFilter, request=HttpRequest())

    def test_set_model(self):
        """It must set the model"""
        self.assertIsInstance(self.paginator.queryset, QuerySet)

    def test_per_page(self):
        """It must set the per_page attribute"""
        self.paginator.set_per_page(10)
        self.assertEqual(10, self.paginator.per_page)

    def test_filterset(self):
        """It must be an django_filter.FilteSet class"""
        self.assertEqual(AccessFilter, self.paginator.filterset)

    def test_request(self):
        """It must be an instance of HttpRequest"""
        self.assertIsInstance(self.paginator.request, HttpRequest)

    def test_get_queryset(self):
        self.assertIsInstance(self.paginator.get_queryset(), AccessFilter)

    def test_get_page(self):
        self.paginator.request.GET.update({'page': 7})
        page = self.paginator.get_page()
        self.assertEqual(7, page)

    def test_get_paginator(self):
        """It must return a Page instance"""
        self.paginator.set_per_page(10)
        paginator = self.paginator.get_paginator()
        self.assertIsInstance(paginator['object_list'].qs, Page)

    def test_page_list(self):
        """It must return the number of pages"""
        self.paginator.set_per_page(10)
        paginator = self.paginator.get_paginator()
        self.assertEqual([1], paginator['page_list'])

    def get_request(self):
        self.paginator.set_per_page(10)
        self.paginator.request.GET.update({'page': 7})
        paginator = self.paginator.get_paginator()
        return paginator['request'].GET.get('page')
