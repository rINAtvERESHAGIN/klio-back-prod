from django.contrib import admin

from .models import User, UserPhone


class UserPhoneInline(admin.TabularInline):
    model = UserPhone


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'registered', 'city', 'email', 'get_phones', 'activity']
    list_filter = ['activity']
    inlines = [
        UserPhoneInline,
    ]

    def get_phones(self, obj):
        return "; ".join([phone.__str__() for phone in obj.phones.filter(activity=True)])


admin.site.register(User, UserAdmin)
