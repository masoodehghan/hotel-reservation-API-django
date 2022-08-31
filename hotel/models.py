from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.urls import reverse
import uuid


class Location(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)


class Hotel(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    description = models.TextField(default='')
    host = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, related_name='hotels'
    )
    gallery = GenericRelation('Gallery')
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel_detail', args=[self.pk])


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel, null=True, blank=True, on_delete=models.CASCADE, related_name='rooms'
    )
    room_type = models.CharField(default='', max_length=20)
    number_of_rooms = models.PositiveSmallIntegerField()
    number_of_adult_beds = models.PositiveSmallIntegerField()
    number_of_child_beds = models.PositiveSmallIntegerField()
    floor = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    gallery = GenericRelation('Gallery')
    uuid = models.UUIDField(default=uuid.uuid4)

    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], null=True, blank=True
    )

    description = models.TextField(default='')

    def get_absolute_url(self):
        return reverse('room_detail', args=[self.uuid])


def photo_path(instance, filename):

    if isinstance(instance.content_object, Room):
        folder_name = str(instance.content_object.id)

    else:
        folder_name = f"{instance.content_object.name}_{instance.content_object.id}"

    return f"gallery/{folder_name}/{filename}"


class Gallery(models.Model):
    """gallery can have relation with Room or Hotel"""
    image = models.ImageField(upload_to=photo_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{str(self.image)}"

    class Meta:
        indexes = [
            models.Index(fields=['object_id', 'content_type'])
        ]
