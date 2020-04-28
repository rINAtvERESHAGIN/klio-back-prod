from django.contrib import admin
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Basket, BasketProduct, Order, OrderPrivateInfo, OrderDeliveryInfo, OrderPaymentInfo, PromoCode


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class BasketProductInline(admin.TabularInline):
    model = BasketProduct


class BasketAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'get_user', 'is_active']
    inlines = [
        BasketProductInline,
    ]

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = _('User')


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'received', 'get_user', 'get_email', 'status', 'get_delivery_type', 'is_paid', 'price',
                    'promo', 'promo_code', 'get_city', 'get_products']
    list_filter = ['status', 'is_paid', 'promo']

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = _('User')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = _('User Email')

    def get_delivery_type(self, obj):
        return obj.delivery_info.get_type_display()
    get_delivery_type.short_description = _('Delivery')

    def get_products(self, obj):
        result = ''
        for bp in obj.basket.inside.all():
            price = bp.promo_price if bp.promo_price else bp.price if bp.price else 0
            line = linebreaks('<strong>{0}</strong> {1}, цена: {2}, кол-во: {3}, сумма: {4}<br />'.format(
                bp.product.art, bp.product.name, price, bp.quantity, price * bp.quantity
            ))
            result += line
        return mark_safe(result)

    get_products.short_description = _('Products')

    def get_city(self, obj):
        return obj.delivery_info.to_city
    get_city.short_description = _('City')


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'activity']
    autocomplete_fields = ['products', 'categories', 'tags']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderPrivateInfo)
admin.site.register(OrderDeliveryInfo, HiddenAdmin)
admin.site.register(OrderPaymentInfo, HiddenAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
