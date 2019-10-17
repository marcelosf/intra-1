from django.urls import path
from intranet.accounts.views import login, authorize

app_name = 'accounts'

urlpatterns = [
    path('login', login, name='login'),
    path('authorize', authorize, name='authorize')
]
