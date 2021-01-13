import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import mail
from django.core.paginator import Paginator
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from intranet.access.forms.forms import AccessForm, actions_formset, AlunoSearchForm
from intranet.access.forms import form_choices
from intranet.access.models import Access
from intranet.access.filters import AccessFilter, PERPAGE
from django_filters.views import FilterView
from intranet.core.mixins import PaginatorMixin
from intranet.access import resources
from intranet.access.api_resources import request_alunos, request_by_name
from django.http import JsonResponse


@login_required(login_url=settings.LOGIN_URL)
def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def create(request):
    form = AccessForm(request.POST)
    if not form.is_valid():
        messages.error(
            request, 'Alguns campos não foram preenchidos corretamente.')
        return render(request, 'access/access_form.html', {'form': form})

    access = Access.objects.create(**form.cleaned_data)
    request.user.access_set.add(access)

    _send_email({'access': access})
    messages.success(request, 'Solicitação enviada com sucesso.')

    return empty_form(request)


@login_required(login_url=settings.LOGIN_URL)
def access_edit(request, slug):
    if request.method == 'POST':
        return _access_update(request, slug)
    access = Access.objects.filter(uuid=slug).values()
    obj = Access.objects.get(uuid=slug)
    data = dict(access[0], **{'weekdays': obj.get_weekdays()})
    form = AccessForm(data)
    return render(request, 'access/access_edit.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
def detail(request, slug):
    access = Access.objects.get(uuid=slug)
    context = {'access': access}
    return render(request, 'access/access_detail.html', context)


@login_required(login_url=settings.LOGIN_URL)
def access_list(request):
    actions_form = actions_formset(queryset=Access.objects.all())
    if request.method == 'POST':
        is_valid, form = _bulk_actions(request, actions_form)
        if not is_valid:
            actions_form = form
    queryset = _select_queryset(request)
    paginator = PaginatorMixin(
        queryset=queryset, filterset=AccessFilter, request=request)
    paginator.set_per_page(PERPAGE)
    pages = paginator.get_paginator()
    context = {'list': pages['object_list'],
               'page_list': pages['page_list'], 'actions_form': actions_form}
    return render(pages['request'], 'access/access_list.html', context)


@login_required(login_url=settings.LOGIN_URL)
def get_access(request):
    data = json.load(request)
    doc_number = data.get('doc_number')
    access = Access.objects.filter(doc_number=doc_number).first()
    if not access:
        return JsonResponse({'access_slug': None})
    data = {'access_slug': access.get_absolute_url()}
    return JsonResponse(data)


def authorization_list(request):
    if request.method == 'POST':
        form = AlunoSearchForm(request.POST)
        if form.is_valid():
            auth_list = request_by_name(form.cleaned_data['name'])
            context = {
                'auth_list': auth_list[0]['byNompes'],
                'form': AlunoSearchForm(),
                'access_form': AccessForm()
            }
            return render(request, 'access/authorization_list.html', context)
    context = {'form': AlunoSearchForm(), 'access_form': AccessForm()}
    return render(request, 'access/authorization_list.html', context)


def _bulk_actions(request, actions_form):
    form = actions_form(request.POST)
    if not form.is_valid():
        return (False, form)
    access = form.cleaned_data['access']
    data = form.cleaned_data
    data = dict((k, v) for k, v in data.items() if v != None)
    del data['access']
    data['status'] = form_choices.WAITING
    access.update(**data)
    keys = list(data.keys())
    Access.objects.bulk_update(access, keys, batch_size=30)
    return (True, form)


def _access_update(request, slug):
    form = AccessForm(request.POST)
    if not form.is_valid():
        messages.error(
            request, 'Alguns campos não foram preenchidos corretamente')
        return render(request, 'access/access_edit.html', {'form': form})

    access = Access.objects.get(uuid=slug)
    access.period_from = form.cleaned_data['period_from']
    access.period_to = form.cleaned_data['period_to']
    access.time_from = form.cleaned_data['time_from']
    access.weekdays = form.cleaned_data['weekdays']
    access.time_to = form.cleaned_data['time_to']
    access.status = form.cleaned_data['status']
    access.enable = form.cleaned_data['enable']

    access.save()
    messages.success(request, message='Acesso atualizado com sucesso')
    return render(request, 'access/access_edit.html', {'form': form})


def _select_queryset(request):
    in_group = request.user.groups.filter(
        name=settings.PORTARIA_GROUP_NAME).exists()
    if in_group:
        return Access.objects.filter(status=form_choices.AUTHORIZED)
    return Access.objects.all()


def empty_form(request):
    return render(request, 'access/access_form.html', {'form': AccessForm()})


def _send_email(context):
    subject = '[IAG-INTRANET] Solicitação de acesso'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = 'intranet@mailinator.com'
    body = render_to_string('email/new_access.txt', context)
    mail.send_mail(subject, body, from_email, [to_email])
