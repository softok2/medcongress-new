# Generated by Django 2.2.3 on 2020-10-06 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0006_perfilusuario_id_openpay'),
    ]

    operations = [
        migrations.AddField(
            model_name='relcongresouser',
            name='is_pagado',
            field=models.BooleanField(default=True),
        ),
    ]
