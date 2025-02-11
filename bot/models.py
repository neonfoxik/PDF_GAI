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
        max_length=20,
        verbose_name='имя кнопки а также колбэк дата'
    )
    button_group = models.ForeignKey(
        'ButtonGroup',
        on_delete=models.CASCADE,
        verbose_name='группа кнопок'
    )
    button_text = models.CharField(
        max_length=100,
        verbose_name='текст кнопки'
    )


    class Meta:
        verbose_name = 'Кнопка'
        verbose_name_plural = 'Кнопки'

    def __str__(self):
        return self.button_name

class ButtonGroup(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=40,
        verbose_name='Имя группы кнопок'
    )
    is_main_group = models.BooleanField(default=False)
    parent_button = models.ForeignKey(
        'Button',
        on_delete=models.CASCADE,
        verbose_name='родительская кнопка'
    )

    class Meta:
        verbose_name = 'Группа кнопок'
        verbose_name_plural = 'Группы кнопок'

    def __str__(self):
        return self.name

class Texts(models.Model):
    name_txt = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name='Имя текста'
    )
    txt_text = models.CharField(
        max_length=4000,
        verbose_name='Текст кнопок'
    )
    parent_button = models.ForeignKey(
        'Button',
        on_delete=models.CASCADE,
        verbose_name='родительская кнопка'
    )

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'

    def __str__(self):
        return self.name_txt
