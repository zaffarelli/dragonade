from django.db import models
from django.contrib import admin
from django.conf import settings

from main.mixins.jsonable import JsonableMixin
from main.utils.ref_dragonade import CHARACTER_STATISTICS
import math
import random
import json
from main.models.characters import Character
from main.models.dreams import Dream


class Nativo(Character, JsonableMixin):
    class Meta:
        verbose_name = "Nativo"
        verbose_name_plural = "Nativi"
    # dream = models.ForeignKey(Dream, null=True, blank=True, on_delete=models.SET_NULL)
    dream = models.CharField(max_length=264, default="",blank=True)
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
        if self.dream == "6":
            self.dream = "RDC"
        if self.dream == "9":
            self.dream = "RHS"
        # self.klass = "Autochton"

    def export_to_json(self):
        super().export_to_json()
        self.data['dream'] = self.dream
        self.data['nameless'] = self.nameless
        return self.data



class NativoAdmin(admin.ModelAdmin):
    ordering = ['factions','group','team_color','name']
    list_display = ['name', 'entrance','title','aka', 'is_female',"age",'group', 'nameless','dream' ]
    list_editable = ['title','aka','group', 'age',"entrance", 'is_female', 'nameless', "dream"]
    list_filter = ['dream','group','team_color','factions','nameless',"is_female", "is_battle_ready"]
    search_fields = ['name','title','factions','aka']
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]

