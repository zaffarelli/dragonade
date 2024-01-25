from django.urls import re_path
from main.views.generic import index, autochtons,  travellers, maps, papers, card_reveal, draconis_artes
from main.views.chiaroscuro import inc_dec, value_push
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^orologio$', index, name='index'),
    re_path(r'^personae_a$', autochtons, name='autochtons'),
    re_path(r'^personae_t$', travellers, name='travellers'),
    re_path(r'^piani$', maps, name='maps'),
    re_path(r'^carte$', papers, name='papers'),
    re_path(r'^risorse$', card_reveal, name='card_reveal'),
    re_path(r'^draconis_artes$', draconis_artes, name='draconis_artes'),
    re_path(r'^ajax/inc_dec$', inc_dec, name='inc_dec'),
    # re_path(r'^ajax/value_pop$', value_pop, name='value_pop'),
    re_path(r'^ajax/value_push$', value_push, name='value_push')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
