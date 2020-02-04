from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from users.models import User


class Brand(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    description = RichTextField(blank=True)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    img = models.ImageField()
    description = RichTextField(blank=True)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIQUE, PARENT, CHILD = 'unique', 'parent', 'child'
    KIND_CHOICES = [
        (UNIQUE, 'Unique product'),
        (PARENT, 'Child product'),
        (CHILD, 'Parent product'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    description = RichTextField(blank=False)

    """
    There's 3 kinds of products:

    - A unique product does not have any children or parent.
    - A child product. All child products have a parent product. They're a
      specific version of the parent.
    - A parent product. It essentially represents a set of products.
    """
    kind = models.CharField(max_length=7, choices=KIND_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, null=False)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=False)
    art = models.IntegerField(blank=False)
    attr = models.ManyToManyField('ProductAttr', through='ProductAttrValue')
    property = models.ManyToManyField('Property', through='ProductProperty')
    in_stock = models.DecimalField(blank=False, null=True, max_digits=10, decimal_places=4)
    price = models.DecimalField(blank=False, null=False, max_digits=10, decimal_places=2)
    wholesale_threshold = models.IntegerField(blank=True)
    wholesale_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(blank=True, max_digits=10, decimal_places=2)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductAttr(models.Model):
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE, null=False)
    property = models.ForeignKey('Property', on_delete=models.CASCADE, null=False)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)


class ProductAttrValue(models.Model):
    attr = models.ForeignKey('ProductAttr', on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False)
    value = models.CharField(max_length=64, blank=False, null=False)


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False)
    img = models.ImageField()
    label = models.CharField(max_length=64, blank=True)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)


class ProductProperty(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False)
    property = models.ForeignKey('Property', on_delete=models.CASCADE, null=False)
    value = models.CharField(max_length=64, blank=False)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)


class ProductType(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (DATETIME, _("Datetime")),
    )

    name = models.CharField(max_length=64, blank=False, null=False)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=20, verbose_name=_("Type"))
    units = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name


class UserProduct(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.product)
