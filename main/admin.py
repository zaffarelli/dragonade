from django.contrib import admin

# Register your models here.
from main.models.autochtons import Autochton, AutochtonAdmin
from main.models.travellers import Traveller, TravellerAdmin
from main.models.dreams import Dream, DreamAdmin
from main.models.equipment import Equipment, EquipmentAdmin


admin.site.register(Autochton, AutochtonAdmin)
admin.site.register(Traveller, TravellerAdmin)
admin.site.register(Dream, DreamAdmin)
admin.site.register(Equipment, EquipmentAdmin)


