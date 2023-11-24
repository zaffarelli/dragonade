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
        {"NAME": "TIR", "TEXT": "Tir", "COMPUTE": "basic_mean,DEX,VUE"},
        {"NAME": "MEL", "TEXT": "Mêlée", "COMPUTE": "basic_mean,FOR,AGI"},
        {"NAME": "DER", "TEXT": "Dérobade", "COMPUTE": "dero_mean,TAI,AGI"},
        {"NAME": "LAN", "TEXT": "Lancer", "COMPUTE": "basic_mean,TIR,FOR"},
        {"NAME": "REV", "TEXT": "Rêve", "COMPUTE": "basic_mean,CON,EMP,APP"},
        {"NAME": "VIE", "TEXT": "Points de Vie", "COMPUTE": "basic_sum,CON,TAI"},
        {"NAME": "FAT", "TEXT": "Fatigue", "COMPUTE": "basic_mean,CON,VOL"}
    ],
    'COMPETENCES': {
        'MARTIALES': {
            "DEFAUT": 0,
            "LISTE": [
                {"NAME": "MAR01", "TEXT": "Arbalète"},
                {"NAME": "MAR02", "TEXT": "Arc"},
                {"NAME": "MAR03", "TEXT": "Bâton"},
                {"NAME": "MAR04", "TEXT": "Bouclier Léger"},
                {"NAME": "MAR05", "TEXT": "Bouclier Moyen"},
                {"NAME": "MAR06", "TEXT": "Bouclier Lourd"},
                {"NAME": "MAR07", "TEXT": "Corps-à-corps"},
                {"NAME": "MAR08", "TEXT": "Dague"},
                {"NAME": "MAR09", "TEXT": "Double Dragonne"},
                {"NAME": "MAR10", "TEXT": "Dragonne"},
                {"NAME": "MAR11", "TEXT": "Esparlongue"},
                {"NAME": "MAR12", "TEXT": "Esquive"},
                {"NAME": "MAR13", "TEXT": "Epée Bâtarde"},
                {"NAME": "MAR14", "TEXT": "Epée Cyane"},
                {"NAME": "MAR15", "TEXT": "Epée Gnome"},
                {"NAME": "MAR16", "TEXT": "Epée Sorde"},
                {"NAME": "MAR17", "TEXT": "Fléau Léger"},
                {"NAME": "MAR18", "TEXT": "Fléau Lourd"},
                {"NAME": "MAR19", "TEXT": "Fouet"},
                {"NAME": "MAR20", "TEXT": "Fronde"},
                {"NAME": "MAR21", "TEXT": "Gourdin"},
                {"NAME": "MAR22", "TEXT": "Grande Hache"},
                {"NAME": "MAR23", "TEXT": "Hâche de Bataille"},
                {"NAME": "MAR24", "TEXT": "Hachette"},
                {"NAME": "MAR25", "TEXT": "Arme d'Hast"},
                {"NAME": "MAR26", "TEXT": "Javeline"},
                {"NAME": "MAR27", "TEXT": "Javelot"},
                {"NAME": "MAR28", "TEXT": "Lance courte"},
                {"NAME": "MAR29", "TEXT": "Massette"},
                {"NAME": "MAR30", "TEXT": "Masse Lourde"}
            ]
        },
        'GENERALES': {
            "DEFAUT": -1,
            "LISTE": [
                {"NAME": "GEN01", "TEXT": "Bricolage"},
                {"NAME": "GEN02", "TEXT": "Chant"},
                {"NAME": "GEN03", "TEXT": "Concentration"},
                {"NAME": "GEN04", "TEXT": "Course"},
                {"NAME": "GEN05", "TEXT": "Cuisine"},
                {"NAME": "GEN06", "TEXT": "Danse"},
                {"NAME": "GEN07", "TEXT": "Dessin"},
                {"NAME": "GEN08", "TEXT": "Discrétion"},
                {"NAME": "GEN09", "TEXT": "Escalade"},
                {"NAME": "GEN10", "TEXT": "Saut"},
                {"NAME": "GEN11", "TEXT": "Sculpture"},
                {"NAME": "GEN12", "TEXT": "Séduction"},
                {"NAME": "GEN13", "TEXT": "Vigilance"}
            ]
        },
        'PARTICULIERES': {
            "DEFAUT": -2,
            "LISTE": [
                {"NAME": "PAR01", "TEXT": "Charpenterie"},
                {"NAME": "PAR02", "TEXT": "Comédie"},
                {"NAME": "PAR03", "TEXT": "Commerce"},
                {"NAME": "PAR04", "TEXT": "Couture"},
                {"NAME": "PAR05", "TEXT": "Equitation"},
                {"NAME": "PAR06", "TEXT": "Maçonnerie"},
                {"NAME": "PAR07", "TEXT": "Musique"},
                {"NAME": "PAR08", "TEXT": "Pickpocket"},
                {"NAME": "PAR09", "TEXT": "Survie (Cité)"},
                {"NAME": "PAR10", "TEXT": "Survie (Désert)"},
                {"NAME": "PAR11", "TEXT": "Survie (Extérieur)"},
                {"NAME": "PAR12", "TEXT": "Survie (Forêt)"},
                {"NAME": "PAR13", "TEXT": "Survie (Glaces)"},
                {"NAME": "PAR14", "TEXT": "Survie (Marais)"},
                {"NAME": "PAR15", "TEXT": "Survie (Montagne)"},
                {"NAME": "PAR16", "TEXT": "Survie (Sous-Sol)"},
                {"NAME": "PAR17", "TEXT": "Travestissement"}
            ]
        },
        'SPECIALISEES': {
            "DEFAUT": -3,
            "LISTE": [
                {"NAME": "SPE01", "TEXT": "Acrobatie"},
                {"NAME": "SPE02", "TEXT": "Chirurgie"},
                {"NAME": "SPE03", "TEXT": "Jeu"},
                {"NAME": "SPE04", "TEXT": "Jonglerie"},
                {"NAME": "SPE05", "TEXT": "Maroquinerie"},
                {"NAME": "SPE06", "TEXT": "Métallurgie"},
                {"NAME": "SPE07", "TEXT": "Natation"},
                {"NAME": "SPE08", "TEXT": "Navigation"},
                {"NAME": "SPE09", "TEXT": "Orfèvrerie"},
                {"NAME": "SPE10", "TEXT": "Serrurerie"}
            ]
        },
        'CONNAISSANCES': {
            "DEFAUT": -4,
            "LISTE": [
                {"NAME": "CON01", "TEXT": "Alchimie"},
                {"NAME": "CON02", "TEXT": "Architecture"},
                {"NAME": "CON03", "TEXT": "Astrologie"},
                {"NAME": "CON05", "TEXT": "Botanique"},
                {"NAME": "CON06", "TEXT": "Ecriture"},
                {"NAME": "CON07", "TEXT": "Légendes"},
                {"NAME": "CON08", "TEXT": "Mathématiques"},
                {"NAME": "CON09", "TEXT": "Médecine"},
                {"NAME": "CON10", "TEXT": "Zoologie"}
            ]
        },
        'DRACONIQUES': {
            "DEFAUT": -5,
            "LISTE": [
                {"NAME": "DRA01", "TEXT": "Contemplatif"},
                {"NAME": "DRA02", "TEXT": "Destructif"},
                {"NAME": "DRA03", "TEXT": "Dynamique"},
                {"NAME": "DRA04", "TEXT": "Génératif"},
                {"NAME": "DRA05", "TEXT": "Mnémonique"},
                {"NAME": "DRA06", "TEXT": "Statique"}
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
