from django.contrib import admin

# Register your models here.
from main.models.autochtons import Autochton, AutochtonAdmin
from main.models.travellers import Traveller, TravellerAdmin


admin.site.register(Autochton, AutochtonAdmin)
admin.site.register(Traveller, TravellerAdmin)


