# Generated by Django 2.2.3 on 2020-10-06 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0005_auto_20201006_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='id_openpay',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
