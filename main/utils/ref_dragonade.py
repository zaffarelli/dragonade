CHARACTER_STATISTICS = {
    'ATTRIBUTS': [
        {'NAME': 'AGI', 'TEXT': 'Agilité'},
        {'NAME': 'CON', 'TEXT': 'Constitution'},
        {'NAME': 'FOR', 'TEXT': 'Force'},
        {'NAME': 'TAI', 'TEXT': 'Taille'},
        {'NAME': 'EMP', 'TEXT': 'Empathie'},
        {'NAME': 'ODG', 'TEXT': 'Odorat/Goût'},
        {'NAME': 'OUI', 'TEXT': 'Ouïe'},
        {'NAME': 'VUE', 'TEXT': 'Vue'},
        {'NAME': 'APP', 'TEXT': 'Apparence'},
        {'NAME': 'DEX', 'TEXT': 'Dextérité'},
        {'NAME': 'INT', 'TEXT': 'Intelligence'},
        {'NAME': 'VOL', 'TEXT': 'Volonté'}
    ],
    'SECONDAIRES': [
        {"NAME": "TIR", "TEXT": "Tir", "COMPUTE": "basic_mean,DEX;VUE"},
        {"NAME": "MEL", "TEXT": "Mêlée", "COMPUTE": "basic_mean,FOR;AGI"},
        {"NAME": "DER", "TEXT": "Dérobade", "COMPUTE": "dero_mean,TAI;AGI"},
        {"NAME": "LAN", "TEXT": "Lancer", "COMPUTE": "basic_mean,TIR;FOR"},
        {"NAME": "REV", "TEXT": "Rêve", "COMPUTE": "basic_mean,CON;EMP;APP"},
        {"NAME": "VIE", "TEXT": "Points de Vie", "COMPUTE": "basic_sum,CON;TAI"},
        {"NAME": "FAT", "TEXT": "Fatigue", "COMPUTE": "basic_mean,CON;VOL"},
        {"NAME": "DOM", "TEXT": "+dom", "COMPUTE": "from_table_mean,TAI;FOR,tbDOM"},
        {"NAME": "SUS", "TEXT": "Sustentation", "COMPUTE": "from_table_mean,TAI,tbSUS"},
        {"NAME": "SCO", "TEXT": "Seuil Con", "COMPUTE": "from_table_mean,CON,tbSCO"},
        {"NAME": "ENC", "TEXT": "Encombrement", "COMPUTE": "precise_mean,TAI,FOR"}
    ],
    'COMPETENCES': {
        'MARTIALES': {
            "DEFAUT": 0,
            "LISTE": [
                {"NAME": "MAR_01", "TEXT": "Arbalète"},
                {"NAME": "MAR_02", "TEXT": "Arc"},
                {"NAME": "MAR_03", "TEXT": "Bâton"},
                {"NAME": "MAR_04", "TEXT": "Bouclier Léger"},
                {"NAME": "MAR_05", "TEXT": "Bouclier Moyen"},
                {"NAME": "MAR_06", "TEXT": "Bouclier Lourd"},
                {"NAME": "MAR_07", "TEXT": "Corps-à-corps"},
                {"NAME": "MAR_08", "TEXT": "Dague"},
                {"NAME": "MAR_09", "TEXT": "Double Dragonne"},
                {"NAME": "MAR_10", "TEXT": "Dragonne"},
                {"NAME": "MAR_11", "TEXT": "Esparlongue"},
                {"NAME": "MAR_12", "TEXT": "Esquive"},
                {"NAME": "MAR_13", "TEXT": "Epée Bâtarde"},
                {"NAME": "MAR_14", "TEXT": "Epée Cyane"},
                {"NAME": "MAR_15", "TEXT": "Epée Gnome"},
                {"NAME": "MAR_16", "TEXT": "Epée Sorde"},
                {"NAME": "MAR_17", "TEXT": "Fléau Léger"},
                {"NAME": "MAR_18", "TEXT": "Fléau Lourd"},
                {"NAME": "MAR_19", "TEXT": "Fouet"},
                {"NAME": "MAR_20", "TEXT": "Fronde"},
                {"NAME": "MAR_21", "TEXT": "Gourdin"},
                {"NAME": "MAR_22", "TEXT": "Grande Hache"},
                {"NAME": "MAR_23", "TEXT": "Hâche de Bataille"},
                {"NAME": "MAR_24", "TEXT": "Hachette"},
                {"NAME": "MAR_25", "TEXT": "Arme d'Hast"},
                {"NAME": "MAR_26", "TEXT": "Javeline"},
                {"NAME": "MAR_27", "TEXT": "Javelot"},
                {"NAME": "MAR_28", "TEXT": "Lance courte"},
                {"NAME": "MAR_29", "TEXT": "Massette"},
                {"NAME": "MAR_30", "TEXT": "Masse Lourde"}
            ]
        },
        'GENERALES': {
            "DEFAUT": -1,
            "LISTE": [
                {"NAME": "GEN_01", "TEXT": "Bricolage"},
                {"NAME": "GEN_02", "TEXT": "Chant"},
                {"NAME": "GEN_03", "TEXT": "Concentration"},
                {"NAME": "GEN_04", "TEXT": "Course"},
                {"NAME": "GEN_05", "TEXT": "Cuisine"},
                {"NAME": "GEN_06", "TEXT": "Danse"},
                {"NAME": "GEN_07", "TEXT": "Dessin"},
                {"NAME": "GEN_08", "TEXT": "Discrétion"},
                {"NAME": "GEN_09", "TEXT": "Escalade"},
                {"NAME": "GEN_10", "TEXT": "Saut"},
                {"NAME": "GEN_11", "TEXT": "Sculpture"},
                {"NAME": "GEN_12", "TEXT": "Séduction"},
                {"NAME": "GEN_13", "TEXT": "Vigilance"}
            ]
        },
        'PARTICULIERES': {
            "DEFAUT": -2,
            "LISTE": [
                {"NAME": "PAR_01", "TEXT": "Charpenterie"},
                {"NAME": "PAR_02", "TEXT": "Comédie"},
                {"NAME": "PAR_03", "TEXT": "Commerce"},
                {"NAME": "PAR_04", "TEXT": "Couture"},
                {"NAME": "PAR_05", "TEXT": "Equitation"},
                {"NAME": "PAR_06", "TEXT": "Maçonnerie"},
                {"NAME": "PAR_07", "TEXT": "Musique"},
                {"NAME": "PAR_08", "TEXT": "Pickpocket"},
                {"NAME": "PAR_09", "TEXT": "Survie (Cité)"},
                {"NAME": "PAR_10", "TEXT": "Survie (Désert)"},
                {"NAME": "PAR_11", "TEXT": "Survie (Extérieur)"},
                {"NAME": "PAR_12", "TEXT": "Survie (Forêt)"},
                {"NAME": "PAR_13", "TEXT": "Survie (Glaces)"},
                {"NAME": "PAR_14", "TEXT": "Survie (Marais)"},
                {"NAME": "PAR_15", "TEXT": "Survie (Montagne)"},
                {"NAME": "PAR_16", "TEXT": "Survie (Sous-Sol)"},
                {"NAME": "PAR_17", "TEXT": "Travestissement"}
            ]
        },
        'SPECIALISEES': {
            "DEFAUT": -3,
            "LISTE": [
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
            ]
        },
        'CONNAISSANCES': {
            "DEFAUT": -4,
            "LISTE": [
                {"NAME": "CON_01", "TEXT": "Alchimie"},
                {"NAME": "CON_02", "TEXT": "Architecture"},
                {"NAME": "CON_03", "TEXT": "Astrologie"},
                {"NAME": "CON_05", "TEXT": "Botanique"},
                {"NAME": "CON_06", "TEXT": "Ecriture"},
                {"NAME": "CON_07", "TEXT": "Légendes"},
                {"NAME": "CON_08", "TEXT": "Mathématiques"},
                {"NAME": "CON_09", "TEXT": "Médecine"},
                {"NAME": "CON_10", "TEXT": "Zoologie"}
            ]
        },
        'DRACONIQUES': {
            "DEFAUT": -5,
            "LISTE": [
                {"NAME": "DRA_01", "TEXT": "Contemplatif"},
                {"NAME": "DRA_02", "TEXT": "Destructif"},
                {"NAME": "DRA_03", "TEXT": "Dynamique"},
                {"NAME": "DRA_04", "TEXT": "Génératif"},
                {"NAME": "DRA_05", "TEXT": "Mnémonique"},
                {"NAME": "DRA_06", "TEXT": "Statique"}
            ]
        }
    }

}

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
    'tbDOM': [-10, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
    'tbSUS': [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
    'tbSCO': [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8]
}

QualiteDesActions = [
    {"NAME": "CRITIQUE", "TEXT": "Réussite Critique", "BasePts": 4, "COEF": 4},
    {"NAME": "SIGNIFICATIVE", "TEXT": "Réussite Significative", "BasePts": 3, "COEF": 3},
    {"NAME": "PARTICULIERE", "TEXT": "Réussite Particulière", "BasePts": 2, "COEF": 2},
    {"NAME": "REUSSITE", "TEXT": "Réussite", "BasePts": 1, "COEF": 1},
    {"NAME": "ECHEC", "TEXT": "Echec", "BasePts": -1, "COEF": 1},
    {"NAME": "NOTABLE", "TEXT": "Echec Notable", "BasePts": -2, "COEF": 0.5},
    {"NAME": "TOTAL", "TEXT": "Echec Total", "BasePts": -4, "COEF": 0}
]

Difficultes = [
    {"NAME": "TF", "TEXT": "Très facile", "COEF": 1},
    {"NAME": "FA", "TEXT": "Facile", "COEF": 2},
    {"NAME": "NO", "TEXT": "Normale", "COEF": 3},
    {"NAME": "DI", "TEXT": "Difficile", "COEF": 4},
    {"NAME": "TD", "TEXT": "Très Difficile", "COEF": 5}
]

ARMES = [
    {"NAME": "Arme d'Hast", "ATT_REF": "MEL", "COMP_REF": "MAR_01", "DOM": 3, "INIT": "P1"}
]
