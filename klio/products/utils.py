from django.http import HttpResponse


def export_product_categories_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Артикул"),
        smart_str(u"Категория"),
    ])
    for obj in queryset:

        writer.writerow([
            smart_str(obj.art),
            smart_str(obj.category.id),
        ])
    return response


export_product_categories_csv.short_description = u"Экспорт категорий товаров (CSV)"
