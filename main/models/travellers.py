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

    def __str__(self):
        return f"v_{self.rid}"

    def export_to_json(self):
        super().export_to_json()
        self.data['player'] = self.player
        return self.data

    def fix(self):
        super().fix()


class TravellerAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'entrance', 'rid', 'player', 'json']
