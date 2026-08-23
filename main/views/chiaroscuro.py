from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import get_template
from main.utils.mechanics import is_ajax, zaff_decode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.stregoneria import Spell
from main.models.autochtons import Autochton
from main.models.travellers import Traveller
from main.models.creatures import Creature


ITEMS_PER_LIST = 15


def inc_dec(request):
    cando = False
    answer = {}
    item = None
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.creatures import Creature
            from main.models.travellers import Traveller
            answer = {}
            attribute = None
            new_roster = ''
            params = request.POST.get('params').split('__')
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                item = None
                if class_name.lower() == "autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name.lower() == "creature":
                    item = Creature.objects.get(id=id)
                    cando = True
                if class_name.lower() == "traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                # if cando:
                #     change_result = item.applyIncDec(attribute, change)
                #     context = {'a': item.toJson()}
                #     template = get_template('main/objects/roster.html')
                #     new_roster = template.render(context, request)
                #     answer['id'] = item.id
                # answer['change_result'] = change_result
                # answer['new_roster'] = new_roster
                # return JsonResponse(answer)
            if cando:
                print("success!!")
                change_result = item.applyIncDec(attribute, change)
                context = {'a': item.toJson()}
                template = get_template('main/objects/roster.html')
                new_roster = template.render(context, request)
                answer['id'] = item.id
                answer['change_result'] = change_result
                answer['new_roster'] = new_roster
                return JsonResponse(answer)

    return HttpResponse(status=204)

def value_shift(request):
    answer = {'rid': None, "data": ''}
    if is_ajax(request):
        from main.models.stregoneria import Spell
        print(request.POST)
        rid = request.POST.get('rid')
        id = request.POST.get('id')
        param = request.POST.get('param')
        back = int(request.POST.get('back'))
        model = request.POST.get('model')
        spells = Spell.objects.filter(rid=rid)
        print(f"{rid} {param} {model} {back}")
        if len(spells) == 1:
            spell = spells.first()
            current_value = getattr(spell, param)
            answer["rid"] = rid
            answer["model"] = model.title()
            from main.models.stregoneria import DragonadeGround, DragonadeEmanation, DragonadeHour, DragonadeElement, DragonadeConsistency, \
                IncantessimoCategory, IncantessimoPath,DragonadeDifficulty
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
            elif param == "diff":
                dataset = DragonadeDifficulty.values

            else:
                dataset = IncantessimoPath.values
            next_value_index = 0
            for k, v in enumerate(dataset):
                if v == current_value:
                    next_value_index = (k + back) % len(dataset)
                    print(dataset)
                    print(f"{k} -> {next_value_index}")
            setattr(spell, param, dataset[next_value_index])
            print(f"New values is [{dataset[next_value_index]}] for [{param}].")
            spell.save()
            context = {"s": spell.export_to_json(), "model": model.title()}

            template = get_template("main/incantessimi/incantessimo_body.html")
            answer['data'] = template.render(context)

    answer['rid'] = rid
    return JsonResponse(answer)


def value_push(request):
    cando = False
    print("CO: VALUE PUSH")
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.creatures import Creature
            from main.models.travellers import Traveller
            from main.models.stregoneria import Spell
            answer = {}
            new_roster = ''
            params = request.POST.get('refs').split('__')
            rid = request.POST.get('rid')
            new_value = request.POST.get('new_value')
            value = zaff_decode(new_value)
            print("New value     =>", new_value)
            print("Value to push =>", value)
            print("Params =>", params)
            if len(params) >= 3:
                class_name = params[0]
                print(f"Class: {class_name}")
                id = params[1]
                attribute = params[2]
                if class_name.title() == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name.title() == "Creature":
                    item = Creature.objects.get(id=id)
                    cando = True
                if class_name.title() == "Incantessimo":
                    print(f"spell: {rid}")
                    item = Spell.objects.get(rid=rid)
                    print(item)
                    cando = True
                if class_name.title() == "Traveller":
                    item = Traveller.objects.get(id=id)
                    print("Traveller found: ", item.rid)
                    cando = True
        if cando:
            print("success!!")
            change_result = item.applyValuePush(attribute, value)
            context = {'s': item.toJson(), "model": class_name.title()}
            template = get_template('main/incantessimi/incantessimo_body.html')
            new_roster = template.render(context, request)
            answer['rid'] = item.rid
            answer['change_result'] = change_result
            answer['data'] = new_roster
            return JsonResponse(answer)
    return HttpResponse(status=204)


def svg_to_pdf(request, slug):
    import cairosvg
    import os
    from django.conf import settings
    category = ""
    response = {'status': 'error'}
    if is_ajax(request):
        if "category" in request.POST:
            category = request.POST["category"]
            if category != "":
                category += "/"
        pdf_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + category + request.POST["pdf_name"])
        svg_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + category + request.POST["svg_name"])
        svgtxt = request.POST["svg"]
        with open(svg_name, "w") as f:
            relinked = svgtxt.replace("static/main/svg/2024/", "../refs/")
            f.write(relinked)
            f.close()
        cairosvg.svg2pdf(url=svg_name, write_to=pdf_name, scale=21, unsafe=True)
        response['status'] = 'ok'
    return JsonResponse(response)


def paginator_switch(request):
    if is_ajax(request):
        params = request.POST["params"]
        p = request.POST["purpose"]
        return paginate(request, t=params, purpose=p)
    return JsonResponse({"html": 'Bad Paginator!'})


def paginate(request, t="", purpose="view"):
    from main.views.generic import prepare_context, list_for
    context = prepare_context(request)
    items = list_for(t)
    page = int(request.POST["page"])
    context = prepare_pagination(context, items, page, t, purpose)
    local_context = {}
    local_context["list"] = context['list'][t]
    template = get_template("main/lists/list_content.html")
    html = template.render(local_context, request)
    return JsonResponse({"html": html})


def prepare_pagination(context, all_items, page=1, type="", purpose="view"):
    from django.core.paginator import Paginator
    if type == "":
        context['error'] = "Not type given to paginator"
    else:
        paginator = Paginator(all_items, ITEMS_PER_LIST)
        p = paginator.page(page)
        pagination = {}
        pagination['type'] = type
        pagination['purpose'] = purpose
        pagination['previous_page'] = p.previous_page_number() if p.has_previous() else page
        pagination['current_page'] = page
        pagination['next_page'] = p.next_page_number() if p.has_next() else page
        pagination['num_pages'] = paginator.num_pages
        pagination['elements'] = p.object_list
        context['list'][type] = pagination
    return context



# Incantessimi
def incantessimi_options():
    zfilters = []
    from main.models.stregoneria import IncantessimoPath
    for k, p in enumerate(IncantessimoPath.values):
        if p > 0:
            pa = {"param": "path", "value": p, "label": IncantessimoPath.labels[k]}
            zfilters.append(pa)
    return zfilters


def incantessimi_list(request):
    options = {}
    options['model'] = "Incantessimo"
    options["zfilters"] = incantessimi_options
    return items_list(request, options)


def incantessimi_filters(request):
    options = {}
    options['model'] = "Incantessimo"
    options["zfilters"] = incantessimi_options()
    return items_filters(request, options)


# Viaggiatori
def viaggiatori_options():
    zfilters = []
    filters = [
        {"param": "is_storyteller", "value": True, "label": "Gardien des Rêves"},
        {"param": "is_storyteller", "value": False, "label": "Joueurs"},
    ]
    for filter in filters:
        zfilters.append(filter)
    return zfilters


def viaggiatori_list(request):
    options = {}
    options['model'] = "Viaggiatore"
    options["zfilters"] = viaggiatori_options()
    return items_list(request, options)


def viaggiatori_filters(request):
    options = {}
    options['model'] = "Viaggiatore"
    options["zfilters"] = viaggiatori_options()
    return items_filters(request, options)


# Nativi
def nativi_options():
    zfilters = []
    pa = {"param": "dream", "value": "RDC", "label": "Royaume du Coint"}
    zfilters.append(pa)
    pa = {"param": "dream", "value": "RHS", "label": "Royaume de Haute-Styrie"}
    zfilters.append(pa)
    return zfilters


def nativi_list(request):
    options = {}
    options['model'] = "Nativo"
    options["zfilters"] = nativi_options()
    return items_list(request, options)


def nativi_filters(request):
    options = {}
    options['model'] = "Nativo"
    options["zfilters"] = nativi_options()
    return items_filters(request, options)

# Creature
def creature_options():
    zfilters = []
    from main.models.creatures import DragonadeCreatureType
    for k, p in enumerate(DragonadeCreatureType.values):
        if p > 0:
            pa = {"param": "creature_type", "value": p, "label": DragonadeCreatureType.labels[k]}
            zfilters.append(pa)
    return zfilters


def creature_list(request):
    options = {}
    options['model'] = "Creature"
    options["zfilters"] = creature_options()
    return items_list(request, options)


def creature_filters(request):
    options = {}
    options['model'] = "Creature"
    options["zfilters"] = creature_options()
    return items_filters(request, options)


# Generics
def items_list(request, options={}):
    """ Landing page for spells listing
    """
    from main.views.generic import prepare_context
    context = prepare_context(request)
    if options["model"] == "Incantessimo":
        context['config']['modules'].append('stregoneria')
        items = []
        for i in Spell.objects.order_by("name"):
            datum = i.export_to_json()
            # datum['type'] = "stregoneria"
            # datum['code'] = i.rid
            items.append(datum)
        context["title"] = "Arts Draconiques"
        context["model"] = "Incantessimo"
    elif options["model"] == "Nativo":
        context['config']['modules'].append('taccuino')
        items = []
        for i in Autochton.objects.order_by("name"):
            datum = i.export_to_json()
            items.append(datum)
        context["title"] = "Autochtones"
        context["model"] = "Nativo"
    elif options["model"] == "Viaggiatore":
        context['config']['modules'].append('taccuino')
        items = []
        for i in Traveller.objects.order_by("name"):
            datum = i.export_to_json()
            items.append(datum)
        context["title"] = "Voyageurs"
        context["model"] = "Viaggiatore"
    elif options["model"] == "Creature":
        context['config']['modules'].append('taccuino')
        items = []
        for i in Creature.objects.order_by("name"):
            datum = i.export_to_json()
            items.append(datum)
        context["title"] = "Créatures"
        context["model"] = "Creature"
    context["items"] = items
    context["zfilters"] = options["zfilters"]
    return render(request, 'main/chiaroscuro/items_list.html', context)


def items_filters(request, options={}):
    """ Spells listing update
    """
    answer = {}
    if is_ajax(request):
        context = {}
        param = request.POST.get('param')
        value = request.POST.get('value')
        if value.lower() in ["true","false"]:
            v = value == "true"
        else:
            v = value
        filters = {
            f"{param}": v
        }
        items = []
        if options["model"].lower() == "incantessimo":
            for i in Spell.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = "Incantessimo"
        elif options["model"].lower() == "nativo":
            items = []
            for i in Autochton.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = "Nativo"
        elif options["model"].lower() == "viaggiatore":
            items = []
            for i in Traveller.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = "Viaggiatore"
        elif options["model"].lower() == "creature":
            items = []
            for i in Creature.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = "Creature"
        context["items"] = items
        context["zfilters"] = options["zfilters"]
        template = get_template("main/chiaroscuro/items_payload.html")
        answer['data'] = template.render(context)
        return JsonResponse(answer)
    return HttpResponse(status=204)
