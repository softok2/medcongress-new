# Generated by Django 2.2.3 on 2020-11-12 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0042_perfilusuario_publicaciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='puesto',
            field=models.CharField(max_length=100, null=True),
        ),
    ]