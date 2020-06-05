from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


def export_orders_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Заказ"),
        smart_str(u"Получено"),
        smart_str(u"Покупатель"),
        smart_str(u"Email покупателя"),
        smart_str(u"Статус"),
        smart_str(u"Доставка"),
        smart_str(u"Стоимость доставки"),
        smart_str(u"Оплачено"),
        smart_str(u"Цена"),
        smart_str(u"Промо"),
        smart_str(u"Промокод"),
        smart_str(u"Город"),
        smart_str(u"Товары"),
    ])
    for obj in queryset:

        result = ''
        basket_products = obj.basket.inside.all()
        for bp in basket_products:
            price = bp.promo_price if bp.promo_price else bp.price if bp.price else 0
            line = '{0} {1}, цена: {2}, кол-во: {3}, сумма: {4};'.format(
                bp.product.art, bp.product.name, price, bp.quantity, price * bp.quantity
            )
            result += line

        try:
            delivery_price = obj.delivery_info.price if obj.delivery_info.price is not None else '-'
        except AttributeError:
            delivery_price = '-'

        writer.writerow([
            smart_str(obj.__str__()),
            smart_str(obj.received.strftime('%Y-%m-%d %H:%M') if obj.received else '-'),
            smart_str(obj.user if obj.user else (
                '{0} {1} (без регистрации)'.format(obj.private_info.last_name, obj.private_info.first_name)
            ) if obj.private_info else '-'),
            smart_str(obj.user.email if obj.user else obj.private_info.email if obj.private_info else '-'),
            smart_str(obj.get_status_display()),
            smart_str(obj.delivery_info.get_type_display() if obj.delivery_info else '-'),
            smart_str(delivery_price),
            smart_str(_('Yes') if obj.is_paid else _('No')),
            smart_str(obj.price if obj.price else '-'),
            smart_str(_('Yes') if obj.promo else _('No')),
            smart_str(obj.promo_code),
            smart_str(obj.delivery_info.to_city.alternate_names if obj.delivery_info else '-'),
            smart_str(result),
        ])
    return response


export_orders_csv.short_description = u"Экспорт выбранных заказов (CSV)"
