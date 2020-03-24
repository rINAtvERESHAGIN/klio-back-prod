from django.contrib import admin

from .models import Basket, BasketProduct, Order, OrderPrivateInfo, OrderDeliveryInfo, OrderPaymentInfo, PromoCode


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class BasketProductInline(admin.TabularInline):
    model = BasketProduct


class BasketAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'get_user', 'active']
    inlines = [
        BasketProductInline,
    ]

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = 'User'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'get_user', 'status', 'step']

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = 'User'


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'activity']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderPrivateInfo, HiddenAdmin)
admin.site.register(OrderDeliveryInfo, HiddenAdmin)
admin.site.register(OrderPaymentInfo, HiddenAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
