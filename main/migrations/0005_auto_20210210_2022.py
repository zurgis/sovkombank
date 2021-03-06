# Generated by Django 3.1.6 on 2021-02-10 20:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210210_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='Номер телефона необходимо вводить в формате "+00000000000". Допускается до 15 цифр.')], verbose_name='Телефон клиента'),
        ),
    ]
