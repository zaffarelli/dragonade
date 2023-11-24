from django.db import models
from django.contrib import admin
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
    entrance = models.CharField(max_length=256, default="", blank=True)
    attributes = models.CharField(max_length=32, default="3 3 3 3 3 3 3 3 3 3 3 3", blank=True)
    martiales = models.CharField(max_length=64, default="", blank=True)
    generales = models.CharField(max_length=64, default="0 0 0 0 0 0 0 0 0 0 0 0 0", blank=True)
    particulieres = models.CharField(max_length=64, default="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0", blank=True)
    specialisees = models.CharField(max_length=64, default="0 0 0 0 0 0 0 0 0 0", blank=True)
    connaissances = models.CharField(max_length=64, default="0 0 0 0 0 0 0 0 0", blank=True)
    draconiques = models.CharField(max_length=64, default="0 0 0 0 0 0", blank=True)
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

    def fix(self):
        self.make_rid()
        if self.birthhour == 0:
            self.birthhour = random.randrange(1, 12)
        self.export_to_json()
        self.calc_indice()

    def calc_indice(self):
        from main.utils.ref_dragonade import ATTRIBUTE_CREA
        self.indice = 0
        print(self.data['attributes'])
        for a in self.data['attributes']:
            self.indice += ATTRIBUTE_CREA[f"{self.data['attributes'][a]}"]

    def ref_to_chr(self, src_ref, src_chr, tgt_chr):
        # src_ref: the path to the set in the structure. Example: COMPETENCES/GENERALES to reah struct['COMPETENCES']['GENERALES']
        # src_chr: where the basic info os located. Example: self.generales
        # tgt_chr: the location in the json (example: self.data['skills']
        transversal = src_ref.split(' ')
        src_struct = CHARACTER_STATISTICS
        for p in transversal:
            src_struct = src_struct[p]
        # Let's count with c
        c = 0
        for v in src_chr.split(' '):
            key = src_struct
            if c < len(key['LISTE']):
                self.data[tgt_chr][key['LISTE'][c]['NAME']] = int(v) if int(v) > 0 else int(key['DEFAUT'])
            c += 1

    def export_to_json(self):
        self.data['rid'] = self.rid
        self.data['id'] = self.id
        self.data['name'] = self.name
        self.data['attributes'] = {}
        self.data['skills'] = {}
        self.data['misc'] = {}
        c = 0
        for a in self.attributes.split(' '):
            if c < len(CHARACTER_STATISTICS['ATTRIBUTS']):
                self.data['attributes'][CHARACTER_STATISTICS['ATTRIBUTS'][c]['NAME']] = int(a)
            else:
                print("Attributes overflow")
            c += 1
        self.ref_to_chr('COMPETENCES GENERALES', self.generales, 'skills')
        self.ref_to_chr('COMPETENCES PARTICULIERES', self.particulieres, 'skills')
        self.ref_to_chr('COMPETENCES SPECIALISEES', self.specialisees, 'skills')
        self.ref_to_chr('COMPETENCES CONNAISSANCES', self.connaissances, 'skills')
        self.ref_to_chr('COMPETENCES DRACONIQUES', self.draconiques, 'skills')
        for k in CHARACTER_STATISTICS['SECONDAIRES']:
            val = -1
            v1 = -1
            v2 = -1
            v3 = -1
            print(k['COMPUTE'])
            words = k['COMPUTE'].split(',')
            if words[0] == 'dero_mean':
                v1 = int(self.value_for(words[1]))
                v2 = int(self.value_for(words[2]))
                if v1 > -1 and v2 > -1:
                    val = self.dero_mean(v1, v2)
            if words[0] == 'basic_mean':
                v1 = int(self.value_for(words[1]))
                v2 = int(self.value_for(words[2]))
                if len(words) > 3:
                    v3 = int(self.value_for(words[3]))
                if v1 > -1 and v2 > -1 and v3 > -1:
                    val = self.basic_mean(v1, v2, v3)
                elif v1 > -1 and v2 > -1:
                    val = self.basic_mean(v1, v2)
            if words[0] == 'basic_sum':
                v1 = int(self.value_for(words[1]))
                v2 = int(self.value_for(words[2]))
                if len(words) > 3:
                    v3 = int(self.value_for(words[3]))
                print(v1,v2,v3)
                if v1 > -1 and v2 > -1 and v3 > -1:
                    val = self.basic_sum(v1, v2, v3)
                elif v1 > -1 and v2 > -1:
                    val = self.basic_sum(v1, v2)
            if val > -1:
                self.data['attributes'][k['NAME']] = val
        self.data['misc']['entrance'] = self.entrance
        self.data['misc']['indice'] = self.indice
        self.data['misc']['groupe'] = self.groupe
        self.data['misc']['equipe'] = self.equipe
        self.data['misc']['titre'] = self.titre
        x = self.data['attributes']['FAT']
        pf = 0
        if x>0:
            while (x > 0):
                pf += x
                x -= 1
        self.data['misc']['pf'] = pf

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
        return result

    @staticmethod
    def basic_mean(*args):
        result = 0
        total = 0
        for a in args:
            total += a
        if len(args) > 0:
            result = math.ceil(total / len(args))
        return int(result)

    @staticmethod
    def basic_sum(*args):
        total = 0
        for a in args:
            total += a
        return int(total)


    @staticmethod
    def dero_mean(v1, v2):
        result = math.ceil((12 - v1 + v2) / 2)
        return result

    def json_dump(self):
        import os
        filename = f'{self.RID}.json'
        json_name = os.path.join(settings.MEDIA_ROOT, 'characters/' + filename)
        with open(json_name, "w") as f:
            f.write(self.json())
            f.close()


class Autochton(Character):
    dream = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"a_{self.rid}"

    def initial_randomize(self):
        x = ["5", "5", "5", "4", "4", "4", "4", "4", "4", "4", "3", "3"]
        random.shuffle(x)
        self.attributes = " ".join(x)


    def fix(self):
        if self.randomize:
            self.initial_randomize()
            self.randomize = False
        super().fix()

    def export_to_json(self):
        super().export_to_json()
        self.data['dream'] = self.dream
        return self.data


class Traveller(Character):
    player = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return f"v_{self.rid}"

    def export_to_json(self):
        super().export_to_json()
        self.data['player'] = self.player
        return self.data

    def fix(self):
        super().fix()


class AutochtonAdmin(admin.ModelAdmin):
    ordering = ['dream', 'name']
    list_display = ['name', 'entrance', 'rid', "randomize", 'dream', 'json']
    list_editable = ['dream', "randomize", 'entrance']


class TravellerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'entrance', 'rid', 'player', 'json']
