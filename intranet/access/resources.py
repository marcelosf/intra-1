from django.conf import settings
import json
import requests

def get_alunos():
    url = settings.ALUNOS_RESOURCES
    resp = requests.get(url=url)
    return resp