from django.shortcuts import render
from datetime import datetime
from main.utils.mechanics import FONTSET


def prepare_index(request):
    d = datetime.now()
    context = {'fontset': FONTSET}
    return context


def index(request):
    context = prepare_index(request)
    return render(request, 'main/index.html', context=context)


def autochtons(request):
    from main.models import Autochton
    context = prepare_index(request)
    characters = []
    for x in Autochton.objects.all().order_by("dream"):
        datum = x.toJson()
        characters.append(datum)
    context['characters'] = characters
    print(context)
    return render(request, 'main/autochtons.html', context=context)
