CHARACTER_STATISTICS = {
    "ATTRIBUTES": {
        "DEFAULT": 3,
        "LIST":[
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
        ]
    },
    "SECONDARIES": [
        {"NAME": "TIR", "TEXT": "Tir", "COMPUTE": "basic_mean,DEX;VUE"},
        {"NAME": "MEL", "TEXT": "Mêlée", "COMPUTE": "basic_mean,FOR;AGI"},
        {"NAME": "DER", "TEXT": "Dérobade", "COMPUTE": "dero_mean,TAI;AGI"},
        {"NAME": "LAN", "TEXT": "Lancer", "COMPUTE": "basic_mean,TIR;FOR"}
    ],
    "MISCELLANEOUS": [
        {"NAME": "REV", "TEXT": "Rêve", "COMPUTE": "basic_mean,CON;EMP;APP"},
        {"NAME": "VIE", "TEXT": "Points de Vie", "COMPUTE": "basic_sum,CON;TAI"},
        {"NAME": "FAT", "TEXT": "Fatigue", "COMPUTE": "basic_mean,CON;VOL"},
        {"NAME": "DOM", "TEXT": "+dom", "COMPUTE": "from_table_mean,TAI;FOR,tbDOM"},
        {"NAME": "SUS", "TEXT": "Sustentation", "COMPUTE": "from_table_mean,TAI,tbSUS"},
        {"NAME": "SCO", "TEXT": "Seuil Con", "COMPUTE": "from_table_mean,CON,tbSCO"},
        {"NAME": "ENC", "TEXT": "Encombrement", "COMPUTE": "precise_mean,TAI,FOR"}
    ],
    "SKILLS": {
        "WEAPONS": {
            "DEFAULT": 0,
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
                {"NAME": "WEA_30", "TEXT": "Masse Lourde"}
            ]
        },
        "GENERIC": {
            "DEFAULT": -1,
            "LIST": [
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
        "PECULIAR": {
            "DEFAULT": -2,
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
            ]
        },
        "SPECIALIZED": {
            "DEFAULT": -3,
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
            ]
        },
        "KNOWLEDGE": {
            "DEFAULT": -4,
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
            ]
        },
        "DRACONIC": {
            "DEFAULT": -5,
            "LIST": [
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
    "tbDOM": [-10, -1, -1, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
    "tbSUS": [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
    "tbSCO": [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8, 8]
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
    {"NAME": "Arme d'Hast", "ATT_REF": "MEL", "COMP_REF": "WEA_01", "DOM": 3, "INIT": "P1"}
]
