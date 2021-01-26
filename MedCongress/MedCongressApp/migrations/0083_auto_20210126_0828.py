# Generated by Django 2.2.3 on 2021-01-26 13:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MedCongressApp', '0082_imagenhome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footer',
            name='telefono',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Entre un No. de teléfono correcto', regex='^(\\(\\+?\\d{2,3}\\)[\\*|\\s|\\-|\\.]?(([\\d][\\*|\\s|\\-|\\.]?){6})(([\\d][\\s|\\-|\\.]?){2})?|(\\+?[\\d][\\s|\\-|\\.]?){8}(([\\d][\\s|\\-|\\.]?){2}(([\\d][\\s|\\-|\\.]?){2})?)?)$')]),
        ),
        migrations.AlterField(
            model_name='reltallervotacion',
            name='taller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MedCongressApp.Taller'),
        ),
        migrations.AlterField(
            model_name='reltallervotacion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
