from django import template
register = template.Library()


@register.filter(name='colorize_val')
def colorize_val(value):
    str = value
    if isinstance(value, int):
        cols = [
            "#f04080",
            "#e04010",
            "#d04020",
            "#c06030",
            "#b06040",
            "#a06050",
            "#908060",
            "#808070",
            "#708080",
            "#60a090",
            "#50a0a0",
            "#40a0b0",
            "#30c0c0",
            "#20c0d0",
            "#10c0e0",
            "#00e0f0"
        ]
        if value > 10:
            idx = 15
        else:
            idx = value +5

        str = f'<span style="color:{cols[idx]};">{value}</span>'

        # if value >= 10:
        #     str = f'<span style="color:cyan;">{value}</span>'
        # elif value >= 7:
        #     str = f'<span style="color:darkcyan;">{value}</span>'
        # elif value >= 5:
        #     str = f'<span style="color:lime;">{value}</span>'
        # elif value >= 3:
        #     str = f'<span style="color:yellowgreen;">{value}</span>'
        # elif value > 0:
        #     str = f'<span style="color:#80f080;">{value}</span>'
        # elif value == 0:
        #     str = f'<span style="color:#808080;">{value}</span>'
        # elif value >= -2:
        #     str = f'<span style="color:#808080;">{value}</span>'
        # elif value >= -3:
        #     str = f'<span style="color:#808080;">{value}</span>'
        # elif value >= -5:
        #     str = f'<span style="color:maroon;">{value}</span>'
    return str


@register.filter(name='signed')
def signed(value):
    str = value
    if isinstance(value, int):
        if value > 0:
            str = f"+{value}"
        else:
            str = f"{value}"
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
            str = f'static/main/svg/2026/sd_{value}.svg'
    return str


@register.filter(name='as_hour')
def as_hour(value):
    str = ""
    if isinstance(value, int):
        vals = ["Vaisseau", "Sirène", "Faucon", "Couronne", "Dragon", "Epées", "Lyre", "Serpent", "Poisson-Acrobate",
                "Araignée", "Roseau", "Chateau-Dormant"]
        if value > 0:
            str = vals[value - 1]
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


@register.filter(name='lefty')
def lefty(value):
    if value == "D":
        result = "Droitier"
    else:
        result = "Gaucher"
    return result


@register.filter(name='genderize')
def genderize(value):
    if value == "M":
        result = "Masculin"
    else:
        result = "Féminin"
    return result


def svg_item(x):
    # print(x)
    y = "generique" if x.lower() == "générique" else x
    return f'<span class="" title="{x}" style="display:inline-block;">' \
           f'<img src="static/main/svg/2026/{y}.svg" style="display:inline-block; width:100px;">' \
           f'</span>'


@register.filter(name='as_category')
def as_category(value):
    ''' used for simple symbols without prefix
    '''
    result = f'blank'
    if isinstance(value, str):
        v = value
        if len(v)>0:
            result = f'{v}'
    return svg_item(result.lower())

@register.filter(name='as_ground_charge')
def as_ground_charge(value):
    result = f'blank'
    if isinstance(value, int):
        v = value
    else:
        v = 0
    if v > 0:
        result = f"tm_{v}"
    return svg_item(result)


@register.filter(name='as_hour_charge')
def as_hour_charge(value):
    result = f'blank'
    if isinstance(value, int):
        v = value
    else:
        v = 0
    if v > 0:
        result = f'sd_{v}'
    return svg_item(result)


@register.filter(name='as_emanation_charge')
def as_emanation_charge(value):
    result = f'blank'
    if isinstance(value, int):
        v = value
    else:
        v = 0
    if v > 0:
        result = f'ed_{v}'
    return svg_item(result)


@register.filter(name='as_consistency_charge')
def as_consistency_charge(value):
    result = f'blank'
    if isinstance(value, int):
        v = value
    else:
        v = 0
    if v > 0:
        result = f'cd_{v}'
    return svg_item(result)


@register.filter(name='as_elemental_charge')
def as_elemental_charge(value):
    result = f'blank'
    if isinstance(value, int):
        v = value
    else:
        v = 0
    if v > 0:
        result = f'ld_{v}'
    return svg_item(result)


@register.filter(name='encoded_z')
def encoded_z(value):
    from main.utils.mechanics import zaff_encode
    # import base64
    # import html
    # val = str(value)
    # x = base64.b64encode(bytes(val, 'utf-8'))
    # print("x",str(x))
    # y = str(x).replace("b'", "").replace("'", "")
    # # print(value,y,type(x))
    res = zaff_encode(str(value))
    return res


@register.filter(name='decoded_z')
def decoded_z(value):
    from main.utils.mechanics import zaff_decode
    from main.utils.mechanics import zaff_encode
    # import base64
    # import html
    # val = str(value)
    # x = base64.b64encode(bytes(val, 'utf-8'))
    # print("x",str(x))
    # y = str(x).replace("b'", "").replace("'", "")
    # # print(value,y,type(x))
    res = zaff_decode(str(value))
    return res


@register.filter(name='maxed_length')
def maxed_length(value):
    max = 20
    s = str(value)
    if len(s) >= max:
        result = s[:(max - 3)] + "..."
    else:
        result = s
    return result


@register.filter(name='acro')
def acro(value):
    max = 3
    s = str(value)
    if len(s) >= max:
        result = s[:(max)]
    else:
        result = s
    return result.upper()


@register.filter(name='as_stack_list')
def as_stack_list(value):
    if type(value).__name__ == "str":
        items = value.split(" ")
    else:
        items = value
    str = ""
    for item in items:
        str += f"<span class='gearit' item='{item}'>{item}</span> "
    return str


@register.filter(name='as_id')
def as_id(value):
    str = value
    if isinstance(value, int):
        str = f"{value:03}"
    return str


@register.filter(name='as_grav')
def as_grav(value):
    str = value
    niveaux = ["min", "mod", "maj", "gra", "ser"]
    if isinstance(value, int):
        str = "<div class='grav'>"
        for n in niveaux:
            str += f'<span class="{n}">'
            for s in range(value):
                str += f'<i class="fas fa-circle"></i>'
            str += f'</span>'
        str += "</div>"
    return str


@register.filter(name='as_teamcol')
def as_teamcol(value):
    str = f'<div class="teamcol" style="background:{value}">&nbsp;</div>'
    return str


@register.filter(name='as_avoidance')
def as_avoidance(value):
    txt = ""
    if value == "A":
        txt = "Action d'Arme"
    elif value == "E":
        txt = "Esquive"
    elif value == "B":
        txt = "Parade au Bouclier"
    elif value == "R":
        txt = "Action de Rapidité"
    elif value == "":
        txt = "(passif)"
    str = f'<div class="avoidance {value}">{txt}</div>'
    return str




@register.filter(name='render_text')
def render_text(value):
    result = f'N/A'
    if isinstance(value, str):
        v = value.split("§")
        result = "<br/>".join(v)
    return result



@register.filter(name='as_bool')
def as_bool(value):
    if value in [True, "true", "1", 1, "on", "True"]:
        str = "<i class='fa fa-check-circle' style='color:#209020;'></i>"
    else:
        str = "<i class='fa fa-times-circle' style='color:#903030;'></i>"
    return str


@register.filter(name='as_filter_value')
def as_filter_value(value):
    result = value
    if isinstance(value,bool):
        result = "true" if value else "false"
    return result

@register.filter(name='as_doma')
def as_doma(value):
    result = "-"
    if value == 1:
        result = "1 (d4)"
    elif value == 2:
        result = "2 (d6)"
    elif value == 3:
        result = "3 (d8)"
    elif value == 4:
        result = "4 (d10)"
    elif value == 5:
        result = "5 (d12)"
    elif value == 6:
        result = "6 (d20)"
    return result

@register.filter(name='as_protection')
def as_protection(value):
    from django.template.loader import get_template
    covers = value.split(" ")
    x = {}
    for cover in covers:
        parts = cover.split("-")
        x[parts[0]] = int(parts[1])
    template = get_template('main/roster/roster_armor_map.html')
    image = template.render(x, None)
    return image


@register.filter(name='as_money')
def as_money(value):
    import math
    sols = math.floor(value)
    deniers = math.floor((value - sols)*100)
    s = ""
    if sols > 0:
        s += f"{sols} sols "
    if deniers > 0:
        s += f"{deniers} deniers "
    return s
