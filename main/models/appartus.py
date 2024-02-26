from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid


class AppartusCategory(models.IntegerChoices):
    WEAPON = 0, "Arme"
    ARMOR = 1, "Armure"
    CONSUMABLE = 2, "Consomable"
    TOME = 3, "Tôme"
    MISCELLANEOUS = 666, "Divers"



class Appartus(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    equipment_match = models.CharField(default="xxx", max_length=256, blank=True)
    category = models.PositiveIntegerField(default=AppartusCategory.MISCELLANEOUS, choices=AppartusCategory.choices, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    price = models.FloatField(default=0.1, blank=True)
    data = {}

    def fix(self):
        self.rid = as_rid(f"{self.name}{self.get_category_display()}")

    def __str__(self):
        return f"{self.name} [{self.get_category_display()}]"

    def export_to_json(self):
        data = {}
        data['name'] = self.name
        data['rid'] = self.rid
        data['category'] = self.rid
        data['description'] = self.description
        self.data = data
        return data


class AppartusAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ["name", "rid", "price"]
    list_filter = ['category']
    search_fields = ['name']
    actions = [refix]
