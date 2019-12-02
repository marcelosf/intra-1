from django import forms
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

