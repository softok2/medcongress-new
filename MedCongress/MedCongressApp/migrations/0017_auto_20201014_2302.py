# Generated by Django 2.2.3 on 2020-10-15 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0016_auto_20201014_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congreso',
            name='lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MedCongressApp.Ubicacion'),
        ),
    ]