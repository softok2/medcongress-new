# Generated by Django 2.2.3 on 2020-10-22 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0025_auto_20201022_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taller',
            name='congreso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Congreso'),
        ),
    ]