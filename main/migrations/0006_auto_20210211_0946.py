# Generated by Django 3.1.6 on 2021-02-11 09:46

import concurrency.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210210_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(help_text='Номер телефона в формате +00000000000. От 9 до 15 цифр', max_length=16, validators=[django.core.validators.RegexValidator('^[+]\\d{9,15}$', message='Номер телефона необходимо вводить в формате "+00000000000". Допускается до 15 цифр.')], verbose_name='Телефон клиента'),
        ),
    ]
