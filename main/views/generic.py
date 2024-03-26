from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

from django.template.loader import get_template
# from django.views.decorators.csrf import csrf_exempt

from main.utils.mechanics import FONTSET, MENU_ENTRIES, is_ajax
from main.utils.ref_dragonade import stress_table_json, action_quality_json, soak_table_json, pdom_table_json, \
    sus_table_json, scon_table_json, comp_table_json, gear_table_json, secondaries_table_json, miscellaneous_table_json

# from main.models.stregoneria import Spell
from main.views.chiaroscuro import prepare_pagination

CHAR_PER_PAGE = 12


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
    context['title'] = "Parallaxe"
    return render(request, 'main/pages/risorse.html', context=context)


def gardiendesreves(request):
    context = prepare_context(request)
    context['config']['modules'].append('risorse')
    context['config']['menu_entries'] = MENU_ENTRIES
    context['config']['gdr'] = 1
    context['title'] = "Gardien des Rêves"
    return render(request, 'main/pages/gardiendesreves.html', context=context)


def maps(request):
    from main.utils.mechanics import fetch_maps
    context = prepare_context(request)
    context['config']['modules'].append('piani')
    context['config']['maps'] = fetch_maps()
    context['title'] = "Cartes & Plans"
    print(context['config']['maps'])
    return render(request, 'main/pages/piani.html', context=context)


def papers(request):
    from main.models.equipment import Equipment
    from main.models.travellers import Traveller
    from main.models.autochtons import Autochton
    # Load all papers
    # Some of them are collection (e.g. SCREEN1)
    context = prepare_context(request)
    context['config']['data'] = {}
    context['config']['data']["STRESS_TABLE"] = {"name": "Table de Stress", "code": "STRESS_TABLE", "id": 101,
                                                 "data": stress_table_json()}
    context['config']['data']["QUALITY_TABLE"] = {"name": "Qualité des Actions", "code": "QUALITY_TABLE", "id": 102,
                                                  "data": action_quality_json()}
    context['config']['data']["SOAK_TABLE"] = {"name": "Table d'encaissement", "code": "SOAK_TABLE", "id": 103,
                                               "data": soak_table_json()}
    context['config']['data']["PDOM_TABLE"] = {"name": "Table +dom", "code": "PDOM_TABLE", "id": 104,
                                               "data": pdom_table_json()}
    context['config']['data']["SUS_TABLE"] = {"name": "Table sus", "code": "SUS_TABLE", "id": 105,
                                              "data": sus_table_json()}
    context['config']['data']["SCON_TABLE"] = {"name": "Table SC", "code": "SCON_TABLE", "id": 106,
                                               "data": scon_table_json()}

    context['config']['data']["COMP_WEAPONS_TABLE"] = {"name": "Martiales", "code": "COMP_WEAPONS_TABLE", "id": 201,
                                                       "data": comp_table_json("WEAPONS")}
    context['config']['data']["COMP_GENERIC_TABLE"] = {"name": "Génériques", "code": "COMP_GENERIC_TABLE", "id": 202,
                                                       "data": comp_table_json("GENERIC")}
    context['config']['data']["COMP_PECULIAR_TABLE"] = {"name": "Particulières", "code": "COMP_PECULIAR_TABLE",
                                                        "id": 203, "data": comp_table_json("PECULIAR")}
    context['config']['data']["COMP_SPECIALIZED_TABLE"] = {"name": "Spécialisées", "code": "COMP_SPECIALIZED_TABLE",
                                                           "id": 204, "data": comp_table_json("SPECIALIZED")}
    context['config']['data']["COMP_KNOWLEDGE_TABLE"] = {"name": "Connaissances", "code": "COMP_KNOWLEDGE_TABLE",
                                                         "id": 205, "data": comp_table_json("KNOWLEDGE")}
    context['config']['data']["COMP_DRACONIC_TABLE"] = {"name": "Draconiques", "code": "COMP_DRACONIC_TABLE", "id": 206,
                                                        "data": comp_table_json("DRACONIC")}

    context['config']['data']["SECONDARIES_TABLE"] = {"name": "Secondaries", "code": "SECONDARIES_TABLE", "id": 250,
                                                      "data": secondaries_table_json()}
    context['config']['data']["MISC_TABLE"] = {"name": "Miscellaneous", "code": "MISC_TABLE", "id": 251,
                                               "data": miscellaneous_table_json()}
    x = 1
    for cat in Equipment.objects.filter(special=False).values('category').distinct():
        context['config']['data'][f"GEAR_TABLE_{cat['category'].upper()}"] = {"name": f"Equipement {x}",
                                                                              "code": f"GEAR_TABLE_{cat['category'].upper()}",
                                                                              "id": 300 + x,
                                                                              "data": gear_table_json(cat['category'])}
        x += 1

    # Autochtons
    characters = []
    for t in Autochton.objects.filter(dream__current=True).order_by("group", "name"):
        t.export_to_json()
        datum = t.data
        datum['text'] = t.name
        datum['type'] = "autochton"
        characters.append(datum)
    page_num = 0
    auto_pack = []
    for index, autochton in enumerate(characters):
        if index % 3 == 0:
            if (len(auto_pack) > 0):
                context['config']['data']["AUTOCHTONS" + str(page_num)] = {"name": "Autochtones " + str(page_num),
                                                                           "code": "AUTOCHTONS" + str(page_num),
                                                                           "id": 800 + page_num, "data": auto_pack}
            page_num += 1
            auto_pack = []
        auto_pack.append(autochton)
    if (len(auto_pack) > 0):
        context['config']['data']["AUTOCHTONS" + str(page_num)] = {"name": "Autochtones " + str(page_num),
                                                                   "code": "AUTOCHTONS" + str(page_num),
                                                                   "id": 800 + page_num, "data": auto_pack}

    # Travellers
    characters = []
    for t in Traveller.objects.filter(gamers_team=True).order_by("player"):
        t.export_to_json()
        datum = t.data
        datum['text'] = t.name
        datum['type'] = "traveller"
        characters.append(datum)
    page_num = 0
    trav_pack = []
    for index, traveller in enumerate(characters):
        if index % 3 == 0:
            if (len(trav_pack) > 0):
                context['config']['data']["TRAVELLERS" + str(page_num)] = {"name": "Voyageurs" + str(page_num),
                                                                           "code": "TRAVELLERS" + str(page_num),
                                                                           "id": 700 + page_num, "data": trav_pack}
            page_num += 1
            trav_pack = []
        trav_pack.append(traveller)
    if (len(trav_pack) > 0):
        context['config']['data']["TRAVELLERS" + str(page_num)] = {"name": "Voyageurs" + str(page_num),
                                                                   "code": "TRAVELLERS" + str(page_num),
                                                                   "id": 700 + page_num, "data": trav_pack}

    context['config']['data']["SCREEN1"] = {"name": "Ecran volet 1", "code": "SCREEN1", "id": 671, "data": {}}
    context['config']['data']["SCREEN2"] = {"name": "Ecran volet 2", "code": "SCREEN2", "id": 672, "data": {}}
    context['config']['data']["SCREEN3"] = {"name": "Ecran volet 3", "code": "SCREEN3", "id": 673, "data": {}}
    context['config']['data']["SCREEN4"] = {"name": "Ecran volet 4", "code": "SCREEN4", "id": 674, "data": {}}
    context['config']['data']["SCREEN5"] = {"name": "Ecran volet 5", "code": "SCREEN5", "id": 675, "data": {}}
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
    for i in Spell.objects.all().order_by("name"):
        spells.append(i.export_to_json())
    context['spells'] = spells
    return render(request, 'main/pages/draconis_artes.html', context=context)


# Spells
def stregoneria(request):
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    context['title'] = "Sortilèges & Effets Draconiques"
    context['config']['modules'].append('stregoneria')
    context['config']['menu_entries'] = MENU_ENTRIES
    stregoneria = []
    for i in Spell.objects.order_by("category", "path", "name"):
        stregoneria.append(i.export_to_json())
    page = 1
    context = prepare_pagination(context, stregoneria, page)
    return render(request, 'main/pages/stregoneria.html', context)


def stregoneria_page(request):
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    stregoneria = []
    for i in Spell.objects.order_by("path", "category", "name"):
        stregoneria.append(i.export_to_json())
    page = int(request.POST["page"])
    context = prepare_pagination(context, stregoneria, page)
    template = get_template("main/lists/stregoneria_list.html")
    html = template.render(context, request)
    return JsonResponse({"html": html})


# Artefacts
def appartuses(request):
    from main.models.appartus import Appartus
    context = prepare_context(request)
    context['title'] = "Appartus & Merveilles Draconiques"
    context['config']['modules'].append('appartuses')
    context['config']['menu_entries'] = MENU_ENTRIES
    page = 1
    appartuses = []
    for i in Appartus.objects.all().order_by("name"):
        appartuses.append(i.export_to_json())
    context = prepare_pagination(context, appartuses, page)
    return render(request, 'main/pages/appartuses.html', context)


def appartuses_page(request):
    from main.models.appartus import Appartus
    context = prepare_context(request)
    appartuses = []
    for i in Appartus.objects.order_by("category", "name"):
        appartuses.append(i.export_to_json())
    page = int(request.POST["page"])
    context = prepare_pagination(context, appartuses, page)
    template = get_template("main/lists/appartuses_list.html")
    html = template.render(context, request)
    return JsonResponse({"html": html})


# Autochtons
def autochtons(request):
    from main.models.autochtons import Autochton
    from main.models.stregoneria import Spell
    from main.models.equipment import Equipment
    context = prepare_context(request)
    characters = []
    for x in Autochton.objects.all().order_by("-priority", "name"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['code'] = x.rid
        datum['type'] = "autochton"
        characters.append(datum)
    context['title'] = "Les Autochtones"
    page = 1
    context['reference'] = {}
    spells_j = Spell.references()
    context['reference']['spells'] = spells_j
    gear_j = Equipment.references()
    context['reference']['gear'] = gear_j
    context = prepare_pagination(context, characters, page)
    return render(request, 'main/pages/autochtons.html', context=context)


def autochtons_page(request):
    from main.models.autochtons import Autochton
    context = prepare_context(request)
    characters = []
    for x in Autochton.objects.all().order_by("-priority", "name"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['code'] = x.rid
        datum['type'] = "autochton"
        characters.append(datum)
    page = int(request.POST["page"])
    context = prepare_pagination(context, characters, page)
    template = get_template("main/lists/autochtons_list.html")
    html = template.render(context, request)
    return JsonResponse({"html": html})


# Travellers
def travellers(request):
    from main.models.travellers import Traveller
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    characters = []
    for x in Traveller.objects.all().order_by("-player"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['type'] = "traveller"
        characters.append(datum)
    page = 1
    context['characters'] = characters
    context['title'] = "Les Voyageurs"

    spells_j = Spell.references()
    context['reference'] = {}
    context['reference']['spells'] = spells_j
    context = prepare_pagination(context, characters, page)

    return render(request, 'main/pages/travellers.html', context=context)


def travellers_page(request):
    from main.models.travellers import Traveller
    context = prepare_context(request)
    characters = []
    for x in Traveller.objects.all().order_by("-priority", "name"):
        datum = x.toJson()
        datum['text'] = x.name
        datum['code'] = x.rid
        datum['type'] = "traveller"
        characters.append(datum)
    context['title'] = "Les Voyageurs"
    page = int(request.POST["page"])
    context = prepare_pagination(request, context, characters, page)
    template = get_template("main/lists/travellers_list.html")
    html = template.render(context, request)
    return JsonResponse({"html": html})
