# Generated by Django 2.2.3 on 2020-11-05 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0031_auto_20201026_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='congreso',
            name='is_openpay',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='congreso',
            name='template',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='moderador',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.PerfilUsuario'),
        ),
        migrations.AlterField(
            model_name='ponente',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.PerfilUsuario'),
        ),
    ]
