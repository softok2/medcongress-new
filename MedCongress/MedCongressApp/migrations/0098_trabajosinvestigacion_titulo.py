# Generated by Django 2.2.3 on 2021-03-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0097_auto_20210303_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajosinvestigacion',
            name='titulo',
            field=models.CharField(error_messages={'max_length': 'El Campo <b>Título</b> debe tener máximo 250 caracteres'}, max_length=250, null=True),
        ),
    ]
