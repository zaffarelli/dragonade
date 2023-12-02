from django.conf import settings
from main.utils.mechanics import MENU_ENTRIES


def commons(request):
    context = {"version": settings.VERSION, "menu_entries": MENU_ENTRIES}
    return context
