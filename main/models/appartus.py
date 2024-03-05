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
    owner = models.CharField(default="", max_length=256, blank=True)
    glance = models.CharField(default="", max_length=256, blank=True)
    materials = models.CharField(default="", max_length=256, blank=True)
    scales = models.CharField(default="e", max_length=256, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    mastery = models.PositiveIntegerField(default=0, blank=True)
    inertia = models.IntegerField(default=0, blank=True)
    dps = models.IntegerField(default=0, blank=True)

    mod_init = models.IntegerField(default=0, blank=True)
    mod_touch = models.IntegerField(default=0, blank=True)
    mod_dmg = models.IntegerField(default=0, blank=True)

    price = models.PositiveIntegerField(default=1000, blank=True)
    data = {}

    def fix(self):
        self.rid = as_rid(f"{self.name}{self.category}")

    def __str__(self):
        return f"{self.name} [{self.category}]"

    @property
    def get_equipment(self):
        str = "---"
        if (self.equipment_match) != "xxx":
            str = self.equipment_match
        return str

    def export_to_json(self):
        data = {}
        data['name'] = self.name
        data['rid'] = self.rid
        data['category'] = self.get_category_display()
        data['materials'] = self.materials
        data['glance'] = self.glance
        data['owner'] = self.owner
        data['mastery'] = self.mastery
        data['type'] = self.get_equipment
        data['inertia'] = self.inertia
        data['dps'] = self.dps
        data['scales'] = self.scales
        data['description'] = self.description
        data['mod_init'] = self.mod_init
        data['mod_touch'] = self.mod_touch
        data['mod_dmg'] = self.mod_dmg
        self.data = data
        return data


class AppartusAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ["name", "rid","equipment_match","mod_init","mod_touch","mod_dmg", "owner","category","glance","materials","description"]
    list_filter = ['category','category']
    search_fields = ['name',"description"]
    list_editable = ["equipment_match","category","mod_init","mod_touch","mod_dmg"]
    actions = [refix]
