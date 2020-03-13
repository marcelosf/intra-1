from django.urls import path
from intranet.access.views import new, detail, access_list, access_edit, authorization_list

app_name = 'access'

urlpatterns = [
    path('', access_list, name='access_list'),
    path('new', new, name='new'),
    path('detail/<slug:slug>/', detail, name='access_detail'),
    path('edit/<slug:slug>/', access_edit, name='access_edit'),
    path('auth-list/', authorization_list, name='authorization_list')
]
