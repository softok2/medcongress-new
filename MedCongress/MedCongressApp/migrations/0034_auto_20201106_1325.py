# Generated by Django 2.2.3 on 2020-11-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0033_auto_20201105_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relcongresouser',
            name='num_autorizacion_transaccion',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='reltalleruser',
            name='num_autorizacion_transaccion',
            field=models.CharField(max_length=20),
        ),
    ]