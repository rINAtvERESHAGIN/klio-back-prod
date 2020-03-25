from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Special(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, _('Percentage discount')),
        (FIXED, _('Fixed discount')),
    ]

    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=128, blank=False, verbose_name=_('slug'))
    img = models.ImageField(blank=True, verbose_name=_('image'))
    content = models.TextField(blank=True, verbose_name=_('content'))
    discount = models.BooleanField(default=True, verbose_name=_('discount'))
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=PERCENT, max_length=10, blank=True,
                                     verbose_name=_('discount type'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('discount amount'))
    # total_price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField(blank=False, default=timezone.now, verbose_name=_('start date'))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_('deadline'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

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
    special = models.ForeignKey('Special', on_delete=models.CASCADE, blank=False, null=False,
                                verbose_name=_('special'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False,
                                related_name='special_relations', verbose_name=_('product'))
    on_main = models.BooleanField(default=False, verbose_name=_('on main'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('discount amount'))

    class Meta:
        ordering = ['-on_main']
        unique_together = [('special', 'product'), ('product', 'on_main')]
        verbose_name = _('Special Product')
        verbose_name_plural = _('Special Products')
