from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.models.sogni import Sogno


@receiver(pre_save, sender=Sogno, dispatch_uid='pre_save_dream')
def pre_save_dream(sender, instance, **kwargs):
    instance.fix()
