from django import template

register = template.Library()


@register.filter(name='colorize_val')
def colorize_val(value):
    str = value
    if isinstance(value, int):
        if value >= 10:
            str = f'<span style="color:red;">{value}</span>'
        elif value >= 7:
            str = f'<span style="color:orangered;">{value}</span>'
        elif value >= 5:
            str = f'<span style="color:yellow;">{value}</span>'
    return str


@register.filter(name='signed')
def signed(value):
    str = value
    if isinstance(value, int):
        if value >= 0:
            str = f"+{value}"
        else:
            str = f"-{value}"
    return str


@register.filter(name='large_id')
def large_id(value):
    str = value
    if isinstance(value, int):
        str = f"{value:05}"
    return str


@register.filter(name='as_draconichour')
def as_draconichour(value):
    str = value
    if isinstance(value, int):
        if value > 0:
            str = f'static/main/svg/hdw_{value}.svg'
    return str


@register.filter(name='as_skill')
def as_skill(value):
    from main.utils.ref_dragonade import CHARACTER_STATISTICS
    str = value
    words = value.split('_')
    if words[0] == 'MAR':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['MARTIALES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'GEN':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['GENERALES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'PAR':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['PARTICULIERES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'SPE':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['SPECIALISEES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'CON':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['CONNAISSANCES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'DRA':
        for ref in CHARACTER_STATISTICS['COMPETENCES']['DRACONIQUES']['LISTE']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    return str


@register.filter(name='check_hidden')
def check_hidden(value):
    str = ""
    if int(value) < 1:
        str = ' hidden'
    return str
