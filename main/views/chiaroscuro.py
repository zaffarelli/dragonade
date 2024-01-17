from django.http import JsonResponse, Http404
from django.shortcuts import render
from datetime import datetime

from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from main.utils.mechanics import FONTSET, is_ajax, MENU_ENTRIES
from main.utils.ref_dragonade import stress_table_json,action_quality_json, soak_table_json, pdom_table_json, sus_table_json, scon_table_json, comp_table_json, gear_table_json, secondaries_table_json, miscellaneous_table_json



@csrf_exempt
def inc_dec(request):
    cando = False
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('params').split('__')
            # print(params)
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                item = None
                if class_name == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name == "Traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    change_result = item.applyIncDec(attribute, change)
                    context = {'a': item.toJson()}
                    template = get_template('main/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster

        return JsonResponse(answer)
    return Http404

@csrf_exempt
def value_pop(request):
    cando = False
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('params').split('__')
            # print(params)
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                if class_name == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name == "Traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    change_result = item.applyIncDec(attribute, change)
                    context = {'a': item.toJson()}
                    template = get_template('main/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster

        return JsonResponse(answer)
    return Http404

@csrf_exempt
def value_push(request):
    cando = False
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('params').split('__')
            # print(params)
            if len(params) == 4:
                class_name = params[0]
                id = int(params[1])
                attribute = params[2]
                change = params[3]
                if class_name == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name == "Traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    change_result = item.applyIncDec(attribute, change)
                    context = {'a': item.toJson()}
                    template = get_template('main/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster

        return JsonResponse(answer)
    return Http404
