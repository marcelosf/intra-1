from django import forms
from django.core.exceptions import ValidationError
from intranet.access.forms.form_choices import DOCS, ANSWERABLE, STATUS


class AccessForm(forms.Form):

    enable = forms.BooleanField(label='Ativar', required=False)
    status = forms.ChoiceField(label='status', choices=STATUS)
    period_to = forms.DateField(label='Data de término', widget=forms.TextInput(attrs={'type': 'date'}))
    period_from = forms.DateField(label='Data de início', widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    time_to = forms.TimeField(label='Horário de término', widget=forms.TimeInput(attrs={'type': 'time'}))
    time_from = forms.TimeField(label='Horário de início', widget=forms.TimeInput(attrs={'type': 'time'}))
    institution = forms.CharField(label='Instituição/Empresa')
    name = forms.CharField(label='Nome')
    job = forms.CharField(label='Cargo')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')
    doc_type = forms.ChoiceField(label='Documento', choices=DOCS)
    doc_number = forms.CharField(label='Número do documento')
    answerable = forms.ChoiceField(label='Responsável', choices=ANSWERABLE)
    observation = forms.CharField(label='Observação', widget=forms.Textarea(attrs={'class': 'materialize-textarea'}))

    def clean(self):
        period_to = self.cleaned_data.get('period_to')
        period_from = self.cleaned_data.get('period_from')

        if (period_from and period_to) and (period_from > period_to):
            raise ValidationError('A Data de início deve ser menor do que a Data de término')
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

