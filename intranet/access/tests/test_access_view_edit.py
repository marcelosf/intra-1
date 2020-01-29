from django.test import TestCase
from django.shortcuts import resolve_url as r
from intranet.access.models import Access
from intranet.accounts.models import User
from intranet.access.forms.forms import AccessForm


class AccessViewEditGETTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.client.force_login(user)
        self.obj = Access(
            enable=True,
            period_to='2019-12-12',
            period_from='2019-12-20',
            time_to='13:13',
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
        )
        self.obj.save()

        self.resp = self.client.get(r('access:access_edit', slug=self.obj.uuid))

    def test_url(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)
        
    def test_template(self):
        """It must render /access/access_edit.html"""
        self.assertTemplateUsed(self.resp, 'access/access_edit.html')

    def test_base_template(self):
        """It must extends base.html"""
        self.assertTemplateUsed(self.resp, 'base.html')
    
    def test_html(self):
        items = (
            ('<form', 1),
            ('<select', 3),
            ('type="date"', 2),
            ('type="time"', 2),
            ('type="text"', 5),
            ('type="email"', 1),
            ('type="checkbox"', 8),
            ('<textarea', 1)
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, AccessForm)

    def test_form_is_bound(self):
        form = self.resp.context['form']
        self.assertTrue(form.is_bound)

    def test_form_content(self):
        items = [
            '2019-12-12',
            '2019-12-20',
            '13:13',
            '20:20',
            'IAG',
            'Marcelo',
            'Analista',
            'marcelo@test.com',
            '11912345678',
            'RG',
            '202000002',
            'Pessoa1',
            'Observações',
            'Para autorização',
        ]

        for expected in items:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_actions_menu_exists(self):
        """Check if actions menu items exists"""
        items = (
            ('Listar', 1),
            ('Adicionar', 1),
        )

        for expected, count in items:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class AccessViewEditGETAnonimousTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.obj = Access(
            enable=True,
            period_to='2019-12-12',
            period_from='2019-12-20',
            time_to='13:13',
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
        )
        self.obj.save()
        self.resp = self.client.get(r('access:access_edit', slug=self.obj.uuid))

    def test_status_code(self):
        """Status code must be 302"""
        self.assertEqual(302, self.resp.status_code)

class AccessViewEditValidPOSTTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.client.force_login(user)
        data = self.make_data()
        access = Access.objects.create(**data)
        data_update = self.make_data(period_to='2019-12-30')
        self.resp = self.client.post(r('access:access_edit', slug=str(access.uuid)), data_update)
        self.access = Access.objects.get(uuid=access.uuid)

    def test_update(self):
        """Period To must be 2019-12-30"""
        self.assertEqual('2019-12-30', self.access.period_to.strftime('%Y-%m-%d'))

    def test_success_message(self):
        """It must show a success message"""
        expected = 'Acesso atualizado com sucesso'
        self.assertContains(self.resp, expected)

    def test_weekdays_update(self):
        """Weekdays should be updated"""
        data = self.make_data(weekdays=[0,2])
        self.client.post(r('access:access_edit', slug=str(self.access.uuid)), data)
        count = Access.objects.filter(weekdays="['0', '2']").count()
        self.assertEqual(1, count)

    def make_data(self, **kwargs):
        default_data = dict(
            enable=True,
            period_to='2019-12-20',
            period_from='2018-12-12',
            time_to='13:13',
            weekdays=[0, 1],
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
        )
        data = dict(default_data, **kwargs)
        return data

class AccessViewEditInvalidPOSTTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('Marc', 'marc@test.com', 'ktw123@777')
        self.client.force_login(user)
        access = self.create_access()
        data = self.make_data(period_from='2019-12-30', period_to='2019-12-12')
        self.resp = self.client.post(r('access:access_edit', slug=str(access.uuid)), data)
    
    def test_status_code(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_errors(self):
        """Form must has errors"""
        form = self.resp.context['form']
        self.assertGreater(len(form.errors.keys()), 0)

    def test_show_field_errors(self):
        """Form must show errors"""
        form = self.resp.context['form']
        errors = form.errors.values()

        for expected in errors:
            with self.subTest():
                self.assertContains(self.resp, expected[0])

    def test_show_no_field_errors(self):
        """It must show non field errors"""
        expected = 'Alguns campos não foram preenchidos corretamente'
        self.assertContains(self.resp, expected)

    def create_access(self):
        data = self.make_data()
        obj = Access.objects.create(**data)
        return obj

    def make_data(self, **kwargs):
        default_data = dict(
            enable=True,
            period_to='2019-12-12',
            period_from='2019-12-20',
            time_to='13:13',
            time_from='20:20',
            institution='IAG',
            name='Marcelo',
            job='Analista',
            email='marcelo@test.com',
            phone='11912345678',
            doc_type='RG',
            doc_number='202000002',
            answerable='Pessoa1',
            observation='Observações',
            status='Para autorização',
        )

        data = dict(default_data, **kwargs)
        return data

