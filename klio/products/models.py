from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City
from ckeditor.fields import RichTextField

from tags.models import Tag

User = get_user_model()


class Brand(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    logo = models.ImageField(verbose_name=_('logo'), upload_to='brands')
    description = RichTextField(blank=True, verbose_name=_('description'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('parent'))
    group = models.PositiveIntegerField(default=0, null=True, editable=False, verbose_name=_('group'))
    img = models.ImageField(verbose_name=_('image'), upload_to='categories')
    description = RichTextField(blank=True, verbose_name=_('description'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    on_main = models.BooleanField(default=False, verbose_name=_('on main'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order', '-group', '-parent__name', 'name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.pk and not self.parent:
            super(Category, self).save(*args, **kwargs)
            self.group = self.pk
            return self.save()
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
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False,
                                 verbose_name=_('category'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('city'))
    rating = models.PositiveIntegerField(default=0, blank=False, null=True, verbose_name=_('rating'))


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

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    description = RichTextField(blank=True, verbose_name=_('description'))

    """
    There's 3 kinds of products:

    - A unique product does not have any children or parent.
    - A child product. All child products have a parent product. They're a
      specific version of the parent.
    - A parent product. It essentially represents a set of products.
    """
    kind = models.CharField(max_length=7, choices=KIND_CHOICES, verbose_name=_('kind'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name=_("Parent product"),
                               help_text="Leave blank if this is a unique product "
                                         "(i.e. product does not have children)")
    """ None for child products, they inherit their parent's product type. """
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='products', verbose_name=_('product type'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name=_('category'))
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('brand'))
    """ Not required for parent products. """
    art = models.IntegerField(blank=True, null=True, verbose_name=_('vendor code'))
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name=_('tags'))
    properties = models.ManyToManyField('ProductProperty', through='ProductPropertyValue', related_name='products',
                                        verbose_name=_('properties'))
    """ Not required for parent products. """
    in_stock = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,
                                   help_text='For parents it will be calculated automatically',
                                   verbose_name=_('In_stock'))
    units = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
                              verbose_name=_('units'))
    """ Not required for parent products. """
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name=_('price'))
    base_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4,
                                      verbose_name=_('base amount'))
    wholesale_threshold = models.IntegerField(blank=True, null=True, verbose_name=_('wholesale threshold'))
    wholesale_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                          verbose_name=_('wholesale price'))
    recommended = models.ManyToManyField('self', blank=True, verbose_name=_('recommended'))
    """ Leave default for parent products. """
    is_new = models.CharField(max_length=12, choices=IS_NEW_CHOICES, default=CALCULATED, verbose_name=_('is new'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'product_type', 'order']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False, related_name='images',
                                verbose_name=_('product'))
    img = models.ImageField(verbose_name=_('image'), upload_to='products')
    label = models.CharField(max_length=64, blank=True, verbose_name=_('label'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

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

    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('name'))
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=20, verbose_name=_("type"))
    units = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True, blank=True, related_name='properties',
                              verbose_name=_('units'))
    required = models.BooleanField(default=False, verbose_name=_('required'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')


class ProductPropertyValue(models.Model):
    prop = models.ForeignKey('ProductProperty', on_delete=models.CASCADE, verbose_name=_('property'),
                             related_name='values')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='property_values',
                                verbose_name=_('product'))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_richtext = models.TextField(_('Richtext'), blank=True, null=True)
    value_date = models.DateField(_('Date'), blank=True, null=True, db_index=True)
    value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)
    value_file = models.FileField(upload_to='products/properties/files', max_length=255, blank=True, null=True,
                                  verbose_name=_('file'))
    value_image = models.ImageField(upload_to='products/properties/images', max_length=255, blank=True, null=True,
                                    verbose_name=_('image'))

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
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False,
                                 verbose_name=_('category'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'category', 'name']
        verbose_name = _('Product type')
        verbose_name_plural = _('Product types')


class Unit(models.Model):
    name = models.CharField(max_length=32, blank=True, verbose_name=_('name'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')

    def __str__(self):
        return self.name


class UserProduct(models.Model):
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('added'))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False,
                                verbose_name=_('product'), related_name='selected_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('user'),
                             related_name='favorites')

    def __str__(self):
        return '{0} - {1}'.format(self.user, self.product)
