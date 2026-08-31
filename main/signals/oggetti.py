from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.oggetti import Oggetto


@receiver(pre_save, sender=Oggetto, dispatch_uid='pre_save_equipment')
def pre_save_equipment(sender, instance, **kwargs):
    instance.fix()
