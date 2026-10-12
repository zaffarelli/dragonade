from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.universes import Universe


@receiver(pre_save, sender=Universe, dispatch_uid='pre_save_universe')
def pre_save_universe(sender, instance, **kwargs):
    instance.fix()
