from django.contrib import admin
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
    list_display = ['__str__', 'created', 'get_user', 'get_email', 'status', 'is_paid']
    list_filter = ['status']

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = _('User')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = _('User Email')

    # def get_sum(self, obj):
    #     return
    # get_sum.short_description = _('Sum')
    #
    # def get_positions(self, obj):
    #     return
    # get_positions.short_description = _('Positions')
    #
    # def get_city(self, obj):
    #     return
    # get_city.short_description = _('City')
    #
    # def get_country(self, obj):
    #     return
    # get_country.short_description = _('Country')


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'activity']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderPrivateInfo)
admin.site.register(OrderDeliveryInfo, HiddenAdmin)
admin.site.register(OrderPaymentInfo, HiddenAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
