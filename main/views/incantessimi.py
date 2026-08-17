from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from main.utils.mechanics import FONTSET, MENU_ENTRIES, is_ajax, MAIN_MENU

CHAR_PER_PAGE = 12

from main.views.generic import prepare_context


def incantessimi_list(request):
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    context['config']['modules'].append('stregoneria')
    incantessimi = []
    for i in Spell.objects.order_by("power"):
        datum = i.export_to_json()
        datum['type'] = "stregoneria"
        datum['code'] = i.rid
        incantessimi.append(datum)
    context["incantessimi"] = incantessimi
    return render(request, 'main/incantessimi/incantessimi_list.html', context)

