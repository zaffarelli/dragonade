from django.db import models
from django.contrib import admin
from main.models.characters import Character


class Viaggiatore(Character):
    class Meta:
        verbose_name = "Viaggiatore"
        verbose_name_plural = "Viaggiatori"

    player = models.CharField(max_length=128, default="", blank=True)
    destiny = models.PositiveIntegerField(default=0, blank=True)
    is_storyteller = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.rid}"

    def fix(self):
        super().fix()
        if self.is_storyteller:
            self.player = "Gardien des Rêves"
            self.stress_acquired = 666666


class ViaggiatoreAdmin(admin.ModelAdmin):
    from main.utils.mechanics import pre_sim, refix
    ordering = ['-indice', 'name']
    list_display = ['id', 'rid', 'name', 'player', 'is_storyteller', 'bug_list', 'color', 'destiny']
    list_editable = ['color', 'destiny', 'is_storyteller']
    list_filter = ['is_storyteller', "priority"]
    actions = [refix, pre_sim]
