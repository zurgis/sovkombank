from django.db import models
from django.core.validators import RegexValidator

from concurrency.fields import IntegerVersionField

# Create your models here.
class Application(models.Model):

    # Добавляем типы перечислений для селекторов
    class Products(models.TextChoices):
        Auto = 'Авто', 'Авто'
        Consumer_credit = 'Потреб', 'Потреб'
        Pledge = 'Залог', 'Залог'
        Mortgage = 'Ипотека', 'Ипотека'

    class Solutions(models.TextChoices):
        Approved = 'Одобрено', 'Одобрено'
        Denied = 'Отказано', 'Отказано'
        Temporarily_denied = 'Временный отказ', 'Временный отказ'

    date = models.DateTimeField('Дата заявки', auto_now_add=True)
    product = models.CharField('Продукт', choices=Products.choices, max_length=10)
    phone = models.CharField('Телефон клиента', 
        validators=[RegexValidator(r'^[+]\d{9,15}$', message='Номер телефона необходимо вводить в формате "+00000000000". Допускается от 9 до 15 цифр.')],
        help_text='Номер телефона в формате +00000000000. От 9 до 15 цифр', max_length=16)
    solution = models.CharField('Решение', choices=Solutions.choices, max_length=15, blank=True, null=True)
    comment = models.TextField('Комментарий к решению', blank=True, null=True)
    # Оптимистическая блокировка
    version = IntegerVersionField()


    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'

    def __str__(self):
        return self.phone