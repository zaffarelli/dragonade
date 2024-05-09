from main.utils.combat_simulator import CombatSimulator
import os


class CombatSim:
    # exec(open('./scripts/combatsim.py').read())
    # MEM_DE_LA_FRA_023
    # BJA_VAR_013

    def __init__(self):

        self.sim = CombatSimulator()
        self.filename = "default.smd.txt"
        self.blue = ""
        self.red = ""

        print(self.fmt('> µ*** Simulateur de Mêlée de Dragonade ***§'))
        print(f"    1 - Ajoût à l'équipe bleue")
        print(f"    2 - Ajoût à l'équipe rouge")
        print(f"    3 - Vérification générale")
        print(f"    4 - Démarrage du combat")
        print(f"    5 - Fichier de postérité [{self.filename}]")
        print(f"    0 - Quitter")
        topic = ''
        while topic != '0':
            topic = input("> Votre choix [0] ? ")
            if topic == '1':
                self.blue_team()
            elif topic == '2':
                self.red_team()
            elif topic == '3':
                self.check_all()
            elif topic == '4':
                self.go()
            elif topic == '5':
                self.change_file()

    def fmt(self, txt):
        new_txt = "\033[97;40m".join(txt.split('µ'))
        new_txt = "\033[1;34m".join(new_txt.split('%'))
        new_txt = "\033[1;31m".join(new_txt.split('£'))
        new_txt = "\033[1;97m".join(new_txt.split('§'))

        new_txt = "\033[93;45m".join(new_txt.split('$'))
        new_txt = "\033[93;46m".join(new_txt.split('€'))




        return new_txt

    def blue_team(self):
        arid = input('  Equipe Bleue: Nouveau membre [RID|fin] ? ')
        if arid != 'fin':
            if arid == "":
                arid = "BJA_VAR_013"
            r = self.sim.add_combattant(arid,True)
            print(self.fmt(r))

    def red_team(self):
        arid = input('  Equipe Rouge: Nouveau membre [RID|fin] ? ')
        if arid != 'fin':
            if arid == "":
                arid = "MEM_DE_LA_FRA_023"
            r = self.sim.add_combattant(arid,False)
            print(self.fmt(r))

    def check_all(self):
        results = self.sim.check_all()
        for result in results:
            print(self.fmt(result))

    def go(self):
        if self.sim.combat_can_start:
            while self.sim.perform() and len(self.sim.rounds)<10:
                for r in self.sim.comments:
                    print(self.fmt(r))


os.system('clear')
CombatSim()
