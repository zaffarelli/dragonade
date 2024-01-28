from django.shortcuts import render
from datetime import datetime
from main.utils.mechanics import FONTSET, MENU_ENTRIES
from main.utils.ref_dragonade import stress_table_json,action_quality_json, soak_table_json, pdom_table_json, sus_table_json, scon_table_json, comp_table_json, gear_table_json, secondaries_table_json, miscellaneous_table_json


def prepare_context(request):
    d = datetime.now()
    context = {
        'config': {
            'fontset': FONTSET,
            'modules': []
        }
    }
    return context


def index(request):
    context = prepare_context(request)
    context['config']['modules'].append('orologio')
    context['config']['menu_entries'] = MENU_ENTRIES
    context['title'] = "Le Portail du Coint"
    return render(request, 'main/pages/orologio.html', context=context)


def card_reveal(request):
    context = prepare_context(request)
    context['config']['modules'].append('risorse')
    context['config']['menu_entries'] = MENU_ENTRIES
    context['title'] = "Paralaxe"
    return render(request, 'main/pages/risorse.html', context=context)


def autochtons(request):
    from main.models.autochtons import Autochton
    context = prepare_context(request)
    context['config']['modules'].append('carte')
    characters = []
    for x in Autochton.objects.all().order_by("dream"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['code'] = x.rid
        datum['type'] = "autochton"
        characters.append(datum)
    context['characters'] = characters
    context['title'] = "Les Autochtones"
    # print(context)
    return render(request, 'main/pages/personae.html', context=context)

# def create_autochton(request, name=""):
#     from main.models.autochtons import Autochton
#     if len(name)==0:
#         key = "Joan Gruge"
#     else:
#         key = name
#     au = Autochton()
#     au.name = key
#     au.save()
#     context['new_autochton'] = au.toJson()
#     return JsonResponse(context)


def travellers(request):
    from main.models.travellers import Traveller
    context = prepare_context(request)
    characters = []
    for x in Traveller.objects.all().order_by("-player"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['type'] = "traveller"
        characters.append(datum)
    context['characters'] = characters
    context['title'] = "Les Voyageurs"
    return render(request, 'main/pages/personae.html', context=context)




def maps(request):
    context = prepare_context(request)
    context['config']['modules'].append('carte')
    context['title'] = "Cartes & Plans"
    return render(request, 'main/pages/piani.html', context=context)


def papers(request):
    # Load all papers
    # Some of them are collection (e.g. SCREEN1)
    context = prepare_context(request)
    context['config']['data'] = {}
    context['config']['data']["STRESS_TABLE"] = {"name": "Table de Stress", "code": "STRESS_TABLE", "id": 101, "data":stress_table_json()}
    context['config']['data']["QUALITY_TABLE"] = {"name": "Qualité des Actions", "code": "QUALITY_TABLE", "id": 102, "data":action_quality_json()}
    context['config']['data']["SOAK_TABLE"] = {"name": "Table d'encaissement", "code": "SOAK_TABLE", "id": 103, "data":soak_table_json()}
    context['config']['data']["PDOM_TABLE"] = {"name": "Table +dom", "code": "PDOM_TABLE", "id": 104, "data": pdom_table_json()}
    context['config']['data']["SUS_TABLE"] = {"name": "Table sus", "code": "SUS_TABLE", "id": 105, "data": sus_table_json()}
    context['config']['data']["SCON_TABLE"] = {"name": "Table SC", "code": "SCON_TABLE", "id": 106, "data": scon_table_json()}

    context['config']['data']["COMP_WEAPONS_TABLE"] = {"name": "Martiales", "code": "COMP_WEAPONS_TABLE", "id": 201, "data": comp_table_json("WEAPONS")}
    context['config']['data']["COMP_GENERIC_TABLE"] = {"name": "Génériques", "code": "COMP_GENERIC_TABLE", "id": 202, "data": comp_table_json("GENERIC")}
    context['config']['data']["COMP_PECULIAR_TABLE"] = {"name": "Particulières", "code": "COMP_PECULIAR_TABLE", "id": 203, "data": comp_table_json("PECULIAR")}
    context['config']['data']["COMP_SPECIALIZED_TABLE"] = {"name": "Spécialisées", "code": "COMP_SPECIALIZED_TABLE", "id": 204, "data": comp_table_json("SPECIALIZED")}
    context['config']['data']["COMP_KNOWLEDGE_TABLE"] = {"name": "Connaissances", "code": "COMP_KNOWLEDGE_TABLE", "id": 205, "data": comp_table_json("KNOWLEDGE")}
    context['config']['data']["COMP_DRACONIC_TABLE"] = {"name": "Draconiques", "code": "COMP_DRACONIC_TABLE", "id": 206, "data": comp_table_json("DRACONIC")}

    context['config']['data']["SECONDARIES_TABLE"] = {"name": "Secondaries", "code": "SECONDARIES_TABLE", "id": 250, "data": secondaries_table_json()}
    context['config']['data']["MISC_TABLE"] = {"name": "Miscellaneous", "code": "MISC_TABLE", "id": 251, "data": miscellaneous_table_json()}

    from main.models.equipment import Equipment
    x = 1
    for cat in Equipment.objects.order_by().values('category').distinct():
        context['config']['data'][f"GEAR_TABLE_{cat['category'].upper()}"] = {"name": f"Equipement {x}", "code": f"GEAR_TABLE_{cat['category'].upper()}", "id": 300+x, "data": gear_table_json(cat['category'])}
        x += 1

    from main.models.travellers import Traveller
    import json
    characters = []
    datum = {}
    for t in Traveller.objects.filter(gamers_team=True).order_by("player"):
        t.export_to_json()
        datum = t.data
        datum['text'] = t.name
        datum['type'] = "traveller"
        characters.append(datum)
    context['config']['data']["TRAVELLERS"] = {"name": "Travellers", "code": "TRAVELLERS", "id": 300, "data": characters}




    context['config']['data']["SCREEN1"] = {"name": "Ecran volet 1", "code": "SCREEN1", "id": 666, "data": {}}
    context['config']['data']["SCREEN2"] = {"name": "Ecran volet 2", "code": "SCREEN2", "id": 667, "data": {}}
    context['config']['data']["SCREEN3"] = {"name": "Ecran volet 3", "code": "SCREEN3", "id": 668, "data": {}}
    context['config']['data']["SCREEN4"] = {"name": "Ecran volet 4", "code": "SCREEN4", "id": 669, "data": {}}
    context['config']['data']["SCREEN5"] = {"name": "Ecran volet 5", "code": "SCREEN5", "id": 670, "data": {}}

    context['title'] = "Aides de Jeu"
    context['config']['modules'].append('carte')

    return render(request, 'main/pages/carte.html', context=context)

def load(request):
    pass
    from main.utils.ref_dragonade import load_from_file
    load_from_file()

def draconis_artes(request):
    from main.models.draconic_arts import Spell
    context = prepare_context(request)
    context['title'] = "Arts Draconiques"
    context['config']['modules'].append('risorse')
    context['config']['menu_entries'] = MENU_ENTRIES
    spells = []
    for i in Spell.objects.exclude(source__exact="-").order_by("name"):
        spells.append(i.export_to_json())
    context['spells'] = spells
    return render(request, 'main/pages/draconis_artes.html', context=context)
