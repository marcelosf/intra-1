from django.conf import settings
import requests
import json


def get_answerables():
    resp = requests.get(settings.ANSWERABLE_RESOURCE)
    json_data = resp.json()
    data = tuple((v['name'], v['name']) for v in json_data)
    return data

replicado_is_set = getattr(settings, 'SET_REPLICADO', False)

DOCS = (
    ('RG', 'RG'),
    ('CPF', 'CPF'),
    ('USP', 'USP'),
    ('Passaporte', 'Passaporte'),
)

ANSWERABLE = (
    ('Pessoa1', 'Pessoa1'),
    ('Pessoa2', 'Pessoa2')
)

if replicado_is_set:
    ANSWERABLE = get_answerables()


ACTIONS_CHOICES = (
    ('period_from', 'Atualizar data de início'),
    ('period_to', 'Atualizar data de término'),
    ('time_from', 'Atualizar hora de início'),
    ('time_to', 'Atualizar hora de término')
)


AUTHORIZED = 'Autorizado'
WAITING = 'Para autorização'
NOT_AUTHORIZED = 'Não autorizado'


AUTHORIZED_ICON = 'check_circle'
WAITING_ICON = 'access_time'
NOT_AUTHORIZED_ICON = 'not_interested'


STATUS = (
    (AUTHORIZED, AUTHORIZED),
    (WAITING, WAITING),
    (NOT_AUTHORIZED, NOT_AUTHORIZED)
)

WEEKDAYS_CHOICES=(
    (0, 'Segunda'),
    (1, 'Terça'),
    (2, 'Quarta'),
    (3, 'Quinta'),
    (4, 'Sexta'),
    (5, 'Sábado'),
    (6, 'Domingo')
)
