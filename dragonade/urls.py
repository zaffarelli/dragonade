from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static

from dragonade import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
