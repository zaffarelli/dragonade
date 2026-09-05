from django.db import models
from django.contrib import admin

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.mechanics import as_rid
import math
from django.utils import timezone


# from main.utils.ref_dragonade import GEAR_CAT

#
# GEAR_CAT = (
#     ("---", "Unsorted"),
#     ("bag", "Cuirs & Bagages"),
#     ("jut", "Jute, Fils & Cordes"),
#     ("lai", "Laine & lin"),
#     ("vel", "Velours & Soies"),
#     ("feu", "Feux"),
#     ("cui", "Poterie, Cuisine"),
#     ("out", "Outillage"),
#     ("soi", "Soins"),
#     ("ecr", "Ecriture"),
#     ("jou", "Jouer"),
#     ("loc", "Locomotion"),
#     ("sus", "Sustentation"),
#     ("hbs", "Herbes de Soins"),
#     ("hbd", "Herbes Diverses"),
#     ("ReD", "Remèdes & Antidotes"),
#     ("sel", "Sels Alchimiques"),
#     ("mel", "Armes de Mêlée"),
#     ("tir", "Armes de Tir"),
#     ("lan", "Armes de Lancer"),
#     ("amu", "Armures"),
#     ("ana", "Armes Naturelles"),
#     ("gem", "Gemmes & Joyaux"),
#
# )


class OggettoCategory(models.IntegerChoices):
    NONE = 1, "n/a"
    BAG = 2, "Cuirs & Bagages"
    JUT = 3, "Jute, Fils & Cordes"
    LAI = 4, "Laine & lin"
    VEL = 5, "Velours & Soies"
    FEU = 6, "Feux"
    CUI = 7, "Poterie, Cuisine"
    OUT = 8, "Outillage"
    SOI = 9, "Soins"
    ECR = 10, "Ecriture"
    JOU = 11, "Jouer"
    LOC = 12, "Locomotion"
    SUS = 13, "Sustentation"
    HBS = 14, "Herbes de Soins"
    HBD = 15, "Herbes Diverses"
    REM = 16, "Remèdes & Antidotes"
    SEL = 17, "Sels Alchimiques"
    MEL = 18, "Armes de Mêlée"
    TIR = 19, "Armes de Tir"
    LAN = 20, "Armes de Lancer"
    AMU = 21, "Armures"
    ANA = 22, "Armes Naturelles"
    GEM = 23, "Gemmes & Joyaux"


class Oggetto(models.Model, ChiaroscuroMixin):
    class Meta:
        ordering = ['category']
        verbose_name = "Oggetto"
        verbose_name_plural = "Oggetti"

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    category = models.IntegerField(default=OggettoCategory.NONE, choices=OggettoCategory.choices)
    can_be_thrown = models.BooleanField(default=False, blank=True)
    plus_dom = models.IntegerField(default=0, null=True, blank=True)
    plus_dom_2m = models.IntegerField(default=0, null=True, blank=True)
    prot = models.IntegerField(default=0, null=True, blank=True)
    quality = models.IntegerField(default=0, null=True, blank=True)
    engagement = models.IntegerField(default=0, null=True, blank=True)
    maneuver = models.IntegerField(default=0, null=True, blank=True)
    cover = models.CharField(default="", max_length=64, blank=True)
    materiaux = models.CharField(default="", max_length=64, blank=True)
    related_skill = models.CharField(default="", max_length=32, blank=True)
    related_attribute = models.CharField(default="", max_length=8, blank=True)
    malus_AGI = models.IntegerField(default=0, null=True, blank=True)
    malus_DEX = models.IntegerField(default=0, null=True, blank=True)
    malus_VUE = models.IntegerField(default=0, null=True, blank=True)
    malus_OUI = models.IntegerField(default=0, null=True, blank=True)
    sogni = models.CharField(max_length=256, default="DEF", blank=True)

    range = models.IntegerField(default=0, null=True, blank=True)

    force_min = models.IntegerField(default=0, null=True, blank=True)
    enc = models.FloatField(default=0, blank=True)
    resistance = models.IntegerField(default=0, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    price = models.FloatField(default=0, blank=True)
    quantity = models.FloatField(default=0.1, blank=True)
    mod_ini = models.IntegerField(default=0, blank=True)
    mod_dom = models.IntegerField(default=0, blank=True)
    mod_att = models.IntegerField(default=0, blank=True)
    special = models.BooleanField(default=False, blank=True)
    similitude = models.TextField(default="", max_length=1024, blank=True)

    skill_match = models.CharField(default="", max_length=32, blank=True)

    def fix(self):
        self.chiaroscuro()
        self.rid = as_rid(f"{self.name}_{self.category}")
        # if self.cover != "":
        #     new_covers = []
        #     covers = self.cover.upper().split(" ")
        #     for cover in covers:
        #         if cover.startswith("H") == False and cover.startswith("P") == False:
        #             new_covers.append(cover)
        #     self.cover = " ".join(new_covers)
        #     self.cover = self.cover.replace("T","H").replace("B","A").replace("J","L").replace("1","S").replace("2","W")

        self.name = self.name.replace("  ", " ")
        self.name = self.name.strip()
        if self.category in [OggettoCategory.ANA]:  # Armes naturelles
            self.price = 0
            self.enc = 0
        if self.category in [OggettoCategory.MEL, OggettoCategory.TIR, OggettoCategory.LAN]:
            from main.utils.ref_dragonade import CHARACTER_STATISTICS
            self.skill_match = ""
            # print("SEARCH", self.name.upper())
            for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                # print(f'  Test: [{skill["TEXT"].upper()}]')
                if skill["TEXT"].upper().strip() == self.name.upper().strip():
                    self.related_skill = skill["NAME"]
                    # print("     MATCH",skill["TEXT"].upper(), self.name.upper(), skill["NAME"])
                    break
                # else:
                #     print(f'     Not matching with [{self.name.upper()}]')
            if len(self.related_skill) > 0:
                skill_match = []
                related_skills = self.related_skill.upper().split(" ")
                for related_skill in related_skills:
                    for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                        if skill["NAME"].upper() == related_skill:
                            skill_match.append(skill["TEXT"])
                            break
                self.skill_match = ", ".join(skill_match)
        if self.category == OggettoCategory.AMU:
            if self.malus_AGI > 0:
                self.malus_AGI = -self.malus_AGI
            if self.malus_DEX > 0:
                self.malus_DEX = -self.malus_DEX
            if self.malus_VUE > 0:
                self.malus_VUE = -self.malus_VUE
            if self.malus_OUI > 0:
                self.malus_OUI = -self.malus_OUI
            if len(self.cover) > 0:
                covs = self.cover.upper().split(" ")
                updated_cover = []
                for cov in covs:
                    if cov == "H":
                        updated_cover.append("H")
                    elif cov in ["A", "AS", "B1", "SA"]:
                        updated_cover.append("A")
                    elif cov in ["C"]:
                        updated_cover.append("C")
                    elif cov in ["B", "WA", "AW", "B2"]:
                        updated_cover.append("B")
                    elif cov in ["L", "SL", "LS"]:
                        updated_cover.append("L")
                    elif cov in ["M", "WL", "LW"]:
                        updated_cover.append("M")
                self.cover = " ".join(updated_cover)
            if len(self.materiaux) > 0:
                tr = 0
                cnt = 0
                materiaux = self.materiaux.split(", ")
                for materiau in materiaux:
                    if materiau == "Acier":
                        tr += 20
                        cnt += 1
                    elif materiau == "Tissu":
                        tr += 4
                        cnt += 1
                    elif materiau == "Caleb Raën Ron":
                        tr += 25
                        cnt += 1
                    elif materiau == "Cuir Souple":
                        tr += 8
                        cnt += 1
                    elif materiau == "Cuir Epais":
                        tr += 12
                        cnt += 1
                    elif materiau == "Bronze":
                        tr += 15
                        cnt += 1
                if cnt > 0:
                    self.resistance = math.ceil(tr / cnt) + self.quality

    def __str__(self):
        return f"{self.name} [{self.get_category_display()}]"

    def covers(self, str=""):
        res = False
        if self.category == OggettoCategory.AMU:
            if self.cover != "":
                keys = self.cover.split(" ")
                for key in keys:
                    if str == key:
                        return True
        return res

    def export_to_json(self):
        self.model_to_data()
        return self._data

    def co_push(self):
        self._data["category_text"] = self.get_category_display()

    @property
    def related_skill_name(self):
        names = []
        if self.category in [OggettoCategory.MEL, OggettoCategory.TIR, OggettoCategory.LAN]:
            if self.related_skill != "":
                from main.utils.ref_dragonade import CHARACTER_STATISTICS
                skills = self.related_skill.upper().strip().split(" ")
                for s in skills:
                    s
                    for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                        if skill["NAME"].upper().strip() == s:
                            names.append(skill["TEXT"])
        return ", ".join(names)

    @classmethod
    def references(klass):
        list = []
        for item in klass.objects.order_by("-category", "name"):
            list.append({"name": '[' + item.get_category_display()[:4] + '] ' + item.name, "rid": item.rid})
        return list

    @classmethod
    def extract_all(cls):
        list = []
        for item in cls.objects.order_by("name").exclude(special=True).order_by("category"):
            list.append({"name": item.name, "rid": item.rid, "price": item.price, "enc": item.enc})
            price = f"{int(item.price):2}s {int(item.price * 100) % 100:2}d"
            print(f"{item.name.strip():30}µ{item.rid:30}µ{item.get_category_display():50}µ{price:20} µ{item.enc:5}§")
        return list


def cat_from_first(modeladmin, request, queryset):
    if len(queryset) > 2:
        cat = ""
        for item in queryset:
            if cat == "":
                cat = item.category
            else:
                item.category = cat
                item.save()
    short_description = "Category from the first item"


class OggettoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['category', 'related_attribute', 'name']
    # Armors
    list_display = ["rid","name", "id", "category", "cover", "enc", "price", "resistance", "materiaux", "prot", "quality",
                    "malus_AGI", "malus_DEX",
                    "malus_VUE", "malus_OUI","force_min"
                    ]
    list_editable = ["category", "cover", "materiaux", "resistance","quality","force_min"]
    # Weapons
    # list_display = ["rid", "id", "category", "name", "maneuver","related_skill", "related_skill_name", "engagement", "enc", "price", "resistance","force_min"
    #                 ]
    # list_editable = ["category", "related_skill","maneuver","engagement", "enc", "price", "resistance","force_min"]
    list_filter = ["category", "can_be_thrown", "special", "materiaux", "cover"]
    search_fields = ['name']
    actions = [refix, cat_from_first]
