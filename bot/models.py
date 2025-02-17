from django.db import models


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
    button_group = models.CharField(
        max_length=20,
        verbose_name='имя группы кнопок'
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

class Documents(models.Model):
    address = models.CharField(
        max_length=40,
        primary_key=True
    )
    name = models.CharField(
        max_length=40,
    )
    parent_button = models.CharField(
        max_length=20,
        verbose_name='Имя родительской кнопки'
    )
    fields = models.CharField(
        max_length=35,
        verbose_name="Поля"
    )
    class Meta:
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.address


class ParsValues(models.Model):
    world_value = models.CharField(
        primary_key=True,
        max_length=60,
        verbose_name='Переменная в ворлде'
    )
    user_text = models.CharField(
        max_length=20,
        verbose_name='текст который видит пользователь'
    )

    class Meta:
        verbose_name = 'Переменная'
        verbose_name_plural = 'Переменные'

    def __str__(self):
        return self.world_value



class ButtonGroup(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=20,
        verbose_name='Имя группы кнопок'
    )
    parent_button = models.CharField(
        max_length=20,
        verbose_name='Имя родительской кнопки'
    )
    is_main_group = models.BooleanField(default=False)
    is_document = models.BooleanField(default=False)
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
    parent_button = models.CharField(
        max_length=20,
        verbose_name='имя родительской кнопки'
    )

    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'

    def __str__(self):
        return self.name_txt

