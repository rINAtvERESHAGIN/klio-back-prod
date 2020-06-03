from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'),
                                  help_text=_('Leave blank to fill automatically with name.'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'),
                                        help_text=_('Leave blank to fill automatically with name.'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'),
                                     help_text=_('Leave blank to fill automatically with words taken from name.'))
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=128, verbose_name=_('slug'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('parent'))
    group = models.PositiveIntegerField(default=0, null=True, editable=False, verbose_name=_('group'))
    img = models.ImageField(blank=True, verbose_name=_('image'), upload_to='categories')
    description = RichTextField(blank=True, verbose_name=_('description'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    on_main = models.BooleanField(default=False, verbose_name=_('on main'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order', '-group', '-parent__name', 'name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.name
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.name.split())

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
        (PARENT, _('Parent product')),
        (CHILD, _('Child product')),
    ]
    NEW, CALCULATED, NOT_NEW = 'new', 'calculated', 'not_new'
    IS_NEW_CHOICES = [
        (NEW, _('New')),
        (CALCULATED, _('Calculated')),
        (NOT_NEW, _('Not new')),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'),
                                  help_text=_('Leave blank to fill automatically with name.'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'),
                                        help_text=_('Leave blank to fill automatically with name.'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'),
                                     help_text=_('Leave blank to fill automatically with words taken from name.'))
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=128, blank=False, verbose_name=_('slug'))
    description = RichTextField(blank=True, verbose_name=_('description'))

    """
    There's 3 kinds of products:

    - A unique product does not have any children or parent.
    - A child product. All child products have a parent product. They're a
      specific version of the parent.
    - A parent product. It essentially represents a set of products.
    """
    kind = models.CharField(max_length=7, choices=KIND_CHOICES, default=UNIQUE, verbose_name=_('kind'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name=_("Parent product"),
                               help_text=_("Leave blank if this is a unique product"))
    """ None for child products, they inherit their parent's product type. """
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='products', verbose_name=_('product type'),
                                     help_text=_("Choose the product type. Properties will be inherited after saving."
                                                 "Click 'Save & Continue' button."))
    """ None for child products, they inherit their parent's product type. """
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name=_('category'), help_text=_('Choose the most detailed category'))
    """ None for child products, they inherit their parent's product type. """
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('brand'),
                              help_text=_("If this field is empty for child product, Brand will be inherited from"
                                          "parent."))
    """ Not required for parent products. """
    art = models.IntegerField(unique=True, blank=True, null=True, verbose_name=_('vendor code'),
                              help_text=_("Do not set article number for parent product."))
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name=_('tags'),
                                  help_text=_("If not provided for child product, tags will be inherited from parent."))
    properties = models.ManyToManyField('ProductProperty', through='ProductPropertyValue', related_name='products',
                                        verbose_name=_('properties'),
                                        help_text=_("Properties should be set on Product Type level, but you can"
                                                    "provide single-product property as well."))
    """ Not required for parent products. """
    in_stock = models.DecimalField(default=0, blank=False, null=True, max_digits=10, decimal_places=4,
                                   help_text=_('For parents it will be calculated automatically'),
                                   verbose_name=_('In_stock'))
    units = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
                              verbose_name=_('units'))
    """ Not required for parent products. """
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name=_('price'),
                                help_text=_("Do not set the price on a parent product."))
    base_amount = models.DecimalField(blank=True, null=True, default=1, max_digits=10, decimal_places=4,
                                      verbose_name=_('base amount'),
                                      help_text=_("Used for correct displaying and calculating the amount and the "
                                                  "price of a product."))
    wholesale_threshold = models.IntegerField(blank=True, null=True, verbose_name=_('wholesale threshold'))
    wholesale_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                          verbose_name=_('wholesale price'))
    recommended = models.ManyToManyField('self', blank=True, verbose_name=_('recommended'),
                                         help_text=_('Choose only unique or child products.'))
    """ Leave default for parent products. """
    is_new = models.CharField(max_length=12, choices=IS_NEW_CHOICES, default=CALCULATED, verbose_name=_('is new'),
                              help_text=_("If set to 'Calculated', the product will be valued as new for 2 months from"
                                          "the date of adding"))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'product_type', 'order']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        unique_together = ('category', 'slug')

    def __str__(self):
        return self.name

    def clean(self):
        # General check
        if self.in_stock:
            if self.in_stock < 0:
                raise ValidationError(_('Amount in stock can not be negative.'))
        if self.price:
            if self.price < 0:
                raise ValidationError(_('Product price can not be negative.'))

        getattr(self, '_clean_%s' % self.kind)()

    def _clean_unique(self):
        if self.parent:
            raise ValidationError(_('Unique product should not have a parent'))
        if not self.category:
            raise ValidationError(_('Unique product should contain a category'))
        if not self.product_type:
            raise ValidationError(_('Unique product should contain a product type'))
        if not self.art:
            raise ValidationError(_('Unique product should contain an article number'))
        if not self.price:
            raise ValidationError(_('Unique product should contain a price'))
        if not self.base_amount:
            raise ValidationError(_('Unique product should contain a base amount'))

    def _clean_parent(self):
        if self.parent:
            raise ValidationError(_('Parent product should not have a parent'))
        if not self.category:
            raise ValidationError(_('Parent product should contain a category'))
        if not self.product_type:
            raise ValidationError(_('Parent product should contain a product type'))
        if self.art:
            raise ValidationError(_('Parent product should not have an article number'))
        if self.in_stock > 0:
            raise ValidationError(_('Parent product should not have a number of items in stock. Set it to 0.'))
        if self.price:
            raise ValidationError(_('Parent product should not have a price'))
        if not self.base_amount:
            raise ValidationError(_('Parent product should contain a base amount'))

    def _clean_child(self):
        if not self.parent:
            raise ValidationError(_('Child product must have a parent'))
        if not self.parent.product_type:
            raise ValidationError(_('Selected parent is not valid - no product type found.'))
        if self.category:
            raise ValidationError(_('Child product inherit its parent category. Leave it blank or choose parents.'))
        if self.product_type:
            raise ValidationError(_('Child product inherit its parent product type'))
        if self.brand:
            raise ValidationError(_('Child product inherit its parent brand'))
        if self.units:
            raise ValidationError(_('Child product inherit its parent units'))
        if self.base_amount:
            raise ValidationError(_('Child product inherit its parent base amount'))
        if not self.price:
            raise ValidationError(_('Child product must have a price'))
        if not self.art:
            raise ValidationError(_('Child product must have an article number'))

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.name
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.name.split())
        super(Product, self).save(*args, **kwargs)
        for prop in self.get_all_properties():
            product_property, created = ProductPropertyValue.objects.get_or_create(product=self, prop=prop)
            if self.is_child and created:
                product_property.value = self.parent.get_value_by_property(prop).value
                product_property.save()

    @property
    def is_unique(self):
        return self.kind == self.UNIQUE

    @property
    def is_parent(self):
        return self.kind == self.PARENT

    @property
    def is_child(self):
        return self.kind == self.CHILD

    def get_brand(self):
        return self.parent.brand if self.is_child else self.brand

    def get_base_amount(self):
        return self.parent.base_amount if self.is_child else self.base_amount

    def get_category(self):
        return self.parent.category if self.is_child else self.category

    def get_product_type(self):
        return self.parent.product_type if self.is_child else self.product_type
    get_product_type.short_description = _("Product type")

    def get_units(self):
        return self.parent.units if self.is_child else self.units

    def get_values(self):
        return self.property_values.all()

    def get_value_by_property(self, prop):
        return self.get_values().filter(prop=prop).first()

    def get_actual_value_by_property_slug(self, prop_name):
        if self.get_values().filter(prop__slug=prop_name).first():
            return self.get_values().filter(prop__slug=prop_name).first().value
        return 0

    def get_all_properties(self):
        if self.get_product_type():
            return self.get_product_type().properties.all()
        return []


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, null=False, related_name='images',
                                verbose_name=_('product'))
    img = models.ImageField(verbose_name=_('image'), upload_to='products')
    label = models.CharField(max_length=128, blank=True, verbose_name=_('label'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')


class ProductProperty(models.Model):
    (TEXT, INTEGER, BOOLEAN, FLOAT) = (
        "text", "integer", "boolean", "float")
    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        # (DATETIME, _("Datetime")),
    )

    name = models.CharField(max_length=128, blank=False, null=False, unique=True, verbose_name=_('name'))
    slug = models.SlugField(max_length=128, blank=False, null=False, unique=True, verbose_name=_('slug'),
                            help_text=_('Slug is used for filtration purposes. Use only symbols [a-z,0-9,-]'))
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=20, verbose_name=_("type"))
    units = models.ForeignKey('Unit', on_delete=models.SET_NULL, null=True, blank=True, related_name='properties',
                              verbose_name=_('units'))
    interval = models.DecimalField(blank=True, null=True, max_digits=6, verbose_name=_('property interval'),
                                   decimal_places=3,
                                   help_text=_("Accuracy between two neighbour values during searching. Used for "
                                               "integer or float types only."))
    required = models.BooleanField(default=False, verbose_name=_('required'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def clean(self):
        if self.type in ['integer', 'float'] and not self.interval:
            raise ValidationError(_('Integer and float properties should have interval.'))
        if '_' in self.slug:
            raise ValidationError(_('Slug can not contain _ symbol.'))

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    def _validate_text(self, value):
        if not isinstance(value, str):
            raise ValidationError(_("Must be str"))

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    # def _validate_datetime(self, value):
    #     if not isinstance(value, datetime):
    #         raise ValidationError(_("Must be a datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))


class ProductPropertyValue(models.Model):
    prop = models.ForeignKey('ProductProperty', on_delete=models.CASCADE, verbose_name=_('property'),
                             related_name='values')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='property_values',
                                verbose_name=_('product'))

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.NullBooleanField(_('Boolean'), blank=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    # value_datetime = models.DateTimeField(_('DateTime'), blank=True, null=True, db_index=True)

    class Meta:
        unique_together = ('prop', 'product')
        verbose_name = _('Product property value')
        verbose_name_plural = _('Product property values')

    def _get_value(self):
        return getattr(self, 'value_%s' % self.prop.type)

    def _set_value(self, new_value):
        attr_name = 'value_%s' % self.prop.type
        setattr(self, attr_name, new_value)
        return

    value = property(_get_value, _set_value)

    def summary(self):
        """
        Gets a string representation of both the attribute and it's value,
        used e.g in product summaries.
        """
        return "%s: %s" % (self.prop.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the attribute's value.
        """
        property_name = '_%s_as_text' % self.prop.type
        return getattr(self, property_name, self.value)

    def clean(self):
        if self.prop.required and not self.product.is_child and not self.value:
            raise ValidationError(_("Value") + self.prop.name + _('is required'))


class ProductType(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    properties = models.ManyToManyField('ProductProperty', related_name='product_types', verbose_name=_('properties'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
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
