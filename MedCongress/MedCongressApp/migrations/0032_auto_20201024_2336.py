# Generated by Django 2.2.3 on 2020-10-25 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0031_bloque_modelador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponencia',
            name='bloque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Bloque'),
        ),
        migrations.AlterField(
            model_name='taller',
            name='bloque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Bloque'),
        ),
    ]
