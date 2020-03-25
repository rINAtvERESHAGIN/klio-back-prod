from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City, Country
from ckeditor.fields import RichTextField


class Contact(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_('country'))
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('city'))
    address = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('address'))
    email = models.EmailField(blank=True)
    phones = models.ManyToManyField('Phone', through='ContactPhone', related_name='contacts', verbose_name=_('phones'))
    map = models.URLField(blank=True, verbose_name=_('map'))
    order = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name=_('order'))
    content = RichTextField(blank=True, verbose_name=_('content'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order', 'name']
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.name


class ContactPhone(models.Model):
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('contact'))
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE, verbose_name=_('phone'))
    main = models.BooleanField(default=False, verbose_name=_('main'))
    order = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'main', 'order']
        verbose_name = _('Contact Phone')
        verbose_name_plural = _('Contact Phones')


class Phone(models.Model):
    MOBILE, HOME, WORK = 'mobile', 'home', 'work'
    LABEL_CHOICES = [
        (MOBILE, _('Mobile phone')),
        (HOME, _('Home phone')),
        (WORK, _('Work phone')),
    ]

    phone = models.CharField(max_length=20, blank=False, null=False, default=None, verbose_name=_('phone'),
                             help_text=_('Enter the phone in the format +7(XXX)XXX-XX-XX'))
    label = models.CharField(max_length=64, choices=LABEL_CHOICES, blank=True, default=None, verbose_name=_('label'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'phone']
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')

    def __str__(self):
        return "{0} ({1})".format(self.phone, self.label)


class SocialNet(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    img = models.FileField(blank=False, upload_to='socials/', verbose_name=_('image'))
    url = models.URLField(blank=False)
    order = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order', 'name']
        verbose_name = _('Social Net')
        verbose_name_plural = _('Social Nets')

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    label = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('label'))
    time = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('time'))
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='hours', verbose_name=_('contact'))
    order = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order', ]
        verbose_name = _('Working Hours')
        verbose_name_plural = _('Working Hours')
