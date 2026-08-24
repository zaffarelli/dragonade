from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.nativi import Nativo


@receiver(pre_save, sender=Nativo, dispatch_uid='pre_save_autochton')
def pre_save_autochton(sender, instance, **kwargs):
    instance.fix()
