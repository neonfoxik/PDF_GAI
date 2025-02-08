from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve as mediaserve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', include('bot.urls', namespace='bot'))
]
