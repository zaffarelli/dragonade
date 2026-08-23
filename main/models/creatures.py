from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character


class DragonadeCreatureType(models.IntegerChoices):
    ANIMAL = 0, "Animal"
    HUMANOID = 1, "Humanoïde"
    NIGHTMARE_CREATURE = 2, "Créature de Cauchemard"
    NIGHTMARE_ENTITY = 3, "Entité de Cauchemard"
    FAERIE = 4, "Fée"
    ELEMENTAL = 5, "Elémentaire"
    ONIRIDE = 6, "Oniride"
    FABULOUS_CREATURE = 7, "Créature fabuleuse"
    CONSTRUCT = 8, "Construct"


class Creature(Character):
    # class CreatureType(models.TextChoices):
    #     ANIMAL = "ANI", "Animal"
    #     HUMANOID = "HUM", "Humanoïde"
    #     NIGHTMARE_CREATURE = "NIC", "Créature de Cauchemard"
    #     NIGHTMARE_ENTITY = "NIE", "Entité de Cauchemard"
    #     FAERIE = "FAE", "Fée"
    #     ELEMENTAL = "ELE", "Elémentaire"
    #     ONIRIDE = "ONI", "Oniride"

    # creature_type = models.CharField(max_length=3, choices=CreatureType.choices, default=CreatureType.ANIMAL, blank=True)
    creature_type = models.IntegerField(choices=DragonadeCreatureType.choices, default=DragonadeCreatureType.ANIMAL, blank=True)

    def __str__(self):
        return f"v_{self.rid}"

    def export_to_json(self):
        super().export_to_json()
        self.data['creature_type'] = self.get_creature_type_display()
        return self.data

    def fix(self):
        super().fix()
        print(f"RID: {self.rid}")
        # self.klass = "Creature"


class CreatureAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'rid', 'creature_type','team_color']
    list_filter = ["creature_type",'team_color']
    list_editable = ["creature_type",'team_color']
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]

