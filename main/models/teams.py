from django.db import models
from django.contrib import admin
from main.models.viaggiatori import Viaggiatore


class Team(models.Model):
    name = models.CharField(max_length=128, default="", blank=True)
    adventure = models.CharField(max_length=128, default="", blank=True)
    rids = models.CharField(max_length=128, default="", blank=True)

    def travellers_list(self):
        list = []
        for rid in self.rids.split(" "):
            travellers = Viaggiatore.objects.filter(rid=rid)
            for traveller in travellers:
                list.append(traveller)
        return list

    @property
    def travellers(self):
        from django.utils.safestring import mark_safe
        list = []
        for x in self.travellers_list():
            list.append(x.name+" > "+x.player)
        return mark_safe("<br/>".join(list))

    def fix(self):
        super().fix()


class TeamAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ['name', 'adventure', 'rids', 'travellers']
    list_editable = ["adventure", 'rids']
    actions = [refix]
