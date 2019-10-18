from django.db import models


class Locals(models.Model):
    DEPARTAMENTS = (
        ('Astronomia', 'Astronomia'),
        ('Ciências Atmosféricas', 'Ciências Atmosféricas'),
        ('Geofísica', 'Geofísica'),
        ('Informática', 'Informática'),
        ('Administração', 'Administração'),
        ('Biblioteca', 'Biblioteca'),
    )

    build = models.CharField('Bloco', max_length=4)
    floor = models.CharField('Pavimento', max_length=50)
    local = models.CharField('Local', max_length=128)
    departament = models.CharField('Departamento', choices=DEPARTAMENTS, max_length=128)
    created_at = models.DateTimeField('created_at', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'locais'
        verbose_name = 'local'
