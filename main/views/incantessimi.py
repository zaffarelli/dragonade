from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from main.utils.mechanics import is_ajax
from main.models.stregoneria import Spell
from main.views.generic import prepare_context


def incantessimi_list(request):
    """ Landing page for spells listing
    """
    context = prepare_context(request)
    context['config']['modules'].append('stregoneria')
    incantessimi = []
    for i in Spell.objects.order_by("power"):
        datum = i.export_to_json()
        datum['type'] = "stregoneria"
        datum['code'] = i.rid
        incantessimi.append(datum)
    context["incantessimi"] = incantessimi
    return render(request, 'main/incantessimi/incantessimi_list.html', context)


def incantessimi_filter(request):
    """ Spells listing update
    """
    answer = {}
    if is_ajax(request):
        param = request.POST.get('param')
        value = request.POST.get('value')
        filters = {
            f"{param}": value
        }
        # context = prepare_context(request)
        incantessimi = []
        for i in Spell.objects.filter(**filters).order_by("power"):
            datum = i.export_to_json()
            datum['type'] = "stregoneria"
            datum['code'] = i.rid
            incantessimi.append(datum)
        context = {}
        context["incantessimi"] = incantessimi
        template = get_template("main/incantessimi/incantessimi_payload.html")
        answer['data'] = template.render(context)
        return JsonResponse(answer)
    return HttpResponse(status=204)
