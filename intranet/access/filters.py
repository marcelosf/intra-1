import django_filters
from django_filters.widgets import BooleanWidget
from django import forms
from intranet.access.models import Access


class AccessFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome')
    period_to = django_filters.DateFilter(widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    period_from = django_filters.DateFilter(widget=forms.TextInput(attrs={'type': 'date', 'class': 'validate'}))
    enable = django_filters.BooleanFilter(label='Ativo', widget=forms.CheckboxInput())
    class Meta:
        model = Access
        fields = ['name', 'period_from', 'period_to', 'enable']