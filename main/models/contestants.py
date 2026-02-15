import random

from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, Chaser, Nougardine, roll, Localizer, Severity, Colorizer
from main.models.combats import Combat
import json
import math


class Contestant(models.Model):
    name = models.CharField(max_length=256, blank=True)
    rid = models.CharField(max_length=256, blank=True)
    source_rid = models.CharField(max_length=256, blank=True)
    _data = models.TextField(max_length=2048, default="{}", blank=True)
    # _data = models.TextField(max_length=2048, default="{}", blank=True)
    vie = models.IntegerField(default=0, blank=True)
    fat = models.IntegerField(default=0, blank=True)
    handicap = models.IntegerField(default=0, blank=True)
    chosen_diff = models.IntegerField(default=5, blank=True)
    two_handed = models.BooleanField(default=False, blank=True)
    combat = models.ForeignKey(Combat, on_delete=models.CASCADE, null=True, related_name="challengers")
    last_initiative = models.IntegerField(default=0, blank=True)
    is_out = models.BooleanField(default=False, blank=True)
    is_dead = models.BooleanField(default=False, blank=True)
    # is_temporary = models.BooleanField(default=True, blank=True)
    fatigue_line = models.CharField(max_length=512, blank=True)
    avoidance = models.CharField(default="E A", max_length=256, blank=True)
    personal_color = models.CharField(default="#808080", max_length=7, blank=True)
    team_color = models.CharField(default="#808080", max_length=7, blank=True)

    def collect_from_rid(self, rid, type="Traveller", color=""):
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

            # Shield
            my_weapons = c.gear_to_weapons()
            shields = ["WEA_04", "WEA_05", "WEA_06"]
            data["shield"] = {}
            data["proficiencies"]["best_shield"] = {"value": 0, "key": "", "name": "sans bouclier"}
            for shield in shields:
                val = c.value_for(shield)
                for my_weapon in my_weapons:
                    if my_weapon["skill"] == shield:
                        data["shield"] = my_weapon
                        data["proficiencies"]["best_shield"] = {"value": c.value_for(my_weapon["skill"]),
                                                                "key": my_weapon["skill"], "name": my_weapon["name"]}

            # Weapons

            data["weapon"] = ""
            for my_weapon in my_weapons:
                if my_weapon["skill"] == key:
                    data["weapon"] = my_weapon

            # Armors
            my_armors = c.gear_to_armors()
            # print(my_weapons)
            data["armor"] = {"name": "Aucune", "prot": 0, "cover": "", "materiaux": "", "skill": "", "malus_armure": 0,
                             "PRO": 0}
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

            self.handicap = data["armor"]["malus_armure"] * -1
        if color != "":
            self.personal_color = Colorizer.random_color()
        else:
            self.personal_color = color
        self.set_data(data)
        return True

    def put_avoidance(self, str):
        result = ""
        words = self.avoidance.split(" ")
        words.append(str)
        self.avoidance = " ".join(words)
        return result

    def take_avoidance(self, priorities=["B","E","A","R"]):
        result = ""
        words = self.avoidance.split(" ")
        if len(words) == 0:
            return result
        for priority in priorities:
            if priority in words:
                result = priority
        if result != "":
            words.remove(result)
        self.avoidance = " ".join(words)
        return result

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



    def rebuild_fatigue(self):
        blocks = []
        for idx in range(self.fat):
            fatigue_block = ""
            for _ in range(math.ceil((idx + 1) / 2) + 2):
                fatigue_block += f"{0}"
            blocks.append(fatigue_block)
        self.fatigue_line = "_".join(blocks)

    def consume_fatigue(self):
        words = self.fatigue_line.split("_")
        if len(words) > 0:
            s = words[-1]
            words[-1] = s[:-1]
            self.fatigue_line = "_".join(words)
        else:
            self.is_out = True
        self.save()

    def fatigue_handicap(self):
        h = 0
        h = self.fat - self.fatigue_line.count("_") - 1
        return h

    def prepare_for_new_fight(self):
        chaser = Chaser(self.get_data())

        self.prepare_for_new_round()
        self.vie = chaser.reach("header:VIE")
        self.fat = chaser.reach("header:FAT")
        self.rebuild_fatigue()
        self.save()

    def roll_initiative(self):
        self.prepare_for_new_round()
        chaser = Chaser(self.get_data())
        d12 = roll(explodes=False)
        self.last_initiative = d12 + chaser.reach("proficiencies:MEL") + chaser.reach("proficiencies:best_weapon:value")
        return self.last_initiative, d12

    def prepare_for_new_round(self):
        chaser = Chaser(self.get_data())
        self.avoidance = "E A"
        if chaser.reach("proficiencies:best_shield:name") != "sans bouclier" and not chaser.reach('header:TWO_HANDED'):
            self.put_avoidance("B")
        self.save()

    def fix_handicap(self, base):
        chaser = Chaser(self.get_data())
        self.handicap = base
        self.handicap -= chaser.reach("armor:malus_armure")

    def fix(self):
        # print(f"Saving contestant {self.name}: {self.vie}")
        self.qualify()  # self.rid = as_rid(f"{self.name}_{self.code}")

    def __str__(self):

        return f"{self.name} [{self.rid}]"


    # @classmethod
    # def prepare_battle(cls, combat):
    #     contestants_to_be_deleted = cls.objects.exclude(combat=combat)
    #     for contestant in contestants_to_be_deleted:
    #         # print(f"Deleting {contestant.name}")
    #         contestant.delete()

    # @property
    # def show_data(self):
    #     return json.dumps(self.get_data(), indent=4, sort_keys=False)

    def select_diff(self):
        audace = 1
        chaser = Chaser(self.get_data())
        MELEE = chaser.reach('proficiencies:MEL')
        WEAPON = chaser.reach('proficiencies:best_weapon:value')
        d = self.handicap + MELEE + WEAPON
        self.chosen_diff = int((math.floor(d / 5) + audace) * 5)
        if self.chosen_diff == 0:
            self.chosen_diff = 5

    def as_two_handed(self):
        chaser = Chaser(self.get_data())
        self.two_handed = chaser.reach('header:TWO_HANDED')

    # def as_shield(self):
    #     result = False
    #     if self.as_two_handed():
    #         result = False
    #     return result

    def qualify(self):
        self.rid = "CON__" + self.combat.code + "__" + as_rid(self.name)

    def battle_roster(self):
        chaser = Chaser(self.get_data())
        self.refresh_from_db()
        json_data = {}
        json_data["name"] = self.name
        json_data["PDV"] = self.vie
        json_data["color"] = self.personal_color
        json_data["team"] = self.team_color
        json_data["SCO"] = chaser.reach("header:SCO")
        json_data["FAT"] = chaser.reach("header:FAT")
        json_data["PDF"] = chaser.reach("header:PDF")
        json_data["INI"] = chaser.reach('proficiencies:MEL') + math.floor(
            chaser.reach('proficiencies:best_weapon:value') / 2)
        # print(self.get_data())
        json_data["PRO"] = chaser.reach("armor:prot")
        json_data["ATK"] = chaser.reach('proficiencies:MEL') + chaser.reach('proficiencies:best_weapon:value')
        json_data["SEV"] = chaser.reach("proficiencies:SEV")
        json_data["HAN"] = self.handicap
        json_data["MAR"] = chaser.reach("armor:malus_armure") * (-1)
        json_data["WEA"] = chaser.reach('proficiencies:best_weapon:name')
        json_data["SHI"] = chaser.reach('proficiencies:best_shield:name')
        json_data["avoidance"] = self.avoidance
        return json_data

    def make_avoid(self, diff):
        chaser = Chaser(self.get_data())
        json_data = {}
        self.refresh_from_db()
        avoidance = self.take_avoidance()
        self.refresh()
        base_def = 0
        if avoidance == "R":
            if self.has_shield():
                avoidance = random.choice(["E", "A", "B"])
            else:
                avoidance = random.choice(["E", "A"])
        if avoidance == "E":
            base_def = chaser.reach("proficiencies:DER") + chaser.reach('proficiencies:ESQ')
        elif avoidance == "A":
            base_def = chaser.reach("proficiencies:MEL") + chaser.reach('proficiencies:best_weapon:value')
        elif avoidance == "B":
            base_def = chaser.reach("proficiencies:MEL") + chaser.reach('proficiencies:best_shield:value')

        if len(avoidance) > 0:
            json_data["defense_avoidance"] = avoidance
            json_data["defense_total"], json_data["dmain"] = roll(whole_details=True)
            json_data["defense_total"] += base_def + self.handicap
        else:
            json_data["defense_total"] = 0
        # self.refresh()
        return json_data

    def refresh(self):
        self.save()
        self.refresh_from_db()


    def make_attack(self, foe):
        chaser = Chaser(self.get_data())
        json_data = {}
        avoidance = self.take_avoidance(priorities=["A","R"])
        self.refresh()
        if avoidance != "":
            json_data["consumed_avoidance"] = avoidance
            json_data["attack_total"], json_data["dmain"] = roll(whole_details=True)
            json_data["attack_status"] = avoidance
            json_data["attack_total"] += (chaser.reach("proficiencies:MEL")
                                       + chaser.reach('proficiencies:best_weapon:value') + self.handicap)
            n = Nougardine(self.chosen_diff)
            q, _, _ = n.quality(json_data["attack_total"])
            json_data["attack_quality"] = q
            attack_success = n.success(json_data["attack_total"])
            json_data["attack_success"] = attack_success
            if attack_success:
                json_data["defense"] = foe.make_avoid(self.chosen_diff)
                qd, _, _ = n.quality(json_data["defense"]["defense_total"])
                json_data["defense"]["defense_quality"] = qd
                defense_success = n.success(json_data["defense"]["defense_total"])
                json_data["defense"]["defense_success"] = defense_success
                if not defense_success:
                    dmargin = n.margin(json_data["attack_total"]) - n.margin(json_data["defense"]["defense_total"])
                    json_data["localize"] = self.localize_hit(foe, dmargin)
                    foe.refresh_from_db()
                    print(f"{foe.name} has {foe.vie} hp!!!")
        else:
            json_data["attack_status"] = "X"
        foe.save()
        print(f"{foe.name} has {foe.vie} hp!!!")
        self.refresh()
        return json_data

    def localize_hit(self, foe, dmargin=0):
        chaser = Chaser(self.get_data())
        foe.refresh_from_db()
        json_data = {"loc": {"H": "", "C": "", "AS": "", "AW": "", "LS": "", "LW": ""}}
        dloc = roll(explodes=False)
        dsev = roll(explodes=False)
        json_data["dloc"] = dloc
        json_data["dsev"] = dsev
        dsev += chaser.reach("proficiencies:SEV") + dmargin
        s = Severity()
        e = s.encaissement(dsev)
        json_data["total_severity"] = dsev
        json_data["severity_name"] = e["name"]
        l = Localizer()
        p, r = l.loc_from_die(dloc)
        dmg = e['pdv'] * r - foe.protection_at(p)
        if dmg < 0:
            dmg = 0
        json_data["loc"][p] = f"{dmg}"
        json_data["total_damage"] = dmg
        foe.vie -= dmg
        print(f"{foe.name} --> {foe.vie}")
        foe.save()
        return json_data

    def protection_at(self, p):
        result = 0
        chaser = Chaser(self.get_data())
        armor_str = chaser.reach("armor:cover")
        armors = armor_str.split(" ")
        if p in armors:
            result = chaser.reach("armor:prot")
        return result


class ContestantAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ["combat", "name"]
    list_display = ["name", "vie", "personal_color", "team_color", "fat", "fatigue_line", "rid", "source_rid", "combat",
                    "vie", "fat",
                    "_data"]
    list_editable = []
    list_filter = ["combat", "source_rid"]
    search_filter = ["_data"]
    actions = [refix]
