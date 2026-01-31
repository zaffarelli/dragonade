import os
from encodings.base64_codec import base64_encode

from dragonade import settings

# Mandatory Fonts
FONTSET = [
    "Neucha",
    "Are+You+Serious",
    "Smythe",
    "Kanit",
    "Grenze+Gotisch",
    "Wellfleet",
    "Roboto",
    "Roboto+Mono",
    "Roboto+Flex",
    "Sansation",
    "Pirata+One"
]
# Testing (Transfert to the previous one if valid)
if settings.DEBUG == False:
    FONTSET += [
        "Emilys Candy",
        "Acme",
        "Protest Revolution",
        "Henny+Penny",
        "Mystery Quest",
        "Miltonian",
        "Marhey",
        "Griffy",
        "Grenze",
        "Mountains of Christmas",
        "Astloch",
        "Fredoka",
        "Jolly+Lodger",
        "Pirata One",
        "Sono",
    ]


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def as_rid(str):
    str_n_free = str.replace("\n", '')
    words = str_n_free.lower().split(" ")
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
            .replace('ö', 'o') \
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
    # {"IDX": 1, "NAME": "Vaisseau", "LINK": "gardiendesreves", "SVG_REF": "_1.svg",     "TEXT": "Le coin du Gardien des Rêves"},
    # {"IDX": 2, "NAME": "Sirene", "LINK": "carte", "SVG_REF": "_2.svg", "TEXT": "Aides de jeu"},
    # {"IDX": 3, "NAME": "Faucon", "LINK": "piani", "SVG_REF": "_3.svg", "TEXT": "Plans & Cartes"},
    # {"IDX": 4, "NAME": "Couronne", "LINK": "stregoneria", "SVG_REF": "_4.svg",     "TEXT": "Sortilèges & Effets Draconiques"},
    # {"IDX": 5, "NAME": "Dragon", "LINK": "orologio", "SVG_REF": "_5.svg", "TEXT": "Horloge des Rêves"},
    # {"IDX": 6, "NAME": "Epees", "LINK": "appartuses", "SVG_REF": "_6.svg", "TEXT": "Objets du Rêve"},
    # {"IDX": 7, "NAME": "Lyre", "LINK": "", "SVG_REF": "_7.svg", "TEXT": ""},
    # {"IDX": 8, "NAME": "Serpent", "LINK": "creatures", "SVG_REF": "_8.svg", "TEXT": "Monstres..."},
    # {"IDX": 9, "NAME": "Poisson-Acrobate", "LINK": "risorse", "SVG_REF": "_9.svg", "TEXT": "Révélation de Cartes"},
    # {"IDX": 10, "NAME": "Araignee", "LINK": "combattimento", "SVG_REF": "_10.svg", "TEXT": "Simulateur de Mêlée"},
    # {"IDX": 11, "NAME": "Roseau", "LINK": "autochtons", "SVG_REF": "_11.svg", "TEXT": "La liste des autochtones (PNJs)"},
    # {"IDX": 12, "NAME": "ChateauDormant", "LINK": "travellers", "SVG_REF": "_12.svg",  "TEXT": "La liste des voyageurs (PJs)"}
]

MAIN_MENU = [
    {"NAME": "DRAGONADE", "ICON": "fa-bars", "SUB": [
        {"NAME": "Parallaxe", "SUB": [
            {"NAME": "Mise en place (Gardien)", "LINK": "gardiendesreves"},
            {"NAME": "Révélation (Voyageurs)", "LINK": "risorse"},
        ]},
        {"NAME": "Artefacts", "LINK": "appartuses"},
        {"NAME": "Magie Draconique", "SUB":[
            {"NAME": "Liste", "LINK": "stregoneria"},
            {"NAME": "Nouveau sort", "LINK": "new_spell"},
        ]},
        {"NAME": "Rêves", "SUB": [
            {"NAME": "Nouveau Rêve", "LINK": "new_dream"},
            {"NAME": "Campagne: El fuego del Mar", "LINK": "combattimento"},
            {"NAME": "Campagne: Le joueur de flute", "LINK": "combattimento"},
            {"NAME": "Orologio", "LINK": "orologio"},
        ]},
        {"NAME": "Créatures", "SUB": [
            {"NAME": "Statistiques", "LINK": "statistics"},
            {"NAME": "Listes...", "SUB": [
                {"NAME": "Liste des monstres", "LINK": "creatures"},
                {"NAME": "Liste des autochtones", "LINK": "autochtons"},
                {"NAME": "Liste des voyageurs", "LINK": "travellers"},
            ]},
            {"NAME": "Nouveau...", "SUB": [
                {"NAME": "Nouveau monstre", "LINK": "new_creature"},
                {"NAME": "Nouvel autochtone", "LINK": "new_autochton"},
                {"NAME": "Nouveau voyageur", "LINK": "new_traveller"},
            ]},
        ]},

        {"NAME": "Visuels", "SUB": [
            {"NAME": "Cartes", "LINK": "piani"},
            {"NAME": "Illustrations", "LINK": "flute"},
        ]},
        {"NAME": "Ressources", "SUB": [
            {"NAME": "Tables", "LINK": "carte"},
        ]},
        {"NAME": "Outils", "SUB": [
            {"NAME": "Options On/Off", "ACTION": "showhide", "TARGET": "spare_right"},
            {"NAME": "Simulateurs", "SUB": [
                {"NAME": "Mêlée", "LINK": "combattimento"},
            ]},
        ]}
    ]}
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


def random_term(length=6):
    import secrets
    str = ""
    opts = "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9"
    options = opts.split(" ")
    if length > 0:
        for l in range(length):
            str += secrets.choice(options)
    return str


def asB2B(str):
    from hashlib import blake2b
    h = blake2b(digest_size=8)
    h.update(bytes(str.encode('utf-8')))
    res = h.hexdigest().encode('utf-8')
    return res
