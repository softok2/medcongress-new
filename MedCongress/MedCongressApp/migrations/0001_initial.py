# Generated by Django 2.2.3 on 2020-09-30 17:30

from django.conf import settings
import django.core.files.storage
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
                ('detalle', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='patrocinadores')),
                ('url', models.CharField(max_length=250)),
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
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=50)),
                ('detalle', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'categoria de pago del congreso',
                'verbose_name_plural': 'categorias de pago para los congresos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('detalle', models.TextField(blank=True, null=True)),
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
                ('titulo', models.CharField(max_length=250)),
                ('imagen', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='congreso')),
                ('detalle', models.TextField(blank=True, null=True)),
                ('precio', models.IntegerField()),
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=50)),
                ('lugar', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
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
                ('detalle', models.TextField(blank=True, null=True)),
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
                ('denominacion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'pais',
                'verbose_name_plural': 'paises',
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('is_ponente', models.BooleanField()),
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=50)),
                ('cel_profecional', models.CharField(max_length=50)),
                ('foto', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='usuarios')),
                ('activation_key', models.CharField(blank=True, max_length=40, null=True)),
                ('key_expires', models.DateTimeField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.CategoriaUsuario')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Genero')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Pais')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil usuario',
                'verbose_name_plural': 'Perfil de usuarios',
            },
        ),
        migrations.CreateModel(
            name='Ponencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250)),
                ('duracion', models.CharField(max_length=250)),
                ('detalle', models.TextField(blank=True, null=True)),
                ('cod_video', models.CharField(max_length=10)),
                ('imagen', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='ponencias')),
                ('fecha_inicio', models.DateTimeField()),
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=50)),
                ('lugar', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('published', models.BooleanField()),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Congreso')),
            ],
            options={
                'verbose_name': 'ponencia',
                'verbose_name_plural': 'ponencias',
            },
        ),
        migrations.CreateModel(
            name='Ponente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.PerfilUsuario')),
            ],
            options={
                'verbose_name': 'ponente',
                'verbose_name_plural': 'ponentes',
            },
        ),
        migrations.CreateModel(
            name='RelTallerPonente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ponente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Ponente')),
            ],
            options={
                'verbose_name': 'Relación Ponente- Taller',
                'verbose_name_plural': 'Relaciones Ponente - Taller',
            },
        ),
        migrations.CreateModel(
            name='RelTallerVotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votacion', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'votación taller - usuario',
                'verbose_name_plural': 'votaciones taller - usuario',
            },
        ),
        migrations.CreateModel(
            name='TipoCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('detalle', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'tipo de congreso',
                'verbose_name_plural': 'tipos de congresos',
            },
        ),
        migrations.CreateModel(
            name='Taller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250)),
                ('duracion', models.CharField(max_length=250)),
                ('precio', models.IntegerField()),
                ('fecha_inicio', models.DateTimeField()),
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=50)),
                ('imagen', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='talleres')),
                ('lugar', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('published', models.BooleanField()),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Congreso')),
                ('ponente', models.ManyToManyField(through='MedCongressApp.RelTallerPonente', to='MedCongressApp.Ponente')),
                ('votacion', models.ManyToManyField(through='MedCongressApp.RelTallerVotacion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'taller',
                'verbose_name_plural': 'talleres',
            },
        ),
        migrations.AddField(
            model_name='reltallervotacion',
            name='taller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Taller'),
        ),
        migrations.AddField(
            model_name='reltallervotacion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reltallerponente',
            name='taller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Taller'),
        ),
        migrations.CreateModel(
            name='RelPonenciaVotacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votacion', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ponencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Ponencia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'votación ponencia - usuario',
                'verbose_name_plural': 'votaciones ponencia - usuario',
                'unique_together': {('user', 'ponencia')},
            },
        ),
        migrations.CreateModel(
            name='RelPonenciaPonente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ponencia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Ponencia')),
                ('ponente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Ponente')),
            ],
            options={
                'verbose_name': 'Relación Ponente- Ponencia',
                'verbose_name_plural': 'Relaciones Ponente - Ponencia',
                'unique_together': {('ponencia', 'ponente')},
            },
        ),
        migrations.CreateModel(
            name='RelCongresoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_transaccion', models.CharField(max_length=20)),
                ('num_autorizacion_transaccion', models.CharField(max_length=6)),
                ('num_tarjeta_tranzaccion', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categoria_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.CategoriaPagoCongreso')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.PerfilUsuario')),
            ],
            options={
                'unique_together': {('user', 'congreso')},
            },
        ),
        migrations.CreateModel(
            name='RelCongresoCategoriaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField()),
                ('moneda', models.CharField(max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.CategoriaPagoCongreso')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
            ],
            options={
                'verbose_name': 'Relación Congreso - Categoría de Pago',
                'verbose_name_plural': 'Relaciones Congreso - Categoría de Pago',
                'unique_together': {('categoria', 'congreso', 'moneda')},
            },
        ),
        migrations.CreateModel(
            name='RelCongresoAval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('aval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.AvalCongreso')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
            ],
            options={
                'verbose_name': 'relacion congreso - aval',
                'verbose_name_plural': 'relaciones congreso - aval',
                'unique_together': {('aval', 'congreso')},
            },
        ),
        migrations.AddField(
            model_name='ponencia',
            name='ponente',
            field=models.ManyToManyField(related_name='ponencia_ponente', through='MedCongressApp.RelPonenciaPonente', to='MedCongressApp.Ponente'),
        ),
        migrations.AddField(
            model_name='ponencia',
            name='votacion',
            field=models.ManyToManyField(through='MedCongressApp.RelPonenciaVotacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='congreso',
            name='aval',
            field=models.ManyToManyField(related_name='congreso_patrosinador', through='MedCongressApp.RelCongresoAval', to='MedCongressApp.AvalCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='categoria_pago',
            field=models.ManyToManyField(related_name='congreso_cat_pago', through='MedCongressApp.RelCongresoCategoriaPago', to='MedCongressApp.CategoriaPagoCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='especialidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.EspecialidadCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='t_congreso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.TipoCongreso'),
        ),
        migrations.AddField(
            model_name='congreso',
            name='user',
            field=models.ManyToManyField(related_name='congreso_perfilusuario', through='MedCongressApp.RelCongresoUser', to='MedCongressApp.PerfilUsuario'),
        ),
        migrations.AlterUniqueTogether(
            name='reltallervotacion',
            unique_together={('user', 'taller')},
        ),
        migrations.AlterUniqueTogether(
            name='reltallerponente',
            unique_together={('ponente', 'taller')},
        ),
    ]
