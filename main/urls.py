from django.urls import re_path
from main.views import index, autochtons, inc_dec, travellers, maps, papers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^index$', index, name='index'),
    re_path(r'^autochtons$', autochtons, name='autochtons'),
    re_path(r'^travellers$', travellers, name='travellers'),
    re_path(r'^maps$', maps, name='maps'),
    re_path(r'^papers$', papers, name='papers'),
    re_path(r'^ajax/inc_dec$', inc_dec, name='inc_dec'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
