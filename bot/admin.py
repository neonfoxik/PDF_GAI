from django.contrib import admin
from .models import (
    User,
    Button
)

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', ]
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', 'has_plan']
    list_editable = ['has_plan',]

class ButtonAdmin(admin.ModelAdmin):
    list_display = ['button_name', 'button_group', 'number_str']
    list_display_links = ['button_name',]
    search_fields = ['button_name', 'button_group']
    list_editable = ['button_group', 'number_str']

admin.site.register(User, UserAdmin)
admin.site.register(Button, ButtonAdmin)
