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
    titre = models.CharField(max_length=256, default="", blank=True)
    groupe = models.CharField(max_length=256, default="", blank=True)
    equipe = models.CharField(max_length=256, default="", blank=True)
    factions = models.CharField(max_length=256, default="", blank=True)
    entrance = models.CharField(max_length=256, default="", blank=True)
    attributes = models.CharField(max_length=64, default="3 3 3 3 3 3 3 3 3 3 3 3", blank=True)
    martiales = models.CharField(max_length=128, default="", blank=True)
    generales = models.CharField(max_length=128, default="", blank=True)
    particulieres = models.CharField(max_length=128, default="", blank=True)
    specialisees = models.CharField(max_length=128, default="", blank=True)
    connaissances = models.CharField(max_length=128, default="", blank=True)
    draconiques = models.CharField(max_length=128, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    updater = models.TextField(max_length=4096, default='{}', blank=True)
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
            # print(self.data)
            # print("appincdec", val, ref, att, chg)
            val += offset
            if ref == "ATTRIBUTS":
                self.data['attributes'][att] = val
                self.updateAttributes()
                self.save()
            else:
                pass
                # self.data['GENERALES'][att] = val

        return result

    def updateAttributes(self):
        attributes_list = []
        for k in CHARACTER_STATISTICS['ATTRIBUTS']:
            attributes_list.append(f"{self.data['attributes'][k['NAME']]}")
        self.attributes = " ".join(attributes_list)

    def fix(self):
        self.make_rid()
        self.initialize()
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
            print(a, self.data['attributes'][a])
            self.indice += ATTRIBUTE_CREA[f"{self.data['attributes'][a]}"]

    def ref_to_chr(self, src_ref, src_chr, tgt_chr):
        # src_ref: the path to the set in the structure. Example: COMPETENCES/GENERALES to reah struct['COMPETENCES']['GENERALES']
        # src_chr: where the basic info os located. Example: self.generales
        # tgt_chr: the location in the json (example: self.data['skills']
        if len(src_chr) > 0:
            transversal = src_ref.split(' ')
            last = ''
            src_struct = CHARACTER_STATISTICS
            for p in transversal:
                src_struct = src_struct[p]
                last = p
            # Let's count with c
            c = 0
            for v in src_chr.split(' '):
                key = src_struct
                if c < len(key['LISTE']):
                    self.data[tgt_chr][last][key['LISTE'][c]['NAME']] = int(v) if int(v) > 0 else int(key['DEFAUT'])
                c += 1

    def export_to_json(self):
        self.data['rid'] = self.rid
        self.data['id'] = self.id
        self.data['name'] = self.name
        self.data['attributes'] = {}
        self.data['skills'] = {'MARTIALES':{},'GENERALES':{},'PARTICULIERES':{},'SPECIALISEES':{},'CONNAISSANCES':{},'DRACONIQUES':{}}
        self.data['misc'] = {}
        self.data['type'] = self.type
        c = 0
        for a in self.attributes.split(' '):
            if c < len(CHARACTER_STATISTICS['ATTRIBUTS']):
                self.data['attributes'][CHARACTER_STATISTICS['ATTRIBUTS'][c]['NAME']] = int(a)
            else:
                print("Attributes overflow")
            c += 1
        self.ref_to_chr('COMPETENCES MARTIALES', self.martiales, 'skills')
        self.ref_to_chr('COMPETENCES GENERALES', self.generales, 'skills')
        self.ref_to_chr('COMPETENCES PARTICULIERES', self.particulieres, 'skills')
        self.ref_to_chr('COMPETENCES SPECIALISEES', self.specialisees, 'skills')
        self.ref_to_chr('COMPETENCES CONNAISSANCES', self.connaissances, 'skills')
        self.ref_to_chr('COMPETENCES DRACONIQUES', self.draconiques, 'skills')
        for k in CHARACTER_STATISTICS['SECONDAIRES']:
            val, errors = self.calcCompute(k['COMPUTE'])
            if len(errors) == 0:
                self.data['misc'][k['NAME']] = val
        self.data['misc']['entrance'] = self.entrance
        self.data['misc']['indice'] = self.indice
        self.data['misc']['groupe'] = self.groupe
        self.data['misc']['equipe'] = self.equipe
        self.data['misc']['titre'] = self.titre
        self.data['birthhour'] = self.birthhour
        x = self.data['misc']['FAT']
        pf = 0
        if x > 0:
            while (x > 0):
                pf += x
                x -= 1
        self.data['misc']['pf'] = pf

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
            print("params:", params)
            for att in params:
                v = self.value_for(att)
                print("v:", att, v)
                param_values.append(v)
            print("param_values:", param_values)
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
        print("args:", args)
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
        print(struct)

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
        for k in CHARACTER_STATISTICS['ATTRIBUTS']:
            if k['NAME'] == str:
                if str in self.data['attributes']:
                    result = self.data['attributes'][str]
        if result == -1:
            for k in CHARACTER_STATISTICS['SECONDAIRES']:
                if k['NAME'] == str:
                    if str in self.data['attributes']:
                        result = self.data['attributes'][str]
        print("result:", result)
        return result

    def index_for(self, str):
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        result = ""
        print(str, CHARACTER_STATISTICS['ATTRIBUTS'])
        for k in CHARACTER_STATISTICS['ATTRIBUTS']:
            if k['NAME'] == str:
                result = "ATTRIBUTS"
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
            for att in CHARACTER_STATISTICS['ATTRIBUTS']:
                list.append("4")
            self.attributes = " ".join(list)

        for k, cat in CHARACTER_STATISTICS['COMPETENCES'].items():
            print("Initialize: ", k, cat)
            list = []
            for item in cat['LISTE']:
                list.append(f"{cat['DEFAUT']}")
            if len(self.martiales) == 0:
                if 'MARTIALES' == k:
                    self.martiales = " ".join(list)
            if len(self.generales) == 0:
                if 'GENERALES' == k:
                    self.generales = " ".join(list)
            if len(self.particulieres) == 0:
                if 'PARTICULIERES' == k:
                    self.particulieres = " ".join(list)
            if len(self.specialisees) == 0:
                if 'SPECIALISEES' == k:
                    self.specialisees = " ".join(list)
            if len(self.connaissances) == 0:
                if 'CONNAISSANCES' == k:
                    self.connaissances = " ".join(list)
            if len(self.draconiques) == 0:
                if 'DRACONIQUES' == k:
                    self.draconiques = " ".join(list)
