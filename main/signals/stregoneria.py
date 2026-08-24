from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.incantessimi import Incantessimo


@receiver(pre_save, sender=Incantessimo, dispatch_uid='pre_save_spell')
def pre_save_spell(sender, instance, **kwargs):
    instance.fix()
