from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render, resolve_url as r
from django.http import HttpResponse
from intranet.accounts.models import User
import json


def login(request):
    if(request.user.is_authenticated):
        return redirect(r('accounts:user'))
    request.session['next'] = request.GET['next']
    usp = get_client()
    redirect_uri = request.build_absolute_uri(r('accounts:authorize'))
    return usp.authorize_redirect(request, redirect_uri)

def authorize(request):
    usp = get_client()
    token = usp.authorize_access_token(request)
    resp = usp.post('/wsusuario/oauth/usuariousp', token=token)
    profile = resp.json()
    data = data_transform(profile, mapper())
    user = persist_user(data)
    log_user_in(request, user)
    path = path_redirect(request)
    return redirect(path)

def logout_view(request):
    logout(request)
    return HttpResponse()

def user(request):
    user = request.user
    return render(request, 'user.html', {'user': user})

def get_client():
    client = getattr(settings, 'USP_CLIENT', None)
    return client.usp

def data_transform(data, mapped):
    transformed = dict()
    for key in mapped:
        if key in data:
            transformed.update({mapped[key]: str(data[key])})
    
    return transformed

def persist_user(data):
    user = User.objects.filter(login=data['login']).first()
    if not user:
        user = User.objects.create_user(**data)
    
    return user

def log_user_in(request, user):
    auth_login(request=request, user=user)
    return request

def mapper():
    return {
        'loginUsuario': 'login',
        'nomeUsuario': 'name',
        'tipoUsuario': 'type',
        'emailPrincipalUsuario': 'main_email',
        'emailAlternativoUsuario': 'alternative_email',
        'emailUspUsuario': 'usp_email',
        'numeroTelefoneFormatado': 'formatted_phone',
        'wsuserid': 'wsuserid',
        'vinculo': 'bond'
    }

def path_redirect(request):
    if (request.session['next']):
        return request.session['next']
    return r('accounts:user')