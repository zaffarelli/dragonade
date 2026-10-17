from django.template import RequestContext

from main.models.oggetti import Oggetto
from main.models.poteri_speciali import PotereSpeciale
from main.utils.mechanics import is_ajax, zaff_decode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.nativi import Nativo
from main.models.artefatti import Artefatto
from main.models.creature import Creatura
from main.models.viaggiatori import Viaggiatore
from main.models.incantessimi import Incantessimo, IncantessimoCategory
from main.models.oggetti import Oggetto
from main.models.sogni import Sogno

# ITEMS_PER_LIST = 15


def model_to_class(cls_str):
    klasses = [Incantessimo, Artefatto, Viaggiatore, Nativo, Creatura, Oggetto, Sogno, PotereSpeciale]
    for klass in klasses:
        if klass.__name__.lower() == cls_str.lower():
            return klass
    return None


def to_pdf(request):
    answer = {"model": None}
    if is_ajax(request):
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            k.export_to_pdf()
            answer["model"] = model
            return JsonResponse(answer)
    return HttpResponse(status=200)


def value_shift(request):
    answer = {'rid': None, "data": ''}
    if is_ajax(request):
        from main.models.incantessimi import Incantessimo
        print(request.POST)
        id = request.POST.get('id')
        param = request.POST.get('param')
        back = int(request.POST.get('back'))
        model = request.POST.get('model').title()
        k = model_to_class(model)
        print(f"{id} {param} {model} {back}")
        if k:
            items = k.objects.filter(id=id)
            if len(items) == 1:
                print("**** OBJECT FOUND !!!")
                item = items.first()
                answer['id'] = id
                item.value_shift(param, back)
                context = {"i": item.export_to_json(), "model": model.title()}
                template = get_template("main/chiaroscuro/item_body.html")
                answer['data'] = template.render(context)
        else:
            print(model, k, "Class not found")
        answer["model"] = model.title()
        answer['id'] = id
    return JsonResponse(answer)


def value_push(request):
    cando = False

    if is_ajax(request):
        if request.method == 'POST':
            answer = {}
            params = request.POST.get('refs').split('__')
            new_value = request.POST.get('new_value')
            value = zaff_decode(new_value)
            value = value.replace("  ", " ")
            value = value.strip()
            print("CO: VALUE PUSH")
            print(params)
            if len(params) >= 3:
                model = params[0].title()
                k = model_to_class(model)
                if k:
                    id = params[1]
                    attribute = params[2]
                    item = k.objects.get(id=id)
                    if item:
                        cando = True
            if cando:
                change_result = item.applyValuePush(attribute, value)
                x = item.export_to_json()
                context = {'i': x, "model": model}
                template = get_template('main/chiaroscuro/item_body.html')
                new_roster = template.render(context, request)
                # answer['rid'] = item.rid
                answer['id'] = item.id
                answer['change_result'] = change_result
                answer['data'] = new_roster
                # context = {}
                context['a'] = x
                # context['model'] = model
                template = get_template("main/objects/roster.html")
                html = template.render(context, request)
                answer['html'] = html
                answer['model'] = model
                return JsonResponse(answer)
    return HttpResponse(status=204)

def initialize_options():
    options = {"sogno_filter":False}
    return options


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

# Incantessimi
def incantessimi_options():
    zfilters = []
    from main.models.incantessimi import IncantessimoPath
    for k, p in enumerate(IncantessimoPath.values):
        if p > 0:
            pa = {"param": "path", "value": p, "label": IncantessimoPath.labels[k]}
            zfilters.append(pa)
    from main.models.incantessimi import IncantessimoCategory
    for k, p in enumerate(IncantessimoCategory.values):
        if p > 0:
            pa = {"param": "category", "value": p, "label": IncantessimoCategory.labels[k]}
            zfilters.append(pa)
    for incantessimo in Incantessimo.objects.filter(category=IncantessimoCategory.PENTACLE):
        if incantessimo.pentacle_code != "":
            zfilters.append({"param": "pentacle_code", "value": incantessimo.pentacle_code, "label": incantessimo.name, "icon": "fa-star"})

    return zfilters


def incantessimi_list(request):
    options = initialize_options()
    options['model'] = "Incantessimo"
    options["zfilters"] = incantessimi_options
    return items_list(request, options)


def incantessimi_filters(request):
    options = initialize_options()
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
    pa = {"param": "is_new", "value": True, "label": "Nouveau"}
    zfilters.append(pa)
    from main.models.sogni import Sogno
    for s in Sogno.objects.all():
        pa = {"param": "sogni", "value": s.acronym, "label": s.title, "rule": "contains"}
        zfilters.append(pa)
    for filter in filters:
        zfilters.append(filter)

    return zfilters


def viaggiatori_list(request):
    options = initialize_options()
    options['model'] = "Viaggiatore"
    options["zfilters"] = viaggiatori_options()
    options["sogno_filter"] = True
    return items_list(request, options)


def viaggiatori_filters(request):
    options = initialize_options()
    options['model'] = "Viaggiatore"
    options["zfilters"] = viaggiatori_options()
    options["sogno_filter"] = True
    return items_filters(request, options)


# Nativi
def nativi_options():
    zfilters = []
    # pa = {"param": "dream", "value": "RDC", "label": "Royaume du Coint"}
    # zfilters.append(pa)
    # pa = {"param": "dream", "value": "RHS", "label": "Royaume de Haute-Styrie"}
    # zfilters.append(pa)
    pa = {"param": "is_new", "value": True, "label": "Nouveau"}
    zfilters.append(pa)
    from main.models.sogni import Sogno
    for s in Sogno.objects.all():
        pa = {"param": "sogni", "value": s.acronym, "label": "Rêve="+s.title, "rule": "contains"}
        zfilters.append(pa)
    from main.models.sogni import Sogno
    s = Sogno.current_sogno()
    if s:
        sog = s.acronym
    else:
        sog = ""
    places = Nativo.objects.filter(sogni__contains=sog).order_by("place").distinct().values_list("place")
    for place in places:
        if len(place[0])>0:
            pa = {"param": "place", "value": place[0], "label": "Lieu="+place[0]}
            zfilters.append(pa)
    return zfilters


def nativi_list(request):
    options = initialize_options()
    options['model'] = "Nativo"
    options["zfilters"] = nativi_options()
    options["sogno_filter"] = True
    return items_list(request, options)


def nativi_filters(request):
    options = initialize_options()
    options['model'] = "Nativo"
    options["zfilters"] = nativi_options()
    options["sogno_filter"] = True
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
    options = initialize_options()
    options['model'] = "Creatura"
    options["zfilters"] = creature_options()
    options["sogno_filter"] = False
    return items_list(request, options)


def creature_filters(request):
    options = initialize_options()
    options['model'] = "Creatura"
    options["zfilters"] = creature_options()
    return items_filters(request, options)


# Artefatto
def artefatti_options():
    zfilters = []
    from main.models.artefatti import ArtefattoCategory
    for k, p in enumerate(ArtefattoCategory.values):
        pa = {"param": "category", "value": p, "label": ArtefattoCategory.labels[k]}
        zfilters.append(pa)
    return zfilters


def artefatti_list(request):
    options = initialize_options()
    options['model'] = "Artefatto"
    options["zfilters"] = artefatti_options()

    return items_list(request, options)


def artefatti_filters(request):
    options = initialize_options()
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
    pa = {"param": "is_basic", "value": True, "label": "Basique"}
    zfilters.append(pa)
    return zfilters


def oggetti_list(request):
    options = initialize_options()
    options['model'] = "Oggetto"
    options["zfilters"] = oggetti_options()

    return items_list(request, options)


def oggetti_filters(request):
    options = initialize_options()
    options['model'] = "Oggetto"
    options["zfilters"] = oggetti_options()
    return items_filters(request, options)

# Poteri Speciali
def poterispeciali_options():
    zfilters = []
    # from main.models.oggetti import OggettoCategory
    # for k, p in enumerate(OggettoCategory.values):
    #     if p > 0:
    #         pa = {"param": "category", "value": p, "label": OggettoCategory.labels[k]}
    #         zfilters.append(pa)
    # pa = {"param": "is_basic", "value": True, "label": "Basique"}
    # zfilters.append(pa)
    return zfilters


def poterispeciali_list(request):
    options = initialize_options()
    options['model'] = "PotereSpeciale"
    options["zfilters"] = poterispeciali_options()

    return items_list(request, options)


def poterispeciali_filters(request):
    options = initialize_options()
    options['model'] = "PotereSpeciale"
    options["zfilters"] = poterispeciali_options()
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
        sa, st = get_sogno()
        filters = {
        }
        if options["model"] in ['Viaggiatore', 'Nativo']:
            filters[f"sogni__contains"] = sa
        for i in k.objects.filter(**filters).order_by("name"):
            datum = i.export_to_json()
            items.append(datum)
        context["title"] = k.__name__
        context["sogno"] = st
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
        sa, st = get_sogno()
        param = request.POST.get('param')
        value = request.POST.get('value')
        rule = request.POST.get('rule')
        if value.lower() in ["true", "false"]:
            v = value == "true"
        else:
            v = value
        more = ""
        if rule:
            more = f"__{rule}"
        filters = {
            f"{param}{more}": v
        }
        # if options["model"] in ['Viaggiatore', 'Nativo']:
        #     filters[f"sogni__contains"] = sa
        items = []
        k = model_to_class(options["model"])
        if k:
            for i in k.objects.filter(**filters).order_by("name"):
                datum = i.export_to_json()
                items.append(datum)
            context["model"] = k.__name__
            context["sogno"] = st
            context["items"] = items
            context["zfilters"] = options["zfilters"]
            template = get_template("main/chiaroscuro/items_payload.html")
            answer['data'] = template.render(context)
            return JsonResponse(answer)
    return HttpResponse(status=204)


def new_item(request):
    answer = {}
    if is_ajax(request):
        context = {}
        model = request.POST.get('model')
        k = model_to_class(model)
        if k:
            id = k.spawn()
            answer['id'] = id
            return JsonResponse(answer)
        else:
            print("Model not found for new item")
    return HttpResponse(status=204)


def get_sogno():
    from main.models.sogni import Sogno
    sogno_acro = "DEF"
    sogno_txt = "FICS 11"
    sogni = Sogno.objects.filter(current=True)
    if len(sogni) > 0:
        sogno = sogni.first()
        sogno_acro = sogno.acronym
        sogno_txt = sogno.title
    return sogno_acro, sogno_txt


def edit(request):
    answer = {'id': "", "model": "", "payload": {}}
    if is_ajax(request):
        id = request.POST.get('id')
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            items = k.objects.filter(id=id)
            if len(items) == 1:
                i = items.first()
                answer['id'] = id
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


def randomize(request):
    answer = {'id': "", "model": "", "payload": {}}
    print("randomize")
    if is_ajax(request):
        id = request.POST.get('id')
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            items = k.objects.filter(id=id)
            if len(items) == 1:
                i = items.first()
                i.randomize()
                i.save()
                answer['id'] = id
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

                # model = request.POST.get('model').title()
                k = model_to_class(model)
                if k:
                    items = k.objects.filter(id=id)
                    if len(items) == 1:
                        item = items.first()
                        print("success!!")
                        change_result = item.applyIncDec(attribute, change)
                        context = {'a': item.export_to_json(), "model": model.title()}
                        template = get_template('main/objects/roster.html')
                        new_roster = template.render(context, request)
                        answer['id'] = item.id
                        answer['rid'] = item.rid
                        answer['change_result'] = change_result
                        answer['new_roster'] = new_roster
                        return JsonResponse(answer)

    return HttpResponse(status=204)


def fetch(request):
    answer = {'id': "", "model": "", "payload": {}}
    if is_ajax(request):
        id = request.POST.get('id')
        model = request.POST.get('model').title()
        k = model_to_class(model)
        if k:
            items = k.objects.filter(id=id)
            if len(items) == 1:
                i = items.first()
                answer['id'] = i.id
                answer['model'] = model
                answer['payload'] = i.export_to_json()
                return JsonResponse(answer)
    return HttpResponse(status=204)


def sogno_nuovo(request):
    # todo
    return HttpResponse(status=204)


def sogno_precedente(request):
    return sogno_nav(request, -1)


def sogno_seguente(request):
    return sogno_nav(request, 1)


def sogno_nav(request, x):
    Sogno.nav(x)
    return HttpResponse(status=204)
