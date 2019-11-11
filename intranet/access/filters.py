import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from intranet.access.models import Access
from intranet.access.forms.form_choices import STATUS


class AccessFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    period_to = django_filters.DateFilter(widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    period_from = django_filters.DateFilter(widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    status = django_filters.ChoiceFilter(label='status', choices=STATUS)
    class Meta:
        model = Access
        fields = ['name', 'period_from', 'period_to', 'status']