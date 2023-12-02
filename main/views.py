from django.http import JsonResponse, Http404
from django.shortcuts import render
from datetime import datetime

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from main.utils.mechanics import FONTSET, is_ajax


def prepare_index(request):
    d = datetime.now()
    context = {'fontset': FONTSET}
    return context


def index(request):
    context = prepare_index(request)
    return render(request, 'main/index.html', context=context)


def autochtons(request):
    from main.models.autochtons import Autochton
    context = prepare_index(request)
    characters = []
    for x in Autochton.objects.all().order_by("birthhour"):
        datum = x.toJson()
        characters.append(datum)
    context['characters'] = characters
    context['title'] = "Les Autochtones"
    # print(context)
    return render(request, 'main/autochtons.html', context=context)


@csrf_exempt
def inc_dec(request):
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            answer = {}
            new_roster = ''
            params = request.POST.get('params').split('__')
            print(params)
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
            if class_name == "Autochton":
                item = Autochton.objects.get(id=id)
                change_result = item.applyIncDec(attribute, change)
                context = {'a': item.toJson()}
                template = get_template('main/roster.html')
                new_roster = template.render(context, request)
                answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster


        return JsonResponse(answer)
    return Http404
