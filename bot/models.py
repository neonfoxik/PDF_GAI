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

    chat_history = models.JSONField(
        verbose_name='История переписки пользователя',
        null=True,
        blank=True,
        default=dict
    )
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Content(models.Model):
    content_text = models.CharField(
        max_length=4096,
        verbose_name='текст контента',
    )
    is_main_group = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контенты'

    def __str__(self):
        return self.content_text[:10]

class Button(models.Model):
    button_id = models.AutoField(primary_key=True, default=0)
    text = models.CharField(
        max_length=20,
        verbose_name='текст кнопки'
    )
    child = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='Child_content', blank=True, null=True)
    parent = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='Parent_content')

    class Meta:
        verbose_name = 'кнопка'
        verbose_name_plural = 'Кнопки'

    def __int__(self):
        return self.button_id


class Documents(models.Model):
    address = models.CharField(
        max_length=40
    )
    name = models.CharField(
        max_length=40,
    )
    template_fields = models.JSONField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.address


class UserTemplateVariable(models.Model):
    """Модель для хранения пользовательских переменных шаблона"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='template_variables')
    display_name = models.CharField(max_length=255, verbose_name="Отображаемое название")
    template_field = models.CharField(max_length=255, verbose_name="Поле в шаблоне")
    value = models.TextField(blank=True, null=True, verbose_name="Значение")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Переменная шаблона"
        verbose_name_plural = "Переменные шаблона"
        ordering = ['display_name']

    def __str__(self):
        return f"{self.display_name} ({self.template_field})"


