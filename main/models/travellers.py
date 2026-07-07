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
        self.data['has_bug'] = 1 if self.has_bug() else 0
        self.data['bug_list'] = self.bug_list
        return self.data

    def fix(self):
        super().fix()
        # self.klass = "Traveller"


class TravellerAdmin(admin.ModelAdmin):
    ordering = ['-indice','name']
    list_display = ['name', 'has_bug','bug_list', 'indice', 'indice_attributes', 'indice_skills', 'color', 'destiny', 'protection_map']
    list_editable = ['color', 'destiny']
    list_filter = ['color', "priority"]
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]
