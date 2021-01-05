import json
import httpretty
import functools


from ..models import Access


def make_data(**kwargs):
    access = {
        'enable': True,
        'period_to': '2019-12-20',
        'period_from': '2019-12-12',
        'time_to': '13:13',
        'time_from': '20:20',
        'institution': 'IAG',
        'name': 'Marcelo',
        'job': 'Analista',
        'email': 'marcelo@test.com',
        'phone': '11912345678',
        'doc_type': 'RG',
        'doc_number': '202000002',
        'answerable': 'Pessoa1',
        'observation': 'Observações',
        'status': 'Para autorização',
    }

    return dict(access, **kwargs)


def make_access():
    data = make_data()
    Access.objects.create(**data)
    return data


base_url = 'http://api.iag.usp.br/'


alunos_by_tipo_vinculo = [
    {
        'byTipvin': [
            {
                "codpes": "1111111",
                "tipvinext": "Aluno de Cultura e Extensão",
                "sitatl": "A",
                "codundclg": "14",
                "nompes": "Merlyn Steves",
                "codema": "mll@gmail.com"
            }
        ]
    }
]


token_payload = {
    'access_token': '87FXExQqaF2NUL9byWcFAQchxUlvoXL', 'token_type': 'bearer'}


api_list = [
    {
        'method': 'POST',
        'uri': base_url + 'token/',
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(token_payload)
    },
    {
        'method': 'GET',
        'uri': base_url + 'localizapessoa?query{byTipvin(tipvin: "ALUNOPOS"){codpes,nompes,tipvinext,codema,sitatl}}',
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(alunos_by_tipo_vinculo)
    }
]


def register_api_uri():
    for api in api_list:
        httpretty.register_uri(
            getattr(httpretty, api.get('method')),
            headers=api.get('headers'),
            uri=api.get('uri'),
            body=api.get('body')
        )


def mock_api(fn):
    @functools.wraps(fn)
    @httpretty.activate
    def wrapper(*args, **kwargs):
        register_api_uri()
        response = fn(*args, **kwargs)
        return response
    return wrapper
