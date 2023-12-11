from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.dreams import Dream


@receiver(pre_save, sender=Dream, dispatch_uid='pre_save_dream')
def pre_save_dream(sender, instance, **kwargs):
    instance.fix()
