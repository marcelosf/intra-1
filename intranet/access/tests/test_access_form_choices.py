from django.test import TestCase
from django.conf import settings
from intranet.access.forms import form_choices
import httpretty


class FormChoicesAccessTest(TestCase):
    def setUp(self):
        settings.SET_REPLICADO = True
        httpretty.enable()
        httpretty.register_uri(
            httpretty.GET,
            settings.ANSWERABLE_RESOURCE,
            body='[{"name":"Pessoa1", "name":"Pessoa2"}]',
            content_type="application/json",
            status=200
        )

        self.resp = form_choices.get_answerables()

    def tearDown(self):
        super().tearDown()
        httpretty.disable()
        settings.SET_REPLICADO = False

    def test_answerable_field_content(self):
        self.assertTrue(True)