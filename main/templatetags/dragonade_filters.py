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
            str = f'<span style="color:orange;">{value}</span>'
        elif value >= 5:
            str = f'<span style="color:yellow;">{value}</span>'
        elif value >= 4:
            str = f'<span style="color:yellowgreen;">{value}</span>'
        elif value >= 3:
            str = f'<span style="color:green;">{value}</span>'
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
    if words[0] == 'WEA':
        for ref in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'GEN':
        for ref in CHARACTER_STATISTICS['SKILLS']['GENERIC']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'PEC':
        for ref in CHARACTER_STATISTICS['SKILLS']['PECULIAR']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'SPE':
        for ref in CHARACTER_STATISTICS['SKILLS']['SPECIALIZED']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'KNO':
        for ref in CHARACTER_STATISTICS['SKILLS']['KNOWLEDGE']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    if words[0] == 'DRA':
        for ref in CHARACTER_STATISTICS['SKILLS']['DRACONIC']['LIST']:
            if ref['NAME'] == value:
                str = ref['TEXT']
    return str


@register.filter(name='check_hidden')
def check_hidden(value):
    str = ""
    if int(value) < 1:
        str = ' hidden'
    return str


@register.filter(name='as_att_subset_position')
def as_att_subset_position(value):
    result = ""
    if value in ["AGI", "EMP", "APP", "TIR"]:
        result = "nw"
    if value in ["CON", "ODG", "DEX", "LAN"]:
        result = "ne"
    if value in ["FOR", "OUI", "INT", "MEL"]:
        result = "sw"
    if value in ["TAI", "VUE", "VOL", "DER"]:
        result = "se"
    return result


@register.filter(name='modulo_of_four')
def modulo_of_four(value):
    result = False
    if isinstance(value, int):
        result = (value % 4 == 1)
    return result


@register.filter(name='modulo_of_four_is_0')
def modulo_of_four_is_0(value):
    result = False
    if isinstance(value, int):
        result = (value % 4 == 0)
    return result


@register.filter(name='modulo_of_four_is_3')
def modulo_of_four_is_3(value):
    result = False
    if isinstance(value, int):
        result = (value % 4 == 3)
    return result


@register.filter(name='as_attribute_sub_group')
def as_attribute_sub_group(value):
    result = ""
    if value in ["AGI"]:
        result = "Physique"
    if value in ["EMP"]:
        result = "Sensoriel"
    if value in ["APP"]:
        result = "Âme"
    return result


@register.filter(name='off_if_blank')
def hidden_if_blank(value):
    result = ""
    if len(value) == 0:
        result = "off"
    return result

@register.filter(name='genderize')
def genderize(value):
    result = value
    if value.lower() == "droitier":
        result = "Droitière"
    elif value.lower() == "geucher":
        result = "Gauchère"
    return result
