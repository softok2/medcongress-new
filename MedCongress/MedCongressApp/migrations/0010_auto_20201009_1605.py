# Generated by Django 2.2.3 on 2020-10-09 20:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0009_auto_20201009_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('detalle', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'especialidad del usuario',
                'verbose_name_plural': 'especialidades del usuario',
            },
        ),
        migrations.AlterField(
            model_name='pais',
            name='denominacion',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\s]+$', 'Entre un nombre válido. Ej(México)')]),
        ),
        migrations.AlterField(
            model_name='relcongresouser',
            name='is_pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reltalleruser',
            name='is_pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='especialidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Especialidades'),
        ),
    ]
