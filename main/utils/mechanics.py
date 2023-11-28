FONTSET = ['Quicksand', 'Fredoka', 'Neucha', 'Syne+Mono', 'Abel', 'Satisfy', 'Acme', 'Roboto', 'Hubballi', 'Gruppo']


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'
