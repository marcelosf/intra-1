DOCS = (
    ('RG', 'RG'),
    ('CPF', 'CPF'),
    ('USP', 'USP'),
    ('Passaporte', 'Passaporte'),
)

ANSWERABLE = (
    ('Pessoa1', 'Pessoa1'),
    ('Pessoa2', 'Pessoa2'),
)

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
