from django.contrib import admin
from .models import (
    User,
    Button,
    ButtonGroup,
    Texts
)

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', ]
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', 'has_plan']
    list_editable = ['has_plan',]

class ButtonAdmin(admin.ModelAdmin):
    list_display = ['button_name', 'button_group']
    list_display_links = ['button_name',]
    search_fields = ['button_name', 'button_group']
    list_editable = ['button_group']

class ButtonGroupAdmin(admin.ModelAdmin):  # Новый класс для аналогии
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']

admin.site.register(User, UserAdmin)
admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonGroup, ButtonGroupAdmin)  # Регистрация нового класса
