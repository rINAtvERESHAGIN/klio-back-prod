from django.contrib import admin


from .models import Special, SpecialProduct


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class SpecialProductInline(admin.TabularInline):
    model = SpecialProduct
    autocomplete_fields = ['product']
    extra = 0


class SpecialAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'discount_type', 'discount_amount', 'start_date', 'deadline', 'activity']
    list_editable = ['activity']
    autocomplete_fields = ['tags']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        SpecialProductInline,
    ]


admin.site.register(Special, SpecialAdmin)
admin.site.register(SpecialProduct, HiddenAdmin)
