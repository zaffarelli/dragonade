from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.creatures import Creature


@receiver(pre_save, sender=Creature, dispatch_uid='pre_save_creature')
def pre_save_creature(sender, instance, **kwargs):
    instance.fix()
