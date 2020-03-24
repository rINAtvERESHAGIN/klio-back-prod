from django.db import models

from cities_light.models import City, Country
from ckeditor.fields import RichTextField


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(blank=True)
    phones = models.ManyToManyField('Phone', through='ContactPhone', related_name='contacts')
    map = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(blank=False, default=1)
    content = RichTextField(blank=True)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'order', 'name']

    def __str__(self):
        return self.name


class ContactPhone(models.Model):
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(blank=False, default=1)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'main', 'order']


class Phone(models.Model):
    MOBILE, HOME, WORK = 'mobile', 'home', 'work'
    LABEL_CHOICES = [
        (MOBILE, 'Mobile phone'),
        (HOME, 'Home phone'),
        (WORK, 'Work phone'),
    ]

    phone = models.CharField(max_length=20, blank=False, null=False, default=None,
                             help_text='Enter the phone in the format +7(XXX)XXX-XX-XX')
    label = models.CharField(max_length=64, choices=LABEL_CHOICES, blank=True, default=None)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'phone']

    def __str__(self):
        return "{0} ({1})".format(self.phone, self.label)


class SocialNet(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    img = models.FileField(blank=False, upload_to='socials/')
    url = models.URLField(blank=False)
    order = models.PositiveSmallIntegerField(blank=False, default=1)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'order', 'name']

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    label = models.CharField(max_length=32, blank=False, null=False)
    time = models.CharField(max_length=32, blank=False, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='hours')
