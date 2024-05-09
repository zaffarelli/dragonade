from main.models.characters import Character
import random
import math


class Combattant:
    def __init__(self):
        self.source_char = None
        self.is_battle_ready = False
        self.current_fatigue = 0
        self.current_hp = 0
        self.hp = 0
        self.fatigue = 0
        self.dom = 0
        self.sco = 0
        self.melee = 0
        self.derobade = 0
        self.constitution = 0
        self.volonte = 0
        self.esquive = 0
        self.name = ""
        self.is_blue_team = True
        self.firsthand = {}
        self.secondhand = {}
        self.used_name = ""
        self.targets = []
        self.outnumbered_mod = 0


    @property

    def improvised_name(self):
        syls = ["eg","on","cha","tre","va","lu","ac","ri","al","lu","ze","in","ga","be","lan","te","dem","cle","or","el", "fau", "mas", "and", "ro", "vi", "que","es","ont","ef"]
        random.shuffle(syls)
        str = "".join(syls[:3]).title()
        print("improvised_name",str)
        return str

    @property
    def nameless(self):
        from main.models.autochtons import Autochton
        value = False
        print(isinstance(self.source_char,Autochton))
        if isinstance(self.source_char,Autochton) == True:
            value = self.source_char.nameless
        print("nameless",value)
        return value

    @property
    def d12(self):
        val = 0
        details = "d12:"
        x = random.randint(1, 12)
        val += x
        details += f"<{x}>"
        if x == 1:
            x = random.randint(1, 12)
            val -= x
            details += f"<{x}>"
            while x == 12:
                x = random.randint(1, 12)
                val -= x
                details += f"<{x}>"
        if x == 12:
            x = random.randint(1, 12)
            val += x
            details += f"<{x}>"
            while x == 12:
                x = random.randint(1, 12)
                val += x
                details += f"<{x}>"
        return val, details

    def roll_diff(self, diff=15, base=0):
        result = ""

        roll, details = self.d12
        val = base + roll
        if val >= diff * 4:
            result += "€Critique!µ"
        elif val >= diff * 3:
            result += "€Significative!µ"
        elif val >= diff * 2:
            result += "€Particulière!µ"
        elif val >= diff:
            result += "€Réussite!µ"
        elif val > math.floor(diff / 2):
            result += "$Echec!µ"
        elif val > 0:
            result += "$Notable!µ"
        else:
            result += "$Total!µ"
        result += f"{base}+{roll}=({details}){val}"
        return result,val



    def life(self):
        result = "("
        x = 0
        while x < self.hp:
            if self.current_hp > x:
                result += "⬛"
            else:
                result += "⬜"
            x += 1
            if x % 5 == 0:
                result += " "
        result += ")"
        return result

    def initialize(self, chr_rid, blue=True):
        infos = []
        from main.models.autochtons import Autochton
        from main.models.travellers import Traveller
        matching_auto = Autochton.objects.filter(rid=chr_rid)
        if len(matching_auto) != 1:
            matching_trav = Traveller.objects.filter(rid=chr_rid)
            if len(matching_trav) != 1:
                infos.append(f"Error character {chr_rid} not found!")
            else:
                self.source_char = matching_trav.first()
        else:
            self.source_char = matching_auto.first()
        if self.source_char:
            if self.nameless:
                self.used_name = self.improvised_name + " ("+self.source_char.name+")"
            else:
                self.used_name = self.source_char.name.split(" ")[0]
            self.is_blue_team = blue
            self.source_char.toJson()
            self.hp = self.source_char.value_for("VIE")
            self.fatigue = self.source_char.value_for("FAT")
            self.dom = self.source_char.value_for("DOM")
            self.sco = self.source_char.value_for("SCO")
            self.melee = self.source_char.value_for("MEL")
            self.derobade = self.source_char.value_for("DER")
            self.constitution = self.source_char.value_for("CON")
            self.volonte = self.source_char.value_for("VOL")
            self.esquive = self.source_char.value_for("WEA_12")
            self.name = self.source_char.name
            self.weapons = self.source_char.gear_to_weapons()
            highest = 0
            self.fhskill = 0
            self.shskill = 0
            for w in self.weapons:
                if w['category'] == 'mel':
                    if w["score"] > highest:
                        highest = w["score"]
                        self.firsthand = w
                        self.fhskill = self.source_char.value_for(self.firsthand['skill'])
            if self.firsthand["dom_2"] == '-':
                if w['category'] == 'mel':
                    for w in self.weapons:
                        if "bouclier" in w["name"].lower():
                            self.secondhand = w
                            self.shskill = self.source_char.value_for(self.secondhand['skill'])
        return infos

    def combatclass(self):
        x = self.source_char.value_for(self.firsthand['skill'])
        if x >= 25:
            result = "SS; oui, ça existe"
        elif x >= 20:
            result = "S; autant dire qu'il est pas venu pour la déco"
        elif x >= 15:
            result = "A; en gros, faut pas le chercher"
        elif x >= 10:
            result = "B; un niveau très correct"
        elif x >= 5:
            result = "C; un niveau raisonable"
        else:
            result = "D; un combattant pas terrible"
        return result

    def roll_init(self):
        base = math.ceil(round(self.melee/2))+self.shskill
        roll,val = self.roll_diff(base=base)
        return val

    def describe(self):
        results = []
        results.append("")
        if self.is_blue_team:
            results.append(f"%{self.used_name}§ fait partie de l'équipe bleue.")
        else:
            results.append(f"£{self.used_name}§ fait partie de l'équipe rouge.")
        results.append(f"Il dispose de {self.hp} points de vie et de {self.fatigue} en fatigue.")
        results.append(f"Son bonus de domages est de {self.dom} et son seuil de constitution de {self.sco}.")
        more = ""
        if self.secondhand != {}:
            more =  f" et {self.secondhand['name']}"
        results.append(f"Sa compétence d'esquive est de {self.esquive} et il se bat avec {self.firsthand['name']}{more}.")
        results.append(f"Avec un score de {self.source_char.value_for(self.firsthand['skill'])} à son arme principale, c'est un combattant de classe {self.combatclass()}.")


        # {self.life()}

        # results.append(f"> µMEL§ {self.melee:02} µDER§ {self.derobade:02}")
        # results.append(f"> µCON§ {self.constitution:02} µVOL§ {self.volonte:02}")
        # results.append(f"> µ* Compétences *§")
        # results.append(
        #     f"> µ{self.firsthand['name']:20}§ ....... {self.source_char.value_for(self.firsthand['skill']):02}")
        # if self.secondhand != {}:
        #     results.append(f"> µ{self.secondhand['name']:20}§ ....... {self.shskill:02}")
        # results.append(f"> µ{'Esquive':20}§ ....... {self.esquive:02}")
        # results.append(f"> µMain+§ ......... {self.firsthand['name']}")
        # if self.secondhand != {}:
        #     results.append(f"> µMain-§ ......... {self.secondhand['name']}")
        # main_weapon = self.fhskill
        return results


class CombatRound:
    def __init__(self, num, parent):
        self.parent = parent
        self.number = num
        self.comments = [f'Début du round numéro {self.number:02}.']
        self.initiative_method = "normal"

    def phase1(self):
        # Intentions
        if len(self.parent.blues) == 1:
            red_outnumbered_mod = len(self.parent.reds)-1
            blue_outnumbered_mod = -red_outnumbered_mod
            b = self.parent.blues[0]
            b.outnumbered_mod = blue_outnumbered_mod
            for r in self.parent.reds:
                r.outnumbered_mod = red_outnumbered_mod
                b.targets.append(r)
                r.targets.append(b)

        str = b.used_name+" fera face à "
        sep = ", "
        for c in b.targets:
            if c == b.targets[len(b.targets)-2]:
                sep = " et "
            elif c == b.targets[len(b.targets) - 1]:
                sep = "."
            str += c.used_name + sep
        self.comments.append(str)


        # Initiative
        if self.number == 1:
            self.initiative_method = "by_weapon_class"
        # if self.initiative_method == "by_weapon_class":
        #     pass
        # else:
        #     pass
        self.initiatives = []
        for c in self.parent.combattants:

            if c.is_blue_team:
                equipe = "bleue"
            else:
                equipe = "rouge"
            init_value = c.roll_init()
            init_for_c = {"nom": c.used_name, "initiative": init_value, "équipe": equipe}
            self.initiatives.append(init_for_c)
        sorted_init = sorted(self.initiatives, key=lambda k: k['initiative'], reverse=True)
        str = ""
        for x in sorted_init:
            str += f"\n  {x['initiative']}: {x['nom']}"
        self.comments.append("L'ordre d'initiative sur ce round de combat sera "+str)
        self.parent.victory = True

    def phase2(self):
        # Magie & Haut-Rêve
        pass

    def phase3(self):
        # Tir
        pass

    def phase4(self):
        # Lancer
        pass

    def phase5(self):
        # Mêlée & Armes Naturelles
        pass

    def phase6(self):
        # Mouvement
        pass

    def phase7(self):
        # Santé & Vitalité
        pass

    def perform(self):
        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()
        self.phase5()
        self.phase6()
        self.phase7()

class CombatSimulator:
    def __init__(self):
        self.rounds = []
        self.comments = []
        self.combattants = []
        self.blues = []
        self.reds = []
        self.combat_can_start = False
        self.victory = None

    def add_combattant(self, character, blue):
        result = ""
        boosted = False
        # Maker unique
        cnt = 1
        while cnt > 0:
            x = Combattant()
            x.initialize(character, blue)
            #print(">>",x.used_name)
            if x.nameless and not boosted:
                boosted = True
                #print("Nameless, adding more !!")
                cnt += random.randint(1,3)


            if blue:
                self.blues.append(x)
            else:
                self.reds.append(x)
            self.combattants.append(x)
            cnt -= 1
        if len(self.combattants) > 0:
            result += "Liste des Combattants..."
            if len(self.reds):
                result += f"\n> Equipe Bleue: "
            for b in self.blues:
                result += f'\n - %{b.used_name}§'
            if len(self.reds):
                result += f"\n> Equipe Rouge: "
            for r in self.reds:
                result += f'\n - £{r.used_name}§'
        if len(self.blues) == 0 or len(self.reds) == 0:
            result += "\n> µErreur:§ Distribution incomplète."
        else:
            self.combat_can_start = True
        result += "\n"

        return result

    def check_all(self):
        results = []
        for b in self.blues:
            results += b.describe()
        for r in self.reds:
            results += r.describe()
        return results

    # def self

    def perform(self):
        is_not_over = self.victory is None
        rnd = CombatRound(len(self.rounds) + 1, self)
        self.rounds.append(rnd)
        rnd.perform()
        self.comments = rnd.comments
        return is_not_over

    # def weapon_class_initiative(self):
    #     pass
    #
    # def standard_initiative(self):
    #     antagonists = []
    #     return antagonists
