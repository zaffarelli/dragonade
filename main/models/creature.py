import os
from django.db import models
from django.contrib import admin
from django.template.loader import get_template
from main.models.characters import Character
from main.utils.mechanics import roll
import io
from xhtml2pdf import pisa
from django.conf import settings


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

    def value_shift(self,param,back):
        current_value = getattr(self, param)
        if param == "creature_type":
            dataset = DragonadeCreatureType.values
        else:
            print(f"Unknown param {param} for {self.type}")
        next_value_index = 0
        for k, v in enumerate(dataset):
            if v == current_value:
                next_value_index = (k + back) % len(dataset)
        setattr(self, param, dataset[next_value_index])
        self.save()


    @classmethod
    def spawn(cls):
        item = cls()
        item.name = f"Nouveau ({roll(faces=12)}-{roll(faces=12)}-{roll(faces=12)})"
        item.save()
        return item.id

    @classmethod
    def export_to_pdf(cls):
        import datetime
        context = {"full_name": "Créatures", "release_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        context["type"] = "creatura"
        context["categories"] = {}
        for k,v in DragonadeCreatureType.choices:
            context["categories"][v] = [i.export_to_json() for i in cls.objects.filter(creature_type=k).order_by("name")]
        template = get_template('main/PDF/extract.html')
        html = template.render(context)
        filename = os.path.join(settings.MEDIA_ROOT, 'pdf/extracts/creature.pdf')
        es_pdf = open(filename, 'wb')
        pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), es_pdf)
        if not pdf.err:
            es_pdf.close()
        else:
            print(pdf.err)


class CreaturaAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['id','rid','name', 'attributes','secondaries', 'creature_type', 'team_color']
    list_filter = ["creature_type", 'team_color']
    list_editable = ['attributes','secondaries',"creature_type", 'team_color']
    from main.utils.mechanics import pre_sim, refix
    actions = [refix, pre_sim]
