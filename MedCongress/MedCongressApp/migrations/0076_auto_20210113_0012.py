# Generated by Django 2.2.3 on 2021-01-13 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0075_taller_detalles_tipo_boleto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taller',
            name='detalles_tipo_boleto',
        ),
        migrations.AddField(
            model_name='congreso',
            name='detalles_tipo_boleto_taller',
            field=models.TextField(blank=True, null=True),
        ),
    ]