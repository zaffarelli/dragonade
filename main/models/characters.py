from django.db import models
from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.utils.ref_dragonade import CHARACTER_STATISTICS, tai_guidelines, SHORTCUTS, stress_cost
from main.utils.mechanics import as_rid, Nougardine, roll, Severity, Chaser
import math


class Character(models.Model, ChiaroscuroMixin):
    class Meta:
        abstract = True

    name = models.CharField(max_length=256)
    rid = models.CharField(max_length=256, default="", blank=True)
    randomize = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=256, default="", blank=True)
    aka = models.CharField(max_length=256, default="", blank=True)
    figure = models.CharField(max_length=256, default="", blank=True)
    group = models.CharField(max_length=256, default="", blank=True)
    team = models.CharField(max_length=256, default="", blank=True)
    factions = models.CharField(max_length=256, default="", blank=True)
    entrance = models.CharField(max_length=256, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    is_female = models.BooleanField(default=False, blank=True)
    is_lefty = models.BooleanField(default=False, blank=True)
    is_battle_ready = models.BooleanField(default=False, blank=True)
    age = models.PositiveIntegerField(default=20, blank=True)
    height = models.PositiveIntegerField(default=10, blank=True)
    weight = models.PositiveIntegerField(default=50, blank=True)
    SON = models.IntegerField(default=0, blank=True)
    FAB = models.IntegerField(default=0, blank=True)
    REV = models.IntegerField(default=0, blank=True)
    IMP = models.IntegerField(default=0, blank=True)
    ENC = models.FloatField(default=0.0, blank=True)
    SUS = models.IntegerField(default=0, blank=True)
    RES = models.IntegerField(default=0, blank=True)
    FAT = models.IntegerField(default=0, blank=True)
    VIE = models.IntegerField(default=0, blank=True)
    prot = models.IntegerField(default=0, blank=True)
    color = models.CharField(max_length=9, default="#808080", blank=True)
    team_color = models.CharField(max_length=10, default="", blank=True)
    gamers_team = models.BooleanField(default=False, blank=True)
    gear = models.TextField(max_length=1024, default="", blank=True)
    spells = models.TextField(max_length=1024, default="", blank=True)
    bug_list = models.TextField(default="", max_length=1024, blank=True)
    imc = models.FloatField(default=0, blank=True)
    place = models.CharField(max_length=256, default="", blank=True)
    attributes = models.CharField(max_length=64, default="", blank=True)
    secondaries = models.CharField(max_length=64, default="", blank=True)
    skills_weapons = models.CharField(max_length=128, default="", blank=True)
    skills_generic = models.CharField(max_length=128, default="", blank=True)
    skills_peculiar = models.CharField(max_length=128, default="", blank=True)
    skills_specialized = models.CharField(max_length=128, default="", blank=True)
    skills_knowledge = models.CharField(max_length=128, default="", blank=True)
    skills_draconic = models.CharField(max_length=128, default="", blank=True)
    indice = models.IntegerField(default=0, blank=True)
    indice_attributes = models.IntegerField(default=0, blank=True)
    indice_skills = models.IntegerField(default=0, blank=True)
    tai_guideline = models.CharField(max_length=128, default="", blank=True)
    total_attributes = models.IntegerField(default=0, blank=True)
    total_skills = models.IntegerField(default=0, blank=True)
    # updater = models.TextField(max_length=1024 * 10, default='{}', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    klass = models.CharField(max_length=16, default="Character", blank=True)
    protection_map = models.CharField(max_length=256, blank=True, default="H-0-X C-0-X A-0-X B-0-X L-0-X M-0-X")

    travel_points = models.IntegerField(default=0, blank=True)
    stress_acquired = models.IntegerField(default=0, blank=True)
    stress_used = models.IntegerField(default=0, blank=True)
    stress_remaining = models.IntegerField(default=0, blank=True)

    malus_AGI = models.IntegerField(default=0, blank=True)
    malus_DEX = models.IntegerField(default=0, blank=True)
    malus_VUE = models.IntegerField(default=0, blank=True)
    malus_OUI = models.IntegerField(default=0, blank=True)

    description = models.TextField(max_length=1024, default="", blank=True)

    # data = {}

    def __str__(self):
        return f"p_{self.id}"

    def make_rid(self):
        if len(self.rid) == 0:
            self.rid = as_rid(self.name)
            self.rid = self.type[:3].upper() + "_" + self.rid

    @property
    def type(self):
        return self.__class__.__name__

    def applyIncDec(self, att, chg):
        self.export_to_json()
        result = False
        offset = 0
        if chg == 'plus':
            offset = 1
        elif chg == 'minus':
            offset = -1

        if offset:
            val = self.value_for(att)
            # print(f"{val} type:{type(val).__name__}")
            if type(val).__name__ == "str":
                val = int(val)
            val += offset
            result = self.overwrite_for(att, val)
            if result:
                # self.updateFromStruct()
                self.save()
        return result

    def applyValuePush(self, att, val):
        # self.export_to_json()
        result = self.overwrite_for(att, val)
        print(result)
        if result:
            # self.updateFromStruct()
            self.save()
        return result

    def has_bug(self):
        return len(self.bug_list) > 0

    has_bug.boolean = True

    def fix(self):
        self.chiaroscuro()
        # initializers
        if len(self.protection_map) == 0:
            self.protection_map = "H-0-X C-0-X AS-0-X AW-0-X LS-0-X LW-0-X"
        if self.birthhour == 0:
            self.birthhour = roll(faces=12, explodes=False)
        self.initialize()
        self.make_rid()

        self.bug_list = "BUGS:"
        self.calc_indice()
        self.challenge_equipment_and_skills()
        secondaries = [0, 0, 0, 0]
        for k in CHARACTER_STATISTICS['SECONDARIES']['LIST']:
            if "FORMULA" in k:
                val = self.from_formula(k['PARAMS'], k['FORMULA'])
                secondaries[k['ORDER']] = str(val)
        self.secondaries = " ".join(secondaries)
        for k in CHARACTER_STATISTICS['MISC']['LIST']:
            if "FORMULA" in k:
                val = self.from_formula(k['PARAMS'], k['FORMULA'])
                setattr(self, k["NAME"], val)
        self.tai_guideline = tai_guidelines(self.value_for('TAI'))
        if self.height > 0:
            self.imc = math.floor(self.weight / ((self.height / 100) ** 2) * 10) / 10
        self.fix_protection_map()
        # self.export_to_json()

    def initialize(self):
        """
            Initialize model properties:
            - attributes to 1
            - secondaries to 1
            - skills_x properties with default values according to reference.
            And do all of this according to the reference.
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        if len(self.attributes) == 0:
            list = ["1" for _ in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']]
            self.attributes = " ".join(list)
        if len(self.secondaries) == 0:
            list = ["1" for _ in CHARACTER_STATISTICS['SECONDARIES']['LIST']]
            self.secondaries = " ".join(list)
        for k, cat in CHARACTER_STATISTICS['SKILLS'].items():
            list = [f"{cat['DEFAULT']}" for _ in cat['LIST']]
            tgt_property = f"skills_{k.lower()}"
            if len(getattr(self, tgt_property)) == 0:
                setattr(self, tgt_property, " ".join(list))

    def calculate_team(self):
        import hashlib
        gfg = hashlib.blake2s(digest_size=2)
        gfg.update(bytes(self.team, 'UTF-8'))
        x = gfg.digest()
        self.team_color = x.decode('UTF-8')
        return self.team_color

    @classmethod
    def stress_map(cls):
        xspan = [-10, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        yspan = [-5, -4, -3, -2, -1, 0]
        for x in xspan:
            if x == -10:
                print(f"{'--------------------- Table de Stress ---------------------':>59}")
                print(f"  V à V+1 ", end="\t")
            else:
                print(f"{x:3} à {x + 1:3} ", end="\t")
            for y in yspan:
                if x >= y:
                    i = stress_cost(x, x + 1, y)
                    print(f"{i:3}", end="\t")
                if x == -10:
                    print(f"{y:3}", end="\t")
            print("")
        print("(Les attributs sont considérés à -5)")

    def expected_totals(self):
        attr_total, skill_total = 0, 0
        if self.__class__.__name__ == "Viaggiatore":
            attr_total, skill_total = 126, 145
        elif self.__class__.__name__ == "Nativo":
            attr_total, skill_total = 114, 50
        elif self.__class__.__name__ == "Creatura":
            attr_total, skill_total = 0, 0
        return attr_total, skill_total

    def calc_indice(self):
        from main.utils.ref_dragonade import stress_cost, skill_cost
        self.total_attributes = 0

        for a in self.attributes.split(" "):
            self.total_attributes += int(a) + 5

        # for skill_cat in self.data['skills']:
        #     for k, v in self.data['skills'][skill_cat].items():
        #         c, txt = skill_cost(k, v)
        #         if c > -1:
        #             self.indice_skills += c
        # self.indice_attributes = int(self.indice_attributes / 3)
        # self.indice_skills = int(self.indice_skills / 3)
        # self.indice = self.indice_attributes + self.indice_skills
        # self.indice = self.total_attributes - (12 * 4)
        # self.indice += self.data['misc']['SON'] * 3

        self.total_skills = 0
        default = 0
        nondefault_cnt = 0
        for kc, vc in CHARACTER_STATISTICS['SKILLS'].items():
            for ks in vc['LIST']:
                v = int(self.value_for(ks['NAME']))
                base = vc['DEFAULT']
                default += base
                if v != base:
                    nondefault_cnt += 1
                    self.total_skills += v - base
        # a, b = self.collect_spells()
        # print("Total spells", b)
        # self.indice += self.total_skills + b
        # self.indice -= default
        # self.indice += self.data['misc']['PROT'] * 2
        # self.indice += self.data['misc']['SON'] ** 2
        self.REV = self.SON + self.FAB
        a, s = self.expected_totals()
        self.total_attributes -= a
        self.total_skills -= s

    # def updateFromStruct(self):
    #     list = []
    #     for k in CHARACTER_STATISTICS['ATTRIBUTES']['LIST']:
    #         list.append(f"{self.data['attributes'][k['NAME']]}")
    #     self.attributes = " ".join(list)
    #
    #     for key, category in CHARACTER_STATISTICS['SKILLS'].items():
    #         list = []
    #         for k in category['LIST']:
    #             vs = f"{self.data['skills'][key.lower()][k['NAME']]}"
    #             list.append(vs)
    #         setattr(self, f"skills_{key.lower()}", " ".join(list))
    #
    #     self.height = int(self.data['features']['HEIGHT'])
    #     self.weight = int(self.data['features']['WEIGHT'])
    #     self.fable = int(self.data['misc']['FAB'])
    #     self.songe = int(self.data['misc']['SON'])
    #     self.entrance = self.data['misc']['ENTRANCE']
    #     self.description = self.data['misc']['DESCRIPTION']
    #     self.age = self.data['features']['AGE']
    #     self.aka = self.data['features']['AKA']
    #     self.is_female = self.data['features']['GENDER'] == "F"
    #     self.is_lefty = self.data['features']['LEFTY'] == "G"
    #     self.gear = self.data['features']['GEAR']
    #     self.spells = self.data['features']['SPELLS']
    #     self.spells_as_list = self.data['features']['SPELLS'].split(" ")

    def ref_to_struct(self, src_ref):
        """        
            self.attributes -> self._data['attributes'], self.skills_generic -> self._data['skills']['generic']
            :param src_ref: source reference among the user filled properties o f the instance
            :returns: nothing / works directly on the instance
        """
        if len(src_ref) > 0:
            transversal = src_ref.split('_')
            src_struct = CHARACTER_STATISTICS
            for p in transversal:
                src_struct = src_struct[p]
            tlow = transversal[0].lower()
            branch = tlow[:4]
            if len(transversal) == 1:
                if tlow == "attributes":
                    cnt = 0
                    arr = getattr(self, tlow).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
                elif tlow == "secondaries":
                    cnt = 0
                    arr = getattr(self, tlow).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
            elif len(transversal) == 2:
                if tlow == "skills":
                    cnt = 0
                    self._data[branch][transversal[1].lower()] = {}
                    arr = getattr(self, src_ref.lower()).split(' ')
                    for item in src_struct['LIST']:
                        self._data[branch][transversal[1].lower()][item['NAME']] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        cnt += 1
            else:
                print(f"!!! Error: Don't know what to do with [{src_ref}]...")

    def skills_summary(self):
        """
            Select only skills with a non default value.
            :returns: JSON list of the skills with a non default value.
        """
        all = []
        SKILLS = CHARACTER_STATISTICS["SKILLS"]
        count_vals = [0 for _ in range(20)]
        count_postes = [0 for _ in range(6)]
        skill_sets = ["weapons", "generic", "peculiar", "specialized", "knowledge", "draconic"]
        for skill_set in skill_sets:
            REF = SKILLS[skill_set.upper()]
            data = getattr(self, "skills_" + skill_set)
            default = REF["DEFAULT"]
            arr = data.split(" ")
            if len(arr) == len(REF["LIST"]):
                for item in REF["LIST"]:
                    if "ORDER" in item:
                        pos = item["ORDER"]
                        v = int(arr[pos])
                        if v > default:
                            count_postes[default * (-1)] += 1
                            count_vals[v] += 1
                            all.append({"value": v, "category": REF['NAME'][:1], "text": item["TEXT"]})
            else:
                self.bug_list += f"{self.rid} doesn't have the correct property for [{skill_set}]."
        sorted_all = sorted(all, key=lambda k: k['text'], reverse=False)
        return sorted_all

    def export_to_json(self):
        """
            :returns: JSON structure for the instance.
        """
        self.model_to_data()
        return self._data

    def co_push(self):
        """
            Push the contextual data to the self._data structure.
            Most of the job is done through the chiaroscuro mixin, here we only add convenience entries or business centerd entries.
            :returns: The updated self._data structure
        """
        # print("### CO_PUSH character")
        self._data["attr"] = {}
        self._data["seco"] = {}
        self._data["skil"] = {}
        self._data["deri"] = {}

        # self.data['deri'][k['NAME']] = val
        self.ref_to_struct('ATTRIBUTES')
        self.ref_to_struct('SECONDARIES')
        self.ref_to_struct('SKILLS_WEAPONS')
        self.ref_to_struct('SKILLS_GENERIC')
        self.ref_to_struct('SKILLS_PECULIAR')
        self.ref_to_struct('SKILLS_SPECIALIZED')
        self.ref_to_struct('SKILLS_KNOWLEDGE')
        self.ref_to_struct('SKILLS_DRACONIC')
        self._data['fatigue_points'], self._data['fatigue_map'] = self.computeFatigue(self.FAT)
        self._data['has_bug'] = self.has_bug()
        self._data['spells'] = self.collect_spells()
        self._data['shortcuts'] = self.shortcuts()
        self._data['weapons'] = self.gear_to_weapons()
        self._data['other'] = self.gear_to_other()
        self._data['armors'] = self.gear_to_armors()
        self._data['GENDER'] = self.is_female
        self._data['LEFTY'] = self.is_lefty
        self._data["skills_summary"] = self.skills_summary()
        self._data['roster_text'] = self.roster_as_text()
        from datetime import datetime
        now = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        self._data['last_update'] = now

    def computeFatigue(self, x):
        i = x
        pf_total = 0
        str = ""
        k = 0
        while i > 0:
            pf = 2 + math.ceil(i / 2)
            for z in range(pf):
                str += f"o "
                k += 1
            str += "__nl__"
            i -= 1
            pf_total += pf
        return pf_total, str

    def gear_to_weapons(self):
        """
            Grab elements from the gear stack list that are neither weapons.
            :returns: JSON list of the elements fetched.
        """
        from main.models.oggetti import Oggetto
        list = []
        weapons = Oggetto.objects.filter(category__in=['mel', 'tir', 'lan'], rid__in=self.gear.split(" ")).order_by(
            "category")
        for weapon in weapons:
            stat_value = self.value_for(weapon.category.upper())
            related_skills = weapon.related_skill.split(" ")
            d = weapon.export_to_json()
            worst = 1000
            for related_skill in related_skills:
                val = self.value_for(related_skill)
                if int(val) < worst:
                    worst = int(val)
                    d['related_skill_value'] = int(val)
                    e = self.entry_for("SKILLS:WEAPONS",related_skill)
                    if e != {}:
                        d['related_skill_text'] = e["TEXT"]

            # All data for the weapon

            # Data specific to the character applied to the wepon's data
            d['stat_value'] = stat_value
            d['IMP'] = self.IMP
            d['base_score'] = int(stat_value) + int(d['related_skill_value'])
            d['stat_skill'] = f"{stat_value}+{d['related_skill_value']}={int(stat_value) + int(d['related_skill_value'])}"
            list.append(d)
        return list

    def gear_to_other(self):
        """
            Grab elements from the gear stack list and get all of those that are neither armor or weapon.
            :returns: JSON list of the elements fetched.
        """
        from main.models.oggetti import Oggetto
        list = []
        others = Oggetto.objects.exclude(category__in=['mel', 'tir', 'lan']).filter(
            rid__in=self.gear.split(" ")).order_by("category")
        for other in others:
            o = other.export_to_json()
            list.append(o)
        return list

    def gear_to_armors(self):
        from main.models.oggetti import Oggetto
        list = []
        pmap = {}
        words = self.protection_map.split(" ")
        for word in words:
            if len(word) > 0:
                pieces = word.split("-")
                pmap[pieces[0]] = {"protection": pieces[1], "source": pieces[2]}
        armors = Oggetto.objects.filter(prot__gte=1, rid__in=self.gear.split(" ")).order_by("materiaux")
        for armor in armors:
            x = armor.prot
            a = armor.export_to_json()
            a["numeric_cover"] = ""
            parts = armor.cover.split(" ")
            for part in parts:
                # print(a["numeric_cover"])
                if part == "-":
                    a["numeric_cover"] += f"0 "
                else:
                    a["numeric_cover"] += f"{x} "
            a["numeric_cover"].strip()
            list.append(a)
        return list

    def collect_spells(self):
        from main.models.incantessimi import Incantessimo
        list = []
        incantessimi = Incantessimo.objects.filter(rid__in=self.spells.split(" ")).order_by("category")
        for incantessimo in incantessimi:
            list.append(incantessimo.rid)
        # sorted_all = sorted(list, key=lambda k: k['diff'], reverse=False)
        return list

    def shortcuts(self):
        list = []
        # for sc in SHORTCUTS:
        #     attr = self.value_for(sc[1])
        #     skill = self.value_for(sc[2])
        #     # print(sc, attr, skill)
        #     list.append({
        #         "roll": sc[0],
        #         "val": attr + skill
        #     })
        return list

    def from_formula(self, params, formula):
        parameter_values = []
        for p in params.split(" "):
            if len(p) > 0:
                val = int(self.value_for(p))
                parameter_values.append(val)
        return formula(parameter_values)

    def value_for(self, str):
        # print(f"### Value for")
        result = -1000
        where = self.index_for(str)
        entry = self.entry_for(where, str)
        if entry != {}:
            # print(f"### Values : {str} => {where}")
            if "ORDER" in entry:
                verbs = where.lower().split(':')
                datalist = getattr(self, "_".join(verbs))
                # print(f"Key:{'_'.join(verbs):20} Value:{datalist} [Type:{type(datalist)}]")
                # print(f"### ORDER = {entry['ORDER']}")
                if type(datalist).__name__ == 'str':
                    parts = datalist.split(" ")
                    result = parts[entry["ORDER"]]
                else:
                    result = datalist[entry["ORDER"]]
                # print(f"### Result = {result}")
            else:
                result = getattr(self, entry['NAME'])
        return result

    def overwrite_for(self, str, val):
        # print("OVERWRITE FOR")
        result = False
        where = self.index_for(str)
        # print(f"## WHERE {where}")
        entry = self.entry_for(where, str)
        # print(f"## ENTRY {entry}")
        if entry != {}:
            if "ORDER" in entry:
                verbs = where.lower().split(':')
                # print(f"***Trying to get {'_'.join(verbs)}")
                datalist = getattr(self, "_".join(verbs))
                # print(f"*** {datalist} type:{type(datalist)}")
                parts = datalist.split(" ")
                parts[entry["ORDER"]] = f"{val}"
                setattr(self, "_".join(verbs), " ".join(parts))
                self.save()
                result = True
            else:
                setattr(self, entry['NAME'].lower(), val)
                self.save()
                result = True
        return result

    def entry_for(self, str, stat):
        """
            :param str: the dataset_name
            :param stat: the value that entry must match with property NAME
            :returns: the full entry, or {}
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        root = CHARACTER_STATISTICS
        result = {}
        # print(f"ENTRY FOR {str} {stat}")
        if len(str) > 0:
            words = str.upper().split(':')
            for word in words:
                root = root[word]
            for item in root["LIST"]:
                if item["NAME"] == stat.upper():
                    result = item
                    break
        # print(f"ENTRY RESULT {item}")
        return result

    def index_for(self, str):
        """
        :param str: The code for the stat
        :returns: the position in the description as a:b:c
        """
        # print("INDEX FOR")
        from main.utils.ref_dragonade import known
        choices = ["ATTRIBUTES", "SKILLS:WEAPONS", "SKILLS:GENERIC", "SKILLS:PECULIAR", "SKILLS:SPECIALIZED", "SKILLS:KNOWLEDGE", "SKILLS:DRACONIC",
                   "SECONDARIES", "MISC", "FEATURES"]
        for choice in choices:
            result = known(choice, str)
            if len(result) > 0:
                break
        return result

    def roster(self):
        # return "Disabled for now."
        lines = []
        lines.append(f"{self.name}")
        if self.aka != "":
            lines.append(f"{self.aka}")
        if self.entrance != "":
            lines.append(f"{self.entrance}")
        if self.title != "":
            lines.append(f"{self.title}")
        ty = "Créature"
        subty = ""
        if self.type == "Viaggiatore":
            ty = f"({self.player})"
        if self.type == "Nativo":
            ty = "Autochtone"
        if self.type == "Creatura":
            subty = (f" ({self.get_creature_type_display()})")
            ty += subty

        lines.append(f"{ty}")
        attributes = ""
        space = "§"
        x = 0
        a = ["", "", "", ""]
        for k, v in self._data["attr"].items():
            a[x % 4] += f"{k} {v!s:{space}>2} "
            x += 1
        x = 0
        for k, v in self._data["seco"].items():
            a[x % 4] += f"| {k} {v!s:{space}>2} "
            x += 1
        x = 0
        m = ["VIE", "FAT", "SUS", "RES"]
        for v in m:
            a[x % 4] += f"| {v} {getattr(self, v)!s:{space}>2} "
            x += 1
        x = 0
        m = ["IMP", "ENC", "FAB", "REV"]
        for v in m:
            a[x % 4] += f"| {v} {getattr(self, v)!s:{space}>2} "
            x += 1
        attributes = f"{a[0]}<br/>{a[1]}<br/>{a[2]}<br/>{a[3]}<br/>"
        lines.append(attributes)

        categories = {
            "M": {"title": "Martiales (-1)", "list": []},
            "G": {"title": "Génériques (-1)", "list": []},
            "P": {"title": "Particulières (-2)", "list": []},
            "S": {"title": "Spécifiques (-3)", "list": []},
            "C": {"title": "Connaissances (-4)", "list": []},
            "D": {"title": "Draconiques (-5)", "list": []}
        }
        for v in self._data["skills_summary"]:
            categories[v["category"]]["list"].append(f"{v['text']} {v['value']:2}")

        skills = ""
        for k, v in categories.items():
            skills += v["title"] + ": "
            skills += ", ".join(v["list"]) + ".<br/>"
        lines.append(skills)

        weapons = f"{'Arme':{space}<20} {'DOMA':{space}>6} {'2M':{space}>6} {'INIT':>6} {'Jet':>10} {'Score':>8}<br/>"
        for w in self._data["weapons"]:
            weapons += f"{w['name']:{space}<20} "
            # print(w)
            if w['category'] == "mel":
                if w['plus_dom'] != 0:
                    d1 = f"{w['plus_dom']}+{self.IMP}"
                    weapons += f"{d1:{space}>6} "
                else:
                    weapons += f"{'-':{space}>6} "

                if w['plus_dom_2m'] != 0:
                    d2 = f"{w['plus_dom_2m']}+{math.floor(self.IMP * 1.5)}"
                    weapons += f"{d2:{space}>6} "
                else:
                    weapons += f"{'-':{space}>6} "
            else:
                weapons += f"{w['plus_dom']:{space}>13} "
            weapons += f"{w['mod_ini']:{space}>6} {w['stat_skill']:{space}>10} {w['base_score']:{space}>8}<br/>"
        lines.append(weapons)

        protection = f'{"Armure/Protection":{space}<35}{"Malus":{space}>25}{"Prot":{space}>6}<br/>'
        for a in self._data['armors']:
            all_malus = f'AGI {a["malus_AGI"]} DEX {a["malus_DEX"]} VUE {a["malus_VUE"]} OUI {a["malus_OUI"]}'
            protection += f"{a['name']:{space}<35}{all_malus:{space}>25}{a['prot']:{space}>6}<br/>"
        lines.append(protection)

        lines.append(f"Description: {self.description}<br/>")

        lines_VIE = []
        life = ""
        # &#9744;
        for x in range(self.VIE):
            life += "o "
            if x % 5 == 4:
                lines_VIE.append(f"{life}")
                life = ""
        if len(life) > 0:
            lines_VIE.append(f"{life}")

        lines_REV = []
        dream = ""
        # &#9744;
        for x in range(self.REV * 3):
            dream += "o "
            if x % self.REV == self.REV - 1:
                lines_REV.append(f"{dream}")
                dream = ""
        if len(dream) > 0:
            lines_REV.append(f"{dream}")

        _, fatigue = self.computeFatigue(self.FAT)
        # fatigue = fatigue.replace("o","&#9744;")
        lines_FAT = fatigue.split("__nl__")
        txt_v = f"PdV ({self.VIE})"
        txt_f = f"PdF ({self.FAT})"
        txt_r = f"PdR ({self.REV})"
        lines.append(f"{txt_v:<14}{txt_f:<20}{txt_r:<20}")
        for x in range(max(len(lines_VIE), len(lines_FAT), len(lines_REV))):
            s = ""
            nope = 0
            if x < len(lines_VIE):
                s += f"{lines_VIE[x]:<14}"
            else:
                s += f"{'':<14}"
                nope += 1
            if x < len(lines_FAT):
                s += f"{lines_FAT[x]:<20}"
            else:
                s += f"{'':<20}"
                nope += 1
            if x < len(lines_REV):
                s += f"{lines_REV[x]:<20}"
            else:
                s += f"{'':<20}"
                nope += 1
            if nope == 3:
                s = ""
            # print(s)
            s = s.replace("o", "&#9744;")
            lines.append(s)

        return lines

    def pre_sim(self, combat, name="", occurrence=0, color=""):
        from main.models.contestants import Contestant
        all = Contestant.objects.filter(name=name, combat=combat)
        if len(all) == 0:
            a = Contestant()
        else:
            a = all.first()
        a.combat = combat

        a.collect_from_rid(self.rid, self.type, color=color)
        if len(name) > 0:
            a.name = name
        else:
            a.name = a.name + f"___{occurrence}"
        return a

    def roster_as_text(self):
        roster = "<br/>".join(self.roster())
        roster = roster.replace("§", " ").replace("<br/>", "\n").replace("<BR/>", "\n")
        return roster

    @classmethod
    def find_from_rid(cls, rid):
        from main.models.viaggiatori import Viaggiatore
        from main.models.nativi import Nativo
        from main.models.creature import Creatura
        viaggiatori = Viaggiatore.objects.filter(rid=rid)
        nativi = Nativo.objects.filter(rid=rid)
        creature = Creatura.objects.filter(rid=rid)
        item = None
        if len(viaggiatori) == 1:
            item = viaggiatori.first()
        elif len(nativi) == 1:
            item = nativi.first()
        elif len(creature) == 1:
            item = creature.first()
        return item

    def challenge_equipment_and_skills(self):
        pass
        # weapons = self.gear_to_weapons()
        # bugs = []
        # for weapon in weapons:
        #     if self.value_for(weapon['skill']) == 0:
        #         bugs.append(f"Arme trouvée pour laquelle le personnage n'a pas de compétence... {weapon['name']} {weapon['skill']}")
        # self.bug_list = "\n".join(bugs)

    def fix_protection_map(self):
        armors = self.gear_to_armors()
        self.malus_AGI = 0
        self.malus_DEX = 0
        self.malus_VUE = 0
        self.malus_OUI = 0
        map = {}
        self.protection_map = "H-0-X C-0-X A-0-X B-0-X L-0-X M-0-X"
        parts = self.protection_map.split(" ")
        for part in parts:
            x = part.split("-")
            map[x[0]] = {"Part": x[0], "Prot": 0, "Str": x[2]}
        for armor in armors:
            pro = armor["prot"]
            covers = armor["cover"].split(" ")
            for cover in covers:
                if cover in ["H"]:
                    p = "H"
                elif cover in ["C", "T"]:
                    p = "C"
                elif cover in ["AS", "SA", "A"]:
                    p = "A"
                elif cover in ["AW", "WA", "B"]:
                    p = "B"
                elif cover in ["SL", "LS", "L"]:
                    p = "L"
                elif cover in ["WL", "LW", "M"]:
                    p = "M"
                else:
                    p = ""
                if len(p) > 0:
                    map[p]["Prot"] += pro
            self.malus_AGI += armor["malus_AGI"]
            self.malus_DEX += armor["malus_DEX"]
            self.malus_VUE += armor["malus_VUE"]
            self.malus_OUI += armor["malus_OUI"]
        pmap = []
        for k, m in map.items():
            pmap.append(f'{m["Part"]}-{m["Prot"]}-{m["Str"]}')
        self.protection_map = " ".join(pmap)
