# Generated by Django 2.2.3 on 2021-08-25 18:55

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0122_auto_20210825_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='relbloquemoderador',
            name='fecha_constancia',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='relbloquemoderador',
            name='folio_constancia',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='relbloquemoderador',
            name='foto_constancia',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='congreso/img_constancia'),
        ),
        migrations.AddField(
            model_name='relbloquemoderador',
            name='is_constancia',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='relcongresouser',
            name='folio_constancia',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='relponenciaponente',
            name='fecha_constancia',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='relponenciaponente',
            name='folio_constancia',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='relponenciaponente',
            name='foto_constancia',
            field=models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='congreso/img_constancia'),
        ),
        migrations.AddField(
            model_name='relponenciaponente',
            name='is_constancia',
            field=models.BooleanField(null=True),
        ),
    ]