# Generated by Django 3.1.6 on 2021-02-10 19:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('product', models.PositiveSmallIntegerField(choices=[(1, 'Авто'), (2, 'Потреб'), (3, 'Залог'), (4, 'Ипотека')], default=0, error_messages={'required': 'Выберите тип продукта'}, verbose_name='Продукт')),
                ('phone', models.PositiveSmallIntegerField(max_length=16, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='Номер телефона необходимо вводить в формате "+00000000000". Допускается до 15 цифр.')], verbose_name='Телефон клиента')),
                ('solution', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Одобрено'), (2, 'Отказано'), (3, 'Временный отказ')], default=0, null=True, verbose_name='Решение')),
                ('comment', models.TextField(verbose_name='Комментарий к решению')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
