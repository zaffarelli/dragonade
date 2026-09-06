import math
import json

CHARACTER_STATISTICS = {
    "ATTRIBUTES": {
        "DEFAULT": 1,
        "LIST": [
            {"NAME": "AGI", "TEXT": "Agilité", "ORDER": 0},
            {"NAME": "CON", "TEXT": "Constitution", "ORDER": 1},
            {"NAME": "FOR", "TEXT": "Force", "ORDER": 2},
            {"NAME": "TAI", "TEXT": "Taille", "ORDER": 3},
            {"NAME": "EMP", "TEXT": "Empathie", "ORDER": 4},
            {"NAME": "ODG", "TEXT": "Odorat/Goût", "ORDER": 5},
            {"NAME": "OUI", "TEXT": "Ouïe", "ORDER": 6},
            {"NAME": "VUE", "TEXT": "Vue", "ORDER": 7},
            {"NAME": "APP", "TEXT": "Apparence", "ORDER": 8},
            {"NAME": "DEX", "TEXT": "Dextérité", "ORDER": 9},
            {"NAME": "INT", "TEXT": "Intelligence", "ORDER": 10},
            {"NAME": "VOL", "TEXT": "Volonté", "ORDER": 11}
        ]
    },
    "SECONDARIES": {
        "LIST": [
            {"NAME": "TIR", "TEXT": "Tir", "RATIONALE": " (DEX + VUE) / 2", "PARAMS": "DEX VUE",
             "FORMULA": lambda p: math.ceil((p[0] + p[1]) / 2), "ORDER": 0
             },
            {"NAME": "MEL", "TEXT": "Mêlée", "RATIONALE": " (FOR + AGI) / 2", "PARAMS": "FOR AGI",
             "FORMULA": lambda p: math.ceil((p[0] + p[1]) / 2), "ORDER": 1
             },
            {"NAME": "DER", "TEXT": "Dérobade", "RATIONALE": " (12 - TAI + AGI) / 2", "PARAMS": "TAI AGI",
             "FORMULA": lambda p: math.ceil((12 - p[0] + p[1]) / 2), "ORDER": 2
             },
            {"NAME": "LAN", "TEXT": "Lancer", "RATIONALE": " (TIR + FOR) / 2", "PARAMS": "TIR FOR",
             "FORMULA": lambda p: math.ceil((p[0] + p[1]) / 2), "ORDER": 3
             }
        ]
    },
    "MISC": {
        "LIST": [
            {"NAME": "FAB", "TEXT": "Fable", "RATIONALE": " (VUE + FOR + INT) / 3", "PARAMS": "VUE FOR INT",
             "FORMULA": lambda p: round((p[0] + p[1] + p[2]) / 3)
             },
            {"NAME": "VIE", "TEXT": "Points de Vie", "RATIONALE": " CON + TAI", "PARAMS": "CON TAI",
             "FORMULA": lambda p: p[0] + p[1]
             },
            {"NAME": "FAT", "TEXT": "Fatigue", "RATIONALE": " (CON + VOL) / 2", "PARAMS": "CON VOL",
             "FORMULA": lambda p: round((p[0] + p[1]) / 2)
             },
            {"NAME": "IMP", "TEXT": "Impact", "RATIONALE": " ArrondiBas((FOR + TAI) / 4) - 2", "PARAMS": "FOR TAI",
             "FORMULA": lambda p: math.floor((p[0] + p[1]) / 4) - 2
             },
            {"NAME": "SUS", "TEXT": "Sustentation", "RATIONALE": " ArrondiBas((CON + 4) / 4) + 1", "PARAMS": "CON",
             "FORMULA": lambda p: math.floor((p[0] + 4) / 4) + 1
             },
            {"NAME": "RES", "TEXT": "Résilience", "RATIONALE": "ArrondiBas((CON + TAI) / 5)", "PARAMS": "CON TAI",
             "FORMULA": lambda p: math.floor((p[0] + p[1]) / 5)
             },
            {"NAME": "ENC", "TEXT": "Encombrement", "RATIONALE": " (TAI + FOR)  [garder une décimale]", "PARAMS": "TAI CON",
             "FORMULA": lambda p: ((p[0] + p[1]) / 2) * 2
             },
            {"NAME": "SON", "TEXT": "Songe", "RATIONALE": "-"},
            {"NAME": "REV", "TEXT": "Rêve", "RATIONALE": "(SON + FAB)", "PARAMS": "SON FAB", "FORMULA": lambda p: p[0] + p[1]},
        ]
    },
    "FEATURES": {
        "LIST": [
            {"NAME": "height", "TEXT": "Hauteur en centimètres", "COMPUTE": "user_choice", "RATIONALE": "-"},
            {"NAME": "weight", "TEXT": "Poids en kilogrammes", "COMPUTE": "user_choice", "RATIONALE": "-"},
            {"NAME": "age", "TEXT": "Entrée", "RATIONALE": "-"},
            {"NAME": "aka", "TEXT": "Entrée", "RATIONALE": "-"},
            {"NAME": "is_female", "TEXT": "Entrée", "RATIONALE": "-"},
            {"NAME": "is_lefty", "TEXT": "Entrée", "RATIONALE": "-"},
            {"NAME": "gear", "TEXT": "Equipement", "RATIONALE": "-"},
            {"NAME": "spells", "TEXT": "Magie", "RATIONALE": "-"},
            {"NAME": "destiny", "TEXT": "Destinée", "RATIONALE": "-"},
            {"NAME": "entrance", "TEXT": "Entrée", "RATIONALE": "-"},
            {"NAME": "description", "TEXT": "Description", "RATIONALE": "-"},
            {"NAME": "birthhour", "TEXT": "Heure de Naissance", "RATIONALE": "-"}
        ]
    },
    "SKILLS": {
        "WEAPONS": {
            "DEFAULT": -1,
            "NAME": "Martiales",
            "LIST": [
                {"NAME": "WEA_01", "TEXT": "Esquive", "ORDER": 0},
                {"NAME": "WEA_02", "TEXT": "Lutte", "ORDER": 1},
                {"NAME": "WEA_03", "TEXT": "Pugilat", "ORDER": 2},
                {"NAME": "WEA_04", "TEXT": "Arbalètes", "ORDER": 3},
                {"NAME": "WEA_05", "TEXT": "Arcs", "ORDER": 4},
                {"NAME": "WEA_06", "TEXT": "Armes à deux mains", "ORDER": 5},
                {"NAME": "WEA_07", "TEXT": "Armes d'Hast", "ORDER": 6},
                {"NAME": "WEA_08", "TEXT": "Bâtons", "ORDER": 7},
                {"NAME": "WEA_09", "TEXT": "Boucliers", "ORDER": 8},
                {"NAME": "WEA_10", "TEXT": "Fouets", "ORDER": 9},
                {"NAME": "WEA_11", "TEXT": "Frondes", "ORDER": 10},
                {"NAME": "WEA_12", "TEXT": "Hâches", "ORDER": 11},
                {"NAME": "WEA_13", "TEXT": "Javelots", "ORDER": 12},
                {"NAME": "WEA_14", "TEXT": "Lames Courtes", "ORDER": 13},
                {"NAME": "WEA_15", "TEXT": "Lames Longues", "ORDER": 14},
                {"NAME": "WEA_16", "TEXT": "Masses", "ORDER": 15},
                {"NAME": "WEA_17", "TEXT": "Lances", "ORDER": 16},
                {"NAME": "WEA_18", "TEXT": "Poignards", "ORDER": 17},

            ]
        },
        "GENERIC": {
            "DEFAULT": -1,
            "NAME": "Génériques",
            "LIST": [
                {"NAME": "GEN_01", "TEXT": "Artisanat", "ORDER": 0},
                {"NAME": "GEN_02", "TEXT": "Chant", "ORDER": 1},
                {"NAME": "GEN_03", "TEXT": "Concentration", "ORDER": 2},
                {"NAME": "GEN_04", "TEXT": "Course", "ORDER": 3},
                {"NAME": "GEN_05", "TEXT": "Cuisine", "ORDER": 4},
                {"NAME": "GEN_06", "TEXT": "Danse", "ORDER": 5},
                {"NAME": "GEN_07", "TEXT": "Dessin", "ORDER": 6},
                {"NAME": "GEN_08", "TEXT": "Discrétion", "ORDER": 7},
                {"NAME": "GEN_09", "TEXT": "Eloquence", "ORDER": 8},
                {"NAME": "GEN_10", "TEXT": "Escalade", "ORDER": 9},
                {"NAME": "GEN_16", "TEXT": "Pièges", "ORDER": 10},
                {"NAME": "GEN_11", "TEXT": "Saut", "ORDER": 11},
                {"NAME": "GEN_12", "TEXT": "Sculpture", "ORDER": 12},
                {"NAME": "GEN_13", "TEXT": "Séduction", "ORDER": 13},
                {"NAME": "GEN_15", "TEXT": "Tactique", "ORDER": 14},
                {"NAME": "GEN_14", "TEXT": "Vigilance", "ORDER": 15},

            ]
        },
        "PECULIAR": {
            "DEFAULT": -2,
            "NAME": "Particulières",
            "LIST": [
                {"NAME": "PEC_01", "TEXT": "Charpenterie", "ORDER": 0},
                {"NAME": "PEC_02", "TEXT": "Comédie", "ORDER": 1},
                {"NAME": "PEC_03", "TEXT": "Commerce", "ORDER": 2},
                {"NAME": "PEC_04", "TEXT": "Couture", "ORDER": 3},
                {"NAME": "PEC_05", "TEXT": "Déguisement", "ORDER": 4},
                {"NAME": "PEC_06", "TEXT": "Equitation", "ORDER": 5},
                {"NAME": "PEC_07", "TEXT": "Jeu de Mains", "ORDER": 6},
                {"NAME": "PEC_08", "TEXT": "Maçonnerie", "ORDER": 7},
                {"NAME": "PEC_09", "TEXT": "Musique", "ORDER": 8},
                {"NAME": "PEC_10", "TEXT": "Survie en Cité", "ORDER": 9},
                {"NAME": "PEC_11", "TEXT": "Survie dans le Désert", "ORDER": 10},
                {"NAME": "PEC_12", "TEXT": "Survie en Forêt", "ORDER": 11},
                {"NAME": "PEC_13", "TEXT": "Survie dans les Glaces", "ORDER": 12},
                {"NAME": "PEC_14", "TEXT": "Survie dans les Marais", "ORDER": 13},
                {"NAME": "PEC_15", "TEXT": "Survie en Montagnes", "ORDER": 14},
                {"NAME": "PEC_16", "TEXT": "Survie en Sous-sols", "ORDER": 15},

            ]
        },
        "SPECIALIZED": {
            "DEFAULT": -3,
            "NAME": "Spécialisées",
            "LIST": [
                {"NAME": "SPE_01", "TEXT": "Acrobatie", "ORDER": 0},
                {"NAME": "SPE_02", "TEXT": "Jeu", "ORDER": 1},
                {"NAME": "SPE_03", "TEXT": "Jonglerie", "ORDER": 2},
                {"NAME": "SPE_04", "TEXT": "Maroquinerie", "ORDER": 3},
                {"NAME": "SPE_05", "TEXT": "Médecine", "ORDER": 4},
                {"NAME": "SPE_06", "TEXT": "Métallurgie", "ORDER": 5},
                {"NAME": "SPE_07", "TEXT": "Natation", "ORDER": 6},
                {"NAME": "SPE_08", "TEXT": "Navigation", "ORDER": 7},
                {"NAME": "SPE_09", "TEXT": "Orfèvrerie", "ORDER": 8},
                {"NAME": "SPE_10", "TEXT": "Serrurerie", "ORDER": 9}
            ]
        },
        "KNOWLEDGE": {
            "DEFAULT": -4,
            "NAME": "Connaissances",
            "LIST": [
                {"NAME": "KNO_01", "TEXT": "Alchimie", "ORDER": 0},
                {"NAME": "KNO_02", "TEXT": "Animaux", "ORDER": 1},
                {"NAME": "KNO_03", "TEXT": "Architecture", "ORDER": 2},
                {"NAME": "KNO_04", "TEXT": "Astrologie", "ORDER": 3},
                {"NAME": "KNO_05", "TEXT": "Chirurgie", "ORDER": 4},
                {"NAME": "KNO_06", "TEXT": "Ecriture", "ORDER": 5},
                {"NAME": "KNO_07", "TEXT": "Légendes", "ORDER": 6},
                {"NAME": "KNO_08", "TEXT": "Mathématiques", "ORDER": 7},
                {"NAME": "KNO_09", "TEXT": "Plantes", "ORDER": 8},
                {"NAME": "KNO_10", "TEXT": "Stratégie", "ORDER": 9}
            ]
        },
        "DRACONIC": {
            "DEFAULT": -5,
            "NAME": "Draconiques",
            "LIST": [
                {"NAME": "DRA_01", "TEXT": "Contemplatif", "ORDER": 0},
                {"NAME": "DRA_02", "TEXT": "Destructif", "ORDER": 1},
                {"NAME": "DRA_03", "TEXT": "Dynamique", "ORDER": 2},
                {"NAME": "DRA_04", "TEXT": "Génératif", "ORDER": 3},
                {"NAME": "DRA_05", "TEXT": "Mnémonique", "ORDER": 4},
                {"NAME": "DRA_06", "TEXT": "Statique", "ORDER": 5}
            ]
        }
    }
}


def known(dataset_str, value):
    """
        Check for the presence of a value in the LIST.NAME property for each "X:Y" named dataset.
        :returns: string with the dataset name if found, blank otherwise.
    """
    result = ""
    source = CHARACTER_STATISTICS
    verbs = dataset_str.split(":")
    # print(f"#VERBS.... {verbs}")
    for verb in verbs:
        source = source[verb]
    elems = source["LIST"]
    for elem in elems:
        if elem["NAME"] == value.upper():
            # print(f"# Found : {value.upper()}")
            result = dataset_str
            break
    # print(f"#KNOWN.... {result}")
    return result


SHORTCUTS = [
    ["Vue + Vigilance", "VUE", "GEN_14"],
    ["Ouïe + Concentration", "OUI", "GEN_03"],
    ["Empathie + Séduction", "EMP", "GEN_13"],
    ["Dérobade + Esquive", "DER", "WEA_12"],
    ["Volonté + Concentration", "VOL", "GEN_03"],
    ["Rêve + Contemplatif", "REV", "DRA_01"]
]


def skill_cost(skill, value):
    cost = -1
    comment = ""
    for cat in CHARACTER_STATISTICS['SKILLS']:
        for s in CHARACTER_STATISTICS['SKILLS'][cat]["LIST"]:
            d = CHARACTER_STATISTICS['SKILLS'][cat]['DEFAULT']
            if s['NAME'] == skill:
                if value > d:
                    cost = stress_cost(d, value, d)
                    comment = f"- {s['TEXT']:30} [{skill:6}] [Contrainte:{d:3}]: {d:3} => {value:2} = {cost:5}"
                    print(comment)
                    break
    return cost, comment


ATTRIBUTE_CREA = {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 6,
    "7": 8,
    "8": 11,
    "9": 15,
    "10": 21,
    "11": 29,
    "12": 40,
    "13": 55,
    "14": 75,
    "15": 103,
    "16": 141,
    "17": 193,
    "18": 264,
    "19": 361,
    "20": 493
}

TABLES = {  # 0    1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
    "tbDOM": [-10, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
    "tbSUS": [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
    "tbSCO": [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8]
}

QualiteDesActions = [
    {"NAME": "CRITIQUE", "TEXT": "Réussite Critique", "BasePts": 7, "COEF": 4, "formula": lambda x: x + 15},
    {"NAME": "SIGNIFICATIVE", "TEXT": "Réussite Significative", "BasePts": 6, "COEF": 3, "formula": lambda x: x + 10},
    {"NAME": "PARTICULIERE", "TEXT": "Réussite Particulière", "BasePts": 5, "COEF": 2, "formula": lambda x: x + 5},
    {"NAME": "REUSSITE", "TEXT": "Réussite", "BasePts": 4, "COEF": 1, "formula": lambda x: x},
    {"NAME": "ECHEC", "TEXT": "Echec", "BasePts": 3, "COEF": 1, "formula": lambda x: x - 1},
    {"NAME": "NOTABLE", "TEXT": "Echec Notable", "BasePts": 2, "COEF": 0.5, "formula": lambda x: math.ceil(x / 2 - 1)},
    {"NAME": "TOTAL", "TEXT": "Echec Total", "BasePts": 1, "COEF": 0, "formula": lambda x: 0}
]

Difficultes = [
    {"NAME": "TF", "TEXT": "Très facile", "COEF": 1, "VALUE": 5},
    {"NAME": "FA", "TEXT": "Facile", "COEF": 2, "VALUE": 10},
    {"NAME": "NO", "TEXT": "Normale", "COEF": 3, "VALUE": 15},
    {"NAME": "DI", "TEXT": "Difficile", "COEF": 4, "VALUE": 20},
    {"NAME": "TD", "TEXT": "Très Difficile", "COEF": 5, "VALUE": 25}
]

STRESS_COEFF = 3


def action_quality_json():
    table = {
        "title": "Qualité des Actions",
        "cols": [],
        "rows": [],
        "values": [],
        "col_back_header": [],
        "row_back_header": [],
        "options": {"even_odd": True, "cell_widths": [3, 3, 3, 3, 3], "cell_height": 1.5, "row_header_width": 4, "big_values": True}
    }
    cols = []
    rows = []
    values = []
    for q in QualiteDesActions:
        rows.append(q["NAME"])
    for d in Difficultes:
        cols.append(d["TEXT"])
    for q in QualiteDesActions:
        for d in Difficultes:
            values.append(q["formula"](d["VALUE"]))
    cbh = []
    rbh = []
    for q in QualiteDesActions:
        rbh.append(q["BasePts"])
    for d in Difficultes:
        cbh.append(d["COEF"])

    table["cols"] = cols
    table["rows"] = rows
    table["values"] = values
    table["col_back_header"] = cbh
    table["row_back_header"] = rbh
    x = json.dumps(table)
    print(x)
    return x


def stress_cost(v1: int, v2: int, d: int):
    """
    Stress points cost per upgrade
    Example : Generatif (default-5) from -2 up to 4 costs 117 stress pts
    :param v1: actual value (ex: -2)
    :param v2: wanted value (ex: 4)
    :param d: default category value (ex: -5)
    :return: number of pts
    """
    if v1 < d:  # starting value cannot be below default value
        v1 = d
    if v1 > v2:  # final value must be supperior to start value
        v2 = v1 + 1
    step0 = (v1 - d)
    steps = sumorial(v2 - v1)
    return (steps + (v2 - v1) * step0) * STRESS_COEFF


def sumorial(n: int):
    # it factorial with + instead of *...
    if n == 0:
        return 0  # neutral in addition
    else:
        return n + sumorial(n - 1)


def stress_table_json():
    table = {
        "title": "Table de Stress",
        "cols": [-5, -4, -3, -2, -1, 0],
        "rows": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "values": [],
        "options": {"even_odd": True, "cell_widths": [2, 2, 2, 2, 2, 2], "cell_height": 0.8}
    }
    values = []
    for row in table["rows"]:
        for col in table["cols"]:
            if col >= row:
                value = "-"
            else:
                value = f"{(row - col) * STRESS_COEFF}"
            values.append(value)
    table["values"] = values
    return json.dumps(table)


def soak_table_json():
    table = {
        "title": "Table d'Encaissement",
        "cols": ["Blessure"],
        "rows": [24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"column_width": 1, "object_values": True, "cell_widths": [2]}
    }
    values = []
    c = "#FFFFFF"
    for x in table["rows"]:
        if x > 23:
            b = "Critique"
            c = "#EEEEEE"
            w = 2.5
        elif x > 19:
            b = "Grave"
            c = "#DDDDDD"
            w = 2
        elif x > 13:
            b = "Légère"
            c = "#CCCCCC"
            w = 1.5
        else:
            b = "Contusion"
            c = "#BBBBBB"
            w = 1
        values.append({"text": b, "color": c, "width": w})
    table['values'] = values
    return json.dumps(table)


def pdom_table_json():
    table = {
        "title": "Impact",
        "cols": ["IMP"],
        "rows": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"rows_header": "TAI+FOR", "cell_widths": [2], "cell_height": 0.75, "even_odd": True}
    }
    values = []
    for val in table["rows"]:
        value = f"{(math.floor((val) / 4) - 2)}"
        values.append(value)
    table["values"] = values
    return json.dumps(table)


def sus_table_json():
    table = {
        "title": "Sustenance",
        "cols": ["sus"],
        "rows": [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"rows_header": "CON", "cell_widths": [2], "cell_height": 0.5, "even_odd": True}
    }
    values = []
    for val in table["rows"]:
        value = f"{math.floor((val + 4) / 4) + 1}"
        values.append(value)
    table["values"] = values
    return json.dumps(table)


def scon_table_json():
    table = {
        "title": "Résilience",
        "cols": ["RES"],
        "rows": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"rows_header": "CON+TAI", "cell_widths": [2], "cell_height": 0.5, "even_odd": True}
    }
    values = []
    for val in table["rows"]:
        value = f"{math.floor((val) / 5)}"
        values.append(value)
    table["values"] = values
    return json.dumps(table)


def comp_table_json(cat=""):
    table = {
        "title": CHARACTER_STATISTICS["SKILLS"][cat.upper()]["NAME"],
        "cols": ["Compétence"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [4], "cell_height": 1,
                    "rows_header": CHARACTER_STATISTICS["SKILLS"][cat.upper()]["DEFAULT"],
                    "even_odd": True}
    }
    rows = []
    values = []
    for c in CHARACTER_STATISTICS["SKILLS"][cat]["LIST"]:
        rows.append(f"{c['NAME']}")
        values.append(f"{c['TEXT']}")
    table["rows"] = rows
    table["values"] = values
    return json.dumps(table)


def gear_table_json(cat=""):
    title = "Matériel"
    for x in GEAR_CAT:
        if x[0] == cat:
            title = x[1]
            break
    table = {
        "title": f"{title.title()}",
        "cols": ["Equipement", "1M", "2M", "Enc", "Prix"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [6, 1, 1, 1, 2], "cell_format": ["", "plus_dom", "plus_dom_2m", "enc", "sols"], "cell_height": 0.5, "even_odd": True}
    }
    rows = []
    values = []
    from main.models.equipment import Equipment
    for c in Equipment.objects.filter(category=cat, special=False):
        rows.append(f"{c.rid}")
        values.append(f"{c.name}")
        values.append(f"{c.plus_dom}")
        values.append(f"{c.plus_dom_2m}")
        values.append(f"{c.enc}")
        values.append(f"{c.price}")
    table["rows"] = rows
    table["values"] = values
    return json.dumps(table)


def weapon_table_json(cat=""):
    title = "Matériel"
    for x in GEAR_CAT:
        if x[0] == cat:
            title = x[1]
            break
    table = {
        "title": f"{title.title()}",
        "cols": ["Equipement", "Compétence", "1M", "2M", "Res", "Enc", "Prix"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [6, 8, 1, 1, 1, 1, 2], "cell_format": ["left", "left", "center", "", "", ""], "cell_height": 0.5,
                    "even_odd": True}
    }
    rows = []
    values = []
    from main.models.equipment import Equipment
    for c in Equipment.objects.filter(category=cat, special=False):
        rows.append(f"{c.rid}")
        values.append(f"{c.name}")
        values.append(f"{c.related_skill_name}")
        values.append(f"{c.plus_dom}")
        values.append(f"{c.plus_dom_2m}")
        values.append(f"{c.resistance}")
        values.append(f"{c.enc}")
        values.append(f"{c.price}")
    table["rows"] = rows
    table["values"] = values
    return json.dumps(table)


def secondaries_table_json():
    table = {
        "title": f"Secondaires",
        "cols": ["Formule"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [7], "cell_height": 0.7, "even_odd": True, "rows_header": "Attr."}
    }
    rows = []
    values = []
    for c in CHARACTER_STATISTICS["SECONDARIES"]["LIST"]:
        rows.append(f"{c['NAME']}")
        values.append(f"{c['RATIONALE']}")
    table["rows"] = rows
    table["values"] = values
    return json.dumps(table)


def miscellaneous_table_json():
    table = {
        "title": f"Divers",
        "cols": ["Formule"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [7], "cell_height": 0.7, "even_odd": True, "rows_header": "Attr."}
    }
    rows = []
    values = []
    for c in CHARACTER_STATISTICS["MISC"]["LIST"]:
        rows.append(f"{c['NAME']}")
        values.append(f"{c['RATIONALE']}")
    table["rows"] = rows
    table["values"] = values
    return json.dumps(table)


def load_from_file():
    from main.models.equipment import Equipment
    with open('main/utils/equipement.csv') as f:
        lines = f.readlines()
        for line in lines:
            e = Equipment()
            e.name = line
            e.category = '---'
            e.save()
