# Generated by Django 2.2.3 on 2020-11-07 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0035_congreso_datos_interes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='congreso',
            name='datos_interes',
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='datos_interes',
            field=models.TextField(null=True),
        ),
    ]
