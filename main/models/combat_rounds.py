from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid
from main.models.combats import Combat


class CombatRound(models.Model):
    class Meta:
        ordering = ['index']

    index = models.IntegerField(default=0, blank=True)
    # if there's no combat, remove associated rounds
    combat = models.ForeignKey(Combat, on_delete= models.CASCADE)
    active_round = models.BooleanField(default=False, blank=True)
    is_over = (models.BooleanField(default=False, blank=True))

    @property
    def is_ready(self):
        teams = []
        for contestant in self.contestants:
            if contestant.team not in teams:
                teams.append(contestant.team)
        return len(teams) > 0

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
    list_display = ['index', 'combat', 'is_ready', 'is_over']
    from main.utils.mechanics import refix
    action = [refix]
