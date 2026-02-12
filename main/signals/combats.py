from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.combats import Combat


@receiver(pre_save, sender=Combat, dispatch_uid='pre_save_combat')
def pre_save_combat(sender, instance, **kwargs):
    instance.fix()
