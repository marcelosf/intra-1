import django_filters
from intranet.access.models import Access


class AccessFilter(django_filters.FilterSet):
    class Meta:
        model = Access
        fields = ['name']