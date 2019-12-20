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
            'period_to': '2019-12-20',
            'period_from': '2019-12-12',
            'time_to': '13:13',
            'time_from': '20:20',
            'institution': 'IAG',
            'name': 'Marcelo',
            'job': 'Analista',
            'email': 'marcelo@test.com',
            'phone': '11912345678',
            'doc_type': 'RG',
            'doc_number': '111111111',
            'answerable': 'Pessoa1',
            'observation': 'Observações',
            'status': 'Para autorização',
        }

    def test_period_validation(self):
       form = self.make_form(period_from='2019-12-20', period_to='2019-12-12')
       errors = form.errors.as_data()
       self.assertListEqual(['__all__'], list(errors))

    def test_name_must_be_captalized(self):
        """Name must be captalized"""
        form = self.make_form(name='mArc FROLDER')
        data = form.cleaned_data
        self.assertEqual('Marc Frolder', data['name'])

    def test_job_must_be_captalized(self):
        """Job must be captalized"""
        form = self.make_form(job='ANALISTA')
        data = form.cleaned_data
        self.assertEqual('Analista', data['job'])

    def test_phone_must_contain_only_numbers(self):
        """Phone must contain only numbers"""
        form = self.make_form(phone='abcd12345')
        self.assertFormCode(form, 'phone', 'digits')

    def test_phone_length(self):
        """Phone must be smaller or equal than 11 digits"""
        form = self.make_form(phone='111111111111')
        self.assertFormCode(form, 'phone', 'length')

    def test_rg_length(self):
        """Rg must have 9 digits"""
        form = self.make_form(doc_number='222', doc_type='RG')
        self.assertFormCode(form, 'doc_number', 'length')

    def test_invalid_cpf_number(self):
        """CPF number must be a valid cpf"""
        form = self.make_form(doc_type='CPF', doc_number='22222222222')
        self.assertFormCode(form, 'doc_number', 'cpf')

    def test_valid_cpf_number(self):
        """CPF number must be valid"""
        form = self.make_form(doc_type='CPF', doc_number='46792039004')
        self.assertIn('doc_number', form.cleaned_data)

    def assertFormMessage(self, form, field, msg):
        errors = form.errors.as_data()
        error_list = errors[field]
        exception = error_list[0]
        self.assertEqual(msg, exception)

    def assertFormCode(self, form, field, code):
        errors = form.errors.as_data()
        error_list = errors[field]
        exception = error_list[0]
        self.assertEqual(code, exception.code)

    def make_form(self, **kwargs):
        data = dict(self.data, **kwargs)
        form = AccessForm(data)
        form.is_valid()

        return form


