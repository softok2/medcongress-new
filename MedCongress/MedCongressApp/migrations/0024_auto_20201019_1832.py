# Generated by Django 2.2.3 on 2020-10-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0023_auto_20201018_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriapagocongreso',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='categoriaponente',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='congreso',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='ponencia',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='taller',
            name='path',
            field=models.CharField(help_text='campo para identificarlo por la URL', max_length=250),
        ),
    ]
