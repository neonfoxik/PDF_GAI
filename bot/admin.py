from django.contrib import admin
from .models import (
    User,
    Content,
    Button,
    Documents,
    UserTemplateVariable
)


class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', 'is_admin']
    list_display_links = ['telegram_id']
    search_fields = ['telegram_id', 'name']
    list_editable = ['has_plan', 'is_admin']


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['address', 'name']
    list_display_links = ['name']
    search_fields = ['address', 'name']


class UserTemplateVariableAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'template_field', 'value']
    list_display_links = ['user', 'display_name']
    search_fields = ['user__name', 'display_name']
    list_editable = ['value']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['content_text_preview', 'get_buttons_count']
    list_display_links = ['content_text_preview']
    search_fields = ['content_text']

    def content_text_preview(self, obj):
        return obj.content_text[:50] + '...' if len(obj.content_text) > 50 else obj.content_text
    content_text_preview.short_description = 'Текст контента'

    def get_buttons_count(self, obj):
        return Button.objects.filter(parent=obj).count()
    get_buttons_count.short_description = 'Количество кнопок'


class ButtonAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_parent_text', 'get_child_text']
    list_display_links = ['text']
    search_fields = ['text']
    list_filter = ['parent']
    raw_id_fields = ['parent', 'child']
    autocomplete_fields = ['parent', 'child']

    def get_parent_text(self, obj):
        return obj.parent.content_text[:30] + '...' if obj.parent else 'Главное меню'
    get_parent_text.short_description = 'Родительский контент'

    def get_child_text(self, obj):
        return obj.child.content_text[:30] + '...' if obj.child else '-'
    get_child_text.short_description = 'Дочерний контент'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].required = False
        form.base_fields['child'].required = False
        return form


admin.site.register(User, UserAdmin)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(UserTemplateVariable, UserTemplateVariableAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Button, ButtonAdmin)
