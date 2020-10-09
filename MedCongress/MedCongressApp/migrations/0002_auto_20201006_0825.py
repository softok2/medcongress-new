# Generated by Django 2.2.3 on 2020-10-06 12:25

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosIniciales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ponentes', models.IntegerField(default=0, null=True)),
                ('ponencias', models.IntegerField(default=0, null=True)),
                ('eventos', models.IntegerField(default=0, null=True)),
                ('paises', models.IntegerField(default=0, null=True)),
                ('especialidades', models.IntegerField(default=0, null=True)),
                ('afiliados', models.IntegerField(default=0, null=True)),
                ('talleres', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='congreso',
            old_name='imagen',
            new_name='imagen_seg',
        ),
        migrations.RemoveField(
            model_name='congreso',
            name='detalle',
        ),
        migrations.RemoveField(
            model_name='congreso',
            name='precio',
        ),
        migrations.CreateModel(
            name='RelTalleresCategoriaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField()),
                ('moneda', models.CharField(max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.CategoriaPagoCongreso')),
                ('taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Taller')),
            ],
            options={
                'verbose_name': 'Relación Taller - Categoría de Pago',
                'verbose_name_plural': 'Relaciones Talleres - Categoría de Pago',
                'unique_together': {('categoria', 'taller', 'moneda')},
            },
        ),
        migrations.CreateModel(
            name='ImagenCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(height_field=100, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='congreso', width_field=100)),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Congreso')),
            ],
            options={
                'verbose_name': 'imagen de congreso',
                'verbose_name_plural': 'Imagenes de congreso',
            },
        ),
        migrations.AddField(
            model_name='taller',
            name='categoria_pago',
            field=models.ManyToManyField(related_name='talleres_cat_pago', through='MedCongressApp.RelTalleresCategoriaPago', to='MedCongressApp.CategoriaPagoCongreso'),
        ),
        migrations.CreateModel(
            name='RelTallerUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_transaccion', models.CharField(max_length=20)),
                ('num_autorizacion_transaccion', models.CharField(max_length=6)),
                ('num_tarjeta_tranzaccion', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categoria_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.CategoriaPagoCongreso')),
                ('taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Taller')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.PerfilUsuario')),
            ],
            options={
                'unique_together': {('user', 'taller')},
            },
        ),
    ]