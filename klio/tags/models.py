from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
