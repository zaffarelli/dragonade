from django.contrib import admin

# Register your models here.
from main.models.nativi import Nativo, NativoAdmin
from main.models.creature import Creatura, CreaturaAdmin
from main.models.viaggiatori import Viaggiatore, ViaggiatoreAdmin
from main.models.contestants import ContestantAdmin, Contestant
from main.models.combats import CombatAdmin, Combat
from main.models.combat_rounds import CombatRound, CombatRoundAdmin
from main.models.sogni import Sogno, SognoAdmin
from main.models.equipment import Equipment, EquipmentAdmin
from main.models.incantessimi import Incantessimo, IncantessimoAdmin
from main.models.artefatti import Artefatto, ArtefattoAdmin
from main.models.teams import Team, TeamAdmin

admin.site.register(Nativo, NativoAdmin)
admin.site.register(Viaggiatore, ViaggiatoreAdmin)
admin.site.register(Creatura, CreaturaAdmin)
admin.site.register(Sogno, SognoAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Incantessimo, IncantessimoAdmin)
admin.site.register(Artefatto, ArtefattoAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Combat, CombatAdmin)
admin.site.register(CombatRound, CombatRoundAdmin)
