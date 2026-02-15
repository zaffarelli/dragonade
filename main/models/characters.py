from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS, tai_guidelines, SHORTCUTS
from main.utils.mechanics import as_rid, Nougardine, roll, Severity, Chaser
import math
import random
import json


class Character(models.Model):
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
    songe = models.IntegerField(default=0, blank=True)
    reve = models.IntegerField(default=0, blank=True)
    prot = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=9, default="#808080", blank=True)
    team_color = models.CharField(max_length=10, default="", blank=True)
    gamers_team = models.BooleanField(default=False, blank=True)
    gear = models.TextField(max_length=1024, default="", blank=True)
    spells = models.TextField(max_length=1024, default="", blank=True)

    imc = models.FloatField(default=0, blank=True)
    place = models.CharField(max_length=256, default="", blank=True)
    attributes = models.CharField(max_length=64, default="", blank=True)
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
    updater = models.TextField(max_length=8192, default='{}', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    klass = models.CharField(max_length=16, default="Character", blank=True)
    data = {}

    def __str__(self):
        return f"p_{self.id}"

    def make_rid(self):
        # print("Class ===> ", self.type[:3])
        if len(self.rid) == 0:
            self.rid = as_rid(self.name)
            self.rid = self.type[:3].upper() + "__" + self.rid

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
            val += offset
            result = self.overwrite_for(att, val)
            if result:
                self.updateFromStruct()
                self.save()
        return result

    def applyValuePush(self, att, val):
        self.export_to_json()
        result = self.overwrite_for(att, val)
        # print(result)
        if result:
            self.updateFromStruct()
            self.save()
        return result

    def fix(self):
        # print("Fixing!")
        self.make_rid()
        if self.birthhour == 0:
            self.birthhour = random.randrange(1, 12)
        self.export_to_json()
        self.calc_indice()
        # self.calculate_team()

        self.tai_guideline = tai_guidelines(self.data['attributes']['TAI'])
        if self.height > 0:
            self.imc = math.floor(self.weight / ((self.height / 100) ** 2) * 10) / 10
        self.updater = self.toJson()
        self.json_dump()

    def calculate_team(self):
        import hashlib
        gfg = hashlib.blake2s(digest_size=2)
        gfg.update(bytes(self.team, 'UTF-8'))
        x = gfg.digest()
        self.team_color = x.decode('UTF-8')
        return self.team_color

    def calc_indice(self):
        from main.utils.ref_dragonade import stress_cost, skill_cost
        self.indice_attributes = 0
        self.total_attributes = 0

        for a in self.data['attributes']:
            self.indice_attributes += stress_cost(-5, self.data['attributes'][a], -5)
            self.total_attributes += self.data['attributes'][a]
        self.indice_skills = 0
        for skill_cat in self.data['skills']:
            for k, v in self.data['skills'][skill_cat].items():
                c, txt = skill_cost(k, v)
                if c > -1:
                    self.indice_skills += c
        self.indice_attributes = int(self.indice_attributes / 3)
        self.indice_skills = int(self.indice_skills / 3)
        self.indice = self.indice_attributes + self.indice_skills

        self.indice = self.total_attributes - (12 * 4)
        self.indice += self.data['misc']['SON'] * 3
        self.total_skills = 0
        default = 0
        nondefault_cnt = 0
        for kc, vc in CHARACTER_STATISTICS['SKILLS'].items():
            # print("* ",kc)
            for ks in vc['LIST']:
                v = self.value_for(ks['NAME'])
                self.total_skills += v
                default += vc['DEFAULT']
                if (v != vc["DEFAULT"]):
                    nondefault_cnt += 1
                # print("** ", ks, v)
        # print("**** default = ", default, "total non default:", nondefault_cnt, self.name)
        a, b = self.collect_spells()
        # print("Total spells", b)
        self.indice += self.total_skills + b
        self.indice -= default
        self.indice += self.data['misc']['PROT'] * 2
        self.indice += self.data['misc']['SON'] ** 2
        self.reve = self.data['misc']['SON'] + self.data['misc']['FAB']

    def updateFromStruct(self):
        list = []
        for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
            list.append(f"{self.data['attributes'][k['NAME']]}")
        self.attributes = " ".join(list)

        for key, category in CHARACTER_STATISTICS['SKILLS'].items():
            list = []
            for k in category['LIST']:
                vs = f"{self.data['skills'][key.lower()][k['NAME']]}"
                list.append(vs)
            setattr(self, f"skills_{key.lower()}", " ".join(list))

        self.height = int(self.data['features']['HEIGHT'])
        self.weight = int(self.data['features']['WEIGHT'])
        self.fable = int(self.data['misc']['FAB'])
        self.songe = int(self.data['misc']['SON'])
        self.entrance = self.data['misc']['ENTRANCE']
        self.age = self.data['features']['AGE']
        self.aka = self.data['features']['AKA']
        self.is_female = self.data['features']['GENDER'] == "F"
        self.is_lefty = self.data['features']['LEFTY'] == "G"
        self.gear = self.data['features']['GEAR']
        self.spells = self.data['features']['SPELLS']
        # self.spells_as_list = self.data['features']['SPELLS'].split(" ")

    def ref_to_struct(self, src_ref):
        """        
        :param src_ref: source reference among the user filled properties of the instance 
        :return: nothing / works directly on the instance
        Examples: - self.attributes --> self.data['attributes']
                  - self.skills_generic --> self.data['skills']['generic']
        """
        if len(src_ref) > 0:
            transversal = src_ref.split('_')
            src_struct = CHARACTER_STATISTICS
            for p in transversal:
                src_struct = src_struct[p]
            if len(transversal) == 1:
                # Attributes
                cnt = 0
                list = getattr(self, transversal[0].lower()).split(' ')
                for item in src_struct['LIST']:
                    self.data[transversal[0].lower()][item['NAME']] = int(list[cnt]) if cnt < len(list) else src_struct[
                        'DEFAULT']
                    cnt += 1
            elif len(transversal) == 2:
                # Skills
                cnt = 0
                list = getattr(self, src_ref.lower()).split(' ')
                for item in src_struct['LIST']:
                    self.data[transversal[0].lower()][transversal[1].lower()][item['NAME']] = int(
                        list[cnt]) if cnt < len(list) else src_struct['DEFAULT']
                    cnt += 1

    def skills_summary(self):
        all = []
        count_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        count_postes = [0, 0, 0, 0, 0, 0]
        for kc, vc in self.data['skills'].items():
            default = CHARACTER_STATISTICS["SKILLS"][kc.upper()]["DEFAULT"]
            for ks, vs in vc.items():
                if vs > default:
                    count_postes[default * (-1)] += 1
                    count_vals[vs] += 1
                    for r in CHARACTER_STATISTICS["SKILLS"][kc.upper()]["LIST"]:
                        if r['NAME'] == ks:
                            all.append({"value": vs, "category": CHARACTER_STATISTICS["SKILLS"][kc.upper()]['NAME'][:1],
                                        "text": r["TEXT"]})
        sorted_all = sorted(all, key=lambda k: k['text'], reverse=True)
        # print("Values=", count_vals)
        # print("Postes=", count_postes)
        return sorted_all

    def export_to_json(self):
        self.data = {}
        self.data['rid'] = self.rid
        self.data['id'] = self.id
        self.data['name'] = self.name
        self.data['attributes'] = {}
        self.data['secondaries'] = {}
        self.data['skills'] = {'weapons': {}, 'generic': {}, 'peculiar': {}, 'specialized': {}, 'knowledge': {},
                               'draconic': {}}
        self.data['misc'] = {}
        self.data['type'] = self.type
        self.data['features'] = {}

        # The initialize function must implement controls to stay safe if data exists
        self.initialize()

        self.ref_to_struct('ATTRIBUTES')
        self.ref_to_struct('SKILLS_WEAPONS')
        self.ref_to_struct('SKILLS_GENERIC')
        self.ref_to_struct('SKILLS_PECULIAR')
        self.ref_to_struct('SKILLS_SPECIALIZED')
        self.ref_to_struct('SKILLS_KNOWLEDGE')
        self.ref_to_struct('SKILLS_DRACONIC')

        for k in CHARACTER_STATISTICS['SECONDARIES']['LIST']:
            if "FORMULA" in k:
                val = self.fromFormula(k['PARAMS'], k['FORMULA'])
                self.data['secondaries'][k['NAME']] = val

        for k in CHARACTER_STATISTICS['MISC']['LIST']:
            if "FORMULA" in k:
                val = self.fromFormula(k['PARAMS'], k['FORMULA'])
                self.data['misc'][k['NAME']] = val

        self.data['misc']['ENTRANCE'] = self.entrance
        self.data['misc']['indice_a'] = self.indice_attributes
        self.data['misc']['indice_s'] = self.indice_skills
        self.data['misc']['indice'] = self.indice
        self.data['misc']['total_attributes'] = self.total_attributes
        self.data['misc']['total_skills'] = self.total_skills
        self.data['misc']['groupe'] = self.group
        self.data['misc']['team'] = self.team
        self.data['misc']['title'] = self.title
        self.data['misc']['SON'] = self.songe
        self.data['misc']['REV'] = self.reve
        self.data['misc']['PROT'] = self.prot

        self.data['features']['HEIGHT'] = self.height
        self.data['features']['WEIGHT'] = self.weight
        self.data['features']['imc'] = self.imc
        self.data['features']['tai_guideline'] = self.tai_guideline
        self.data['features']['GEAR'] = self.gear
        self.data['features']['SPELLS'] = self.spells

        self.data['features']['AGE'] = self.age
        self.data['features']['AKA'] = self.aka
        self.data['features']['FIGURE'] = self.figure
        self.data['features']['GENDER'] = "F" if self.is_female else "M"
        self.data['features']['LEFTY'] = "G" if self.is_lefty else "D"

        self.data['features']['weapons'] = self.gear_to_weapons()
        self.data['features']['other'] = self.gear_to_other()
        self.data['features']['armors'] = self.gear_to_armors()
        a, b = self.collect_spells()
        self.data['features']['spells'] = a
        self.data['features']['shortcuts'] = self.shortcuts()

        self.data['birthhour'] = self.birthhour
        self.data['color'] = self.color
        self.data['misc']['pf'] = self.computeFatigue(self.data['misc']['FAT'])
        self.data["skills_summary"] = self.skills_summary()

        self.data['priority'] = self.priority
        self.data['roster_text'] = self.roster_as_text()

        self.json_dump()
        # return self.data

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
            stat = self.value_for(weapon.category.upper())
            half_stat = int(math.ceil(stat / 2))
            skill = self.value_for(weapon.related_skill.upper())
            # print(stat, skill)
            list.append({
                "name": weapon.name,
                "category": weapon.category,
                "dom_1": weapon.mod_dom + weapon.plus_dom if weapon.plus_dom > 0 else "-",
                "dom_2": weapon.mod_dom + weapon.plus_dom_2m if weapon.plus_dom_2m > 0 else "-",
                "init": half_stat + skill + weapon.mod_ini,
                "score": stat + skill + weapon.mod_att,
                "skill": weapon.related_skill.upper(),
            })
        return list

    def gear_to_other(self):
        from main.models.equipment import Equipment
        list = []
        others = Equipment.objects.exclude(category__in=['mel', 'tir', 'lan']).filter(
            rid__in=self.gear.split(" ")).order_by("category")
        for other in others:
            list.append({
                "name": other.name,
                "category": other.category
            })
        return list

    def gear_to_armors(self):
        from main.models.equipment import Equipment
        list = []
        armors = Equipment.objects.filter(prot__gte=1, rid__in=self.gear.split(" ")).order_by("materiaux")
        for armor in armors:
            list.append({
                "name": armor.name,
                "prot": armor.prot,
                "cover": armor.cover,
                "materiaux": armor.materiaux,
                "skill": armor.related_skill,
                "malus_armure": armor.malus_armure
            })
            if self.prot < armor.prot:
                self.prot = armor.prot
        return list

    def collect_spells(self):
        from main.models.stregoneria import Spell
        indice_points = 0
        list = []
        spells = Spell.objects.filter(rid__in=self.spells.split(" ")).order_by("category")
        for spell in spells:
            roll = self.value_for(f"DRA_{spell.roll:02}")
            roll += self.value_for(f"FAB")
            list.append({
                "name": spell.name,
                "roll": roll,
                "diff": spell.diff,
                "dps": spell.dps,
                "category": spell.get_category_display(),
                "path": spell.path,
                'roll_str': spell.get_roll_display(),
                'path_str': spell.get_path_display(),
                'category_str': spell.get_category_display()
            })
            indice_points += spell.diff / 5
        sorted_all = sorted(list, key=lambda k: k['diff'], reverse=True)
        return sorted_all, indice_points

    def shortcuts(self):
        list = []
        for sc in SHORTCUTS:
            attr = self.value_for(sc[1])
            skill = self.value_for(sc[2])
            # print(sc, attr, skill)
            list.append({
                "roll": sc[0],
                "val": attr + skill
            })
        return list

    def fromFormula(self, params, formula):
        pvalues = []
        for p in params.split(" "):
            pvalues.append(self.value_for(p))
        return formula(pvalues)

    def toJson(self):
        self.export_to_json()
        struct = json.loads(json.dumps(self.data))
        return struct

    def value_for(self, str):
        # from main.utils.ref_dragonade import CHARACTER_STATISTICS
        result = -1000
        where = self.index_for(str)
        # print("value ", str, " found in ", where)
        if len(where) > 0:
            words = where.split(':')
            # print(self.data)
            if len(words) == 1:
                result = self.data[words[0].lower()][str]
            else:
                result = self.data[words[0].lower()][words[1].lower()][str]
        return result

    def entry_for(self, str, stat):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        # result = -1000
        # where = self.index_for(str)

        root = CHARACTER_STATISTICS
        result = {}
        if len(str) > 0:
            words = str.upper().split(':')
            for word in words:
                root = root[word]
            for item in root["LIST"]:
                if item["NAME"] == stat:
                    # print(item)
                    result = item
            # # print(self.data)
            # if len(words) == 1:
            #     result = self.data[words[0].lower()][str]
            # else:
            #     result = self.data[words[0].lower()][words[1].lower()][str]
        return result

    def best_for(self, str):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        words = str.split(":")
        root = CHARACTER_STATISTICS
        for word in words:
            root = root[word]
        data_set = root["KNOWN"]
        # print(data_set)
        result = "???", 0, "???"
        txt = ""
        max = -1000
        for elem in data_set:
            val = self.value_for(elem)
            if val >= max:
                max = val
                x = self.entry_for(str, elem)
                txt = x["TEXT"]
                r = f"{elem} => {val} ({str}) {txt}"
                result = val, elem, txt
        # print("Found: " + r)
        return result

    def overwrite_for(self, str, val):
        # print("OVERWRITE FOR")
        result = False
        where = self.index_for(str)
        # print("value ", str, " found in ", where)
        if len(where) > 0:
            words = where.split(':')
            # print("words ", words)
            if len(words) == 1:
                self.data[words[0].lower()][str] = val
                # print("-->where 1 ", words[0].lower(), str)
                result = True
            else:
                self.data[words[0].lower()][words[1].lower()][str] = val
                # print("-->where 1 ", words[0].lower(), words[1].lower(), str)
                result = True
        # print(self.data)
        return result

    def index_for(self, str):
        """
        @params str: The code for the stat
        @returns the position in the description as a:b:c
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        # print(str.upper())
        if str.upper() in CHARACTER_STATISTICS['ATTRIBUTES']['KNOWN']:
            result = "ATTRIBUTES"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['KNOWN']:
            result = "SKILLS:WEAPONS"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['GENERIC']['KNOWN']:
            result = "SKILLS:GENERIC"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['PECULIAR']['KNOWN']:
            result = "SKILLS:PECULIAR"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['SPECIALIZED']['KNOWN']:
            result = "SKILLS:SPECIALIZED"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['KNOWLEDGE']['KNOWN']:
            result = "SKILLS:KNOWLEDGE"
        elif str.upper() in CHARACTER_STATISTICS['SKILLS']['DRACONIC']['KNOWN']:
            result = "SKILLS:DRACONIC"
        elif str.upper() in CHARACTER_STATISTICS['SECONDARIES']['KNOWN']:
            result = "SECONDARIES"
        elif str.upper() in CHARACTER_STATISTICS['MISC']['KNOWN']:
            result = "MISC"
        elif str.upper() in CHARACTER_STATISTICS['FEATURES']['KNOWN']:
            result = "FEATURES"
        else:
            result = ""
        return result

    def json_dump(self):
        import os
        filename = f'{self.rid}.json'
        json_name = os.path.join(settings.MEDIA_ROOT, 'datablocks/' + filename)
        js = json.dumps(self.data)
        with open(json_name, "w") as f:
            f.write(js)
            f.close()

    def initialize(self):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        if len(self.attributes) == 0:
            list = []
            for att in CHARACTER_STATISTICS['ATTRIBUTES']:
                list.append("4")
            self.attributes = " ".join(list)
        for k, cat in CHARACTER_STATISTICS['SKILLS'].items():
            list = []
            for item in cat['LIST']:
                list.append(f"{cat['DEFAULT']}")
            tgt_property = f"skills_{k.lower()}"
            if len(getattr(self, tgt_property)) == 0:
                setattr(self, tgt_property, " ".join(list))

    def roster(self):
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
        if self.type == "Traveller":
            ty = f"({self.player})"
        if self.type == "Autochton":
            ty = "Autochtone"
        if self.type == "Creature":
            subty = (f" ({self.get_creature_type_display()})")
            ty += subty

        lines.append(f"{ty}")
        attributes = ""
        space = "§"
        x = 0
        a = ["", "", "", ""]
        for k, v in self.data["attributes"].items():
            a[x % 4] += f"{k} {v!s:{space}>2} "
            x += 1
        x = 0
        for k, v in self.data["secondaries"].items():
            a[x % 4] += f"| {k} {v!s:{space}>2} "
            x += 1
        x = 0
        m = ["VIE", "FAT", "SUS", "SCO"]
        for v in m:
            a[x % 4] += f"| {v} {self.data['misc'][v]!s:{space}>2} "
            x += 1
        x = 0
        m = ["DOM", "ENC", "FAB", "REV"]
        dom = self.data['misc']["DOM"]
        for v in m:
            a[x % 4] += f"| {v} {int(self.data['misc'][v])!s:{space}>2} "
            x += 1
        attributes = f"{a[0]}<br/>{a[1]}<br/>{a[2]}<br/>{a[3]}<br/>"
        lines.append(attributes)

        categories = {
            "M": {"title": "Armes (0)", "list": []},
            "G": {"title": "Génériques (-1)", "list": []},
            "P": {"title": "Particulières (-2)", "list": []},
            "S": {"title": "Spécifiques (-3)", "list": []},
            "C": {"title": "Connaissances (-4)", "list": []},
            "D": {"title": "Draconiques (-5)", "list": []}
        }
        for v in self.data["skills_summary"]:
            categories[v["category"]]["list"].append(f"{v['text']} {v['value']:2}")

        skills = ""
        for k, v in categories.items():
            skills += v["title"] + ": "
            skills += ", ".join(v["list"]) + ".<BR/>"
        lines.append(skills)

        life = "VIE: "
        for x in range(self.data["misc"]["VIE"]):
            life += "&#9744;"
            if x % 5 == 4:
                life += "&nbsp;"
        life += "<br/>"
        fatigue = "FAT: "
        len = 6
        for x in range(self.data['misc']['FAT'], 0, -1):
            for y in range(10):
                if y < len:
                    fatigue += f"&#9744;"
                else:
                    if x % 2 == 1:
                        len -= 1
                        break
            fatigue = fatigue + "o "
        fatigue += "<BR/>"

        weapons = f"{'Arme':{space}<20} {'1M':{space}>4} /{'2M':{space}>4} INIT Score</BR>"
        for w in self.data['features']['weapons']:
            weapons += f"{w['name']:{space}<20} "
            if w['category'] == "mel":
                if w['dom_1'] != '-':
                    d1 = f"{w['dom_1']}+{dom}"
                    weapons += f"{d1:{space}>4} "
                else:
                    weapons += f"{'-':{space}>4} "
                weapons += "/"
                if w['dom_2'] != '-':
                    d2 = f"{w['dom_2']}+{math.floor(dom * 1.5)}"
                    weapons += f"{d2:{space}>4} "
                else:
                    weapons += f"{'-':{space}>4} "
            else:
                weapons += f"{w['dom_1']:{space}>10} "
            weapons += f" {w['init']:{space}>4} {w['score']:{space}>5}</BR>"
        lines.append(weapons)
        if self.data['features']['armors']:
            protection = f"{'Protection':{space}<35}{'Malus':{space}>7}{'Prot':{space}>6}<br/>"
            for a in self.data['features']['armors']:
                protection += f"{a['name']:{space}<35}{a['malus_armure']:{space}>7}{a['prot']:{space}>6}</BR>"
            lines.append(protection)
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

        a.collect_from_rid(self.rid, self.type, color=color if self.type == "Creature" else self.color)
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
        from main.models.travellers import Traveller
        from main.models.autochtons import Autochton
        from main.models.creatures import Creature
        travellers = Traveller.objects.filter(rid=rid)
        autochtons = Autochton.objects.filter(rid=rid)
        creatures = Creature.objects.filter(rid=rid)
        item = None
        if len(travellers) == 1:
            item = travellers.first()
        elif len(autochtons) == 1:
            item = autochtons.first()
        elif len(creatures) == 1:
            item = creatures.first()
        return item
