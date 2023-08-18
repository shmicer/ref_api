# Generated by Django 4.2.4 on 2023-08-18 08:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_invited_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='invited_by',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, to_field='phone_number'),
        ),
    ]
