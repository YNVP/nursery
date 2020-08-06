from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Nursery


@receiver(post_save, sender=User)
def create_nursery(sender, instance, created, **kwargs):
    if created:
        Nursery.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_nursery(sender, instance, **kwargs):
    instance.nursery.save()