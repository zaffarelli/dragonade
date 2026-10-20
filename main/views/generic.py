from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from main.utils.mechanics import FONTSET, MENU_ENTRIES, is_ajax, MAIN_MENU
from main.utils.ref_dragonade import stress_table_json, action_quality_json, soak_table_json, pdom_table_json, sus_table_json, scon_table_json, comp_table_json, \
    gear_table_json, weapon_table_json, secondaries_table_json, miscellaneous_table_json
from main.models.nativi import Nativo
from main.models.oggetti import Oggetto
from main.models.teams import Team


def prepare_context(request):
    context = {}
    context['config'] = {
        'fontset': FONTSET,
        'modules': [],
        'zmenu': MAIN_MENU
    }
    return context



@login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, "main/registration/login_error.html")
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
    return render(request, 'main/pages/piani.html', context=context)


def papers(request):
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
    for cat in Oggetto.objects.filter(special=False).values('category').distinct():
        print(cat)
        if cat['category'] == "mel":
            context['config']['data'][f"GEAR_TABLE_{cat['category'].upper()}"] = {"name": f"Equipement {x}",
                                                                                  "code": f"GEAR_TABLE_{cat['category'].upper()}",
                                                                                  "id": 300 + x,
                                                                                  "data": weapon_table_json(cat['category'])}
        else:
            context['config']['data'][f"GEAR_TABLE_{cat['category'].upper()}"] = {"name": f"Equipement {x}",
                                                                                  "code": f"GEAR_TABLE_{cat['category'].upper()}",
                                                                                  "id": 300 + x,
                                                                                  "data": gear_table_json(cat['category'])}
        x += 1

    # Autochtons
    characters = []
    for t in Nativo.objects.filter(dream__current=True).order_by("team", "name"):
        t.export_to_json()
        datum = t.data
        datum['text'] = t.name
        datum['type'] = "autochton"
        characters.append(datum)
    page_num = 0
    per_page = 2
    auto_pack = []
    for index, autochton in enumerate(characters):
        if index % per_page == 0:
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
    for team in Team.objects.order_by("name"):
        for t in team.travellers_list():
            t.export_to_json()
            datum = t.data
            datum['text'] = t.name
            datum['current_label'] = team.name
            datum['type'] = "traveller"
            characters.append(datum)
    page_num = 0
    trav_pack = []
    for index, traveller in enumerate(characters):
        # print("*****TRAV")
        # print(traveller)
        if index % per_page == 0:
            if (len(trav_pack) > 0):
                context['config']['data']["TRAVELLERS" + str(page_num)] = {
                    "name": traveller["current_label"] + " " + str(page_num),
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


def overlay_edit(request):
    answer = {}
    changes = False
    import json
    from main.models.incantessimi import Spell
    if is_ajax(request):
        json = json.loads(request.POST.get("item_info"))
        if json["model"] == "stregoneria":
            spell = Spell.objects.get(rid=json["rid"])
            for p in json["properties"]:
                if p in spell.__dict__:

                    nv = getattr(spell, p)
                    t = type(nv).__name__
                    if json["properties"][p] != f'{nv}':
                        print("Found: " + p)
                        print("Type: " + t, json["properties"][p], f'{nv}')
                        changes = True
                        print(f" > New value : {nv} becomes {json['properties'][p]} (with type {t})")
                        if t == "int":
                            setattr(spell, p, int(json['properties'][p]))
                        elif t == "string":
                            pval = json['properties'][p]
                            npval = pval.replace('"', "¤").replace("\n", " § ")
                            setattr(spell, p, npval)
                        elif t == "bool":
                            setattr(spell, p, bool(json['properties'][p]))
                        elif t == "float":
                            setattr(spell, p, float(json['properties'][p]))

                else:
                    print("Not Found: " + p)
                    if p == "charges":
                        print("Handling charges")
                        previous = [spell.ground_charge, spell.hour_charge, spell.consistency_charge,
                                    spell.emanation_charge, spell.elemental_charge]
                        current = json["properties"][p].split(" ")
                        next = []
                        for c in current:
                            next.append(int(c))
                        print(f"Previous...... {previous}")
                        print(f"Next.......... {next}")
                        idx = 0
                        for c in current:
                            if c != previous[idx]:
                                changes = True
                                if idx == 0:
                                    spell.ground_charge = c
                                elif idx == 1:
                                    spell.hour_charge = c
                                elif idx == 2:
                                    spell.consistency_charge = c
                                elif idx == 3:
                                    spell.emanation_charge = c
                                elif idx == 4:
                                    spell.elemental_charge = c
                            idx += 1
            if changes:
                spell.save()
    return JsonResponse(answer)
