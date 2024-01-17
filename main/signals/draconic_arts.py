from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.draconic_arts import Spell


@receiver(pre_save, sender=Spell, dispatch_uid='pre_save_spell')
def pre_save_spell(sender, instance, **kwargs):
    instance.fix()
