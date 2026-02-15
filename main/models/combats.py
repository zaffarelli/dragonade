from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, Chaser, Nougardine, Colorizer
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
    red_real_rids = models.TextField(default="", max_length=2048, blank=True)
    blue_real_rids = models.TextField(default="", max_length=2048, blank=True)
    current_round = models.IntegerField(default=0, blank=True)

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

    # def remove_contestants(self):
    #     from main.models.contestants import Contestant
    #     contestants = Contestant.objects.filter(combat=self)
    #     for contestant in contestants:
    #         print("WWWWW " + contestant.name)
    #         contestant.delete()

    def add_contestants(self, team="blue", rids=[]):
        from main.models.characters import Character
        from main.models.contestants import Contestant
        # Phase 0: Transfrom Character.rids into Traveller/Autochton/Creature contestant.rids
        if team == "blue":
            str = self.blue_team_str.strip()
            self.blue_real_rids = ""
            blue_real_rids = []
        else:
            str = self.red_team_str.strip()
            self.red_real_rids = ""
            red_real_rids = []
        for rid in rids:
            if len(rid) > 0:
                t = str.split(" ")
                if rid.startswith("CRE__"):
                    t.append(rid)
                else:
                    if rid not in t:
                        t.append(rid)
        print("Phase 0")
        if team == "blue":
            self.blue_team_str = " ".join(t)
            str = self.blue_team_str
            print(self.blue_team_str)
        else:
            self.red_team_str = " ".join(t)
            str = self.red_team_str
            print(self.red_team_str)



        contestants = []
        same = {}
        counts = {}
        rids = str.split(" ")
        # Phase 1: Just count what we have
        print("Phase 1")
        for rid in rids:
            if len(rid) > 0:
                x = Character.find_from_rid(rid)
                if x is not None:
                    if x.rid not in same:
                        same[x.rid] = 0
                    else:
                        same[x.rid] += 1
                self.challengers.filter(source_rid=x.rid).delete()
                # for contestant in contestants:
                #     print(f"- {contestant.name:<30} {contestant.rid:>40}")
        print("same")
        print(same)
        print("counts")
        print(counts)

        colorizer = Colorizer()
        colorizer.randomize(8)

        # Phase 2: Clean contestant creation and naming
        print("Phase 2")
        for rid in rids:
            if len(rid) > 0:
                color = colorizer.pop()
                x = Character.find_from_rid(rid)
                if x.rid not in counts:
                    counts[x.rid] = 0
                if x is not None:
                    if same[rid] == 0: # No multiple occurences: traveller/autochton
                        a = x.pre_sim(self, name=x.name, occurrence=same[x.rid],color=color)
                        # if not x.rid.startswith("CRE__"):
                        #     a.is_temporary = False
                        # else:
                        #     if counts[x.rid] == 0:
                        #         a.is_temporary = False
                    else:
                        counts[x.rid] += 1
                        new_name = f'{x.name} {counts[x.rid]}'
                        a = x.pre_sim(self, name=new_name, occurrence=counts[x.rid],color=color)
                        # a.is_temporary = False
                    if team == "blue":
                        a.team_color = "#3b6cb9"
                    else:
                        a.team_color = "#b93b3d"
                    a.save()
                    contestants.append('{"rid":"' + a.rid + '","name":"' + a.name + '"}')
                    if team == "blue":
                        blue_real_rids.append(a.rid)
                    else:
                        red_real_rids.append(a.rid)
        if team == "blue":
            self.blue_contestants_str = f'{"§".join(contestants)}'
            self.blue_real_rids = " ".join(blue_real_rids)
            print(self.blue_real_rids)
        else:
            self.red_contestants_str = f'{"§".join(contestants)}'
            self.red_real_rids = " ".join(red_real_rids)
            print(self.red_real_rids)
        # Phase 3
        print("Phase 3")
        # Contestant.objects.filter(is_temporary=True).delete()
        contestants = self.challengers.all()
        for contestant in contestants:
            print(f"- {contestant.name:<30} {contestant.rid:>40}")

    def new_round(self):
        print("New Round!!")
        from main.models.combat_rounds import CombatRound
        highest_index = 0
        create = False
        round = None
        for rnd in self.combat_rounds.all():
            if highest_index < rnd.index:
                highest_index = rnd.index
                round = rnd
        if round is None:
            create = True
        else:
            if round.is_over:
                create = True
        if create:
            r = CombatRound()
            r.combat = self
            r.index = highest_index + 1
            round = r
        round.solve()
        round.save()
        round.refresh_from_db()
        self.current_round = round.index

    # def start_fight(self):
    #     round = self.new_round()
    #     return round

    def set_up(self, config):
        self._config = json.dumps(config, indent=2, sort_keys=True)

    def belongs_to_team(self, contestant):
        """
        Find matching team for a contestant
        :param contestant: Contestant object
        :returns: Returns (friends/foes) tuple
        """
        friends = "blue"
        foes = "red"
        reds = self.fetch("red")
        if contestant in reds:
            friends = "red"
            foes = "blue"
        return friends, foes

    def fix(self):
        self.code = self.code.upper().strip()
        self.red_team_str.strip()
        self.blue_team_str.strip()

    def fetch_contestants(self):
        reds = self.fetch("red")
        blues = self.fetch("blue")
        all = blues + reds
        return all

    def fetch(self, str, must_be_alive=False):
        search_str = self.blue_real_rids
        if "red" in str:
            search_str = self.red_real_rids
        group = []
        from main.models.contestants import Contestant
        rids = search_str.split(" ")
        for rid in rids:
            if len(rid) > 0:
                contestants = Contestant.objects.filter(rid=rid)
                if len(contestants) == 1:
                    contestant = contestants.first()
                    if must_be_alive:
                        if not contestant.is_dead:
                            group.append(contestant)
                    else:
                        group.append(contestant)
        return group

    def prepare_fight(self):
        from main.models.combat_rounds import CombatRound
        reds = self.fetch("red")
        blues = self.fetch("blue")
        CombatRound.objects.filter(combat=self).delete()

        self.current_round = 0
        for blue in blues:
            blue.fix_handicap(len(blues) - 1)
            blue.prepare_for_new_fight()
            blue.save()
        for red in reds:
            red.fix_handicap(len(reds) - 1)
            red.prepare_for_new_fight()
            red.save()

    def results(self):
        reds = self.fetch("red")
        blues = self.fetch("blue")
        json_data = {"title": self.code, "teams": {"blue": [], "red": []}, "combat_rounds": []}
        for blue in blues:
            blue.refresh_from_db()
            json_data["teams"]["blue"].append(blue.battle_roster())
        for red in reds:
            red.refresh_from_db()
            json_data["teams"]["red"].append(red.battle_roster())
        for combat_round in self.combat_rounds.all():
            combat_round.refresh_from_db()
            json_data["combat_rounds"].append(combat_round.export_to_json())
        # print("Rounds count:",len(json_data["combat_rounds"]))
        return json_data


class CombatAdmin(admin.ModelAdmin):
    ordering = ['code']
    list_display = ['code', 'is_current', "blue_real_rids", "red_real_rids", "current_round"]
    list_editable = ['is_current']
    from main.utils.mechanics import refix
    actions = [refix]
