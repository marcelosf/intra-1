from django import forms
from django.core.exceptions import ValidationError
from intranet.access import validators
from intranet.access.forms.form_choices import DOCS, ANSWERABLE, STATUS, ACTIONS_CHOICES, WEEKDAYS_CHOICES
from intranet.access.models import Access


class AccessForm(forms.Form):
    enable = forms.BooleanField(label='Ativar', required=False)
    status = forms.ChoiceField(label='status', choices=STATUS)
    period_to = forms.DateField(label='Data de término', widget=forms.TextInput(attrs={'type': 'date'}))
    period_from = forms.DateField(label='Data de início', widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    weekdays = forms.MultipleChoiceField(label='Dias da semana', choices=WEEKDAYS_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    time_to = forms.TimeField(label='Horário de término', widget=forms.TimeInput(attrs={'type': 'time'}))
    time_from = forms.TimeField(label='Horário de início', widget=forms.TimeInput(attrs={'type': 'time'}))
    institution = forms.CharField(label='Instituição/Empresa')
    name = forms.CharField(label='Nome')
    job = forms.CharField(label='Cargo')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone', validators=[validators.validate_phone])
    doc_type = forms.ChoiceField(label='Documento', choices=DOCS)
    doc_number = forms.CharField(label='Número do documento')
    answerable = forms.ChoiceField(label='Responsável', choices=ANSWERABLE)
    observation = forms.CharField(label='Observação', widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))

    def clean(self):
        cleaned_data = super().clean()
        validators.validate_period(cleaned_data.get('period_from'), cleaned_data.get('period_to'))
        validators.validate_doc_number(self, cleaned_data.get('doc_type'), cleaned_data.get('doc_number'))
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

    def clean_job(self):
        job = self.cleaned_data['job']
        words = [w.capitalize() for w in job.split()]
        return ' '.join(words)


def actions_formset(queryset):
    class _ActionsForm(forms.Form):
        access = forms.ModelMultipleChoiceField(queryset=queryset, widget=forms.CheckboxSelectMultiple)
        enable = forms.BooleanField(label='Ativo', required=False)
        period_from = forms.DateField(label='Data de início', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
        period_to = forms.DateField(label='Data de término', widget=forms.TextInput(attrs={'type': 'date'}), required=False)
        time_from = forms.TimeField(label='Hora de início', widget=forms.TimeInput(), required=False)
        time_to = forms.TimeField(label='Hora de término', widget=forms.TimeInput(), required=False)
        observation = forms.CharField(label='Observação', widget=forms.Textarea(), required=False)

        def clean(self):
            cleaned_data = super().clean()
            validators.validate_period(cleaned_data.get('period_from'), cleaned_data.get('period_to'))
            return self.cleaned_data

    return _ActionsForm


class AlunoSearchForm(forms.Form):
    name = forms.CharField(label='nome', required=False, widget=forms.TextInput(attrs={'id': 'id_search_name'}))