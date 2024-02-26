import os
from encodings.base64_codec import base64_encode

from dragonade import settings

FONTSET = ["Neucha", "Are+You+Serious", "Fredoka", "Griffy", "Miltonian", "Henny+Penny", "Astloch",
           "Mountains of Christmas", "Emilys Candy", "Mystery Quest", "Smythe", "Marhey", "Wellfleet"]


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def as_rid(str):
    words = str.lower().split(" ")
    list = []
    for word in words:
        w = word \
            .replace('é', 'e') \
            .replace('è', 'e') \
            .replace('ê', 'e') \
            .replace('ë', 'e') \
            .replace(' ', '') \
            .replace('-', '') \
            .replace('+', '') \
            .replace('/', '') \
            .replace('\\', '') \
            .replace('ç', 'c') \
            .replace('à', 'a') \
            .replace('â', 'a') \
            .replace('ä', 'a') \
            .replace('ô', 'o') \
            .replace('ù', 'u') \
            .replace('û', 'u') \
            .replace('ï', 'i') \
            .replace('î', 'i') \
            .replace("'", '') \
            .replace('"', '') \
            .replace('(', '_') \
            .replace(')', '') \
            .replace('[', '_') \
            .replace(']', '') \
            .upper()
        if len(w) > 3:
            list.append(w[:3])
        else:
            list.append(w)
    list.append(f'{len(str):03}')
    return "_".join(list)


MENU_ENTRIES = [
    {"IDX": 1, "NAME": "Vaisseau", "LINK": "gardiendesreves", "SVG_REF": "_1.svg",
     "TEXT": "Le coin du Gardien des Rêves"},
    {"IDX": 2, "NAME": "Sirene", "LINK": "carte", "SVG_REF": "_2.svg", "TEXT": "Aides de jeu"},
    {"IDX": 3, "NAME": "Faucon", "LINK": "piani", "SVG_REF": "_3.svg", "TEXT": "Plans & Cartes"},
    {"IDX": 4, "NAME": "Couronne", "LINK": "", "SVG_REF": "_4.svg", "TEXT": ""},
    {"IDX": 5, "NAME": "Dragon", "LINK": "orologio", "SVG_REF": "_5.svg", "TEXT": "Retour au Portail..."},
    {"IDX": 6, "NAME": "Epees", "LINK": "appartus", "SVG_REF": "_6.svg", "TEXT": "Objets du Rêve"},
    {"IDX": 7, "NAME": "Lyre", "LINK": "draconis_artes", "SVG_REF": "_7.svg", "TEXT": "Arts Draconiques..."},
    {"IDX": 8, "NAME": "Serpent", "LINK": "", "SVG_REF": "_8.svg", "TEXT": "Monstres..."},
    {"IDX": 9, "NAME": "Poisson-Acrobate", "LINK": "risorse", "SVG_REF": "_9.svg", "TEXT": "Révélation de Cartes"},
    {"IDX": 10, "NAME": "Araignee", "LINK": "", "SVG_REF": "_10.svg", "TEXT": "Références & Règles..."},
    {"IDX": 11, "NAME": "Roseau", "LINK": "personae_a", "SVG_REF": "_11.svg",
     "TEXT": "La liste des autochtones (PNJs)"},
    {"IDX": 12, "NAME": "ChateauDormant", "LINK": "personae_t", "SVG_REF": "_12.svg",
     "TEXT": "La liste des voyageurs (PJs)"}
]


def refix(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    short_description = "Refix"


def fetch_maps():
    map_list = []
    map_path = os.path.join(settings.MEDIA_ROOT, 'maps/')
    print(map_path)
    id = 1
    for filename in os.listdir(map_path):
        if filename.endswith('.jpg'):
            words = filename.split(".")
            file = map_path + filename
            map_list.append({"id": id, "text": words[0], "file": file})
            id += 1
    return map_list


ZAFF_MATCHES = [('é', 'WeA_'), ('é', 'WeG_'), ('à', 'WeG_'), ('ï', 'WiT_'), ('ë', 'WeT_'), ('ä', 'WaT_'), ('ù', 'WuG_'),
                ('ç', 'WcC_'), ('ô', 'WoC_'), ('ê', 'WeC_'), ('â', 'WaC_'), (' ', 'Wsp_'), ("'", 'Wsq_'), ('"', 'Wdq_')]


def zaff_encode(str):
    zstr = str
    for m in ZAFF_MATCHES:
        zstr = zstr.replace(m[0], m[1])
    return zstr


def zaff_decode(zstr):
    str = zstr
    for m in ZAFF_MATCHES:
        str = str.replace(m[1], m[0])
    return str
