from django.test import TestCase
from intranet.access.filters import AccessFilter


class AccessFiltersTest(TestCase):
    def test_fields(self):
        fields = ['name', 'period_from', 'period_to', 'enable']
        filter_fields = AccessFilter.Meta.fields

        for expected in fields:
            with self.subTest():
                self.assertIn(expected, filter_fields)