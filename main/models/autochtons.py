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
    spotlight = models.BooleanField(default=False, blank=True)
    nameless = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"a_{self.rid}"

    def initial_randomize(self):
        x = ["4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4"]
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
    ordering = ['factions','group','team','name']
    list_display = ['name', 'title','aka','priority',"spotlight","is_battle_ready", 'is_female',"age", 'team','group', 'dream','nameless' ]
    list_editable = ['dream','priority', "spotlight",'title','aka','team','group', 'age',"is_battle_ready", 'is_female', 'nameless']
    list_filter = ['dream','group','team','factions','nameless',"is_female", "is_battle_ready"]
    search_fields = ['name','title','factions','aka']
    actions = [refix]
