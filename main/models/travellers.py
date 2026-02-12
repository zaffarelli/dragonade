from django.db import models
from django.contrib import admin
from django.conf import settings

from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character


class Traveller(Character):
    player = models.CharField(max_length=128, default="", blank=True)
    destiny = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"v_{self.rid}"

    def export_to_json(self):
        super().export_to_json()
        self.data['player'] = self.player
        self.data['destiny'] = self.destiny
        return self.data

    def fix(self):
        super().fix()
        # self.klass = "Traveller"


class TravellerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'team_color', 'rid', 'player', 'gear', 'spells', 'destiny', "is_battle_ready"]
    list_editable = ['gear', 'spells', 'team_color', 'destiny', "is_battle_ready", 'player']
    list_filter = ["is_battle_ready", 'team_color', "priority"]
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]
