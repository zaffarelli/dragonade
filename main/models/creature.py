from django.db import models
from django.contrib import admin
from main.models.characters import Character


class DragonadeCreatureType(models.IntegerChoices):
    ANIMAL = 0, "Animal"
    HUMANOID = 1, "Humanoïde"
    NIGHTMARE_CREATURE = 2, "Créature de Cauchemard"
    NIGHTMARE_ENTITY = 3, "Entité de Cauchemard"
    FAERIE = 4, "Fée"
    ELEMENTAL = 5, "Elémentaire"
    ONIRIDE = 6, "Oniride"
    FABULOUS_CREATURE = 7, "Créature fabuleuse"
    CONSTRUCT = 8, "Construct"


class Creatura(Character):
    class Meta:
        verbose_name = "Creatura"
        verbose_name_plural = "Creature"

    creature_type = models.IntegerField(choices=DragonadeCreatureType.choices, default=DragonadeCreatureType.ANIMAL, blank=True)

    def __str__(self):
        return f"{self.rid}"

    def co_push(self):
        super().co_push()
        self._data["creature_type_str"] = self.get_creature_type_display()



class CreaturaAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id','rid','name', 'attributes','secondaries', 'creature_type', 'team_color']
    list_filter = ["creature_type", 'team_color']
    list_editable = ['attributes','secondaries',"creature_type", 'team_color']
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]
