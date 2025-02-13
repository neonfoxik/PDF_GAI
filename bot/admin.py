from django.contrib import admin
from .models import (
    User,
    Button,
    Documents,
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

class ButtonGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_button', 'is_main_group']
    list_display_links = ['name']
    search_fields = ['name', 'parent_button']
    list_editable = ['is_main_group']

class TextsAdmin(admin.ModelAdmin):
    list_display = ['name_txt', 'parent_button']
    list_display_links = ['name_txt']
    search_fields = ['name_txt', 'parent_button']
    list_editable = ['parent_button']


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['address', 'name', ]
    list_display_links = ['name', ]


admin.site.register(User, UserAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonGroup, ButtonGroupAdmin)
admin.site.register(Texts, TextsAdmin)  # Регистрация нового класса
