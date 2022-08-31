from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Hotel, Reservation
from django.utils.text import slugify


@receiver(pre_save, sender=Hotel)
def hotel_slug(sender, instance=None, *args, **kwargs):
    instance.slug = slugify(f"{instance.location.country} {instance.location.city} {instance.name}")


@receiver(pre_save, sender=Reservation)
def reservation_total_price(sender, instance: Reservation | None = None, **kwargs):
    total_price = instance.room.price * (instance.end_date - instance.start_date).days
    discount_price = (total_price * instance.room.discount_percent) / 100
    instance.total_price = total_price - discount_price
