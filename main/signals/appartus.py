from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.appartus import Appartus


@receiver(pre_save, sender=Appartus, dispatch_uid='pre_save_appartus')
def pre_save_appartus(sender, instance, **kwargs):
    instance.fix()
