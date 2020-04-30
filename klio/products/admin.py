from django.contrib import admin
from django.db import models
from django.forms import Textarea

from sale.models import SpecialProduct
from .models import (Brand, Category, Product, ProductImage, ProductProperty, ProductPropertyValue,
                     ProductType, Unit)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'activity']
    list_editable = ['order', 'activity']
    list_filter = ['activity']
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_parent', 'group', 'order', 'on_main', 'activity']
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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'kind', 'category', 'art', 'in_stock', 'price', 'order', 'modified',
                    'activity']
    list_editable = ['in_stock', 'price', 'order', 'activity']
    search_fields = ['name', 'art']
    list_filter = ['kind', 'product_type', 'activity']
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ['parent', 'category', 'product_type', 'tags', 'units', 'recommended']
    inlines = [
        ProductPropertyValueInline,
        ProductImageInline,
        SpecialProductInline,
    ]
    save_on_top = True

    class Media:
        css = {
            'all': ('../static/css/style.css',)
        }

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['recommended'].queryset = Product.objects.exclude(id__exact=obj.id)
        return form


class ProductAttrAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'activity']
    list_editable = ['activity']


class ProductPropertyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['__str__', 'type', 'units']


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
