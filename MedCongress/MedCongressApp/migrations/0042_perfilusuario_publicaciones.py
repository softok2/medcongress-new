# Generated by Django 2.2.3 on 2020-11-12 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0041_auto_20201111_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='publicaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
