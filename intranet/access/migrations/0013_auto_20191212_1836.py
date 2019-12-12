# Generated by Django 3.0 on 2019-12-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0012_auto_20191119_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='status',
            field=models.CharField(blank=True, choices=[('Autorizado', 'Autorizado'), ('Para autorização', 'Para autorização'), ('Não autorizado', 'Não autorizado')], default='Para autorização', max_length=128, null=True, verbose_name='status'),
        ),
    ]
