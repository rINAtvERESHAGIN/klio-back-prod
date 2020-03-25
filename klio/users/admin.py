from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserPhone


class UserPhoneInline(admin.TabularInline):
    model = UserPhone


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets, (
            _('Additional data'), {'fields': ('middle_name', 'birthday', 'country', 'city', 'address', 'avatar')},
        ),
    )
    list_display = ['__str__', 'registered', 'city', 'email', 'get_phones', 'activity']
    list_filter = ['activity']
    inlines = [
        UserPhoneInline,
    ]

    def get_phones(self, obj):
        return "; ".join([phone.__str__() for phone in obj.phones.filter(activity=True)])


admin.site.register(User, CustomUserAdmin)
