# Generated by Django 2.2.5 on 2019-11-07 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0010_access_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid'),
        ),
    ]
