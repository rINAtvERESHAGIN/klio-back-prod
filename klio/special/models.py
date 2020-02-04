from django.db import models

from products.models import Category, Product


class Special(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, 'Percentage discount'),
        (FIXED, 'Fixed discount'),
    ]

    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    img = models.ImageField()
    content = models.TextField()
    discount = models.BooleanField(default=False)
    discount_type = models.CharField(choices=DISCOUNT_TYPES, max_length=10, blank=True)
    discount_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    total_price_min = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SpecialCategory(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, 'Percentage discount'),
        (FIXED, 'Fixed discount'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    special = models.ForeignKey('Special', on_delete=models.CASCADE, blank=False, null=False)
    discount = models.BooleanField(default=False)
    discount_type = models.CharField(choices=DISCOUNT_TYPES, max_length=10, blank=True)
    discount_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)


class SpecialProduct(models.Model):
    special = models.ForeignKey('Special', on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    discount_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
