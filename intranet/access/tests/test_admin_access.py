from django.test import TestCase
from intranet.access.admin import AccessAdmin, admin
from intranet.access.models import Access


class TestAdminAccess(TestCase):
    def setUp(self):
        self.obj = AccessAdmin(Access, AccessAdmin)

    def test_list_display(self):
        """Must contain all of access data"""
        expected = [
            'answerable',
            'name',
            'institution',
            'list_period_from',
            'list_period_to',
            'doc_type',
            'doc_number',
            'authorized',
        ]

        self.assertEqual(expected, list(self.obj.list_display))

    def test_search_fields(self):
        expected = ['answerable', 'name', 'period_from', 'period_to']
        self.assertEqual(expected, list(self.obj.search_fields))

    def test_list_filter(self):
        expected = ['created_at', 'period_from', 'period_to', 'answerable']
        self.assertEqual(expected, list(self.obj.list_filter))

    def test_make_authorized(self):
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
                status='Para autorização',
        )

        query_set = Access.objects.all()
        model_admin = AccessAdmin(Access, admin.site)
        model_admin.make_authorized(None, query_set)

        self.assertEqual(1, Access.objects.filter(status='Autorizado').count())

