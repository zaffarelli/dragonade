from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models import Autochton, Traveller


@receiver(pre_save, sender=Autochton, dispatch_uid='pre_save_autochton')
def pre_save_autochton(sender, instance, **kwargs):
    instance.fix()


@receiver(pre_save, sender=Traveller, dispatch_uid='pre_save_traveller')
def pre_save_traveller(sender, instance, **kwargs):
    instance.fix()
