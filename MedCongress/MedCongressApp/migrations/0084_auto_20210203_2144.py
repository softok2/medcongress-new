# Generated by Django 2.2.3 on 2021-02-04 02:44

import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0083_auto_20210126_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='documentos')),
                ('titulo', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Documento',
            },
        ),
        migrations.AlterField(
            model_name='footer',
            name='telefono',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Entre un No. de <b>Teléfono</b> correcto. Ej. <b>(+99)999-999-999</b>', regex='^[0-9()+-]+$')]),
        ),
        migrations.AlterField(
            model_name='footer',
            name='whatsapp',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Entre un No. de <b>Whatsapp</b> correcto. Ej. <b>(+99)999-999-999</b>', regex='^[0-9()+-]+$')]),
        ),
    ]
