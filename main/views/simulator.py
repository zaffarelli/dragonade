from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.incantessimi import Incantessimo
from main.models.nativi import Nativo
from main.models.viaggiatori import Viaggiatore
from main.models.creature import Creatura
from main.models.oggetti import Oggetto
from main.models.artefatti import Artefatto


def list_for(t):
    items = []
    klass = None
    if t == "viaggiatore":
        klass = Viaggiatore
    elif t == "nativo":
        klass = Nativo
    elif t == "creatura":
        klass = Creatura
    elif t == "incantessimo":
        klass = Incantessimo
    elif t == "artefatto":
        klass = Artefatto
    elif t == "oggetto":
        klass = Oggetto
    for x in klass.objects.all().order_by("name"):
        datum = x.toJson()
        datum['name'] = x.name
        datum['code'] = x.rid
        datum['type'] = t
        items.append(datum)
    return items


# Simulateur de Mêlée
def combattants(request):
    pass
    context = prepare_context(request)
    travellers = list_for("Viaggiatore")
    autochtons = list_for("Nativo")
    creatures = list_for("Creatura")
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


def kicker(request):
    answer = {'html': "", "red_team": [], "green_team": [], "blue_team": []}
    html = ''
    if is_ajax(request):
        from main.models.characters import Character
        from main.models.viaggiatori import Viaggiatore
        from main.models.nativi import Nativo
        from main.models.creature import Creatura
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
