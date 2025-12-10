from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character


class Creature(Character):
    class CreatureType(models.TextChoices):
        ANIMAL = "ANI", "Animal"
        HUMANOID = "HUM", "Humanoïde"
        NIGHTMARE_CREATURE = "NIC", "Créature de Cauchemard"
        NIGHTMARE_ENTITY = "NIE", "Entité de Cauchemard"
        FAERIE = "FAE", "Fée"
        ELEMENTAL = "ELE", "Elémentaire"

    creature_type = models.CharField(max_length=3, choices=CreatureType.choices, default=CreatureType.ANIMAL, blank=True)

    def __str__(self):
        return f"v_{self.rid}"

    def export_to_json(self):
        super().export_to_json()
        self.data['type'] = self.type
        return self.data

    def fix(self):
        super().fix()


class CreatureAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ['name', 'rid', 'creature_type']
    list_filter = ["creature_type"]
    actions = [refix]
