# Generated by Django 2.2.3 on 2020-10-10 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0010_auto_20201009_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='is_ponente',
            field=models.BooleanField(default=False),
        ),
    ]
