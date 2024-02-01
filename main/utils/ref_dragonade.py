import math
import json

CHARACTER_STATISTICS = {
    "ATTRIBUTES": {
        "DEFAULT": 3,
        "LIST": [
            {"NAME": "AGI", "TEXT": "Agilité"},
            {"NAME": "CON", "TEXT": "Constitution"},
            {"NAME": "FOR", "TEXT": "Force"},
            {"NAME": "TAI", "TEXT": "Taille"},
            {"NAME": "EMP", "TEXT": "Empathie"},
            {"NAME": "ODG", "TEXT": "Odorat/Goût"},
            {"NAME": "OUI", "TEXT": "Ouïe"},
            {"NAME": "VUE", "TEXT": "Vue"},
            {"NAME": "APP", "TEXT": "Apparence"},
            {"NAME": "DEX", "TEXT": "Dextérité"},
            {"NAME": "INT", "TEXT": "Intelligence"},
            {"NAME": "VOL", "TEXT": "Volonté"}
        ],
        "KNOWN": ["AGI","CON","FOR","TAI","EMP","ODG","OUI", "VUE","APP","DEX","INT","VOL"]
        
    },
    "SECONDARIES": { 
        "LIST":[
            {"NAME": "TIR", "TEXT": "Tir", "COMPUTE": "basic_mean,DEX;VUE", "RATIONALE": " (DEX + VUE) / 2"},
            {"NAME": "MEL", "TEXT": "Mêlée", "COMPUTE": "basic_mean,FOR;AGI", "RATIONALE": " (FOR + AGI) / 2"},
            {"NAME": "DER", "TEXT": "Dérobade", "COMPUTE": "dero_mean,TAI;AGI", "RATIONALE": " (12 - TAI + AGI) / 2"},
            {"NAME": "LAN", "TEXT": "Lancer", "COMPUTE": "basic_mean,TIR;FOR", "RATIONALE": " (TIR + FOR) / 2"}
        ],
        "KNOWN": ["DER","LAN","MEL","TIR"]
    },
    "MISC": {
        "LIST":[
            {"NAME": "FAB", "TEXT": "Rêve", "COMPUTE": "basic_mean,CON;EMP;APP", "RATIONALE": " (CON + EMP + APP) / 3"},
            {"NAME": "VIE", "TEXT": "Points de Vie", "COMPUTE": "basic_sum,CON;TAI", "RATIONALE": " CON + TAI"},
            {"NAME": "FAT", "TEXT": "Fatigue", "COMPUTE": "basic_mean,CON;VOL", "RATIONALE": " (CON + VOL) / 2"},
            {"NAME": "DOM", "TEXT": "+dom", "COMPUTE": "from_table_mean,TAI;FOR,tbDOM","RATIONALE": " ArrondiBas((FOR + 2) / 3) - 2"},
            {"NAME": "SUS", "TEXT": "Sustentation", "COMPUTE": "from_table_mean,TAI,tbSUS","RATIONALE": " ArrondiBas((CON + 4) / 4) + 1"},
            {"NAME": "SCO", "TEXT": "Seuil Con", "COMPUTE": "from_table_mean,CON,tbSCO","RATIONALE": "ArrondiBas((CON + 3) / 3) + 1"},
            {"NAME": "ENC", "TEXT": "Encombrement", "COMPUTE": "precise_mean,TAI,FOR","RATIONALE": " (TAI + FOR)  [garder une décimale]"},
            {"NAME": "SON", "TEXT": "Songe", "COMPUTE": "user_choice", "RATIONALE":"-"},
            {"NAME": "REV", "TEXT": "Fable", "COMPUTE": "user_choice", "RATIONALE":"-"},
            {"NAME": "entrance", "TEXT": "Entrée", "COMPUTE": "user_choice", "RATIONALE":"-"}
        ],
        "KNOWN":["FAB","VIE","FAT","DOM","SUS","SCO","ENC","SON","REV","entrance"]
    },
    "FEATURES": {
        "LIST":[
            {"NAME": "HEIGHT", "TEXT": "Hauteur en centimètres", "COMPUTE": "user_choice", "RATIONALE":"-"},
            {"NAME": "WEIGHT", "TEXT": "Poids en kilogrammes", "COMPUTE": "user_choice", "RATIONALE":"-"}
        ],
        "KNOWN":
            ["HEIGHT","WEIGHT"]
    },

    "SKILLS": {
        "WEAPONS": {
            "DEFAULT": 0,
            "NAME": "Martiales",
            "LIST": [
                {"NAME": "WEA_01", "TEXT": "Arbalète"},
                {"NAME": "WEA_02", "TEXT": "Arc"},
                {"NAME": "WEA_03", "TEXT": "Bâton"},
                {"NAME": "WEA_04", "TEXT": "Bouclier Léger"},
                {"NAME": "WEA_05", "TEXT": "Bouclier Moyen"},
                {"NAME": "WEA_06", "TEXT": "Bouclier Lourd"},
                {"NAME": "WEA_07", "TEXT": "Corps-à-corps"},
                {"NAME": "WEA_08", "TEXT": "Dague"},
                {"NAME": "WEA_09", "TEXT": "Double Dragonne"},
                {"NAME": "WEA_10", "TEXT": "Dragonne"},
                {"NAME": "WEA_11", "TEXT": "Esparlongue"},
                {"NAME": "WEA_12", "TEXT": "Esquive"},
                {"NAME": "WEA_13", "TEXT": "Epée Bâtarde"},
                {"NAME": "WEA_14", "TEXT": "Epée Cyane"},
                {"NAME": "WEA_15", "TEXT": "Epée Gnome"},
                {"NAME": "WEA_16", "TEXT": "Epée Sorde"},
                {"NAME": "WEA_17", "TEXT": "Fléau Léger"},
                {"NAME": "WEA_18", "TEXT": "Fléau Lourd"},
                {"NAME": "WEA_19", "TEXT": "Fouet"},
                {"NAME": "WEA_20", "TEXT": "Fronde"},
                {"NAME": "WEA_21", "TEXT": "Gourdin"},
                {"NAME": "WEA_22", "TEXT": "Grande Hache"},
                {"NAME": "WEA_23", "TEXT": "Hache de Bataille"},
                {"NAME": "WEA_24", "TEXT": "Hachette"},
                {"NAME": "WEA_25", "TEXT": "Arme d'Hast"},
                {"NAME": "WEA_26", "TEXT": "Javeline"},
                {"NAME": "WEA_27", "TEXT": "Javelot"},
                {"NAME": "WEA_28", "TEXT": "Lance courte"},
                {"NAME": "WEA_29", "TEXT": "Massette"},
                {"NAME": "WEA_30", "TEXT": "Masse Lourde"},
                {"NAME": "WEA_31", "TEXT": "Pugilat"}
            ],
            "KNOWN": [
                "WEA_01","WEA_02","WEA_03","WEA_04","WEA_05","WEA_06","WEA_07","WEA_08","WEA_09","WEA_10",
                "WEA_11","WEA_12","WEA_13","WEA_14","WEA_15","WEA_16","WEA_17","WEA_18","WEA_19","WEA_20",
                "WEA_21","WEA_22","WEA_23","WEA_24","WEA_25","WEA_26","WEA_27","WEA_28","WEA_29","WEA_30",
                "WEA_31"
            ]               
        },
        "GENERIC": {
            "DEFAULT": -1,
            "NAME": "Génériques",
            "LIST": [
                {"NAME": "GEN_01", "TEXT": "Bricolage"},
                {"NAME": "GEN_02", "TEXT": "Chant"},
                {"NAME": "GEN_03", "TEXT": "Concentration"},
                {"NAME": "GEN_04", "TEXT": "Course"},
                {"NAME": "GEN_05", "TEXT": "Cuisine"},
                {"NAME": "GEN_06", "TEXT": "Danse"},
                {"NAME": "GEN_07", "TEXT": "Dessin"},
                {"NAME": "GEN_08", "TEXT": "Discrétion"},
                {"NAME": "GEN_09", "TEXT": "Eloquence"},
                {"NAME": "GEN_10", "TEXT": "Escalade"},
                {"NAME": "GEN_11", "TEXT": "Saut"},
                {"NAME": "GEN_12", "TEXT": "Sculpture"},
                {"NAME": "GEN_13", "TEXT": "Séduction"},
                {"NAME": "GEN_14", "TEXT": "Vigilance"}
            ], 
            "KNOWN": [
                "GEN_01","GEN_02","GEN_03","GEN_04","GEN_05","GEN_06","GEN_07","GEN_08","GEN_09","GEN_10",
                "GEN_11","GEN_12","GEN_13","GEN_14"
            ]   
        },
        "PECULIAR": {
            "DEFAULT": -2,
            "NAME": "Particulières",
            "LIST": [
                {"NAME": "PEC_01", "TEXT": "Charpenterie"},
                {"NAME": "PEC_02", "TEXT": "Comédie"},
                {"NAME": "PEC_03", "TEXT": "Commerce"},
                {"NAME": "PEC_04", "TEXT": "Couture"},
                {"NAME": "PEC_05", "TEXT": "Equitation"},
                {"NAME": "PEC_06", "TEXT": "Maçonnerie"},
                {"NAME": "PEC_07", "TEXT": "Musique"},
                {"NAME": "PEC_08", "TEXT": "Pickpocket"},
                {"NAME": "PEC_09", "TEXT": "Survie (Cité)"},
                {"NAME": "PEC_10", "TEXT": "Survie (Désert)"},
                {"NAME": "PEC_11", "TEXT": "Survie (Extérieur)"},
                {"NAME": "PEC_12", "TEXT": "Survie (Forêt)"},
                {"NAME": "PEC_13", "TEXT": "Survie (Glaces)"},
                {"NAME": "PEC_14", "TEXT": "Survie (Marais)"},
                {"NAME": "PEC_15", "TEXT": "Survie (Montagne)"},
                {"NAME": "PEC_16", "TEXT": "Survie (Sous-Sol)"},
                {"NAME": "PEC_17", "TEXT": "Travestissement"}
            ],
            "KNOWN": [
                "PEC_01", "PEC_02", "PEC_03", "PEC_04", "PEC_05", "PEC_06", "PEC_07", "PEC_08", "PEC_09", "PEC_10",
                "PEC_11", "PEC_12", "PEC_13", "PEC_14", "PEC_15", "PEC_16", "PEC_17"
            ]
        },
        "SPECIALIZED": {
            "DEFAULT": -3,
            "NAME": "Spécialisées",
            "LIST": [
                {"NAME": "SPE_01", "TEXT": "Acrobatie"},
                {"NAME": "SPE_02", "TEXT": "Chirurgie"},
                {"NAME": "SPE_03", "TEXT": "Jeu"},
                {"NAME": "SPE_04", "TEXT": "Jonglerie"},
                {"NAME": "SPE_05", "TEXT": "Maroquinerie"},
                {"NAME": "SPE_06", "TEXT": "Métallurgie"},
                {"NAME": "SPE_07", "TEXT": "Natation"},
                {"NAME": "SPE_08", "TEXT": "Navigation"},
                {"NAME": "SPE_09", "TEXT": "Orfèvrerie"},
                {"NAME": "SPE_10", "TEXT": "Serrurerie"}
            ],
            "KNOWN": [
                "SPE_01", "SPE_02", "SPE_03", "SPE_04", "SPE_05", "SPE_06", "SPE_07", "SPE_08", "SPE_09", "SPE_10"
            ]
        },
        "KNOWLEDGE": {
            "DEFAULT": -4,
            "NAME": "Connaissances",
            "LIST": [
                {"NAME": "KNO_01", "TEXT": "Alchimie"},
                {"NAME": "KNO_02", "TEXT": "Architecture"},
                {"NAME": "KNO_03", "TEXT": "Astrologie"},
                {"NAME": "KNO_05", "TEXT": "Botanique"},
                {"NAME": "KNO_06", "TEXT": "Ecriture"},
                {"NAME": "KNO_07", "TEXT": "Légendes"},
                {"NAME": "KNO_08", "TEXT": "Mathématiques"},
                {"NAME": "KNO_09", "TEXT": "Médecine"},
                {"NAME": "KNO_10", "TEXT": "Zoologie"}
            ],
            "KNOWN": [
                "KNO_01", "KNO_02", "KNO_03", "KNO_04", "KNO_05", "KNO_06", "KNO_07", "KNO_08", "KNO_09", "KNO_10"
            ]
        },
        "DRACONIC": {
            "DEFAULT": -5,
            "NAME": "Draconiques",
            "LIST": [
                {"NAME": "DRA_01", "TEXT": "Contemplatif"},
                {"NAME": "DRA_02", "TEXT": "Destructif"},
                {"NAME": "DRA_03", "TEXT": "Dynamique"},
                {"NAME": "DRA_04", "TEXT": "Génératif"},
                {"NAME": "DRA_05", "TEXT": "Mnémonique"},
                {"NAME": "DRA_06", "TEXT": "Statique"}
            ],
            "KNOWN": [
                "DRA_01", "DRA_02", "DRA_03", "DRA_04", "DRA_05", "DRA_06"
            ]
        }
    }
}


SHORTCUTS = [
    ["Vue + Vigilance","VUE","GEN_14"],
    ["Ouïe + Concentration","OUI","GEN_03"],
    ["Empathie + Séduction","EMP","GEN_13"],
    ["Dérobade + Esquive","DER","WEA_12"],
    ["Volonté + Concentration","VOL","GEN_03"],
    ["Rêve + Contemplatif","REV","DRA_01"]
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
                    comment = f"- {skill:6} [{d:3}]: {d:3} => {value:2} = {cost:5}"
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
    {"NAME": "CRITIQUE", "TEXT": "Réussite Critique", "BasePts": 4, "COEF": 4, "formula": lambda x: x * 4},
    {"NAME": "SIGNIFICATIVE", "TEXT": "Réussite Significative", "BasePts": 3, "COEF": 3, "formula": lambda x: x * 3},
    {"NAME": "PARTICULIERE", "TEXT": "Réussite Particulière", "BasePts": 2, "COEF": 2, "formula": lambda x: x * 2},
    {"NAME": "REUSSITE", "TEXT": "Réussite", "BasePts": 1, "COEF": 1, "formula": lambda x: x},
    {"NAME": "ECHEC", "TEXT": "Echec", "BasePts": -1, "COEF": 1, "formula": lambda x: x - 1},
    {"NAME": "NOTABLE", "TEXT": "Echec Notable", "BasePts": -2, "COEF": 0.5, "formula": lambda x: math.ceil(x / 2 - 1)},
    {"NAME": "TOTAL", "TEXT": "Echec Total", "BasePts": -4, "COEF": 0, "formula": lambda x: 0}
]

Difficultes = [
    {"NAME": "TF", "TEXT": "Très facile", "COEF": 1, "VALUE": 5},
    {"NAME": "FA", "TEXT": "Facile", "COEF": 2, "VALUE": 10},
    {"NAME": "NO", "TEXT": "Normale", "COEF": 3, "VALUE": 15},
    {"NAME": "DI", "TEXT": "Difficile", "COEF": 4, "VALUE": 20},
    {"NAME": "TD", "TEXT": "Très Difficile", "COEF": 5, "VALUE": 25}
]

GEAR_CAT = (
    ("---", "Unsorted"),
    ("bag", "Cuirs & Bagages"),
    ("jut", "Jute, Fils & Cordes"),
    ("lai", "Laine & lin"),
    ("vel", "Velours & Soies"),
    ("feu", "Feux"),
    ("cui", "Poterie, Cuisine"),
    ("out", "Outillage"),
    ("soi", "Soins"),
    ("ecr", "Ecriture"),
    ("jou", "Jouer"),
    ("loc", "Locomotion"),
    ("sus", "Sustentation"),
    ("hbs", "Herbes de Soins"),
    ("hbd", "Herbes Diverses"),
    ("ReD", "Remèdes & Antidotes"),
    ("sel", "Sels Alchimiques"),
    ("mel", "Armes de Mêlée"),
    ("tir", "Armes de Tir"),
    ("lan", "Armes de Lancer"),
    ("amu", "Armures"),

)

STRESS_COEFF = 3


def action_quality_json():
    table = {
        "title": "Qualité des Actions",
        "cols": [],
        "rows": [],
        "values": [],
        "col_back_header": [],
        "row_back_header": [],
        "options": {"even_odd": True, "cell_widths": [2, 2, 2, 2, 2], "cell_height": 0.8, "row_header_width": 4}
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
    return json.dumps(table)


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
        "title": "+dom",
        "cols": ["+dom"],
        "rows": [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"rows_header": "(TAI+FOR)/2", "cell_widths": [2], "cell_height": 0.5, "even_odd": True}
    }
    values = []
    for val in table["rows"]:
        value = f"{(math.floor((val + 2) / 3) - 2)}"
        values.append(value)
    table["values"] = values
    return json.dumps(table)


def sus_table_json():
    table = {
        "title": "sust.",
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
        "title": "sco.",
        "cols": ["SCO"],
        "rows": [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2],
        "values": [],
        "options": {"rows_header": "CON", "cell_widths": [2], "cell_height": 0.5, "even_odd": True}
    }
    values = []
    for val in table["rows"]:
        value = f"{math.floor((val + 3) / 3) + 1}"
        values.append(value)
    table["values"] = values
    return json.dumps(table)


def comp_table_json(cat=""):
    table = {
        "title": CHARACTER_STATISTICS["SKILLS"][cat.upper()]["NAME"],
        "cols": ["Compétence"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [4], "cell_height": 0.75,
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
        "cols": ["Equipement", "Enc", "Prix"],
        "rows": [],
        "values": [],
        "options": {"cell_widths": [6, 1, 2], "cell_format": ["", "enc", "sols"], "cell_height": 0.5, "even_odd": True}
    }
    rows = []
    values = []
    from main.models.equipment import Equipment
    for c in Equipment.objects.filter(category=cat,special=False):
        rows.append(f"{c.rid}")
        values.append(f"{c.name}")
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

def tai_guidelines(tai):
    base_average_weight = 56
    base_average_height = 150
    # lowest_weight_ratio = 0.9
    # highest_weight_ratio = 1.1
    # lowest_height_ratio = 0.85
    # highest_height_ratio = 1.15
    weight_ratio = 1.06
    height_ratio = 1.025
    height = base_average_height
    weight = base_average_weight
    for x in range(2,tai):
        height *= height_ratio
        weight *= weight_ratio
    height = math.ceil(height)
    weight = math.ceil(weight)
    return f"TAI={tai}: H={height} / W={weight}"