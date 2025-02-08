from django.contrib import admin
from .models import (
    User,

)

class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', 'has_plan', ]
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', 'has_plan']
    list_editable = ['has_plan',]


admin.site.register(User, UserAdmin)
