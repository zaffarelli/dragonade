from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.poteri_speciali import PotereSpeciale


@receiver(pre_save, sender=PotereSpeciale, dispatch_uid='pre_save_potere')
def pre_save_potere(sender, instance, **kwargs):
    instance.fix()
