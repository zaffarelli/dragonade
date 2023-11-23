from django.urls import re_path
from main.views import index, autochtons
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^autochtons$', autochtons, name='autochtons'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
