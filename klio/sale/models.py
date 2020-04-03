from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from products.models import Product
from tags.models import Tag


class Special(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, _('Percentage discount')),
        (FIXED, _('Fixed discount')),
    ]

    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=128, blank=False, verbose_name=_('slug'))
    date = models.DateTimeField(default=timezone.now,
                                help_text=_('Date of special offer to be shown.'), verbose_name=_('published'))
    start_date = models.DateTimeField(blank=True, null=True,
                                      help_text=_("""Date to make special offer visible on site.
                                                  Leave this blank to show the special offer immediately."""),
                                      verbose_name=_('start date'))
    deadline = models.DateTimeField(blank=False, null=False,
                                    help_text=_("""Show special offer until this date.
                                                Special offer will appear forever if this field is blank."""),
                                    verbose_name=_('deadline'))
    img = models.ImageField(blank=True, verbose_name=_('image'))
    content = RichTextField(blank=True, verbose_name=_('content'))
    discount = models.BooleanField(default=True, verbose_name=_('discount'))
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=PERCENT, max_length=10, blank=True,
                                     verbose_name=_('discount type'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('discount amount'))
    products = models.ManyToManyField(Product, through='SpecialProduct',
                                      help_text=_('At least 1 product is required.'),
                                      related_name='specials', verbose_name=_('products'))
    tags = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'), verbose_name=_('tags'))
    # total_price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity']
        verbose_name = _('Special')
        verbose_name_plural = _('Specials')

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.deadline and self.start_date >= self.deadline:
            raise ValidationError(_("Deadline must be more than start date"))


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
