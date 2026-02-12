from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, Chaser, Nougardine
import json
import math


class Combat(models.Model):
    code = models.CharField(max_length=32, unique=True)
    _config = models.TextField(max_length=2048, default="{}", blank=True)
    red_team_str = models.TextField(default="", max_length=2048, blank=True)
    blue_team_str = models.TextField(default="", max_length=2048, blank=True)
    is_current = models.BooleanField(default=True, blank=True)
    red_contestants_str = models.TextField(max_length=2048, default="", blank=True)
    blue_contestants_str = models.TextField(max_length=2048, default="", blank=True)

    def __str__(self):
        return "Combat:" + self.code

    @classmethod
    def deactivate(cls):
        combats = cls.objects.all()
        for combat in combats:
            combat.is_current = False
            combat.save()

    def export_to_json(self):
        data = {}
        data['code'] = self.code
        data['teams'] = {}
        data['teams']['red'] = []
        data['teams']['blue'] = []
        for item in self.red_contestants_str.split("§"):
            # print("******",item)
            if len(item) > 0:
                data['teams']['red'].append(json.loads(item))
        for item in self.blue_contestants_str.split("§"):
            if len(item) > 0:
                data['teams']['blue'].append(json.loads(item))

        data['is_current'] = self.is_current
        return data

    def quality_table(self, diff):
        t = None
        if "quality_table" in self._config:
            if self._config["quality_table"].lower() == "nougardine":
                t = Nougardine(diff)
        return t

    def add_contestants(self, team="blue", rids=[]):
        if team == "blue":
            str = self.blue_team_str.strip()
        else:
            str = self.red_team_str.strip()
        for rid in rids:
            if len(rid) > 0:
                t = str.split(" ")
                if rid.startswith("CRE__"):
                    t.append(rid)
                else:
                    if rid not in t:
                        t.append(rid)
        if team == "blue":
            self.blue_team_str = " ".join(t)
            str = self.blue_team_str
        else:
            self.red_team_str = " ".join(t)
            str = self.red_team_str

        from main.models.travellers import Traveller
        from main.models.creatures import Creature
        from main.models.autochtons import Autochton
        contestants = []
        same = {}
        objects = []
        for rid in str.split(" "):
            if len(rid) > 0:
                x = None
                travellers = Traveller.objects.filter(rid=rid)
                autochtons = Autochton.objects.filter(rid=rid)
                creatures = Creature.objects.filter(rid=rid)
                if len(travellers) == 1:
                    x = travellers.first()
                elif len(creatures) == 1:
                    x = creatures.first()
                elif len(autochtons) == 1:
                    x = autochtons.first()
                if x is not None:
                    if x.rid not in same:
                        same[x.rid] = 0
                    else:
                        same[x.rid] += 1
                    a = x.pre_sim(self, occurrence=same[x.rid])
                    objects.append(a)

        for o in objects:
            print("xxxxxxxxxx", o.name, o.rid)
            words = o.name.split("___")
            if same[o.source_rid] == 0:
                o.name = words[0]
            else:
                n = int(words[1])
                o.name = f'{words[0]} {n + 1}'
            o.save()
            contestants.append('{"rid":"' + o.rid + '","name":"' + o.name + '"}')
        if team == "blue":
            self.blue_contestants_str = f'{"§".join(contestants)}'
        else:
            self.red_contestants_str = f'{"§".join(contestants)}'

    # @property
    # def reds_str(self):
    #     l = []
    #     for contestant in self.reds:
    #         l.append(f"{contestant.name} [{contestant.team}]")
    #     return ", ".join(l)
    #
    # @property
    # def blues_str(self):
    #     l = []
    #     for contestant in self.blues:
    #         l.append(f"{contestant.name} [{contestant.team}]")
    #     return ", ".join(l)

    @property
    def new_round(self):
        from main.models.combat_rounds import CombatRound
        highest_index = 0
        r = None
        for round in self.combatround_set:
            if highest_index < round.index:
                highest_index = round.index
            if not round.is_over:
                r = round
        if r is None:
            r = CombatRound()
            r.combat = self
            r.index = highest_index + 1
            r.save()
        return r

    def start_fight(self):
        round = self.new_round()
        return round

    def set_up(self, config):
        self._config = json.dumps(config, indent=2, sort_keys=True)

    def fix(self):
        self.code = self.code.upper().strip()
        from main.models.travellers import Traveller
        from main.models.creatures import Creature
        from main.models.autochtons import Autochton
        self.red_team_str.strip()
        self.blue_team_str.strip()

        # reds = self.red_team_str.split(" ")
        # for red in reds:
        #     if len(red) > 0:
        #         x = None
        #         travellers = Traveller.objects.filter(rid=red)
        #         autochtons = Autochton.objects.filter(rid=red)
        #         creatures = Creature.objects.filter(rid=red)
        #         if len(travellers) == 1:
        #             x = travellers.first()
        #         elif len(creatures) == 1:
        #             x = creatures.first()
        #         elif len(autochtons) == 1:
        #             x = autochtons.first()
        #         if x is not None:
        #             x.pre_sim(self.code)

        # blues = self.blue_team_str.split(" ")
        # for blue in blues:
        #     if len(blue) > 0:
        #         x = None
        #         travellers = Traveller.objects.filter(rid=blue)
        #         autochtons = Autochton.objects.filter(rid=blue)
        #         creatures = Creature.objects.filter(rid=blue)
        #         # print(len(travellers), len(autochtons), len(creatures))
        #         if len(travellers) == 1:
        #             x = travellers.first()
        #         elif len(creatures) == 1:
        #             x = creatures.first()
        #         elif len(autochtons) == 1:
        #             x = autochtons.first()
        #         if x is not None:
        #             x.pre_sim(self.code)


class CombatAdmin(admin.ModelAdmin):
    ordering = ['code']
    list_display = ['code', 'is_current', 'red_team_str', 'blue_team_str', "red_contestants_str",
                    "blue_contestants_str"]
    list_editable = ['is_current']
    from main.utils.mechanics import refix
    actions = [refix]
