from django import template

register = template.Library()


@register.filter(name='colorize_val')
def colorize_val(value):
    str = value
    if isinstance(value, int):
        if value >= 10:
            str = f'<span style="color:orangered;">{value}</span>'
        elif value >= 7:
            str = f'<span style="color:yellow;">{value}</span>'
    return str
