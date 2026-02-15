from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, roll
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

    # @property
    # def is_ready(self):
    #     teams = []
    #     for contestant in self.contestants:
    #         if contestant.team not in teams:
    #             teams.append(contestant.team)
    #     return len(teams) > 0

    def solve(self):
        print(f"Solving round #{self.index}!")
        inits = []
        contestants = self.combat.fetch_contestants()
        num = 0
        for contestant in contestants:
            init, die = contestant.roll_initiative()
            contestant.select_diff()
            friends, foes = self.combat.belongs_to_team(contestant)
            potential_enemies = self.combat.fetch(foes, must_be_alive=True)
            enemy = {"name":"","rid":""}
            foes_cnt = len(potential_enemies)
            if foes_cnt > 0:
                rand = roll(faces=foes_cnt,explodes=False)-1
                foe = potential_enemies[rand]
                enemy["name"] = foe.name
                enemy["rid"] = foe.rid

            init_datum = {
                "contestant":contestant,
                "foe": foe,
                "name": contestant.name,
                "color": contestant.personal_color,
                "foe_color": foe.personal_color,
                "init": init,
                "die": die,
                "order": 1000 - init,
                "diff": contestant.chosen_diff,
                "versus": enemy,
            }
            # print(init_datum)
            inits.append(init_datum)
        inits.sort(key=lambda x: x['order'])

        for init in inits:
            contestant = init["contestant"]
            num += 1
            print(f"Initiative dans l'ordre")
            print(f"({init['init']:02}) {contestant.name} en n°{num}")
            foe = init["foe"]
            foe.refresh_from_db()
            attack_result = contestant.make_attack(foe)
            print(f"{foe.name} has {foe.vie} hp!!!")
            contestant.refresh_from_db()
            foe.refresh_from_db()
            init["attack"] = attack_result
            init["contestant"] = contestant.rid
            init["foe"] = foe.rid

        ji = []
        for init in inits:
            ji.append(json.dumps(init))
        self.inits = "§".join(ji)


    def export_to_json(self):
        datum = {}
        datum["index"] = self.index
        inits = self.inits.split("§")
        datum["initiatives"] = []
        for init in inits:
            datum["initiatives"].append(json.loads(init))
        return datum

    def fix(self):
        pass
        # for iter in range(3):
        #     ATTACK_ROLL = roll()
        #
        #     MELEE = chaser.reach('proficiencies:MEL')
        #     WEAPON = chaser.reach('proficiencies:best_weapon:value')
        #     ATTACK = ATTACK_ROLL + MELEE + WEAPON
        #     print(f"# Jet:{ATTACK_ROLL} Mêlée:{MELEE} Compétence:{WEAPON} Total: ==> {ATTACK}")
        #     n = Nougardine(a.chosen_diff)
        #     qa, qb, qc = n.quality(ATTACK)
        #     ATTACK_MARGIN = n.margin(ATTACK)
        #     if ATTACK_MARGIN >= 4:
        #         print(f"#  Succès de l'Attaque à difficulté {qb}: {qa} => {qc}")
        #         DEFENSE_ROLL = roll()
        #         DEROBADE = chaser.reach("proficiencies:DER")
        #         ESQUIVE = chaser.reach("proficiencies:ESQ")
        #         DEFENSE = DEFENSE_ROLL + DEROBADE + ESQUIVE
        #         da, db, dc = n.quality(DEFENSE)
        #         DEFENSE_MARGIN = n.margin(DEFENSE)
        #         if DEFENSE_MARGIN >= 4:
        #             print(f"#   Succès de la défense à difficulté {db}: {da} => {dc}")
        #         else:
        #             DELTA_MARGIN = ATTACK_MARGIN - DEFENSE_MARGIN
        #             print(
        #                 f"#   Echec de la défense à difficulté {db}: {da} => {dc} DIFFERENCE DE MARGE (dM)={DELTA_MARGIN}")
        #             SEVERITY_ROLL = roll(explodes=False)
        #             QUALITY = math.floor((a.chosen_diff / 5) - 1)
        #             BASE_SEVERITY = chaser.reach('proficiencies:SEV')
        #             SEVERITY = SEVERITY_ROLL + DELTA_MARGIN + QUALITY + BASE_SEVERITY
        #             full_damage = Severity().encaissement(SEVERITY)
        #             print(
        #                 f"#   Dégâts = {SEVERITY_ROLL} + {BASE_SEVERITY} +{DELTA_MARGIN} + {QUALITY} = {SEVERITY} ==> PDV: {full_damage['pdv']}")
        #     else:
        #         print(f"#  Echec de l'Attaque à difficulté {qb}: {qa} => {qc}")


class CombatRoundAdmin(admin.ModelAdmin):
    ordering = ['combat', 'index']
    list_display = ['index', 'combat', 'is_over', 'inits']
    from main.utils.mechanics import refix
    action = [refix]
