import uuid
import ast
from datetime import datetime

from django.db import models
from django.shortcuts import resolve_url as r
from django.utils.translation import ugettext as _

from intranet.access.forms import form_choices
from intranet.accounts.models import User

WEEKDAYS={'0': 'Segunda', '1': 'Terça', '2': 'Quarta', '3': 'Quinta',
            '4': 'Sexta', '5': 'Sábado', '6': 'Domingo'}

class Access(models.Model):
    DOCS = form_choices.DOCS
    ANSWERABLE = form_choices.ANSWERABLE
    STATUS = form_choices.STATUS

    uuid = models.UUIDField('uuid', default=uuid.uuid4, editable=False, unique=True)
    enable = models.BooleanField('ativar', default=False)
    period_to = models.DateField('data de término')
    period_from = models.DateField('data de início')
    weekdays = models.CharField('dia da semana', max_length=20, null=True, choices=form_choices.WEEKDAYS_CHOICES)
    time_to = models.TimeField('hora de termino')
    time_from = models.TimeField('hora de início')
    institution = models.CharField('instituição', max_length=128)
    name = models.CharField('nome', max_length=128)
    job = models.CharField('cargo', max_length=128)
    email = models.EmailField('email')
    phone = models.CharField('telefone', max_length=20)
    doc_type = models.CharField('tipo documento', choices=DOCS, max_length=128)
    doc_number = models.CharField('numero do documento', max_length=128)
    answerable = models.CharField('responsável', choices=ANSWERABLE, max_length=128)
    observation = models.CharField('observação', max_length=1024)
    status = models.CharField('status', choices=STATUS, max_length=128, default='Para autorização', null=True, blank=True)
    created_at = models.DateTimeField('data de criação', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return r('access:access_detail', slug=self.uuid)

    def get_week_name(self):
        weekdays = []
        if self.weekdays != None:
            for item in self.weekdays:
                if item in WEEKDAYS.keys():
                    weekdays.append(WEEKDAYS[item])
        return weekdays

    def get_weekdays(self):
        if self.weekdays:
            return ast.literal_eval(self.weekdays)
        return None

    class Meta:
        verbose_name_plural = 'acessos'
        verbose_name = 'acesso'
        ordering = ('-created_at',)
