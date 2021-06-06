# Generated by Django 2.2.3 on 2021-04-30 12:31

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0102_congreso_is_home'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(error_messages={'max_length': 'El Campo <b>Título </b> debe tener máximo 250 caracteres'}, max_length=250)),
                ('detalle', models.TextField(blank=True, null=True)),
                ('cod_video', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='MedCongressApp/static/'), upload_to='salas')),
                ('congreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso')),
            ],
        ),
        migrations.AddField(
            model_name='ponencia',
            name='sala',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Sala'),
        ),
    ]
