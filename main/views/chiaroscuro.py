from django.http import JsonResponse, Http404, HttpResponse
from django.template.loader import get_template
from main.utils.mechanics import is_ajax, zaff_decode

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


def value_push(request):
    cando = False
    print("CO: VALUE PUSH")
    if is_ajax(request):
        if request.method == 'POST':
            from main.models.autochtons import Autochton
            from main.models.creatures import Creature
            from main.models.travellers import Traveller
            answer = {}
            new_roster = ''
            params = request.POST.get('refs').split('__')
            new_value = request.POST.get('new_value')
            value = zaff_decode(new_value)
            print("New value     =>", new_value)
            print("Value to push =>", value)
            print("Params =>", params)
            if len(params) >= 3:
                class_name = params[0]
                id = params[1]
                attribute = params[2]
                if class_name.title() == "Autochton":
                    item = Autochton.objects.get(id=id)
                    cando = True
                if class_name.title() == "Creature":
                    item = Creature.objects.get(id=id)
                    cando = True
                if class_name.title() == "Traveller":
                    item = Traveller.objects.get(id=id)
                    print("Traveller found: ", item.rid)
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
