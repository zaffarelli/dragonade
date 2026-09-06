from multiprocessing.util import abstract_sockets_supported

from django.db import models
from main.mixins.chiaroscuro_mixin import ChiaroscuroMixin
from main.models.oggetti import OggettoCategory
from main.utils.ref_dragonade import CHARACTER_STATISTICS, SHORTCUTS, stress_cost
from main.utils.mechanics import as_rid, Nougardine, roll, Severity, Chaser
from datetime import datetime
import math
import json


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
    entrance = models.TextField(max_length=1024, default="", blank=True)
    birthhour = models.IntegerField(default=0, blank=True)
    is_female = models.BooleanField(default=False, blank=True)
    is_lefty = models.BooleanField(default=False, blank=True)
    skills_creation_ok = models.BooleanField(default=False, blank=True)
    attributes_creation_ok = models.BooleanField(default=False, blank=True)
    is_battle_ready = models.BooleanField(default=False, blank=True)
    age = models.PositiveIntegerField(default=20, blank=True)
    height = models.PositiveIntegerField(default=150, blank=True)
    weight = models.PositiveIntegerField(default=0, blank=True)
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
    priority = models.IntegerField(default=0, blank=True)
    klass = models.CharField(max_length=16, default="Character", blank=True)
    protection_map = models.CharField(max_length=256, blank=True, default="H-0-X C-0-X A-0-X B-0-X L-0-X M-0-X")
    skills_map_str = models.TextField(max_length=2048, default="{}", blank=True)

    sogni = models.CharField(max_length=256, default="DEF", blank=True)

    travel_points = models.IntegerField(default=0, blank=True)
    stress_acquired = models.IntegerField(default=0, blank=True)
    stress_used = models.IntegerField(default=0, blank=True)
    stress_remaining = models.IntegerField(default=0, blank=True)

    malus_AGI = models.IntegerField(default=0, blank=True)
    malus_DEX = models.IntegerField(default=0, blank=True)
    malus_VUE = models.IntegerField(default=0, blank=True)
    malus_OUI = models.IntegerField(default=0, blank=True)

    description = models.TextField(max_length=1024, default="", blank=True)
    bugs = []

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
        # self.export_to_json()
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
        result = self.overwrite_for(att, val)
        if result:
            self.save()
        return result

    def has_bug(self):
        return len(self.bugs) > 0

    has_bug.boolean = True

    def fix(self):
        self.bugs = []
        self.chiaroscuro()
        # initializers
        if len(self.protection_map) == 0:
            self.protection_map = "H-0-X C-0-X AS-0-X AW-0-X LS-0-X LW-0-X"
        if self.birthhour == 0:
            self.birthhour = roll(faces=12, explodes=False)
        self.initialize()
        self.make_rid()
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
        # self.tai_guideline = tai_guidelines(self.value_for('TAI'))
        self.compute_weight()

        #
        # if self.height > 0:
        #     self.imc = math.floor(self.weight / ((self.height / 100) ** 2) * 10) / 10
        self.fix_protection_map()
        self.calc_indice()
        self.challenge_equipment()
        self.challenge_skills()
        self.bug_list = "§".join(self.bugs)
        # print(self.bug_list)
        # self.export_to_json()

    def compute_weight(self):
        """
            IMC = 15 -> 35
            IMC = 10 + 2 * TAI + 1xCON + 1xFOR
        """
        if self.height <= 0:
            self.height = 170
        height = self.height / 100
        IMC = 15 + int(self.value_for("CON")) + int(self.value_for("FOR")) - int(self.value_for("AGI")) + int(self.value_for("AGI"))
        weight = IMC * height ** 2
        self.imc = IMC
        self.weight = round(weight)

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
        self.total_attributes = 0
        for a in self.attributes.split(" "):
            self.total_attributes += int(a) + 5
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
        self.REV = int(self.SON) + int(self.FAB)
        a, s = self.expected_totals()
        self.total_attributes -= a
        self.total_skills -= s

    def ref_to_struct(self, src_ref):
        """        
            self.attributes -> self._data['attributes'], self.skills_generic -> self._data['skills']['generic']
            :param src_ref: source reference among the user filled properties o f the instance
            :returns: nothing / works directly on the instance
        """
        j = json.loads(self.skills_map_str)
        if "all" in j:
            cvs = j["all"]
        else:
            cvs = {}
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

                        self._data[branch][transversal[1].lower()][item['NAME']] = {"val": 666, "abs": 666, "cv": ""}
                        self._data[branch][transversal[1].lower()][item['NAME']]['val'] = int(arr[cnt]) if cnt < len(arr) else src_struct['DEFAULT']
                        self._data[branch][transversal[1].lower()][item['NAME']]['abs'] = self._data[branch][transversal[1].lower()][item['NAME']]['val'] - \
                                                                                          src_struct['DEFAULT']
                        if item['NAME'] in cvs:
                            self._data[branch][transversal[1].lower()][item['NAME']]['cv'] = cvs[item['NAME']]
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
                self.bugs.append(f"{self.rid} doesn't have the correct property for [{skill_set}].")
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
        self._data['spells_details'] = self.collect_spells()
        self._data['shortcuts'] = self.shortcuts()
        self._data['weapons'] = self.gear_to_weapons()
        self._data['other'] = self.gear_to_other()
        self._data['armors'] = self.gear_to_armors()
        # self._data['GENDER'] = self.is_female
        # self._data['LEFTY'] = self.is_lefty

        self._data["skills_summary"] = self.skills_summary()
        self._data['roster_text'] = self.roster_as_text()
        now = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        self._data['last_update'] = now
        self._data['bug_list'] = self.bug_list

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
        # print("******* GEAR TO WEAPONS *******")
        """
            Grab elements from the gear stack list that are neither weapons.
            :returns: JSON list of the elements fetched.
        """
        from main.models.oggetti import Oggetto
        list = []
        # print(self.gear.split(" "))
        weapons = Oggetto.objects.filter(category__in=[OggettoCategory.MEL, OggettoCategory.TIR, OggettoCategory.LAN], rid__in=self.gear.split(" ")).order_by(
            "category")
        # print(len(weapons))
        for weapon in weapons:
            # print(weapon)
            svs = {"18": "MEL", "19": "TIR", "20": "LAN"}
            stat_value = self.value_for(svs[str(weapon.category)])
            related_skills = weapon.related_skill.split(" ")
            d = weapon.export_to_json()
            worst = 1000
            for related_skill in related_skills:
                val = self.value_for(related_skill)
                if int(val) < worst:
                    worst = int(val)
                    d['related_skill_value'] = int(val)
                    e,_ = self.entry_for(related_skill)
                    if e:
                        d['related_skill_text'] = e["TEXT"]
            # Data specific to the character applied to the wepon's data
            d['stat_value'] = stat_value
            d['stat_name'] = svs[str(weapon.category)]
            d['IMP'] = self.IMP
            d['base_score'] = int(stat_value) + int(d['related_skill_value'])
            d['stat_skill'] = f"{svs[str(weapon.category)]}+{d['related_skill_value']}={int(stat_value) + int(d['related_skill_value'])}"
            list.append(d)
            # print(d)
        return list

    def gear_to_other(self):
        """
            Grab elements from the gear stack list and get all of those that are neither armor or weapon.
            :returns: JSON list of the elements fetched.
        """
        from main.models.oggetti import Oggetto
        list = []
        others = Oggetto.objects.exclude(category__in=[OggettoCategory.MEL, OggettoCategory.TIR, OggettoCategory.LAN]).filter(
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
            list.append(incantessimo.export_to_json())
        # sorted_all = sorted(list, key=lambda k: k['diff'], reverse=False)
        return list

    def shortcuts(self):
        list = []
        # for sc in SHORTCUTS:
        #     attr = int(self.value_for(sc[1]))
        #     skill = int(self.value_for(sc[2]))
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
        result = None
        entry, statistic_property = self.entry_for(str)
        if entry:
            # print(f"### Values : {str} => {where}")
            if "ORDER" in entry:
                datalist = getattr(self, statistic_property)
                if type(datalist).__name__ == 'str':
                    parts = datalist.split(" ")
                    x = entry["ORDER"]
                    if x < len(parts):
                        result = parts[x]
                    else:
                        print(f"Data out of bounds for {statistic_property}")
                else:
                    result = datalist[entry["ORDER"]]
                # print(f"### Result = {result}")
            else:
                result = getattr(self, statistic_property)
        return result

    def overwrite_for(self, str, val):
        result = False
        entry,statistic_property = self.entry_for(str)
        print(f"Entry for [{str}] is {statistic_property}: {entry}")
        if entry:
            if "ORDER" in entry:
                datalist = getattr(self, statistic_property)
                parts = datalist.split(" ")
                parts[entry["ORDER"]] = f"{val}"
                setattr(self, statistic_property, " ".join(parts))
                self.save()
                result = True
            else:
                setattr(self, statistic_property, val)
                self.save()
                result = True
        return result

    def entry_for(self, stat):
        """
            :param stat: the value that entry must match with property NAME
            :returns: the full entry, or {}
        """
        from main.utils.ref_dragonade import CHARACTER_STATISTICS
        found = None
        statistic_property = None
        root = CHARACTER_STATISTICS
        for bname, branch in root.items():
            if "LIST" in branch:
                for item in branch["LIST"]:
                    if item["NAME"] == stat:
                        if "ORDER" in item:
                            statistic_property = f"{bname.lower()}"
                        else:
                            statistic_property = f"{item['NAME']}"
                        found = item
                        break
            else:
                for sbname, subbranch in branch.items():
                    if "LIST" in subbranch:
                        for item in subbranch["LIST"]:
                            # print(f'Searching... {stat}')
                            if item["NAME"] == stat:
                                # print(f'Found {item["NAME"]} for {stat}')
                                found = item
                                if "ORDER" in item:
                                    statistic_property = f"{bname.lower()}_{sbname.lower()}"
                                else:
                                    statistic_property = f"{item['NAME'].lower()}"
                                break
            if found:
                break


        # result = {}
        # # print(f"ENTRY FOR {str} {stat}")
        # if len(str) > 0:
        #     words = str.upper().split(':')
        #     for word in words:
        #         root = root[word]
        #     if "LIST" in root:
        #         for item in root["LIST"]:
        #             if item["NAME"] == stat.upper():
        #                 result = item
        #                 break
        #     else:
        #         print(f"We might be lost in `entry_for` str=[{str}] stat=[{stat}]: [{root}]")
        return found, statistic_property

    # def index_for(self, str):
    #     """
    #     :param str: The code for the stat
    #     :returns: the position in the description as a:b:c
    #     """
    #     result = None
    #     print("INDEX FOR",str)
    #     from main.utils.ref_dragonade import known
    #     choices = ["ATTRIBUTES", "SKILLS:WEAPONS", "SKILLS:GENERIC", "SKILLS:PECULIAR", "SKILLS:SPECIALIZED", "SKILLS:KNOWLEDGE", "SKILLS:DRACONIC",
    #                "SECONDARIES", "MISC", "FEATURES"]
    #     for choice in choices:
    #         root = CHARACTER_STATISTICS[choice]
    #         # result = known(choice, str)
    #         for item in root["LIST"]:
    #             if item["NAME"] == str:
    #                 result = item
    #                 break
    #     return result

    def roster(self):
        """
            Build exportable roster for the character.
            HTML compatible.
        """
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
            ty = "Nativo"
        if self.type == "Creatura":
            subty = (f" ({self.get_creature_type_display()})")
            ty += subty

        lines.append(f"{ty}")
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

    def challenge_equipment(self):
        weapons = self.gear_to_weapons()
        for weapon in weapons:
            x = int(self.value_for(weapon['related_skill']))
            if x == -1:
                print(f"*** {weapon['related_skill']} {x}")
                self.bugs.append(f"(??) Pas de compétence avec {weapon['name']} ({weapon['related_skill']})§")

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

    def randomize(self):
        pass

    def challenge_skills(self):
        """
            Checks for the amount of by default skills against skills enhanced with stress
        """

        def track_perfect(root):
            """
                From a root in CHARACTER_STATISTICS:
                    - Tracks the exact values that should be given at character creation.
                    - Tracks if those values are matching the spots from character creation.
                    - This gives map on how the character was first created.
            """
            default = -root["DEFAULT"]
            for stat in root["LIST"]:
                tgt = stat["NAME"]
                val = self.value_for(tgt)
                if val in skills_map["values"]:
                    for k, v in skills_map["values"].items():
                        if int(k) == int(val):
                            nice_value = ""
                            nice_spot = ""
                            arrv = v["perfect_matches"]
                            sizev = len(arrv)
                            if v["count"] > sizev and tgt not in v["perfect_matches"]:
                                nice_value = k
                            for l, w in skills_map["spots"].items():
                                if l == str(default):
                                    # print("-----------------",l, w['count'])
                                    arrs = w["perfect_matches"]
                                    sizes = len(arrs)
                                    if w["count"] > sizes and tgt not in w["perfect_matches"]:
                                        nice_spot = l
                                        break
                            if len(nice_value) > 0 and len(nice_spot) > 0:
                                skills_map["values"][nice_value]["perfect_matches"].append(tgt)
                                skills_map["spots"][nice_spot]["perfect_matches"].append(tgt)
                                skills_map["all"][tgt] = nice_value

        def track_enhanced(root):
            """
                From a root in CHARACTER_STATISTICS:
                    - Tracks the scores that are greater than expected than the values that should be given at character creation.
                    - Tracks if those scores are matching the spots from character creation.
                    - This completes the full map of skills affectation at creation.
            """
            default = -root["DEFAULT"]
            for stat in root["LIST"]:
                tgt = stat["NAME"]
                val = self.value_for(tgt)
                if int(val) > 0:
                    for k, v in skills_map["values"].items():
                        if int(k) < int(val):
                            nice_value = ""
                            nice_spot = ""
                            perfect_values = v["perfect_matches"]
                            enhanced_values = v["partial_matches"]
                            spv = len(perfect_values)
                            sev = len(enhanced_values)
                            if (v["count"] > spv + sev) and tgt not in v["perfect_matches"] and tgt not in v["partial_matches"]:
                                nice_value = k
                            for l, w in skills_map["spots"].items():
                                if l == str(default):
                                    # print("-----------------",l, w['count'])
                                    perfect_spots = w["perfect_matches"]
                                    enhanced_spots = w["partial_matches"]
                                    sps = len(perfect_spots)
                                    ses = len(enhanced_spots)
                                    if (w["count"] > sps + ses) and tgt not in w["perfect_matches"] and tgt not in w["partial_matches"]:
                                        # if tgt not in w["perfect_matches"] and tgt not in w["partial_matches"]:
                                        nice_spot = l
                                        break
                            if len(nice_value) > 0 and len(nice_spot) > 0:
                                skills_map["values"][nice_value]["partial_matches"].append(tgt)
                                skills_map["spots"][nice_spot]["partial_matches"].append(tgt)
                                skills_map["all"][tgt] = nice_value

        def compute_stress(root):
            stress = 0
            default = root["DEFAULT"]
            for stat in root["LIST"]:
                tgt = stat["NAME"]
                val = int(self.value_for(tgt))
                forget = True
                if val > default:
                    forget = False
                    start_value = default
                    s = 0
                    for l, w in skills_map["values"].items():
                        # If target in perfect match: nothing to do
                        if tgt in w["partial_matches"]:
                            start_value = int(l)
                            # print(start_value)
                        if tgt in w["perfect_matches"]:
                            forget = True
                    if not forget:
                        x = ""
                        abss = start_value - default
                        absv = val - default
                        while abss < absv:
                            abss += 1
                            s = abss
                            x += f"{s:2}"
                            x += f"({abss + default:2}) "
                            stress += s
                        # print(f"{tgt:8} Compute from {start_value} to {val - default} >>> {s:3} stress [{x:50}]")

                else:
                    # if value is default: nothing to do
                    pass
            return stress

        if self.type != "Viaggiatore":
            pass
        else:
            skills_map = {
                "name": self.name,
                "all": {},
                "spots": {
                    "5": {
                        "count": 1,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "4": {
                        "count": 3,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "3": {
                        "count": 6,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "2": {
                        "count": 8,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "1": {
                        "count": 10,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                },
                "values": {
                    "7": {
                        "count": 1,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "6": {
                        "count": 2,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "5": {
                        "count": 3,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "4": {
                        "count": 4,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "3": {
                        "count": 5,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "2": {
                        "count": 6,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                    "1": {
                        "count": 7,
                        "perfect_matches": [],
                        "partial_matches": []
                    },
                }
            }
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["DRACONIC"])
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["KNOWLEDGE"])
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["SPECIALIZED"])
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["PECULIAR"])
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["GENERIC"])
            track_perfect(CHARACTER_STATISTICS["SKILLS"]["WEAPONS"])

            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["WEAPONS"])
            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["GENERIC"])
            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["PECULIAR"])
            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["SPECIALIZED"])
            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["KNOWLEDGE"])
            track_enhanced(CHARACTER_STATISTICS["SKILLS"]["DRACONIC"])

            # Control
            spots_ok = True
            for k, v in skills_map["spots"].items():
                e = v["perfect_matches"]
                a = v["partial_matches"]
                se = len(e)
                sa = len(a)
                if v["count"] != se + sa:
                    spots_ok = False
                    break
            values_ok = True
            for k, v in skills_map["values"].items():
                e = v["perfect_matches"]
                a = v["partial_matches"]
                se = len(e)
                sa = len(a)
                if v["count"] != se + sa:
                    values_ok = False
                    break
            if spots_ok and values_ok:
                self.bugs.append("(---) Skills control ok.")
                self.skills_creation_ok = True
            else:
                self.bugs.append("(???) Missing skills control")
                self.skills_creation_ok = False

            self.skills_map_str = json.dumps(skills_map)

            # Computing Stress
            self.stress_used = 0
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["DRACONIC"])
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["KNOWLEDGE"])
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["SPECIALIZED"])
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["PECULIAR"])
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["GENERIC"])
            self.stress_used += compute_stress(CHARACTER_STATISTICS["SKILLS"]["WEAPONS"])
            skill_stress = self.stress_used
            # Check Attributes
            starting_values = [8, 7, 7, 6, 6, 5, 5, 5, 5, 4, 4, 4]
            arr = self.attributes.split(" ")
            current_attributes = [int(v) for v in arr]
            idx = 0
            while idx < 12:
                if starting_values[idx] in current_attributes:
                    current_attributes.remove(starting_values[idx])
                    starting_values[idx] = -1
                idx += 1
            starting_values = [a for a in starting_values if a != -1]
            starting_values.sort(reverse=True)
            current_attributes.sort(reverse=True)
            idx = 0
            attr_ok = True
            while idx < len(current_attributes):
                if current_attributes[idx] <= starting_values[idx]:
                    attr_ok = False
                idx += 1
            if attr_ok:
                self.bugs.append("(---) Attributes control ok.")
                self.attributes_creation_ok = True
            else:
                self.bugs.append("(???) Attributes Error")
                self.attributes_creation_ok = False

            # print(current_attributes, starting_values)
            attr_stress = 0
            # Attr higher than expected
            while len(current_attributes) > 0:
                ca = current_attributes[0]
                bsv = starting_values[0]
                sv = bsv
                while sv < ca:
                    attr_stress += sv + 6  # -(-5) +1
                    sv += 1
                current_attributes.remove(ca)
                starting_values.remove(bsv)
            self.stress_used += attr_stress
            # print(current_attributes, starting_values, skill_stress, attr_stress)
            self.stress_remaining = self.stress_acquired - self.stress_used
