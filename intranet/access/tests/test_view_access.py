
from django.test import TestCase
from intranet.accounts.models import User
from intranet.access.forms.forms import AccessForm
from intranet.access.models import Access
from django.shortcuts import resolve_url as r


class TestAccessNewLoggedInGet(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.resp = self.client.get(r('access:new'))

    def test_url(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must render new template"""
        self.assertTemplateUsed(self.resp, 'access/access_form.html')

    def test_html(self):
        """Must contain form html tags"""
        tags = (
            ('<form', 1),
            ('type="date"', 2),
            ('type="time"', 2),
            ('type="text"', 5),
            ('type="email"', 1),
            ('<select', 2),
            ('<textarea', 1),
            ('type="checkbox"', 1),
            ('type="submit"', 1),
        )

        for item, count in tags:
            with self.subTest():
                self.assertContains(self.resp, item, count)

    def test_scrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """html must have access form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, AccessForm)


class TestAccessNewAnonymousGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('access:new'))

    def test_anonimous_redirect_to_login_page(self):
        """User must be redirect to login page"""
        self.assertEqual(302, self.resp.status_code)


class TestAccessNewPostValid(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.data = {
            'enable': True,
            'period_to': '2019-12-12',
            'period_from': '2019-12-20',
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

        self.resp = self.client.post(r('access:new'), self.data)

    def test_post(self):
        """Post response status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_save_access(self):
        """Post data must exists on database"""
        self.assertTrue(Access.objects.exists())

    def test_redirect(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_message(self):
        """Must show status message"""
        self.assertContains(self.resp, 'Solicitação enviada com sucesso.')


class TestAccessNewPostInvalid(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc','marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.resp = self.client.post(r('access:new'), {})

    def test_template(self):
        """Must render the form"""
        self.assertTemplateUsed(self.resp, 'access/access_form.html')

    def test_form_has_errors(self):
        """Form must show errors"""
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_access(self):
        self.assertFalse(Access.objects.exists())
