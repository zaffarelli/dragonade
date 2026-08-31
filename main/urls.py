from django.urls import re_path
from main.views.generic import index, autochtons, creatures, travellers, maps, papers, card_reveal, \
    gardiendesreves, appartuses, combattants, new_creature, new_autochton, new_traveller, new_spell, overlay_edit, kicker


from main.views.incantessimi import IncantessimoDetailView
from main.views.chiaroscuro import inc_dec, value_push, svg_to_pdf, paginator_switch, value_shift, incantessimi_list, incantessimi_filters, nativi_list, \
    nativi_filters, viaggiatori_list, viaggiatori_filters, creature_list, creature_filters, artefatti_list, artefatti_filters, fetch, edit, oggetti_list, oggetti_filters
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  re_path(r'^$', index, name='index'),
                  re_path(r'^orologio$', index, name='index'),
                  re_path(r'^autochtons$', autochtons, name='autochtons'),
                  re_path(r'^creatures$', creatures, name='creatures'),
                  re_path(r'^travellers$', travellers, name='travellers'),
                  re_path(r'^piani$', maps, name='maps'),
                  re_path(r'^carte$', papers, name='papers'),
                  re_path(r'^combattimento', combattants, name='combattants'),
                  re_path(r'^risorse$', card_reveal, name='card_reveal'),
                  re_path(r'^appartuses$', appartuses, name='appartuses'),
                  # re_path(r'^stregoneria$', stregoneria, name='stregoneria'),
                  re_path(r'^nativi$', nativi_list, name='nativi_list'),
                  re_path(r'^gardiendesreves$', gardiendesreves, name='gardiendesreves'),
                  re_path(r'^ajax/inc_dec$', inc_dec, name='inc_dec'),
                  re_path(r'^ajax/value_push$', value_push, name='value_push'),
                  re_path(r'^ajax/paginator$', paginator_switch, name='paginator_switch'),
                  re_path(r'^ajax/svg2pdf/(?P<slug>[\w-]+)/$', svg_to_pdf, name='svg_to_pdf'),
                  re_path(r'^new_creature', new_creature, name='new_creature'),
                  re_path(r'^new_traveller', new_traveller, name='new_traveller'),
                  re_path(r'^new_autochton', new_autochton, name='new_autochton'),
                  re_path(r'^ajax/new/spell', new_spell, name='new_spell'),
                  re_path(r'^ajax/embedded/edit', IncantessimoDetailView.as_view()),
                  re_path(r'^ajax/overlay/edit', overlay_edit, name="overlay_edit"),
                  re_path(r'^ajax/kicker', kicker, name="kicker"),


                  re_path(r'^ajax/fetch', fetch, name="fetch"),
                  re_path(r'^ajax/edit', edit, name="edit"),
                  re_path(r'^ajax/value_shift', value_shift, name="value_shift"),
                  # Viaggiatori
                  re_path(r'^viaggiatori_list$', viaggiatori_list, name='viaggiatori_list'),
                  re_path(r'^ajax/viaggiatore_filter$', viaggiatori_filters, name='viaggiatori_filter'),
                  # Nativi
                  re_path(r'^nativi_list$', nativi_list, name='nativi_list'),
                  re_path(r'^ajax/nativo_filter$', nativi_filters, name='nativi_filter'),
                  # Creature
                  re_path(r'^creature_list$', creature_list, name='creature_list'),
                  re_path(r'^ajax/creatura_filter$', creature_filters, name='creature_filter'),
                  # Incantessimi
                  re_path(r'^incantessimi_list$', incantessimi_list, name='incantessimi_list'),
                  re_path(r'^ajax/incantessimo_filter$', incantessimi_filters, name='incantessimi_filter'),
                  # Artefatti
                  re_path(r'^artefatti_list$', artefatti_list, name='artefatti_list'),
                  re_path(r'^ajax/artefatto_filter$', artefatti_filters, name='artefatti_filters'),
                  # Oggetti
                  re_path(r'^oggetti_list$', oggetti_list, name='oggetti_list'),
                  re_path(r'^ajax/oggetto_filter$', oggetti_filters, name='oggetti_filters'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # + debug_toolbar_urls()
