from django.db import models
from django.contrib import admin

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.mechanics import as_rid, asShortB2B
from django.utils import timezone



class Sogno(models.Model, ChiaroscuroMixin):
    title = models.CharField(default="", max_length=256, blank=True)
    subtitle = models.CharField(default="", max_length=256, blank=True)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    code = models.CharField(default="", max_length=6, blank=True)
    description = models.CharField(default="", max_length=256, blank=True)
    session_number = models.PositiveIntegerField(default=1, blank=True)
    date_run = models.DateField(default=timezone.now, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    current = models.BooleanField(default=False,blank=True)
    population = models.PositiveIntegerField(default=0,blank=True)

    def fix(self):
        self.chiaroscuro()
        self.rid = as_rid(f"{self.title}_{self.subtitle}")
        self.code = asShortB2B(self.rid).decode('utf-8').upper()
        from main.models.nativi import Nativo
        self.population = len(Nativo.objects.filter(dream=self.rid))

    def __str__(self):
        return f"{self.title} [{self.code}]"


class SognoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ["date_run",'title','session_number']
    list_display = ["code", "title","current", "subtitle", "date_run", "session_number", "description", "population"]
    list_editable = ["session_number","current","title", "subtitle", "description"]
    actions = [refix]
