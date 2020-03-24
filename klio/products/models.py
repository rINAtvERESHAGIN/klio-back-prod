from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City
from ckeditor.fields import RichTextField

from tags.models import Tag

User = get_user_model()


class Brand(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    logo = models.ImageField()
    description = RichTextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    group = models.PositiveIntegerField(default=0, null=True, editable=False)
    img = models.ImageField()
    description = RichTextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    on_main = models.BooleanField(default=False)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'order', '-group', '-parent__name', 'name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.pk and not self.parent:
            new_base_cat = super(Category, self).save(*args, **kwargs)
            new_base_cat.group = new_base_cat.pk
            return new_base_cat.save()
        if self.pk and not self.parent:
            self.group = self.pk
            return super(Category, self).save(*args, **kwargs)
        self.group = self.parent.group
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        full_name = self.name
        while self.parent:
            parent_name = self.parent.name[:15 - 3] + '...' if len(self.parent.name) > 15 else self.parent.name
            full_name = parent_name + ' / ' + full_name
            self = self.parent
        return full_name

    def get_parent_name(self):
        return self.parent.name


class CategoryCityRating(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)
    rating = models.PositiveIntegerField(default=0, blank=False, null=True)


class Product(models.Model):
    UNIQUE, PARENT, CHILD = 'unique', 'parent', 'child'
    KIND_CHOICES = [
        (UNIQUE, _('Unique product')),
        (PARENT, _('Child product')),
        (CHILD, _('Parent product')),
    ]
    NEW, CALCULATED, NOT_NEW = 'new', 'calculated', 'not_new'
    IS_NEW_CHOICES = [
        (NEW, _('New')),
        (CALCULATED, _('Calculated')),
        (NOT_NEW, _('Not new')),
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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name=_("Parent product"),
                               help_text="Leave blank if this is a unique product "
                                         "(i.e. product does not have children)")
    """ None for child products, they inherit their parent's product type. """
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='products')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    """ Not required for parent products. """
    art = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    properties = models.ManyToManyField('ProductProperty', through='ProductPropertyValue', related_name='products')
    """ Not required for parent products. """
    in_stock = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,
                                   help_text='For parents it will be calculated automatically',
                                   verbose_name=_('In_stock'))
    """ Not required for parent products. """
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    base_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    units = models.CharField(max_length=32, blank=True, verbose_name=_('Units'))
    wholesale_threshold = models.IntegerField(blank=True, null=True)
    wholesale_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    recommended = models.ManyToManyField('self', blank=True)
    """ Leave default for parent products. """
    is_new = models.CharField(max_length=12, choices=IS_NEW_CHOICES, default=CALCULATED)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'product_type', 'order']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False, related_name='images')
    img = models.ImageField()
    label = models.CharField(max_length=64, blank=True)
    order = models.PositiveIntegerField(default=1)
    activity = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


class ProductProperty(models.Model):
    (TEXT, INTEGER, BOOLEAN, FLOAT, RICHTEXT, DATE, DATETIME) = (
        "text", "integer", "boolean", "float", "richtext", "date", "datetime")
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE, _("Date")),
        (DATETIME, _("Datetime")),
    )

    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('Name'))
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=20, verbose_name=_("Type"))
    units = models.CharField(max_length=32, blank=True, verbose_name=_('Units'))
    required = models.BooleanField(default=False, verbose_name=_('Required'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')


class ProductPropertyValue(models.Model):
    prop = models.ForeignKey('ProductProperty', on_delete=models.CASCADE, verbose_name=_('Property'),
                             related_name='values')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='property_values',
                                verbose_name=_('Product'))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)
    value_file = models.FileField(upload_to='products/properties/files', max_length=255, blank=True, null=True)
    value_image = models.ImageField(upload_to='products/properties/images', max_length=255, blank=True, null=True)

    def _get_value(self):
        value = getattr(self, 'value_%s' % self.prop.type)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        attr_name = 'value_%s' % self.prop.type

        setattr(self, attr_name, new_value)
        return

    value = property(_get_value, _set_value)

    class Meta:
        unique_together = ('prop', 'product')
        verbose_name = _('Product property value')
        verbose_name_plural = _('Product property values')

    def __str__(self):
        return self.summary()

    def summary(self):
        """
        Gets a string representation of both the property and it's value,
        used e.g in product summaries.
        """
        return "%s: %s" % (self.prop.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_text property and
        return something appropriate.
        """
        property_name = '_%s_as_text' % self.prop.type
        return getattr(self, property_name, self.value)


class ProductType(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'category', 'name']
        verbose_name = _('Product type')
        verbose_name_plural = _('Product types')


class UserProduct(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.product)
