from django.contrib import admin
from intranet.locals.models import Locals


class LocalsAdmin(admin.ModelAdmin):
    list_display = ('build', 'floor', 'local', 'departament')
    search_fields = ('build', 'floor', 'local', 'departament')
    list_filter = ('departament', 'build', 'floor')


admin.site.register(Locals, LocalsAdmin)
admin.site.site_header = 'Intranet'
admin.site.index_title = 'Painel de Gerenciamento'
