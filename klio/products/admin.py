import csv
import re
from decimal import Decimal

from django.contrib import admin
from django.db import models
from django.db import IntegrityError
from django.forms import FileField, Form, Textarea
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from slugify import slugify

from sale.models import SpecialProduct
from .forms import ProductForm
from .models import (Brand, Category, Product, ProductImage, ProductProperty, ProductPropertyValue,
                     ProductType, Unit)
from .utils import export_products_names_csv

CYRILLIC = [
    (u'ё', u'yo'),
    (u'Ё', u'yo'),
    (u'я', u'ya'),
    (u'Я', u'ya'),
    (u'х', u'h'),
    (u'Х', u'h'),
    (u'щ', u'sh'),
    (u'Щ', u'sh'),
    (u'ю', u'yu'),
    (u'Ю', u'yu'),
]


class BrandAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'activity']
    list_editable = ['order', 'activity']
    list_filter = ['activity']
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_parent', 'group', 'order', 'on_main', 'activity']
    list_per_page = 25
    list_editable = ['order', 'on_main', 'activity']
    search_fields = ['name']
    list_filter = ['on_main', 'activity']
    prepopulated_fields = {"slug": ("name",)}

    def get_parent(self, obj):
        return obj.parent.name if obj.parent else '-'

    get_parent.short_description = 'Parent'
    get_parent.admin_order_field = 'parent__name'


class ProductPropertyValueInline(admin.TabularInline):
    model = ProductPropertyValue
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class SpecialProductInline(admin.TabularInline):
    model = SpecialProduct


class CsvImportForm(Form):
    csv_file = FileField()


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['__str__', 'slug', 'kind', 'get_type', 'get_categories', 'art', 'in_stock', 'price', 'order',
                    'modified', 'activity']
    list_per_page = 25
    list_editable = ['slug', 'in_stock', 'price', 'order', 'activity']
    search_fields = ['name', 'slug', 'art']
    list_filter = ['kind', 'product_type', 'activity']
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ['parent', 'categories', 'product_type', 'tags', 'units', 'recommended']
    inlines = [
        ProductPropertyValueInline,
        ProductImageInline,
        SpecialProductInline,
    ]
    actions = [export_products_names_csv]
    save_on_top = True
    change_list_template = "products_changelist.html"

    class Media:
        css = {
            'all': ('../static/css/style.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
            path('update-names/', self.update_names_csv),
            path('update-prices/', self.update_prices_csv),
            path('update-properties/', self.update_properties_csv),
            # path('update-category-content/', self.update_category_csv),
            # path('move-category-fk-m2m/', self.categories_FK_to_M2M_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';')
            for row in csv_data:
                categories_str, name, art, description, price, images_str = row

                categories_names = re.split(r',(?=")', categories_str)
                parent_category = None
                for category_name in categories_names:
                    if category_name.startswith('"') and category_name.endswith('"'):
                        category_name = category_name[1:-1]
                    category_slug = slugify(category_name, replacements=CYRILLIC)
                    same_name_categories = Category.objects.filter(slug__startswith=category_slug)

                    # Find exact match
                    category = same_name_categories.filter(slug=category_slug, parent=parent_category).first()

                    if not category:

                        # Find not strict match in same parent (False for root categories!)
                        category = same_name_categories.filter(parent=parent_category, parent__isnull=False).first()
                        if category:
                            try:
                                int(category.slug[-1])
                            except ValueError:
                                category = None
                        if not category:

                            # Find match from other parent categories
                            in_other_parent = same_name_categories.filter(slug=category_slug).exists()
                            if in_other_parent:
                                if same_name_categories.count() > 0:
                                    category_slug = "{0}{1}".format(category_slug, same_name_categories.count())

                    if not category:
                        category = Category.objects.create(
                            name=category_name, slug=category_slug, parent=parent_category
                        )
                    parent_category = category

                product = Product.objects.filter(art=art)
                if product:
                    try:
                        product.update(categories=parent_category, name=name, description=description,
                                       price=Decimal(price.replace(" ", "")))
                    except IntegrityError:
                        prod_slug = product.values_list('slug', flat=True)[0]
                        prod_count = Product.objects.filter(slug=prod_slug).count()
                        product.update(slug='{0}{1}'.format(prod_slug, prod_count), name=name, description=description,
                                       categories=parent_category, price=Decimal(price.replace(" ", "")))
                    product = product.first()

                else:
                    count = Product.objects.filter(slug__startswith=slugify(name, replacements=CYRILLIC),
                                                   categories=parent_category).count()
                    count = count if count else ''
                    prod_slug = '{0}{1}'.format(slugify(name, replacements=CYRILLIC), count)
                    product = Product.objects.create(name=name, slug=prod_slug,
                                                     categories=parent_category, kind=Product.UNIQUE, art=art,
                                                     description=description,
                                                     price=Decimal(price.replace(" ", "")))

                images_names = images_str.split(',')
                for index, image_name in enumerate(images_names):
                    prod_img, created = ProductImage.objects.get_or_create(product=product,
                                                                           img='products/{0}'.format(image_name))
                    prod_img.label = '{0} - Изображение #{1}'.format(product.name, index + 1)
                    prod_img.save()

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def update_names_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';')
            next(csv_data)
            for row in csv_data:
                art, name = row
                slug = slugify(name, replacements=CYRILLIC)
                try:
                    product = Product.objects.filter(art=art)
                except ValueError:
                    continue
                if product:
                    if product.first().name != name:
                        try:
                            product.update(name=name, slug=slug)
                        except IntegrityError:
                            prod_count = Product.objects.filter(slug__startswith=slug).count()
                            product.update(slug='{0}-{1}'.format(slug, prod_count + 1), name=name)

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def update_prices_csv(self, request):
        """
        Loads new data about products amount and prices.
        The uploaded file should be of the next format:

        articule;amount;price

        accepted amount format: 5,00
        accepted price format: 150,00

        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';')
            for row in csv_data:
                art, in_stock, price = row
                try:
                    Product.objects.filter(art=art).update(price=Decimal(price.replace(',', '.')),
                                                           in_stock=Decimal(in_stock.replace(',', '.')))
                except ValueError:
                    continue

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def update_category_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';')
            for row in csv_data:
                category1, category2, category3, category4, art, content, brand_name = row

                category_list = [c for c in [category1, category2, category3, category4] if c != '']
                parent_category = None
                for category_name in category_list:
                    category_slug = slugify(category_name, replacements=CYRILLIC)
                    same_name_categories = Category.objects.filter(slug__startswith=category_slug)

                    # Find exact match
                    category = same_name_categories.filter(slug=category_slug, parent=parent_category).first()

                    if not category:

                        # Find not strict match in same parent (False for root categories!)
                        category = same_name_categories.filter(parent=parent_category, parent__isnull=False).first()
                        if category:
                            try:
                                int(category.slug[-1])
                            except ValueError:
                                category = None
                        if not category:

                            # Find match from other parent categories
                            in_other_parent = same_name_categories.filter(slug=category_slug).exists()
                            if in_other_parent:
                                if same_name_categories.count() > 0:
                                    category_slug = "{0}{1}".format(category_slug, same_name_categories.count())

                    if not category:
                        category = Category.objects.create(
                            name=category_name, slug=category_slug, parent=parent_category
                        )
                    parent_category = category

                brand_slug = slugify(brand_name, replacements=CYRILLIC)
                brand = Brand.objects.filter(slug=brand_slug).first()
                if not brand:
                    brand = Brand.objects.create(name=brand_name, slug=brand_slug, activity=False)

                try:
                    if content:
                        try:
                            Product.objects.filter(art=art).update(categories=parent_category, description=content,
                                                                   brand=brand)
                        except IntegrityError:
                            prod_slug = Product.objects.filter(art=art).values_list('slug', flat=True)[0]
                            prod_count = Product.objects.filter(slug=prod_slug).count()
                            Product.objects.filter(art=art).update(slug='{0}{1}'.format(prod_slug, prod_count),
                                                                   categories=parent_category, description=content,
                                                                   brand=brand)

                    else:
                        try:
                            Product.objects.filter(art=art).update(categories=parent_category, brand=brand)
                        except IntegrityError:
                            prod_slug = Product.objects.filter(art=art).values_list('slug', flat=True)
                            prod_count = Product.objects.filter(slug=prod_slug)
                            Product.objects.filter(art=art).update(slug='{0}{1}'.format(prod_slug, prod_count),
                                                                   categories=parent_category, brand=brand)
                except ValueError:
                    continue

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def update_properties_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=';')
            header = next(csv_data)
            props_names = header[1:]
            for row in csv_data:
                art, props_values = row[0], row[1:]

                if not props_values or not art:
                    continue

                try:
                    product_id = Product.objects.filter(art=art).values_list('id', flat=True)[0]
                except IndexError:
                    continue

                for index, pv in enumerate(props_values):

                    if not pv:
                        continue

                    if '.' in pv:
                        try:
                            pv = float(pv)
                        except ValueError:
                            value_type, interval = 'text', None
                        else:
                            value_type, interval = 'float', 0.01

                    else:
                        try:
                            pv = int(pv)
                        except ValueError:
                            value_type, interval = 'text', None
                        else:
                            value_type, interval = 'integer', 1

                    prop_slug = slugify(props_names[index], replacements=CYRILLIC)
                    try:
                        prop_id = ProductProperty.objects.filter(slug=prop_slug).values_list('id', flat=True)[0]
                    except IndexError:
                        prop = ProductProperty.objects.create(name=props_names[index], slug=prop_slug,
                                                              interval=interval, type=value_type)
                        prop_id = prop.id

                    value, is_new_value = ProductPropertyValue.objects.get_or_create(product_id=product_id,
                                                                                     prop_id=prop_id)
                    if value_type == 'integer':
                        value.value_integer = pv
                    if value_type == 'float':
                        value.value_float = pv
                    if value_type == 'text':
                        value.value_text = pv

                    value.save()

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def categories_FK_to_M2M_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines(), delimiter=',')
            for row in csv_data:
                art, category_id = row
                try:
                    product = Product.objects.filter(art=art).first()
                    if product:
                        product.categories.add(category_id)
                except ValueError:
                    continue

            self.message_user(request, _("CSV file was successfully uploaded."))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['recommended'].queryset = Product.objects.exclude(id__exact=obj.id)
        return form

    def get_categories(self, obj):
        return ', '.join(c.name for c in obj.get_categories())

    get_categories.short_description = _('Categories')
    get_categories.admin_order_field = 'categories__name'

    def get_type(self, obj):
        return obj.get_product_type()

    get_type.short_description = _('Product Type')
    get_type.admin_order_field = 'product_type__name'


class ProductPropertyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['__str__', 'slug', 'type', 'units', 'interval', 'required']
    prepopulated_fields = {"slug": ("name",)}


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    autocomplete_fields = ['properties']


class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductProperty, ProductPropertyAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Unit, UnitAdmin)
