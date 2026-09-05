from django.db import models
from django.contrib import admin
from main.mixins.jsonable import JsonableMixin
import random
from main.models.characters import Character


class Nativo(Character, JsonableMixin):
    class Meta:
        verbose_name = "Nativo"
        verbose_name_plural = "Nativi"

    dream = models.CharField(max_length=264, default="", blank=True)
    spotlight = models.BooleanField(default=False, blank=True)
    nameless = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.rid}"

    def initial_randomize(self):
        x = ["4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4"]
        random.shuffle(x)
        self.attributes = " ".join(x)

    def fix(self):
        super().fix()
        if self.randomize:
            self.initial_randomize()
            self.randomize = False
        if self.dream == "6":
            self.dream = "RDC"
        if self.dream == "9":
            self.dream = "RHS"


class NativoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import pre_sim, refix
    ordering = ['factions', 'group', 'team_color', 'name']
    list_display = ['id', 'rid', 'name', "sogni",'skills_generic', 'skills_knowledge', 'entrance', 'title', 'aka', 'is_female', "age", 'group', 'nameless', 'dream']
    list_editable = ['title', 'aka', "sogni",'skills_generic', 'skills_knowledge','group', 'age', "entrance", 'is_female', 'nameless', "dream"]
    list_filter = ['dream', 'group', 'team_color', 'factions', 'nameless', "is_female", "is_battle_ready"]
    search_fields = ['name', 'title', 'factions', 'aka', 'sogni']
    actions = [refix, pre_sim]
