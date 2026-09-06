from django.db import models
from django.contrib import admin

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.mechanics import as_rid, asShortB2B
from django.utils import timezone


class Sogno(models.Model, ChiaroscuroMixin):
    class Meta:
        verbose_name_plural = "Sogni"

    title = models.CharField(default="", max_length=256, blank=True)
    subtitle = models.CharField(default="", max_length=256, blank=True)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    code = models.CharField(default="", max_length=6, blank=True)
    acronym = models.CharField(default="", max_length=10, blank=True)
    description = models.CharField(default="", max_length=256, blank=True)
    sort_order = models.PositiveIntegerField(default=1, blank=True)
    date_run = models.DateField(default=timezone.now, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    current = models.BooleanField(default=False, blank=True)
    population = models.PositiveIntegerField(default=0, blank=True)
    viaggiatori = models.PositiveIntegerField(default=0, blank=True)
    nativi = models.PositiveIntegerField(default=0, blank=True)
    creature = models.PositiveIntegerField(default=0, blank=True)

    def fix(self):
        self.chiaroscuro()
        self.rid = as_rid(f"{self.title}_{self.subtitle}")
        self.code = asShortB2B(self.rid).decode('utf-8').upper()
        self.update_population()

    def update_population(self):
        from main.models.nativi import Nativo
        from main.models.viaggiatori import Viaggiatore
        from main.models.creature import Creatura
        self.viaggiatori = len(Viaggiatore.objects.filter(sogni__contains=self.acronym))
        self.nativi = len(Nativo.objects.filter(sogni__contains=self.acronym))
        self.creature = len(Creatura.objects.filter(sogni__contains=self.acronym))

    def __str__(self):
        return f"{self.title} [{self.code}]"

    @classmethod
    def nav(cls,x):
        all = cls.objects.all()
        cnt = len(all)
        current = cls.objects.filter(current=True).first()
        idx = (current.sort_order+x)%cnt
        for s in all:
            if idx == s.sort_order:
                s.current = True
            else:
                s.current = False
            s.save()




class SognoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['sort_order',"date_run", 'title' ]
    list_display = ["id", "rid", "acronym", "code", "title", "current", "subtitle", "date_run", "sort_order", "description", "viaggiatori", "nativi",
                    "creature"]
    list_editable = ["acronym", "sort_order", "current", "title", "subtitle", "description"]
    actions = [refix]
