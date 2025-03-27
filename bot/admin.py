from django.contrib import admin
from .models import (
    User,
    Content,
    Button
)


class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', 'is_admin']
    list_display_links = ['telegram_id']
    search_fields = ['telegram_id', 'name']
    list_editable = ['has_plan', 'is_admin']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['content_text', 'is_main_group']
    list_display_links = ['content_text']
    search_fields = ['content_text']


class ButtonAdmin(admin.ModelAdmin):
    list_display = ['text', 'parent']
    list_display_links = ['text']
    search_fields = ['text']


admin.site.register(User, UserAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Button, ButtonAdmin)
