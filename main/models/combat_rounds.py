from django.db import models
from django.contrib import admin
from main.models.combats import Combat
import json


class CombatRound(models.Model):
    class Meta:
        ordering = ['index']

    index = models.IntegerField(default=0, blank=True)
    # if there's no combat, remove associated rounds
    combat = models.ForeignKey(Combat, on_delete=models.CASCADE, related_name="combat_rounds")
    active_round = models.BooleanField(default=False, blank=True)
    is_over = models.BooleanField(default=False, blank=True)
    inits = models.TextField(max_length=1024, default="", blank=True)

    def solve(self):
        fight_is_over = ""
        print(f"Solving round #{self.index}!")
        inits = []
        contestants, special = self.combat.fetch_contestants(must_be_alive=True)
        if special != "":
            fight_is_over = special
            print(f"Contestants: {special}")
        else:
            num = 0
            for contestant in contestants:
                init, die = contestant.roll_initiative()
                init_datum = {
                    "init": init,
                    "die": die,
                    "name": contestant.name,
                    "color": contestant.personal_color,
                    "contestant": contestant.rid,
                    "team_color": contestant.team_color,
                    "order": 1000 - init,
                    "is_dead": False,
                }
                inits.append(init_datum)
            new_inits = []
            for contestant in contestants:
                for init in inits:
                    print(f'Search: {contestant.rid} ')
                    if init["contestant"] == contestant.rid:
                        init_datum = inits.remove(init)
                        print(f'Found: {contestant.rid} => {init_datum}')
                        break
                contestant.select_diff()
                enemy = contestant.select_enemy(contestants, contestant.team)
                print(f'{contestant.name} will attack {enemy["name"]}!')
                init_datum["foe"] = enemy["rid"]
                init_datum["foe_name"] = enemy["name"]
                init_datum["foe_color"] = enemy["color"]
                init_datum["diff"] = contestant.chosen_diff
                init_datum["versus"] = enemy
                new_inits.append(init_datum)
            inits = new_inits
            inits.sort(key=lambda x: x['order'])
            for init in inits:
                for c in contestants:
                    if c.rid == init["contestant"]:
                        contestant = c
                        # contestant = self.combat.challengers.filter(rid=init["contestant"]).first()
                if not contestant.is_dead:
                    num += 1
                    contestant.foe = self.combat.challengers.filter(rid=init["foe"]).first()
                    print(f"Initiative dans l'ordre")
                    print(f"({init['init']:02}) {contestant.name} en n°{num}")
                    if contestant.foe:
                        print(f"({init['init']:02}) {contestant.name} attaque contre {contestant.foe.name} !")
                        attack_result = contestant.make_attack()
                        #  init["attacks"] = []
                        init["attacks"] = [attack_result]
                        while "R" in contestant.avoidance:
                            attack_result = contestant.make_attack()
                            init["attacks"].append(attack_result)
                        if contestant.foe.is_dead:
                            contestant.foe = None
                    else:
                        print(f"({init['init']:02}) {contestant.name} Plus d'ennemi !")
                else:
                    init["is_dead"] = True
                init["contestant"] = contestant.rid
                if contestant.foe:
                    init["foe"] = contestant.foe.rid
            ji = []
            for init in inits:
                ji.append(json.dumps(init))
            self.inits = "§".join(ji)
            self.is_over = True
        return fight_is_over

    def export_to_json(self):
        datum = {}
        datum["index"] = self.index
        datum["order"] = 10000 - self.index
        inits = self.inits.split("§")
        datum["initiatives"] = []
        for init in inits:
            datum["initiatives"].append(json.loads(init))
        return datum

    def fix(self):
        pass


class CombatRoundAdmin(admin.ModelAdmin):
    ordering = ['combat', 'index']
    list_display = ['index', 'combat', 'is_over', 'inits']
    from main.utils.mechanics import refix
    action = [refix]
