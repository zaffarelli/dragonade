from django.db import models
from django.contrib import admin
from django.conf import settings
from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character
from main.models.dreams import Dream


class Autochton(Character):
    dream = models.ForeignKey(Dream, null=True, blank=True, on_delete=models.SET_NULL)

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
        self.data['dream'] = f"{self.dream.title} [{self.dream.subtitle}]" if self.dream else "---"
        return self.data



class AutochtonAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ['name', 'is_female',"age", 'entrance', 'rid', 'dream' ]
    list_editable = ['dream', 'entrance', 'age', 'is_female']
    list_filter = ['dream']
    actions = [refix]
