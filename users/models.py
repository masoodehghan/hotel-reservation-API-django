from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.urls import reverse


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        HOST = 'h'
        GUEST = 'g'
        ADMIN = 'a'

    base_role = Roles.ADMIN
    role = models.CharField(max_length=1, choices=Roles.choices, default=base_role)
    uuid = models.UUIDField(default=uuid.uuid4)


from hotel.api.v1.models import Hotel


class Review(models.Model):
    class VoteTypes(models.TextChoices):
        UP = 'u'
        DOWN = 'd'
        NOT_SURE = 'n'

    value = models.CharField(max_length=1, choices=VoteTypes.choices)
    body = models.CharField(max_length=200, default='')
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE
    )
    pros = models.CharField(max_length=100, default='')
    cons = models.CharField(max_length=100, default='')

    class Meta:
        unique_together = [['user_id', 'hotel_id']]

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.pk])
