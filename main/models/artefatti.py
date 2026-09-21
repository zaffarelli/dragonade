from django.db import models
from django.contrib import admin

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.models.oggetti import Oggetto
from main.utils.mechanics import as_rid
import json

class ArtefattoCategory(models.IntegerChoices):
    WEAPON = 0, "Arme"
    ARMOR = 1, "Armure"
    CONSUMABLE = 2, "Consomable"
    TOME = 3, "Tôme"
    MISCELLANEOUS = 666, "Divers"

class ArtefattoPeriod(models.IntegerChoices):
    ONCE = 0, "Unique"
    PER_TURN = 1, "Par Tour"
    PER_HD = 2, "Par HD"
    PER_DAY = 3, "Par Jour"

class Artefatto(models.Model,ChiaroscuroMixin):
    class Meta:
        ordering = ['name']
        verbose_name = "Artefatto"
        verbose_name_plural = "Artefatti"

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    equipment_match = models.CharField(default="xxx", max_length=256, blank=True)
    equipment_code = models.CharField(default="", max_length=256, blank=True)
    category = models.PositiveIntegerField(default=ArtefattoCategory.MISCELLANEOUS, choices=ArtefattoCategory.choices,
                                           blank=True)
    owner = models.CharField(default="", max_length=256, blank=True)
    creator = models.CharField(default="", max_length=256, blank=True)
    glance = models.CharField(default="", max_length=256, blank=True)
    materials = models.CharField(default="", max_length=256, blank=True)
    scales = models.CharField(default="e", max_length=256, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    rules = models.TextField(default="", max_length=2048, blank=True)
    notes = models.TextField(default="", max_length=1024, blank=True)
    mastery = models.PositiveIntegerField(default=0, blank=True)
    inertia = models.IntegerField(default=0, blank=True)
    period = models.PositiveIntegerField(default=ArtefattoPeriod.ONCE, choices=ArtefattoPeriod.choices, blank=True)
    gems_str = models.CharField(default="", max_length=512, blank=True)
    pdr = models.IntegerField(default=1, blank=True)
    charges = models.IntegerField(default=0, blank=True)

    mod_ini = models.IntegerField(default=0, blank=True)
    mod_man = models.IntegerField(default=0, blank=True)
    mod_dmg = models.IntegerField(default=0, blank=True)

    price = models.PositiveIntegerField(default=1000, blank=True)
    power = models.IntegerField(default=0, blank=True)
    sogni = models.CharField(max_length=256, default="DEF", blank=True)
    # data = {}

    def fix(self):
        self.chiaroscuro()
        from main.utils.mechanics import asB2B
        self.rid = as_rid(f"{self.name}")
        # self.code = asB2B(self.rid).decode('utf-8').upper()
        sp = 0
        for scale in self.scales.split(" "):
            if scale in ["e","p","a"]:
                sp += 1
            elif scale in ["ge","gp","ga"]:
                sp += 3
            elif scale in ["gl"]:
                sp += 2
        self.power = sp * 5

        if self.equipment_match != "xxx":
            Oggetto.objects.filter(rid=self.rid).delete()
            found = Oggetto.objects.filter(name=self.equipment_match)
            if len(found)==1:
                o = found.first()
                self.equipment_code = o.rid
                o.pk = None
                o.name = self.name
                o.special = True
                o.price = self.price
                o.mod_ini = self.mod_ini
                o.mod_att = self.mod_man
                o.mod_dmg = self.mod_dmg
                o.save()

    def get_scales_from_str(self):
        result = []
        if self.scales != "":
            scales = self.scales.split(" ")
            result = scales
            for scale in scales:
                if scale.lower() == "e":
                    pass
                elif scale.lower() == "a":
                    pass
                elif scale.lower() == "p":
                    pass
            for _ in range(7-len(scales)):
                result.append("")
        return result

    def __str__(self):
        return f"{self.name} [{self.category}]"

    def co_push(self):
        """
            The Chiaroscuro push function adds more fields to the data structure prepared,
            like additional interpretation of values or alternative names.
        """
        self._data['category_str'] = self.get_category_display()
        self._data['period_str'] = self.get_period_display()
        self._data['all_scales'] = self.get_scales_from_str()
        self._data['all_gems'] = self.get_gems_from_str()

    @property
    def get_equipment(self):
        str = "---"
        if (self.equipment_match) != "xxx":
            str = self.equipment_match
        return str

    def get_gems_from_str(self):
        all_gems = []
        if self.gems_str != "":
            print("Gems:",self.gems_str)
            gems = self.gems_str.split(" ")
            for gem in gems:
                print("Gem:", gem)
                details = gem.upper().split(":")
                if len(details) == 4:
                    from main.models.oggetti import Oggetto
                    gs = Oggetto.objects.filter(gcode=details[0])
                    if len(gs) == 1:
                        g = gs.first()
                        info = {
                            "name": g.name,
                            "type": details[0],
                            "purity": int(details[1]),
                            "size": int(details[2]),
                            "price": int(details[1])*int(details[2]),
                            "inertia": 7-int(details[1]),
                            "attachment": details[3],
                        }
                        print("***", info)
                        all_gems.append(info)
        return all_gems

    def export_to_json(self):
        self.model_to_data()
        return self._data

class ArtefattoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ["name", "gems_str","mastery","pdr", "charges", "equipment_code", "equipment_match", "mod_ini", "mod_man", "mod_dmg", "owner", "category", "glance",
                    "materials", "description"]
    list_filter = ['category', 'category']
    search_fields = ['name', "description"]
    list_editable = ["equipment_match","mastery","pdr", "charges", "gems_str", "category", "mod_ini", "mod_man", "mod_dmg"]
    actions = [refix]
