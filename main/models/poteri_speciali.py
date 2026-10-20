from django.contrib import admin
from django.db import models

from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.mechanics import as_rid, roll


class UsageLimit(models.IntegerChoices):
    NONE = 0, "Unique"
    HD = 1, "Heure Draconique"
    DD = 2, "Jour Draconique"
    CIRC = 3, "Circonstances"
    WILL = 4, "A volonté"


class PowerType(models.IntegerChoices):
    NAT = 0, "Talent Naturel"
    ONI = 1, "Capacité Onirique"
    CAU = 2, "Faculté Cauchemardesque"


class Roll(models.IntegerChoices):
    NONE = 0, "-"
    CONTEMPLATIVE = 1, "Contemplatif"
    DESTRUCTIVE = 2, "Destructif"
    DYNAMIC = 3, "Dynamique"
    GENERATIVE = 4, "Génératif"
    MNEMONIC = 5, "Mnémonique"
    STATIC = 6, "Statique"


class PotereSpeciale(models.Model, ChiaroscuroMixin):
    class Meta:
        ordering = ['name']
        verbose_name = "Potere Speciale"
        verbose_name_plural = "Poteri Speciali"

    name = models.CharField(default="", max_length=256)
    rid = models.CharField(default="xxx", max_length=256, blank=True)
    pdr_cost = models.PositiveIntegerField(default=0, blank=True)
    power = models.PositiveIntegerField(default=0, blank=True)
    usage_limit = models.IntegerField(default=UsageLimit.NONE, choices=UsageLimit.choices, blank=True)
    power_type = models.IntegerField(default=PowerType.NAT, choices=PowerType.choices, blank=True)
    roll = models.IntegerField(default=Roll.NONE, choices=Roll.choices, blank=True)
    rationale = models.TextField(default="", max_length=1024, blank=True)
    description = models.TextField(default="", max_length=2048, blank=True)

    def fix(self):
        self.chiaroscuro()
        self.rid = as_rid(f"{self.name}")
        # self.name = self.name.replace("  ", " ")
        # self.name = self.name.strip()

    def __str__(self):
        return f"{self.name}"

    def export_to_json(self):
        self.model_to_data()
        return self._data

    def co_push(self):
        self._data['power_type_str'] = self.get_power_type_display()
        self._data['usage_limit_str'] = self.get_usage_limit_display()
        self._data['roll'] = self.get_roll_display()

    def applyValuePush(self, att, val):
        setattr(self,att, val)
        self.save()
        return True

    @classmethod
    def extract_from_list(cls, str):
        items = str.split(" ")
        rids = [item.strip() for item in items]
        poteri = cls.objects.filter(rid__in=rids)
        return poteri

    @classmethod
    def spawn(cls):
        item = cls()
        item.name = f"PouvoirSpeciaux_{roll(explodes=False,faces=10)-1}{roll(explodes=False,faces=10)-1}{roll(explodes=False,faces=10)-1}"
        item.save()
        return item.id

    @classmethod
    def export_to_pdf(cls):
        pass
        # context = {"full_name": "Voyageurs", "release_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        # context["type"] = "viaggiatore"
        # context["categories"] = {}
        # context["categories"]["PNJ"] = [i.export_to_json() for i in cls.objects.filter(is_storyteller=True).order_by("name")]
        # context["categories"]["PJ"] = [i.export_to_json() for i in cls.objects.filter(is_storyteller=False).order_by("name")]
        # template = get_template('main/PDF/extract.html')
        # html = template.render(context)
        # filename = os.path.join(settings.MEDIA_ROOT, 'pdf/extracts/viaggiatori.pdf')
        # es_pdf = open(filename, 'wb')
        # pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), es_pdf)
        # if not pdf.err:
        #     es_pdf.close()
        #     print(f"PDF exportation complete: {filename}")
        # else:
        #     print(pdf.err)


class PotereSpecialeAdmin(admin.ModelAdmin):
    from main.utils.mechanics import refix
    ordering = ['name']
    list_display = ["rid", "name", "power", "pdr_cost", "usage_limit", "get_usage_limit_display", "description", "rationale"]
    list_editable = ["power", "pdr_cost", "rationale", "description", "usage_limit"]
    search_fields = ['name', 'description', 'rationale']
    actions = [refix]
