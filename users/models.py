from django.db import models
from django.contrib.auth.models import AbstractUser


class GuestManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.Roles.GUEST)


class HostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.Roles.HOST)


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        HOST = 'h'
        GUEST = 'g'
        ADMIN = 'a'

    base_role = Roles.ADMIN
    role = models.CharField(max_length=1, choices=Roles.choices, default=base_role)


class Guest(CustomUser):

    base_role = super().Roles.GUEST
    objects = GuestManager()

    class Meta:
        proxy = True


class Host(CustomUser):

    base_role = super().Roles.HOST
    objects = HostManager()

    class Meta:
        proxy = True
