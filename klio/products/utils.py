from django.http import HttpResponse


def export_products_names_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=products_names.csv'
    writer = csv.writer(response, csv.excel, delimiter=';')
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Артикул"),
        smart_str(u"Наименование"),
    ])
    for obj in queryset:

        writer.writerow([
            smart_str(obj.art),
            smart_str(obj.name),
        ])
    return response


export_products_names_csv.short_description = u"Экспорт наименований товаров (CSV)"
