from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.contestants import Contestant


@receiver(pre_save, sender=Contestant, dispatch_uid='pre_save_contestant')
def pre_save_contestant(sender, instance, **kwargs):
    instance.fix()
