from django.db import models
from django.contrib.auth.models import AbstractUser

from cities_light.models import City, Country

from contacts.models import Phone


# https://habrahabr.ru/post/313764/
class User(AbstractUser):
    """Override build-in User model."""

    registered = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    last_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None)
    birthday = models.DateField(null=True, blank=True, default=None)
    phones = models.ManyToManyField(Phone, through='UserPhone', related_name='users')
    email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True)
    address = models.CharField(max_length=256, blank=True)
    avatar = models.ImageField(blank=True)
    activity = models.BooleanField(default=True)
    personal_data = models.BooleanField(default=False, blank=False)

    def __str__(self):
        if self.first_name:
            return "{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)
        else:
            return self.username

    class Meta:
        ordering = ['-activity', 'last_name', 'username']


class UserPhone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(blank=False, default=1)
    activity = models.BooleanField(default=True)
