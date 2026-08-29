from django.db import models
from django.contrib import admin
from django.conf import settings

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.ref_dragonade import CHARACTER_STATISTICS, tai_guidelines, SHORTCUTS, stress_cost
from main.utils.mechanics import as_rid, Nougardine, roll, Severity, Chaser
import math
import random
import json


class Character(models.Model, ChiaroscuroMixin):
    class Meta:
        abstract = True

    name = models.CharField(max_length=256)
    rid = models.CharField(max_length=256, default="", blank=True)
    randomize = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=256, default="", blank=True)
    aka = models.CharField(max_length=256, default="", blank=True)
    figure = models.CharField(max_length=256, default="", blank=True)
    group = models.CharField(max_length=256, default="", blank=True)
    team = models.CharField(max_length=256, default="", blank=True)
    factions = models.CharField(max_length=256, default="", blank=True)
    entrance = models.CharField(max_length=256, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    is_female = models.BooleanField(default=False, blank=True)

    is_lefty = models.BooleanField(default=False, blank=True)
    is_battle_ready = models.BooleanField(default=False, blank=True)
    age = models.PositiveIntegerField(default=20, blank=True)
    height = models.PositiveIntegerField(default=10, blank=True)
    weight = models.PositiveIntegerField(default=50, blank=True)
    SON = models.IntegerField(default=0, blank=True)
    FAB = models.IntegerField(default=0, blank=True)
    REV = models.IntegerField(default=0, blank=True)
    IMP = models.IntegerField(default=0, blank=True)
    ENC = models.FloatField(default=0.0, blank=True)
    SUS = models.IntegerField(default=0, blank=True)
    RES = models.IntegerField(default=0, blank=True)
    FAT = models.IntegerField(default=0, blank=True)
    VIE = models.IntegerField(default=0, blank=True)
    prot = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=9, default="#808080", blank=True)
    team_color = models.CharField(max_length=10, default="", blank=True)
    gamers_team = models.BooleanField(default=False, blank=True)
    gear = models.TextField(max_length=1024, default="", blank=True)
    spells = models.TextField(max_length=1024, default="", blank=True)

    bug_list = models.TextField(default="", max_length=1024, blank=True)

    imc = models.FloatField(default=0, blank=True)
    place = models.CharField(max_length=256, default="", blank=True)
    attributes = models.CharField(max_length=64, default="3 3 3 3 3 3 3 3 3 3 3 3", blank=True)
    secondaries = models.CharField(max_length=64, default="0 0 0 0", blank=True)
    skills_weapons = models.CharField(max_length=128, default="", blank=True)
    skills_generic = models.CharField(max_length=128, default="", blank=True)
    skills_peculiar = models.CharField(max_length=128, default="", blank=True)
    skills_specialized = models.CharField(max_length=128, default="", blank=True)
    skills_knowledge = models.CharField(max_length=128, default="", blank=True)
    skills_draconic = models.CharField(max_length=128, default="", blank=True)
    indice = models.IntegerField(default=0, blank=True)
    indice_attributes = models.IntegerField(default=0, blank=True)
    indice_skills = models.IntegerField(default=0, blank=True)
    tai_guideline = models.CharField(max_length=128, default="", blank=True)
    total_attributes = models.IntegerField(default=0, blank=True)
    total_skills = models.IntegerField(default=0, blank=True)
    # updater = models.TextField(max_length=1024 * 10, default='{}', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    klass = models.CharField(max_length=16, default="Character", blank=True)
    protection_map = models.CharField(max_length=256, blank=True, default="H-0-X C-0-X AS-0-X AW-0-X LS-0-X LW-0-X")

    travel_points = models.IntegerField(default=0, blank=True)
    stress_acquired = models.IntegerField(default=0, blank=True)
    stress_used = models.IntegerField(default=0, blank=True)
    stress_remaining = models.IntegerField(default=0, blank=True)

    description = models.TextField(max_length=1024, default="", blank=True)

    data = {}

    def __str__(self):
        return f"p_{self.id}"

    def make_rid(self):
        # print("Class ===> ", self.type[:3])
        if len(self.rid) == 0:
            self.rid = as_rid(self.name)
            self.rid = self.type[:3].upper() + "_" + self.rid

            # print("New RID", self.rid)

    @property
    def type(self):
        return self.__class__.__name__

    def applyIncDec(self, att, chg):
        self.export_to_json()
        result = False
        offset = 0
        if chg == 'plus':
            offset = 1
        elif chg == 'minus':
            offset = -1

        if offset:
            val = self.value_for(att)
            print(f"{val} type:{type(val).__name__}")
            if type(val).__name__ == "str":
                val = int(val)
            val += offset
            result = self.overwrite_for(att, val)
            if result:
                # self.updateFromStruct()
                self.save()
        return result

    def applyValuePush(self, att, val):
        self.export_to_json()
        result = self.overwrite_for(att, val)
        # print(result)
        if result:
            # self.updateFromStruct()
            self.save()
        return result

    def has_bug(self):
        return len(self.bug_list) > 0

    has_bug.boolean = True

    def fix(self):
        self.chiaroscuro()
        self.initialize()
        self.bug_list = ""
        self.make_rid()
        if len(self.protection_map) == 0:
            self.protection_map = "H-0-X C-0-X AS-0-X AW-0-X LS-0-X LW-0-X"
        if self.birthhour == 0:
            self.birthhour = random.randrange(1, 12)
        self.calc_indice()
        self.challenge_equipment_and_skills()
        self.tai_guideline = tai_guidelines(self.value_for('TAI'))
        if self.height > 0:
            self.imc = math.floor(self.weight / ((self.height / 100) ** 2) * 10) / 10
        secondaries = [0, 0, 0, 0]
        for k in CHARACTER_STATISTICS['SECONDARIES']['LIST']:
            if "FORMULA" in k:
                val = self.from_formula(k['PARAMS'], k['FORMULA'])
                secondaries[k['ORDER']] = str(val)
        self.secondaries = " ".join(secondaries)
        for k in CHARACTER_STATISTICS['MISC']['LIST']:
            if "FORMULA" in k:
                val = self.from_formula(k['PARAMS'], k['FORMULA'])
                setattr(self, k["NAME"], val)
        self.fix_protection_map()
        self.export_to_json()

    def calculate_team(self):
        import hashlib
        gfg = hashlib.blake2s(digest_size=2)
        gfg.update(bytes(self.team, 'UTF-8'))
        x = gfg.digest()
        self.team_color = x.decode('UTF-8')
        return self.team_color

    @classmethod
    def stress_map(cls):
        xspan = [-10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        yspan = [-5, -4, -3, -2, -1, 0]
        for x in xspan:
            if x == -10:
                print(f"{'--------------------- Table de Stress ---------------------':>59}")
                print(f"  V à V+1 ", end="\t")
            else:
                print(f"{x:3} à {x + 1:3} ", end="\t")
            for y in yspan:
                if x >= y:
                    i = stress_cost(x, x + 1, y)
                    print(f"{i:3}", end="\t")
                if x == -10:
                    print(f"{y:3}", end="\t")
            print("")
        print("(Les attributs sont considérés à -5)")

    def calc_indice(self):
        pass
        # # Character.stress_map()
        # from main.utils.ref_dragonade import stress_cost, skill_cost
        # self.indice_attributes = 0
        # self.total_attributes = 0
        #
        # for a in self.attributes.split(" "):
        #     # self.indice_attributes += stress_cost(-5, self.data['attributes'][a], -5)
        #     self.total_attributes += int(a) + 5
        # self.indice_skills = 0
        # for skill_cat in self.data['skills']:
        #     for k, v in self.data['skills'][skill_cat].items():
        #         c, txt = skill_cost(k, v)
        #         if c > -1:
        #             self.indice_skills += c
        # self.indice_attributes = int(self.indice_attributes / 3)
        # self.indice_skills = int(self.indice_skills / 3)
        # self.indice = self.indice_attributes + self.indice_skills
        #
        # self.indice = self.total_attributes - (12 * 4)
        # self.indice += self.data['misc']['SON'] * 3
        # self.total_skills = 0
        # default = 0
        # nondefault_cnt = 0
        # for kc, vc in CHARACTER_STATISTICS['SKILLS'].items():
        #     # print("* ",kc)
        #     for ks in vc['LIST']:
        #         v = self.value_for(ks['NAME'])
        #         default += vc['DEFAULT']
        #         if (v != vc["DEFAULT"]):
        #             nondefault_cnt += 1
        #             self.total_skills += v - vc["DEFAULT"]
        #         # print("** ", ks, v)
        # # print("**** default = ", default, "total non default:", nondefault_cnt, self.name)
        # a, b = self.collect_spells()
        # # print("Total spells", b)
        # self.indice += self.total_skills + b
        # self.indice -= default
        # self.indice += self.data['misc']['PROT'] * 2
        # self.indice += self.data['misc']['SON'] ** 2
        # self.reve = self.data['misc']['SON'] + self.data['misc']['FAB']

    # def updateFromStruct(self):
    #     list = []
    #     for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
    #         list.append(f"{self.data['attributes'][k['NAME']]}")
    #     self.attributes = " ".join(list)
    #
    #     for key, category in CHARACTER_STATISTICS['SKILLS'].items():
    #         list = []
    #         for k in category['LIST']:
    #             vs = f"{self.data['skills'][key.lower()][k['NAME']]}"
    #             list.append(vs)
    #         setattr(self, f"skills_{key.lower()}", " ".join(list))
    #
    #     self.height = int(self.data['features']['HEIGHT'])
    #     self.weight = int(self.data['features']['WEIGHT'])
    #     self.fable = int(self.data['misc']['FAB'])
    #     self.songe = int(self.data['misc']['SON'])
    #     self.entrance = self.data['misc']['ENTRANCE']
    #     self.description = self.data['misc']['DESCRIPTION']
    #     self.age = self.data['features']['AGE']
    #     self.aka = self.data['features']['AKA']
    #     self.is_female = self.data['features']['GENDER'] == "F"
    #     self.is_lefty = self.data['features']['LEFTY'] == "G"
    #     self.gear = self.data['features']['GEAR']
    #     self.spells = self.data['features']['SPELLS']
    #     self.spells_as_list = self.data['features']['SPELLS'].split(" ")

    def ref_to_struct(self, src_ref):
        """        
        :param src_ref: source reference among the user filled properties of the instance 
        :return: nothing / works directly on the instance
        Examples: - self.attributes --> self._data['attributes']
                  - self.skills_generic --> self._data['skills']['generic']
        """
        if len(src_ref) > 0:
            transversal = src_ref.split('_')
            src_struct = CHARACTER_STATISTICS
            for p in transversal:
                src_struct = src_struct[p]
            tlow = transversal[0].lower()
            branch = tlow[:4]
            if len(transversal) == 1:
                if tlow == "attributes":
                    cnt = 0
                    arr = getattr(self, tlow).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
                elif tlow == "secondaries":
                    cnt = 0
                    arr = getattr(self, tlow).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
            elif len(transversal) == 2:
                if tlow == "skills":
                    cnt = 0
                    self._data[branch][transversal[1].lower()] = {}
                    arr = getattr(self, src_ref.lower()).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][transversal[1].lower()][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
            else:
                print(f"!!! Error: Don't know what to do with [{src_ref}]...")

    def skills_summary(self):
        """
            Select only skills with a non default value.
        """
        all = []
        SKILLS = CHARACTER_STATISTICS["SKILLS"]
        count_vals = [0 for _ in range(20)]
        count_postes = [0 for _ in range(6)]
        skill_sets = ["weapons", "generic", "peculiar", "specialized", "knowledge", "draconic"]
        for skill_set in skill_sets:
            REF = SKILLS[skill_set.upper()]
            data = getattr(self, "skills_" + skill_set)
            default = REF["DEFAULT"]
            arr = data.split(" ")
            for item in REF["LIST"]:
                pos = item["ORDER"]
                v = int(arr[pos])
                if v > default:
                    count_postes[default * (-1)] += 1
                    count_vals[v] += 1
                    all.append({"value": v, "category": REF['NAME'][:1], "text": item["TEXT"]})
        sorted_all = sorted(all, key=lambda k: k['text'], reverse=False)
        return sorted_all

    def export_to_json(self):
        self.model_to_data()
        return self._data

    def co_push(self):
        # print("### CO_PUSH character")
        self._data["attr"] = {}
        self._data["seco"] = {}
        self._data["skil"] = {}
        self._data["deri"] = {}

        # self.data['deri'][k['NAME']] = val
        self.ref_to_struct('ATTRIBUTES')
        self.ref_to_struct('SECONDARIES')
        self.ref_to_struct('SKILLS_WEAPONS')
        self.ref_to_struct('SKILLS_GENERIC')
        self.ref_to_struct('SKILLS_PECULIAR')
        self.ref_to_struct('SKILLS_SPECIALIZED')
        self.ref_to_struct('SKILLS_KNOWLEDGE')
        self.ref_to_struct('SKILLS_DRACONIC')
        self._data['fatigue_points'] = self.computeFatigue(self.FAT)
        self._data['has_bug'] = self.has_bug()
        spells_list, b = self.collect_spells()
        self._data['spells'] = spells_list
        self._data['shortcuts'] = self.shortcuts()
        self._data['weapons'] = self.gear_to_weapons()
        self._data['other'] = self.gear_to_other()
        self._data['armors'] = self.gear_to_armors()
        self._data['GENDER'] = self.is_female
        self._data['LEFTY'] = self.is_lefty
        self._data["skills_summary"] = self.skills_summary()
        self._data['roster_text'] = self.roster_as_text()
        from datetime import datetime
        now = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        self._data['last_update'] = now

    def computeFatigue(self, x):
        i = 1
        pf = 0
        while i <= x:
            pf += 2 + math.ceil(i / 2)
            i += 1
        return pf

    def gear_to_weapons(self):
        from main.models.equipment import Equipment
        list = []
        weapons = Equipment.objects.filter(category__in=['mel', 'tir', 'lan'], rid__in=self.gear.split(" ")).order_by(
            "category")
        for weapon in weapons:
            stat_value = self.value_for(weapon.category.upper())
            skill = self.value_for(weapon.related_skill.upper())
            # All data for the weapon
            d = weapon.export_to_json()
            # Data specific to the character applied to the wepon's data
            d['stat_value'] = stat_value
            d['related_skill_value'] = skill
            d['related_skill_text'] = "Poignards"
            d['stat_skill'] = f"{stat_value}+{skill}={int(stat_value) + int(skill)}"
            list.append(d)
        return list

    def gear_to_other(self):
        from main.models.equipment import Equipment
        list = []
        # others = Equipment.objects.exclude(category__in=['mel', 'tir', 'lan']).filter(
        #     rid__in=self.gear.split(" ")).order_by("category")
        # for other in others:
        #     list.append({
        #         "name": other.name,
        #         "category": other.category
        #     })
        return list

    def gear_to_armors(self):
        from main.models.equipment import Equipment
        list = []
        pmap = {}
        words = self.protection_map.split(" ")
        for word in words:
            if len(word) > 0:
                pieces = word.split("-")
                pmap[pieces[0]] = {"protection": pieces[1], "source": pieces[2]}
        armors = Equipment.objects.filter(prot__gte=1, rid__in=self.gear.split(" ")).order_by("materiaux")
        for armor in armors:
            x = armor.prot
            a = armor.export_to_json()
            a["numeric_cover"] = ""
            parts = armor.cover.split(" ")
            for part in parts:
                print(a["numeric_cover"])
                if part == "-":
                    a["numeric_cover"] += f"0 "
                else:
                    a["numeric_cover"] += f"{x} "
            a["numeric_cover"].strip()
            list.append(a)
        return list

    def collect_spells(self):
        from main.models.incantessimi import Incantessimo
        indice_points = 0
        list = []
        # spells = Incantessimo.objects.filter(rid__in=self.spells.split(" ")).order_by("category")
        # for spell in spells:
        #     roll = 0
        #     if spell.roll > 0:
        #         roll += self.value_for(f"DRA_{spell.roll+1:02}")
        #     roll += self.value_for(f"REV")
        #     list.append({
        #         "name": spell.name,
        #         "roll": roll,
        #         "diff": spell.diff,
        #         "dps": spell.dps,
        #         "category": spell.get_category_display(),
        #         "path": spell.path,
        #         'roll_str': spell.get_roll_display(),
        #         'path_str': spell.get_path_display(),
        #         'category_str': spell.get_category_display()
        #     })
        #     indice_points += spell.diff / 5
        sorted_all = sorted(list, key=lambda k: k['diff'], reverse=True)
        return sorted_all, indice_points

    def shortcuts(self):
        list = []
        # for sc in SHORTCUTS:
        #     attr = self.value_for(sc[1])
        #     skill = self.value_for(sc[2])
        #     # print(sc, attr, skill)
        #     list.append({
        #         "roll": sc[0],
        #         "val": attr + skill
        #     })
        return list

    def from_formula(self, params, formula):
        pvalues = []
        for p in params.split(" "):
            if len(p) > 0:
                val = int(self.value_for(p))
                pvalues.append(val)
        return formula(pvalues)

    def value_for(self, str):
        # print(f"### Value for")
        result = -1000
        where = self.index_for(str)
        entry = self.entry_for(where, str)
        if entry != {}:
            # print(f"### Values : {str} => {where}")
            if "ORDER" in entry:
                verbs = where.lower().split(':')
                datalist = getattr(self, "_".join(verbs))
                # print(f"Key:{'_'.join(verbs):20} Value:{datalist} [Type:{type(datalist)}]")
                # print(f"### ORDER = {entry['ORDER']}")
                if type(datalist).__name__ == 'str':
                    parts = datalist.split(" ")
                    result = parts[entry["ORDER"]]
                else:
                    result = datalist[entry["ORDER"]]
                # print(f"### Result = {result}")
            else:
                result = getattr(self, entry['NAME'])
        return result

    def overwrite_for(self, str, val):
        # print("OVERWRITE FOR")
        result = False
        where = self.index_for(str)
        entry = self.entry_for(where, str)
        if entry != {}:
            if "ORDER" in entry:
                verbs = where.lower().split(':')
                # print(f"***Trying to get {'_'.join(verbs)}")
                datalist = getattr(self, "_".join(verbs))
                # print(f"*** {datalist} type:{type(datalist)}")
                parts = datalist.split(" ")
                parts[entry["ORDER"]] = f"{val}"
                setattr(self, "_".join(verbs), " ".join(parts))
                self.save()
                result = True
            else:
                setattr(self, entry['NAME'], val)
                self.save()
                result = True
        return result

    def entry_for(self, str, stat):
        """
            :param str: the dataset_name
            :param: stat: the value that entry must match with property NAME
            :returns: the full entry, or {}
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        root = CHARACTER_STATISTICS
        result = {}
        if len(str) > 0:
            words = str.upper().split(':')
            for word in words:
                root = root[word]
            for item in root["LIST"]:
                if item["NAME"] == stat:
                    result = item
        return result

    def index_for(self, str):
        """
        @params str: The code for the stat
        @returns the position in the description as a:b:c
        """
        from main.utils.ref_dragonade import known
        choices = ["ATTRIBUTES", "SKILLS:WEAPONS", "SKILLS:GENERIC", "SKILLS:PECULIAR", "SKILLS:SPECIALIZED", "SKILLS:KNOWLEDGE", "SKILLS:DRACONIC",
                   "SECONDARIES", "MISC", "FEATURES"]
        for choice in choices:
            result = known(choice, str)
            if len(result) > 0:
                break
        return result

    def json_dump(self):
        pass
        # import os
        # filename = f'{self.rid}.json'
        # json_name = os.path.join(settings.MEDIA_ROOT, 'datablocks/' + filename)
        # js = json.dumps(self.data)
        # with open(json_name, "w") as f:
        #     f.write(js)
        #     f.close()

    def initialize(self):
        """
            Set the attributes and skills_x properties with default values according to reference.
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        if len(self.attributes) == 0:
            list = []
            for att in CHARACTER_STATISTICS['ATTRIBUTES']:
                list.append("3")
            self.attributes = " ".join(list)
        if len(self.secondaries) == 0:
            list = []
            for att in CHARACTER_STATISTICS['SECONDARIES']:
                list.append("0")
            self.secondaries = " ".join(list)
        for k, cat in CHARACTER_STATISTICS['SKILLS'].items():
            list = []
            for item in cat['LIST']:
                list.append(f"{cat['DEFAULT']}")
            tgt_property = f"skills_{k.lower()}"
            if len(getattr(self, tgt_property)) == 0:
                setattr(self, tgt_property, " ".join(list))

    def roster(self):
        # return "Disabled for now."
        lines = []
        lines.append(f"{self.name}")
        if self.aka != "":
            lines.append(f"{self.aka}")
        if self.entrance != "":
            lines.append(f"{self.entrance}")
        if self.title != "":
            lines.append(f"{self.title}")
        ty = "Créature"
        subty = ""
        if self.type == "Viaggiatore":
            ty = f"({self.player})"
        if self.type == "Nativo":
            ty = "Autochtone"
        if self.type == "Creatura":
            subty = (f" ({self.get_creature_type_display()})")
            ty += subty

        lines.append(f"{ty}")
        attributes = ""
        space = "§"
        x = 0
        a = ["", "", "", ""]
        for k, v in self._data["attr"].items():
            a[x % 4] += f"{k} {v!s:{space}>2} "
            x += 1
        x = 0
        for k, v in self._data["seco"].items():
            a[x % 4] += f"| {k} {v!s:{space}>2} "
            x += 1
        x = 0
        m = ["VIE", "FAT", "SUS", "RES"]
        for v in m:
            a[x % 4] += f"| {v} {getattr(self, v)!s:{space}>2} "
            x += 1
        x = 0
        m = ["IMP", "ENC", "FAB", "REV"]
        for v in m:
            a[x % 4] += f"| {v} {getattr(self, v)!s:{space}>2} "
            x += 1
        attributes = f"{a[0]}<br/>{a[1]}<br/>{a[2]}<br/>{a[3]}<br/>"
        lines.append(attributes)

        categories = {
            "M": {"title": "Martiales (-1)", "list": []},
            "G": {"title": "Génériques (-1)", "list": []},
            "P": {"title": "Particulières (-2)", "list": []},
            "S": {"title": "Spécifiques (-3)", "list": []},
            "C": {"title": "Connaissances (-4)", "list": []},
            "D": {"title": "Draconiques (-5)", "list": []}
        }
        for v in self._data["skills_summary"]:
            categories[v["category"]]["list"].append(f"{v['text']} {v['value']:2}")

        skills = ""
        for k, v in categories.items():
            skills += v["title"] + ": "
            skills += ", ".join(v["list"]) + ".<BR/>"
        lines.append(skills)

        life = "PdV<br/>"
        for x in range(self.VIE):
            life += "&#9744; "
            if x % 5 == 4:
                life += "<br/>"
        life += "<br/>"
        fatigue = "PdF<br/> "
        len = 6
        for x in range(self.FAT, 0, -1):
            for y in range(10):
                if y < len:
                    fatigue += f"&#9744; "
                else:
                    if x % 2 == 1:
                        len -= 1
                        break
            fatigue = fatigue + "<br/>"
        fatigue += "<BR/>"

        # weapons = f"{'Arme':{space}<20} {'1M':{space}>4} /{'2M':{space}>4} INIT Score</BR>"
        # for w in self.data['features']['weapons']:
        #     weapons += f"{w['name']:{space}<20} "
        #     if w['category'] == "mel":
        #         if w['dom_1'] != '-':
        #             d1 = f"{w['dom_1']}+{dom}"
        #             weapons += f"{d1:{space}>4} "
        #         else:
        #             weapons += f"{'-':{space}>4} "
        #         weapons += "/"
        #         if w['dom_2'] != '-':
        #             d2 = f"{w['dom_2']}+{math.floor(dom * 1.5)}"
        #             weapons += f"{d2:{space}>4} "
        #         else:
        #             weapons += f"{'-':{space}>4} "
        #     else:
        #         weapons += f"{w['dom_1']:{space}>10} "
        #     weapons += f" {w['init']:{space}>4} {w['score']:{space}>5}</BR>"
        # lines.append(weapons)
        # lines.append(f"Description: {self.data['misc']['DESCRIPTION']}</BR>")
        # if self.data['features']['armors']:
        #     protection = f"{'Protection':{space}<35}{'Malus':{space}>7}{'Prot':{space}>6}<br/>"
        #     for a in self.data['features']['armors']:
        #         protection += f"{a['name']:{space}<35}{a['malus_armure']:{space}>7}{a['prot']:{space}>6}</BR>"
        #     lines.append(protection)
        lines.append(life)
        lines.append(fatigue)
        return lines

    def pre_sim(self, combat, name="", occurrence=0, color=""):
        from main.models.contestants import Contestant
        all = Contestant.objects.filter(name=name, combat=combat)
        if len(all) == 0:
            a = Contestant()
        else:
            a = all.first()
        a.combat = combat

        a.collect_from_rid(self.rid, self.type, color=color)
        if len(name) > 0:
            a.name = name
        else:
            a.name = a.name + f"___{occurrence}"
        return a

    def roster_as_text(self):
        roster = "<br/>".join(self.roster())
        roster = roster.replace("§", "&nbsp;")
        return roster

    @classmethod
    def find_from_rid(cls, rid):
        from main.models.viaggiatori import Viaggiatore
        from main.models.nativi import Nativo
        from main.models.creature import Creatura
        viaggiatori = Viaggiatore.objects.filter(rid=rid)
        nativi = Nativo.objects.filter(rid=rid)
        creature = Creatura.objects.filter(rid=rid)
        item = None
        if len(viaggiatori) == 1:
            item = viaggiatori.first()
        elif len(nativi) == 1:
            item = nativi.first()
        elif len(creature) == 1:
            item = creature.first()
        return item

    def challenge_equipment_and_skills(self):
        weapons = self.gear_to_weapons()
        # bugs = []
        # for weapon in weapons:
        #     if self.value_for(weapon['skill']) == 0:
        #         bugs.append(f"Arme trouvée pour laquelle le personnage n'a pas de compétence... {weapon['name']} {weapon['skill']}")
        # self.bug_list = "\n".join(bugs)

    def fix_protection_map(self):
        armors = self.gear_to_armors()
        map = {}
        parts = self.protection_map.split(" ")
        for part in parts:
            x = part.split("-")
            map[x[0]] = {"Part":x[0],"Prot":0,"Str":x[2]}
        for armor in armors:
            pro = armor["prot"]
            covers = armor["cover"].split(" ")
            for cover in covers:
                if cover in ["H"]:
                    p = "H"
                elif cover in ["C","T"]:
                    p = "C"
                elif cover in ["AS", "SA"]:
                    p = "AS"
                elif cover in ["AW", "WA"]:
                    p = "AW"
                elif cover in ["SL", "LS"]:
                    p = "LS"
                elif cover in ["WL", "LW"]:
                    p = "LW"
                else:
                    p = ""
                if len(p)>0:
                    map[p]["Prot"] += pro
        pmap = []
        print(map)
        for k,m in map.items():
            print(m,k)
            pmap.append(f'{m["Part"]}-{m["Prot"]}-{m["Str"]}')
        self.protection_map = " ".join(pmap)