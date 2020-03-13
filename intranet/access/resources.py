from django.conf import settings
import json
import requests
from urllib.parse import urljoin


GET_ALUNOS_RESOURCE = settings.GET_ALUNOS_RESOURCE

def get_alunos(query=None):
    url_base = settings.ALUNOS_RESOURCES
    if not query:
        resp = requests.get(url=url_base)
        return resp
    url_query = ''
    search_keys = dict(GET_ALUNOS_RESOURCE, **query)
    for qs in search_keys.keys():
        if search_keys[qs]:
            url_query = '/'.join([url_query, qs, search_keys[qs]])
    url = urljoin(base=url_base, url=url_query)
    resp = requests.get(url=url)
    return resp