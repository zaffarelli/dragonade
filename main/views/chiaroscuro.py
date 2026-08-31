from main.models.oggetti import Oggetto
from main.utils.mechanics import is_ajax, zaff_decode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.nativi import Nativo
from main.models.artefatti import Artefatto
from main.models.creature import Creatura
from main.models.viaggiatori import Viaggiatore
from main.models.incantessimi import Incantessimo
from main.models.oggetti import Oggetto
from main.models.sogni import Sogno

ITEMS_PER_LIST = 15


def model_to_class(cls_str):
    klasses = [Incantessimo, Artefatto, Viaggiatore, Nativo, Creatura, Oggetto, Sogno]
    for klass in klasses:
        if klass.__name__ == cls_str:
            return klass
    return None




def value_shift(request):
    answer = {'rid': None, "data": ''}
    if is_ajax(request):
        from main.models.incantessimi import Incantessimo
        print(request.POST)
        rid = request.POST.get('rid')
        id = request.POST.get('id')
        param = request.POST.get('param')
        back = int(request.POST.get('back'))
        model = request.POST.get('model')
        spells = Incantessimo.objects.filter(rid=rid)
        print(f"{rid} {param} {model} {back}")
        if len(spells) == 1:
            spell = spells.first()
            current_value = getattr(spell, param)
            answer["rid"] = rid
            answer["model"] = model.title()
            from main.models.incantessimi import DragonadeGround, DragonadeEmanation, DragonadeHour, DragonadeElement, DragonadeConsistency, \
                IncantessimoCategory, IncantessimoPath, DragonadeDifficulty
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
            context = {"i": spell.export_to_json(), "model": model.title()}

            template = get_template("main/chiaroscuro/item_body.html")
            answer['data'] = template.render(context)

    answer['rid'] = rid
    return JsonResponse(answer)


def value_push(request):
    cando = False
    print("CO: VALUE PUSH")
    if is_ajax(request):
        if request.method == 'POST':
            answer = {}
            new_roster = ''
            params = request.POST.get('refs').split('__')
            rid = request.POST.get('rid')
            new_value = request.POST.get('new_value')
            value = zaff_decode(new_value)
            value = value.replace("  "," ")
            value = value.strip()
            print("New value     =>", new_value)
            print("Value to push =>", value)
            print("Params =>", params)
            if len(params) >= 3:
                class_name = params[0].title()
                print(f"Class: {class_name}")
                rid = params[1]
                attribute = params[2].lower()
                if class_name.title() == "Nativo":
                    item = Nativo.objects.get(rid=rid)
                    cando = True
                if class_name.title() == "Creature":
                    item = Creatura.objects.get(rid=rid)
                    cando = True
                if class_name.title() == "Incantessimo":
                    print(f"spell: {rid}")
                    item = Incantessimo.objects.get(rid=rid)
                    print(item)
                    cando = True
                if class_name.title() == "Viaggiatore":
                    item = Viaggiatore.objects.get(rid=rid)
                    print("Traveller found: ", item.rid)
                    cando = True
        if cando:
            print(f"### VALUE PUSH ### {item.name}: Pushing [{attribute}] with [{value}]!!")
            change_result = item.applyValuePush(attribute, value)
            x = item.export_to_json()
            model = class_name.title()
            context = {'i': x, "model": model}
            template = get_template('main/chiaroscuro/item_body.html')
            new_roster = template.render(context, request)
            answer['rid'] = item.rid
            answer['id'] = item.id
            answer['change_result'] = change_result
            answer['data'] = new_roster
            context = {}
            context['a'] = x
            context['model'] = model
            template = get_template("main/objects/roster.html")
            html = template.render(context, request)
            answer['html'] = html

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
    from main.models.incantessimi import IncantessimoPath
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
    from main.models.creature import DragonadeCreatureType
    for k, p in enumerate(DragonadeCreatureType.values):
        if p > 0:
            pa = {"param": "creature_type", "value": p, "label": DragonadeCreatureType.labels[k]}
            zfilters.append(pa)
    return zfilters


def creature_list(request):
    options = {}
    options['model'] = "Creatura"
    options["zfilters"] = creature_options()
    return items_list(request, options)


def creature_filters(request):
    options = {}
    options['model'] = "Creatura"
    options["zfilters"] = creature_options()
    return items_filters(request, options)


# Artefatto
def artefatti_options():
    zfilters = []
    return zfilters


def artefatti_list(request):
    options = {}
    options['model'] = "Artefatto"
    options["zfilters"] = artefatti_options()
    return items_list(request, options)


def artefatti_filters(request):
    options = {}
    options['model'] = "Artefatto"
    options["zfilters"] = artefatti_options()
    return items_filters(request, options)

# Oggetti
def oggetti_options():
    zfilters = []
    from main.models.oggetti import OggettoCategory
    for k, p in enumerate(OggettoCategory.values):
        if p > 0:
            pa = {"param": "category", "value": p, "label": OggettoCategory.labels[k]}
            zfilters.append(pa)
    return zfilters


def oggetti_list(request):
    options = {}
    options['model'] = "Oggetto"
    options["zfilters"] = oggetti_options()
    return items_list(request, options)


def oggetti_filters(request):
    options = {}
    options['model'] = "Oggetto"
    options["zfilters"] = oggetti_options()
    return items_filters(request, options)



# Generics
def items_list(request, options={}):
    """ Landing page for spells listing
    """
    from main.views.generic import prepare_context
    context = prepare_context(request)
    k = model_to_class(options["model"])
    if k:
        if options["model"] == 'Incantessimo':
            context['config']['modules'].append('stregoneria')
        elif options["model"] == 'Artefatto':
            context['config']['modules'].append('appartus')
        else:
            context['config']['modules'].append('taccuino')
        items = []
        for i in k.objects.order_by("name"):
            datum = i.export_to_json()
            items.append(datum)
        context["title"] = k.__name__
        context["model"] = options['model']
        context["items"] = items
        spells_j = Incantessimo.references()
        refs = {}
        refs['incantessimi'] = spells_j
        equipment = Oggetto.references()
        refs['equipment'] = equipment
        context["references"] = refs

        context["zfilters"] = options["zfilters"]
        return render(request, 'main/chiaroscuro/items_list.html', context)
    return HttpResponse(status=204)


def items_filters(request, options={}):
    """ Spells listing update
    """
    answer = {}
    if is_ajax(request):
        context = {}
        param = request.POST.get('param')
        value = request.POST.get('value')
        if value.lower() in ["true", "false"]:
            v = value == "true"
        else:
            v = value
        filters = {
            f"{param}": v
        }
        items = []
        k = model_to_class(options["model"])
        if k:
            for i in k.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = k.__name__
            context["items"] = items
            context["zfilters"] = options["zfilters"]
            template = get_template("main/chiaroscuro/items_payload.html")
            answer['data'] = template.render(context)
            return JsonResponse(answer)
    return HttpResponse(status=204)


def edit(request):
    answer = {'rid': "", "model": "", "payload": {}}
    if is_ajax(request):
        rid = request.POST.get('rid')
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            items = k.objects.filter(rid=rid)
            if len(items) == 1:
                i = items.first()
                answer['rid'] = rid
                answer['model'] = k.__name__
                answer['payload'] = i.export_to_json()
                context = {}
                context['a'] = answer['payload']
                context['model'] = k.__name__
                template = get_template("main/objects/roster.html")
                html = template.render(context, request)
                answer['html'] = html
                return JsonResponse(answer)
    return HttpResponse(status=204)

def inc_dec(request):
    cando = False
    answer = {}
    item = None
    if is_ajax(request):
        if request.method == 'POST':
            answer = {}
            attribute = None
            new_roster = ''
            params = request.POST.get('params').split('__')
            if len(params) == 4:
                model = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                item = None
                if model.lower() == "nativo":
                    item = Nativo.objects.get(id=id)
                    cando = True
                if model.lower() == "creatura":
                    item = Creatura.objects.get(id=id)
                    cando = True
                if model.lower() == "incantessimo":
                    item = Incantessimo.objects.get(id=id)
                    cando = True
                if model.lower() == "viaggiatore":
                    item = Viaggiatore.objects.get(id=id)
                    cando = True
            if cando:
                print("success!!")
                change_result = item.applyIncDec(attribute, change)
                context = {'a': item.export_to_json(), "model":model.title()}
                template = get_template('main/objects/roster.html')
                new_roster = template.render(context, request)
                answer['id'] = item.id
                answer['rid'] = item.rid
                answer['change_result'] = change_result
                answer['new_roster'] = new_roster
                return JsonResponse(answer)

    return HttpResponse(status=204)



def fetch(request):
    answer = {'rid': "", "model": "", "payload": {}}
    if is_ajax(request):
        rid = request.POST.get('rid')
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            items = k.objects.filter(rid=rid)
            if len(items) == 1:
                i = items.first()
                answer['rid'] = i.rid
                answer['model'] = model
                answer['payload'] = i.export_to_json()
                return JsonResponse(answer)
    return HttpResponse(status=204)
