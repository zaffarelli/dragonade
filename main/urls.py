from django.urls import re_path
from main.views.generic import index, autochtons, travellers, maps, papers, card_reveal, draconis_artes, \
    gardiendesreves, appartuses, stregoneria
from main.views.chiaroscuro import inc_dec, value_push, svg_to_pdf, paginator_switch
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
    re_path(r'^appartuses$', appartuses, name='appartuses'),
    re_path(r'^stregoneria$', stregoneria, name='stregoneria'),
    re_path(r'^gardiendesreves$', gardiendesreves, name='gardiendesreves'),
    re_path(r'^draconis_artes$', draconis_artes, name='draconis_artes'),
    re_path(r'^ajax/inc_dec$', inc_dec, name='inc_dec'),
    # re_path(r'^ajax/value_pop$', value_pop, name='value_pop'),
    re_path(r'^ajax/value_push$', value_push, name='value_push'),
    re_path(r'^ajax/paginator$', paginator_switch, name='paginator_switch'),
    re_path(r'^ajax/svg2pdf/(?P<slug>[\w-]+)/$', svg_to_pdf, name='svg_to_pdf')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
