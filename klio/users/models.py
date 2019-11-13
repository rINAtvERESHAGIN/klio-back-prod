from django.db import models
from django.contrib.auth.models import AbstractUser


# https://habrahabr.ru/post/313764/
class User(AbstractUser):
    """Override build-in User model."""

    first_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    last_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None)
    birthday = models.DateField(null=True, blank=True, default=None)
    phone = models.CharField(max_length=64, null=True, blank=False, default=None)
