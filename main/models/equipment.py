from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid
from django.utils import timezone
from main.utils.ref_dragonade import GEAR_CAT


class Equipment(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    category = models.CharField(default="gen", max_length=3, choices=GEAR_CAT)
    plus_dom = models.IntegerField(default=0, null=True, blank=True)
    plus_dom_2m = models.IntegerField(default=0, null=True, blank=True)
    prot = models.IntegerField(default=0, null=True, blank=True)
    related_skill = models.CharField(default="", max_length=8, blank=True)
    related_attribute = models.CharField(default="", max_length=8, blank=True)
    malus_armure = models.IntegerField(default=0, null=True, blank=True)
    force_min = models.IntegerField(default=0, null=True, blank=True)
    enc = models.FloatField(default=0.1, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    price = models.FloatField(default=0.1, blank=True)
    quantity = models.FloatField(default=0.1, blank=True)


    def fix(self):
        self.rid = as_rid(f"{self.name}_{self.category}")

    def __str__(self):
        return f"{self.name} [{self.category}]"




def cat_from_first(modeladmin, request, queryset):
    if len(queryset)>2:
        cat = ""
        for item in queryset:
            if cat == "":
                cat = item.category
            else:
                item.category = cat
                item.save()
    short_description = "Category from the first item"


class EquipmentAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['category', 'related_attribute', 'name']
    list_display = ["name", "category", "plus_dom", "plus_dom_2m", "force_min", "prot", "malus_armure", "related_skill",
                    "related_attribute", "enc", "price"]
    list_editable = ["category",  "enc", "price"]
    list_filter = ["category", "related_attribute", "related_skill"]
    actions = [refix, cat_from_first]

