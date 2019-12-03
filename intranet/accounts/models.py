from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from intranet.accounts.managers import UserManager
from django.core.mail import send_mail
from django.conf import settings
import json


class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(_("usp number"), max_length=50, unique=True)
    name = models.CharField(_("name"), max_length=100)
    type = models.CharField(_("type"), max_length=1)
    main_email = models.EmailField(_("main email"), max_length=50)
    alternative_email = models.EmailField(_("alternative email"), max_length=50, blank=True)
    usp_email = models.EmailField(_("usp email"), max_length=50, blank=True)
    formatted_phone = models.CharField(_("phone"), max_length=50, blank=True)
    wsuserid = models.CharField(_("wsuserid"), max_length=1024)
    bond = models.TextField(_("bond"))
    is_staff = models.BooleanField(_("is staff"))
    is_active = models.BooleanField(_("is active"))
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)


    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name', 'type', 'main_email']
    ALLOWED_UNIDADES = settings.ALLOWED_UNIDADES

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        names = self.name.split()
        return names[0]

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.main_email])

    def get_phone(self):
        return self.formatted_phone

    def is_servidor(self):
        bound = self.get_bound()
        for item in bound:
            if item["tipoVinculo"] == 'SERVIDOR':
                return True

        return False

    def unidade_is_allowed(self):
        bound = self.get_bound()
        for item in bound:
            codigo_unidade = item["codigoUnidade"]
            if codigo_unidade in self.ALLOWED_UNIDADES:
                return True

        return False

    def get_bound(self):
        bound = self.bond.replace("'", '"')
        return json.loads(bound)