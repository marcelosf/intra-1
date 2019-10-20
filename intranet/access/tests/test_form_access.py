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
        self.assertEqual(fields, list(self.form.fields))
