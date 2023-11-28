from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.autochtons import Autochton


@receiver(pre_save, sender=Autochton, dispatch_uid='pre_save_autochton')
def pre_save_autochton(sender, instance, **kwargs):
    instance.fix()
