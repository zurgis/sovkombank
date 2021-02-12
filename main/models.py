from django.db import models
from django.core.validators import RegexValidator

#from concurrency.api import concurrency_check
from concurrency.fields import IntegerVersionField

# Create your models here.
class Application(models.Model):

    class Products(models.IntegerChoices):
        Auto = 1, 'Авто'
        Consumer_credit = 2, 'Потреб'
        Pledge = 3, 'Залог'
        Mortgage = 4, 'Ипотека'

    class Solutions(models.IntegerChoices):
        Approved = 1, 'Одобрено'
        Denied = 2, 'Отказано'
        Temporarily_denied = 3, 'Временный отказ'


    date = models.DateTimeField('Дата заявки', auto_now_add=True)
    product = models.PositiveSmallIntegerField('Продукт', choices=Products.choices)
    phone = models.CharField('Телефон клиента', 
        validators=[RegexValidator(r'^[+]\d{9,15}$', message='Номер телефона необходимо вводить в формате "+00000000000". Допускается до 15 цифр.')],
        help_text='Номер телефона в формате +00000000000. От 9 до 15 цифр', max_length=16)
    solution = models.PositiveIntegerField('Решение', choices=Solutions.choices, blank=True, null=True)
    comment = models.TextField('Комментарий к решению', blank=True, null=True)
    version = IntegerVersionField()


    class Meta:
        verbose_name_plural = 'Заявки'
        verbose_name = 'Заявка'


    # def save(self, *args, **kwargs):
    #     concurrency_check(self, *args, **kwargs)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.phone