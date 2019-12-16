from django.contrib import admin
from intranet.access.models import Access


class AccessAdmin(admin.ModelAdmin):
    search_fields = ('answerable', 'name', 'period_from', 'period_to')
    list_filter = ('created_at', 'period_from', 'period_to', 'answerable')
    date_hierarchy = 'period_from'
    list_display = (
            'answerable',
            'name',
            'institution',
            'list_period_from',
            'list_period_to',
            'doc_type',
            'doc_number',
            'authorized'
    )

    actions = ['make_authorized']

    def list_period_from(self, obj):
        return obj.period_from.strftime('%d/%m/%Y')

    def list_period_to(self, obj):
        return obj.period_to.strftime('%d/%m/%Y')

    def make_authorized(self, request, queryset):
        queryset.update(status='Autorizado')

    def authorized(self, obj):
        return obj.status == 'Autorizado'
    
    list_period_from.short_description = 'Data de início'
    list_period_to.short_description = 'Data de término'
    authorized.short_description = 'Autorizado'
    authorized.boolean = True
    make_authorized.short_description = 'Autorizar'

    list_per_page=15


admin.site.register(Access, AccessAdmin)
