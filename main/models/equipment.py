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
    can_be_thrown = models.BooleanField(default=False, blank=True)
    plus_dom = models.IntegerField(default=0, null=True, blank=True)
    plus_dom_2m = models.IntegerField(default=0, null=True, blank=True)
    prot = models.IntegerField(default=0, null=True, blank=True)
    classe_engagement = models.IntegerField(default=0, null=True, blank=True)
    cover = models.CharField(default="", max_length=64, blank=True)
    materiaux = models.CharField(default="", max_length=64, blank=True)
    related_skill = models.CharField(default="", max_length=32, blank=True)
    related_attribute = models.CharField(default="", max_length=8, blank=True)
    malus_armure = models.IntegerField(default=0, null=True, blank=True)
    force_min = models.IntegerField(default=0, null=True, blank=True)
    enc = models.FloatField(default=0, blank=True)
    description = models.TextField(default="", max_length=1024, blank=True)
    price = models.FloatField(default=0, blank=True)
    quantity = models.FloatField(default=0.1, blank=True)
    mod_ini = models.IntegerField(default=0, blank=True)
    mod_dom = models.IntegerField(default=0, blank=True)
    mod_att = models.IntegerField(default=0, blank=True)
    special = models.BooleanField(default=False, blank=True)
    similitude = models.TextField(default="", max_length=1024, blank=True)

    skill_match = models.CharField(default="", max_length=32, blank=True)

    def fix(self):
        self.rid = as_rid(f"{self.name}_{self.category}")
        # if self.cover != "":
        #     new_covers = []
        #     covers = self.cover.upper().split(" ")
        #     for cover in covers:
        #         if cover.startswith("H") == False and cover.startswith("P") == False:
        #             new_covers.append(cover)
        #     self.cover = " ".join(new_covers)
        #     self.cover = self.cover.replace("T","H").replace("B","A").replace("J","L").replace("1","S").replace("2","W")
        self.name = self.name.strip()
        if self.category in ["ana"]: # Armes naturelles
            self.price = 0
            self.enc = 0
        if self.category in ["mel","tir","lan"]:
            from main.utils.ref_dragonade import CHARACTER_STATISTICS
            self.skill_match = ""
            # print("SEARCH", self.name.upper())
            for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                # print(f'  Test: [{skill["TEXT"].upper()}]')
                if skill["TEXT"].upper().strip() == self.name.upper().strip():
                    self.related_skill = skill["NAME"]
                    # print("     MATCH",skill["TEXT"].upper(), self.name.upper(), skill["NAME"])
                    break
                # else:
                #     print(f'     Not matching with [{self.name.upper()}]')
            for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                if skill["NAME"].upper() == self.related_skill.upper():
                    self.skill_match = skill["TEXT"]
                    break

    def __str__(self):
        return f"{self.name} [{self.category}]"

    def covers(self,str=""):
        res = False
        if self.category == "amu":
            if self.cover != "":
                keys = self.cover.split(" ")
                for key in keys:
                    if str == key:
                        return True
        return res

    @property
    def related_skill_name(self):
        names = []
        if self.category in ["mel","tir","lan"]:
            if self.related_skill != "":
                from main.utils.ref_dragonade import CHARACTER_STATISTICS
                skills = self.related_skill.upper().strip().split(" ")
                for s in skills:
                    s
                    for skill in CHARACTER_STATISTICS['SKILLS']['WEAPONS']['LIST']:
                        if skill["NAME"].upper().strip() == s:
                            names.append(skill["TEXT"])
        return ", ".join(names)

    @classmethod
    def references(klass):
        list = []
        for item in klass.objects.order_by("name"):
            list.append({"name":item.name, "rid": item.rid})
        return list




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
    list_display = ["name", "rid", "category", "similitude","can_be_thrown", "cover", "plus_dom", "plus_dom_2m", "force_min", "prot", "malus_armure", "related_skill_name", "related_skill",
                    "related_attribute", "enc", "price", "skill_match"]
    list_editable = [ "cover","can_be_thrown","category", "prot", "malus_armure","related_skill"]
    list_filter = ["category", "can_be_thrown", "related_attribute", "related_skill", "special"]
    search_fields = ['name']
    actions = [refix, cat_from_first]

