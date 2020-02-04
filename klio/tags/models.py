from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['activity', 'name']
