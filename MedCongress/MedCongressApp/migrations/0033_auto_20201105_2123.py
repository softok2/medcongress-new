# Generated by Django 2.2.3 on 2020-11-06 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0032_auto_20201105_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='relcongresouser',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='reltalleruser',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
    ]
