from django.urls import path
from intranet.access.views import new

app_name = 'access'

urlpatterns = [
    path('new', new, name='new'),
]
