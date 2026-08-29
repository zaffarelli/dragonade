from django.db.models.signals import pre_save #, post_save
from django.dispatch import receiver
from main.models.incantessimi import Incantessimo


@receiver(pre_save, sender=Incantessimo, dispatch_uid='pre_save_incantessimo')
def pre_save_incantessimo(sender, instance, **kwargs):
    instance.fix()

# @receiver(post_save, sender=Incantessimo, dispatch_uid='post_save_incantessimo')
# def post_save_incantessimo(sender, instance, **kwargs):
#     instance.model_to_data()
