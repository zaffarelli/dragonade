from django.contrib import admin

# Register your models here.
from main.models import Autochton, AutochtonAdmin, Traveller, TravellerAdmin


admin.site.register(Autochton, AutochtonAdmin)
admin.site.register(Traveller, TravellerAdmin)


