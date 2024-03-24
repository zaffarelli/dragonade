from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import get_template
from main.utils.mechanics import is_ajax, zaff_decode


ITEMS_PER_LIST = 12

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


# @csrf_exempt
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
            print("New value     =>", new_value)
            print("Value to push =>", value)
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


# @csrf_exempt
def svg_to_pdf(request, slug):
    import cairosvg
    import os
    from django.conf import settings
    print("svg_to_pdf")
    response = {'status': 'error'}
    if is_ajax(request):
        pdf_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + request.POST["pdf_name"])
        svg_name = os.path.join(settings.MEDIA_ROOT, 'pdf/results/svg/' + request.POST["svg_name"])
        svgtxt = request.POST["svg"]
        with open(svg_name, "w") as f:
            f.write(svgtxt)
            f.close()
        cairosvg.svg2pdf(url=svg_name, write_to=pdf_name, scale=21)
        response['status'] = 'ok'
    return JsonResponse(response)

def paginator_switch(request):
    from main.views.generic import stregoneria_page, appartuses_page, autochtons_page, travellers_page
    if is_ajax(request):
        params = request.POST["params"]
        if params == "stregoneria":
            return stregoneria_page(request)
        if params == "appartuses":
            return appartuses_page(request)
        if params == "autochtons":
            return autochtons_page(request)
        if params == "travellers":
            return travellers_page(request)
    return JsonResponse({"html": 'Bad Paginator!'})

def prepare_pagination(context, all_items, page):
    from django.core.paginator import Paginator
    paginator = Paginator(all_items, ITEMS_PER_LIST)
    items_set = paginator.get_page(page)
    context['elements'] = items_set
    context['config']['data'] = all_items
    context['previous_page'] = ((page - 1) % paginator.num_pages)
    if context['previous_page'] == 0:
        context['previous_page'] = paginator.num_pages
    context['next_page'] = ((page + 1) % paginator.num_pages)
    if context['next_page'] == paginator.num_pages + 1:
        context['next_page'] = 1
    return context
