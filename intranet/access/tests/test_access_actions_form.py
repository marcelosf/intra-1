from django.test import TestCase
from intranet.access.forms import forms
from intranet.access.models import Access


class ActionsFormTest(TestCase):
    def setUp(self):
        self.form = forms.actions_formset(queryset=Access.objects.all())

    def test_form_fields(self):
        fields = (
            'access',
            'period_from',
            'period_to',
            'time_from',
            'time_to',
            'observation',
            'enable'
        )

        for field in fields:
            with self.subTest():
                self.assertIn(field, list(self.form.base_fields))
