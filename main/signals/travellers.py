from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.travellers import Traveller


@receiver(pre_save, sender=Traveller, dispatch_uid='pre_save_traveller')
def pre_save_traveller(sender, instance, **kwargs):
    instance.fix()
