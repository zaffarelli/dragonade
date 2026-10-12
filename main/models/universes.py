from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid, roll
from colorfield.fields import ColorField


class Universe(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = "Universe"
        verbose_name_plural = "Universes"

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    description = models.TextField(default="", max_length=2048, blank=True)
    palette1 = ColorField(default="#888888", max_length=9, blank=True)
    palette2 = ColorField(default="#888888", max_length=9, blank=True)
    palette3 = ColorField(default="#888888", max_length=9, blank=True)
    is_current = models.BooleanField(default=False, blank=True)

    def fix(self):
        self.rid = as_rid(f"{self.name}")
        self.name = self.name.replace("  ", " ")
        self.name = self.name.strip()
        if self.is_current:
            universes = Universe.objects.exclude(name=self.name)
            for universe in universes:
                universe.is_current = False
                universe.save()

    def __str__(self):
        return f"{self.name}"




class UniverseAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ["rid", "name", "palette1", "palette2", "palette3", "description","is_current"]
    list_editable = ["palette1", "palette2", "palette3", "description","is_current"]
    search_fields = ['name', 'description']
    actions = [refix]
