from django.http import HttpRequest, JsonResponse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Permission
from django.shortcuts import resolve_url as r
from django.conf import settings
from intranet.accounts.models import User
from intranet.access.forms.forms import AccessForm
from intranet.access.models import Access


from . import mock
from .. import views


class TestAccessNewLoggedInGet(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@email.com', 'marcpass')
        perm = Permission.objects.get(name='Can manage access status')
        user.user_permissions.set([perm])
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
            ('<select', 3),
            ('<textarea', 1),
            ('type="checkbox"', 8),
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

    def test_actions_menu(self):
        """Check if actions menu exists"""
        items = (
            ('Listar', 1),
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class TestAccessNewAnonymousGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('access:new'))

    def test_anonimous_redirect_to_login_page(self):
        """User must be redirect to login page"""
        self.assertEqual(302, self.resp.status_code)


class TestAccessNewPostValid(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.resp = self.send_post()

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

    def test_alert_status(self):
        """It must show an alert status"""
        expected = 'alert alert-success'
        self.assertContains(self.resp, expected)

    def test_relation(self):
        expected = Access.objects.get(pk=1)
        self.assertEqual(expected.created_by.login, 'Marc')

    def test_weekdays_in_form_context(self):
        """Context should have weekdays"""
        self.send_post(weekdays=[0, 2])
        count = Access.objects.filter(weekdays="['0', '2']").count()
        self.assertEqual(1, count)

    def send_post(self, **kwargs):
        default_data = {'enable': True, 'period_to': '2019-12-20', 'period_from': '2019-12-12',
                        'time_to': '13:13', 'time_from': '20:20', 'institution': 'IAG',
                        'name': 'Marcelo', 'job': 'Analista', 'email': 'marcelo@test.com',
                        'phone': '11912345678', 'doc_type': 'RG', 'doc_number': '202000002',
                        'answerable': 'Pessoa1', 'observation': 'Observações',
                        'status': 'Para autorização'}

        data = dict(default_data, **kwargs)
        resp = self.client.post(r('access:new'), data)

        return resp


class TestAccessNewPostInvalid(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.resp = self.client.post(r('access:new'), {})

    def test_template(self):
        """Must render the form"""
        self.assertTemplateUsed(self.resp, 'access/access_form.html')

    def test_form_has_errors(self):
        """Form must show errors"""
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_show_errors(self):
        form = self.resp.context['form']
        errors = form.errors.values()

        for expected in errors:
            with self.subTest():
                self.assertContains(self.resp, expected[0])

    def test_show_error_message(self):
        expected = 'alert alert-danger'
        self.assertContains(self.resp, expected)

    def test_show_non_field_errors(self):
        """It must contain non field errors"""
        data = self.make_data(
            **{'period_from': '2019-02-10', 'period_to': '2019-01-10'})
        resp = self.make_request(data)
        self.assertContains(
            resp, 'A Data de início deve ser menor do que a Data de término')

    def test_dont_save_access(self):
        self.assertFalse(Access.objects.exists())

    def make_request(self, data):
        return self.client.post(r('access:new'), data)

    def make_data(self, **kwargs):
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


class TestAccessNewAnonimous(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('access:new'))

    def test_redirect(self):
        """Status code must be 302"""
        self.assertEqual(302, self.resp.status_code)


class TestAccessManager(TestCase):
    def test_can_see_status_field(self):
        """Status field should be present"""
        expected = 'name="status"'
        resp = self.make_request(can_manage_status=True)
        self.assertContains(resp, expected)

    def test_can_not_see_status_field(self):
        """Status field should not be present"""
        expected = 'name="status"'
        resp = self.make_request()
        self.assertNotContains(resp, expected)

    def make_request(self, can_manage_status=False):
        user = User.objects.create_user('Marc', 'marc@email.com', 'marcpass')
        if can_manage_status:
            can_manage_access_status = Permission.objects.get(
                name='Can manage access status')
            user.user_permissions.set([can_manage_access_status])
        self.client.force_login(user)
        return self.client.get(r('access:new'))


class TestGeTAccess(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = user = User.objects.create_user(
            'Marc', 'marc@email.com', 'marcpass')
        self.access = mock.make_access()

    def test_get_access(self):
        doc_type = self.access.get('doc_type')
        doc_number = self.access.get('doc_number')
        request = self.factory.post(
            '/access/get-access', {'doc_number': doc_number})
        request.user = self.user
        resp = views.get_access(request)
        access = Access.objects.get(doc_number=doc_number)
        data = {'access_slug': access.get_absolute_url()}
        expected = JsonResponse(data)
        self.assertEqual(expected.content, resp.content)


class TestGetAccessUrl(TestCase):
    def setUp(self):
        self.data = mock.make_access()
        user = user = User.objects.create_user(
            'Marc', 'marc@email.com', 'marcpass')
        self.client.force_login(user)
        self.resp = self.client.post(r('access:get_access'), data=self.data)

    def test_status_code(self):
        self.assertEqual(200, self.resp.status_code)

    def test_response(self):
        access = Access.objects.get(doc_number=self.data.get('doc_number'))
        self.assertEqual(access.get_absolute_url(), self.resp.json().get('access_slug'))

    def test_redirectto_login(self):
        self.client.logout()
        resp = self.client.post(r('access:get_access'), self.data)
        self.assertEqual(302, resp.status_code)