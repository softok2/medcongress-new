# Generated by Django 2.2.3 on 2020-11-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0045_auto_20201117_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaPagInicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_og_title', models.CharField(max_length=50, null=True)),
                ('meta_description', models.CharField(max_length=160, null=True)),
                ('meta_og_description', models.CharField(max_length=160, null=True)),
                ('meta_og_type', models.CharField(max_length=50, null=True)),
                ('meta_og_url', models.CharField(max_length=50, null=True)),
                ('meta_twitter_card', models.CharField(max_length=50, null=True)),
                ('meta_twitter_site', models.CharField(max_length=50, null=True)),
                ('meta_twitter_creator', models.CharField(max_length=50, null=True)),
                ('meta_keywords', models.CharField(max_length=250, null=True)),
                ('meta_og_imagen', models.CharField(max_length=250, null=True)),
                ('meta_title', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'El Meta de la Página Inicio',
                'verbose_name_plural': 'Los Metas de la Página de Inicio',
            },
        ),
        migrations.CreateModel(
            name='MetaPagListCongreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_og_title', models.CharField(max_length=50, null=True)),
                ('meta_description', models.CharField(max_length=160, null=True)),
                ('meta_og_description', models.CharField(max_length=160, null=True)),
                ('meta_og_type', models.CharField(max_length=50, null=True)),
                ('meta_og_url', models.CharField(max_length=50, null=True)),
                ('meta_twitter_card', models.CharField(max_length=50, null=True)),
                ('meta_twitter_site', models.CharField(max_length=50, null=True)),
                ('meta_twitter_creator', models.CharField(max_length=50, null=True)),
                ('meta_keywords', models.CharField(max_length=250, null=True)),
                ('meta_og_imagen', models.CharField(max_length=250, null=True)),
                ('meta_title', models.CharField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'El Meta de la Página Listar Congresos',
                'verbose_name_plural': 'Los Metas de la Página Listar Congresos',
            },
        ),
    ]
