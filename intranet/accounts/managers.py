from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, login, name, type, main_email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not login:
            raise ValueError(_('The login must be set.'))
        if not name:
            raise ValueError(_('The name must be set.'))
        if not type:
            raise ValueError(_('The type must be set'))

        main_email = self.normalize_email(main_email)
        user = self.model(login=login, name=name, type=type, main_email=main_email, is_staff=is_staff, is_active=True, 
                is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_user(self, login, name, type, main_email=None, password=None, **extra_fields):
        return self._create_user(login, name, type, main_email, password, False, False, **extra_fields)


    def create_superuser(self, login, name, type, main_email, password, **extra_fields):
        user=self._create_user(login, name, type, main_email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user 