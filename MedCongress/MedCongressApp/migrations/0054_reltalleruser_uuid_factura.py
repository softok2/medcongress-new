# Generated by Django 2.2.3 on 2020-11-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0053_relcongresouser_uuid_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='reltalleruser',
            name='uuid_factura',
            field=models.CharField(max_length=36, null=True),
        ),
    ]