from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.equipment import Equipment


@receiver(pre_save, sender=Equipment, dispatch_uid='pre_save_equipment')
def pre_save_equipment(sender, instance, **kwargs):
    instance.fix()
