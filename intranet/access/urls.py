from django.urls import path
from intranet.access.views import new, detail

app_name = 'access'

urlpatterns = [
    path('new', new, name='new'),
    path('detail/<slug:slug>/', detail, name='access_detail')
]
