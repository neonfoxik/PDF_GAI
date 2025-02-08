from django.conf import settings
from django.urls import path
from django.contrib import admin

from bot import views


app_name = 'bot'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.BOT_TOKEN, views.index, name="index"),
    path('', views.set_webhook, name="set_webhook"),
    path('status/', views.status, name="status"),
]
