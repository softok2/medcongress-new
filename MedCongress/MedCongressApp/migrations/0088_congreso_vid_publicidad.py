# Generated by Django 2.2.3 on 2021-02-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0087_auto_20210217_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='congreso',
            name='vid_publicidad',
            field=models.TextField(blank=True, null=True),
        ),
    ]
