# Generated by Django 2.2.3 on 2021-01-13 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0076_auto_20210113_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='congreso',
            name='ver_titulo',
            field=models.BooleanField(default=True),
        ),
    ]
