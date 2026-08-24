from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.creature import Creatura


@receiver(pre_save, sender=Creatura, dispatch_uid='pre_save_creature')
def pre_save_creature(sender, instance, **kwargs):
    instance.fix()
