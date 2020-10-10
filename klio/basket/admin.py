from django.contrib import admin
from django.urls import reverse, re_path
from django.utils.html import linebreaks, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse

from .models import Basket, BasketProduct, Order, OrderPrivateInfo, OrderDeliveryInfo, OrderPaymentInfo, PromoCode, OrderPaymentB2PInfo
from .utils import export_orders_csv


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class BasketProductInline(admin.TabularInline):
    model = BasketProduct
    fields = ['product', 'quantity', 'price', 'promo_price']
    raw_id_fields = ('product',)


class BasketAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'get_user', 'is_active']
    list_per_page = 50
    inlines = [
        BasketProductInline,
    ]

    def get_user(self, obj):
        return obj.user.__str__()
    get_user.short_description = _('User')


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'received', 'get_user', 'get_email', 'status', 'get_delivery_type', 'get_delivery_price',
                    'is_paid', 'price', 'promo', 'promo_code', 'get_city', 'get_products', 'print_action']
    list_per_page = 25
    list_filter = ['status', 'is_paid', 'promo', 'received']
    search_fields = ['user__first_name', 'user__last_name', 'user__middle_name', 'user__username', 'user__email']
    actions = [export_orders_csv]

    def get_user(self, obj):
        if obj.user:
            return obj.user.__str__()
        if obj.private_info:
            return '{0} {1} (без регистрации)'.format(obj.private_info.last_name, obj.private_info.first_name)
        return _('Anonymous')
    get_user.short_description = _('User')

    def get_email(self, obj):
        if obj.user:
            return obj.user.email
        if obj.private_info:
            return obj.private_info.email
        return None
    get_email.short_description = _('User Email')

    def get_delivery_type(self, obj):
        if obj.delivery_info:
            return obj.delivery_info.get_type_display()
        return None
    get_delivery_type.short_description = _('Delivery')

    def get_delivery_price(self, obj):
        if obj.delivery_info:
            return obj.delivery_info.price
        return None
    get_delivery_price.short_description = _('Delivery price')

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
        if obj.delivery_info:
            return obj.delivery_info.to_city.alternate_names
        return None
    get_city.short_description = _('City')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<order_id>.+)/print/$',
                self.admin_site.admin_view(self.print_form_view),
                name='order-print',
            ),
        ]
        return custom_urls + urls

    def print_action(self, obj):
        return format_html(
            '<a class="grp-button grp-default" href="{}">{}</a>&nbsp;',
            reverse('admin:order-print', args=[obj.pk]),
            _('Print')
        )
    print_action.short_description = _('Print')
    print_action.allow_tags = True

    def print_form_view(self, request, order_id, *args, **kwargs):
        order = self.get_object(request, order_id)
        context = self.admin_site.each_context(request)
        context['order'] = order
        return TemplateResponse(
            request,
            'admin/basket/print_form.html',
            context,
        )


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'start_date', 'deadline', 'activity']
    autocomplete_fields = ['products', 'categories', 'tags']


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderPrivateInfo)
admin.site.register(OrderDeliveryInfo, HiddenAdmin)
admin.site.register(OrderPaymentInfo, HiddenAdmin)
admin.site.register(OrderPaymentB2PInfo, HiddenAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
