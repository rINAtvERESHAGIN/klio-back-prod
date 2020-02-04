from django.db import models

from cities_light.models import City, Country
from ckeditor.fields import RichTextField


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField()
    phones = models.ManyToManyField('Phone', through='ContactPhone')
    map = models.URLField(blank=True)
    content = RichTextField(blank=True)

    def __str__(self):
        return self.name


class SocialNet(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name


class ContactPhone(models.Model):
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(blank=False, default=1)
    activity = models.BooleanField(default=True)


class Phone(models.Model):
    phone = models.CharField(max_length=20, blank=False, null=False, default=None,
                             help_text='Enter the phone in the format +7(XXX)XXX-XX-XX')
    label = models.CharField(max_length=64, blank=True, null=False, default=None)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return "{0} ({1})".format(self.phone, self.label)
