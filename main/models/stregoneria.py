from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid
from django.utils import timezone
import math


class DragonadeDifficulty(models.IntegerChoices):
    VERY_EASY = 5, "Très Facile"
    EASY = 10, "Facile"
    AVERAGE = 15, "Moyenne"
    HARD = 20, "Difficile"
    VERY_HARD = 25, "Très Difficile"


class DragonadeGround(models.IntegerChoices):
    NONE = 0, "-"
    SANCTUARY = 1, "Sanctuaire"
    DESERT = 2, "Désert"
    MOUNTS = 3, "Monts"
    CITY = 4, "Cité"
    FOREST = 5, "Forêt"
    PLAIN = 6, "Plaine"
    HILLS = 7, "Collines"
    BRIDGE = 8, "Pont"
    RIVER = 9, "Fleuve"
    LAKE = 10, "Lac"
    SWAMP = 11, "Marais"
    DESOLATION = 12, "Désolation"
    CHASM = 13, "Gouffre"
    NECROPOLIS = 14, "Nécropole"
    SPECIAL = 666, "Voir Texte"


class DragonadeHour(models.IntegerChoices):
    NONE = 0, "-"
    SHIP = 1, "Vaisseau"
    SIREN = 2, "Sirène"
    FALCON = 3, "Faucon"
    CROWN = 4, "Couronne"
    DRAGON = 5, "Dragon"
    SWORDS = 6, "Epées"
    HARP = 7, "Lyre"
    SNAKE = 8, "Serpent"
    FLYING_FISH = 9, "Poisson-Acrobate"
    SPIDER = 10, "Araignée"
    REED = 11, "Roseau"
    SLEEPY_CASTLE = 12, "Château-Dormant"
    SPECIAL = 666, "Voir Texte"


class DragonadeEmanation(models.IntegerChoices):
    NONE = 0, "-"
    WAVY = 1, "Ondée"
    FLOW = 2, "Flux"
    FLUENT = 3, "Courant"
    WAVE = 4, "Vague"
    TIDE = 5, "Marée"
    FLUSH = 6, "Ras"
    SURGING = 7, "Déferlante"
    SPECIAL = 666, "Voir Texte"


class DragonadeConsistency(models.IntegerChoices):
    NONE = 0, "-"
    SPIRIT = 1, "Humeur"
    STEAM = 2, "Vapeur"
    FLUID = 3, "Fluide"
    CITY = 4, "Précipité"
    CONGESTION = 5, "Congestion"
    CLUSTER = 6, "Amas"
    CRYSTAL = 7, "Cristal"
    SPECIAL = 666, "Voir Texte"


class DragonadeElement(models.IntegerChoices):
    NONE = 0, "-"
    WATER = 1, "Eau"
    FIRE = 2, "Feu"
    EARTH = 3, "Terre"
    AIR = 4, "Air"
    WOOD = 5, "Bois"
    METAL = 6, "Métal"
    HEPTA = 7, "Septième"
    SPECIAL = 666, "Voir Texte"


class SpellCategory(models.IntegerChoices):
    NONE = 0, "-"
    INCANTATION = 1, "Incantation"
    RITUAL = 2, "Rituel"
    PENTACLE = 3, "Pentacle"


class SpellPath(models.IntegerChoices):
    NONE = 0, "-"
    GENERIC = 1, "Générique"
    HYPNOS = 2, "Hypnos"
    ONIROS = 3, "Oniros"
    NARCOS = 4, "Narcos"
    THANATOS = 5, "Thanatos"
    MORPHEOS = 6, "Morpheos"



class SpellRoll(models.IntegerChoices):
    NONE = 0, "-"
    CONTEMPLATIVE = 1, "Contemplatif"
    DESTRUCTIVE = 2, "Destructif"
    DYNAMIC = 3, "Dynamique"
    GENERATIVE = 4, "Génératif"
    MNEMONIC = 5, "Mnémonique"
    STATIC = 6, "Statique"



class SpellCastingTime(models.IntegerChoices):
    INSTANT = 0, "Instantanné"
    ROUND = 1, "Tour"
    MINUTE = 2, "Minute"
    HOUR = 3, "Demi-Heure Draconique"
    DRACONIC_HOUR = 4, "Heure Draconique"
    DAY = 5, "Jour"
    WEEK = 6, "Semaine"

class Spell(models.Model):
    class Meta:
        ordering = ["-spell_ready", 'name']

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    alternative_names = models.CharField(default="", max_length=512, blank=True)

    casting_time = models.PositiveIntegerField(default=1, blank=True)

    ground_charge = models.PositiveIntegerField(default=DragonadeGround.NONE, choices=DragonadeGround.choices,
                                                blank=True)
    hour_charge = models.PositiveIntegerField(default=DragonadeHour.NONE, choices=DragonadeHour.choices, blank=True)
    emanation_charge = models.PositiveIntegerField(default=DragonadeEmanation.NONE, choices=DragonadeEmanation.choices,
                                                   blank=True)
    consistency_charge = models.PositiveIntegerField(default=DragonadeConsistency.NONE,
                                                     choices=DragonadeConsistency.choices, blank=True)
    elemental_charge = models.PositiveIntegerField(default=DragonadeElement.NONE, choices=DragonadeElement.choices,
                                                   blank=True)

    dps = models.PositiveIntegerField(default=3, blank=True)
    songe = models.PositiveIntegerField(default=0, blank=True)
    duration = models.CharField(default="-", max_length=128, blank=True)
    range = models.CharField(default="-", max_length=128, blank=True)
    resistance = models.CharField(default="-", max_length=128, blank=True)
    diff = models.PositiveIntegerField(default=DragonadeDifficulty.AVERAGE, choices=DragonadeDifficulty.choices,
                                       blank=True)

    original_casting_cost = models.CharField(default="-", max_length=1024, blank=True)

    description = models.TextField(default="", max_length=1024, blank=True)
    composantes = models.TextField(default="-", max_length=1024, blank=True)
    path = models.PositiveIntegerField(default=SpellPath.NONE, choices=SpellPath.choices, blank=True)
    category = models.PositiveIntegerField(default=SpellCategory.NONE, choices=SpellCategory.choices, blank=True)
    ref = models.CharField(default="RDD 2nd p.", max_length=32, blank=True)
    source = models.CharField(default="-", max_length=64, blank=True)
    ti = models.PositiveIntegerField(default=SpellCastingTime.INSTANT, choices=SpellCastingTime.choices, blank=True)

    roll = models.PositiveIntegerField(default=SpellRoll.NONE, choices=SpellRoll.choices, blank=True)
    spell_ready = models.BooleanField(default=False, blank=True)
    power = models.IntegerField(default=0, blank=True)
    data = {}

    def fix(self):
        self.rid = as_rid(f"{self.name}")
        if len(self.original_casting_cost) > 1:
            chunks = self.original_casting_cost.split(' ')
            old_diff = int(chunks[0][1:])
            old_dps = chunks[1][1:]
            if '+' in old_dps:
                old_dps = old_dps[:1]
            diff = int((-1 * math.ceil(old_diff / 2)) * 5)
            diff_pen = old_diff % 2
            dps = int(old_dps) + diff_pen
            self.diff = diff
            self.dps = dps
            str = f'{old_diff} {old_dps} / {diff} {diff_pen} {dps}'
        z = 0
        z += 1 if self.ground_charge != DragonadeGround.NONE else 0
        z += 1 if self.hour_charge != DragonadeHour.NONE else 0
        z += 1 if self.emanation_charge != DragonadeEmanation.NONE else 0
        z += 1 if self.consistency_charge != DragonadeConsistency.NONE else 0
        z += 1 if self.elemental_charge != DragonadeElement.NONE else 0
        self.power = self.diff/5 + self.dps + z + self.songe * 2

    def __str__(self):
        return f"{self.name} ({self.get_path_display()} {self.get_category_display()}) "

    @property
    def str_charges(self):
        str = f"{self.get_ground_charge_display()} {self.get_hour_charge_display()} {self.get_emanation_charge_display()} {self.get_consistency_charge_display()} {self.get_elemental_charge_display()}"
        return str

    def export_to_json(self):
        data = {}
        data['name'] = self.name
        data['rid'] = self.rid
        data['alternative_names'] = self.alternative_names
        data['casting_time'] = self.casting_time
        data['ground_charge'] = self.ground_charge
        data['hour_charge'] = self.hour_charge
        data['emanation_charge'] = self.emanation_charge
        data['consistency_charge'] = self.consistency_charge
        data['elemental_charge'] = self.elemental_charge
        data['dps'] = self.dps
        data['diff'] = self.diff
        data['ref'] = self.ref
        data['duration'] = self.duration
        data['range'] = self.range
        data['songe'] = self.songe
        data['resistance'] = self.resistance
        data['roll'] = self.get_roll_display()
        data['path'] = self.get_path_display()
        data['category'] = self.get_category_display()
        data['description'] = self.description
        data['composantes'] = self.composantes
        data['ti'] = self.get_ti_display()[:4]+"."
        data['puissance'] = self.power
        self.data = data
        return data

    @property
    def conversion(self):
        str = ""
        if len(self.original_casting_cost) > 1:
            chunks = self.original_casting_cost.split(' ')
            old_diff = int(chunks[0][1:])
            old_dps = chunks[1][1:]
            if '+' in old_dps:
                old_dps = old_dps[:1]
            diff = int((-1 * math.ceil(old_diff / 2)) * 5)
            diff_pen = old_diff % 2
            dps = int(old_dps) + diff_pen
            self.diff = diff
            self.dps = dps
            str = f'{old_diff} {old_dps} / {diff} {diff_pen} {dps}'
        return str

    @classmethod
    def references(klass):
        json_list = []
        for spell in klass.objects.order_by("name"):
            json_list.append({"name": spell.name, "rid": spell.rid})
        return json_list


class SpellAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ["-spell_ready", "name"]
    list_display = ["name", "rid", "power", "spell_ready","songe", "roll", "original_casting_cost", "conversion", "ground_charge",
                    "str_charges",
                    "path", "ref", "category", "source"]
    list_editable = ["original_casting_cost", "songe", "roll", "spell_ready", "ground_charge", "path", "ref", "category",
                     "source"]
    list_filter = ["spell_ready", "path", "category", "diff", "dps", "ref", "original_casting_cost", "ground_charge",
                   "elemental_charge", "emanation_charge",
                   "consistency_charge", "hour_charge", "source"]
    search_fields = ["name", "description"]
    actions = [refix]
