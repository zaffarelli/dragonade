from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from datetime import datetime

from django.template.loader import get_template
# from django.views.decorators.csrf import csrf_exempt

from main.utils.mechanics import FONTSET, MENU_ENTRIES, is_ajax, MAIN_MENU
from main.utils.ref_dragonade import stress_table_json, action_quality_json, soak_table_json, pdom_table_json, \
    sus_table_json, scon_table_json, comp_table_json, gear_table_json, weapon_table_json, secondaries_table_json, miscellaneous_table_json

# from main.models.stregoneria import Spell
from main.views.chiaroscuro import prepare_pagination

CHAR_PER_PAGE = 12

from main.views.generic import prepare_context


def incantessimi_list(request):
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    context['config']['modules'].append('stregoneria')
    incantessimi = []
    for i in Spell.objects.order_by("path","-category", "pentacle_code"):
        datum = i.export_to_json()
        datum['type'] = "stregoneria"
        datum['code'] = i.rid
        incantessimi.append(datum)
    context["incantessimi"]  = incantessimi
    return render(request, 'main/incantessimi/incantessimi_list.html', context)

def incantessimo_show(request):
    context = prepare_context(request)
    context['config']['modules'].append('stregoneria')
    from main.models.stregoneria import Spell
    if is_ajax(request):
        rid = request.POST["rid"]
        stregoneria = Spell.objects.filter(rid=rid)
        if len(stregoneria)==1:
            s = stregoneria.first()
            datum = s.export_to_json()
            datum['type'] = "stregoneria"
            datum['code'] = s.rid
            context["stregoneria"] = datum
            return render(request, 'main/incantessimi/stregoneria_card.html', context)
    return HttpResponse(status=204)