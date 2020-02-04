from django.contrib import admin

from .models import Basket, Order, PromoCode


class BasketAdmin(admin.ModelAdmin):
    pass


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'activity']


admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(PromoCode, PromoCodeAdmin)
