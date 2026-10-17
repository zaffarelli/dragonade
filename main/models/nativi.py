import os

from django.db import models
from django.contrib import admin
from django.template.loader import get_template

from main.mixins.jsonable import JsonableMixin
import random
from main.models.characters import Character
from main.utils.mechanics import roll
from xhtml2pdf import pisa
import io
from django.conf import settings
import datetime


class Nativo(Character, JsonableMixin):
    class Meta:
        verbose_name = "Nativo"
        verbose_name_plural = "Nativi"

    # dream = models.CharField(max_length=264, default="", blank=True)
    spotlight = models.BooleanField(default=False, blank=True)
    nameless = models.BooleanField(default=False, blank=True)
    occupation = models.CharField(default="",max_length=64, blank=True)

    def __str__(self):
        return f"{self.rid}"

    def initial_randomize(self):
        x = ["4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4", "4"]
        random.shuffle(x)
        self.attributes = " ".join(x)

    def fix(self):
        super().fix()
        if self.is_new:
            self.initial_randomize()
            self.is_new = False



    def randomize(self):
        print("Randomizing Nativo")
        self.birthhour = roll(explodes=False,faces=12)
        attributes = ["4", "4", "4", "4", "4", "4", "4", "4", "4", "6", "7", "8"]
        random.shuffle(attributes)
        self.attributes = " ".join(attributes)
        all_values = [
            "6",
            "5", "5",
            "4", "4", "4",
            "3", "3", "3", "3",]
        random.shuffle(all_values)
        # r = roll(False, faces=10)
        spots = [0, 1, 1, 2, 4, 2]
        skills = [[], [], [], [], [], []]
        skills[0] = ["-5" for _ in range(6)]
        skills[1] = ["-4" for _ in range(10)]
        skills[2] = ["-3" for _ in range(10)]
        skills[3] = ["-2" for _ in range(16)]
        skills[4] = ["-1" for _ in range(16)]
        skills[5] = ["-1" for _ in range(18)]
        global_val_idx = 0
        cur_val_idx = 0
        cur_set = 0
        while cur_set < 6:
            print(f"Set #{cur_set:1} => {len(skills[cur_set]):3} GVI {global_val_idx:3} {spots[cur_set]:2}")
            while cur_val_idx < spots[cur_set]:
                skills[cur_set][cur_val_idx] = all_values[global_val_idx]
                cur_val_idx += 1
                global_val_idx += 1
            cur_val_idx = 0
            random.shuffle(skills[cur_set])
            cur_set += 1
        self.skills_draconic = " ".join(skills[0])
        self.skills_knowledge = " ".join(skills[1])
        self.skills_specialized = " ".join(skills[2])
        self.skills_peculiar = " ".join(skills[3])
        self.skills_generic = " ".join(skills[4])
        self.skills_weapons = " ".join(skills[5])



    @classmethod
    def spawn(cls):
        from main.models.sogni import Sogno
        s = Sogno.current_sogno()
        if s:
            sog = s.acronym
        else:
            sog = "DEF"
        item = cls()
        item.name = f"Autochtone_{roll(explodes=False, faces=10) - 1}{roll(explodes=False, faces=10) - 1}{roll(explodes=False, faces=10) - 1}"
        item.is_storyteller = True
        item.is_new = True
        item.sogni = sog
        item.save()
        return item.id

    @classmethod
    def export_to_pdf(cls):
        from main.models.sogni import Sogno
        s = Sogno.current_sogno()
        if s:
            sog = s.acronym
        else:
            sog = ""
        context = {"full_name": "Autochtones", "release_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        context["type"] = "nativo"
        context["categories"] = {}

        places = cls.objects.filter(sogni=sog).order_by("place").distinct().values_list("place", flat=True)
        lieux = [place for place in places]
        for lieu in lieux:
            context["categories"][lieu] = [i.export_to_json() for i in cls.objects.filter(sogni=sog,place=lieu).order_by("name")]
        template = get_template('main/PDF/extract.html')
        html = template.render(context)
        filename = os.path.join(settings.MEDIA_ROOT, 'pdf/extracts/nativi.pdf')
        es_pdf = open(filename, 'wb')
        pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), es_pdf)
        if not pdf.err:
            es_pdf.close()
            print(f"PDF exportation complete: {filename}")
        else:
            print(pdf.err)



class NativoAdmin(admin.ModelAdmin):
    from main.utils.mechanics import pre_sim, refix
    ordering = ['factions', 'group', 'team_color', 'name']
    list_display = ['name','rid', "sogni",'is_new','nameless', 'entrance', 'title', 'aka', 'is_female', "age", 'group']
    list_editable = ['is_new','sogni','title', 'aka', 'age']
    list_filter = ['team_color', 'factions', 'nameless', "is_female", "is_battle_ready", 'sogni','is_new']
    search_fields = ['name', 'title', 'factions', 'aka', 'sogni']
    actions = [refix, pre_sim]
