from django.conf import settings
import json
import requests
from urllib.parse import urljoin


def get_alunos(query=None):
    url_base = settings.ALUNOS_RESOURCES
    if not query:
        resp = requests.get(url=url_base)
        return resp
    url_query = ''
    for qs in query.keys():
        url_query = '/'.join([url_query, qs, query[qs]])
    url = urljoin(base=url_base, url=url_query)
    resp = requests.get(url=url)
    return resp