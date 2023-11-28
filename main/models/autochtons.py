from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character

class Autochton(Character):
    dream = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"a_{self.rid}"

    def initial_randomize(self):
        x = ["5", "5", "5", "4", "4", "4", "4", "4", "4", "4", "3", "3"]
        random.shuffle(x)
        self.attributes = " ".join(x)

    def fix(self):
        if self.randomize:
            self.initial_randomize()
            self.randomize = False
        super().fix()

    def export_to_json(self):
        super().export_to_json()
        self.data['dream'] = self.dream
        return self.data


class AutochtonAdmin(admin.ModelAdmin):
    ordering = ['dream', 'name']
    list_display = ['name', 'entrance', 'rid', "randomize", 'dream', 'json']
    list_editable = ['dream', "randomize", 'entrance']
