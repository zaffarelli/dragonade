FONTSET = ['Quicksand', 'Fredoka', 'Neucha', 'Syne+Mono', 'Abel', 'Satisfy', 'Acme', 'Roboto', 'Hubballi', 'Gruppo']


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


MENU_ENTRIES = [
    {"IDX": 1, "NAME": "Vaisseau", "LINK": "", "SVG_REF": "_1.svg", "TEXT": ""},
    {"IDX": 2, "NAME": "Sirène", "LINK": "", "SVG_REF": "_2.svg", "TEXT": ""},
    {"IDX": 3, "NAME": "Faucon", "LINK": "", "SVG_REF": "_3.svg", "TEXT": ""},
    {"IDX": 4, "NAME": "Couronne", "LINK": "", "SVG_REF": "_4.svg", "TEXT": "La liste des voyageurs (PJs)"},
    {"IDX": 5, "NAME": "Dragon", "LINK": "index", "SVG_REF": "_5.svg", "TEXT": "Retour au Portail..."},
    {"IDX": 6, "NAME": "Epées", "LINK": "", "SVG_REF": "_6.svg", "TEXT": "Références & Règles..."},
    {"IDX": 7, "NAME": "Lyre", "LINK": "", "SVG_REF": "_7.svg", "TEXT": "Magie Draconique..."},
    {"IDX": 8, "NAME": "Serpent", "LINK": "", "SVG_REF": "_8.svg", "TEXT": "Monstres..."},
    {"IDX": 9, "NAME": "Poisson-Acrobate", "LINK": "", "SVG_REF": "_9.svg", "TEXT": ""},
    {"IDX": 10, "NAME": "Araignée", "LINK": "", "SVG_REF": "_10.svg", "TEXT": ""},
    {"IDX": 11, "NAME": "Roseau", "LINK": "autochtons", "SVG_REF": "_11.svg", "TEXT": "La liste des autochtones (PNJs)"},
    {"IDX": 12, "NAME": "Chateau-Dormant", "LINK": "", "SVG_REF": "_12.svg", "TEXT": ""}
]
