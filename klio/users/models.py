from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City, Country

from contacts.models import Phone


# https://habrahabr.ru/post/313764/
class User(AbstractUser):
    """Override build-in User model."""

    registered = models.DateTimeField(auto_now_add=True, verbose_name=_('registered'))
    username = models.CharField(max_length=64, unique=False, null=True, blank=True, default=None,
                                verbose_name=_('username'))
    first_name = models.CharField(max_length=64, null=True, blank=False, default=None, verbose_name=_('first name'))
    last_name = models.CharField(max_length=64, null=True, blank=False, default=None, verbose_name=_('last name'))
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None, verbose_name=_('middle name'))
    birthday = models.DateField(null=True, blank=True, default=None, verbose_name=_('birthday'))
    phones = models.ManyToManyField(Phone, through='UserPhone', related_name='users', verbose_name=_('phones'))
    email = models.EmailField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('country'))
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('city'))
    address = models.CharField(max_length=256, blank=True, verbose_name=_('address'))
    avatar = models.ImageField(blank=True, verbose_name=_('avatar'))
    personal_data = models.BooleanField(default=False, blank=False, verbose_name=_('personal data'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-is_active', 'last_name', 'username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.middle_name:
            return "{0} {1} {2}".format(self.last_name, self.first_name, self.middle_name)
        elif self.first_name and self.last_name:
            return "{0} {1}".format(self.last_name, self.first_name)
        elif self.username:
            return self.username
        else:
            return self.first_name


class UserPhone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, verbose_name=_('phone'))
    main = models.BooleanField(default=False, verbose_name=_('main'))
    order = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'user', 'phone']
        verbose_name = _('User Phone')
        verbose_name_plural = _('User Phones')
