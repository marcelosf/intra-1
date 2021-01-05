import requests
from django.conf import settings


TOKEN_URL = getattr(settings, 'RESOURCE_TOKEN_URL')
RESOURCE_ALUNOS = getattr(settings, 'RESOURCE_ALUNOS')
CLIENT = getattr(settings, 'RESOURCE_CLIENT')
SECRET = getattr(settings, 'RESOURCE_SECRET')


class Resource:
    def get_alunos(self):
        self.set_headers()
        self.get_token()
        self.get_bearer()
        resp = requests.get(RESOURCE_ALUNOS, headers=self.bearer)
        return resp.json()

    def set_headers(self):
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_token(self):
        headers = getattr(self, 'headers')
        payload = {'username': CLIENT, 'password': SECRET}
        response = requests.post(TOKEN_URL, headers=headers, data=payload)
        self.token = response.json()

    def get_bearer(self):
        token = getattr(self, 'token')
        bearer = 'Bearer {}'.format(token.get('access_token'))
        self.bearer = {'Authorization': bearer}


def request_alunos():
    resource = Resource()
    return resource.get_alunos()
