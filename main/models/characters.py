from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS
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
    group = models.CharField(max_length=256, default="", blank=True)
    team = models.CharField(max_length=256, default="", blank=True)
    factions = models.CharField(max_length=256, default="", blank=True)
    entrance = models.CharField(max_length=256, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    updater = models.TextField(max_length=4096, default='{}', blank=True)

    attributes = models.CharField(max_length=64, default="", blank=True)
    skills_weapons = models.CharField(max_length=128, default="", blank=True)
    skills_generic = models.CharField(max_length=128, default="", blank=True)
    skills_peculiar = models.CharField(max_length=128, default="", blank=True)
    skills_specialized = models.CharField(max_length=128, default="", blank=True)
    skills_knowledge = models.CharField(max_length=128, default="", blank=True)
    skills_draconic = models.CharField(max_length=128, default="", blank=True)
    indice = models.IntegerField(default=0, blank=True)
    data = {}

    def __str__(self):
        return f"p_{self.id}"

    def make_rid(self):
        if self.name is not None:
            self.rid = self.name \
                .replace('é', 'e') \
                .replace('è', 'e') \
                .replace('ê', 'e') \
                .replace(' ', '_') \
                .replace('-', '_') \
                .replace('ç', 'c') \
                .replace('à', 'a') \
                .replace('ô', 'o') \
                .replace('ù', 'u') \
                .replace('û', 'u') \
                .upper()

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
            result = True
            val = self.value_for(att)
            ref = self.index_for(att)
            val += offset
            # print(self.data['skills']['weapons'][att], val, att, ref)
            if ref == "ATTRIBUTES":
                self.data['attributes'][att] = val
            else:
                self.data['skills'][ref.lower()][att] = val

            self.updateFromStruct()
            self.save()
        return result

    def updateFromStruct(self):
        list = []
        for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
            list.append(f"{self.data['attributes'][k['NAME']]}")
        self.attributes = " ".join(list)

        for key, category in CHARACTER_STATISTICS['SKILLS'].items():
            list = []
            for k in category['LIST']:
                # print("++++++++++++++++++++++++",key, k['NAME'])
                vs = f"{self.data['skills'][key.lower()][k['NAME']]}"
                list.append(vs)
            setattr(self, f"skills_{key.lower()}", " ".join(list))

        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['MARTIALES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['MARTIALES']}")
        # self.martiales = " ".join(skills_list)
        #
        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['GENERALES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['GENERALES']}")
        # self.generales = " ".join(skills_list)
        #
        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['PARTICULIERES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['PARTICULIERES']}")
        # self.particulieres = " ".join(skills_list)
        #
        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['SPECIALISEES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['SPECIALISEES']}")
        # self.specialisees = " ".join(skills_list)
        #
        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['CONNAISSANCES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['CONNAISSANCES']}")
        # self.connaissances = " ".join(skills_list)
        #
        # skills_list = []
        # for k in CHARACTER_STATISTICS['COMPETENCES']['DRACONIQUES']['LISTE']:
        #     skills_list.append(f"{self.data['skills']['DRACONIQUES']}")
        # self.draconiques = " ".join(skills_list)

    def fix(self):
        self.make_rid()
        if self.birthhour == 0:
            self.birthhour = random.randrange(1, 12)
        self.export_to_json()
        self.calc_indice()
        self.updater = self.toJson()
        self.json_dump()

    def calc_indice(self):
        from main.utils.ref_dragonade import ATTRIBUTE_CREA
        self.indice = 0
        for a in self.data['attributes']:
            self.indice += ATTRIBUTE_CREA[f"{self.data['attributes'][a]}"]

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
                    self.data[transversal[0].lower()][item['NAME']] = int(list[cnt]) if cnt<len(list) else src_struct['DEFAULT']
                    cnt += 1
            elif len(transversal) == 2:
                # Skills
                cnt = 0
                list = getattr(self, src_ref.lower()).split(' ')
                for item in src_struct['LIST']:
                    self.data[transversal[0].lower()][transversal[1].lower()][item['NAME']] = int(list[cnt]) if cnt<len(list) else src_struct['DEFAULT']
                    cnt += 1

    def export_to_json(self):
        self.data['rid'] = self.rid
        self.data['id'] = self.id
        self.data['name'] = self.name
        self.data['attributes'] = {}
        self.data['skills'] = {'weapons': {}, 'generic': {}, 'peculiar': {}, 'specialized': {}, 'knowledge': {},
                               'draconic': {}}
        self.data['secondaries'] = {}
        self.data['misc'] = {}
        self.data['type'] = self.type

        # The initialize function must implement controls to stay safe if data exists
        self.initialize()


        self.ref_to_struct('ATTRIBUTES')
        self.ref_to_struct('SKILLS_WEAPONS')
        self.ref_to_struct('SKILLS_GENERIC')
        self.ref_to_struct('SKILLS_PECULIAR')
        self.ref_to_struct('SKILLS_SPECIALIZED')
        self.ref_to_struct('SKILLS_KNOWLEDGE')
        self.ref_to_struct('SKILLS_DRACONIC')

        for k in CHARACTER_STATISTICS['SECONDARIES']:
            val, errors = self.calcCompute(k['COMPUTE'])
            if len(errors) == 0:
                self.data['secondaries'][k['NAME']] = val

        for k in CHARACTER_STATISTICS['MISCELLANEOUS']:
            val, errors = self.calcCompute(k['COMPUTE'])
            if len(errors) == 0:
                self.data['misc'][k['NAME']] = val

        self.data['misc']['entrance'] = self.entrance
        self.data['misc']['indice'] = self.indice
        self.data['misc']['groupe'] = self.group
        self.data['misc']['team'] = self.team
        self.data['misc']['title'] = self.title
        self.data['birthhour'] = self.birthhour
        x = self.data['misc']['FAT']
        pf = 0
        if x > 0:
            while (x > 0):
                pf += x
                x -= 1
        self.data['misc']['pf'] = pf
#        self.json_dump()

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
            result = math.ceil(10 * total / len(args)) / 10
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

    def import_from_json(self, jsonstring):
        struct = json.loads(jsonstring)


    def toJson(self):
        self.export_to_json()
        struct = json.loads(json.dumps(self.data))
        return struct

    def json(self):
        self.export_to_json()
        js = json.dumps(self.data)
        return self.data

    def value_for(self, str):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        result = -1
        for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
            if k['NAME'] == str:
                if str in self.data['attributes']:
                    result = self.data['attributes'][str]
        if result == -1:
            for k in CHARACTER_STATISTICS['SECONDARIES']:
                if k['NAME'] == str:
                    if str in self.data['attributes']:
                        result = self.data['attributes'][str]
        if result == -1:
            for k in CHARACTER_STATISTICS['MISCELLANEOUS']:
                if k['NAME'] == str:
                    if str in self.data['misc']:
                        result = self.data['misc'][str]
        for key, value in CHARACTER_STATISTICS['SKILLS'].items():
            for i in value['LIST']:
                if i['NAME'] == str:
                    result = self.data['skills'][key.lower()][str]
        return result

    def index_for(self, str):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        result = ""
        for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
            if k['NAME'] == str:
                result = "ATTRIBUTES"
        for key, value in CHARACTER_STATISTICS['SKILLS'].items():
            for i in value['LIST']:
                if i['NAME'] == str:
                    result = key
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
