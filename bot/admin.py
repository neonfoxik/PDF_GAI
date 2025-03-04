from django.contrib import admin
from .models import (
    User,
    Button, 
    Documents,
    ButtonGroup,
    Texts,
    UserTemplateVariable
)


class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', 'is_admin']
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', 'has_plan']
    list_editable = ['has_plan', 'is_admin']


class ButtonAdmin(admin.ModelAdmin):
    list_display = ['button_name', 'button_group', 'button_text']
    list_display_links = ['button_name',]
    search_fields = ['button_name', 'button_group', 'button_text']
    list_editable = ['button_group', 'button_text']


class ButtonGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_button', 'is_main_group']
    list_display_links = ['name']
    search_fields = ['name', 'parent_button']
    list_editable = ['is_main_group']


class TextsAdmin(admin.ModelAdmin):
    list_display = ['name_txt', 'parent_button', 'txt_text']
    list_display_links = ['name_txt']
    search_fields = ['name_txt', 'parent_button', 'txt_text']
    list_editable = ['parent_button', 'txt_text']


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['address', 'name', 'template_fields']
    list_display_links = ['name', ]
    search_fields = ['address', 'name']


class UserTemplateVariableAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'template_field', 'value', 'created_at', 'updated_at']
    list_display_links = ['user', 'display_name']
    search_fields = ['user__name', 'display_name', 'template_field']
    list_editable = ['value']


admin.site.register(User, UserAdmin)
admin.site.register(Documents, DocumentsAdmin) 
admin.site.register(Button, ButtonAdmin)
admin.site.register(ButtonGroup, ButtonGroupAdmin)
admin.site.register(Texts, TextsAdmin)
admin.site.register(UserTemplateVariable, UserTemplateVariableAdmin)
