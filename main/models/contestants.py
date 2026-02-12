from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, Chaser, Nougardine
from main.models.combats import Combat
import json
import math


class Contestant(models.Model):
    name = models.CharField(max_length=256, blank=True)
    rid =  models.CharField(max_length=256, blank=True)
    source_rid = models.CharField(max_length=256, blank=True)
    # code = models.CharField(max_length=16, default="", blank=True)
    # team = models.CharField(max_length=16, default="white", blank=True)
    _data = models.TextField(max_length=2048, default="{}", blank=True)
    _data = models.TextField(max_length=2048, default="{}", blank=True)
    vie = models.IntegerField(default=0, blank=True)
    fat = models.IntegerField(default=0, blank=True)
    handicap = models.IntegerField(default=0, blank=True)
    chosen_diff = models.IntegerField(default=5, blank=True)
    two_handed = models.BooleanField(default=False, blank=True)
    combat = models.ForeignKey(Combat, on_delete= models.CASCADE, null=True)

    def collect_from_rid(self, rid, type="Traveller"):
        from main.models.travellers import Traveller
        from main.models.autochtons import Autochton
        from main.models.creatures import Creature
        data = {}
        c = None
        # print("Type:",type)
        if type == "Traveller":
            cs = Traveller.objects.filter(rid=rid)
            if len(cs) == 1:
                c = cs.first()
        elif type == "Autochton":
            cs = Autochton.objects.filter(rid=rid)
            if len(cs) == 1:
                c = cs.first()
        elif type == "Creature":
            cs = Creature.objects.filter(rid=rid)
            if len(cs) == 1:
                c = cs.first()
        else:
            return False
        # print("-*-*-*-*-")
        # print(c)
        # print(rid)
        # print("-*-*-*-*-")
        if c is not None:
            c.export_to_json()
            # print("CDATA")
            # print(c.data)
            data = {"header": {}, "proficiencies": {}, "equipment": {}}
            data["header"]["name"] = c.name
            data["header"]["type"] = type
            data["header"]["rid"] = c.rid
            self.source_rid = rid
            data["proficiencies"]["MEL"] = c.value_for("MEL")
            data["proficiencies"]["DER"] = c.value_for("DER")
            data["proficiencies"]["ESQ"] = c.value_for("WEA_12")
            data["header"]["SCO"] = c.value_for("SCO")
            data["header"]["VIE"] = c.value_for("VIE")
            data["header"]["FAT"] = c.value_for("FAT")
            data["header"]["DOM"] = c.value_for("DOM")
            data["header"]["PDF"] = c.computeFatigue(data["header"]["FAT"])
            data["header"]["TWO_HANDED"] = False
            value, key, txt = c.best_for("SKILLS:WEAPONS")
            data["proficiencies"]["best_weapon"] = {"value": value, "key": key, "name": txt}

            # Weapons
            my_weapons = c.gear_to_weapons()
            data["weapon"] = ""
            for my_weapon in my_weapons:
                if my_weapon["skill"] == key:
                    data["weapon"] = my_weapon

            # Armors
            my_armors = c.gear_to_armors()
            # print(my_weapons)
            data["armor"] = ""
            max = 0
            for my_armor in my_armors:
                if my_armor["prot"] > max:
                    data["armor"] = my_armor
                    max = my_armor["prot"]

            if data["weapon"] != "":
                data["proficiencies"]["SEV"] = data["header"]["DOM"]
                if data["weapon"]["dom_1"] != "-":
                    data["proficiencies"]["SEV"] += data["weapon"]["dom_1"]
                    data["header"]["TWO_HANDED"] = False
                else:
                    data["proficiencies"]["SEV"] += data["weapon"]["dom_2"]
                    data["header"]["TWO_HANDED"] = True
        self.set_data(data)
        return True

    def set_data(self, json_data):
        self._data = json.dumps(json_data, indent=4, sort_keys=False)
        chaser = Chaser(self.get_data())
        self.name = chaser.reach("header:name")
        self.vie = chaser.reach("header:VIE")
        self.fat = chaser.reach("header:FAT")
        self.as_two_handed()
        self.select_diff()

    def get_data(self):
        json_data = json.loads(self._data)
        return json_data

    def fix(self):
        self.qualify() #self.rid = as_rid(f"{self.name}_{self.code}")

    def __str__(self):
        return f"{self.name} [TEAM:{self.team}]"

    def attack(self):
        pass

    @classmethod
    def prepare_battle(cls, combat):
        contestants_to_be_deleted = cls.objects.exclude(combat=combat)
        for contestant in contestants_to_be_deleted:
            # print(f"Deleting {contestant.name}")
            contestant.delete()

    @property
    def show_data(self):
        return json.dumps(self.get_data(), indent=4, sort_keys=False)

    def select_diff(self):
        chaser = Chaser(self.get_data())
        MELEE = chaser.reach('proficiencies:MEL')
        WEAPON = chaser.reach('proficiencies:best_weapon:value')
        d = self.handicap + MELEE + WEAPON
        self.chosen_diff = int(math.floor(d / 5) * 5)
        # print(f"Chosen diff = {self.chosen_diff} [{MELEE} {WEAPON} {self.handicap}]")
        if self.chosen_diff == 0:
            self.chosen_diff = 5
            # print(f"Chosen diff = {self.chosen_diff}")

    def as_two_handed(self):
        chaser = Chaser(self.get_data())
        self.two_handed = chaser.reach('header:TWO_HANDED')


    def qualify(self):
        self.rid = "CON__"+self.combat.code+"__"+as_rid(self.name)


class ContestantAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ["combat","name"]
    list_display = ["name", "rid", "source_rid","combat", "vie", "fat", "_data"]
    list_editable = []
    list_filter = ["combat", "source_rid"]
    search_filter = ["_data"]
    actions = [refix]
