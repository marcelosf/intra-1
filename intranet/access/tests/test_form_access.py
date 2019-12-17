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


class AccessFormValidationTest(TestCase):
    def setUp(self):
        self.data = {
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
            'status': 'Para autorização',
        }

    def test_period_validation(self):
       form = self.make_form()
       errors = form.errors.as_data()
       self.assertListEqual(['__all__'], list(errors))
        

    def make_form(self, **kwargs):
        data = dict(self.data, **kwargs)
        form = AccessForm(data)
        form.is_valid()

        return form


