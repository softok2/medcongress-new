# Generated by Django 2.2.3 on 2021-02-04 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0084_auto_20210203_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='programa',
            new_name='documento',
        ),
    ]