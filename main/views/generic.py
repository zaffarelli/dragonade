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


def prepare_context(request):
    d = datetime.now()
    context = {
        'config': {
            'fontset': FONTSET,
            'modules': [],
            'zmenu': MAIN_MENU
        },
        'list': {}
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
    from main.models.teams import Team
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
    for t in Autochton.objects.filter(dream__current=True).order_by("team", "name"):
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


def draconis_artes(request):
    from main.models.draconic_arts import Spell
    context = prepare_context(request)
    context['title'] = "Arts Draconiques"
    context['config']['modules'].append('risorse')
    context['config']['menu_entries'] = MENU_ENTRIES
    spells = list_for()
    for i in Spell.objects.all().order_by("name"):
        spells.append(i.export_to_json())
    context['spells'] = spells
    return render(request, 'main/pages/draconis_artes.html', context=context)


# Simulateur de Mêlée
def combattants(request):
    context = prepare_context(request)
    travellers = list_for("traveller")
    autochtons = list_for("autochton")
    creatures = list_for("creature")
    page = 1
    context['list']['traveller'] = travellers
    context = prepare_pagination(context, travellers, page, type="traveller", purpose="select")
    context['list']['autochton'] = autochtons
    context = prepare_pagination(context, autochtons, page, type="autochton", purpose="select")
    context['list']['creature'] = creatures
    context = prepare_pagination(context, creatures, page, type="creature", purpose="select")
    context['title'] = "Simulateur de Mêlée"

    from main.models.combats import Combat
    combats = Combat.objects.filter(is_current=True)
    if len(combats) == 1:
        combat = combats.first()
        context['combat'] = combat.export_to_json()
        print(combat.code)
    else:
        context['combat'] = ""
    return render(request, 'main/pages/combattants.html', context=context)


# Artefacts
def appartuses(request):
    from main.models.appartus import Appartus
    context = prepare_context(request)
    context['title'] = "Appartus & Merveilles Draconiques"
    context['config']['modules'].append('appartuses')
    context['config']['menu_entries'] = MENU_ENTRIES
    page = 1
    appartuses = list_for("appartus")
    for i in Appartus.objects.all().order_by("name"):
        appartuses.append(i.export_to_json())
    context = prepare_pagination(context, appartuses, page, "appartuses")
    return render(request, 'main/pages/appartuses.html', context)


# Autochtons
def autochtons(request):
    from main.models.stregoneria import Spell
    from main.models.equipment import Equipment
    context = prepare_context(request)
    t = "autochton"
    items = list_for(t)
    page = 1
    context = prepare_pagination(context, items, page, type=t, purpose="view")
    context['title'] = "Les Autochtones"
    # Options
    context['reference'] = {}
    spells_j = Spell.references()
    context['reference']['spells'] = spells_j
    gear_j = Equipment.references()
    context['reference']['gear'] = gear_j
    return render(request, 'main/pages/autochtons.html', context=context)


# Creatures
def creatures(request):
    from main.models.creatures import Creature
    from main.models.stregoneria import Spell
    from main.models.equipment import Equipment
    context = prepare_context(request)
    t = "creature"
    items = list_for(t)
    page = 1
    context = prepare_pagination(context, items, page, type=t)
    context['title'] = "Les Creatures"
    context['reference'] = {}
    spells_j = Spell.references()
    context['reference']['spells'] = spells_j
    equipment = Equipment.references()
    context['reference']['equipment'] = equipment
    return render(request, 'main/pages/creatures.html', context=context)


# Travellers
def travellers(request):
    from main.models.travellers import Traveller
    from main.models.stregoneria import Spell
    from main.models.equipment import Equipment
    context = prepare_context(request)
    t = 'traveller'
    items = list_for(t)
    page = 1
    context = prepare_pagination(context, items, page, type=t, purpose="view")
    context['title'] = "Les Voyageurs"
    # options
    spells_j = Spell.references()
    context['reference'] = {}
    context['reference']['spells'] = spells_j
    equipment = Equipment.references()
    context['reference']['equipment'] = equipment
    return render(request, 'main/pages/travellers.html', context=context)


def list_for(t):
    from main.models.stregoneria import Spell
    from main.models.autochtons import Autochton
    from main.models.travellers import Traveller
    from main.models.creatures import Creature
    from main.models.appartus import Appartus
    items = []
    klass = None
    if t == "traveller":
        klass = Traveller
    elif t == "autochton":
        klass = Autochton
    elif t == "creature":
        klass = Creature
    elif t == "stregoneria":
        klass = Spell
    elif t == "appartus":
        klass = Appartus
    for x in klass.objects.all().order_by("name"):
        datum = x.toJson()
        datum['name'] = x.name
        datum['code'] = x.rid
        datum['type'] = t
        items.append(datum)
    return items


# Spells
def stregoneria(request):
    from main.models.stregoneria import Spell
    from main.models.autochtons import Autochton
    from main.models.travellers import Traveller
    context = prepare_context(request)
    context['title'] = "Sortilèges & Effets Draconiques"
    context['config']['modules'].append('stregoneria')
    context['config']['menu_entries'] = MENU_ENTRIES
    haut_revants = []
    for t in Traveller.objects.all():
        if len(t.spells) > 0:
            datum = t.export_to_json()
            datum["spells_as_list"] = t.spells.split(" ")
            haut_revants.append(datum)
    for a in Autochton.objects.all():
        if len(a.spells) > 0:
            datum = a.export_to_json()
            datum["spells_as_list"] = a.spells.split(" ")
            haut_revants.append(datum)
    context['config']['haut_revants'] = haut_revants
    stregoneria = []
    for i in Spell.objects.order_by("-category", "name"):
        datum = i.export_to_json()
        datum['type'] = "stregoneria"
        datum['code'] = i.rid
        stregoneria.append(datum)
    context['config']['data'] = stregoneria
    print(stregoneria)
    page = 1
    context = prepare_pagination(context, stregoneria, page, "stregoneria")

    return render(request, 'main/pages/stregoneria.html', context)


def stregoneria_page(request):
    from main.models.stregoneria import Spell
    context = prepare_context(request)
    stregoneria = []
    for i in Spell.objects.order_by("-category", "name"):
        datum = i.export_to_json()
        datum['type'] = "stregoneria"
        datum['code'] = i.rid
        stregoneria.append(datum)
    page = int(request.POST["page"])
    context = prepare_pagination(context, stregoneria, page, "stregoneria")
    template = get_template("main/lists/list_content.html")
    html = template.render(context, request)
    return JsonResponse({"html": html})


def nativi_list(request):
    from main.models.autochtons import Autochton
    context = prepare_context(request)
    nativi = []
    for i in Autochton.objects.all().order_by("dream","name"):
        datum = i.export_to_json()
        datum['type'] = "autochton"
        datum['code'] = i.rid
        print(datum)
        nativi.append(datum)

    context["nativi"] = nativi
    return render(request, 'main/pages/nativi_list.html', context)



def new_creature(request):
    from main.models.creatures import Creature
    from main.utils.mechanics import random_term
    c = Creature()
    c.name = "Nouvelle " + random_term()
    c.save()
    return HttpResponse(status=204)


def new_spell(request):
    from main.models.stregoneria import Spell
    if is_ajax(request):
        name = request.POST.get('spell_name')
        s = Spell.new(name)
        print(f"New spell created: {s.name} [{s.rid}]")
    return HttpResponse(status=204)


def new_traveller(request):
    from main.models.travellers import Traveller
    from main.utils.mechanics import random_term
    c = Traveller()
    c.name = "Jane " + random_term()
    c.save()
    return HttpResponse(status=204)


def new_autochton(request):
    from main.models.autochtons import Autochton
    from main.utils.mechanics import random_term
    c = Autochton()
    c.name = "Joe " + random_term()
    c.save()
    return HttpResponse(status=204)


def overlay_edit(request):
    answer = {}
    changes = False
    import json
    from main.models.stregoneria import Spell
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

def value_shift(request):
    answer = {'rid': None, "data":''}
    if is_ajax(request):
        from main.models.stregoneria import Spell
        rid = request.POST.get('rid')
        param = request.POST.get('param')
        back = int(request.POST.get('back'))
        spells = Spell.objects.filter(rid=rid)
        if len(spells)==1:
            spell = spells.first()
            current_value = getattr(spell, param)
            answer["data"] = current_value
            from main.models.stregoneria import DragonadeGround, DragonadeEmanation, DragonadeHour, DragonadeElement, DragonadeConsistency, IncantessimoCategory, IncantessimoPath
            if param == "ground_charge":
                dataset = DragonadeGround.values
            elif param == "hour_charge":
                dataset = DragonadeHour.values
            elif param == "elemental_charge":
                dataset = DragonadeElement.values
            elif param == "emanation_charge":
                dataset = DragonadeEmanation.values
            elif param == "consistency_charge":
                dataset = DragonadeConsistency.values
            elif param == "category":
                dataset = IncantessimoCategory.values
            else:
                dataset = IncantessimoPath .values
            next_value_index = 0
            for k,v in enumerate(dataset):
                if v == current_value:
                    next_value_index = (k+back) % len(dataset)
                    print(dataset)
                    print(f"{k} -> {next_value_index}")
            setattr(spell, param, dataset[next_value_index])
            spell.save()
            context = {"s": spell.export_to_json()}
            template = get_template("main/incantessimi/incantessimo_body.html")
            answer['data'] = template.render(context)

    answer['rid'] = rid
    return JsonResponse(answer)

def fetch(request):
    answer = {'rid': "", "type": "", "payload": {}}
    if is_ajax(request):
        rid = request.POST.get('rid')
        type = request.POST.get('type')
        if type.lower() == "incantessimo":
            from main.models.stregoneria import Spell
            spells = Spell.objects.filter(rid=rid)
            if len(spells)==1:
                s = spells.first()
                answer['rid'] = rid
                answer['type'] = type
                answer['payload'] = s.export_to_json()
        return JsonResponse(answer)
    return HttpResponse(status=204)

def kicker(request):
    answer = {'html': "", "red_team": [], "green_team": [], "blue_team": []}
    html = ''
    if is_ajax(request):
        from main.models.characters import Character
        from main.models.travellers import Traveller
        from main.models.autochtons import Autochton
        from main.models.creatures import Creature
        from main.models.combats import Combat
        id = request.POST.get('id')
        code = request.POST.get('code')
        target = request.POST.get('target')
        action = request.POST.get('action')
        print(f"*** Id:{id} Code:{code} Target:{target} Action:{action}")
        item = None
        if target.lower() == "combat":
            if action.lower() == "ini":
                Combat.deactivate()
                combat = Combat()
                x = datetime.now()
                combat.code = f'{x.strftime("%W")}{x.strftime("%A")[:2]}{x.strftime("%H%M")}'
                combat.is_current = True
                combat.save()
                datum = combat.export_to_json()
                context = {"combat": datum}
                template = get_template("main/objects/combat_parameters.html")
                html = template.render(context, request)
            elif action.lower() == "run":
                combats = Combat.objects.filter(code=code)
                if len(combats) == 1:
                    combat = combats.first()
                    combat.prepare_fight()
                    main_data = combat.results()
                    context = {"battle": main_data}
                    template = get_template("main/objects/battle.html")
                    answer['main_html'] = template.render(context, request)
                    combat.save()
                    datum = combat.export_to_json()
                    context = {"combat": datum}
                    template = get_template("main/objects/combat_parameters.html")
                    html = template.render(context, request)
            elif action.lower() == "next":
                import json
                combats = Combat.objects.filter(code=code)
                if len(combats) == 1:
                    combat = combats.first()
                    issue = combat.new_round()
                    main_data = combat.results()
                    context = {"battle": main_data}
                    # print("Transmitted context...")
                    # print(json.dumps(context,indent=2))
                    template = get_template("main/objects/battle.html")
                    answer['main_html'] = template.render(context, request)
                    datum = combat.export_to_json()
                    context = {"combat": datum}
                    template = get_template("main/objects/combat_parameters.html")
                    html = template.render(context, request)

        if action.lower() == "view":
            item = Character.find_from_rid(code)
            if item is not None:
                datum = item.export_to_json()
                datum['type'] = item.type
                datum['code'] = item.rid
                context = {"a": datum}
                template = get_template("main/objects/roster.html")
                html = template.render(context, request)
                # print(html)
        if action.lower() == "select":
            item = Character.find_from_rid(code)
            blue = False
            if item is not None:
                combats = Combat.objects.filter(is_current=True)
                if len(combats) == 1:
                    combat = combats.first()
                    # combat.remove_contestants()
                    if item.type.lower() != 'creature':
                        # print(item.name)
                        combat.add_contestants("blue", [code])
                    else:
                        combat.add_contestants("red", [code])
                    combat.save()
                    datum = combat.export_to_json()
                    context = {"combat": datum}
                    template = get_template("main/objects/combat_parameters.html")
                    html = template.render(context, request)

    answer['html'] = html
    return JsonResponse(answer)
