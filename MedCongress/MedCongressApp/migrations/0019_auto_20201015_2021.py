# Generated by Django 2.2.3 on 2020-10-16 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0018_auto_20201015_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relcongresouser',
            options={'verbose_name': 'relacion congreso - usuario', 'verbose_name_plural': 'relaciones congreso - usuarios'},
        ),
        migrations.AlterUniqueTogether(
            name='relcongresouser',
            unique_together=set(),
        ),
    ]