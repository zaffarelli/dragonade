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
        # self.klass = "Autochton"

    def export_to_json(self):
        super().export_to_json()
        self.data['dream'] = f"{self.dream.title} [{self.dream.subtitle}]" if self.dream else "---"
        self.data['nameless'] = "true" if self.nameless else "false"
        return self.data



class AutochtonAdmin(admin.ModelAdmin):
    ordering = ['factions','group','team_color','name']
    list_display = ['name', 'entrance','title','aka', 'is_female',"age",'group', 'dream','nameless' ]
    list_editable = ['dream','title','aka','group', 'age',"entrance", 'is_female', 'nameless']
    list_filter = ['dream','group','team_color','factions','nameless',"is_female", "is_battle_ready"]
    search_fields = ['name','title','factions','aka']
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]

