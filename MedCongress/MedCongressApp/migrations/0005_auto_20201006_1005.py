# Generated by Django 2.2.3 on 2020-10-06 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0004_auto_20201006_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ponente',
            name='categoria',
        ),
        migrations.AddField(
            model_name='relponenciaponente',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.CategoriaPonente'),
        ),
    ]
