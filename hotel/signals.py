from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Hotel
from django.utils.text import slugify


@receiver(pre_save, sender=Hotel)
def hotel_slug(sender, instance=None, *args, **kwargs):
    instance.slug = slugify(f"{instance.location.country} {instance.location.city} {instance.name}")
