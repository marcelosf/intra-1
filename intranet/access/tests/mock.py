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
