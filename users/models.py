from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        HOST = 'h'
        GUEST = 'g'
        ADMIN = 'a'

    base_role = Roles.ADMIN
    role = models.CharField(max_length=1, choices=Roles.choices, default=base_role)
