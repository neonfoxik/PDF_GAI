from django.db import models
from django import utils



class User(models.Model):
    telegram_id = models.CharField(
        primary_key=True,
        max_length=50
    )
    name = models.CharField(
        max_length=35,
        verbose_name='Имя',
    )
    is_admin = models.BooleanField(default=False)
    has_plan = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Button(models.Model):
    button_name = models.CharField(
        primary_key=True,
        max_length=40
    )
    button_group = models.CharField(
        max_length=40,
        verbose_name='группа кнопок'
    )
    button_text = models.CharField(
        max_length=100,
        verbose_name='группа кнопок'
    )
    number_str = models.IntegerField()

    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return self.button_name