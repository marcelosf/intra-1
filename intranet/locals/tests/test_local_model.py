from django.test import TestCase
from intranet.locals.models import Locals


class TestLocalModel(TestCase):
    def setUp(self):
        self.obj = Locals(
            build='P',
            floor='Terreo',
            local='108',
            departament='Astronomia'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Locals.objects.exists())
