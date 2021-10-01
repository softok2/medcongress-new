# Generated by Django 2.2.3 on 2021-08-26 16:57

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MedCongressApp', '0123_auto_20210825_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relbloquemoderador',
            name='fecha_constancia',
        ),
        migrations.RemoveField(
            model_name='relbloquemoderador',
            name='folio_constancia',
        ),
        migrations.RemoveField(
            model_name='relbloquemoderador',
            name='foto_constancia',
        ),
        migrations.RemoveField(
            model_name='relbloquemoderador',
            name='is_constancia',
        ),
        migrations.RemoveField(
            model_name='relponenciaponente',
            name='fecha_constancia',
        ),
        migrations.RemoveField(
            model_name='relponenciaponente',
            name='folio_constancia',
        ),
        migrations.RemoveField(
            model_name='relponenciaponente',
            name='foto_constancia',
        ),
        migrations.RemoveField(
            model_name='relponenciaponente',
            name='is_constancia',
        ),
        migrations.CreateModel(
            name='ConstanciaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio_constancia', models.CharField(max_length=250, null=True)),
                ('fecha_constancia', models.DateField(null=True)),
                ('tipo_constancia', models.CharField(max_length=50, null=True)),
                ('foto_constancia', models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='congreso/img_constancia')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'constancia - usuario',
                'unique_together': {('user', 'congreso', 'tipo_constancia')},
            },
        ),
    ]