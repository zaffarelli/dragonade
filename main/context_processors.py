from django.conf import settings
from main.utils.mechanics import MENU_ENTRIES


def commons(request):
    from main.models.sogni import Sogno
    sogno_acro = "DEF"
    sogno_txt  = "FICS 11"
    # sogni = Sogno.objects.filter(current=True)
    # if len(sogni)>0:
    #     sogno = sogni.first()
    #     sogno_acro = sogno.acronym
    #     sogno_txt  = sogno.title
    context = {
        "version": settings.VERSION,
        "menu_entries": MENU_ENTRIES,
        "sogno_acro":sogno_acro,
        "sogno_txt": sogno_txt,
    }
    return context