from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS, tai_guidelines, SHORTCUTS
from main.utils.mechanics import as_rid
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
    group = models.CharField(max_length=256, default="", blank=True)
    team = models.CharField(max_length=256, default="", blank=True)
    factions = models.CharField(max_length=256, default="", blank=True)
    entrance = models.CharField(max_length=256, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    is_female = models.BooleanField(default=False, blank=True)
    is_lefty = models.BooleanField(default=False, blank=True)
    age = models.PositiveIntegerField(default=20, blank=True)
    height = models.PositiveIntegerField(default=10, blank=True)
    weight = models.PositiveIntegerField(default=50, blank=True)
    songe = models.IntegerField(default=0, blank=True)
    reve = models.IntegerField(default=0, blank=True)
    prot = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=9, default="#808080", blank=True)
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
    updater = models.TextField(max_length=8192, default='{}', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    data = {}

    def __str__(self):
        return f"p_{self.id}"

    def make_rid(self):
        if self.name is not None:
            self.rid = as_rid(self.name)

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
        print(result)
        if result:
            self.updateFromStruct()
            self.save()
        return result

    def fix(self):
        self.make_rid()
        if self.birthhour == 0:
            self.birthhour = random.randrange(1, 12)
        self.export_to_json()
        self.calc_indice()
        self.tai_guideline = tai_guidelines(self.data['attributes']['TAI'])
        if self.height > 0:
            self.imc = math.floor(self.weight / ((self.height / 100) ** 2) * 10) / 10
        self.updater = self.toJson()
        self.json_dump()

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
        total_skills = 0
        default = 0
        nondefault_cnt = 0
        for kc, vc in CHARACTER_STATISTICS['SKILLS'].items():
            # print("* ",kc)
            for ks in vc['LIST']:
                v = self.value_for(ks['NAME'])
                total_skills += v
                default += vc['DEFAULT']
                if (v != vc["DEFAULT"]):
                    nondefault_cnt += 1
                # print("** ", ks, v)
        print("**** default = ", default, "total non default:", nondefault_cnt, self.name)
        self.indice += total_skills
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
        self.gender = self.data['features']['GENDER']
        self.lefty = self.data['features']['LEFTY']
        self.gear = self.data['features']['GEAR']
        self.spells = self.data['features']['SPELLS']

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
        for kc, vc in self.data['skills'].items():
            default = CHARACTER_STATISTICS["SKILLS"][kc.upper()]["DEFAULT"]
            for ks, vs in vc.items():
                if vs > default:
                    for r in CHARACTER_STATISTICS["SKILLS"][kc.upper()]["LIST"]:
                        if r['NAME'] == ks:
                            all.append({'value': vs, 'category': CHARACTER_STATISTICS["SKILLS"][kc.upper()]['NAME'][:4],
                                        'text': r["TEXT"]})
        sorted_all = sorted(all, key=lambda k: k['text'], reverse=False)
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
            val, errors = self.calcCompute(k['COMPUTE'])
            if len(errors) == 0:
                self.data['secondaries'][k['NAME']] = val

        for k in CHARACTER_STATISTICS['MISC']['LIST']:
            val, errors = self.calcCompute(k['COMPUTE'])
            if len(errors) == 0:
                self.data['misc'][k['NAME']] = val

        self.data['misc']['ENTRANCE'] = self.entrance
        self.data['misc']['indice_a'] = self.indice_attributes
        self.data['misc']['indice_s'] = self.indice_skills
        self.data['misc']['indice'] = self.indice
        self.data['misc']['total_attributes'] = self.total_attributes
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

        # self.data['features']['gender'] =
        # self.data['features']['lefty'] =
        self.data['features']['AGE'] = self.age
        self.data['features']['AKA'] = self.aka
        self.data['features']['GENDER'] = self.is_female
        self.data['features']['LEFTY'] = self.is_lefty

        self.data['features']['weapons'] = self.gear_to_weapons()
        self.data['features']['armors'] = self.gear_to_armors()
        self.data['features']['spells'] = self.collect_spells()
        self.data['features']['shortcuts'] = self.shortcuts()

        self.data['birthhour'] = self.birthhour
        self.data['color'] = self.color
        x = self.data['misc']['FAT']
        pf = 0
        if x > 0:
            while (x > 0):
                pf += x
                x -= 1
        self.data['misc']['pf'] = pf
        self.data["skills_summary"] = self.skills_summary()

        self.json_dump()
        # return self.data

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
                "score": stat + skill + weapon.mod_att
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
                "malus_armure": armor.malus_armure
            })
            if self.prot < armor.prot:
                self.prot = armor.prot
        return list

    def collect_spells(self):
        from main.models.draconic_arts import Spell
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
                "category": spell.category,
                "path": spell.path,
                'roll_str': spell.get_roll_display(),
                'path_str': spell.get_path_display(),
                'category_str': spell.get_category_display()
            })
        return list

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

    def calcCompute(self, str):
        result = -1
        errors = []
        param_values = []
        funky = ""
        params = []
        reference = ""
        words = str.split(',')
        if len(words) > 0:
            funky = words[0]
            if len(words) > 1:
                params = words[1].split(';')
                if len(words) > 2:
                    reference = words[2]
            else:
                errors.append(f"No Parameters")
        else:
            errors.append(f"Wrong computation line formatting for [{str}]")
        if len(errors) == 0:
            for att in params:
                v = self.value_for(att)
                param_values.append(v)
            if 'dero_mean' == funky:
                result = self.dero_mean(param_values)
            elif 'basic_mean' == funky:
                result = self.basic_mean(param_values)
            elif 'basic_sum' == funky:
                result = self.basic_sum(param_values)
            elif 'precise_mean' == funky:
                result = self.precise_mean(param_values)
            elif 'from_table_mean' == funky:
                result = self.from_table_mean(reference, param_values)
            else:
                errors.append(f"Unknown function [{funky}].")
        return result, errors

    @staticmethod
    def basic_mean(args):
        result = 0
        total = 0
        for a in args:
            total += a
        if len(args) > 0:
            result = math.ceil(total / len(args))
        return int(result)

    def from_table_mean(self, ref, args):
        from main.utils.ref_dragonade import TABLES
        result = -1
        if ref != '':
            mean = self.basic_mean(args)
        if ref in TABLES:
            result = TABLES[ref][mean]
        return result

    @staticmethod
    def precise_mean(args):
        result = 0
        total = 0
        for a in args:
            total += a
        if len(args) > 0:
            result = math.ceil(10 * total) / 10
        return result

    @staticmethod
    def basic_sum(args):
        total = 0
        for a in args:
            total += a
        return int(total)

    @staticmethod
    def dero_mean(args):
        if len(args) > 0:
            result = math.ceil((12 - args[0] + args[1]) / 2)
        else:
            result = -1
        return result

    # def import_from_json(self, jsonstring):
    #     struct = json.loads(jsonstring)

    def toJson(self):
        self.export_to_json()
        struct = json.loads(json.dumps(self.data))
        return struct

    # def json(self):
    #     self.export_to_json()
    #     js = json.dumps(self.data)
    #     return self.data

    def value_for(self, str):
        # from main.utils.ref_dragonade import CHARACTER_STATISTICS
        result = -1000
        where = self.index_for(str)
        if len(where) > 0:
            words = where.split(':')
            if len(words) == 1:
                result = self.data[words[0].lower()][str]
            else:
                result = self.data[words[0].lower()][words[1].lower()][str]
        return result

    def overwrite_for(self, str, val):
        result = False
        where = self.index_for(str)
        print("value ",str," found in ",where)
        if len(where) > 0:
            words = where.split(':')
            print("words ", words)
            if len(words) == 1:
                self.data[words[0].lower()][str] = val
                print("-->where 1 ", words[0].lower(), str)
                result = True
            else:
                self.data[words[0].lower()][words[1].lower()][str] = val
                print("-->where 1 ", words[0].lower(), words[1].lower(), str)
                result = True
        print(self.data)
        return result

    def index_for(self, str):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        #print(str.upper())
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
