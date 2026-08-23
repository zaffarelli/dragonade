from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.stregoneria import Spell
from main.models.autochtons import Autochton
from main.models.travellers import Traveller
from main.models.creatures import Creature
from main.views.generic import prepare_context


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
