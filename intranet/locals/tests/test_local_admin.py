from django.test import TestCase

from intranet.locals.admin import LocalsAdmin
from intranet.locals.models import Locals


class TestLocalAdmin(TestCase):
    def setUp(self):
        self.obj = LocalsAdmin(Locals, LocalsAdmin)

    def test_list_display(self):
        """Admin must contain build, floor, and local list_display"""
        expected = ['build', 'floor', 'local', 'departament']
        self.assertEquals(expected, list(self.obj.list_display))

    def test_search_list(self):
        """Search list must contain build, floor and local"""
        expected = ['build', 'floor', 'local', 'departament']
        self.assertEqual(expected, list(self.obj.search_fields))

    def test_list_filter(self):
        """List filter must contain build an floor"""
        expected = ['departament', 'build', 'floor']
        self.assertEquals(expected, list(self.obj.list_filter))
