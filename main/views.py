from django.http import JsonResponse, Http404
from django.shortcuts import render
from datetime import datetime

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from main.utils.mechanics import FONTSET, is_ajax
from main.utils.ref_dragonade import stress_table_json,action_quality_json, soak_table_json, pdom_table_json, sus_table_json, scon_table_json, comp_table_json, gear_table_json, secondaries_table_json, miscellaneous_table_json


def prepare_index(request):
    d = datetime.now()
    context = {'config': {'fontset': FONTSET} }
    return context


def index(request):
    context = prepare_index(request)
    return render(request, 'main/index.html', context=context)


def autochtons(request):
    from main.models.autochtons import Autochton
    context = prepare_index(request)
    characters = []
    for x in Autochton.objects.all().order_by("dream"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['code'] = x.rid
        characters.append(datum)
    context['characters'] = characters
    context['title'] = "Les Autochtones"
    # print(context)
    return render(request, 'main/autochtons.html', context=context)


def travellers(request):
    from main.models.travellers import Traveller
    context = prepare_index(request)
    characters = []
    for x in Traveller.objects.all().order_by("player"):
        datum = x.toJson()
        datum['text'] = x.name
        characters.append(datum)
    context['characters'] = characters
    context['title'] = "Les Voyageurs"
    # print(context)
    return render(request, 'main/autochtons.html', context=context)


@csrf_exempt
def inc_dec(request):
    cando = False
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('params').split('__')
            # print(params)
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                if class_name == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name == "Traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    change_result = item.applyIncDec(attribute, change)
                    context = {'a': item.toJson()}
                    template = get_template('main/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster

        return JsonResponse(answer)
    return Http404


def maps(request):
    context = prepare_index(request)
    context['title'] = "Cartes & Plans"
    return render(request, 'main/autochtons.html', context=context)


def papers(request):
    # Load all papers
    # Some of them are collection (e.g. SCREEN1)
    context = prepare_index(request)
    context['data'] = []
    context['data'].append({"name": "Table de Stress", "code": "STRESS_TABLE", "id": 101, "data":stress_table_json()})
    context['data'].append({"name": "Qualité des Actions", "code": "QUALITY_TABLE", "id": 102, "data":action_quality_json()})
    context['data'].append({"name": "Table d'encaissement", "code": "SOAK_TABLE", "id": 103, "data":soak_table_json()})
    context['data'].append({"name": "Table +dom", "code": "PDOM_TABLE", "id": 104, "data": pdom_table_json()})
    context['data'].append({"name": "Table sus", "code": "SUS_TABLE", "id": 105, "data": sus_table_json()})
    context['data'].append({"name": "Table SC", "code": "SCON_TABLE", "id": 106, "data": scon_table_json()})

    context['data'].append({"name": "Martiales", "code": "COMP_WEAPONS_TABLE", "id": 201, "data": comp_table_json("WEAPONS")})
    context['data'].append({"name": "Génériques", "code": "COMP_GENERIC_TABLE", "id": 202, "data": comp_table_json("GENERIC")})
    context['data'].append({"name": "Particulières", "code": "COMP_PECULIAR_TABLE", "id": 203, "data": comp_table_json("PECULIAR")})
    context['data'].append({"name": "Spécialisées", "code": "COMP_SPECIALIZED_TABLE", "id": 204, "data": comp_table_json("SPECIALIZED")})
    context['data'].append({"name": "Connaissances", "code": "COMP_KNOWLEDGE_TABLE", "id": 205, "data": comp_table_json("KNOWLEDGE")})
    context['data'].append({"name": "Draconiques", "code": "COMP_DRACONIC_TABLE", "id": 206, "data": comp_table_json("DRACONIC")})

    context['data'].append({"name": "Secondaries", "code": "SECONDARIES_TABLE", "id": 250, "data": secondaries_table_json()})
    context['data'].append({"name": "Miscellaneous", "code": "MISC_TABLE", "id": 251, "data": miscellaneous_table_json()})

    from main.models.equipment import Equipment
    x = 1
    for cat in Equipment.objects.order_by().values('category').distinct():
        context['data'].append({"name": f"Equipement {x}", "code": f"GEAR_TABLE_{cat['category'].upper()}", "id": 300+x, "data": gear_table_json(cat['category'])})
        x += 1
        print(x,cat)



    context['data'].append({"name": "Ecran volet 1", "code": "SCREEN1", "id": 666, "data": {}})
    context['data'].append({"name": "Ecran volet 2", "code": "SCREEN2", "id": 667, "data": {}})
    context['data'].append({"name": "Ecran volet 3", "code": "SCREEN3", "id": 668, "data": {}})
    context['data'].append({"name": "Ecran volet 4", "code": "SCREEN4", "id": 669, "data": {}})
    context['data'].append({"name": "Ecran volet 5", "code": "SCREEN5", "id": 670, "data": {}})

    context['title'] = "Aides de Jeu"
    return render(request, 'main/papers.html', context=context)

def load(request):
    from main.utils.ref_dragonade import load_from_file
    load_from_file()