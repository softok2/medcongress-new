# Generated by Django 2.2.3 on 2020-10-25 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0029_auto_20201023_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250)),
                ('duracion', models.CharField(max_length=250)),
                ('detalle', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('path', models.CharField(help_text='campo para identificarlo por la URL', max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('published', models.BooleanField()),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
            ],
            options={
                'verbose_name': 'bloque',
                'verbose_name_plural': 'bloques',
            },
        ),
        migrations.CreateModel(
            name='Moderador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.PerfilUsuario')),
            ],
            options={
                'verbose_name': 'moderador',
                'verbose_name_plural': 'moderadores',
            },
        ),
        migrations.RemoveField(
            model_name='relponenciaponente',
            name='categoria',
        ),
        migrations.CreateModel(
            name='RelBloqueModerador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bloque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Bloque')),
                ('moderador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Moderador')),
            ],
            options={
                'verbose_name': 'Relación Maderador - Bloque',
                'verbose_name_plural': 'Relaciones moderador - bloque',
                'unique_together': {('moderador', 'bloque')},
            },
        ),
        migrations.AddField(
            model_name='bloque',
            name='moderador',
            field=models.ManyToManyField(related_name='bloque_moderador', through='MedCongressApp.RelBloqueModerador', to='MedCongressApp.Moderador'),
        ),
        migrations.AddField(
            model_name='ponencia',
            name='bloque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Bloque'),
        ),
        migrations.AddField(
            model_name='taller',
            name='bloque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Bloque'),
        ),
    ]
