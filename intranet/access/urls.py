from django.urls import path
from intranet.access.views import new, detail, report_list

app_name = 'access'

urlpatterns = [
    path('', report_list, name='access_list'),
    path('new', new, name='new'),
    path('detail/<slug:slug>/', detail, name='access_detail')
]
