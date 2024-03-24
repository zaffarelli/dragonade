from django.db import models
from django.contrib import admin
from main.utils.mechanics import as_rid
from django.utils import timezone



class Dream(models.Model):
    title = models.CharField(default="", max_length=256, blank=True)
    subtitle = models.CharField(default="", max_length=256, blank=True)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    session_number = models.PositiveIntegerField(default=1, blank=True)
    date_run = models.DateField(default=timezone.now, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    current = models.BooleanField(default=False,blank=True)

    def fix(self):
        self.rid = as_rid(f"{self.title}_{self.subtitle}")

    def __str__(self):
        return f"{self.subtitle} [{self.title}]"


class DreamAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ["date_run",'title','session_number']
    list_display = ["rid", "title","current", "subtitle", "date_run", "session_number", "description"]
    list_editable = ["session_number","current","title", "subtitle", "description"]
    actions = [refix]
