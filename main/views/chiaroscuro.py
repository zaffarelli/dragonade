from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from main.utils.mechanics import is_ajax, zaff_decode
import base64




@csrf_exempt
def inc_dec(request):
    cando = False
    answer = {}
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
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
                if class_name.lower() == "traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    change_result = item.applyIncDec(attribute, change)
                    context = {'a': item.toJson()}
                    template = get_template('main/objects/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
                answer['change_result'] = change_result
                answer['new_roster'] = new_roster
                return JsonResponse(answer)
    return HttpResponse(status=204)


@csrf_exempt
def value_push(request):
    cando = False
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('refs').split('__')
            new_value = request.POST.get('new_value')
            value = zaff_decode(new_value)
            print("New value     =>",new_value)
            print("Value to push =>",value)
            if len(params) >= 3:
                class_name = params[0]
                id = params[1]
                attribute = params[2]
                if class_name.title() == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name.title() == "Traveller":
                    item = Traveller.objects.get(id=id)
                    cando = True
                if cando:
                    print("success!!")
                    change_result = item.applyValuePush(attribute, value)
                    context = {'a': item.toJson()}
                    template = get_template('main/objects/roster.html')
                    new_roster = template.render(context, request)
                    answer['id'] = item.id
            answer['change_result'] = change_result
            answer['new_roster'] = new_roster
            return JsonResponse(answer)
    return HttpResponse(status=204)
