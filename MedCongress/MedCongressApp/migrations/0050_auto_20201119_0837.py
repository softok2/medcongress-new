# Generated by Django 2.2.3 on 2020-11-19 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0049_relcongresouser_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relcongresouser',
            old_name='fecha',
            new_name='fecha_constancia',
        ),
    ]