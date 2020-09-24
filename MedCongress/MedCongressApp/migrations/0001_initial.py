# Generated by Django 2.2.3 on 2020-09-22 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvalCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
                ('logo', models.ImageField(upload_to='img')),
            ],
            options={
                'verbose_name': 'aval del congreso',
                'verbose_name_plural': 'avales de los congresos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaPagoCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'categoria de pago del congreso',
                'verbose_name_plural': 'categorias de pago de los congresos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'categoria del usuario',
                'verbose_name_plural': 'categorias del usuario',
            },
        ),
        migrations.CreateModel(
            name='Congreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('imagen', models.ImageField(upload_to='img')),
                ('detalle', models.CharField(max_length=250)),
                ('precio', models.IntegerField()),
                ('lugar', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(null=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('published', models.BooleanField()),
            ],
            options={
                'verbose_name': 'congreso',
                'verbose_name_plural': 'congresos',
            },
        ),
        migrations.CreateModel(
            name='EspecialidadCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'especialidad del congreso',
                'verbose_name_plural': 'especialidades de los congresos',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacion', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'genero',
                'verbose_name_plural': 'generos',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominacion', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'pais',
                'verbose_name_plural': 'paises',
            },
        ),
        migrations.CreateModel(
            name='TipoCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'tipo de congreso',
                'verbose_name_plural': 'tipos de congresos',
            },
        ),
        migrations.CreateModel(
            name='RelCongresoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RelCongresoCategoriaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.CategoriaPagoCongreso')),
            ],
        ),
        migrations.CreateModel(
            name='RelCongresoAval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('aval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.AvalCongreso')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
            ],
            
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('puntuacion', models.IntegerField()),
                ('ponente', models.BooleanField()),
                ('cel_profecional', models.CharField(max_length=50)),
                ('foto', models.ImageField(upload_to='img')),
                ('activation_key', models.CharField(blank=True, max_length=40, null=True)),
                ('key_expires', models.DateTimeField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.CategoriaUsuario')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Genero')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Pais')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='congreso',
            name='aval',
            field=models.ManyToManyField(through='MedCongressApp.RelCongresoAval', to='MedCongressApp.AvalCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='categoria_pago',
            field=models.ManyToManyField(through='MedCongressApp.RelCongresoCategoriaPago', to='MedCongressApp.CategoriaPagoCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='t_congreo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.TipoCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='user',
            field=models.ManyToManyField(through='MedCongressApp.RelCongresoUser', to=settings.AUTH_USER_MODEL),
        ),
       
    ]
