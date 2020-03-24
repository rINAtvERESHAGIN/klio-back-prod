from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Special(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, 'Percentage discount'),
        (FIXED, 'Fixed discount'),
    ]

    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField(max_length=128, blank=False)
    img = models.ImageField(blank=True)
    content = models.TextField(blank=True)
    discount = models.BooleanField(default=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=PERCENT, max_length=10, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # total_price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField(blank=False, default=timezone.now)
    deadline = models.DateTimeField(blank=True, null=True)
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity']
        verbose_name = _('Special')
        verbose_name_plural = _('Specials')


# class SpecialCategory(models.Model):
#     PERCENT, FIXED = 'percent', 'fixed'
#     DISCOUNT_TYPES = [
#         (PERCENT, 'Percentage discount'),
#         (FIXED, 'Fixed discount'),
#     ]
#
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
#     special = models.ForeignKey('Special', on_delete=models.CASCADE, blank=False, null=False)
#     discount = models.BooleanField(default=False)
#     discount_type = models.CharField(choices=DISCOUNT_TYPES, max_length=10, blank=True)
#     discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#
#     class Meta:
#         verbose_name = _('Special Category')
#         verbose_name_plural = _('Special Categories')


class SpecialProduct(models.Model):
    special = models.ForeignKey('Special', on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='special_relations')
    on_main = models.BooleanField(default=False)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-on_main']
        unique_together = [('special', 'product'), ('product', 'on_main')]
        verbose_name = _('Special Product')
        verbose_name_plural = _('Special Products')
