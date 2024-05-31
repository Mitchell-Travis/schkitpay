# Generated by Django 5.0.1 on 2024-02-11 02:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wellet', '0002_alter_cardpasscode_pass_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpasscode',
            name='pass_code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Numeric Field. Only 4 digits allowed.', regex='^\\+?1?\\d{6}$')]),
        ),
        migrations.AlterField(
            model_name='verifiedpasscode',
            name='verified_pass_code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Numeric Field. Only 4 digits allowed.', regex='^\\+?1?\\d{6}$')]),
        ),
    ]