from django.test import TestCase
from intranet.access.forms.forms import AccessForm


class TestFormAccess(TestCase):
    def setUp(self):
        self.form = AccessForm()

    def test_form_has_fields(self):
        fields = [
            'enable',
            'period_to',
            'period_from',
            'time_to',
            'time_from',
            'institution',
            'name',
            'job',
            'email',
            'phone',
            'doc_type',
            'doc_number',
            'answerable',
            'observation',
        ]

        for expected in fields:
            with self.subTest():
                self.assertIn(expected, list(self.form.fields))

    def test_status(self):
        """Form must have status field"""
        self.assertIn('status', list(self.form.fields))