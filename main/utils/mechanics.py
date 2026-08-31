import os
import math
from encodings.base64_codec import base64_encode
from colour import Color

from dragonade import settings

# Mandatory Fonts
FONTSET = [
    "Khand",
    "Fira+Sans+Condensed",
    "Fira+Mono",
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
        "Khand",
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
    {"IDX": 1, "NAME": "Vaisseau", "LINK": "gardiendesreves", "SVG_REF": "_1.svg",     "TEXT": "Le coin du Gardien des Rêves"},
    {"IDX": 2, "NAME": "Sirene", "LINK": "carte", "SVG_REF": "_2.svg", "TEXT": "Aides de jeu"},
    {"IDX": 3, "NAME": "Faucon", "LINK": "piani", "SVG_REF": "_3.svg", "TEXT": "Plans & Cartes"},
    {"IDX": 4, "NAME": "Couronne", "LINK": "stregoneria", "SVG_REF": "_4.svg",     "TEXT": "Sortilèges & Effets Draconiques"},
    {"IDX": 5, "NAME": "Dragon", "LINK": "orologio", "SVG_REF": "_5.svg", "TEXT": "Horloge des Rêves"},
    {"IDX": 6, "NAME": "Epees", "LINK": "appartuses", "SVG_REF": "_6.svg", "TEXT": "Objets du Rêve"},
    {"IDX": 7, "NAME": "Lyre", "LINK": "", "SVG_REF": "_7.svg", "TEXT": ""},
    {"IDX": 8, "NAME": "Serpent", "LINK": "creatures", "SVG_REF": "_8.svg", "TEXT": "Monstres..."},
    {"IDX": 9, "NAME": "Poisson-Acrobate", "LINK": "risorse", "SVG_REF": "_9.svg", "TEXT": "Révélation de Cartes"},
    {"IDX": 10, "NAME": "Araignee", "LINK": "combattimento", "SVG_REF": "_10.svg", "TEXT": "Simulateur de Mêlée"},
    {"IDX": 11, "NAME": "Roseau", "LINK": "autochtons", "SVG_REF": "_11.svg", "TEXT": "La liste des autochtones (PNJs)"},
    {"IDX": 12, "NAME": "ChateauDormant", "LINK": "travellers", "SVG_REF": "_12.svg",  "TEXT": "La liste des voyageurs (PJs)"}
]

MAIN_MENU = [
    {"NAME": "DRAGONADE", "ICON": "fa-bars", "SUB": [
        {"NAME": "Parallaxe", "SUB": [
            {"NAME": "Gardien", "LINK": "gardiendesreves"},
            {"NAME": "Voyageurs", "LINK": "risorse"},
        ]},
        {"NAME": "Rêves", "SUB": [
            {"NAME": "Nouveau Rêve", "LINK": "new_dream"},
            {"NAME": "Campagne: El fuego del Mar", "LINK": "sogno"},
            {"NAME": "Campagne: Le joueur de flute", "LINK": "sogno"},
            {"NAME": "Campagne: La Rose Pourpre", "LINK": "sogno"},
        ]},
        {"NAME": "Personnages", "SUB": [
            {"NAME": "Viaggiatori", "LINK": "viaggiatori_list"},
            {"NAME": "Nativi", "LINK": "nativi_list"},
            {"NAME": "Creature", "LINK": "creature_list"},
        ]},
        {"NAME": "Ressources", "SUB": [
            {"NAME": "Incantessimi", "LINK": "incantessimi_list"},
            {"NAME": "Artefatti", "LINK": "artefatti_list"},
            {"NAME": "Oggetti", "LINK": "oggetti_list"},
        ]},
        {"NAME": "Visuels", "SUB": [
            {"NAME": "Cartes", "LINK": "piani"},
            {"NAME": "Illustrations", "LINK": "flute"},
            {"NAME": "Orologio", "LINK": "orologio"},
        ]},
        {"NAME": "Autre", "SUB": [
            {"NAME": "Tables", "LINK": "carte"},
        ]},
        {"NAME": "Outils", "SUB": [
            {"NAME": "Options On/Off", "ACTION": "showhide", "TARGET": "spare_right", "ID":"options_showhide"},
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


def pre_sim(modeladmin, request, queryset):
    # for item in queryset:
    #     item.pre_sim()
    pass
    short_description = "PreSim"


def fetch_maps():
    map_list = []
    map_path = os.path.join(settings.MEDIA_ROOT, 'maps/')
    # print(map_path)
    id = 1
    for filename in os.listdir(map_path):
        if filename.endswith('.jpg'):
            words = filename.split(".")
            file = map_path + filename
            map_list.append({"id": id, "text": words[0], "file": file})
            id += 1
    return map_list


ZAFF_MATCHES = [('é', 'WeA_'), ('è', 'WeG_'), ('à', 'WaG_'), ('ï', 'WiT_'), ('ë', 'WeT_'), ('ä', 'WaT_'), ('ù', 'WuG_'),
                ('ç', 'WcC_'), ('ô', 'WoC_'), ('ê', 'WeC_'), ('â', 'WaC_'), (' ', 'Wsp_'), ("'", 'Wsq_'), ('"', 'Wdq_')
                ]


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
    h = blake2b(digest_size=5)
    h.update(bytes(str.encode('utf-8')))
    res = h.hexdigest().encode('utf-8')
    return res

def asShortB2B(str):
    from hashlib import blake2b
    h = blake2b(digest_size=3)
    h.update(bytes(str.encode('utf-8')))
    res = h.hexdigest().encode('utf-8')
    return res


def roll(explodes=True, faces=12, whole_details=False):
    def die():
        return math.floor((int.from_bytes(os.urandom(1)) / 256) * faces) + 1

    terms = []
    dice = []
    d12 = die()
    result = d12
    dice.append(d12)
    terms.append(str(d12))
    if explodes:
        if d12 == 1:
            while True:
                more = die()
                result -= more
                terms.append(f"-{more: 2}")
                dice.append(more)
                if more != faces:
                    break
        elif d12 == faces:
            while True:
                more = die()
                result += more
                terms.append(f"+{more: 2}")
                dice.append(more)
                if more != faces:
                    break
    # print(f' ----> d{faces}:{" ".join(terms):10} => {result}')
    if whole_details:
        return result, dice
    return result


class Nougardine:

    def __init__(self, diff):
        self.valid_diffs = [5, 10, 15, 20, 25]
        self.current_diff = 15
        if diff in self.valid_diffs:
            self.current_diff = diff

    def quality(self, die):
        q = ""
        delta = die - self.current_diff
        if delta >= 15:
            q = "Critique"
        elif delta >= 10:
            q = "Significative"
        elif delta >= 5:
            q = "Particulière"
        elif delta >= 0:
            q = "Réussite"
        elif die > math.ceil(self.current_diff / 2):
            q = "Echec"
        elif die > 0:
            q = "Echec Notable"
        else:
            q = "Echec Total"
        return q, self.current_diff, die

    def success(self, die):
        s = False
        delta = die - self.current_diff
        if delta >= 15:
            s = True
        elif delta >= 10:
            s = True
        elif delta >= 5:
            s = True
        elif delta >= 0:
            s = True
        return s

    def margin(self, die):
        q = ""
        delta = die - self.current_diff
        if delta >= 15:
            m = 7
        elif delta >= 10:
            m = 6
        elif delta >= 5:
            m = 5
        elif delta >= 0:
            m = 4
        elif die > math.ceil(self.current_diff / 2):
            m = 3
        elif die > 0:
            m = 2
        else:
            m = 1
        return m


class Severity:
    def __init__(self):
        self.steps = [
            {"milestone": 2, "pdv": 1, "name": "Touche", "Res": 0},
            {"milestone": 4, "pdv": 2, "name": "Eraflure", "Res": 0},
            {"milestone": 7, "pdv": 3, "name": "Estafilade", "Res": 0},
            {"milestone": 10, "pdv": 5, "name": "Taillade", "Res": 5},
            {"milestone": 16, "pdv": 8, "name": "Offense", "Res": 10},
            {"milestone": 20, "pdv": 13, "name": "Meurtrissure", "Res": 15},
            {"milestone": 23, "pdv": 21, "name": "Mutilation", "Res": 20},
            {"milestone": 25, "pdv": 34, "name": "Trauma", "Res": 25},
        ]

    def encaissement(self, die):
        encaissement = {}
        for step in self.steps:
            if die >= step["milestone"]:
                encaissement = step
        return encaissement


class Chaser:
    def __init__(self, json, sep=":"):
        self.json = json
        self.sep = sep

    def reach(self, t):
        debug = False
        if debug:
            print("Searching --> " + t)
        root = self.json
        keys = t.split(self.sep)
        for key in keys:
            if debug:
                print(root)
            root = root[key]
        return root


class Localizer:

    def __init__(self):
        pass

    def loc_from_die(self, die):
        loc = "H"
        ratio = 1
        if die == 12:
            loc = "H"
            ratio = 2
        if die in [9, 10, 11]:
            loc = "C"
        if die in [7, 8]:
            loc = "AS"
        if die in [5, 6]:
            loc = "AW"
        if die in [1, 2]:
            loc = "LS"
        if die in [3, 4]:
            loc = "LW"
        return loc, ratio


class Colorizer:
    def __init__(self):
        self.palette = []
        self.current = 0
        self.randomize(color_count=8)

    def randomize(self, color_count=4):
        a = Color("yellow")
        b = Color("purple")
        self.palette = list(a.range_to(b, color_count))
        palette = []
        for p in self.palette:
            p.saturation = 0.3
            p.luminance = 0.3
            palette.append(p)
        self.palette = palette
        self.current = 0

    def pop(self):
        self.current = (self.current + 1) % len(self.palette)
        return self.palette[self.current]

    @classmethod
    def random_color(cls):
        red = int.from_bytes(os.urandom(1))
        green = int.from_bytes(os.urandom(1))
        blue = int.from_bytes(os.urandom(1))
        c = f'#{red:02x}{green:02x}{blue:02x}'
        return c
